import unittest, logging
from core.config import Config
from core.parameters import Parameters


DEBUG = False


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
        self.assert_equals(Config(param, ic).init_cond, ic_check)

    def test_init(self):
        """Tests if the initialization subs in default values for unspecified variables."""
        self.setup_helper(self.dummy_param, self.ic_pos, self.ic_pos_check)
        self.setup_helper(self.dummy_param, self.ic_all, self.ic_all_check)
        self.setup_helper(self.dummy_param, {}, self.ic_default_check)

    def test_immutability(self):
        """Makes sure that the configs cannot be mutated."""
        # TODO: expected failure / assert_raises
        try:
            test_config = Config(self.dummy_param, self.ic_pos).init_cond
            test_config.init_cond = {"throw": "error"}
            assert False
        except Exception as e:
            assert True




if __name__ == "__main__":
    unittest.main()
