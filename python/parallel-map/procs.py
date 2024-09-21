#!/usr/bin/env python3

from multiprocessing import Pool
from typing import Callable, List, TypeVar

from main import main, split_chunks

A, B = TypeVar("A"), TypeVar("B")

def chunk_map(fn: Callable[[A], B], chunk: List[A]) -> List[B]:
    return list(map(fn, chunk))

def par_map(fn: Callable[[A], B], xs: List[A], procs_cnt: int) -> List[B]:
    with Pool(procs_cnt) as pool:
        chunks = split_chunks(xs, procs_cnt)
        promises = [pool.apply_async(chunk_map, [fn, chunk]) for chunk in chunks]
        return [chunk.get() for chunk in promises]

if __name__ == '__main__':
    main(par_map)
