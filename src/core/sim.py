from core.config import Config

class CislunarSim():
    def __init__(self, config: Config) -> None:
        self._config = config
        self.models = build_models(self._config.models)
    
    def step(self):
        raise NotImplementedError