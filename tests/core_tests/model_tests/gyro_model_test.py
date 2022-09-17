import unittest
from core.parameters import Parameters
from core.models.gyro_model import GyroModel
from core.state.statetime import StateTime
from typing import Dict
from utils.test_utils import state_1


class GyroModelUnitTest(unittest.TestCase):
    def test_gyro_model(self):

        # test "clean" model: no bias, noise, quantization - aka no changes
        clean_vars = {
            "gyro_bias": [0, 0, 0],
            "gyro_noise": [0, 0, 0],
            "gyro_sensitivity": 1,
        }

        param_clean = Parameters(clean_vars)
        dummy_state = StateTime(state_1)

        gyro_clean = GyroModel(param_clean)
        eval_clean = gyro_clean.evaluate(dummy_state)

        # verify objects exist/are reasonable
        self.assertIsNotNone(eval_clean)
        self.assertIsInstance(gyro_clean, GyroModel)
        self.assertIsInstance(eval_clean, Dict)

        # verify the original values have not been augmented by the model
        self.assertEqual(eval_clean["ang_vel_x"], state_1.ang_vel_x)
        self.assertEqual(eval_clean["ang_vel_y"], state_1.ang_vel_y)
        self.assertEqual(eval_clean["ang_vel_z"], state_1.ang_vel_z)

        # test noisy and biased model
        param_noisy_biased = Parameters({})
        dummy_state = StateTime(state_1)

        gyro_noisy_biased = GyroModel(param_noisy_biased)
        eval_noisy_biased = gyro_noisy_biased.evaluate(dummy_state)

        # verify objects exist/are reasonable
        self.assertIsNotNone(eval_noisy_biased)
        self.assertIsInstance(gyro_noisy_biased, GyroModel)
        self.assertIsInstance(eval_noisy_biased, Dict)

        # verify the original values have been augmented by the model
        self.assertNotEqual(eval_noisy_biased["ang_vel_x"], state_1.ang_vel_x)
        self.assertNotEqual(eval_noisy_biased["ang_vel_y"], state_1.ang_vel_y)
        self.assertNotEqual(eval_noisy_biased["ang_vel_z"], state_1.ang_vel_z)


if __name__ == "__main__":
    unittest.main()
