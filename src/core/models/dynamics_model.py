import numpy as np
from core.models.model import EnvironmentModel
from core.models.derived_models import DerivedStateModel
from typing import Dict, Any
from core.state.state import State
from core.state.statetime import StateTime
from utils import gnc_utils
from utils import constants


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
        c = kane[q]

        return {"kane_c": c}


class AttitudeDynamics(EnvironmentModel):
    """Class for the angular velocity and position model."""

    def d_state(self, state_time: StateTime) -> Dict[str, constants.State_Type]:
        """Evaluates
        (tau)   =   [I_b d(omega_{B/N})/dt]
                +   [(omega_{B/N}) x (I_b (omega_{B/N}))]
                + c [(omega_{B/N}) - (omega_{D/N})]
        where c is the "Kane Damping" constant.
        """

        s = state_time.state
        d = state_time.derived_state

        cur_quat = np.array([s.quat_v1, s.quat_v2, s.quat_v3, s.quat_r])
        angular_vel = d.ang_vel
        d_quat = gnc_utils.quaternion_derivative(cur_quat, angular_vel)
        # TODONE: Use angular momentum as state variable and for most dynamics evaluation
        # then calculate angular rates from momenta b/c inertia matricies change over time

        # TODO: track external moments somewhere in state
        # external moments include mostly just ACS firings/torques, but can also include:
        # gravity gradient torques (J2, of Earth and Moon), differential solar wind pressure, atmospheric drag, etc.
        external_moments = np.array([[0.0, 0.0, 0.0]]).T

        # page 16 of MAE 4060 Handout: Rigid Body Dynamics:
        # I dw/dt + w cross h = tau
        # --> dh/dt =  (tau - w cross h)
        angular_momentum = np.array([[s.h_x, s.h_y, s.h_z]]).T

        # time derivative of angular momentum
        cross_matrix = gnc_utils.cross_product_matrix(d.ang_vel)
        dhdt = external_moments - np.matmul(cross_matrix, angular_momentum)

        dh_x = dhdt[0][0]
        dh_y = dhdt[1][0]
        dh_z = dhdt[2][0]
        
        return {
            "quat_v1": float(d_quat[0][0]),
            "quat_v2": float(d_quat[1][0]),
            "quat_v3": float(d_quat[2][0]),
            "quat_r": float(d_quat[3][0]),
            "h_x": float(dh_x),
            "h_y": float(dh_y),
            "h_z": float(dh_z),
        }
