"""
Sim Parameters Spreadsheet: https://cornell.box.com/s/z20wbp66q0pseqievmadf515ucd971g2
"""


from typing import Dict, Optional


class Parameters:
    def __init__(self, param_dict: Dict = {}):
        self.gyro_bias = 0
        self.gyro_noise = 0
        self.dry_mass = 0
        self.com = 0
        self.tank_volume = 0
        self.thruster_force = 0

        for key, value in param_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)
