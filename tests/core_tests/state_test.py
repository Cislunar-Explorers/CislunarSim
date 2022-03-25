import unittest, logging
from core.state import State

import numpy as np

DEBUG = False


class StateTestCases(unittest.TestCase):
    def test_state_fields(self):
        s_0 = {
            "time": 0.0,
            "ang_vel_x": 0.0,
            "ang_vel_y": 0.0,
            "ang_vel_z": 0.0,
            "gnc_pos_q1": 0.0,
            "gnc_pos_q2": 0.0,
            "gnc_pos_q3": 0.0,
            "gnc_pos_q4": 0.0,
            "vel_x": 0.0,
            "vel_y": 0.0,
            "vel_z": 0.0,
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "force_propulsion_thrusters": 0.0,
            "fuel_mass": 0.0,
            "force_earth": 0.0,
            "force_moon": 0.0,
            "propulsion_on": False,
            "solenoid_actuation_on": False,
        }

        bool_fields = ["propulsion_on", "solenoid_actuation_on"]

        for field in s_0.keys():
            dummy_data = 1.0
            if field in bool_fields:
                dummy_data = True
            s_copy = dict(s_0)
            s_copy[field] = dummy_data
            self.assertEqual(
                s_copy,
                State({field: dummy_data}).__dict__,
            )

        self.assertEqual(
            {
                "time": 0.0,
                "ang_vel_x": 0.0,
                "ang_vel_y": 0.0,
                "ang_vel_z": 0.0,
                "gnc_pos_q1": 0.0,
                "gnc_pos_q2": 0.0,
                "gnc_pos_q3": 0.0,
                "gnc_pos_q4": 0.0,
                "vel_x": 0.0,
                "vel_y": 0.0,
                "vel_z": 0.0,
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "force_propulsion_thrusters": 0.0,
                "fuel_mass": 0.0,
                "force_earth": 0.0,
                "force_moon": 0.0,
                "propulsion_on": False,
                "solenoid_actuation_on": False,
            },
            State({}).__dict__,
        )

    def test_to_array(self):

        self.assertEqual(
            [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
                15.0,
                16.0,
                17.0,
                18.0,
                True,
                False,
            ],
            State(
                {
                    "time": 1.0,
                    "ang_vel_x": 2.0,
                    "ang_vel_y": 3.0,
                    "ang_vel_z": 4.0,
                    "gnc_pos_q1": 5.0,
                    "gnc_pos_q2": 6.0,
                    "gnc_pos_q3": 7.0,
                    "gnc_pos_q4": 8.0,
                    "vel_x": 9.0,
                    "vel_y": 10.0,
                    "vel_z": 11.0,
                    "x": 12.0,
                    "y": 13.0,
                    "z": 14.0,
                    "force_propulsion_thrusters": 15.0,
                    "fuel_mass": 16.0,
                    "force_earth": 17.0,
                    "force_moon": 18.0,
                    "propulsion_on": True,
                    "solenoid_actuation_on": False,
                }
            )
            .to_array()
            .tolist(),
        )


if __name__ == "__main__":
    unittest.main()
