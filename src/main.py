import logging
from typing import Optional

log = logging.getLogger()

class SimRunner():
    def __init__(self, Optional[config_path] = None) -> None:
        
        self._sim = sim(config_)
        pass

    def run(self):
        for t in config.timesteps:
            try:
                self._sim.step()
            except Exception as e:
                log.error(e, exc_info=True)
                break
