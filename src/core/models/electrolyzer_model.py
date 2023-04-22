#from src.core.models.model import ActuatorModel
from core.models.model import ActuatorModel
from core.parameters import Parameters
from core.state.statetime import StateTime
from typing import Dict, Any
from utils.constants import R, M_WATER
import numpy as np
from utils.log import log

class ElectrolyzerModel(ActuatorModel):
  """Propagates fuel mass and chamber pressure according to electrolysis parameters"""

  def __init__(self, parameters: Parameters) -> None:
      super().__init__(parameters)
      # volume of combustion chamber
      self._chamber_vol = np.array(self._parameters.combustion_chamber_volume)
      # determines whether the electrolyzer is electrolyzing -- this will come from flight software
      self.wasOn = False
      # the time that electrolyzer turns on
      self.onTime = 0.0

  def evaluate(self, state_time: StateTime) -> Dict[str, Any]:
      """Abstracts the electrolysis process according to the model

      Args:
          state_time (StateTime): The input statetime, wrapper object that depicts the current state 
          of the spacecraft and the current time
          

      Returns:
          Dict[str, Any]: The augmented fuel mass and chamber pressure
          desired return: the augumented fuel mass at each specific dt?
      """
      # get the electrolyzer rate from state
      self._electrolyzer_rate = state_time.state.electrolyzer_rate

      # keeps track of the time it turns on and how long it's been on
      if (state_time.state.electrolyzer_on and not self.wasOn):
         wasOn = True
         onTime = state_time.time 
      if (not state_time.state.electrolyzer_on):
         wasOn = False
      else:
         state_time.state.onDuration = state_time.time - onTime

      # get fuel mass at this time
      fuel_mass_i = np.array([state_time.state.fuel_mass])
      chamber_temp = np.array([state_time.state.chamber_temp])
      #kg_electrolyzed = np.array([state_time.state.kg_electrolyzed])
      
      # log the critical chamber temperature
      if (chamber_temp <= np.array(self._parameters.temperature_min) or 
          chamber_temp >= np.array(self._parameters.temperature_max)):
        log.critical("Chamber temp is out of range")

      # if the spacecraft is spinning too slowly, we cannot electrolyze
      if (state_time.state.ang_vel_z < np.array(self._parameters.min_ang_vel)):
         log.critical("Not spinning fast enough")

      # if the water height is too small, we cannot electrolyze
      currHeight = state_time.state.fuel_mass/(np.array(self._parameters.tank_length)*np.array(self._parameters.tank_width))
      minHeight = np.array(self._parameters.min_height)
      if (currHeight < minHeight):
         log.critical("Not enough water")
      
      #non-constant electrolyzer rate

      # calculate updated fuel mass
      # state_time.state.kg_electrolyzed += self._duration * self._electrolyzer_rate
      #fuel_mass_d = fuel_mass_i - kg_electrolyzed

      moleWaterRate = self._electrolyzer_rate * (1/M_WATER)

      h2Rate = moleWaterRate
      o2Rate = moleWaterRate * 0.5

      # return updated fuel mass
      return {
        "Electrolyzer rate (kg/s)": self._electrolyzer_rate, "H2 Production Rate (Moles/s)": h2Rate, 
        "O2 Production Rate (moles/s)": o2Rate, "Time it was on": onTime
      }
