
"""Configurations of parameters and initial conditions for a given simulation."""

from typing import Dict, Optional
from dataclasses import dataclass

import parameters
import state

@dataclass (frozen = True)
class Config:
    """Representation of the parameters and initial conditions of the simulation. This module depends on parameters.py. The variation in performance of different runs of the simulation depends on the variation of config.""" 

    def _init_(self, p : parameters.Parameters, time = 0.0, pos_x = 0.0, pos_y = 0.0, pos_z = 0.0, pos_ang = 0.0, vel = 0.0,quat_rate = 0.0):
        self.param = p
        self.init_cond = {
            "pos_x": pos_x,
            "pos_y": pos_y,
            "pos_z": pos_z,
            "pos_ang": pos_ang,
            "velocity": vel,
            "quat_rate": quat_rate    
        }

    # def _init_(self, parameters : parameters.Parameters, initial_conditions : Dict = {
    #     "pos_x": 0.0,
    #     "pos_y": 0.0,
    #     "pos_z": 0.0,
    #     "pos_ang": 0.0,
    #     "velocity": 0.0,
    #     "quad_rate": 0.0
    #     }):
    #     self.param = parameters
    #     self.init_cond = initial_conditions

