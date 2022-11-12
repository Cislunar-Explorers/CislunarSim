import unittest
from core.parameters import Parameters
from core.models.electrolyzer_model import ElectrolyzerModel
from core.state.statetime import StateTime
from typing import Dict
from utils.test_utils import state_1

class ElectrolyzerModelUnitTest(unittest.TestCase):

    def test_electrolyzer_model(self):
        config_a = {
            "electrolyzer_rate": 0.1,
            "combustion_chamber_volume": 100
        }

        param_a = Parameters(config_a)
        state_a = StateTime(state_1)

        electrolyzer_a = ElectrolyzerModel(10.0, param_a)
        eval_a = electrolyzer_a.evaluate(state_a)

        # verify objects exist/are reasonable
        self.assertIsNotNone(eval_a)
        self.assertIsInstance(electrolyzer_a, ElectrolyzerModel)
        self.assertIsInstance(eval_a, Dict)

if __name__ == "__main__":
    unittest.main()