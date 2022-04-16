from dataclasses import dataclass
from core.config import Config
from core.integrator.integrator import propagate_state
from core.state import ObservedState, StateTime
from core.models.model_list import ModelContainer


@dataclass
class PropagatedOutput:
    """
    This is a container class that holds a true_state and its corresponding observed_state.
    """

    true_state: StateTime
    observed_state: ObservedState
    # commanded_actuations


class CislunarSim:
    """
    This class consolidates all parts of the sim (config, models, state).
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._models = ModelContainer(self._config)
        self.state: StateTime = self._config.init_cond
        self.observed_state = ObservedState()

    def step(self) -> PropagatedOutput:
        """
        step() is the combined true and observed state after one step.
        """

        # Evaluate Actuator models to update state
        for actuator_model in self._models.actuator:
            self.state.state.update(actuator_model.evaluate(self.state.state))

        # TODO: Propagate derived state
        for derived_state_model in self._models.derived:
            self.state.state.derived_state.update(
                derived_state_model.evaluate(self.state.state))

        # Evaluate environmental models to propagate state
        self.state = propagate_state(self._models.state_update_function, self.state)

        # Evaluate sensor models
        for sensor_model in self._models.sensor:
            self.observed_state.state.update(sensor_model.evaluate(self.state.state))

        # synchronize observed state time with true state time
        self.observed_state.time = self.state.time

        # TODO: Feed outputs of sensor models into FSW and return actuator's state as part of `PropagatedOutput`

        return PropagatedOutput(self.state, self.observed_state)
