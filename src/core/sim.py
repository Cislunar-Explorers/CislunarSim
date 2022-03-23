from core.config import Config
from core.models.model_list import ModelContainer


class CislunarSim:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._models = ModelContainer(self._config)
        self.state = self._config.init_cond
        self.observed_state = {}
        # self._integrator =

    def step(self):
        # Evaluate Actuator models to update state
        for actuator_model in self._models.actuator:
            self.state.update(actuator_model.evaluate(self.state))


        # Evaluate environmental models, save previous and propagated state
        previous_state = self.state
        


        # Evaluate sensor models
        for sensor_model in self._models.sensor:
            self.observed_state.update(sensor_model.evaluate(self.state))

        # TODO: Feed outputs of sensor models into FSW

        raise NotImplementedError
