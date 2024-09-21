import time
from signal import signal, SIGINT
from threading import Thread, Event
from queue import Empty, Full, Queue

start_time = time.time()

def _log(message):
    print(f"{time.time() - start_time:.3f}: {message}")

def Producer(name, queue, stop_event):
    def produce(i):
        time.sleep(1) # time consuming production
        return i
    def log(message):
        _log(f"[PRODUCER #{name}] {message}")

    for i in range(1, 6):
        value = produce(i)
        try:
            queue.put(value, timeout=3)
        except Full:
            log("queue FULL")
            break
        log(f"put {value}")
    log(f"producer dies")

def Consumer(name, queue, stop_event):
    def consume(x):
        time.sleep(1.1) # time consuming consuming
    def log(message):
        _log(f"[CONSUMER #{name}] {message}")

    while True:
        try:
            msg = queue.get(timeout=3)
        except Empty:
            # stop consuming if no items got in 3 secs
            log("queue EMPTY")
            break
        consume(msg)
        log(f"consumed {msg}")
    log(f"consumer dies")

def start_threads(producers_num, consumers_num):
    queue = Queue()
    threads = []
    stop_event = Event()
    for i in range(producers_num):
        thread = Thread(target=Producer, args=(i, queue, stop_event), daemon=True)
        thread.start()
        threads.append(thread)
    for i in range(consumers_num):
        thread = Thread(target=Consumer, args=(i, queue, stop_event), daemon=True)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def sigint_handler(a, b):
    _log(f"INTERRUPT")
    exit(1)

if __name__ == "__main__":
    signal(SIGINT, sigint_handler)
    start_threads(4, 7)

