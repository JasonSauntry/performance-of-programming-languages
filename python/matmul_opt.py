#!/usr/bin/env python3
import os

import numpy as np
from numpy.random import default_rng

from python.common import rand
from python.common import run_bench
from python.common import timef

rng = default_rng()


def get_matrix(size: int) -> np.ndarray:
    return rng.normal(size=(size, size))


def act(size: int) -> float:
    """
    Run the benchmark.

    I.e. get two matrixes and time the process of multiplying them.

    :param size: The size of matrices.
    :return: The time required in milliseconds.
    """
    matrix_a = get_matrix(size).astype(np.float64)
    matrix_b = get_matrix(size).astype(np.float64)

    time, result_matrix = timef(lambda: matrix_a @ matrix_b)

    print(
        result_matrix[rand.randint(0, size - 1)][rand.randint(0, size - 1)],
    )

    return time


if __name__ == "__main__":
    run_bench(
        lambda size: act(size),
        description="Optimized matrix multiplication benchmark",
        size_help="Width of the square matrices",
    )
