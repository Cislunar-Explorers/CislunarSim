import cProfile
import pstats

from main import freefall


def main():
    # The following line requires Python 3.8+
    # https://github.com/mCodingLLC/VideosSampleCode/issues/5
    with cProfile.Profile() as pr:
        freefall()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="for_snakeviz.prof")


if __name__ == "__main__":
    main()
