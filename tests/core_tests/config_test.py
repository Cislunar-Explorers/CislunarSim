import unittest
from core.config import Config, MutationException
from core.parameters import Parameters
from core.state import State, StateTime


class ConfigTestCases(unittest.TestCase):
    """This test tests whether Config initializes as expected and if it is immutable."""

    param_pos = {"gyro_bias": [5.0, 5.0, 5.0], "dry_mass": 10, "com": 5}
    param_all = {
        "gyro_bias": [5.0, 5.0, 5.0],
        "gyro_noise": [5.0, 5.0, 5.0],
        "gyro_sensitivity": 0.05,
        "dry_mass": 10,
        "com": 10,
        "tank_volume": 10,
        "thruster_force": 10,
    }
    ic_pos = {"x": 3.0, "y": 3.0, "z": 3.0}
    ic_all = {
        "ang_vel_x": 10.0,
        "ang_vel_y": 10.0,
        "ang_vel_z": 10.0,
        "gnc_pos_q1": 10.0,
        "gnc_pos_q2": 10.0,
        "gnc_pos_q3": 10.0,
        "gnc_pos_q4": 10.0,
        "vel_x": 10.0,
        "vel_y": 10.0,
        "vel_z": 10.0,
        "x": 10.0,
        "y": 10.0,
        "z": 10.0,
        "force_propulsion_thrusters": 10.0,
        "fuel_mass": 10.0,
        "force_earth": 10.0,
        "force_moon": 10.0,
        "propulsion_on": True,
        "solenoid_actuation_on": True,
    }

    def setup_helper(self, param, ic):
        self.assertEqual(Config(param, ic).param.__dict__, Parameters(param).__dict__)
        self.assertEqual(Config(param, ic).init_cond.__dict__, StateTime.from_dict(ic).__dict__)

    def test_init(self):
        """Tests if the initialization subs in default values for unspecified variables."""
        for p in [{}, self.param_pos, self.param_all]:
            for i in [{}, self.ic_pos, self.ic_all]:
                self.setup_helper(p, i)

    def test_immutability(self):
        """Makes sure that the configs can be initialized but cannot be mutated."""
        test_config_1 = Config(self.param_pos, self.ic_pos)
        test_config_2 = Config(self.param_all, self.ic_all)
        with self.assertRaises(MutationException):
            test_config_1.init_cond = StateTime(
                {"throw": "error"}
            )  # mutating init_cond would throw error
        with self.assertRaises(MutationException):
            test_config_2.param = Parameters({})  # mutating param would throw error
        with self.assertRaises(MutationException):
            test_config_2.new_attribute = {}  # adding attribute would throw error


if __name__ == "__main__":
    unittest.main()
