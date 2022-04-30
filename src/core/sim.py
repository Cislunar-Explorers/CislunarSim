import numpy as np
from core.config import Config
from core.integrator.integrator import propagate_state
from core.state import StateTime, ObservedState, PropagatedOutput
from core.models.model_list import ModelContainer
from utils.log import log
from utils.numbers import R_EARTH


class CislunarSim:
    """
    This class consolidates all parts of the sim (config, models, state).
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._models = ModelContainer(self._config)
        self.state_time: StateTime = self._config.init_cond
        self.observed_state = ObservedState()

        self.should_run = True
        self.num_iters = 0

    def step(self) -> PropagatedOutput:
        """
        step() is the combined true and observed state after one step.
        """

        # Evaluate Actuator models to update state
        for actuator_model in self._models.actuator:
            self.state_time.update(actuator_model.evaluate(self.state_time))

        # Propagate derived state
        for derived_state_model in self._models.derived:
            self.state_time.derived_state.update(
                derived_state_model.evaluate(self.state_time))

        # Evaluate environmental models to propagate state
        self.state_time = propagate_state(self._models, self.state_time)

        # Evaluate sensor models
        temp_state = StateTime()
        for sensor_model in self._models.sensor:
            temp_state.update(sensor_model.evaluate(self.state_time))

        # synchronize observed state time with true state time
        # TODO: clock drift?
        self.observed_state = ObservedState(temp_state, self.state_time.time)

        # TODO: Feed outputs of sensor models into FSW and return actuator's state as part of `PropagatedOutput`

        # check if we should stop the sim
        self.should_run = not (self.should_stop())
        self.num_iters += 1
        log.debug(self.state_time.state)
        return PropagatedOutput(self.state_time, self.observed_state)

    def should_stop(self) -> bool:
        """Returns True if something in our state reaches a condition that should stop the sim

        Args:
            state (StateTime): The current state of the system to evaluate

        Returns:
            bool: Whether the sim should be stopped
        """

        state = self.state_time.state

        if not np.isfinite(state.float_fields_to_array()).all():
            # Thank you: https://stackoverflow.com/questions/911871/
            log.error("Stopping sim because of infinite value in state")
            log.debug(f"{state}")
            return True

        if self.num_iters > 1e5:
            log.error("Stopping sim because it's running too long")
            return True

        if (state.x**2 + state.y**2 + state.z**2)**0.5 < R_EARTH:
            log.error("Stopping sim because craft is inside the Earth")
            log.debug(f"r={(state.x**2 + state.y**2 + state.z**2)**0.5} < {R_EARTH}")
            return True

        return False
