from dataclasses import dataclass
import numpy as np
from typing import Dict

from utils.constants import State_Type


@dataclass
class State:
    """This is a container class for all state variables as defined in this sheet:
        https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2.

    In order to init a class of State, by far the easiest way is via kwarg unpacking:
        `my_state = State{**state_dict}`
    """

    # primitive state
    fill_frac: float = 0.0  # TODO, decouple with fuel_mass

    # angular momentum (kg*m^2/s)
    ang_vel_x: float = 0.0
    ang_vel_y: float = 0.0
    ang_vel_z: float = 0.0

    # angular position (quaternion)
    quat_v1: float = 0.0
    quat_v2: float = 0.0
    quat_v3: float = 0.0
    quat_r: float = 0.0

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
    dry_mass: float = 0.0
    chamber_temp: float = 0.0

    # derived state (Newtons)
    force_earth: float = 0.0
    force_moon: float = 0.0

    # discrete state
    propulsion_on: bool = False
    time_since_propulsing: float = 0.0
    solenoid_actuation_on: bool = False

    def update(self, state_dict: Dict[str, State_Type]) -> None:
        """Updates the fields of the state with specified key/value pairs in state_dict.
        If a key in the `state_dict` is not defined as an attribute in State.__init__, it will be ignored.
        """
        for key, value in state_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)

    def to_array(self):
        """The representation of the values of the fields as an array.

        Returns:
            Numpy array: contains all values stored in the fields.
        """
        return np.array(list(self.__dict__.values()))

    def from_array(self, state_array: np.ndarray):
        new_state = dict(zip(self.__dict__.keys(), state_array))
        self.update(new_state)


STATE_ARRAY_ORDER = list(State().__dict__.keys())


def array_to_state(values: np.ndarray) -> State:
    """Converts a numpy array or list into a `State` object.
        This assumes that the items in `state_array` are consistent with
        `STATE_ARRAY_ORDER`(which is an assumption that will probably lead
        to many bugs in the future...)

    Args:
        state_array (np.ndarray): n-by-1 numpy array of each state
    """
    return State(**dict(zip(STATE_ARRAY_ORDER, values)))


@dataclass
class ObservedState(State):
    # This is the true state with some noise applied
    # TODO: Implement noise application

    # angular velocity (radians/second)
    ang_vel_x: float = 0.0
    ang_vel_y: float = 0.0
    ang_vel_z: float = 0.0

    # angular position
    quat_v1: float = 0.0
    quat_v2: float = 0.0
    quat_v3: float = 0.0
    quat_r: float = 0.0

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
    dry_mass: float = 0.0
    chamber_temp: float = 0.0

    # derived state (Newtons)
    force_earth: float = 0.0
    force_moon: float = 0.0

    # discrete state
    #Is cubesat firing boolean
    propulsion_on: bool = False 
    #Time since start of firing
    time_since_propulsing: float = 0.0 
    #Time of last integrator propulsion call since start of prop firing (Reset to 0 after current firing completed)
    last_prop_call_time: float = 0.0 
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
