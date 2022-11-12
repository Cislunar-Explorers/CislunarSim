from utils.log import log
from utils.data_handling import states_to_df, df_to_csv
import logging
from typing import Union
from core.config import Config
from core.sim import CislunarSim
import pandas as pd
from utils.matplotlib_util import Plot


import argparse


_DESCRIPTION = """Cislunar Sim Runner!"""


class SimRunner:
    """This class serves as the main entry point to the sim."""

    def __init__(self, config: Union[Config, None] = None) -> None:
        """Runs the sim from specified config path or from a Config Object.

        Input structure:
            "python3 src/main.py {file path} [-v]"
            File path is a required argument, verbose is an optional argument.
        Example:
            "python3 src/main.py configs/freefall.json"
            "python3 src/main.py configs/test_angles.json -v"
        """
        # if called from somewhere within the program, with config objects
        if isinstance(config, Config):
            self._sim = CislunarSim(config)

        # if called from command line
        else:
            # Build the argument parser
            parser = argparse.ArgumentParser(description=_DESCRIPTION)
            parser.add_argument(
                "config",
                type=str,
                help="initialize simulation with given path to json config file",
            )
            parser.add_argument(
                "-v",
                "--verbose",
                action="store_true",
                help="set the logging level to DEBUG instead of INFO",
            )
            parser.add_argument(
                "-p",
                "--plot",
                action="store_true",
                help="plot the sim output"
            )
            parser.add_argument(
                "-o",
                "--out",
                const="None",
                nargs="?",
                help="write the sim output to a CSV file"
            )
            
            # Parser command line arguments
            args = parser.parse_args()

            # Set Logging level of "Sim" based on --verbose argument.
            log.setLevel(logging.DEBUG) if args.verbose else log.setLevel(logging.INFO)
            self.out = args.out
            self.plot = args.plot
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
        run_df = states_to_df(states)

        log.setLevel(logging.INFO)  # to prevent being spammed by matplotlib's debug logs (doesn't work)

        if self.plot:
            data_plot = Plot(run_df)
            data_plot.plot_data()
        
        return run_df

    def _run(self):
        while self._sim.should_run:
            try:
                updated_states = self._sim.step()
                self.state_history.append(updated_states)
            except (Exception) as e:
                log.critical("Stopping sim due to unhandled exception:")
                log.error(e, exc_info=True)
                break
            except (KeyboardInterrupt):
                log.info("Stopping sim")
                break

        return self.state_history


def run_sim():
    sim = SimRunner()
    data = sim.run()

    # don't store any data if the sim was not specified to output to a file
    if sim.out != "None":
        df_to_csv(data, sim.out)


if __name__ == "__main__":
    run_sim()
