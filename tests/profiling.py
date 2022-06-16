"""profiling.py - a util for finding what's slowing down your CislunarSim runs

    Run this sim the same way you would run main.py: `python tests/profiling.py configs/... -v`
    A sim with the config file and other args you specify will be run, its data stored, and the
    runtime profile of the sim will be stored to `for_snakeviz.prof`, where you can inspect the
    results with `snakeviz for_snakeviz.prof`. Install it via `pip install snakeviz`
    """

import cProfile
import pstats

from main import run_sim


def main():
    # The following line requires Python 3.8+
    # https://github.com/mCodingLLC/VideosSampleCode/issues/5
    with cProfile.Profile() as pr:
        run_sim()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="for_snakeviz.prof")
    print("Writing to for_snakeviz.prof")
    # Now you can investigate the results with `snakevix for_snakeviz.prof`


if __name__ == "__main__":
    main()
