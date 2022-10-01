from typing import Dict, Any
from core.models.model import ActuatorModel
from core.state.statetime import StateTime

class AttitudeActuatorModel(ActuatorModel):
    def __init__(self, parameters):
        super().__init__(parameters)

    def evaluate(self, state_time):
        return self.d_state(state_time)

    def d_state(self, state_time: StateTime) -> Dict[str, Any]:
        """Function which evaluates the differential equation:
            dy / dt = f(t, y)
            for the current state. "y" is a state vector (not just one variable)

        Args:
            state_time (StateTime): Current simulation StateTime

        Returns:
            Dict[str, Any]: the name of each state being updated, and the
                value of its derivative. The keys of this dictionary must be in
                `STATE_ARRAY_ORDER`
        """
        ...
