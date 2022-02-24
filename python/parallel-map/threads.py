from threading import Thread
from typing import Callable, List, TypeVar

from main import main, split_chunks

A, B = TypeVar("A"), TypeVar("B")

def chunk_map(fn: Callable[[A], B], thread_id: int, results: List[List[B]], chunk: List[A]):
    results[thread_id] = list(map(fn, chunk))

def par_map(fn: Callable[[A], B], xs: List[A], threads_cnt: int) -> List[B]:
    chunks = split_chunks(xs, threads_cnt)
    results = [None] * threads_cnt
    threads = [
        Thread(target=chunk_map, args=[fn, i, results, chunk])
        for i, chunk in enumerate(chunks)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results

if __name__ == '__main__':
    main(par_map)
