"""
Async/Await - Advanced Python Exercises
========================================
Asynchronous programming allows concurrent execution of
coroutines, ideal for I/O-bound tasks.
"""

import asyncio
import time
from typing import Coroutine, Any


# =============================================================================
# 1. Basic Async Functions
# =============================================================================

async def fetch_data(name: str, delay: float) -> str:
    """Simulate an async HTTP request."""
    print(f"  Starting fetch: {name}")
    await asyncio.sleep(delay)
    result = f"Data from {name} (took {delay:.1f}s)"
    print(f"  Completed: {name}")
    return result


async def count_up(name: str, count: int, delay: float):
    """Async counter with delays."""
    for i in range(1, count + 1):
        await asyncio.sleep(delay)
        print(f"  {name}: {i}/{count}")


# =============================================================================
# 2. Task Management
# =============================================================================

async def demo_tasks():
    """Demonstrate asyncio.Task creation and management."""
    print("\n--- Creating Tasks ---")

    # Create tasks - they start immediately
    task1 = asyncio.create_task(fetch_data("API-1", 0.3))
    task2 = asyncio.create_task(fetch_data("API-2", 0.2))
    task3 = asyncio.create_task(fetch_data("API-3", 0.1))

    # Gather results
    results = await asyncio.gather(task1, task2, task3)
    print(f"  Results: {results}")
    return results


async def demo_task_with_timeout():
    """Demonstrate task timeout handling."""
    print("\n--- Task Timeout ---")
    try:
        result = await asyncio.wait_for(
            fetch_data("Slow API", 5.0),
            timeout=0.5
        )
        print(f"  Result: {result}")
    except asyncio.TimeoutError:
        print(f"  Task timed out (as expected)")


# =============================================================================
# 3. Concurrency Patterns
# =============================================================================

async def producer(queue: asyncio.Queue, name: str, count: int):
    """Producer coroutine - puts items in queue."""
    for i in range(count):
        item = f"{name}-item-{i}"
        await asyncio.sleep(0.1)
        await queue.put(item)
        print(f"  Produced: {item}")
    await queue.put(None)  # Sentinel


async def consumer(queue: asyncio.Queue, name: str):
    """Consumer coroutine - gets items from queue."""
    while True:
        item = await queue.get()
        if item is None:
            break
        await asyncio.sleep(0.05)  # Simulate processing
        print(f"  {name} consumed: {item}")
        queue.task_done()


async def demo_producer_consumer():
    """Producer-consumer pattern with asyncio.Queue."""
    print("\n--- Producer-Consumer ---")
    queue = asyncio.Queue(maxsize=5)

    producers = [
        asyncio.create_task(producer(queue, "P1", 3)),
        asyncio.create_task(producer(queue, "P2", 3)),
    ]
    consumers = [
        asyncio.create_task(consumer(queue, "C1")),
        asyncio.create_task(consumer(queue, "C2")),
    ]

    await asyncio.gather(*producers)
    await asyncio.gather(*consumers)


async def demo_semaphore():
    """Limit concurrent operations with Semaphore."""
    print("\n--- Semaphore (max 2 concurrent) ---")
    sem = asyncio.Semaphore(2)

    async def limited_fetch(name: str, delay: float):
        async with sem:
            print(f"  {name} acquired semaphore")
            await asyncio.sleep(delay)
            print(f"  {name} releasing semaphore")
            return f"Result from {name}"

    tasks = [
        asyncio.create_task(limited_fetch(f"Task-{i}", 0.2))
        for i in range(5)
    ]
    results = await asyncio.gather(*tasks)
    print(f"  All completed: {len(results)} results")


# =============================================================================
# 4. Async Iteration
# =============================================================================

class AsyncCounter:
    """Async iterable counter."""

    def __init__(self, stop: int):
        self.stop = stop

    def __aiter__(self):
        self.current = 0
        return self

    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(0.05)
        self.current += 1
        return self.current


async def demo_async_iteration():
    """Demonstrate async for loop."""
    print("\n--- Async Iteration ---")
    counter = AsyncCounter(5)
    async for num in counter:
        print(f"  Async value: {num}")


# =============================================================================
# DEMO
# =============================================================================

async def main():
    print("=" * 60)
    print("ASYNC/AWAIT DEMO")
    print("=" * 60)

    # 1. Basic async
    print("\n--- Sequential vs Concurrent ---")

    start = time.perf_counter()
    await fetch_data("Sequential-1", 0.2)
    await fetch_data("Sequential-2", 0.2)
    await fetch_data("Sequential-3", 0.2)
    print(f"  Sequential: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    await asyncio.gather(
        fetch_data("Concurrent-1", 0.2),
        fetch_data("Concurrent-2", 0.2),
        fetch_data("Concurrent-3", 0.2),
    )
    print(f"  Concurrent: {time.perf_counter() - start:.2f}s")

    # 2. Tasks
    await demo_tasks()

    # 3. Timeout
    await demo_task_with_timeout()

    # 4. Producer-Consumer
    await demo_producer_consumer()

    # 5. Semaphore
    await demo_semaphore()

    # 6. Async iteration
    await demo_async_iteration()

    print("\n" + "=" * 60)
    print("All async demos complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
