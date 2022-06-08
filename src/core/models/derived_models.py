from abc import abstractmethod
from core.parameters import Parameters
from core.state.state import State
from utils.astropy_util import get_body_position
from typing import Dict, Tuple, Union, List
import numpy as np
from utils.constants import BodyEnum, State_Type
from core.models.model_base import Model


class DerivedStateModel(Model):
    """
    Abstract Base class for all models this sim uses.
    """

    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    @abstractmethod
    def evaluate(self, time: float, state: State) -> Dict[str, Union[float, int, bool]]:
        """
        Abstract method for any model that evaluates the model based on the
            current state.
        An instance of State is required to evaluate the model, (because each
            model should be dependent on the state of the system.)
        Args:
            state (State): a instance of a State class.

        Returns:
            _type_: Defined in concrete instantiation of subclasses.
        """
        ...


class DerivedPosition(DerivedStateModel):
    """Updates position column vectors for use in the position dynamics model."""

    def evaluate(self, t: float, state: State) -> Dict[str, np.ndarray]:

        # Position column vectors from moon/sun/earth/craft to the origin, where the origin is
        # the Earth's center of mass.
        # Craft to origin
        r_co = np.array([state.x, state.y, state.z])
        # Moon to origin
        r_mo = np.array(get_body_position(10 * t // 10, BodyEnum.Moon))
        # Sun to origin
        r_so = np.array(get_body_position(10 * t // 10, BodyEnum.Sun))
        # Earth to origin (Note: Earth is at the origin in GCRS)
        r_eo = np.array((0.0, 0.0, 0.0))

        # Position column vectors from body to the craft.
        # Moon to the craft
        r_mc = np.subtract(r_mo, r_co)
        # Sun to the craft
        r_sc = np.subtract(r_so, r_co)
        # Earth to the craft
        r_ec = np.subtract(r_eo, r_co)

        return {
            "r_co": r_co,
            "r_mo": r_mo,
            "r_so": r_so,
            "r_eo": r_eo,
            "r_mc": r_mc,
            "r_sc": r_sc,
            "r_ec": r_ec,
        }


def quat_to_rotvec(q: Tuple[float, float, float, float]) -> np.ndarray:
    """Converts a 4-tuple representation of a quaternion into a 3-tuple Euler angle rotation vector.

    Uses the vector/scalar convention used in Markley and Crassidis (vector is the first 3 elements,
    scalar is the 4th element)"""
    norm = np.linalg.norm(q[:3])
    if not norm:
        return np.array([0, 0, 0])

    rotvec = np.array(q[:3]) / norm
    return rotvec


def cartesian_to_spherical(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """Converts a cartesian vector into a spherical coordinates"""

    r = np.sqrt(x * x + y * y + z * z)
    phi = np.arctan2(y, x)  # azimuth angle
    if r == 0:
        theta = 0
    else:
        theta = np.arccos(z / r)  # elevation angle

    return (r, phi, theta)


class FillFracModel(DerivedStateModel):
    def evaluate(self, state: State) -> Dict[str, State_Type]:
        return {"fill_frac": state.water_liquid_mass / self._parameters.tank_volume}


class InertiaModel(DerivedStateModel):
    def evaluate(self, state: State) -> Dict[str, np.ndarray]:
        fill_frac = FillFracModel().evaluate(state)["fill_frac"]

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
            "I": ioxy,
        }


class KaneModel(DerivedStateModel):
    """Calculates the Kane damping coefficient from 2016 simulation data by K. Doyle."""

    def evaluate(self, state: State) -> Dict[str, State_Type]:
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


class DerivedAttitude(DerivedStateModel):
    def evaluate(self, _: float, state: State):
        spin_vector = quat_to_rotvec((state.quat_v1, state.quat_v2, state.quat_v3, state.quat_r))
        spherical_coordinates = cartesian_to_spherical(*spin_vector)

        # I can't think of a good way to do this that is easy:
        moment_of_inertia = InertiaModel().evaluate(state)["I"]

        ang_momentum = np.array([state.h_x, state.h_y, state.h_z]).T
        # is there no numpy equivalent of MATLAB's `\` operator?
        angular_vel = np.matmul(np.linalg.inv(moment_of_inertia), ang_momentum)

        return {
            "attitude_vector": np.array(spin_vector),
            "azimuth": spherical_coordinates[1],
            "elevation": spherical_coordinates[2],
            "I": moment_of_inertia,
            "angular_velocity": angular_vel,
        }


DERIVED_MODEL_LIST: List[DerivedStateModel] = [DerivedPosition, DerivedAttitude]
