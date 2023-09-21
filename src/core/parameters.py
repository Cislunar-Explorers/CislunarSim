import math
from typing import Dict


class Parameters:
    """This is a container class for all parameters as defined in this sheet:
     https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2.
    """

    def __init__(self, param_dict: Dict = {}):

        self.gyro_bias = [0.4976250, -0.10821875, 0.77490625]
        self.gyro_noise = [0.1824535, 0.11738579, 0.19192256]
        self.gyro_sensitivity = 0.015625 * (math.pi / 180)

        self.dry_mass = 0
        self.com = 0
        
        # fuel tank
        self.tank_length = 1 # m
        self.tank_width = 1 
        self.tank_height = 1
        # changed rate to match that of the actual electrolyzer (was 10.0 * (1/1000) g/s): 
        # https://h-tec-education.com/quattro-electrolyzer-htec-e105
        self.electolyzer_rate = 0.00222222 #g/s
        self.min_ang_vel = 0.0
        self.min_height = 0.0

        self.temperature_min = 5
        self.temperature_max = 45

        # prop
        self.thruster_force = 0
        self.combustion_chamber_volume = 1

        # sim
        self.max_iter = 1e6

        for key, value in param_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)
