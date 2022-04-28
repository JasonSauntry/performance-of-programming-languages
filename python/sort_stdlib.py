#!/usr/bin/env python3

from python.common import timef, run_bench, rand, get_number

def act(size: int) -> int:
    l = [get_number() for i in range(size)]

    time, _ = timef(lambda: l.sort())

    if len(l) < 50:
        print(l)
    else:
        print(l[rand.randint(0, len(l) - 1)])

    return time


if __name__ == '__main__':
    run_bench(
        lambda size: act(size),
        description="Optimized matrix multiplication benchmark",
        size_help="Width of the square matrices",
    )
