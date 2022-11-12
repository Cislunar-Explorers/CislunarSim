import unittest

from core.parameters import Parameters
import math
from utils.test_utils import d3456, d3456_dict


class ParametersTestCase(unittest.TestCase):
    def test_parameters(self):
        self.assertEqual(
            d3456_dict,
            d3456.__dict__,
        )

        d_main = {
            "gyro_bias": [0.497625, -0.10821875, 0.77490625],
            "gyro_noise": [0.1824535, 0.11738579, 0.19192256],
            "gyro_sensitivity": 0.015625 * (math.pi / 180),
            "dry_mass": 0,
            "com": 0,
            "tank_volume": 0,
            "electolyzer_rate": 10.0 * (1/1000),
            "thruster_force": 0,
            "combustion_chamber_volume": 0,
            "max_iter": 1000000,
        }
        d_main["gyro_bias"] = [1.0, 2.0, 3.0]
        self.assertEqual(
            d_main,
            Parameters({"gyro_bias": [1.0, 2.0, 3.0]}).__dict__,
        )
        d_main["gyro_bias"] = [0.497625, -0.10821875, 0.77490625]
        d_main["gyro_noise"] = [4.0, 5.0, 6.0]
        self.assertEqual(
            d_main,
            Parameters({"gyro_noise": [4.0, 5.0, 6.0]}).__dict__,
        )
        d_main["gyro_noise"] = [0.1824535, 0.11738579, 0.19192256]
        d_main["dry_mass"] = 3
        self.assertEqual(
            d_main,
            Parameters({"dry_mass": 3}).__dict__,
        )
        d_main["dry_mass"] = 0
        d_main["com"] = 4
        self.assertEqual(
            d_main,
            Parameters({"com": 4}).__dict__,
        )
        d_main["com"] = 0
        d_main["tank_volume"] = 5
        self.assertEqual(
            d_main,
            Parameters({"tank_volume": 5}).__dict__,
        )
        d_main["tank_volume"] = 0
        d_main["thruster_force"] = 6
        self.assertEqual(
            d_main,
            Parameters({"thruster_force": 6}).__dict__,
        )
        self.assertEqual(
            {
                "gyro_bias": [0.497625, -0.10821875, 0.77490625],
                "gyro_noise": [0.1824535, 0.11738579, 0.19192256],
                "gyro_sensitivity": 0.015625 * (math.pi / 180),
                "dry_mass": 0,
                "com": 0,
                "tank_volume": 0,
                "electolyzer_rate": 10.0 * (1/1000),
                "thruster_force": 0,
                "combustion_chamber_volume": 0,
                "max_iter": 1000000,
            },
            Parameters({}).__dict__,
        )
