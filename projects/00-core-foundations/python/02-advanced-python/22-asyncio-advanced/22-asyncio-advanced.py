"""
Advanced Python - 22: Asyncio Advanced
=======================================
Topics: TaskGroup vs gather; cancellation and shielding; asyncio.timeout;
        async context managers and iterators; queues; Semaphore rate
        limiting; run_in_executor; never block the loop.

Why this matters for AI/backend engineering:
    Streaming responses from several LLM providers at once, a bounded-
    concurrency embedding pipeline, and graceful cancellation when a client
    disconnects mid-generation all hang off these primitives. The single
    biggest throughput lever for API-based AI workloads is doing hundreds
    of calls concurrently without blocking the event loop.

Run:      python 22-asyncio-advanced.py
Verify:   python 22-asyncio-advanced.py --verify
Reference: https://docs.python.org/3/library/asyncio.html
           (requires Python 3.11+ for TaskGroup and asyncio.timeout)
"""

from __future__ import annotations

import asyncio
import os
import random
import sys
import time

random.seed(42)
os.environ.setdefault("MPLBACKEND", "Agg")   # never open a GUI window

# ============================================================
# 1. TaskGroup vs gather
# ============================================================
# asyncio.gather returns one future that fails only when you await it.
# A TaskGroup (3.11+) cancels its remaining tasks the moment ANY child
# fails, then raises an ExceptionGroup -- fail-fast semantics. That is
# what you want when one bad embedding should abort the whole batch.

async def _fetch(name: str, delay: float, fail: bool = False) -> str:
    """Simulate one async provider call."""
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(f"{name} returned an error")
    return f"{name}:ok"


async def demo_gather() -> list[str]:
    """gather: children keep running even if one fails (no auto-cancel)."""
    results = await asyncio.gather(
        _fetch("a", 0.02), _fetch("b", 0.01), _fetch("c", 0.03)
    )
    print(f"  gather results: {results}")
    return results


async def demo_task_group() -> None:
    """TaskGroup: one failure cancels the rest, surfaced as ExceptionGroup."""
    cancelled: list[str] = []
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(_fetch("a", 0.05))
            group.create_task(_fetch("boom", 0.02, fail=True))
            group.create_task(_wrap_cancel("c", 0.2, cancelled))
    except ExceptionGroup as eg:
        print(f"  TaskGroup raised {type(eg).__name__}: "
              f"{[e.__class__.__name__ for e in eg.exceptions]}")
    print(f"  tasks cancelled by the group: {cancelled}")
    # Output:
    #   TaskGroup raised ExceptionGroup: ['ValueError']
    #   tasks cancelled by the group: ['c']


async def _wrap_cancel(name: str, delay: float, cancelled: list[str]) -> None:
    """Record cancellation so we can assert the group cancelled this task."""
    try:
        await _fetch(name, delay)
    except asyncio.CancelledError:
        cancelled.append(name)
        raise


# ============================================================
# 2. Cancellation and Shielding
# ============================================================
# Cancelling a task raises CancelledError inside it. asyncio.shield keeps
# a *dependency* alive while the caller itself can still be cancelled --
# useful to finish flushing a generation buffer before acknowledging.

async def demo_cancel() -> None:
    """Plain cancellation: the task stops at its next await."""
    task = asyncio.create_task(_fetch("slow", 5.0))
    await asyncio.sleep(0.01)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("  plain task was cancelled (as expected)")


async def demo_shield() -> str:
    """Shielded work survives cancellation of the awaiting caller.

    The client gives up after 0.02s (timeout), but the model call (0.1s)
    is shielded: it keeps running, and we can still collect its result.
    """
    task = asyncio.create_task(_fetch("shielded", 0.1))
    timed_out = False
    try:
        async with asyncio.timeout(0.02):
            await asyncio.shield(task)
    except TimeoutError:
        timed_out = True
    result = await task            # shielded call finished anyway
    print(f"  outer wait timed out: {timed_out}; shielded work still "
          f"completed: {result}")
    return result


# ============================================================
# 3. asyncio.timeout
# ============================================================
# asyncio.wait_for wraps a single awaitable; asyncio.timeout (3.11+) is a
# context manager: the whole block shares one deadline. SLOs on a model
# endpoint are implemented exactly like this.

async def demo_timeout() -> None:
    """A deadline applied to a block, not a single call."""
    try:
        async with asyncio.timeout(0.05):
            await _fetch("slow", 0.5)
    except TimeoutError:
        print("  asyncio.timeout raised TimeoutError (as expected)")


# ============================================================
# 4. Async Context Managers and Iterators
# ============================================================
# __aenter__/__aexit__ and __aiter__/__anext__ mirror their sync twins.
# Async iterators let you stream tokens from a model instead of buffering
# the whole response. Complexity: O(1) memory -- one chunk at a time.

class AsyncSession:
    """An async context manager: setup and teardown around an async block."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.opened = False
        self.closed = False

    async def __aenter__(self) -> "AsyncSession":
        await asyncio.sleep(0.01)        # e.g. open a DB connection
        self.opened = True
        return self

    async def __aexit__(self, exc_type: object, exc: object,
                        tb: object) -> bool:
        await asyncio.sleep(0.01)        # e.g. close the connection
        self.closed = True
        return False                     # False = do not suppress


class TokenStream:
    """An async iterator yielding a few tokens with tiny gaps."""

    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens
        self._index = 0

    def __aiter__(self) -> "TokenStream":
        return self

    async def __anext__(self) -> str:
        if self._index >= len(self._tokens):
            raise StopAsyncIteration
        await asyncio.sleep(0.01)
        token = self._tokens[self._index]
        self._index += 1
        return token


async def demo_async_context_and_iter() -> tuple[bool, bool, list[str]]:
    """Exercise async with and async for."""
    session = AsyncSession("db")
    async with session as s:
        inside = (s.opened is True and s.closed is False)
    collected: list[str] = []
    async for token in TokenStream(["token", "by", "token"]):
        collected.append(token)
    print(f"  inside context (opened, not closed): {inside}")
    print(f"  context closed after block: {session.closed}")
    print(f"  streamed tokens: {collected}")
    return inside, session.closed, collected


# ============================================================
# 5. Queues for Producer-Consumer
# ============================================================
# asyncio.Queue with maxsize gives backpressure: a full queue parks the
# producer until a consumer frees a slot. Bounded memory, no polling.

async def demo_queue() -> list[str]:
    """One producer, two consumers, bounded queue."""
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=3)
    processed: list[str] = []

    async def producer() -> None:
        for i in range(8):
            await queue.put(f"item-{i}")     # parks when full
        await queue.put(None)                # sentinel: no more work
        await queue.put(None)

    async def consumer(name: str) -> None:
        while True:
            item = await queue.get()
            if item is None:
                return
            await asyncio.sleep(0.005)       # simulate processing
            processed.append(f"{name}:{item}")

    async with asyncio.TaskGroup() as group:
        group.create_task(producer())
        group.create_task(consumer("c1"))
        group.create_task(consumer("c2"))
    print(f"  consumers processed {len(processed)} items")
    return processed


# ============================================================
# 6. Semaphore Rate Limiting
# ============================================================
# A Semaphore caps how many coroutines are inside the guarded region.
# This is how you respect a provider's "10 requests/second" contract.
# Complexity: O(1) per acquire; concurrency bounded by the limit.

async def demo_semaphore() -> tuple[int, int]:
    """Run 8 calls with at most 3 in flight; track the observed max."""
    sem = asyncio.Semaphore(3)
    in_flight = 0
    max_seen = 0

    async def limited(name: str) -> str:
        nonlocal in_flight, max_seen
        async with sem:
            in_flight += 1
            max_seen = max(max_seen, in_flight)
            await asyncio.sleep(0.02)
            in_flight -= 1
            return f"{name}:ok"

    results = await asyncio.gather(*(limited(f"r{i}") for i in range(8)))
    print(f"  completed {len(results)} calls; max in-flight = {max_seen}")
    return len(results), max_seen


# ============================================================
# 7. run_in_executor: Bridging Blocking Sync Code
# ============================================================
# Never put time.sleep or a CPU-heavy sync call directly in a coroutine --
# it freezes the whole loop. asyncio.to_thread (or run_in_executor) ships
# the call to a thread so the loop stays responsive.

def _blocking_db_query(query: str) -> str:
    """A hypothetical sync driver call that blocks for a while."""
    time.sleep(0.05)
    return f"result-of-{query}"


async def demo_to_thread() -> str:
    """Bridge a blocking sync call without stalling the loop."""
    result = await asyncio.to_thread(_blocking_db_query, "SELECT 1")
    print(f"  blocking call bridged: {result}")
    return result


# ============================================================
# 8. Never Block the Loop
# ============================================================
# Measured proof: two tasks that each time.sleep(0.15) take ~0.3s (they
# serialize, the loop is frozen). The same with asyncio.sleep takes ~0.15s.

async def _direct_block() -> None:
    """A coroutine that blocks with time.sleep -- freezes the whole loop."""
    time.sleep(0.15)


async def _blocking_pair() -> float:
    """Two direct time.sleep calls: the loop cannot interleave them."""
    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        group.create_task(_direct_block())
        group.create_task(_direct_block())
    return time.perf_counter() - start


async def _cooperative_pair() -> float:
    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        group.create_task(asyncio.sleep(0.15))
        group.create_task(asyncio.sleep(0.15))
    return time.perf_counter() - start


async def demo_loop_blocking() -> tuple[float, float]:
    """Measure direct time.sleep vs cooperative asyncio.sleep."""
    blocking = await _blocking_pair()
    cooperative = await _cooperative_pair()
    print(f"  time.sleep in coroutines: {blocking:.3f}s (loop frozen, serialized)")
    print(f"  asyncio.sleep            : {cooperative:.3f}s (overlapped)")
    return blocking, cooperative


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: time.sleep(1) inside a coroutine -- the entire loop stalls.
# CORRECT: await asyncio.sleep(1), or asyncio.to_thread for real blocking
#   work you cannot refactor.
# MISTAKE: gather(*tasks) and assuming one failure cancels the rest.
# CORRECT: TaskGroup for fail-fast batches; gather(return_exceptions=True)
#   when you want partial results.
# MISTAKE: unbounded task creation ("for x in big_list: create_task").
# CORRECT: Semaphore or a bounded queue -- backpressure protects you from
#   the provider, the DB, and your own RAM.


# ============================================================
# Self-Verification  (MANDATORY -- every file ends with this)
# ============================================================
async def _verify_async() -> None:
    """Run all assertions inside one event loop."""
    # 1. TaskGroup cancels siblings when one child fails.
    cancelled: list[str] = []
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(_fetch("a", 0.03))
            group.create_task(_fetch("boom", 0.01, fail=True))
            group.create_task(_wrap_cancel("b", 0.3, cancelled))
    except ExceptionGroup:
        pass
    assert cancelled == ["b"], \
        "TaskGroup must cancel remaining siblings on failure (got %s)" % cancelled

    # 2. gather still returns results for tasks that succeeded.
    results = await demo_gather()
    assert results == ["a:ok", "b:ok", "c:ok"], \
        "gather must collect all successful results in order"

    # 3. Plain cancellation raises CancelledError; shielding preserves work.
    task = asyncio.create_task(_fetch("x", 5.0))
    await asyncio.sleep(0.01)
    task.cancel()
    cancelled_raised = False
    try:
        await task
    except asyncio.CancelledError:
        cancelled_raised = True
    assert cancelled_raised, "cancelling a task must raise CancelledError"
    assert await demo_shield() == "shielded:ok", \
        "shielded work must survive cancellation of the waiter"

    # 4. asyncio.timeout raises TimeoutError past the deadline.
    timed_out = False
    try:
        async with asyncio.timeout(0.05):
            await _fetch("slow", 0.5)
    except TimeoutError:
        timed_out = True
    assert timed_out, "asyncio.timeout must raise TimeoutError past the deadline"

    # 5. Async context manager + iterator behave like their sync twins.
    inside, closed, tokens = await demo_async_context_and_iter()
    assert inside and closed, "async context must open then close cleanly"
    assert tokens == ["token", "by", "token"], \
        "async iterator must yield tokens in order"

    # 6. Queue: every item processed exactly once (2 consumers, 8 items).
    processed = await demo_queue()
    assert len(processed) == 8, \
        "queue consumers must process all 8 items (got %d)" % len(processed)

    # 7. Semaphore observably caps concurrency.
    done, max_seen = await demo_semaphore()
    assert done == 8, "all semaphore-limited calls must complete"
    assert max_seen <= 3, "semaphore(3) must cap in-flight work (got %d)" % max_seen
    assert max_seen == 3, \
        "8 calls with a semaphore(3) must actually reach the cap (got %d)" % max_seen

    # 8. run_in_executor bridges blocking sync code.
    assert await demo_to_thread() == "result-of-SELECT 1", \
        "to_thread must return the blocking call's result"

    # 9. Blocking sleep in threads serializes; asyncio.sleep overlaps.
    blocking, cooperative = await demo_loop_blocking()
    assert blocking >= cooperative * 1.5, \
        "blocking sleeps must take longer than cooperative ones: %s vs %s" % (
            blocking, cooperative)


def _verify() -> None:
    """Entry point for --verify: wraps the async suite."""
    asyncio.run(_verify_async())
    print("\n[OK] 22-asyncio-advanced: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("=" * 60)
        print("ADVANCED ASYNCIO: 8 PRIMITIVES FOR CONCURRENT AI CALLS")
        print("=" * 60)

        async def main() -> None:
            print("\n--- 1. TaskGroup vs gather ---")
            await demo_gather()
            await demo_task_group()
            print("\n--- 2. Cancellation and shielding ---")
            await demo_cancel()
            await demo_shield()
            print("\n--- 3. asyncio.timeout ---")
            await demo_timeout()
            print("\n--- 4. Async context managers and iterators ---")
            await demo_async_context_and_iter()
            print("\n--- 5. Queues ---")
            await demo_queue()
            print("\n--- 6. Semaphore rate limiting ---")
            await demo_semaphore()
            print("\n--- 7. run_in_executor ---")
            await demo_to_thread()
            print("\n--- 8. Never block the loop ---")
            await demo_loop_blocking()
            print("\n1. TaskGroup = fail-fast batches; gather = best-effort.")
            print("2. Semaphore + bounded queues = provider rate limits.")
            print("3. Blocking calls go to threads; the loop never sleeps.")
            print("4. shield keeps critical work alive through cancellation.")

        asyncio.run(main())
        _verify()
