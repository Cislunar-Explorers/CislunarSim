"""
Sim Parameters Spreadsheet: https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2
"""


from typing import Dict, Optional


class Parameters:
    def __init__(self, param_dict: Dict = {}):
        self.gyro_bias = [0.497625, -0.10821875, 0.77490625] #truncate to same # of decimal places?
        self.gyro_noise = [0.1824535, 0.11738579, 0.19192256]
        self.dry_mass = 0
        self.com = 0
        self.tank_volume = 0
        self.thruster_force = 0

        for key, value in param_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)