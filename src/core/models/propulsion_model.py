from core.models.model import ActuatorModel
from core.parameters import Parameters
from core.state.statetime import StateTime
from typing import Dict, Any
import numpy as np
import matplotlib.pyplot as plt

class PropulsionModel(ActuatorModel):
    """Propagates location, time, based on propulsion model"""

    def __init__(self, start_time: float, end_time: float, parameters: Parameters) -> None:
      super().__init__(parameters)

      self._t1 = start_time
      self._t2 = end_time
    
    def evaluate(self, state_time: StateTime) -> Dict[str, Any]:
        """Function that calculates force, position, and velocity based on model

      Args:
          t1: start time
          t2: end time
          state_time (StateTime): The input statetime

      Returns:
          Dict[str, Any]: Thrust (force)
      """
        
        # Define variables
        d = 3 * 0.0254
        h = (3.968 + 1.618) * 0.0254
        d2 = 0.05 * 0.0254
        d2mm = d2 * 1000
        d3 = 0.305 * 0.0254
        A1 = np.pi * d ** 2 / 4
        A2 = np.pi * d2 ** 2 / 4
        A3 = np.pi * d3 ** 2 / 4
        vc = h * np.pi * d ** 2 / 4
        plim1 = 45 * 6894.76  # Pa
        plim2 = 100 * 6894.76  # Pa
        RH2 = 4.124e3  # J/kg*K
        RO2 = 0.2598e3  # J/kg*K
        RH2O = 0.4615e3  # J/kg*K
        CpH2O = 2532.8
        CvH2O = 2071.2
        gamma = CpH2O / CvH2O
        calc = (gamma + 1) / (2 * (gamma - 1))
        arearatio = A2 / A3
        int = arearatio * 1 / ((1 + (gamma - 1) / 2) ** calc)

        # Find M3
        eqn = M3 / ((1 + (gamma - 1) / 2 * M3 ** 2) ** calc) - int
        sol = solve(eqn, M3)
        M3 = float(sol[0])

        # Define time parameters
        dt = 0.0001
        tend = 1
        t = np.arange(0, tend + dt, dt)
        
        #Calculated variables
        mass_flow_rate = 1
        exit_mach = 1
        #exit_temperature = 1
        exit_pressure = 1
        free_stream_pressure = 1
        exit_velocity = 1

        #Calculate force
        thrust = mass_flow_rate * exit_velocity + (exit_pressure - free_stream_pressure) * exit_mach

        # return updated fuel mass and chamber pressure
        return {
            "thrust": thrust
        }




