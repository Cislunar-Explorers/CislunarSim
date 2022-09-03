from dataclasses import dataclass
import numpy as np
from typing import Dict, Union
from core.derived_state import DerivedState
from core.models.derived_models import DERIVED_MODEL_LIST
from utils.constants import State_Type


@dataclass
class State:
    """
    This is a container class for all state variables as defined in this sheet:
        https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2.

    In order to init a class of State, by far the easiest way is via kwarg unpacking:
        `my_state = State{**state_dict}`
    """

    # primitive state

    # angular velocity (radians/second)
    ang_vel_x: float = 0.0
    ang_vel_y: float = 0.0
    ang_vel_z: float = 0.0

    # angular position
    gnc_pos_q1: float = 0.0
    gnc_pos_q2: float = 0.0
    gnc_pos_q3: float = 0.0
    gnc_pos_q4: float = 0.0

    # velocity (meters / second)
    vel_x: float = 0.0
    vel_y: float = 0.0
    vel_z: float = 0.0

    # position (meters)
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    force_propulsion_thrusters: float = 0.0
    fuel_mass: float = 0.0

    # derived state (Newtons)
    force_earth: float = 0.0
    force_moon: float = 0.0

    # discrete state
    propulsion_on: bool = False
    solenoid_actuation_on: bool = False

    def update(self, state_dict: Dict[str, Union[int, float, bool]]) -> None:
        """
        Updates the fields of the state with specified key/value pairs in state_dict.
        If a key in the `state_dict` is not defined as an attribute in State.__init__, it will be ignored.
        """
        for key, value in state_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)

    def to_array(self):
        """
        The representation of the values of the fields as an
            array.

        Returns:
            Numpy array: contains all values stored in the fields.
        """
        return np.array(list(self.__dict__.values()))

    def from_array(self, state_array: np.ndarray):

        new_state = dict(zip(self.__dict__.keys(), state_array))
        self.update(new_state)

    # being a dataclass means __eq__ is automatically generated for you!
    # def __eq__(self, other):
    #    """
    #
    #    Args:
    #        other (State): the "other" object self is being compared to.
    #
    #    Returns:
    #        True iff other is a State object with equal attributes.
    #    """
    #    if type(other) == State:
    #        return self.__dict__ == other.__dict__
    #    return False


STATE_ARRAY_ORDER = list(k for k in State().__dict__.keys() if k != "derived_state")


def array_to_state(values: np.ndarray) -> State:
    """
    Converts a numpy array or list into a `State` object.
        This assumes that the items in `state_array` are consistent with
        `STATE_ARRAY_ORDER`(which is an assumption that will probably lead
        to many bugs in the future...)

    Args:
        state_array (np.ndarray): n-by-1 numpy array of each state
    """
    return State(**dict(zip(STATE_ARRAY_ORDER, values)))


@dataclass
class StateTime:
    """
    This class associates the state with the time.
    """

    state: State = State()
    time: float = 0.0
    derived_state: DerivedState = DerivedState()

    def __post_init__(self):
        for derived_state_model in DERIVED_MODEL_LIST:
            self.update_derived(
                derived_state_model.evaluate(self.time, self.state.__dict__)
            )

    @classmethod
    def from_dict(cls, statetime_dict: Dict[str, State_Type]):
        """
        Generates a new StateTime instance from an input dictionary. Can be called via `StateTime.from_dict(...)` to make a new StateTime object

        Args:
            statetime_dict (Dict[str, State_Type]): _description_

        Returns:
            StateTime: _description_
        """
        try:
            time = statetime_dict.pop("time")
        except KeyError:
            time = 0.0

        return cls(State(**statetime_dict), time=time)

    def update(self, state_dict: Dict[str, Union[int, float, bool]]) -> None:
        """
        update() is a procedure that updates the fields of the state with specified key/value pairs in state_dict.
        If a key in the `state_dict` is not defined as an attribute in State.__init__, it will be ignored.
        """
        self.state.update(state_dict)

    def update_derived(self, state_dict: Dict) -> None:
        """
        update_derived() is a procedure that updates the fields of the derived state with specified key/value pairs in state_dict.
        If a key in the `state_dict` is not defined as an attribute in DerivedState.__init__, it will be ignored.
        """
        self.derived_state.update(state_dict)

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


@dataclass
class ObservedState(State):
    # This is the true state with some noise applied
    # TODO: Implement noise application

    # angular velocity (radians/second)
    ang_vel_x: float = 0.0
    ang_vel_y: float = 0.0
    ang_vel_z: float = 0.0

    # angular position
    gnc_pos_q1: float = 0.0
    gnc_pos_q2: float = 0.0
    gnc_pos_q3: float = 0.0
    gnc_pos_q4: float = 0.0

    # velocity (meters / second)
    vel_x: float = 0.0
    vel_y: float = 0.0
    vel_z: float = 0.0

    # position (meters)
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    force_propulsion_thrusters: float = 0.0
    fuel_mass: float = 0.0

    # derived state (Newtons)
    force_earth: float = 0.0
    force_moon: float = 0.0

    # discrete state
    propulsion_on: bool = False
    solenoid_actuation_on: bool = False

    def init_from_state(self, state: State):
        for key, value in state.__dict__.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)

    def gaussian_noise(self, mu: float, sigma: float):
        """
        Args:
            sigma (float): standard deviation of the noise
        """
        noise = np.random.normal(mu, sigma)
        self.mu = noise


@dataclass
class PropagatedOutput:
    """
    This is a container class that holds a true_state and its corresponding observed_state.
    """

    true_state: StateTime
    observed_state: ObservedState
    # commanded_actuations
