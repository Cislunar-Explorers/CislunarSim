import numpy as np
from typing import Dict


class State:
    """
    This is a container class for all state variables as defined in this sheet: https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2.
    """

    def __init__(self, state_dict: Dict = {}):
        self.time = 0

        # primitive state

        # angular velocity
        self.ang_vel_x = 0.0
        self.ang_vel_y = 0.0
        self.ang_vel_z = 0.0

        # angular position (in quaternions)
        self.gnc_pos_q1 = 0.0
        self.gnc_pos_q2 = 0.0
        self.gnc_pos_q3 = 0.0
        self.gnc_pos_q4 = 0.0

        # velocity
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.vel_z = 0.0

        # position
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.force_propulsion_thrusters = 0.0
        self.fuel_mass = 0.0

        # derived state
        self.force_earth = 0.0
        self.force_moon = 0.0

        # discrete state
        self.propulsion_on = True
        self.solenoid_actuation_on = True

        for key, value in state_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)

    def to_array(self):
        return np.array(list(self.__dict__.values()))


class ObservedState(dict):
    # This is the true state with some noise applied
    pass  # TODO
