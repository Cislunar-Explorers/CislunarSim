from typing import Callable, List, Dict, Type
import numpy as np
from core.models.model import ActuatorModel, EnvironmentModel, SensorModel
from core.state import State, array_to_state
from core.config import Config
from utils.constants import ModelEnum, State_Type


class AttitudeDynamics(EnvironmentModel):
    ...


class PositionDynamics(EnvironmentModel):
    def __init__(self, parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, t: float, state: State) -> Dict[str, State_Type]:
        return super().evaluate(t, state)

    def d_state(self, t: float, state: State) -> Dict[str, State_Type]:
        return {
            "x": 0,
            "y": 0,
            "z": 0,
            "vel_x": 0,
            "vel_y": 0,
            "vel_z": 0,
        }


class TestModel(EnvironmentModel):
    def __init__(self, parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, t: float, state: State) -> Dict[str, State_Type]:
        return super().evaluate(t, state)

    def d_state(self, t: float, state: State) -> Dict[str, State_Type]:
        dx = 0
        dy = 0
        dz = 0
        dwx = 0
        dwy = 0
        dwz = 0

        return {
            "ang_vel_x": dwx,
            "ang_vel_y": dwy,
            "ang_vel_z": dwz,
            "x": dx,
            "y": dy,
            "z": dz,
        }


# Dict containing all the models that are implemented
MODEL_DICT: Dict[ModelEnum, Type[EnvironmentModel]] = {
    ModelEnum.AttitudeModel: AttitudeDynamics,
    ModelEnum.PositionModel: PositionDynamics,
    ModelEnum.UnittestModel: TestModel,
}


def build_state_update_function(
    env_models: List[EnvironmentModel],
) -> Callable[[float, np.ndarray], np.ndarray]:
    def update_function(t: float, state_array: np.ndarray) -> np.ndarray:
        """The function that gets plugged into the integrator and propagates the state.
        The input to this function is the current state.

        Args:
            state (np.ndarray): _description_

        Returns:
            np.ndarray: _description_
        """
        propagated_state = State()
        state_in = array_to_state(state_array)

        for model in env_models:
            propagated_state.update(model.evaluate(t, state_in))

        propagated_state_array = propagated_state.to_array()
        return propagated_state_array

    return update_function


class ModelContainer:
    def __init__(self, config: Config) -> None:
        # env models propagate the state of the spacecraft
        self.environmental: List[EnvironmentModel] = []

        # actuator models convert actions from FSW to changes in (force/torque)
        # states
        self.actuator: List[ActuatorModel] = []

        # sensor models convert a true state to an observed state
        self.sensor: List[SensorModel] = []

        # sort models into env/sense/actuate
        for model_name in config.models:
            model = MODEL_DICT[model_name]
            # model_instantiated = model(config.param)
            if issubclass(model, EnvironmentModel):
                model_instantiated = model(config.param)
                self.environmental.append(model_instantiated)
            elif issubclass(model, ActuatorModel):
                model_instantiated = model(config.param)
                self.actuator.append(model_instantiated)
            elif issubclass(model, SensorModel):
                model_instantiated = model(config.param)
                self.sensor.append(model_instantiated)
            else:
                raise RuntimeError(
                    f"The type of `{model_name}` is not an expected type: {model}."
                )

        self.state_update_function: Callable = build_state_update_function(
            self.environmental
        )
