from core.models.model import ActuatorModel
from core.parameters import Parameters
from core.state.statetime import StateTime
from typing import Dict, Any
from utils.constants import R
import numpy as np


class ElectrolyzerModel(ActuatorModel):

  """"""

  def __init__(self, duration: float, parameters: Parameters) -> None:
      super().__init__(parameters)

      self._duration = duration
      self._electrolyzer_rate = np.array(self._parameters.electolyzer_rate)
      self._fuel_volume = np.array(self._parameters.fuel_volume)
      self._tank_volume = np.array(self._parameters.tank_volume)
      self._chamber_temp = np.array(self._parameters.combustion_chamber_temp)
      self._chamber_vol = np.array(self._parameters.combustion_chamber_volume)

  def evaluate(self, state_time: StateTime) -> Dict[str, Any]:

      fuel_mass_i = np.array([state_time.state.fuel_mass])

      grams_electrolyzed = self._duration * self._electrolyzer_rate
      fuel_mass_d = fuel_mass_i - grams_electrolyzed

      chamber_pressure_d = ((grams_electrolyzed / 18.015) * R * self._chamber_temp) / self._chamber_vol

      return {
        "fuel_mass": fuel_mass_d,
        "chamber_pressure": chamber_pressure_d
      }