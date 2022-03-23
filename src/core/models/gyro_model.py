from core.models.model import SensorModel
import numpy as np

class GyroModel(SensorModel):
    """The gyro sensor model. This model applies the gyro bias and noise as specified in parameters.py"""

    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)
    
    def evaluate(self, state: State) -> Dict[str, Any]:
        return super().evaluate(state)
    
    def d_state(self, state: State) -> Dict[str, Any]:
        ang_vel_i = np.array([state.ang_vel_x, state.ang_vel_y, state.ang_vel_z])
        gyro_bias = np.array(self._parameters.gyro_bias)

        ang_vel_d = ang_vel_i + gyro_bias
        ang_vel_d = np.random.normal(loc=ang_vel_d, scale=self._parameters.gyro_noise, size=3)
        return {"ang_vel.x": ang_vel_d[0], "ang_vel.y": ang_vel_d[1], "ang_vel.z": ang_vel_d[2]} #return as quaternion rate?