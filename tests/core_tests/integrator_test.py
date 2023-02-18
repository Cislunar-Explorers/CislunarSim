import unittest
from core.integrator import propagate_state

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
