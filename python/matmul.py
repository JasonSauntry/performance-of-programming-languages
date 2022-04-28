#!/usr/bin/env python3

from pprint import PrettyPrinter
import sys
from typing import List

from python.common import timef, run_bench, get_number, rand

pp = PrettyPrinter(stream=sys.stderr)
oldprint = print
print = pp.pprint

matrix = List[List[float]]


def get_matrix(size: int) -> matrix:
    """
    Generate a random ``size`` by ``size`` square matrix.

    :param size: The column and row count of the matrix.
    :return: The matrix.
    """
    return [[get_number() for i in range(size)] for j in range(size)]


def multiply_matrices(a: matrix, b: matrix) -> matrix:
    size = len(a)  # Assume square matrices.
    ret = []
    for i in range(size):
        ret.append([])
        for j in range(size):
            ret[i].append(0.0)
            for k in range(size):
                ret[i][j] += a[k][j] * b[i][k]
    return ret


def act(size: int) -> float:
    """
    Run the benchmark.

    I.e. get two matrixes and time the process of multiplying them.

    :param size: The size of matrices.
    :return: The time required in milliseconds.
    """
    matrix_a = get_matrix(size)
    matrix_b = get_matrix(size)

    time, result_matrix = timef(lambda: multiply_matrices(matrix_a, matrix_b))

    print(
        result_matrix[rand.randint(0, size - 1)][rand.randint(0, size - 1)],
    )

    return time


if __name__ == '__main__':
    run_bench(
        lambda size: act(size),
        description="Naïve matrix multiplication benchmark",
        size_help="Width of the square matrices",
    )
