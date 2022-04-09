from dataclasses import asdict
from core import models
from utils.constants import ModelEnum
from utils.log import log
from typing import List, Optional
from core.config import Config
from core.sim import CislunarSim, PropagatedOutput
import pandas as pd
import time


class SimRunner:
    """
    This class serves as the main entry point to the sim.
    """

    def __init__(self, config_path: Optional[str] = None) -> None:
        # TODO: config = core.config.make_config(config_path)
        config = Config()
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
    dataframes = []
    for output in states:
        flattened_output_dict = pd.json_normalize(asdict(output))
        single_dataframe = pd.DataFrame.from_dict(flattened_output_dict)
        dataframes.append(single_dataframe)

    complete_df = pd.concat(dataframes)
    complete_df.to_csv(f"runs/cislunarsim-{time.time()}")


if __name__ == "__main__":
    # freefall from ~4000km altitude to test basic functionality of the sim  
    initial_condition = {"x": 10_000_000, "y": 1_000, "z": 1_000, "ang_vel_x": 4.5}
    models_to_use = [ModelEnum.PositionModel]
    conf = Config({}, initial_condition, models=models_to_use)