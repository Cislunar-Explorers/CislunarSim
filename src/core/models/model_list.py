from typing import Callable, List, Dict, Type
import numpy as np
from core.models.model import ActuatorModel, EnvironmentModel, SensorModel
from core.state import State, array_to_state
from core.config import Config
from utils.constants import BodyEnum, ModelEnum, State_Type
from utils.astropy_util import get_body_position


class AttitudeDynamics(EnvironmentModel):
    ...


class PositionDynamics(EnvironmentModel):
    """
    The position dynamics model implementation.
    """

    def __init__(self, parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, t: float, state: State) -> Dict[str, State_Type]:
        return super().evaluate(t, state)

    def d_state(self, t: float, state: State) -> Dict[str, State_Type]:
        """
        Takes the derivative of a vector [r v] to compute [v a], where r is a position vector,
        v is the velocity vector, and a is the acceleration vector
        Args:
            t (float): the initial time
            state (State): the initial state

        Returns:
            Dict[str, State_Type]: The updated vector [v a]
        """
        # position column vectors from moon/sun/earth/craft to the origin, where the origin is the Earth's center of mass

        # craft to origin
        r_co = np.array([state.x, state.y, state.z])
        # moon to origin
        r_mo = np.array(get_body_position(t, BodyEnum.Moon))
        # sun to origin
        r_so = np.array(get_body_position(t, BodyEnum.Sun))
        # earth to origin
        r_eo = np.array((0.0, 0.0, 0.0))  # Earth is at the origin in GCRS

        # position column vectors from body to the craft

        # moon to the craft
        r_mc = np.subtract(r_mo, r_co)
        # sun to the craft
        r_sc = np.subtract(r_so, r_co)
        # earth to the craft
        r_ec = np.subtract(r_eo, r_co)

        # mu values of the body, where mu = G * m_body
        G = 6.6743e-11
        mu_moon = G * 7.34767309e22
        mu_sun = G * 1.988409870698051e30
        mu_earth = G * 5.972167867791379e24
        # acceleration column vector calculation
        a = (
            # moon to craft acceleration component
            mu_moon * r_mc / (np.dot(r_mc, r_mc) ** (3 / 2))
            # sun to craft acceleration component
            + mu_sun * r_sc / (np.dot(r_sc, r_sc) ** (3 / 2))
            # earth to craft acceleration component
            + mu_earth * r_ec / (np.dot(r_ec, r_ec) ** (3 / 2))
        )
        print(
            {
                "x": state.vel_x,
                "y": state.vel_y,
                "z": state.vel_z,
                "vel_x": a[0],
                "vel_y": a[1],
                "vel_z": a[2],
            }
        )

        return {
            "x": state.vel_x,
            "y": state.vel_y,
            "z": state.vel_z,
            "vel_x": a[0],
            "vel_y": a[1],
            "vel_z": a[2],
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
