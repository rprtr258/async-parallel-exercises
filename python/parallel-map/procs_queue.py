from multiprocessing import Process, Queue
from typing import Callable, List, TypeVar

from main import main, split_chunks

A, B = TypeVar("A"), TypeVar("B")

def worker(fn: Callable[[A], B], i: int, chunk: List[A], out_q: Queue):
    out_q.put((i, list(map(fn, chunk))))

def par_map(fn: Callable[[A], B], xs: List[A], procs_cnt: int) -> List[B]:
    results_q = Queue()
    chunks = list(split_chunks(xs, procs_cnt))
    processes = [
        Process(target=worker, args=[fn, i, chunk, results_q])
        for i, chunk in enumerate(chunks)
    ]
    for process in processes:
        process.start()
    res = []
    for _ in range(procs_cnt):
        i, fchunkx = results_q.get()
        res.append((i, fchunkx))
    for process in processes:
        process.join()
    return sum(map(lambda ix:ix[1], sorted(res, key=lambda ix:ix[0])), [])

if __name__ == '__main__':
    main(par_map)
