# FastAPI — 32: Async Endpoints Deep

Companion exercise: `32-async-endpoints-deep.py`

---

## Topic Overview

FastAPI lets you write `def` or `async def` endpoints, and the choice is not
cosmetic — it changes how your handler executes. `async def` handlers run
directly on the event loop; `def` handlers are executed in a worker
threadpool. The subtlety most people get wrong: **an `async def` handler that
contains blocking code blocks the entire event loop**, freezing every other
request on the process, while a plain `def` handler with the same blocking
code runs in a thread and lets the loop stay free.

The rule is short and load-bearing: **never block the event loop.** Await-based
I/O belongs in `async def`; blocking libraries (requests, sync DB drivers, CPU
loops) belong in `def` or in `run_in_threadpool`.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain how FastAPI executes `def` vs `async def` handlers.
2. Identify blocking calls that would freeze the event loop.
3. Use `run_in_threadpool` to escape to a thread inside async code.
4. Measure the serialization cost of blocking the loop.
5. Decide when a sync `def` endpoint is the correct choice.
6. State the concurrency model: one event loop, many threads.
7. Debug "my API is slow under load" with the loop-blocking lens.
8. Design async endpoints that genuinely overlap I/O.

## Prerequisites

| Need | Where |
|---|---|
| Async basics | `02-advanced-python/04-async-await.py` |
| FastAPI basics | `01-introduction.py`, `21-async.py` |
| Concurrency comparison | `02-advanced-python/21-concurrency-comparison.py` |

## 1. Two Kinds of Handlers

```python
@app.get("/sync")
def sync_endpoint(): ...        # runs in a worker thread (threadpool)

@app.get("/async")
async def async_endpoint(): ... # runs ON the event loop
```

Output:
```
# /sync   -> handler executes in a thread from the pool
# /async  -> handler executes on the single event loop
```

FastAPI detects the signature: plain `def` goes to the threadpool (via
`run_in_threadpool` internally), `async def` runs directly on the loop.

## 2. The Event Loop Is Single-Threaded

One process = one event loop thread. It juggles all concurrent async requests
by switching between `await` points. While any `async def` handler is *not*
awaiting — while it runs synchronous code — the loop is busy and **no other
request progresses**.

```python
@app.get("/async/blocking")
async def async_blocking():
    time.sleep(0.05)        # BAD: blocks the loop for 50ms
    return {"ok": True}
```

Output:
```
# every concurrent request waits while this sleeps — the API serializes
```

This is the classic footgun: an `async def` endpoint calling `requests.get`,
`time.sleep`, a sync DB driver, or heavy CPU work silently destroys
concurrency.

## 3. Blocking Code in `def` — The Threadpool Escape

```python
@app.get("/sync")
def sync_endpoint():
    time.sleep(0.05)        # OK: runs in a thread, loop stays free
    return {"ok": True}
```

Output:
```
# 4 concurrent requests -> ~4 threads, ~1x wall time (parallel)
```

A plain `def` handler with the same blocking work is executed in the
threadpool: the loop stays responsive and the blocking work overlaps across
threads. This is why "just make it `def`" is often the right fix.

## 4. run_in_threadpool — Escape Inside Async Code

```python
from fastapi.concurrency import run_in_threadpool

@app.get("/async/threaded")
async def async_threaded():
    result = await run_in_threadpool(blocking_work, 0.05)
    return {"result": result}
```

Output:
```
# async signature kept; the blocking call is handed to a worker thread
```

Use this when you must keep an async signature (e.g. inside a larger async
flow) but hit a blocking library. `run_in_threadpool` returns an awaitable
that runs the callable in the pool.

## 5. Measuring the Cost — Blocking Serializes

```python
await asyncio.gather(*[async_correct_body() for _ in range(4)])   # ~1x
await asyncio.gather(*[blocked_body() for _ in range(4)])          # ~4x
```

Output:
```
async (await sleep) : 0.105s   (parallel)
async (time.sleep)  : 0.402s   (serial — the loop was blocked)
```

The demonstration is the whole argument: awaiting genuine async I/O overlaps;
blocking inside async code serializes concurrent requests.

## 6. When Sync Is Correct

- The handler calls blocking libraries you won't replace (requests, psycopg2,
  boto3 sync).
- The work is short — the threadpool handles it.
- You cannot make the dependency async.

Choose `def` for blocking, `async def` for awaited I/O. Choosing "because it
looks modern" is how the loop gets blocked.

## 7. Common Mistakes to Avoid

### Mistake 1: Blocking calls in async def
```python
# WRONG — time.sleep / requests.get / CPU loops inside async def
# CORRECT — make it def, or await run_in_threadpool(...)
```

### Mistake 2: Believing async def is always faster
```python
# WRONG — async def with blocking bodies is SLOWER than def
# CORRECT — match the handler type to the I/O type
```

### Mistake 3: Sync driver in an async endpoint "for now"
```python
# WRONG — "I'll swap to asyncpg later" — the loop is already blocked
# CORRECT — run_in_threadpool now, swap the driver when ready
```

### Mistake 4: Ignoring the threadpool size
```python
# WRONG — 40 threads for 4 workers saturates and queues
# CORRECT — size the pool (see 49-uvicorn-gunicorn) to your workload
```

### Mistake 5: CPU-bound work in async def
```python
# WRONG — matrix math inside async def freezes the loop
# CORRECT — def (threadpool) or process/worker for heavy compute
```

## 8. Best Practices

1. `def` for blocking libraries, `async def` for awaited I/O.
2. Never call `time.sleep`, `requests.get`, or sync drivers in `async def`.
3. Use `run_in_threadpool` to escape while keeping an async signature.
4. Measure concurrency with a small load test (see 37-load-testing).
5. Keep CPU-heavy work out of the request path entirely when possible.
6. Use async drivers (httpx.AsyncClient, asyncpg, aiosqlite) with async def.
7. Size the threadpool for your mix of sync handlers.
8. Profile before optimizing — the bottleneck is rarely the framework.

## 9. Complexity and Cost

| Pattern | Concurrency | Cost |
|---|---|---|
| async def + await I/O | High (loop switches) | Best for I/O-bound |
| def (threadpool) | Pool-bounded threads | Correct for blocking libs |
| async def + blocking | **Zero overlap** | Serializes the whole process |
| run_in_threadpool | Pool-bounded | Escape hatch in async flows |

The blocking-in-async pattern is the worst of both worlds — async signature,
serial behavior, global freeze.

## 10. AI Engineering Relevance

**Where this shows up:** model-serving and LLM APIs are I/O-bound — streaming
tokens, calling providers, fetching documents. The loop-blocking bug is how
inference services degrade under two concurrent requests.

| Concept here | Used for |
|---|---|
| Async I/O | Concurrent LLM provider calls without blocking |
| run_in_threadpool | Calling sync tokenizers/embedders inside async handlers |
| Streaming | Token streaming keeps the loop free between chunks |
| def for blocking | Sync embedding libraries in threadpool handlers |
| Measuring | Load-testing serving endpoints before launch |

**Scale note:** at 200 concurrent LLM calls, a single blocking `time.sleep` in
an async handler is the difference between 200 overlapping calls and a 200x
serial queue. The async discipline is the serving layer's core performance
decision.

## 11. Summary

| Concept | Description |
|---|---|
| async def | Runs on the event loop; only for awaited I/O |
| def | Runs in the threadpool; correct for blocking code |
| Event loop | Single-threaded; blocked = whole process frozen |
| run_in_threadpool | Escape hatch inside async handlers |
| Measurement | Blocking-in-async serializes; await overlaps |

## 12. Quick Reference

| Task | Idiom |
|---|---|
| Awaited I/O | `async def` + `await async_call()` |
| Blocking library | `def` endpoint (threadpool) |
| Escape in async | `await run_in_threadpool(fn, *args)` |
| Detect the bug | Concurrent load test; latency grows linearly |
| Async HTTP | `httpx.AsyncClient` |

## Next Steps

Next: **[33 — Database Async](33-database-async-lecture.md)** — async sessions and pool sizing.

Continues in: **[02-advanced-python — 21 Concurrency Comparison](../../02-advanced-python/lectures/21-concurrency-comparison-lecture.md)** — threads vs processes vs async.

Official docs: <https://fastapi.tiangolo.com/async/> · <https://fastapi.tiangolo.com/advanced/async-sql-databases/>
