# FastAPI — 33: Database Async

Companion exercise: `33-database-async.py`

---

## Topic Overview

Async database access completes the async story: if your handlers are
`async def`, the database calls inside them must be awaitable too, or the loop
blocks. This topic covers the async SQLAlchemy/AIOSQLite pattern in FastAPI —
session-per-request dependency injection, transaction scope, and pool sizing —
and the failure mode that follows every async DB setup: **pool exhaustion**,
which shows up as 503s and timeout storms under load.

The mental model: one session per request, acquired through a dependency,
closed in `finally`; a connection pool sized to `workers x concurrent
requests`; and every await keeping the loop free.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why async handlers need async database calls.
2. Implement session-per-request DI with yield + finally.
3. Scope transactions correctly per request.
4. Size a connection pool using the workers x concurrency rule.
5. Recognize pool-exhaustion symptoms (503s, timeouts).
6. Choose async drivers (asyncpg/aiosqlite) for async endpoints.
7. Avoid blocking the loop with sync drivers.
8. Debug "database" slowness that is actually pool misconfiguration.

## Prerequisites

| Need | Where |
|---|---|
| Async endpoints | `32-async-endpoints-deep.py` |
| SQLAlchemy basics | `04-databases/sqlalchemy/01-core-vs-orm.py` |
| Dependency injection | `09-dependency-injection.py` |
| Pooling concepts | `04-databases/postgres/06-connection-pooling.py` |

## 1. Async Handlers Need Async Drivers

An `async def` endpoint calling a sync DB driver blocks the loop. The pairing
must be consistent:

| Handler | Driver | Result |
|---|---|---|
| async def | asyncpg / aiosqlite / async SQLAlchemy | Loop free, overlaps |
| async def | psycopg2 / sync SQLAlchemy | Loop blocked |
| def | any | Threadpool absorbs blocking |

The exercise uses `aiosqlite` when available and a stub otherwise — the DI
shape is what matters.

## 2. Session-per-Request DI

```python
async def get_db() -> AsyncDB:
    await db.connect()          # acquire for THIS request
    try:
        yield db                # handler uses it
    finally:
        await db.close()        # always released, even on error
```

Output:
```
# every request gets one session, released in finally
```

The `yield` dependency is the session-per-request pattern: acquire before the
handler, guarantee release after. FastAPI manages the generator lifecycle
automatically — including on exceptions.

## 3. Transaction Scope

A transaction should span exactly one request (or one unit of work):

```python
async with session.begin():          # or explicit commit/rollback
    await session.execute(...)
# committed or rolled back with the block
```

Output:
```
# one begin/commit per request; nothing leaks across requests
```

Rules: never hold a transaction open across requests; commit explicitly or
roll back; let the session close in `finally` regardless.

## 4. Pool Sizing — The Workers x Concurrency Rule

```python
def recommend_pool_size(workers, concurrency_per_worker=10):
    return {"pool_size": workers * concurrency_per_worker,
            "max_overflow": workers * concurrency_per_worker // 2}
```

Output:
```
{'pool_size': 40, 'max_overflow': 20, ...}   # for 4 workers
```

Under-sizing (pool of 5 for 4 workers x 10 concurrent) means requests queue
for a connection and 503. Over-sizing means idle connections and exhausted
file descriptors on the database. The rule: pool must cover peak concurrent
requests across all workers.

## 5. Pool Exhaustion — The Symptoms

When every connection is checked out:
- New requests wait for a free connection → latency spikes.
- Waits exceed timeouts → 503 / timeout storms.
- Postgres itself is fine; the pool is the bottleneck.

Diagnosis: monitor pool utilization; if it pins at 100% under normal load,
the pool is too small or connections are not being returned (leaked sessions).

## 6. Common Mistakes to Avoid

### Mistake 1: Sync driver in an async endpoint
```python
# WRONG — psycopg2/requests inside async def blocks the loop
# CORRECT — asyncpg / aiosqlite / def endpoint + threadpool
```

### Mistake 2: Sessions not closed
```python
# WRONG — acquire without finally; connections leak until pool exhaustion
# CORRECT — yield + finally in the dependency
```

### Mistake 3: Pool sized to workers, not concurrency
```python
# WRONG — pool_size = workers (4) when each worker handles 10 concurrent
# CORRECT — pool_size = workers x concurrency
```

### Mistake 4: Transactions spanning requests
```python
# WRONG — begin in one request, commit in another
# CORRECT — one begin/commit per request
```

### Mistake 5: Ignoring pool-monitoring signals
```python
# WRONG — 503s blamed on the DB while the pool pins at 100%
# CORRECT — watch utilization; return sessions; right-size the pool
```

## 7. Best Practices

1. Pair async handlers with async drivers.
2. Session-per-request via yield dependency; close in finally.
3. Scope one transaction per request.
4. Size pool = workers x concurrent requests per worker.
5. Monitor pool utilization; alarm on sustained 100%.
6. Set connection timeouts so waits fail fast instead of stacking.
7. Use `max_overflow` for burst headroom, not routine capacity.
8. Create the engine once at startup; never per request.
9. Keep echo off in production.
10. Load-test before trusting the sizing math.

## 8. Complexity and Cost

| Resource | Cost | Notes |
|---|---|---|
| Async session | O(1) per request | Allocated/released per request |
| Connection pool | fixed size | Idle connections cost DB resources |
| Transaction | O(ops) | Short and scoped |
| Pool wait | O(wait) | The failure mode — bounded by timeout |

The pool is a fixed resource: sizing it correctly is a capacity-planning
decision, not a tuning nicety.

## 9. AI Engineering Relevance

**Where this shows up:** every service that stores documents, vectors,
predictions, or usage records behind an async API. Feature stores, vector
stores, and eval databases all run through this pattern.

| Concept here | Used for |
|---|---|
| Async sessions | Concurrent ingestion into vector/feature stores |
| Pool sizing | Embedding services hitting Postgres/pgvector at scale |
| Session-per-request | Clean transaction scope in RAG write paths |
| Pool monitoring | The first alarm for a degrading ML service |
| Timeouts | Failing fast instead of queueing behind the DB |

**Scale note:** at high concurrency the DB is rarely the first to break — the
pool is. The classic incident: "database slow" turns out to be a leaked
session or an undersized pool pinning connections at 100%.

## 10. Summary

| Concept | Description |
|---|---|
| Async drivers | await-based clients for async handlers |
| Session-per-request | yield DI + finally close |
| Transaction scope | One begin/commit per request |
| Pool sizing | workers x concurrency |
| Pool exhaustion | 503s and timeouts from a saturated pool |

## 11. Quick Reference

| Task | Idiom |
|---|---|
| Async session DI | `async def get_db(): yield session; finally: close` |
| Transaction | `async with session.begin():` |
| Pool size | `workers * concurrency_per_worker` |
| Burst headroom | `max_overflow = pool_size // 2` |
| Async SQLAlchemy | `create_async_engine(url)` + `AsyncSession` |
| Watch for | 100% pool utilization = sizing bug |

## 12. Next Steps

Next: **[34 — Caching Strategies](34-caching-strategies-lecture.md)** — the layer above the database.

Continues in: **[04-databases — SQLAlchemy 07 Async](../../04-databases/sqlalchemy/lectures/07-async-sqlalchemy-lecture.md)** — the full async ORM pattern.

Official docs: <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html>
