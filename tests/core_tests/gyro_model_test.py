import unittest
from core.parameters import Parameters
from core.models.gyro_model import GyroModel
from core.state import State
from typing import Dict, Any


class GyroModelUnitTest(unittest.TestCase):

    def test_gyro_model(self):
        
        s_1 = {
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

        # test "clean" model: no bias, noise, quantization - aka no changes
        clean_vars = {
            "gyro_bias": [0, 0, 0],
            "gyro_noise": [0, 0, 0],
            "gyro_sensitivity": 1
        }

        param_clean = Parameters(clean_vars)
        dummy_state = State(s_1)

        gyro_clean = GyroModel(param_clean)
        eval_clean = gyro_clean.evaluate(dummy_state)

        self.assertIsNotNone(eval_clean)
        self.assertIsInstance(gyro_clean, GyroModel)
        self.assertIsInstance(eval_clean, Dict)
        self.assertEqual(eval_clean["ang_vel_x"], s_1["ang_vel_x"])
        self.assertEqual(eval_clean["ang_vel_y"], s_1["ang_vel_y"])
        self.assertEqual(eval_clean["ang_vel_z"], s_1["ang_vel_z"])

        # test noisy and biased model
        param_noisy_biased = Parameters({})
        dummy_state = State(s_1)

        gyro_noisy_biased = GyroModel(param_noisy_biased)
        eval_noisy_biased = gyro_noisy_biased.evaluate(dummy_state)

        self.assertIsNotNone(eval_noisy_biased)
        self.assertIsInstance(gyro_noisy_biased, GyroModel)
        self.assertIsInstance(eval_noisy_biased, Dict)
        self.assertNotEqual(eval_noisy_biased["ang_vel_x"], s_1["ang_vel_x"])
        self.assertNotEqual(eval_noisy_biased["ang_vel_y"], s_1["ang_vel_y"])
        self.assertNotEqual(eval_noisy_biased["ang_vel_z"], s_1["ang_vel_z"])



if __name__ == "__main__":
    unittest.main()