from utils.log import log
from typing import Optional
import core.config
from core.sim import CislunarSim


class SimRunner:
    def __init__(self, config_path: Optional[str] = None) -> None:
        config = core.config.make_config(config_path)
        self._sim = CislunarSim(config)
        self.state_history = []

    def run(self):
        while True:  # TODO, add better break conditions
            try:
                updated_states = self._sim.step()
                self.state_history.append(updated_states)
            except Exception as e:
                log.error(e, exc_info=True)
                break
