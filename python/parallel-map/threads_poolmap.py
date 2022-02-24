from multiprocessing.pool import ThreadPool
from typing import Callable, List, TypeVar

from main import main

A, B = TypeVar("A"), TypeVar("B")

def par_map(fn: Callable[[A], B], xs: List[A], threads_cnt: int) -> List[B]:
    with ThreadPool(threads_cnt) as pool:
        return list(pool.map(fn, xs))

if __name__ == '__main__':
    main(par_map)
