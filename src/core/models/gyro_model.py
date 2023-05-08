"""
Gyro sensor model documentation: https://cornell.box.com/s/6nu08iqfk5i389wlpp44r0yu5h50by8n
"""

from core.models.model import SensorModel
from core.parameters import Parameters
from core.state.statetime import StateTime
from typing import Dict, Any
import numpy as np


class GyroModel(SensorModel):
    """Applies the gyro bias and noise as specified in parameters.py"""

    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)
        self.gyro_bias = np.array(self._parameters.gyro_bias)
        self.gyro_noise = np.array(self._parameters.gyro_noise)

    def evaluate(self, state_time: StateTime) -> Dict[str, Any]:
        """Abstracts the angular velocities according to the model

        Args:
            state (State): The input state

        Returns:
            Dict[str, Any]: The augmented angular velocities
        """

        # smush the x, y, z components from state into a vector
        # (because vectorization is cool as hecc)
        ang_vel_true = state_time.derived_state.ang_vel

        # add gyro's bias
        ang_vel_biased = ang_vel_true.reshape(3) + self.gyro_bias.reshape(3)
        # add gyro's noise
        ang_vel_observed = np.random.normal(loc=ang_vel_biased, scale=self.gyro_noise, size=3)

        # filling in the array, applying gyro sensitivity
        for i in range(3):
            ang_vel_observed[i] = self._parameters.gyro_sensitivity * int(
                self._parameters.gyro_sensitivity / 2 + ang_vel_observed[i] / self._parameters.gyro_sensitivity
            )

        # return components of the angular velocity
        return {
            "ang_vel_x": ang_vel_observed[0],
            "ang_vel_y": ang_vel_observed[1],
            "ang_vel_z": ang_vel_observed[2],
        }
