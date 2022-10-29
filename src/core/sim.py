from queue import Queue
import numpy as np
from core.config import Config
from core.state.state import ObservedState
from core.state.statetime import StateTime, PropagatedOutput
from core.models.model_list import ModelContainer
from utils.log import log
from utils.constants import R_EARTH, EARTH_SOI
from core.event import Event, NormalEvent

class CislunarSim:
    """This class consolidates all parts of the sim (config, models, state). It is responsible for 
    stepping the sim and checking stop conditions.
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._models = ModelContainer(self._config) #wouldn't need for event-based
        self.state_time: StateTime = self._config.init_cond
        self.observed_state = ObservedState()

        self.should_run = True
        self.num_iters = 0
        self.event_queue : "Queue[Event]" = Queue()

    def step(self) -> PropagatedOutput:
        """step() is the combined true and observed state after one step."""

        event = NormalEvent(self._models)
        self.event_queue.put(event)

        current_event = self.event_queue.get()
        self.state_time, self.observed_state = current_event.evaluate(self.state_time)

        # TODO: Feed outputs of sensor models into FSW and return actuator's state as part of `PropagatedOutput`

        # check if we should stop the sim
        self.should_run = not (self.should_stop())
        self.num_iters += 1

        log.debug(self.state_time)
        return PropagatedOutput(self.state_time, self.observed_state)

    def should_stop(self) -> bool:
        """Returns true if our state reaches a condition that should stop the sim

        Returns:
            bool: Whether the sim should be stopped
        """

        state = self.state_time.state

        if not np.isfinite(state.to_array()).all():
            # Thank you: https://stackoverflow.com/questions/911871/
            log.error("Stopping sim because of infinite value in state")
            log.debug(f"{state}")
            return True

        if self.num_iters > self._config.param.max_iter:
            log.error("Stopping sim because it's running too long")
            return True

        if (self.state_time.time - self._config.init_cond.time) > 6.312e7:
            log.error("Stopping sim because two years have passed")
            log.debug(f"Elapsed time = {int(self.state_time.time - self._config.init_cond.time)}s > 6.312e7")
            return True
        
        r_e = (state.x**2 + state.y**2 + state.z**2) ** 0.5
        if r_e < R_EARTH:
            log.error("Stopping sim because craft is inside the Earth")
            log.debug(f"r={r_e} < {R_EARTH}")
            return True

        if r_e > 5 * EARTH_SOI:
            log.error("Stopping sim because craft in Heliocentric orbit (way outside of Earth's SOI)")
            log.debug(f"r={r_e} > 5xEARTH_SOI")
            return True

        return False
