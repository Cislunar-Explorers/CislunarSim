#from core.models.model import ActuatorModel
#from core.parameters import Parameters
#from core.state.statetime import StateTime
#from typing import Dict, Any
import numpy as np
import matplotlib.pyplot as plt
import cantera as ct
import numpy as np

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

        ct.suppress_thermo_warnings(True)

        d = 3 * 0.0254  # in meters
        h = (3.968 + 1.618) * 0.0254  # in meters
        d2 = 0.05 * 0.0254  # in meters
        d2mm = d2 * 1000
        d3 = 0.305 * 0.0254  # in meters
        A1 = np.pi * d ** 2 / 4 #Cross-sectional area of the nozzle throat (in square meters)
        A2 = np.pi * d2 ** 2 / 4 #Cross-sectional area of the nozzle exit (in square meters)
        A3 = np.pi * d3 ** 2 / 4  # Cross-sectional area of the combustion chamber (in square meters)
        vc = h * np.pi * d ** 2 / 4
        plim1 = 45 * 6894.76  # in Pascals
        plim2 = 100 * 6894.76  # in Pascals
        RH2 = 4.124e3  # in J/kg*K
        RO2 = 0.2598e3  # in J/kg*K
        RH2O = 0.4615e3  # in J/kg*K

        gas1 = ct.Solution('gri30.xml')
        gas2 = ct.Solution('gri30.xml')

        gas1.TP = 298.0, plim1, 'H2:2,O2:1'
        gas2.TP = 298.0, 1

        gas1.equilibrate('SV')
        combustor = ct.IdealGasReactor(gas1)
        exhaust = ct.Reservoir(gas2)
        combustor.volume = vc
        network = ct.ReactorNet([combustor])
        Choke = ct.MassFlowController(combustor, exhaust)
        CpH2O = 2532.8  # in J/kg*K
        CvH2O = 2071.2  # in J/kg*K
        RH2O = CpH2O - CvH2O
        gamma = CpH2O / CvH2O
        calc = (gamma + 1) / (2 * (gamma - 1))
        arearatio = A2 / A3
        int = arearatio * 1 / ((1 + (gamma - 1) / 2) ** calc)
        M3 = ct.oneD.solve_area_ratio(gas2, A2, A3, int, gamma=gamma)
        dt = 0.0001 #time step
        tend = 1
        t = np.arange(0, tend + dt, dt)
        m = np.zeros_like(t)
        P = np.zeros_like(t)
        mdot = np.zeros_like(t)
        mdot[0] = 0
        for i, time in enumerate(t[:-1]):
            mdot[i] = Choke.mass_flow_rate
            network.advance(time + dt)
            Taft = combustor.thermo.T
            Paft = combustor.thermo.P
            m[i] = combustor.mass
            P[i] = Paft
            if Paft > plim2:
                mdot[i+1] = A2 * Paft * np.sqrt(gamma/RH2O) * ((gamma+1)/2)**num / np.sqrt(Taft)
                Pc = P[i] #Pressure in combustion chamber
            else:
                mdot[i+1] = 0 #Reset to zero if we've gone over
                P[i] = plim2
                # return updated fuel mass and chamber pressure
        Pc = P[-1]
        P3 = Pc / ((1 + (gamma - 1) / 2 * M3 ** 2) ** (gamma / (gamma - 1)))
        #Thrust & Impulse
        Force = P3 * A3 / mdot[-1]
        Impulse = np.sum(Force, axis=0) * dt
        #Position = 1;
        #Velocity = 1;
        #Return
        return {
          "thrust": Force,
          "impulse": Impulse,
          #"position": Position,
          #"velocity": Velocity
        }