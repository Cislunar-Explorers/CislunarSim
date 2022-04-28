from typing import Callable
import numpy as np
from scipy.integrate import solve_ivp
from core.state import StateTime, array_to_state


def propagate_state(
    propagate_state_function: Callable[[float, np.ndarray], np.ndarray],
    state_time: StateTime,
    dt: float = 3.0,
) -> StateTime:
    """Takes in a state and propagates it over a timestep of `dt` seconds.
    Returns a new State object at t+dt"""
    t = state_time.time
    state_array = state_time.state.to_array()
    solution = solve_ivp(propagate_state_function, (t, t + dt), state_array)
    propagated_state = solution.y[:, -1]  # get the last state in the solution
    propagated_state_obj = StateTime(array_to_state(propagated_state), solution.t[-1])
    return propagated_state_obj
