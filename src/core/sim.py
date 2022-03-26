from core.config import Config


class CislunarSim:
    def __init__(self, config: Config) -> None:
        self._config = config
        # TODO: Implement and fill in models into the list below and store as field models
        self.models = []

    def step(self):
        raise NotImplementedError
