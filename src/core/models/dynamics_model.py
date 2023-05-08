import numpy as np
from core.models.model import EnvironmentModel
from typing import Dict
from core.state.statetime import StateTime
from utils import gnc_utils
from utils import constants


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

        # time derivative of angular momentum in the rigid body case
        cross_matrix = gnc_utils.cross_product_matrix(d.ang_vel)
        dhdt_rigid_body = external_moments - np.matmul(cross_matrix, angular_momentum)
        # Kane damper dynamics:
        # solves the second equation on page 5 of Bernardini_Pietro_2022_Spring_ACS.docx
        # for \dot{\omega}^{D/I}
        kane_damper_angular_velocity = np.array([[s.w_kane_x, s.w_kane_y, s.w_kane_z]]).T
        I_kd = self._parameters.kane_damper_inertia
        kane_cross_matrix = gnc_utils.cross_product_matrix(kane_damper_angular_velocity)
        kane_damping_term = d.kane_c * (kane_damper_angular_velocity - d.ang_vel)
        rhs = kane_damping_term - np.matmul(np.matmul(kane_cross_matrix, I_kd), kane_damper_angular_velocity)
        d_kane_ang_vel_dt = np.matmul(np.linalg.inv(I_kd), rhs)

        dhdt = dhdt_rigid_body - kane_damping_term.reshape((3, 1))
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
            "w_kane_x": float(d_kane_ang_vel_dt[0]),
            "w_kane_y": float(d_kane_ang_vel_dt[1]),
            "w_kane_z": float(d_kane_ang_vel_dt[2]),
        }
