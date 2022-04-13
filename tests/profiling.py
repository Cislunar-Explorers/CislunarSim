import cProfile
import pstats

from main import freefall


def main():
    with cProfile.Profile() as pr:
        freefall()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="for_snakeviz.prof")


if __name__ == "__main__":
    main()
