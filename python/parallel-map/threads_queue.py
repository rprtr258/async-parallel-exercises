from queue import Queue
from threading import Thread
from typing import Callable, List, TypeVar

from main import main

A, B = TypeVar("A"), TypeVar("B")

def worker(fn: Callable[[A], B], q: Queue, results: List[B]):
    while True:
        i, x = q.get()
        results[i] = fn(x)
        q.task_done()

def par_map(fn: Callable[[A], B], xs: List[A], threads_cnt: int) -> List[B]:
    results = [None] * len(xs)
    q = Queue()
    threads = [
        Thread(target=worker, args=[fn, q, results], daemon=True)
        for _ in range(threads_cnt)
    ]
    for thread in threads:
        thread.start()
    for i, x in enumerate(xs):
        q.put((i, x))
    q.join()
    return results

if __name__ == '__main__':
    main(par_map)
