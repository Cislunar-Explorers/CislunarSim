"""Configurations of parameters and initial conditions for a given simulation."""

from typing import Dict, List
from dataclasses import dataclass
from utils.constants import DEFAULT_MODELS

import core.parameters as parameters
from utils.constants import ModelEnum


@dataclass(frozen=True)
class Config:
    """Representation of the parameters and initial conditions of the simulation. 
    This module depends on parameters.py. 
    The variation in performance of different runs of the simulation depends on the variation of config."""

    def __init__(
        self,
        parameters: parameters.Parameters,
        initial_conditions: Dict,
        models: List[ModelEnum]=DEFAULT_MODELS,
    ):
        self.param = parameters
        self.models = models
        default_conditions = {
            "pos_x": 0.0,
            "pos_y": 0.0,
            "pos_z": 0.0,
            "pos_ang": 0.0,
            "velocity": 0.0,
            "quad_rate": 0.0,
        }

        for key, value in initial_conditions.items():
            if key in default_conditions.keys():
                default_conditions[key] = value

        self.init_cond = default_conditions
