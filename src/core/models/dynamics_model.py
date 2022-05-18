import numpy as np
from core.models.model import EnvironmentModel
from core.models.derived_models import DerivedStateModel
from typing import Dict, Any
from core.state import State, StateTime


class InertiaModel(DerivedStateModel):
    def evaluate(self, state: State) -> Dict[str, Any]:
        fill_frac = state.fill_frac

        dcm = np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]], dtype=np.int32)
        dcmT = np.transpose(dcm)

        # Inertia tensor when full. Structure is:
        # [[Ixx, Ixy, Ixz],
        #  [Iyx, Iyy, Iyz],
        #  [Izx, Izy, Izz]].
        # Units are (kg * m^2).
        idf = (
            np.array(
                [
                    [933513642.20, 260948256.18, 430810000.30],
                    [260948256.18, 1070855457.07, 387172545.62],
                    [430810000.30, 387172545.62, 629606813.62],
                ],
                dtype=np.float64,
            )
            * 1e-9
        )
        idf_b = np.matmul(np.matmul(dcm, idf), dcmT)

        # Inertia tensor at 125 mL. Structure is:
        # [[Ixx, Ixy, Ixz],
        #  [Iyx, Iyy, Iyz],
        #  [Izx, Izy, Izz]].
        # Units are (kg * m^2).
        idi = (
            np.array(
                [
                    [855858994.14, 229481961.55, 377087149.13],
                    [229481961.55, 963124288.81, 353943859.15],
                    [377087149.13, 353943859.15, 559805590.96],
                ],
                dtype=np.float64,
            )
            * 1e-9
        )
        idi_b = np.matmul(np.matmul(dcm, idi), dcmT)

        # Determine inertia tensor for Oxygen via linear interpolation as a function of fill
        # fraction.

        # TODO: determine whether linear fit is accurate enough
        ioxy = (idf_b - idi_b) * fill_frac + idi_b

        return {
            "Ixx": ioxy[0][0],
            "Ixy": ioxy[0][1],
            "Ixz": ioxy[0][2],
            "Iyx": ioxy[1][0],
            "Iyy": ioxy[1][1],
            "Iyz": ioxy[1][2],
            "Izx": ioxy[2][0],
            "Izy": ioxy[2][1],
            "Izz": ioxy[2][2],
        }


class KaneModel(DerivedStateModel):
    """Calculates the Kane damping coefficient from 2016 simulation data by K. Doyle."""

    def evaluate(self, state: State) -> Dict[str, Any]:
        # Coefficients below are from Kyle's work.
        # TODO: Update them when we conduct a new Ansys analysis.
        k = 0.00085
        factor = 1.2

        N = 50
        kane = fill = tau1 = tau2 = np.zeros(N)
        for i in range(N):
            fill[i] = (i - 1) / N
            tau1[i] = k * fill[i]
            tau2[i] = factor * k * (1 - fill[i])
            kane[i] = -np.sqrt(tau1[i] ** 2 + tau2[i] ** 2)

        kane = kane - np.max(kane) + k
        kane = kane - np.min(kane)
        kane = kane * k / np.max(kane)

        q = np.round(state.fill_frac / 0.02 + 1)
        c = kane(q)

        return {"kane_c": c}


# # Maybe in another life...
# class LModel(EnvironmentModel):
#     """Class for the angular momentum model."""
#     def __init__(self, parameters: Parameters) -> None:
#         super().__init__(parameters)

#     def evaluate(self, state: State) -> Dict[str, Any]:
#         return super().evaluate(state)

#     def d_state(self, state: State) -> Dict[str, Any]:
#         ...


def cross_product_matrix(vector: np.array) -> np.matrix:
    """Creates a cross-multiplication matrix for a length 3 vector
    See bottom of page 2 of https://cornell.app.box.com/file/809903125394
    for brief reference.


    Args:
        vector (np.array): a 3x1 vector

    Returns:
        np.matrix: a 3x3 matrix which when matrix multiplied
    """
    return np.matrix([[0, -vector[2], vector[1]], [vector[2], 0, -vector[0]], [-vector[1], vector[0], 0]])


class AttitudeModel(EnvironmentModel):
    """Class for the angular velocity and position model."""

    def d_state(self, state_time: StateTime) -> Dict[str, Any]:
        """Evaluates
        (tau)   =   [I_b d(omega_{B/N})/dt]
                +   [(omega_{B/N}) x (I_b (omega_{B/N}))]
                + c [(omega_{B/N}) - (omega_{D/N})]
        where c is the "Kane Damping" constant.


        """

        s = state_time.state
        d = state_time.derived_state

        # angular position (quaternion dynamics)
        # taken from page 11 of https://cornell.app.box.com/file/809903125394

        cur_quat = np.array([s.quat_1, s.quat_2, s.quat_3, s.quat_4]).T
        v = cur_quat[1:3]
        r = cur_quat[4]

        xi = np.array([r * np.eye(3) + cross_product_matrix(v), -v.T])
        q_odot = np.array([xi, cur_quat])

        d_quat = 0.5 * np.matmul(q_odot, np.array([d.omega_x, d.omega_y, d.omega_z]))

        # TODO: Use angular momentum as state variable and for most dynamics evaluation
        # then calculate angular rates from momenta b/c inertia matricies change over time
