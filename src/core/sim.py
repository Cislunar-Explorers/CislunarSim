import numpy as np
from core.config import Config
from core.integrator.integrator import propagate_state
from core.state import State, StateTime, ObservedState, PropagatedOutput
from core.models.model_list import ModelContainer
from utils.astropy_util import get_body_position
from utils.log import log
import matplotlib.pyplot as plt
from utils.constants import BodyEnum, R_EARTH, R_MOON


class CislunarSim:
    """
    This class consolidates all parts of the sim (config, models, state).
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._models = ModelContainer(self._config)
        self.state: StateTime = self._config.init_cond
        self.observed_state = ObservedState()

        self.should_run = True
        self.num_iters = 0

        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection="3d")
        self.ax.set_xlim(-10000000, 10000000)
        self.ax.set_ylim(-10000000, 10000000)
        self.ax.set_zlim(-10000000, 10000000)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        # self.ax = plt.axes(projection='3d')
        self.xlocs = np.array([])
        self.ylocs = np.array([])
        self.zlocs = np.array([])

        self.ax.set

    def step(self) -> PropagatedOutput:
        """
        step() is the combined true and observed state after one step.
        """

        # Evaluate Actuator models to update state
        for actuator_model in self._models.actuator:
            self.state.state.update(actuator_model.evaluate(self.state.state))

        # Evaluate environmental models to propagate state
        self.state = propagate_state(self._models.state_update_function, self.state)

        # Evaluate sensor models
        temp_state = State()
        for sensor_model in self._models.sensor:
            temp_state.update(sensor_model.evaluate(self.state.state))

        # synchronize observed state time with true state time
        # TODO: clock drift?
        self.observed_state = ObservedState(temp_state, self.state.time)

        # TODO: Feed outputs of sensor models into FSW and return actuator's state as part of `PropagatedOutput`

        # check if we should stop the sim
        self.should_run = not (self.should_stop())
        self.num_iters += 1

        self.xlocs = np.append(self.xlocs, self.state.state.x)
        self.ylocs = np.append(self.ylocs, self.state.state.y)
        self.zlocs = np.append(self.zlocs, self.state.state.z)

        log.debug(self.state)
        return PropagatedOutput(self.state, self.observed_state)

    def should_stop(self) -> bool:
        """Returns True if something in our state reaches a condition that should stop the sim

        Args:
            state (StateTime): The current state of the system to evaluate

        Returns:
            bool: Whether the sim should be stopped
        """

        state = self.state.state

        if not np.isfinite(state.to_array()).all():
            # Thank you: https://stackoverflow.com/questions/911871/
            log.error("Stopping sim because of infinite value in state")
            log.debug(f"{self.state}")
            return True

        if self.num_iters > 1e5:
            log.error("Stopping sim because it's running too long")
            return True

        if (state.x**2 + state.y**2 + state.z**2) ** 0.5 < R_EARTH:
            log.error("Stopping sim because craft is inside the Earth")
            log.debug(f"r={(state.x**2 + state.y**2 + state.z**2)**0.5} < {R_EARTH}")
            self.plot_data()
            return True

        return False

    def plot_data(self):
        self.ax.scatter3D(self.xlocs, self.ylocs, self.zlocs, cmap="Greens")
        u, v = np.mgrid[0 : 2 * np.pi : 20j, 0 : np.pi : 10j]
        earth_x = R_EARTH * np.cos(u) * np.sin(v)
        earth_y = R_EARTH * np.sin(u) * np.sin(v)
        earth_z = R_EARTH * np.cos(v)
        self.ax.plot_surface(earth_x, earth_y, earth_z, color="g")

        moon_cx, moon_cy, moon_cz = get_body_position(self.state.time, BodyEnum.Moon)
        moon_x = moon_cx + R_MOON * np.cos(u) * np.sin(v)
        moon_y = moon_cy + R_MOON * np.sin(u) * np.sin(v)
        moon_z = moon_cz + R_MOON * np.cos(v)
        self.ax.plot_surface(moon_x, moon_y, moon_z, color="g")

        plt.show()
