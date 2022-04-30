import pandas as pd
from utils.matplotlib_util import Plot


import argparse


class PlotHelper:
    """This class serves as a helper tool for plotting sim run csvs."""

    def __init__(self) -> None:
        # if called from command line
        # Build the argument parser
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "csv_link",
            type=str,
            help="Plot graph given path to csv file",
        )
        # Parser command line arguments
        args = parser.parse_args()

        self.data = pd.read_csv(args.csv_link)
        self.pl = Plot(self.data)


if __name__ == "__main__":
    data = PlotHelper().pl.plot_data()
