import time
import unittest
from core.config import Config
from core.sim import CislunarSim
from utils.constants import ModelEnum, D_T


class SimTest(unittest.TestCase):
    def test_init(self):
        config = Config({}, {"time": time.time()},
                        models=[ModelEnum.UnittestModel])
        sim = CislunarSim(config, False)
        self.assertIsNotNone(sim)

    def test_step(self):
        config = Config({}, {"time": time.time()},
                        models=[ModelEnum.UnittestModel])
        sim = CislunarSim(config, False)

        initial_conditions = sim._config.init_cond
        next_conditions = sim.step()
        # The unittest model keeps every state the same. dState/dt = 0
        self.assertEqual(initial_conditions.state,
                         next_conditions.true_state.state)

        # Verify that time incremented in the sim by the expected amount
        self.assertEqual(next_conditions.true_state.time,
                         sim._config.init_cond.time + D_T)


if __name__ == "__main__":
    unittest.main()
