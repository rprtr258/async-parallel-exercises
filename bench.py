#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Any, Dict, List, Callable, Iterator
from subprocess import Popen, PIPE
from time import time_ns
from itertools import product

import matplotlib.pyplot as plt

def info(msg: str) -> None:
  print("[INFO]", msg)

def label(file: str, **kwargs: Dict[str, Any]) -> str:
  params = ", ".join(f"{p[0]}={p[1]}" for p in kwargs.items())
  return f"{file}({params})"

tries = 2
def cmd(args: List[str]) -> Iterator[int]:
  for _ in range(tries):
    time_start = time_ns()
    _, _ = Popen(args, stdout=PIPE).communicate()
    time_end = time_ns()
    yield (time_end - time_start) / 1000000000

def make_save_plot(data: Dict[str, float], name: str) -> None:
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
  fig.savefig(f"{name}.png")

# TODO: add colors
if __name__ == "__main__":
  n = 1000000
  problems: Dict[str, Dict[str, List[str]]] = {
    "is_prime": {
      "serial": ["python/parallel-map/serial.py", "-n", str(n), "-f", "is_prime"],
    } | {
      label("procs", p=p): ["python/parallel-map/procs.py", "-p", str(p), "-n", str(n), "-f", "is_prime"]
      # "procs_futures": lambda p, n: cmd("python/parallel-map/procs_futures.py", "-p", str(p), "-n", str(n), "-f", "is_prime"),
      # "python/parallel-map/procs_poolmap.py",
      # "python/parallel-map/procs_queue.py",
      # "python/parallel-map/threads.py",
      # "python/parallel-map/threads_queue.py",
      # "python/parallel-map/threads_poolmap.py",
      for p in [2, 4, 8, 16, 32]
    },
    "factorize": {
      "serial": ["python/parallel-map/serial.py", "-n", str(n), "-f", "factorize"],
    } | {
      label("procs", p=p): ["python/parallel-map/procs.py", "-p", str(p), "-n", str(n), "-f", "factorize"]
      # "procs_futures": lambda p, n: cmd("python/parallel-map/procs_futures.py", "-p", str(p), "-n", str(n), "-f", "is_prime"),
      # "python/parallel-map/procs_poolmap.py",
      # "python/parallel-map/procs_queue.py",
      # "python/parallel-map/threads.py",
      # "python/parallel-map/threads_queue.py",
      # "python/parallel-map/threads_poolmap.py",
      for p in [2, 4, 8, 16, 32]
    },
  }

  for task, cfg in problems.items():
    info(f"running task {task}")

    data: Dict[str, float] = {}
    for label, file in cfg.items():
      info(f"Started bench '{label}'")
      times = list(cmd(file))
      data[label] = min(times)
      info(f"min: {min(times):.2f}s, max: {max(times):.2f}s, avg: {sum(times)/len(times):.2f}s")

    print(data)
    make_save_plot(data, task)
