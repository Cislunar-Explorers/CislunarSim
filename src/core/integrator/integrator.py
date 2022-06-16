from scipy.integrate import solve_ivp
from core.state.statetime import StateTime
from core.state.state import array_to_state
from core.models.model_list import ModelContainer
from utils.constants import D_T


def propagate_state(
    models: ModelContainer,
    state_time: StateTime,
    dt: float = D_T,
) -> StateTime:
    """Takes in a state and propagates it over a timestep of `dt` seconds.
    Returns a new State object at t+dt"""
    t = state_time.time
    propagate_state_function = models.state_update_function
    state_array = state_time.state.to_array()
    solution = solve_ivp(propagate_state_function, (t, t + dt), state_array)
    propagated_state = solution.y[:, -1]  # get the last state in the solution
    propagated_state_obj = StateTime(array_to_state(propagated_state), solution.t[-1])
    return propagated_state_obj
