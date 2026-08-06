"""Challenge 22: Asyncio Advanced — reference solution.

Why these approaches:
- Bronze: the semaphore is the rate limit; max-in-flight tracking makes
  the cap observable instead of hoped for.
- Silver: a bounded queue is the backpressure seam — the producer parks
  when full, so observed size can never exceed maxsize.
- Gold: TaskGroup fail-fast semantics are deterministic — tasks after
  the failure are cancelled, tasks before it complete.
"""

from __future__ import annotations

import asyncio


def run_limited(n_calls: int, limit: int) -> tuple[int, int]:
    """Cap in-flight simulated API calls with a semaphore; prove the cap
    by tracking max concurrent coroutines inside the guarded region."""

    async def _run() -> tuple[int, int]:
        sem = asyncio.Semaphore(limit)
        in_flight = 0
        max_seen = 0
        completed = 0

        async def call() -> None:
            nonlocal in_flight, max_seen, completed
            async with sem:
                in_flight += 1
                max_seen = max(max_seen, in_flight)
                await asyncio.sleep(0.01)
                in_flight -= 1
                completed += 1

        await asyncio.gather(*(call() for _ in range(n_calls)))
        return completed, max_seen

    return asyncio.run(_run())


def pipeline(items: list[str], maxsize: int) -> tuple[int, int]:
    """Bounded producer-consumer: put parks when full, get parks when
    empty. The queue size is the backpressure signal."""

    async def _run() -> tuple[int, int]:
        queue: asyncio.Queue[str] = asyncio.Queue(maxsize=maxsize)
        max_observed = 0
        processed = 0

        async def producer() -> None:
            nonlocal max_observed
            for item in items:
                await queue.put(item)
                max_observed = max(max_observed, queue.qsize())

        async def consumer() -> None:
            nonlocal processed
            for _ in range(len(items)):
                item = await queue.get()
                await asyncio.sleep(0.005)
                processed += 1

        async with asyncio.TaskGroup() as group:
            group.create_task(producer())
            group.create_task(consumer())
        return processed, max_observed

    return asyncio.run(_run())


def run_batch(n: int, fail_at: int) -> tuple[int, int]:
    """TaskGroup batch: on failure the group cancels every remaining
    task, then raises ExceptionGroup. We swallow it and count."""

    async def _run() -> tuple[int, int]:
        completed = 0
        cancelled = 0

        async def task(i: int) -> None:
            nonlocal completed, cancelled
            try:
                if i < fail_at:
                    await asyncio.sleep(0.005)   # finishes before failure
                elif i == fail_at:
                    await asyncio.sleep(0.02)    # the one that fails
                    raise ValueError(f"task {i} failed")
                else:
                    await asyncio.sleep(5)       # still pending -> cancelled
                completed += 1
            except asyncio.CancelledError:
                cancelled += 1
                raise

        try:
            async with asyncio.TaskGroup() as group:
                for i in range(n):
                    group.create_task(task(i))
        except ExceptionGroup:
            pass
        return completed, cancelled

    return asyncio.run(_run())
