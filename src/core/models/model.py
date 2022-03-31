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
    def d_state(self, state: State)  -> Dict[str, Any]:
        ...

class EnvironmentModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, t: float, state: State) -> Dict[str, Any]:
        return self.d_state(t, state)

    @abstractmethod
    def d_state(self, t: float, state: State) -> Dict[str, Any]:
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

    def evaluate(self, state: State) -> Dict[str, Any]:
        return super().evaluate(state)

    def d_state(self, state: State) -> Dict[str, Any]:
        pass


class ActuatorModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        """Creates an actuator model with the given parameters

        Args:
            parameters (Parameters): parameters for actuator model
        """
        super().__init__(parameters)

    def evaluate(self, state: State) -> Dict[str, Any]:
        """Evaluates the model for a given state

        Args:
            state (State): state of model

        Returns:
            Dict[str, Any]: idk
        """
        return super().evaluate(state)

    def d_state(self, state: State) -> Dict[str, Any]:
        pass

