from dataclasses import dataclass
import numpy as np
from typing import Dict, Union

from utils.constants import State_Type

class DerivedState:
    """
    Container class for derived state variables needed for state determination.
    TODO: Concretely document these somewhere.
    """

    def __init__(self, derived_state_dict: Dict = {}):

        # inertia matrix components (kg * m^2). Structure is
        # [[Ixx, Ixy, Ixz], 
        #  [Iyx, Iyy, Iyz], 
        #  [Izx, Izy, Izz]].
        self.Ixx = 0.0
        self.Ixy = 0.0
        self.Ixz = 0.0
        self.Iyx = 0.0
        self.Iyy = 0.0
        self.Iyz = 0.0
        self.Izx = 0.0
        self.Izy = 0.0
        self.Izz = 0.0

        # Kane damping constant
        self.kane_c = 0.0

        # Position column vectors from moon/sun/earth/craft to the origin, where the origin is # the Earth's center of mass.
        # craft to origin
        self.r_co = np.array((0.0, 0.0, 0.0))
        # moon to origin
        self.r_mo = np.array((0.0, 0.0, 0.0))
        # sun to origin
        self.r_so = np.array((0.0, 0.0, 0.0))
        # earth to origin
        self.r_eo = np.array((0.0, 0.0, 0.0))

        # Position column vectors from body to the craft.
        # moon to the craft
        r_mc = np.array((0.0, 0.0, 0.0))
        # sun to the craft
        r_sc = np.array((0.0, 0.0, 0.0))
        # earth to the craft
        r_ec = np.array((0.0, 0.0, 0.0))

        self.update(derived_state_dict)

    def update(self, derived_state_dict: Dict) -> None:
        for key, value in derived_state_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)
