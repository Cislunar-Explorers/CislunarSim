"""Configurations of parameters and initial conditions for a given simulation."""

from typing import Dict

import core.parameters as parameters


class MutationException(Exception):
    pass


class Config:
    """Representation of the parameters and initial conditions of the simulation. This module depends on parameters.py. The variation in performance of different runs of the simulation depends on the variation of config."""

    _frozen = False

    def __init__(self, parameters: parameters.Parameters, initial_conditions: Dict):
        self.param = parameters

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

        self._frozen = True

    def __setattr__(self, __name, __value) -> None:
        if self._frozen:
            raise MutationException("Cannot mutate config.")
        super.__setattr__(self, __name, __value)

    def __delattr__(self, __name) -> None:
        if self._frozen:
            raise MutationException("Cannot mutate config.")
        super.__setattr__(self, __name)
