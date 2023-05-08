from dataclasses import dataclass
from core.state.state import State, ObservedState
from core.state.derived_state import DerivedState
from core.models.derived_models import DERIVED_MODEL_LIST
from utils.constants import State_Type
from typing import Dict, Union


@dataclass
class StateTime:
    """This class associates the state with the time."""

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


def apply_coupled_initial_conditions(st: StateTime) -> None:
    """Updates the input statetime with any coupled initial conditions"""
    # page 5 of Bernardini_Pietro_2022_Spring_ACS.docx:
    # initial condition of angular velocity of kane damper = spacecraft spin rate
    if st.derived_state.ang_vel.any():
        st.state.w_kane_x = float(st.derived_state.ang_vel[0][0])
        st.state.w_kane_y = float(st.derived_state.ang_vel[1][0])
        st.state.w_kane_z = float(st.derived_state.ang_vel[2][0])


@dataclass
class PropagatedOutput:
    """This is a container class that holds a true_state and its corresponding observed_state."""

    true_state: StateTime
    observed_state: ObservedState
    # commanded_actuations
