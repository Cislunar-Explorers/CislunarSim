from typing import Callable, List, Dict, Type
import numpy as np
from core.models.model import ActuatorModel, EnvironmentModel, SensorModel
from core.state import State, array_to_state
from core.config import Config
from utils.constants import ModelEnum


class AttitudeDynamics(EnvironmentModel):
    ...


class PositionDynamics(EnvironmentModel):
    ...


# Dict containing all the models that are implemented
MODEL_DICT: Dict[ModelEnum, Type[EnvironmentModel]] = {
    ModelEnum.AttitudeModel: AttitudeDynamics,
    ModelEnum.PositionModel: PositionDynamics,
}


def build_state_update_function(env_models: List[EnvironmentModel]):
    def update_function(t: float, state_array: np.ndarray) -> np.ndarray:
        """The function that gets plugged into the integrator and propagates the state.
        The input to this function is the current state.

        Args:
            state (np.ndarray): _description_

        Returns:
            np.ndarray: _description_
        """
        propagated_state = State()
        state = array_to_state(state_array)

        for model in env_models:
            propagated_state.update(model.evaluate(t, state))

        propagated_state_array = propagated_state.to_array()
        return propagated_state_array

    return update_function


class ModelContainer:
    # env models propagate the state of the spacecraft
    environmental: List[EnvironmentModel]

    # actuator models convert actions from FSW to changes in (force/torque)
    # states
    actuator: List[ActuatorModel]

    # sensor models convert a true state to an observed state
    sensor: List[SensorModel]

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
