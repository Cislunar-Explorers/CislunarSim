"""Configurations of parameters and initial conditions for a given simulation."""

from typing import Dict, List
from dataclasses import dataclass
from utils.constants import DEFAULT_MODELS

import core.parameters as parameters
from utils.constants import ModelEnum
from core.state import State


@dataclass(frozen=True)
class Config:
    """Representation of the parameters and initial conditions of the simulation.
    This module depends on parameters.py.
    The variation in performance of different runs of the simulation depends on the variation of config."""

    def __init__(
        self,
        parameters: parameters.Parameters,
        initial_conditions: Dict,
        models: List[ModelEnum] = DEFAULT_MODELS,
    ):
        self.param = parameters
        self.models = models
        default_conditions = {
            "time": 0.0,
            "ang_vel_x": 0.0,
            "ang_vel_y": 0.0,
            "ang_vel_z": 0.0,
            "gnc_pos_q1": 0.0,
            "gnc_pos_q2": 0.0,
            "gnc_pos_q3": 0.0,
            "gnc_pos_q4": 0.0,
            "vel_x": 0.0,
            "vel_y": 0.0,
            "vel_z": 0.0,
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "force_propulsion_thrusters": 0.0,
            "fuel_mass": 0.0,
            "force_earth": 0.0,
            "force_moon": 0.0,
            "propulsion_on": False,
            "solenoid_actuation_on": False,
        }

        for key, value in initial_conditions.items():
            if key in default_conditions.keys():
                default_conditions[key] = value

        self.init_cond = State(default_conditions)
