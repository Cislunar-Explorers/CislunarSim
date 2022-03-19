
import unittest, logging
from src.core.config import Config
from src.core.parameters import Parameters


DEBUG = False

class ConfigTestCases(unittest.TestCase):
    '''This test tests whether '''
    dummy_param = Parameters()
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


    def setup_helper (self, param, ic, ic_check):
        self.assert_equals(Config(param,ic).init_cond,ic_check)

    def test_init(self):
        self.setup_helper (self.dummy_param, self.ic_pos, self.ic_pos_check)
        self.setup_helper (self.dummy_param, self.ic_all, self.ic_all_check)
        self.setup_helper (self.dummy_param, {}, self.ic_default_check)

if __name__ == "__main__":
    unittest.main()