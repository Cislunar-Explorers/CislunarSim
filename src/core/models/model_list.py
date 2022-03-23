from typing import Callable, List, Dict, Type, Any
from core.models.model import ActuatorModel, EnvironmentModel, Model, SensorModel
from core.state import State
from core.config import Config
from utils.constants import ModelEnum


class AttitudeDynamics(Model):
    ...


class PositionDynamics(Model):
    ...



# Dict containing all the models that are implemented
MODEL_DICT: Dict[ModelEnum, Type[Model]] = {
    ModelEnum.AttitudeModel: AttitudeDynamics,
    ModelEnum.PositionModel: PositionDynamics,
}

def build_state_update_function(env_models: List[EnvironmentModel]):
    def update_function(state: State) -> Dict[str, Any]:
        propagated_state = state
        for model in env_models:
            propagated_state.update(model.evaluate(state))
        return propagated_state
        
    return update_function


class ModelContainer:
    environmental: List[EnvironmentModel] # env models propagate the state of the spacecraft
    actuator: List[ActuatorModel] # actuator models convert actions from FSW to changes in (force/torque) states
    sensor: List[SensorModel] # sensor models convert a true state to an observed state
    
    def __init__(self, config: Config) -> None:
        for model_name in config.models:
            model = MODEL_DICT[model_name](config.param)
            if type(model) is EnvironmentModel:
                self.environmental.append(model)
            elif type(model) is ActuatorModel:
                self.actuator.append(model)
            elif type(model) is SensorModel:
                self.sensor.append(model)
            else:
                raise RuntimeError(f"The type of `{model_name}` is not an expected type.")
        
        self.state_update_function: Callable = build_state_update_function(self.environmental)