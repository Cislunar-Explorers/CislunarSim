from utils.constants import ModelEnum
from utils.log import log
from utils.data_handling import states_to_df, df_to_csv
from typing import List, Union, cast
from core.config import Config
from core.sim import CislunarSim
from core.state import PropagatedOutput
import pandas as pd


class SimRunner:
    """
    This class serves as the main entry point to the sim.
    """

    def __init__(self, config: Union[str, Config]) -> None:
        if type(config) is str:
            # TODO: config = core.config.make_config(config_path)
            config = Config({}, {})

        self._sim = CislunarSim(cast(Config, config))
        self.state_history: List[PropagatedOutput] = []

    def run(self) -> pd.DataFrame:
        """Runs the sim and returns the truth and observed states in a pandas dataframe.
        Both the truth and observed states between each control cycle get thrown out
        (this is something we'll probably want to change)

        Returns:
            pd.DataFrame: Dataframe of the true and observed states at each instant of observation.
        """
        states = self._run()
        return states_to_df(states)

    def _run(self):
        while self._sim.should_run:
            try:
                updated_states = self._sim.step()
                self.state_history.append(updated_states)
            except (Exception, KeyboardInterrupt) as e:
                log.critical("Stopping sim due to unhandled exception:")
                log.error(e, exc_info=True)
                break

        return self.state_history


if __name__ == "__main__":
    # freefall from ~4000km altitude to test basic functionality of the sim
    initial_condition = {"x": 10_000_000, "y": 1_000, "z": 1_000, "ang_vel_x": 4.5, "time": 0.0}
    models_to_use = [ModelEnum.PositionModel, ModelEnum.GyroModel]
    conf = Config({}, initial_condition, models=models_to_use)

    test_sim = SimRunner(conf)
    data = test_sim.run()
    df_to_csv(data)
