from abc import ABC, abstractmethod
from utils.astropy_util import get_body_position
from typing import Dict
import numpy as np
from utils.constants import BodyEnum


class DerivedStateModel(ABC):
    """
    Abstract Base class for all models this sim uses.
    """

    def __init__(self) -> None:
        """Model __init__
        All models will be dependent on some parameters, so we load them in
        here.
        Args:
            parameters (Parameters): Instance of the parameters class gets
            passed in to be accessible by the model.
        """
        ...

    @abstractmethod
    def evaluate(self, state_time: Dict):
        """
        Evaluates the model based on the
            current state.
        An instance of State is required to evaluate the model, (because each
            model should be dependent on the state of the system.)
        Args:
            state (State): a instance of a State class.

        Returns:
            _type_: Defined in concrete instantiation of subclasses.
        """


class DerivedAttitude(DerivedStateModel):
    ...


class DerivedPosition(DerivedStateModel):
    """Updates position column vectors for use in the position dynamics model."""

    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, t: float, state: Dict) -> Dict[str, np.ndarray]:

        # Position column vectors from moon/sun/earth/craft to the origin, where the origin is
        # the Earth's center of mass.
        # Craft to origin
        r_co = np.array([state["x"], state["y"], state["z"]])
        # Moon to origin
        r_mo = np.array(get_body_position(10 * t // 10, BodyEnum.Moon))
        # Sun to origin
        r_so = np.array(get_body_position(10 * t // 10, BodyEnum.Sun))
        # Earth to origin (Note: Earth is at the origin in GCRS)
        r_eo = np.array((0.0, 0.0, 0.0))

        # Position column vectors from body to the craft.
        # Moon to the craft
        r_mc = np.subtract(r_mo, r_co)
        # Sun to the craft
        r_sc = np.subtract(r_so, r_co)
        # Earth to the craft
        r_ec = np.subtract(r_eo, r_co)

        return {
            "r_co": r_co,
            "r_mo": r_mo,
            "r_so": r_so,
            "r_eo": r_eo,
            "r_mc": r_mc,
            "r_sc": r_sc,
            "r_ec": r_ec,
        }


DERIVED_MODEL_LIST = [DerivedPosition()]
