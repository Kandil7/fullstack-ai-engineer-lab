"""
Multiprocessing - Advanced Python Exercises
============================================
Multiprocessing allows true parallelism by using multiple
CPU cores, bypassing the GIL.
"""

import multiprocessing
import time
import os
from typing import List, Any
from multiprocessing import Pool, Queue, Process, Value, Array


# =============================================================================
# Module-level worker callables
# =============================================================================
# Windows uses the "spawn" start method: the child re-imports this module and
# pickles each target by qualified name. Nested (local) functions cannot be
# pickled, so every Process/Queue target MUST live at module level.
# This is the fork-vs-spawn lesson from the lecture - keep it visible.


def _worker(name: str):
    print(f"  [{name}] PID: {os.getpid()}")
    time.sleep(0.1)
    print(f"  [{name}] Done")


def _increment(shared_val, n):
    for _ in range(n):
        with shared_val.get_lock():
            shared_val.value += 1


def _fill_array(shared_arr, index, value):
    shared_arr[index] = value


def _producer(q: Queue, count: int):
    for i in range(count):
        q.put(f"item-{i}")
    q.put(None)  # Sentinel


def _consumer(q: Queue, results: list):
    while True:
        item = q.get()
        if item is None:
            break
        results.append(item.upper())


def _safe_print(msg: str, lock_obj):
    with lock_obj:
        print(f"  {msg}")


def _background_task():
    while True:
        time.sleep(0.1)
        print("  Background running...")


# =============================================================================
# 1. Basic Process
# =============================================================================

def demo_basic_process():
    """Demonstrate basic process creation."""
    processes = []
    for i in range(3):
        p = Process(target=_worker, args=(f"Process-{i}",))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"  Main process PID: {os.getpid()}")


# =============================================================================
# 2. Process with Return Value
# =============================================================================

def compute_square(n: int) -> int:
    """Compute square of a number."""
    return n ** 2


def demo_process_return():
    """Get return values from processes using Pool."""
    with Pool(processes=4) as pool:
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        results = pool.map(compute_square, numbers)
        print(f"  Squares: {results}")

        # Async map
        async_result = pool.map_async(compute_square, numbers)
        print(f"  Async results: {async_result.get()}")


# =============================================================================
# 3. CPU-Bound Task
# =============================================================================

def fibonacci(n: int) -> int:
    """Calculate Fibonacci number (CPU-bound)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def demo_cpu_bound():
    """Compare sequential vs parallel for CPU-bound tasks."""
    numbers = [30, 32, 34, 35]

    # Sequential
    start = time.perf_counter()
    seq_results = [fibonacci(n) for n in numbers]
    seq_time = time.perf_counter() - start
    print(f"  Sequential: {seq_time:.2f}s, results: {seq_results}")

    # Parallel
    start = time.perf_counter()
    with Pool(processes=4) as pool:
        par_results = pool.map(fibonacci, numbers)
    par_time = time.perf_counter() - start
    print(f"  Parallel: {par_time:.2f}s, results: {par_results}")
    print(f"  Speedup: {seq_time/par_time:.2f}x")


# =============================================================================
# 4. Shared State
# =============================================================================

def demo_shared_state():
    """Demonstrate shared memory between processes."""
    # Shared value
    counter = Value('i', 0)  # 'i' = int

    processes = []
    for _ in range(4):
        p = Process(target=_increment, args=(counter, 1000))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"  Shared counter: {counter.value} (expected 4000)")

    # Shared array
    arr = Array('i', [0, 0, 0, 0, 0])

    processes = []
    for i in range(5):
        p = Process(target=_fill_array, args=(arr, i, i * 10))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"  Shared array: {list(arr)}")


# =============================================================================
# 5. Queue Communication
# =============================================================================

def demo_queue():
    """Demonstrate Queue for inter-process communication."""
    q = Queue()
    manager = multiprocessing.Manager()
    results = manager.list()

    prod = Process(target=_producer, args=(q, 5))
    cons = Process(target=_consumer, args=(q, results))

    prod.start()
    cons.start()

    prod.join()
    cons.join()

    print(f"  Queue results: {list(results)}")


# =============================================================================
# 6. Pool with Multiple Arguments
# =============================================================================

def power(base: int, exponent: int) -> int:
    """Calculate power."""
    return base ** exponent


def demo_pool_starmap():
    """Demonstrate starmap for multiple arguments."""
    args = [(2, 3), (3, 4), (4, 2), (5, 3)]

    with Pool(processes=2) as pool:
        results = pool.starmap(power, args)
        print(f"  Power results: {results}")

        # Apply with callback
        def callback(result):
            print(f"  Callback: {result}")

        pool.apply_async(power, (2, 10), callback=callback)
        pool.close()
        pool.join()


# =============================================================================
# 7. Process with Lock
# =============================================================================

def demo_process_lock():
    """Demonstrate Lock for process safety."""
    lock = multiprocessing.Lock()

    processes = []
    for i in range(5):
        p = Process(target=_safe_print, args=(f"Message from process {i}", lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


# =============================================================================
# 8. Daemon Processes
# =============================================================================

def demo_daemon():
    """Demonstrate daemon processes."""
    # Daemon process stops when main process exits
    daemon = Process(target=_background_task, daemon=True)
    daemon.start()
    time.sleep(0.3)
    print("  Main process exiting (daemon will stop)")
    # daemon.join()  # Would wait forever


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MULTIPROCESSING DEMO")
    print("=" * 60)

    # 1. Basic process
    print("\n--- Basic Process ---")
    demo_basic_process()

    # 2. Process return value
    print("\n--- Process Return Value (Pool) ---")
    demo_process_return()

    # 3. CPU-bound comparison
    print("\n--- CPU-Bound Task ---")
    demo_cpu_bound()

    # 4. Shared state
    print("\n--- Shared State ---")
    demo_shared_state()

    # 5. Queue communication
    print("\n--- Queue Communication ---")
    demo_queue()

    # 6. Pool starmap
    print("\n--- Pool Starmap ---")
    demo_pool_starmap()

    # 7. Process lock
    print("\n--- Process Lock ---")
    demo_process_lock()

    # 8. Daemon processes
    print("\n--- Daemon Process ---")
    demo_daemon()

    print("\n" + "=" * 60)
    print("All multiprocessing demos complete!")
    print("=" * 60)
