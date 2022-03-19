from utils.log import log
from typing import Optional
import core.config
from core.sim import CislunarSim


class SimRunner():
    def __init__(self, config_path: Optional[str] = None) -> None:
        config = core.config.make_config(config_path)
        self._sim = CislunarSim(config)
        pass

    def run(self):
        for t in config.timesteps:
            try:
                self._sim.step()
            except Exception as e:
                log.error(e, exc_info=True)
                break
        
