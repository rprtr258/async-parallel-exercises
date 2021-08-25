from time import sleep, time
from multiprocessing import Pool

start_time = time()

def _log(message):
    print(" " * int(4 * (time() - start_time - 1)) + message)

def task(params):
    sleep(1)
    _log(f"end {params}")
    return 1


if __name__ == '__main__':
    pool = Pool()
    pool.map(task, list(range(20)))
    pool.close()
    pool.join()
