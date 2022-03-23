from typing import Callable, Dict, List, Union
import numpy as np
from scipy.integrate import solve_ivp
from core.state import State


# TODO define all states in state.py
STATE_ARRAY_ORDER = ["time", 
                     "pos_x", "pos_y", "pos_z", 
                     "vel_x", "vel_y", "vel_z"]


def dict_state_to_array(state: State) -> np.ndarray:
    """Converts a `State` object into an numpy array. 
    Most ODE solvers only work with lists/arrays, 
    so we need to convert our state dictionary into a list to get solved by an ode solver.
    The order of the states in the list are defined in `STATE_ARRAY_ORDER`, which needs updating"""
    return np.array([state[key] for key in STATE_ARRAY_ORDER])

def array_state_to_dict(state: Union[np.ndarray, List]) -> State:
    """Converts a numpy array or list into a `State` dictionary object. 
    The order of the states in the list should be consistent with `STATE_ARRAY_ORDER` if you want meaningful results"""
    return State(zip(STATE_ARRAY_ORDER, state))


def propagate_state(propagate_state_function: Callable, state: State, dt:float = 3.0) -> State:
    """Takes in a state and propagates it over a timestep of `dt` seconds. Returns a new State object at t+dt"""
    t = state["time"]
    state_array = dict_state_to_array(state)
    solution = solve_ivp(propagate_state_function, (t, t+dt), state_array)
    propagated_state = solution.y[:,-1] # get the last state in the solution
    propagated_state[0] = solution.t[-1] # set the time of the propagated state
    propagated_state_obj = array_state_to_dict(propagated_state)
    return propagated_state_obj


if __name__ == "__main__":
    # quick test to see if this thing works
    STATE_ARRAY_ORDER = ["time", "pos_x", "pos_y", "pos_z"]

    def f(t,y): # exponential decay function, just for testing purposes
        return -0.25 * y

    initial_state = State({"time": 0, "pos_x": 1, "pos_y": -10, "pos_z": 1})
    final_state = propagate_state(f, initial_state)
    print(final_state)