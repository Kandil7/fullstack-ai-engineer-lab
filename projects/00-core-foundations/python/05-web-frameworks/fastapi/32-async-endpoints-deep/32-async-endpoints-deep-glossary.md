# Async Endpoints Deep — Glossary 32

Companion lecture: `32-async-endpoints-deep-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| async def handler | Concurrency | Runs on the event loop; only for awaited I/O |
| Await point | Concurrency | Where the loop yields and switches to other work |
| Blocking call | Failure | Synchronous work that occupies the loop or thread |
| def handler | Concurrency | Runs in a worker thread from the threadpool |
| Event loop | Concurrency | The single thread juggling all async requests |
| I/O-bound | Workload | Work dominated by waiting on I/O |
| CPU-bound | Workload | Work dominated by computation |
| run_in_threadpool | Mechanism | FastAPI helper running a blocking call in a thread |
| Serialization | Failure | Concurrent requests executing one-after-another |
| Threadpool | Concurrency | The pool of worker threads for def handlers |
| Timeout | Failure | The symptom of a blocked loop under load |
| asyncio.gather | Mechanism | Running multiple awaitables concurrently |
| Overlap | Concurrency | Multiple I/O operations progressing simultaneously |
| Async driver | Mechanism | A client library with await-based I/O (asyncpg, httpx) |
| Sync driver | Mechanism | A blocking client (psycopg2, requests) |
| First-byte latency | Performance | Time until the first response bytes arrive |

## Detailed Definitions

### async def handler
**Definition**: An endpoint declared `async def`; FastAPI runs it directly on
the event loop. Correct only when its body awaits genuine I/O.
**Related**: Event loop, Await point

### Await point
**Definition**: A place where `await` yields control so the loop can run other
tasks; the mechanism behind concurrency.
**Related**: Event loop

### Blocking call
**Definition**: Synchronous work — `time.sleep`, `requests.get`, sync drivers,
CPU loops — that occupies its executor without yielding.
**Related**: Serialization

### def handler
**Definition**: An endpoint declared with plain `def`; FastAPI executes it in a
worker thread from the threadpool, keeping the loop free.
**Related**: Threadpool

### Event loop
**Definition**: The single thread that runs all async handlers and switches
between them at await points. A blocked loop freezes the whole process.
**Related**: async def handler

### I/O-bound
**Definition**: A workload dominated by waiting on I/O (network, disk) — where
async concurrency shines.
**Related**: CPU-bound

### CPU-bound
**Definition**: A workload dominated by computation — where threads don't help
and processes do.
**Related**: I/O-bound

### run_in_threadpool
**Definition**: `fastapi.concurrency.run_in_threadpool(fn, *args)` — runs a
blocking callable in a worker thread and returns an awaitable.
**Example**:
```python
result = await run_in_threadpool(blocking_work, 0.05)
```
**Related**: Threadpool

### Serialization
**Definition**: Concurrent requests executing one at a time — the outcome of
blocking calls inside async handlers.
**Related**: Blocking call

### Threadpool
**Definition**: The pool of worker threads FastAPI uses for `def` handlers;
sized to the workload, not to the number of workers.
**Related**: def handler

### Timeout
**Definition**: The observable symptom of a blocked loop — requests queue and
expire under load.
**Related**: Serialization

### asyncio.gather
**Definition**: Runs multiple awaitables concurrently and waits for all of
them — the tool for measuring overlap vs serialization.
**Example**:
```python
await asyncio.gather(*[body() for _ in range(4)])
```
**Related**: Overlap

### Overlap
**Definition**: Multiple I/O operations in flight simultaneously — the goal of
async code.
**Related**: asyncio.gather

### Async driver
**Definition**: A client library with await-based I/O (asyncpg, aiosqlite,
httpx.AsyncClient) — the correct companion to async handlers.
**Related**: Async driver

### Sync driver
**Definition**: A blocking client (psycopg2, requests, boto3 sync) — belongs in
`def` handlers or threads.
**Related**: run_in_threadpool

### First-byte latency
**Definition**: Time until the first bytes of a response arrive — the metric
streaming optimizes.
**Related**: I/O-bound

## Key Concepts Summary

### The handler-type rule
- async def: awaited I/O, runs on the loop.
- def: blocking code, runs in a threadpool.
- Blocking inside async def serializes the entire process.

### Escapes
- run_in_threadpool for blocking calls inside async flows.
- Async drivers let you stay async end to end.
- CPU-bound work belongs off the request path.

### Detection
- Concurrent load test: linear latency growth = blocked loop.
- Timeout storms under two concurrent requests = the bug.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The single thread running all async handlers — ___
2. Runs in a worker thread from the pool — ___
3. FastAPI helper running a blocking call in a thread — ___
4. Concurrent requests executing one at a time — ___
5. Where the loop yields and switches — ___
6. A blocking client library — ___
7. Running multiple awaitables concurrently — ___
8. Work dominated by waiting on I/O — ___

**Answers:** 1-event loop, 2-def handler, 3-run_in_threadpool, 4-serialization,
5-await point, 6-sync driver, 7-asyncio.gather, 8-I/O-bound
