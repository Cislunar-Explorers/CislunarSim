
from core.models.model import ActuatorModel
from core.parameters import Parameters
from core.state.statetime import StateTime
from typing import Dict, Any
import numpy as np

class PropulsionModel(ActuatorModel):
    """Models propulsion with start time, end time, pressure, and the FSW command as inputs."""

    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)
        self.start_time = self.__parameters.prop_start_t
        self.end_time = self.__parameters.prop_end_t

        self.gaussian_noise
        self.pressure

    def evaluate(self, state_time: StateTime) -> Dict[str, Any]:
        """Evaluates the propulsion model to return its new velocity and position

        Args:
            start time t1, end time t2, pressure, FSW command 

        Returns:
            force over time, velocity, position cislun
        """

