from abc import ABC, abstractmethod
from typing import Dict, Any
from core.state import State
from core.parameters import Parameters
from utils.constants import State_Type

class DerivedStateModel(ABC):
    """
    Abstract Base Class for all derived state models this sim uses.
    """

    def __init__(self, parameters: Parameters) -> None:
        """DerivedStateModel __init__
        All derived state models will be dependent on some parameters, so we load them in
        here.
        Args:
            parameters (Parameters): Instance of the parameters class gets
            passed in to be accessible by the derived state model.
        """
        self._parameters = parameters

    @abstractmethod
    def evaluate(self, state: State):
        """
        Abstract method for any model that evaluates the model based on the
         current state.
        An instance of State is required to evaluate the model, (because each
         model should be dependent on the state of the system.)
        Args:
            state (State): a instance of a State class.

        Returns:
            _type_: Defined in concrete instantiation of subclasses.
        """