"""Configurations of parameters and initial conditions for a given simulation."""

from typing import Dict

import core.parameters as parameters
import core.state as state


class MutationException(Exception):
    pass


class Config:
    """Representation of the parameters and initial conditions of the simulation. This module depends on parameters.py. The variation in performance of different runs of the simulation depends on the variation of config."""

    _frozen = False

    def __init__(self, parameter: Dict, initial_condition: Dict):

        self.param = parameters.Parameters(parameter)
        self.init_cond = state.State(initial_condition)
        self._frozen = True

    def __setattr__(self, __name, __value) -> None:
        if self._frozen:
            raise MutationException("Cannot mutate config.")
        super.__setattr__(self, __name, __value)

    def __delattr__(self, __name) -> None:
        if self._frozen:
            raise MutationException("Cannot mutate config.")
        super.__setattr__(self, __name)
