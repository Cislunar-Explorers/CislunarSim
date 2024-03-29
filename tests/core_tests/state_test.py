import unittest
from core.state.state import State
from core.state.derived_state import DerivedState
from core.state.statetime import StateTime
from utils.test_utils import s_0, state_1


class StateTestCases(unittest.TestCase):
    """
    This class tests the constructor and methods of class StateTest.
    """

    def test_state_time_fields(self):
        """
        Tests that all fields are set properly when creating a new instance of StateTime.
        """
        st_1 = StateTime(state_1, 10.0)
        self.assertEqual(state_1, st_1.state)
        self.assertEqual(10.0, st_1.time)

    def test_state_fields(self):
        """
        Tests that all fields are set properly when creating a new instance of State.
        """
        bool_fields = ["propulsion_on", "solenoid_actuation_on"]

        s_copy = {}
        field = ""
        dummy_data = None

        for field in s_0.keys():
            dummy_data = 1.0
            if field in bool_fields:
                dummy_data = True
            if field == "derived_state":
                dummy_data = DerivedState()
            s_copy = dict(s_0)
            s_copy[field] = dummy_data

        self.assertEqual(
            s_copy,
            State(**{field: dummy_data}).__dict__,
        )

    def test_to_array(self):
        """
        Tests that float_fields_to_array() returns the correct values for the fields of an instance of State, in a consistent order.
        """
        
        state_list = [
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            True,
            False
        ]
        self.assertEqual(
            state_list,
            state_1.to_array().tolist(),
        )


if __name__ == "__main__":
    unittest.main()
