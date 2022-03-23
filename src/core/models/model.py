from abc import ABC, abstractmethod
from typing import Dict, Any
from core.state import State
from core.parameters import Parameters


class Model(ABC):
    def __init__(self, parameters: Parameters) -> None:
        self._parameters = parameters

    def evaluate(self, state: State) -> Dict[str, Any]:
        # TODO: wrap d_state with something (error checking?)
        delta_state = self.d_state(state)
        return delta_state

    @abstractmethod
    def d_state(self, state: State) -> Dict[str, Any]:
        ...


class EnvironmentModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, state: State) -> Dict[str, Any]:
        return super().evaluate(state)

    def d_state(self, state: State) -> Dict[str, Any]:
        ...


class SensorModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, state: State) -> Dict[str, Any]:
        return super().evaluate(state)

    def d_state(self, state: State) -> Dict[str, Any]:
        ...


class ActuatorModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, state: State) -> Dict[str, Any]:
        return super().evaluate(state)

    def d_state(self, state: State) -> Dict[str, Any]:
        ...
