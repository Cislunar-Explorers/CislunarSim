from os import stat
from typing import Callable, List, Dict, Type
import numpy as np
# from core.models.model import ActuatorModel, EnvironmentModel, SensorModel
from core.models.derived_model_list import DerivedStateModel
from core.state import State, array_to_state
from core.derived_state import DerivedState
from core.config import Config
from utils.constants import BodyEnum, ModelEnum, State_Type
from utils.astropy_util import get_body_position

class DerivedPosition(DerivedStateModel):
    """Updates position column vectors for use in the position dynamics model."""

    def __init__(self, parameters) -> None:
        super().__init__(parameters)

    def evaluate(self, t: float, state: State) -> Dict[str, State_Type]:
        # Position column vectors from moon/sun/earth/craft to the origin, where the origin is # the Earth's center of mass.
        # craft to origin
        r_co = np.array([state.x, state.y, state.z])
        # moon to origin
        r_mo = np.array(get_body_position(t, BodyEnum.Moon))
        # sun to origin
        r_so = np.array(get_body_position(t, BodyEnum.Sun))
        # earth to origin
        r_eo = np.array((0.0, 0.0, 0.0))  # Earth is at the origin in GCRS

        # Position column vectors from body to the craft.
        # moon to the craft
        r_mc = np.subtract(r_mo, r_co)
        # sun to the craft
        r_sc = np.subtract(r_so, r_co)
        # earth to the craft
        r_ec = np.subtract(r_eo, r_co)

        return {
            'r_co': r_co,
            'r_mo': r_mo,
            'r_so': r_so,
            'r_mc': r_mc,
            'r_sc': r_sc,
            'r_ec': r_ec,
        }