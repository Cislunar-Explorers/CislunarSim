from abc import ABC, abstractmethod
from typing import Dict, Any, Type, Union
from core.state import State
from core.parameters import Parameters
from utils.constants import State_Type


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


class EnvironmentModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, t: float, state: State) -> Dict[str, State_Type]:
        return self.d_state(t, state)

    @abstractmethod
    def d_state(self, t: float, state: State) -> Dict[str, State_Type]:
        """Function which evaluates the differential equation:
         dy / dt = f(t, y)
         for the current state. "y" is a state vector (not just one variable)

        Args:
            t (float): current simulation time
            state (State): Current state object

        Returns:
            Dict[str, Any]: the name of each state being updated, and the
             value of its derivative. The keys of this dictionary must be in
             `STATE_ARRAY_ORDER`
        """
        ...


class SensorModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    @abstractmethod
    def evaluate(self, state: State) -> Dict[str, Any]:
        ...


class ActuatorModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        """Creates an actuator model with the given parameters

        Args:
            parameters (Parameters): parameters for actuator model
        """
        super().__init__(parameters)

    @abstractmethod
    def evaluate(self, state: State) -> Dict[str, Any]:
        ...


class DerivedStateModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    @abstractmethod
    def evaluate(self, state: State) -> Dict[str, Any]:
        ...
        

MODEL_TYPES = Union[Type[EnvironmentModel], Type[SensorModel], Type[ActuatorModel], Type[DerivedStateModel]]
