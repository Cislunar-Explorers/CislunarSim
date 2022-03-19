import unittest

from core.parameters import Parameters


class ParametersTestCase(unittest.TestCase):
    def test_parameters(self):
        d123456 = {
            "gyro_bias": 1,
            "gyro_noise": 2,
            "dry_mass": 3,
            "com": 4,
            "tank_volume": 5,
            "thruster_force": 6,
        }
        self.assert_equals(
            d123456,
            Parameters(d123456).__dict__,
        )

        d_main = {
            "gyro_bias": 1,
            "gyro_noise": 0,
            "dry_mass": 0,
            "com": 0,
            "tank_volume": 0,
            "thruster_force": 0,
        }

        self.assert_equals(
            d_main,
            Parameters({"gyro_bias": 1}).__dict__,
        )
        d_main["gyro_bias"] = 0
        d_main["gyro_noise"] = 2
        self.assert_equals(
            d_main,
            Parameters({"gyro_noise": 2}).__dict__,
        )
        d_main["gyro_noise"] = 0
        d_main["dry_mass"] = 3
        self.assert_equals(
            d_main,
            Parameters({"dry_mass": 3}).__dict__,
        )
        d_main["dry_mass"] = 0
        d_main["com"] = 4
        self.assert_equals(
            d_main,
            Parameters({"com": 4}).__dict__,
        )
        d_main["com"] = 0
        d_main["tank_volume"] = 5
        self.assert_equals(
            d_main,
            Parameters({"tank_volume": 5}).__dict__,
        )
        d_main["tank_volume"] = 0
        d_main["thruster_force"] = 6
        self.assert_equals(
            d_main,
            Parameters({"thruster_force": 6}).__dict__,
        )
        self.assert_equals(
            {
                "gyro_bias": 0,
                "gyro_noise": 0,
                "dry_mass": 0,
                "com": 0,
                "tank_volume": 0,
                "thruster_force": 0,
            },
            Parameters({}).__dict__,
        )
