from typing import List
import time
import pandas as pd
from core.state import PropagatedOutput
from dataclasses import asdict


def states_to_df(states: List[PropagatedOutput]) -> pd.DataFrame:
    dataframes: List[pd.DataFrame] = []
    for output in states:
        flattened_output_dict = pd.json_normalize(asdict(output))
        single_dataframe = pd.DataFrame.from_dict(flattened_output_dict)
        dataframes.append(single_dataframe)

    complete_df = pd.concat(dataframes)
    return complete_df


def df_to_csv(dataframe: pd.DataFrame):
    dataframe.to_csv(f"runs/cislunarsim-{time.time()}")
