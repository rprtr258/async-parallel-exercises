#!/usr/bin/env python3

from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, List, TypeVar

from main import main

A, B = TypeVar("A"), TypeVar("B")

def par_map(fn: Callable[[A], B], xs: List[A], procs_cnt: int) -> List[B]:
    with ProcessPoolExecutor(procs_cnt) as pool:
        return list(pool.map(fn, xs))

if __name__ == '__main__':
    main(par_map)
