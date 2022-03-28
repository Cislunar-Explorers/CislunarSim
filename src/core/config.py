"""Configurations of parameters and initial conditions for a given simulation."""

from typing import Dict, List
from utils.constants import DEFAULT_MODELS
from utils.constants import ModelEnum

from core.parameters import Parameters
from core.state import State


class MutationException(Exception):
    pass


class Config:
    """Representation of the parameters and initial conditions of the simulation. 
    This module depends on parameters.py, models.py, and state.py. 
    The variation in performance of different runs of the simulation depends on the variation of config."""

    _frozen = False

    def __init__(self, parameter: Dict, 
                 initial_condition: Dict, 
                 models: List[ModelEnum] = DEFAULT_MODELS):

        self.param = Parameters(parameter)
        self.init_cond = State(initial_condition)
        self.models = models
        self._frozen = True

    def __setattr__(self, __name, __value) -> None:
        if self._frozen:
            raise MutationException("Cannot mutate config.")
        object.__setattr__(self, __name, __value)

    def __delattr__(self, __name) -> None:
        if self._frozen:
            raise MutationException("Cannot mutate config.")
        object.__delattr__(self, __name)

