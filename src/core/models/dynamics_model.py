import numpy as np
from core.models.model import Model
from typing import Dict, Any
from core.state import State
from core.parameters import Parameters

class InertiaModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        self._parameters = parameters

    def evaluate(self, state: State) -> Dict[str, Any]:
        # TODO: wrap d_state with something (error checking?)
        delta_state = self.d_state(state)
        return delta_state

    def d_state(self, state: State) -> Dict[str, Any]:
        fill_frac = state.fill_frac

        dcm = np.array([[0, 1, 0],[0, 0, -1],[-1, 0, 0]], dtype=np.int32)
        dcmT = np.transpose(dcm)

        # Inertia tensor at 125 mL. Structure is:
        # [[Ixx, Ixy, Ixz], 
        #  [Iyx, Iyy, Iyz], 
        #  [Izx, Izy, Izz]].
        # Units are (kg * m^2).
        idi = np.array([[855858994.14, 229481961.55, 377087149.13],
                        [229481961.55, 963124288.81, 353943859.15],
                        [377087149.13, 353943859.15, 559805590.96]], dtype=np.float64) * 1e-9
        idi_b = np.matmul(np.matmul(dcm, idi), dcmT)

        # Inertia tensor when full. Structure is:
        # [[Ixx, Ixy, Ixz], 
        #  [Iyx, Iyy, Iyz], 
        #  [Izx, Izy, Izz]].
        # Units are (kg * m^2).
        idf = np.array([[933513642.20, 260948256.18, 430810000.30],
                        [260948256.18, 1070855457.07, 387172545.62],
                        [430810000.30, 387172545.62, 629606813.62]], dtype=np.float64) * 1e-9
        idf_b = np.matmul(np.matmul(dcm, idf), dcmT)

        # Determine inertia tensor for Oxygen via linear interpolation as a function of fill fraction.
        ioxy = (idf_b - idi_b) * fill_frac + idi_b
        pass
    

class DynamicsModel():
    """ Class for the dynamics model. """
    ...