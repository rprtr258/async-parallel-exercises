#!/usr/bin/env python
from typing import Any, Dict, List, Tuple
from subprocess import Popen, PIPE
from logging import info, basicConfig, INFO
from time import time_ns
from os import environ
from itertools import product

from yaml import safe_load
import matplotlib.pyplot as plt

def cmd(file: str, params: Tuple[Tuple[str, Any]]) -> List[str]:
    return ["python", file] + sum([[f"-{param}", str(value)] for param, value in params], [])

def bench_label(file: str, params: Tuple[Tuple[str, Any]], dims: List[Dict[str, Any]]) -> str:
    dims_dict = {x["name"]: x for x in dims}
    params_list = [
        (p[0], p[1])
        for p in params if (lambda x: not "show" in x or x["show"])(dims_dict[p[0]])
    ]
    params = ','.join(f'{p[0]}={p[1]}' for p in params_list)
    return f"{file}({params})"

def bench_cmd(cmd_line: List[str]) -> List[int]:
    times = []
    for _ in range(tries):
        time_start = time_ns() / 1000000000
        process = Popen(cmd_line, stdout=PIPE)
        _, _ = process.communicate()
        time_end = time_ns() / 1000000000
        times.append(time_end - time_start)
    return times

def make_save_plot(data):
    N = len(data.keys())
    fig, ax = plt.subplots()
    fig.set_size_inches((N / 1.3, N / 2))
    ax.barh(list(range(N)), data.values())
    ax.set_yticks(list(range(N)))
    ax.set_yticklabels(data.keys())
    ax.invert_yaxis()
    ax.set_xlabel("Time (in secs)")
    ax.set_title("map(is_prime)")
    ax.grid(axis="x")
    plt.subplots_adjust(left=0.6, bottom=0.2)
    fig.savefig("bench.png")

# TODO: add colors
if __name__ == "__main__":
    basicConfig(level=INFO)
    with open("bench_list.yaml", "r") as fd:
        config = safe_load(fd.read())
    serial, files, dims, tries = config["serial"], config["files"], config["dims"], int(config["tries"])
    if "BENCH_ARGS" in environ:
        args = list(map(lambda x: x.split("="), environ["BENCH_ARGS"].split(",")))
        dims = dims + [{
            "name": arg_name,
            "values": [arg_value]
        } for arg_name, arg_value in args]

    params_list = list(product(*map(lambda dim: list(map(lambda v: (dim["name"], v), dim["values"])), dims)))
    data = {}

    for params in params_list:
        label = "serial"
        cmd_line = cmd(serial, params)
        times = []
        info(f"Started bench '{label}'")
        times = bench_cmd(cmd_line)
        data[label] = min(times)
        info(f"min: {data[label]:.2f}s")
        break

    for file in files:
        for params in params_list:
            label = bench_label(file[:-3], params, dims)
            cmd_line = cmd(file, params)
            times = []
            info(f"Started bench '{label}'")
            times = bench_cmd(cmd_line)
            data[label] = min(times)
            info(f"min: {data[label]:.2f}s")

    print(data)
    make_save_plot(data)
