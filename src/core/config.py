"""Configurations of parameters and initial conditions for a given simulation."""

from typing import Dict, List
from utils.constants import DEFAULT_MODELS
from utils.constants import ModelEnum

from core.parameters import Parameters
from core.state import State, StateTime


class MutationException(Exception):
    pass


# TODO: Implement make_config function that takes in a config path (most likely leading to a JSON file) and construct a Config object


class Config:
    """Representation of the parameters and initial conditions of the simulation.
    This module depends on parameters.py, models.py, and state.py.
    The variation in performance of different runs of the simulation depends on the variation of config.
    This class is frozen, so it cannot be changed."""

    _frozen = False

    def __init__(
        self,
        parameters: Dict,
        initial_condition: Dict,
        models: List[ModelEnum] = DEFAULT_MODELS,
    ):

        self.param = Parameters(param_dict=parameters)
        try:
            time = parameters.pop("time")
        except KeyError:
            time = 0.0

        self.init_cond = StateTime(State(state_dict=initial_condition), time)
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
