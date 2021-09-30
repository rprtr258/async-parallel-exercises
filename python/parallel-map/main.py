import argparse
from multiprocessing import Pool
from os import cpu_count

def is_prime(n: int) -> bool:
    p = 2
    while p * p <= n:
        if n % p == 0:
            return False
        p += 1
    return True

def check_prime(n: int):
    if is_prime(n):
        print(n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find prime numbers.')
    parser.add_argument('-n', type=int, default=1000000, help='upper bound to search (default: 1000000)')
    parser.add_argument('-p', type=int, dest="processes", default=cpu_count(), help='number of processes to use (default: one for every cpu core)')

    args = parser.parse_args()
    print(f"CPU count: {args.processes}")
    with Pool(args.processes) as pool:
        list(pool.map(check_prime, range(2, args.n)))
