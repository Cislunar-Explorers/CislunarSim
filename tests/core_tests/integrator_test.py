import unittest
from core.integrator.integrator import propagate_state
from core.state import StateTime
from state_test import state_1

import numpy as np


DEBUG = False


class IntegratorTestCases(unittest.TestCase):
    """
    This class tests the methods of class IntegratorTest.
    """

    def test_propagate_state(self):
        """
        This class tests that propagate_state updates the time and fields of the state correctly given a model.
        TODO: Write this test given new interface for propagate_state.
        """
        ...


if __name__ == "__main__":
    unittest.main()
