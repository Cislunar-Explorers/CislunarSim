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
        self.assert_equals(
            {
                "gyro_bias": 1,
                "gyro_noise": 0,
                "dry_mass": 0,
                "com": 0,
                "tank_volume": 0,
                "thruster_force": 0,
            },
            Parameters({"gyro_bias": 1}).__dict__,
        )
        self.assert_equals(
            {
                "gyro_bias": 0,
                "gyro_noise": 2,
                "dry_mass": 0,
                "com": 0,
                "tank_volume": 0,
                "thruster_force": 0,
            },
            Parameters({"gyro_noise": 2}).__dict__,
        )
        self.assert_equals(
            {
                "gyro_bias": 0,
                "gyro_noise": 0,
                "dry_mass": 3,
                "com": 0,
                "tank_volume": 0,
                "thruster_force": 0,
            },
            Parameters({"dry_mass": 3}).__dict__,
        )
        self.assert_equals(
            {
                "gyro_bias": 1,
                "gyro_noise": 0,
                "dry_mass": 0,
                "com": 4,
                "tank_volume": 0,
                "thruster_force": 0,
            },
            Parameters({"com": 4}).__dict__,
        )
        self.assert_equals(
            {
                "gyro_bias": 0,
                "gyro_noise": 0,
                "dry_mass": 0,
                "com": 0,
                "tank_volume": 5,
                "thruster_force": 0,
            },
            Parameters({"tank_volume": 5}).__dict__,
        )
        self.assert_equals(
            {
                "gyro_bias": 0,
                "gyro_noise": 0,
                "dry_mass": 0,
                "com": 0,
                "tank_volume": 0,
                "thruster_force": 6,
            },
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


"""

        self.gyro_bias = 0
        self.gyro_noise = 0
        self.dry_mass = 0
        self.com = 0
        self.tank_volume = 0
        self.thruster_force = 0

"""
