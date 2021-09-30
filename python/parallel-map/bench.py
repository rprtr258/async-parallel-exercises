#!/usr/bin/env python3
from typing import List
from sys import argv
import subprocess
import logging
import time

import matplotlib.pyplot as plt

def cmd(n: int) -> List[str]:
    return argv[1:] + ["-n", "100", "-p", str(n)]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    times = {k: [] for k in [1, 2, 4, 10, 50]}
    times = {k: [] for k in [1, 2, 4]}
    for processes in times.keys():
        logging.info(f"Started benching using {processes} processes")
        cmd_line = cmd(processes)
        for _ in range(2):
            time_start = time.time_ns()
            process = subprocess.Popen(cmd_line, stdout=subprocess.PIPE)
            output, error = process.communicate()
            time_end = time.time_ns()
            times[processes].append(time_end - time_start)
    plt.hist(times)
    plt.show()
