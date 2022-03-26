"""
Gyro sensor model documentation: https://cornell.box.com/s/6nu08iqfk5i389wlpp44r0yu5h50by8n
"""

from core.models.model import SensorModel
from core.parameters import Parameters
from core.state import State
from typing import Dict, Any
import numpy as np

class GyroModel(SensorModel):
    """Applies the gyro bias and noise as specified in parameters.py"""

    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, state: State) -> Dict[str, Any]:
        return super().evaluate(state)
    
    def d_state(self, state: State) -> Dict[str, Any]:
        """Abstracts the angular velocities according to the model

        Args:
            state (State): The input state

        Returns:
            Dict[str, Any]: The augmented angular velocities
        """
        ang_vel_i = np.array([state.ang_vel_x, state.ang_vel_y, state.ang_vel_z])
        gyro_bias = np.array(self._parameters.gyro_bias)

        ang_vel_d = ang_vel_i + gyro_bias
        ang_vel_d = np.random.normal(loc=ang_vel_d, scale=self._parameters.gyro_noise, size=3)

        for i in range(3):
            ang_vel_d[i] = self._parameters.gyro_sensitivity*int(self._parameters.gyro_sensitivity/2 + ang_vel_d[i]/self._parameters.gyro_sensitivity)

        return {"ang_vel_x": ang_vel_d[0], "ang_vel_y": ang_vel_d[1], "ang_vel_z": ang_vel_d[2]}