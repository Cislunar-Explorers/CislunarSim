from dataclasses import dataclass

import numpy as np
from core.config import Config
from core.integrator.integrator import propagate_state
from core.state import ObservedState, StateTime
from core.models.model_list import ModelContainer
from utils.log import log
from utils.numbers import R_EARTH


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

        self.should_run = True
        self.num_iters = 0

    def step(self) -> PropagatedOutput:
        """
        step() is the combined true and observed state after one step.
        """

        # Evaluate Actuator models to update state
        for actuator_model in self._models.actuator:
            self.state.state.update(actuator_model.evaluate(self.state.state))

        # Evaluate environmental models to propagate state
        self.state = propagate_state(self._models.state_update_function, self.state)

        # Evaluate sensor models
        for sensor_model in self._models.sensor:
            self.observed_state.state.update(sensor_model.evaluate(self.state.state))

        # synchronize observed state time with true state time
        self.observed_state.time = self.state.time

        # TODO: Feed outputs of sensor models into FSW and return actuator's state as part of `PropagatedOutput`

        # check if we should stop the sim
        self.should_run = not (self.should_stop())
        self.num_iters += 1
        return PropagatedOutput(self.state, self.observed_state)

    def should_stop(self) -> bool:
        """Returns True if something in our state reaches a condition that should stop the sim

        Args:
            state (StateTime): The current state of the system to evaluate

        Returns:
            bool: Whether the sim should be stopped
        """

        state = self.state.state

        if np.isfinite(state.to_array()).all():
            # Thank you: https://stackoverflow.com/questions/911871/
            log.error("Stopping sim because of infinite value in state")
            log.debug(f"{self.state}")
            return True

        if self.num_iters > 1e5:
            log.error("Stopping sim because it's running too long")
            return True

        if (state.x**2 + state.y**2 + state.z**2)**0.5 < R_EARTH:
            log.error("Stopping sim because craft is inside the Earth")
            return True

        return False
