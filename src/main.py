from utils.log import log
from typing import List, Optional
import core.config
from core.sim import CislunarSim, PropagatedOutput


class SimRunner:
    """
    This class serves as the main entry point to the sim.
    """

    def __init__(self, config_path: Optional[str] = None) -> None:
        config = core.config.make_config(config_path)
        self._sim = CislunarSim(config)
        self.state_history: List[PropagatedOutput] = []

    def run(self):
        states = self._run()
        export_states_to_csv(states)

    def _run(self):
        while self._sim.should_run:
            try:
                updated_states = self._sim.step()
                self.state_history.append(updated_states)
            except Exception as e:
                log.critical("Stopping sim due to unhandled exception:")
                log.error(e, exc_info=True)
                break

        return self.state_history

def export_states_to_csv(states: List[PropagatedOutput]) -> None:
    # convert list of PropagatedOutputs to List of flattened Dicts
    
    state_dict_list = []