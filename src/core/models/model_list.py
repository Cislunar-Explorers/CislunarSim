from typing import Callable, List, Dict
import numpy as np
from core.models.model import ActuatorModel, EnvironmentModel, SensorModel, MODEL_TYPES
from core.models.gyro_model import GyroModel
from core.state import State, StateTime, array_to_state
from core.config import Config
from utils.constants import ModelEnum, State_Type


class AttitudeDynamics(EnvironmentModel):
    ...


class PositionDynamics(EnvironmentModel):
    """
    The position dynamics model implementation.
    """

    def __init__(self, parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, state_time: StateTime) -> Dict[str, State_Type]:
        return super().evaluate(state_time)

    def d_state(self, state_time: StateTime) -> Dict[str, State_Type]:
        """ Takes the derivative of a vector [r v] to compute [v a], where r is a position vector,
        v is the velocity vector, and a is the acceleration vector
        Args:
            t (float): the initial time
            state (State): the initial state

        Returns:
            Dict[str, State_Type]: The updated vector [v a]
        """

        # Position column vectors from body to the craft
        r_mc = state_time.derived_state.r_mc
        r_sc = state_time.derived_state.r_sc
        r_ec = state_time.derived_state.r_ec

        # Mu values of the body, where mu = G * m_body
        G = 6.6743e-11
        mu_moon = G * 7.34767309e22
        mu_sun = G * 1.988409870698051e30
        mu_earth = G * 5.972167867791379e24
        
        # Acceleration column vector calculation
        a = (
            # Moon to craft acceleration component
            mu_moon * r_mc / (np.dot(r_mc, r_mc) ** (3 / 2))
            # Sun to craft acceleration component
            + mu_sun * r_sc / (np.dot(r_sc, r_sc) ** (3 / 2))
            # Earth to craft acceleration component
            + mu_earth * r_ec / (np.dot(r_ec, r_ec) ** (3 / 2))
        )

        return {
            "x": state_time.state.vel_x,
            "y": state_time.state.vel_y,
            "z": state_time.state.vel_z,
            "vel_x": a[0],
            "vel_y": a[1],
            "vel_z": a[2],
        }


class TestModel(EnvironmentModel):
    def __init__(self, parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, state_time: StateTime) -> Dict[str, State_Type]:
        return super().evaluate(state_time)

    def d_state(self, state_time: StateTime) -> Dict[str, State_Type]:
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


# Dict containing all the models that are implemented.
MODEL_DICT: Dict[ModelEnum, MODEL_TYPES] = {
    ModelEnum.AttitudeModel: AttitudeDynamics,
    ModelEnum.PositionModel: PositionDynamics,
    ModelEnum.GyroModel: GyroModel,
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
        state_in = StateTime(array_to_state(state_array), t)

        for model in env_models:
            propagated_state.update(model.evaluate(state_in))

        propagated_state_array = propagated_state.float_fields_to_array()
        return propagated_state_array

    return update_function


class ModelContainer:
    def __init__(self, config: Config) -> None:

        # Derived state models propagate derived values.
        # They are the same each time, meaning we can simply list them here.
        # TODO: Determine whether this is the best way to do this.
        # self.derived: List[DerivedStateModel] = [DerivedPosition(config.param)]

        # Environmental models propagate the state of the spacecraft.
        self.environmental: List[EnvironmentModel] = []

        # Actuator models convert actions from FSW to changes in (force/torque) states.
        self.actuator: List[ActuatorModel] = []

        # Sensor models convert a true state to an observed state.
        self.sensor: List[SensorModel] = []

        # Sort models into environmental/actuator/sensor.
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
                raise RuntimeError(f"The type of `{model_name}` is not an expected type: {model}.")

        self.state_update_function: Callable = build_state_update_function(self.environmental)
