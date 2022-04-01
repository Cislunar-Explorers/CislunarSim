import unittest
from core.models.model_list import PositionDynamics
from core.state import State
import math

s_2 = {
    "ang_vel_x": 0.0,
    "ang_vel_y": 0.0,
    "ang_vel_z": 0.0,
    "gnc_pos_q1": 0.0,
    "gnc_pos_q2": 0.0,
    "gnc_pos_q3": 0.0,
    "gnc_pos_q4": 0.0,
    "vel_x": 1.0,
    "vel_y": 2.0,
    "vel_z": 3.0,
    "x": 10.0,
    "y": 20.0,
    "z": 30.0,
    "force_propulsion_thrusters": 0.0,
    "fuel_mass": 0.0,
    "force_earth": 0.0,
    "force_moon": 0.0,
    "propulsion_on": False,
    "solenoid_actuation_on": False,
}
dummy_state = State(s_2)

d3456 = {
    "gyro_bias": [0.497625, -0.10821875, 0.77490625],
    "gyro_noise": [0.1824535, 0.11738579, 0.19192256],
    "gyro_sensitivity": 0.015625 * (math.pi / 180),
    "dry_mass": 3,
    "com": 4,
    "tank_volume": 5,
    "thruster_force": 6,
}


class PositionDynamicsModelTest(unittest.TestCase):
    def test_position_dynamics_model(self):
        dummy_pd = PositionDynamics(d3456)
        propagated_state = dummy_pd.d_state(1.0, dummy_state)
        self.assertEqual(1.0, propagated_state["vel_x"])
        self.assertEqual(2.0, propagated_state["vel_y"])
        self.assertEqual(3.0, propagated_state["vel_z"])


if __name__ == "__main__":
    unittest.main()
