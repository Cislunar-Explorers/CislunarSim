from core.config import Config

class CislunarSim():
    def __init__(self, config: Config) -> None:
        self._config = config
    
    def step(self):
        raise NotImplementedError