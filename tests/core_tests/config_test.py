import unittest
from core.config import Config, JsonError, MutationException
from core.parameters import Parameters
from core.state import State, StateTime
from jsonschema import SchemaError, ValidationError


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

    # make_config_dicts
    zeroes_param = {
        "gyro_bias" : [0.0, 0.0, 0.0],
        "gyro_noise" : [0.0, 0.0, 0.0],
        "gyro_sensitivity": 0.0,
        "dry_mass": 0.0,
        "com": 0.0,
        "tank_volume": 0.0,
        "thruster_force": 0.0
    }

    zeroes_ic = {
        
        "ang_vel_x" : 0.0, 
        "ang_vel_y" : 0.0, 
        "ang_vel_z" : 0.0, 
        
        "gnc_pos_q1" : 0.0, 
        "gnc_pos_q2" : 0.0, 
        "gnc_pos_q3" : 0.0, 
        "gnc_pos_q4" : 0.0, 

        "vel_x" : 0.0, 
        "vel_y" : 0.0, 
        "vel_z" : 0.0, 

        "x" : 0.0,
        "y" : 0.0,
        "z" : 0.0,
        
        "force_propulsion_thrusters": 0.0,
        "fuel_mass": 0.0,
        "force_earth": 0.0,
        "force_moon": 0.0,
        "propulsion_on": True,
        "solenoid_actuation_on": True
    }
    default_model = ["att", "pos"]

    angles_ic = {
        
        "ang_vel_x" : 5.0, 
        "ang_vel_y" : 5.0, 
        "ang_vel_z" : 5.0, 
        
        "gnc_pos_q1" : 10.0, 
        "gnc_pos_q2" : 10.0, 
        "gnc_pos_q3" : 10.0, 
        "gnc_pos_q4" : 10.0, 

        "vel_x" : 3.0, 
        "vel_y" : 3.0, 
        "vel_z" : 3.0, 

        "x" : 80.5,
        "y" : 70.5,
        "z" : 0.0
        }
    test1_param = {
        "thruster_force": 30.0
    } 
    test1_ic = {
        "vel_x" : 38.0, 
        "vel_y" : 37.0, 
        "vel_z" : 36.0, 
        "propulsion_on": False,
        "solenoid_actuation_on": False
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
            test_config_1.init_cond = StateTime.from_dict(self.ic_all)
            # mutating init_cond would throw error
        with self.assertRaises(MutationException):
            test_config_2.param = Parameters({})  # mutating param would throw error
        with self.assertRaises(MutationException):
            test_config_2.new_attribute = {}  # adding attribute would throw error

    def make_config_helper(self, path: str, param: dict, ic: dict):
        c = Config.make_config(path)
        self.assertEqual(c.param.__dict__, Parameters(param).__dict__)
        self.assertEqual(c.init_cond.__dict__, StateTime.from_dict(ic).__dict__)

    def test_make_config(self):
        """Tests creating config from json files in the data folder. """  
        DEFAULT_PATH = "configs/test_zeroes.json"      
        ANGLES_PATH = "configs/test_angles.json"
        EMPTY_PATH = "configs/test_empty.json"
        TEST1_PATH = "configs/test1.json"
        FAIL_PATH = "configs/test_fail.json"
        FAIL_GYRO_PATH = "configs/test_fail2.json"

        self.make_config_helper(DEFAULT_PATH, self.zeroes_param, self.zeroes_ic)
        self.make_config_helper(ANGLES_PATH, {}, self.angles_ic)
        self.make_config_helper(EMPTY_PATH, {}, {})
        self.make_config_helper(TEST1_PATH, self.test1_param, self.test1_ic)

        # with self.assertRaises(JsonError):
        #     Config.make_config(FAIL_PATH)
        #     # some of the fields in fail path are mistyped
        with self.assertRaises(JsonError):
            Config.make_config(FAIL_GYRO_PATH)
            # gyro_bias only has two items, it requires 3, this test tests against the requirements not specified by the json schema






if __name__ == "__main__":
    unittest.main()
