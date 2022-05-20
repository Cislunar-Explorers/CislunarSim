from abc import ABC, abstractmethod
from typing import Any
from core.config import Parameters


class Model(ABC):
    """
    Abstract Base class for all models this sim uses.
    """

    def __init__(self, parameters: Parameters) -> None:
        """Model __init__
        All models will be dependent on some parameters, so we load them in
        here.
        Args:
            parameters (Parameters): Instance of the parameters class gets
            passed in to be accessible by the model.
        """
        self._parameters = parameters

    @abstractmethod
    def evaluate(self, state_time: Any) -> Any:
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
