import unittest
from core.integrator.integrator import propagate_state
from core.state import State, StateTime
from state_test import s_1

import numpy as np


DEBUG = False


class IntegratorTestCases(unittest.TestCase):
    """
    This class tests the methods of class IntegratorTest.
    """

    def test_propagate_state(self):
        """
        This class tests that propagate_state updates the time and fields of the state correctly given a model.
        """

        def f(t: float, y: np.ndarray) -> np.ndarray:  # function that keeps the field constant
            return np.array([0]*len(y))

        initial_state_time = StateTime(State(s_1), 0.0)
        final_state_time = propagate_state(f, initial_state_time, 3.0)
        self.assertTrue(initial_state_time.__eq__(final_state_time))
        self.assertEqual(3.0, final_state_time.time)
        # Tests if function f, which keeps field constant causes propagate_state to
        # return an equivalent state (with time incremented accordingly).


if __name__ == "__main__":
    unittest.main()
