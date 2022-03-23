from core.config import Config
from core.models.model_list import build_models


class CislunarSim:
    def __init__(self, config: Config) -> None:
        self._config = config
<<<<<<< HEAD
        self.models = build_models(self._config)
=======
        # TODO: Implement and fill in models into the list below and store as field models
        self.models = []
>>>>>>> main

    def step(self):
        raise NotImplementedError
