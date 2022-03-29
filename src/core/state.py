from dataclasses import dataclass
import numpy as np
from typing import Dict, Union


class State:
    """
    This is a container class for all state variables as defined in this sheet:
     https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2.
    """

    def __init__(self, state_dict: Dict = {}):
        # primitive state

        # angular velocity (radians/second)
        self.ang_vel_x = 0.0
        self.ang_vel_y = 0.0
        self.ang_vel_z = 0.0

        # angular position
        self.gnc_pos_q1 = 0.0
        self.gnc_pos_q2 = 0.0
        self.gnc_pos_q3 = 0.0
        self.gnc_pos_q4 = 0.0

        # velocity (meters / second)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.vel_z = 0.0

        # position (meters)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.force_propulsion_thrusters = 0.0
        self.fuel_mass = 0.0

        # derived state (Newtons)
        self.force_earth = 0.0
        self.force_moon = 0.0

        # discrete state
        self.propulsion_on = False
        self.solenoid_actuation_on = False

        self.update(state_dict)

    def update(self, state_dict: Dict[str, Union[int, float, bool]]) -> None:
        for key, value in state_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)

    def to_array(self):
        """
        to_array() is the representation of the values of the fields as an
         array.

        Returns:
            Numpy array: contains all values stored in the fields.
        """
        return np.array(list(self.__dict__.values()))

    def from_array(self, state_array: np.ndarray):

        new_state = dict(zip(self.__dict__.keys(), state_array))
        self.update(new_state)

    def __eq__(self, other):
        """

        Args:
            other (State): the "other" object self is being compared to.

        Returns:
            True iff other is a State object with equal attributes.
        """
        if type(other) == State:
            return self.__dict__ == other.__dict__
        return False


STATE_ARRAY_ORDER = list(State().__dict__.keys())


def array_to_state(values: np.ndarray) -> State:
    """Converts a numpy array or list into a `State` object.
     This assumes that the items in `state_array` are consistent with
     `STATE_ARRAY_ORDER`(which is an assumption that will probably lead
     to many bugs in the future...)

    Args:
        state_array (np.ndarray): n-by-1 numpy array of each state
    """
    return State(dict(zip(STATE_ARRAY_ORDER, values)))


@dataclass
class StateTime:
    """
    This class associates the state with the time.
    """

    state: State
    time: float = 0.0

    def __init__(self, state: State = State(), time: float = 0.0):
        self.state = state
        self.time = time

    def __eq__(self, other):
        """

        Args:
            other (StateTime): the "other" object self is being compared to.

        Returns:
            True iff other is a StateTime object and the states are equal to
             each other.
        """
        if type(other) == StateTime:
            return self.state.__eq__(other.state)
        return False


class ObservedState(dict):
    # This is the true state with some noise applied
    pass  # TODO
