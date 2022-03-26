import numpy as np
from typing import Dict


class State:
    """
    This is a container class for all state variables as defined in this sheet: https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2.
    """

    def __init__(self, state_dict: Dict = {}):
        self.time = 0.0

        # primitive state
        self.fill_frac = 0.88

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

        for key, value in state_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)

    def to_array(self):
        """
        to_array() is the representation of the values of the fields as an array.

        Returns:
            Numpy array: contains all values stored in the fields.
        """
        return np.array(list(self.__dict__.values()))


class ObservedState(dict):
    # This is the true state with some noise applied
    pass  # TODO
