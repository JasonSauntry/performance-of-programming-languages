from random import Random
from time import perf_counter
from typing import Tuple, Callable

import argparse

rand = Random()
rand.seed()


def get_number():
    return rand.normalvariate(0, 1)

def milliseconds(seconds: float) -> float:
    """
    Given a time in seconds, return the same time in milliseconds.
    """
    return seconds * 1000

def timef(f: Callable[[], any]) -> Tuple[float, any]:
    """
    Run the function, get the time taken in milliseconds.

    :return:
    """
    start = perf_counter()
    ret = f()
    end = perf_counter()

    return (milliseconds(end - start), ret)

def run_bench(
    f: Callable[[int], float],
    description="Run some benchmark",
    size_help="The benchmark's input size",
) -> None:
    """
    Run a benchmark and print the runtime to stdout.

    :param f:
        The benchmark.

        Given a size, do something and return the time taken in milliseconds.
    """
    parser = argparse.ArgumentParser(description="Run a benchmark")

    parser.add_argument('size', help=size_help, type=int)

    args = parser.parse_args()

    time = f(args.size)

    print(f"time: {time}")
