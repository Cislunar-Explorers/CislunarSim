import unittest
from core.models.model_list import PositionDynamics, DerivedPosition
from utils.test_utils import state_1, d3456


class PositionDynamicsModelTest(unittest.TestCase):
    """
    This class tests the position dynamics model implementation.
    """

    def test_position_dynamics_model(self):
        """
        This function tests the position dynamics model's d_state function.
        """
        base_state = state_1
        dummy_pd = PositionDynamics(d3456)
        dummy_dpd = DerivedPosition(d3456)
        base_state.derived_state.update(dummy_dpd.evaluate(1.0, state_1))
        propagated_state = dummy_pd.d_state(1.0, base_state)


        # trivial tests that check to make sure the velocity components from the input to the output match exactly
        self.assertEqual(9.0, propagated_state["x"])
        self.assertEqual(10.0, propagated_state["y"])
        self.assertEqual(11.0, propagated_state["z"])


if __name__ == "__main__":
    unittest.main()
