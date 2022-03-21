from core.config import Config
from core.models.model_list import build_models


class CislunarSim:
    def __init__(self, config: Config) -> None:
        self._config = config
        self.models = build_models(self._config)

    def step(self):
        raise NotImplementedError
