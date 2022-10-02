from typing import List, Optional, Union
import time
import pandas as pd
from core.state.statetime import PropagatedOutput
from dataclasses import asdict
from utils.constants import SIM_ROOT
from pathlib import Path
from matplotlib.animation import FuncAnimation, PillowWriter


def states_to_df(states: List[PropagatedOutput]) -> pd.DataFrame:
    """Converts [states] to a DataFrame to use for plotting

    Args:
        states (List[PropagatedOutput]): the current state

    Returns:
        pd.DataFrame: a Pandas DataFrame containing the states' data
    """
    dataframes: List[pd.DataFrame] = []
    for output in states:
        flattened_output_dict = pd.json_normalize(asdict(output))
        single_dataframe = pd.DataFrame.from_dict(flattened_output_dict)
        dataframes.append(single_dataframe)

    complete_df = pd.concat(dataframes)
    return complete_df


def df_to_csv(dataframe: pd.DataFrame, path: Optional[Union[str, Path]] = None):
    """Creates and writes the data in [dataframe] into a csv file at [path]

    Args:
        dataframe (pd.DataFrame): Pandas DataFrame containing state data
        path (Optional[Union[str, Path]]): path of the CSV to write the state data to
    """
    if path is None:
        path = SIM_ROOT / "runs"
    dataframe.to_csv(f"{path}/cislunarsim-{current_int_time()}.csv")


def save_anim(anim: FuncAnimation):
    """Saves [anim] as gif file under [/playbacks].

    Args:
        anim (FuncAnimation): The animation of the sim playback.

    We eventually also want to be able to embed this animation onto a web
    playback app. We can pass around gif files, or we could embed the animation
    as an HTML tag. These links give some leads on how to do that.
    https://stackoverflow.com/questions/55163024/how-to-convert-matplotlib-animation-to-an-html5-video-tag
    https://www.programcreek.com/python/example/76369/matplotlib.animation
    """
    writervideo = PillowWriter(fps=60)
    anim.save(
        f"{SIM_ROOT}/playbacks/playback-{current_int_time()}.gif", writer=writervideo
    )


def current_int_time():
    return int(time.time())
