
import unittest
from core.config import Config, MutationException
from core.parameters import Parameters



class ConfigTestCases(unittest.TestCase):
    """This test tests whether Config initializes as expected and if it is immutable."""

    dummy_param = Parameters({})
    ic_pos = {
        "pos_x": 3.0,
        "pos_y": 3.0,
        "pos_z": 3.0,
    }
    ic_pos_check = {
        "pos_x": 3.0,
        "pos_y": 3.0,
        "pos_z": 3.0,
        "pos_ang": 0.0,
        "velocity": 0.0,
        "quad_rate": 0.0,
    }
    ic_all = {
        "pos_x": 10.0,
        "pos_y": 10.0,
        "pos_z": 10.0,
        "pos_ang": 100.0,
        "velocity": 100.0,
        "quad_rate": 100.0,
    }
    ic_all_check = {
        "pos_x": 10.0,
        "pos_y": 10.0,
        "pos_z": 10.0,
        "pos_ang": 100.0,
        "velocity": 100.0,
        "quad_rate": 100.0,
    }
    ic_default_check = {
        "pos_x": 0.0,
        "pos_y": 0.0,
        "pos_z": 0.0,
        "pos_ang": 0.0,
        "velocity": 0.0,
        "quad_rate": 0.0,
    }

    def setup_helper(self, param, ic, ic_check):
        self.assertEqual(Config(param, ic).init_cond, ic_check)

    def test_init(self):
        """Tests if the initialization subs in default values for unspecified variables."""
        self.setup_helper(self.dummy_param, self.ic_pos, self.ic_pos_check)
        self.setup_helper(self.dummy_param, self.ic_all, self.ic_all_check)
        self.setup_helper(self.dummy_param, {}, self.ic_default_check)

    def test_immutability(self):
        """Makes sure that the configs can be initialized but cannot be mutated."""
        test_config_1 = Config(self.dummy_param, self.ic_pos)
        test_config_2 = Config(self.dummy_param, self.ic_all)
        with self.assertRaises(MutationException):
            test_config_1.init_cond = {
                "throw": "error"
            }  # mutating init_cond would throw error
        with self.assertRaises(MutationException):
            test_config_2.param = {}  # mutating param would throw error
        with self.assertRaises(MutationException):
            test_config_2.new_attribute = {}  # adding attribute would throw error


if __name__ == "__main__":
    unittest.main()
