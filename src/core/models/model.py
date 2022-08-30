from abc import abstractmethod
from typing import Dict, Any, Type, Union
from core.state.statetime import StateTime
from core.parameters import Parameters
from utils.constants import State_Type
from core.models.model_base import Model


class EnvironmentModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, state_time: StateTime) -> Dict[str, State_Type]:
        return self.d_state(state_time)

    @abstractmethod
    def d_state(self, state_time: StateTime) -> Dict[str, State_Type]:
        """Evaluates the differential equation:
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
    def evaluate(self, state: StateTime) -> Dict[str, Any]:
        ...


class ActuatorModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        """Creates an actuator model with the given parameters

        Args:
            parameters (Parameters): parameters for actuator model
        """
        super().__init__(parameters)

    @abstractmethod
    def evaluate(self, state_time: StateTime) -> Dict[str, Any]:
        ...


MODEL_TYPES = Union[Type[EnvironmentModel], Type[SensorModel], Type[ActuatorModel]]
