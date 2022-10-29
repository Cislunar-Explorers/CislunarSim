from core.models.model import ActuatorModel
from core.parameters import Parameters
from core.state.statetime import StateTime
from typing import Dict, Any
from utils.constants import R, M_WATER
import numpy as np


class ElectrolyzerModel(ActuatorModel):
  """Propagates fuel mass and chamber pressure according to electrolysis parameters"""

  def __init__(self, duration: float, parameters: Parameters) -> None:
      super().__init__(parameters)

      self._duration = duration
      self._electrolyzer_rate = np.array(self._parameters.electolyzer_rate)
      self._chamber_temp = np.array(self._parameters.combustion_chamber_temp)
      self._chamber_vol = np.array(self._parameters.combustion_chamber_volume)

  def evaluate(self, state_time: StateTime) -> Dict[str, Any]:
      """Abstracts the electrolysis process according to the model

      Args:
          state_time (StateTime): The input statetime

      Returns:
          Dict[str, Any]: The augmented fuel mass and chamber pressure
      """

      # get fuel mass at this time
      fuel_mass_i = np.array([state_time.state.fuel_mass])

      # calculate updated fuel mass
      kg_electrolyzed = self._duration * self._electrolyzer_rate
      fuel_mass_d = fuel_mass_i - kg_electrolyzed

      # P = nRT / V, calculate updated chamber pressure
      chamber_pressure_d = ((kg_electrolyzed / (M_WATER / 1000)) * R * self._chamber_temp) / self._chamber_vol

      # return updated fuel mass and chamber pressure
      return {
        "fuel_mass": fuel_mass_d,
        "chamber_pressure": chamber_pressure_d
      }