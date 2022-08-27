from sre_parse import State
from typing import List
from core.integrator.integrator import propagate_state
#from core.models.model import Model
from core.models.model_list import ModelContainer
from core.state import ObservedState, PropagatedOutput, StateTime

class Event:

    #each event has only 1 state?
    def __init__(self, model_container: ModelContainer):
        self.model_container = model_container
    
    def evaluate_model_list(self, state_time: StateTime) -> PropagatedOutput:

        # Evaluate Actuator models to update state
        for actuator_model in self.model_container.actuator:
            state_time.state.update(actuator_model.evaluate(state_time.state))

        # Propagate derived state
        for derived_state_model in self.model_container.derived:
            state_time.state.derived_state.update(
                derived_state_model.evaluate(state_time.time, state_time.state))

        # Evaluate environmental models to propagate state
        new_state_time = propagate_state(self.model_container, state_time)

        # Evaluate sensor models
        temp_state = State()
        for sensor_model in self.model_container.sensor:
            temp_state.update(sensor_model.evaluate(new_state_time.state))
        
        observed_state = ObservedState(temp_state, new_state_time.time)

        return PropagatedOutput(new_state_time, observed_state)