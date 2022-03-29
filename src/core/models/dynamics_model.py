import numpy as np
from core.models.model import Model
from typing import Dict, Any
from core.state import State
from core.parameters import Parameters

class InertiaModel(Model):
    def __init__(self, parameters: Parameters) -> None:
        super.__init__(parameters)

    def evaluate(self, state: State) -> Dict[str, Any]:
        return super().evaluate(state)

    def d_state(self, state: State) -> Dict[str, Any]:
        fill_frac = state.fill_frac

        dcm = np.array([[0, 1, 0],[0, 0, -1],[-1, 0, 0]], dtype=np.int32)
        dcmT = np.transpose(dcm)

        # Inertia tensor when full. Structure is:
        # [[Ixx, Ixy, Ixz], 
        #  [Iyx, Iyy, Iyz], 
        #  [Izx, Izy, Izz]].
        # Units are (kg * m^2).
        idf = np.array([[933513642.20, 260948256.18, 430810000.30],
                        [260948256.18, 1070855457.07, 387172545.62],
                        [430810000.30, 387172545.62, 629606813.62]], dtype=np.float64) * 1e-9
        idf_b = np.matmul(np.matmul(dcm, idf), dcmT)

        # Inertia tensor at 125 mL. Structure is:
        # [[Ixx, Ixy, Ixz], 
        #  [Iyx, Iyy, Iyz], 
        #  [Izx, Izy, Izz]].
        # Units are (kg * m^2).
        idi = np.array([[855858994.14, 229481961.55, 377087149.13],
                        [229481961.55, 963124288.81, 353943859.15],
                        [377087149.13, 353943859.15, 559805590.96]], dtype=np.float64) * 1e-9
        idi_b = np.matmul(np.matmul(dcm, idi), dcmT)

        # Determine inertia tensor for Oxygen via linear interpolation as a function of fill fraction.
        ioxy = (idf_b - idi_b) * fill_frac + idi_b
        
        return {"Ixx": ioxy[0][0], 
                "Ixy": ioxy[0][1], 
                "Ixz": ioxy[0][2], 
                "Iyx": ioxy[1][0], 
                "Iyy": ioxy[1][1], 
                "Iyz": ioxy[1][2], 
                "Izx": ioxy[2][0], 
                "Izy": ioxy[2][1], 
                "Izz": ioxy[2][2]} 
    

class OmegaModel(Model):
    """ Class for the angular velocity model. """
    def __init__(self, parameters: Parameters) -> None:
        super.__init__(parameters)

    def evaluate(self, state: State) -> Dict[str, Any]:
        return super().evaluate(state)

    def d_state(self, state: State) -> Dict[str, Any]:
        return super().d_state(state)