import argparse
from os import cpu_count
from typing import Callable, List, TypeVar, Iterator

A, B = TypeVar("A"), TypeVar("B")

def is_prime(n: int) -> bool:
    p = 2
    while p * p <= n:
        if n % p == 0:
            return False
        p += 1
    return True

def factorize(n: int) -> int:
    res = []
    print(n, end=" ")
    while n % 2 == 0:
        n //= 2
        res.append(2)
    p = 3
    while n > 1:
        while n % p == 0:
            n //= p
            res.append(p)
        p += 2
        # all primes less than p found
        # hence, left divisors of n are >= p
        if p * p > n:
            res.append(n)
            break
    return res

def split_chunks(lst: List[A], chunks: int) -> Iterator[List[A]]:
    chunk_size, chunk_rest = divmod(len(lst), chunks)
    i = 0
    while i < len(lst):
        next_i = i + chunk_size + (chunk_rest > 0)
        yield lst[i : next_i]
        chunks -= 1
        i = next_i
        chunk_rest -= 1
    while chunks > 0:
        yield []
        chunks -= 1

def main(par_map: Callable[[Callable[[A], B], List[A], int], List[B]]):
    fns = {
        "is_prime": is_prime,
        "factorize": factorize
    }
    parser = argparse.ArgumentParser(description='Calc map.')
    parser.add_argument(
        "-n",
        type=int,
        default=100000,
        help="list range upper bound (default: 100000)"
    )
    parser.add_argument(
        "-p",
        type=int,
        default=cpu_count(),
        help="number of processes/threads to use (default: one for every cpu core)"
    )
    parser.add_argument(
        "-f",
        required=True,
        choices=fns.keys(),
        help="function to map"
    )

    args = parser.parse_args()
    print(par_map(fns[args.f], list(range(1, args.n + 1)), args.p))
