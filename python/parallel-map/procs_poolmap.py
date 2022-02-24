from multiprocessing import Pool
from typing import Callable, List, TypeVar

from main import main

A, B = TypeVar("A"), TypeVar("B")

def par_map(fn: Callable[[A], B], xs: List[A], procs_cnt: int) -> List[B]:
    with Pool(procs_cnt) as pool:
        return list(pool.map(fn, xs))

if __name__ == '__main__':
    main(par_map)
