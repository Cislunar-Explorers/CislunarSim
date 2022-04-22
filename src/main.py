from utils.constants import ModelEnum
from utils.log import log
from utils.data_handling import states_to_df, df_to_csv
from typing import List, Union, cast
from core.config import Config
from core.sim import CislunarSim
from core.state import PropagatedOutput
import pandas as pd

import argparse

_DESCRIPTION = """CISLUNAR Simulation Runner!"""


class SimRunner:
    """
    This class serves as the main entry point to the sim.
    """

    def __init__(self, config: Config = None) -> None:
        """
        Runs the sim from specified config path. Called from command-line.

        Input structure: "python3 src/main.py {file path}"
        Example: "python3 src/main.py configs/freefall.json"
        """
        # if called from somewhere within the program, with config objects
        if config:
            self._sim = CislunarSim(config)

        # if called from command line
        else:
            # Build the argument parser
            parser = argparse.ArgumentParser(description=_DESCRIPTION)
            parser.add_argument(
                "config",
                type=str,
                help="Initialize simulation with given path to json config file.",
            )

            # Parser command line arguments
            args = parser.parse_args()
            self._sim = CislunarSim(Config.make_config(args.config))

        self.state_history = []

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
    data = SimRunner().run()
    df_to_csv(data)
