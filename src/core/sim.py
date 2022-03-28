from dataclasses import dataclass
from core.config import Config
from core.integrator.integrator import propagate_state
from core.state import ObservedState, State, StateTime
from core.models.model_list import ModelContainer


@dataclass
class PropagatedOutput:
    true_state: StateTime
    observed_state: ObservedState
    # commanded_actuations


class CislunarSim:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._models = ModelContainer(self._config)
        self.state: State = self._config.init_cond
        self.observed_state = ObservedState()

    def step(self) -> PropagatedOutput:
        # Evaluate Actuator models to update state
        for actuator_model in self._models.actuator:
            self.state = State(actuator_model.evaluate(self.state))

        # Evaluate environmental models to propagate state
        self.state = propagate_state(self._models.state_update_function, self.state)

        # Evaluate sensor models
        for sensor_model in self._models.sensor:
            self.observed_state.update(sensor_model.evaluate(self.state))

        # TODO: Feed outputs of sensor models into FSW and return actuator's state as part of `PropagatedOutput`

        return PropagatedOutput(self.state, self.observed_state)
