#!/usr/bin/env python
from typing import List
from sys import argv
import subprocess
import logging
import time

import matplotlib.pyplot as plt
import seaborn

def cmd(n: int) -> List[str]:
    return argv[1:] + ["-p", str(n)]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    colors = ["r", "g", "b", "k", "gold", "purple", "lime"]
    times = {k: [] for k in [1, 2, 4, 10]}
    for color, processes in zip(colors, times.keys()):
        logging.info(f"Started benching using {processes} processes")
        cmd_line = cmd(processes)
        for _ in range(10):
            time_start = time.time_ns() // 1000
            process = subprocess.Popen(cmd_line, stdout=subprocess.PIPE)
            output, error = process.communicate()
            time_end = time.time_ns() // 1000
            times[processes].append(time_end - time_start)
        print(f"min: {min(times[processes])}, max: {max(times[processes])}, mean: {max(times[processes]) / len(times[processes])}")
        seaborn.histplot(times[processes], kde=True, label=f"{processes} procs", color=color)
    plt.legend()
    plt.show()
