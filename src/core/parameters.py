import math
from typing import Dict


class Parameters:
    """
    This is a container class for all parameters as defined in this sheet:
     https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2.
    """

    def __init__(self, param_dict: Dict = {}):
        self.gyro_bias = [0.497625, -0.10821875, 0.77490625]
        self.gyro_noise = [0.1824535, 0.11738579, 0.19192256]
        self.gyro_sensitivity = 0.015625 * (math.pi / 180)
        self.dry_mass = 0
        self.com = 0
        self.tank_volume = 0
        self.thruster_force = 0

        for key, value in param_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)
