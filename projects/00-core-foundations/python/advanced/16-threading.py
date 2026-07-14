"""
Threading - Advanced Python Exercises
======================================
Threading allows concurrent execution of code, useful for
I/O-bound tasks.
"""

import threading
import time
from typing import List, Callable
from queue import Queue


# =============================================================================
# 1. Basic Thread
# =============================================================================

def demo_basic_thread():
    """Demonstrate basic thread creation."""
    def worker(name: str, delay: float):
        print(f"  [{name}] Starting")
        time.sleep(delay)
        print(f"  [{name}] Finished")

    # Create threads
    t1 = threading.Thread(target=worker, args=("Thread-1", 0.3))
    t2 = threading.Thread(target=worker, args=("Thread-2", 0.1))

    # Start threads
    t1.start()
    t2.start()

    # Wait for completion
    t1.join()
    t2.join()
    print("  Both threads completed")


# =============================================================================
# 2. Thread with Return Value
# =============================================================================

class ThreadResult:
    """Helper to capture thread return value."""

    def __init__(self):
        self._result = None
        self._exception = None

    @property
    def result(self):
        if self._exception:
            raise self._exception
        return self._result

    def set_result(self, result):
        self._result = result

    def set_exception(self, exception):
        self._exception = exception


def demo_thread_return():
    """Capture return values from threads."""
    def compute_square(n: int, result: ThreadResult):
        try:
            time.sleep(0.1)
            result.set_result(n ** 2)
        except Exception as e:
            result.set_exception(e)

    results = []
    threads = []

    for i in range(5):
        tr = ThreadResult()
        t = threading.Thread(target=compute_square, args=(i, tr))
        results.append(tr)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"  Results: {[r.result for r in results]}")


# =============================================================================
# 3. Lock and RLock
# =============================================================================

class Counter:
    """Thread-safe counter using Lock."""

    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._count += 1

    @property
    def count(self):
        return self._count


def demo_lock():
    """Demonstrate Lock for thread safety."""
    counter = Counter()

    def increment_many(n: int):
        for _ in range(n):
            counter.increment()

    threads = []
    for _ in range(10):
        t = threading.Thread(target=increment_many, args=(1000,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"  Expected: 10000, Actual: {counter.count}")


class BankAccount:
    """Thread-safe bank account using RLock."""

    def __init__(self, balance: float = 0):
        self._balance = balance
        self._lock = threading.RLock()

    def deposit(self, amount: float):
        with self._lock:
            self._balance += amount

    def withdraw(self, amount: float) -> bool:
        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                return True
            return False

    def transfer(self, other: "BankAccount", amount: float):
        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                other.deposit(amount)
                return True
            return False

    @property
    def balance(self):
        return self._balance


# =============================================================================
# 4. Semaphore
# =============================================================================

def demo_semaphore():
    """Demonstrate Semaphore for limiting concurrency."""
    semaphore = threading.Semaphore(2)  # Max 2 concurrent

    def limited_task(name: str):
        with semaphore:
            print(f"  {name} started")
            time.sleep(0.1)
            print(f"  {name} finished")

    threads = []
    for i in range(5):
        t = threading.Thread(target=limited_task, args=(f"Task-{i}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


# =============================================================================
# 5. Producer-Consumer
# =============================================================================

def demo_producer_consumer():
    """Producer-consumer pattern with Queue."""
    queue = Queue(maxsize=5)
    items_produced = []
    items_consumed = []

    def producer(name: str, count: int):
        for i in range(count):
            item = f"{name}-{i}"
            queue.put(item)
            items_produced.append(item)
            time.sleep(0.01)

    def consumer(name: str):
        while True:
            item = queue.get()
            if item is None:
                break
            items_consumed.append(item)
            time.sleep(0.02)
            queue.task_done()

    # Start producer and consumer
    prod = threading.Thread(target=producer, args=("P1", 10))
    cons = threading.Thread(target=consumer, args=("C1",))

    prod.start()
    cons.start()

    prod.join()
    queue.put(None)  # Sentinel
    cons.join()

    print(f"  Produced: {len(items_produced)} items")
    print(f"  Consumed: {len(items_consumed)} items")


# =============================================================================
# 6. Event and Condition
# =============================================================================

def demo_event():
    """Demonstrate Event for thread coordination."""
    event = threading.Event()

    def waiter():
        print("  Waiter: Waiting for event...")
        event.wait()
        print("  Waiter: Event received!")

    def setter():
        time.sleep(0.2)
        print("  Setter: Setting event")
        event.set()

    t1 = threading.Thread(target=waiter)
    t2 = threading.Thread(target=setter)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


# =============================================================================
# 7. Thread Pool (concurrent.futures)
# =============================================================================

def demo_thread_pool():
    """Demonstrate ThreadPoolExecutor."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def fetch_url(url: str) -> str:
        time.sleep(0.1)  # Simulate network request
        return f"Data from {url}"

    urls = [f"http://example.com/page{i}" for i in range(5)]

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fetch_url, url): url for url in urls}
        results = {}
        for future in as_completed(futures):
            url = futures[future]
            results[url] = future.result()

    print(f"  Fetched {len(results)} URLs")


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("THREADING DEMO")
    print("=" * 60)

    # 1. Basic thread
    print("\n--- Basic Thread ---")
    demo_basic_thread()

    # 2. Thread return value
    print("\n--- Thread Return Value ---")
    demo_thread_return()

    # 3. Lock
    print("\n--- Lock (Thread Safety) ---")
    demo_lock()

    # 4. Semaphore
    print("\n--- Semaphore ---")
    demo_semaphore()

    # 5. Producer-Consumer
    print("\n--- Producer-Consumer ---")
    demo_producer_consumer()

    # 6. Event
    print("\n--- Event ---")
    demo_event()

    # 7. Thread Pool
    print("\n--- Thread Pool ---")
    demo_thread_pool()

    # 8. Bank account transfer
    print("\n--- Bank Account Transfer ---")
    account1 = BankAccount(1000)
    account2 = BankAccount(500)
    print(f"  Initial: A1=${account1.balance}, A2=${account2.balance}")

    transfer_threads = []
    for _ in range(5):
        t = threading.Thread(target=account1.transfer, args=(account2, 100))
        transfer_threads.append(t)
        t.start()

    for t in transfer_threads:
        t.join()

    print(f"  Final: A1=${account1.balance}, A2=${account2.balance}")

    print("\n" + "=" * 60)
    print("All threading demos complete!")
    print("=" * 60)
