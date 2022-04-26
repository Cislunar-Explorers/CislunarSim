import numpy as np
from core.config import Config
from core.integrator.integrator import propagate_state
from core.state import State, StateTime, ObservedState, PropagatedOutput
from core.models.model_list import ModelContainer
from utils.log import log
from utils.constants import R_EARTH, EARTH_SOI
from utils.matplotlib_util import Plot


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
        temp_state = State()
        for sensor_model in self._models.sensor:
            temp_state.update(sensor_model.evaluate(self.state.state))

        # synchronize observed state time with true state time
        # TODO: clock drift?
        self.observed_state = ObservedState(temp_state, self.state.time)

        # TODO: Feed outputs of sensor models into FSW and return actuator's state as part of `PropagatedOutput`

        # check if we should stop the sim
        self.should_run = not (self.should_stop())
        self.num_iters += 1

        log.debug(self.state)
        return PropagatedOutput(self.state, self.observed_state)

    def should_stop(self) -> bool:
        """Returns True if something in our state reaches a condition that should stop the sim

        Args:
            state (StateTime): The current state of the system to evaluate

        Returns:
            bool: Whether the sim should be stopped
        """

        state = self.state.state

        if not np.isfinite(state.to_array()).all():
            # Thank you: https://stackoverflow.com/questions/911871/
            log.error("Stopping sim because of infinite value in state")
            log.debug(f"{self.state}")
            return True

        if self.num_iters > 1e6:
            log.error("Stopping sim because it's running too long")
            return True

        r_e = (state.x**2 + state.y**2 + state.z**2) ** 0.5
        if r_e < R_EARTH:
            log.error("Stopping sim because craft is inside the Earth")
            log.debug(f"r={r_e} < {R_EARTH}")
            return True

        if r_e > EARTH_SOI:
            log.error("Stopping sim because craft in Heliocentric orbit (outside of Earth's SOI)")
            log.debug(f"r={r_e} > {EARTH_SOI}")
            return True

        return False
