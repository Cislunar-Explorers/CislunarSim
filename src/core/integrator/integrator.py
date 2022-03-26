from typing import Callable, Dict, List, Union
import numpy as np
from scipy.integrate import solve_ivp
from core.state import State, StateTime


STATE_ARRAY_ORDER = list(State().__dict__.keys())


def array_to_state(values: List) -> State:
    """Converts a numpy array or list into a `State` object.
    The order of the states in the list should be consistent with `STATE_ARRAY_ORDER` if you want meaningful results"""
    return State(dict(zip(STATE_ARRAY_ORDER, values)))


def propagate_state(
    propagate_state_function: Callable, state_time: StateTime, dt: float = 3.0
) -> StateTime:
    """Takes in a state and propagates it over a timestep of `dt` seconds. Returns a new State object at t+dt"""
    t = state_time.time
    state_array = state_time.state.to_array()
    solution = solve_ivp(propagate_state_function, (t, t + dt), list(state_array))
    propagated_state = solution.y[:, -1]  # get the last state in the solution
    propagated_state_obj = StateTime(array_to_state(propagated_state))
    propagated_state_obj.time = solution.t[-1]  # set the time of the propagated state
    return propagated_state_obj
