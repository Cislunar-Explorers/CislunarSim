from dataclasses import dataclass
import numpy as np
from typing import Dict, Union

from utils.constants import State_Type

class DerivedState:
    """
    Container class for derived state variables needed for state determination.
    TODO: Concretely document what these are.
    """

    def __init__(self, derived_state_dict: Dict = {}):
        self.update(derived_state_dict)

    def update(self, derived_state_dict: Dict) -> None:
        for key, value in derived_state_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)
