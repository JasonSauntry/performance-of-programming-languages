#!/usr/bin/env python3
import os.path
import re
from os import environ
from pprint import PrettyPrinter
from subprocess import PIPE
from subprocess import Popen
from subprocess import run
from sys import stderr
from typing import Dict
from typing import Iterable
from typing import List
from typing import Union

import yaml
from tqdm import tqdm

pp = PrettyPrinter()
oldprint = print
print = pp.pprint


def write_data(
    file_path: str,
    operation: str,
    language: str,
    input_size: int,
    time: Union[float, None] = None,
    memory: Union[float, None] = None,
):
    """
    Write data out to the end of a tsv file.

    If file does not exist, create it with headers.
    """
    exists = os.path.exists(file_path)
    with open(file_path, f"{'a' if exists else 'w'}t") as f:
        if not exists:
            f.write("operation\tlanguage\tinput_size\ttime\tmemory\n")
        time = "" if time is None else time
        memory = "" if memory is None else memory
        f.write(f"{operation}\t{language}\t{input_size}\t{time}\t{memory}\n")


def time_program(args: List[str], env: dict = {}):
    """
    Run a program and capture its runtime from stdout.
    """
    result = run(
        args,
        stdout=PIPE,
        stderr=PIPE,
        check=True,
        text=True,
        env={**os.environ, **env},
    )

    try:
        time_line = re.search("time:(\s)*.*", result.stdout).string
    except ParserError as e:
        print(f"Failed to faind `time: ` string in: {result.stdout}", stream=stderr)
        raise
    try:
        _, time_num_start = re.search("time:(\s)*", time_line).span()
        time_num = float(time_line[time_num_start:])
    except ParserError as e:
        print(f"Failed to to parse number from time_line: {time_line}", stream=stderr)

    return time_num


def massif_uncomment(line: str):
    comment = re.search("#", line)
    if comment:
        comment_start, _ = comment.span()
        return line[:comment_start]
    else:
        return line


def massif_get_peak_mem(lines: Iterable[str]):
    mem = 0
    peak_reached = False
    for line in lines:
        line = massif_uncomment(line).strip()

        equals = re.search("=", line)
        if equals is not None:
            _, num_start = equals.span()

        if line == "":
            continue
        elif (
            line.startswith("mem_heap_B")
            or line.startswith("mem_heap_extra_B")
            or line.startswith("mem_stacks_B")
        ) and equals:
            mem_local = int((line[num_start:]))
            mem += mem_local
        elif line.startswith("snapshot"):
            if peak_reached:
                return mem
            else:
                mem = 0
        elif line.startswith("heap_tree=peak"):
            peak_reached = True
    if peak_reached:
        return mem
    else:
        raise ValueError("Function terminated without peak memory")


def measure_memory(args: List[str], env: dict = {}):
    try:
        sub = Popen(
            ["valgrind", "--trace-children=yes", "--tool=massif", *args],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            env={**os.environ, **env},
        )
        sub.communicate()

        massif_path = f"massif.out.{sub.pid}"

        with open(massif_path, "rt") as massif:
            mem = massif_get_peak_mem(massif.readlines())

    except:
        print({"desc": "Failure in measure_memory:", "args": args, "env": env})
        raise
    finally:
        if massif_path and os.path.exists(massif_path):
            os.remove(massif_path)

    return mem


def run_program(
    outfile: str,
    program: List[str],
    size: int,
    mode: str,
    language: str,
    operation: str,
    env: dict = {},
):
    time = None
    memory = None
    if mode == "TIME":
        time = time_program(program, env=env)
    elif mode == "PEAK_MEM":
        memory = measure_memory(program, env=env)

    write_data(outfile, operation, language, size, time, memory)


def read_config(config_path: str) -> dict:
    with open(config_path, "rt") as config_file:
        ret = yaml.load(config_file, yaml.Loader)
    return ret


def run_config(config_path: str) -> None:
    config = read_config(config_path)
    print(config)

    for benchmark in tqdm(
        config["benchmarks"],
        desc="benckmarks",
        leave=None,
    ):
        name = benchmark["name"]
        for mode in tqdm(
            benchmark["modes"],
            desc=f"modes in {name}",
            leave=None,
        ):
            for program in tqdm(
                benchmark["programs"],
                desc=f"languages in {name}",
                leave=None,
            ):
                for size in tqdm(
                    benchmark["sizes"],
                    desc=f"inputs in {name}",
                    leave=None,
                ):
                    run_program(
                        outfile="/tmp/foo.tsv",
                        program=[*program["args"], str(size)],
                        size=size,
                        mode=mode,
                        language=program["language"],
                        operation=name,
                        env=program["env"] if "env" in program else {},
                    )


if __name__ == "__main__":
    run_config("./benchmark_spec.yaml")
