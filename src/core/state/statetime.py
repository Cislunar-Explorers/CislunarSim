from dataclasses import dataclass
from core.state.state import State, ObservedState
from core.state.derived_state import DerivedState
from core.models.derived_models import DERIVED_MODEL_LIST
from utils.constants import State_Type
from typing import Dict, Union


@dataclass
class StateTime:
    """ This class associates the state with the time. """

    state: State = State()
    time: float = 0.0
    derived_state: DerivedState = DerivedState()

    def __post_init__(self):
        for derived_state_model in DERIVED_MODEL_LIST:
            self.update_derived(derived_state_model.evaluate(self.time, self.state))

    @classmethod
    def from_dict(cls, statetime_dict: Dict[str, State_Type]):
        """Generates a new StateTime instance from an input dictionary.
            Can be called via `StateTime.from_dict(...)` to make a new StateTime object

        Args:
            statetime_dict (Dict[str, State_Type]): _description_

        Returns:
            StateTime: _description_
        """
        try:
            time = statetime_dict.pop("time")
        except KeyError:
            time = 0.0

        return cls(State(**statetime_dict), time=time)

    def update(self, state_dict: Dict[str, Union[int, float, bool]]) -> None:
        """update() is a procedure that updates the fields of the state with specified key/value pairs in state_dict.
        If a key in the `state_dict` is not defined as an attribute in State.__init__, it will be ignored.
        """
        self.state.update(state_dict)

    def update_derived(self, state_dict: Dict) -> None:
        """update_derived() is a procedure that updates the fields of the derived state with specified key/value pairs
        in state_dict.
        If a key in the `state_dict` is not defined as an attribute in DerivedState.__init__, it will be ignored.
        """
        self.derived_state.update(state_dict)


@dataclass
class PropagatedOutput:
    """This is a container class that holds a true_state and its corresponding observed_state."""

    true_state: StateTime
    observed_state: ObservedState
    # commanded_actuations
