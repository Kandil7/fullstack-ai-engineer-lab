# Databases (SQLAlchemy) — 07: Async SQLAlchemy

## Topic Overview

Modern AI services are async: FastAPI endpoints, streaming inference gateways,
and training orchestrators all run on `asyncio`. SQLAlchemy's async support —
`create_async_engine`, `AsyncSession`, `async_sessionmaker` — mirrors the sync
API exactly: the statements are identical, only the `await` boundary changed.
The async dialect (here `aiosqlite`; in production `asyncpg` for Postgres)
drives the same SQL through an asyncio-compatible driver.

For AI/backend engineers this is the difference between blocking a single
event-loop thread per DB call and overlapping thousands of pending DB
operations. An async inference endpoint that stores predictions cannot afford
to block the loop; the async session is the standard answer. The one rule that
never bends: **never share an AsyncSession across tasks, and never call sync
Session methods on it** — the greenlet bridge (`run_sync`) exists for the rare
sync helper that must run inside async code.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create an `AsyncEngine` with `create_async_engine("sqlite+aiosqlite://", ...)`
2. Run Core statements with `async with engine.connect()` and `await`
3. Use `AsyncSession` for ORM writes and reads, awaiting every DB operation
4. Build sessions with `async_sessionmaker(engine, expire_on_commit=False)`
5. Bridge sync ORM helpers with `session.run_sync(...)` (the greenlet bridge)
6. Simulate the async session-per-request FastAPI pattern
7. Handle `IntegrityError` and keep the engine usable afterwards
8. Batch-ingest predictions with one `add_all` + one commit
9. Dispose the engine on shutdown to stop worker threads cleanly
10. Decide between sync and async SQLAlchemy for a service

---

## Prerequisites

| Need | Where |
|---|---|
| asyncio basics | `02-advanced-python/lectures/04-async-await-lecture.md` |
| Session lifecycle | `03-session-lifecycle-lecture.md` |
| Core transactions | `01-core-vs-orm-lecture.md` |

---

## 1. AsyncEngine: Core Statements, Await Boundary

The URL changes (`sqlite+aiosqlite://`) and every blocking call gains `await` —
the statement API is otherwise identical.

```python
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool

async_engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)

async def demo_core_roundtrip() -> int:
    async with async_engine.connect() as conn:
        return (await conn.execute(text("SELECT 1"))).scalar_one()
```

`StaticPool` pins one connection so every AsyncSession sees the same
in-memory database — the async equivalent of the shared-engine trick used
throughout this module.

## 2. AsyncSession: Add, Commit, Read — All Awaited

`AsyncSession` mirrors the sync `Session`: `add`/`commit`/`rollback` are now
coroutines. The rule: never share an AsyncSession across tasks, and never call
sync Session methods on it.

```python
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Prediction(Base):
    __tablename__ = "predictions"
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    latency_ms: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(12), default="ok")

async def demo_async_session() -> None:
    async with AsyncSession(async_engine) as session:
        session.add(Prediction(model="bert", input_hash="hash-0001", latency_ms=42))
        await session.commit()
        rows = await session.scalars(select(Prediction))
        for row in rows:
            print(f"async read: {row.model} {row.input_hash} {row.latency_ms}ms")
# Output:
# async read: bert hash-0001 42ms
```

## 3. async_sessionmaker: The Session Factory

`async_sessionmaker` is the async sibling of `sessionmaker`: one factory,
fresh `AsyncSession` per request/task — the production pattern for async
endpoints.

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

async def demo_sessionmaker() -> list[str]:
    async with AsyncSessionLocal() as session:
        session.add(Prediction(model="gpt2", input_hash="hash-0002", latency_ms=88))
        await session.commit()
    async with AsyncSessionLocal() as session:
        names = await session.scalars(
            select(Prediction.model).order_by(Prediction.model)
        )
        return list(names)
```

Two independent sessions, one factory, two transactions — the request-scoped
lifecycle made explicit.

## 4. run_sync: The Greenlet Bridge

Some ORM code is inherently synchronous: custom mixins, legacy helpers, or
sync-only libraries. `session.run_sync(fn)` hands a sync function the
AsyncSession and executes it inside a greenlet — the bridge that lets sync
ORM internals run on the async loop without deadlocking it.

```python
def _count_models_sync(session: AsyncSession) -> int:
    """Sync-style helper; run inside run_sync."""
    return len(list(session.scalars(select(Prediction.model)).all()))

async def demo_greenlet_bridge() -> int:
    async with AsyncSessionLocal() as session:
        return await session.run_sync(_count_models_sync)
```

The helper stays fully synchronous; `run_sync` is what converts it.

## 5. Async Session-per-Request (FastAPI Pattern)

The FastAPI dependency for async apps is an async generator that yields one
AsyncSession per request and closes it in `finally`:

```python
async def get_async_db():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
```

The simulated endpoint body — what `simulate_async_request` mirrors — writes
one row per request, exactly like a real endpoint:

```python
async def simulate_async_request(model: str, input_hash: str) -> str:
    async with AsyncSessionLocal() as session:
        session.add(Prediction(model=model, input_hash=input_hash, latency_ms=7))
        await session.commit()
        return f"stored {input_hash}"
```

## 6. Production Pattern: Batch Async Ingest

The batch ingest shape: one `add_all`, one commit, rows returned as a count.
On `IntegrityError` the `async with` closes the session — rollback is
guaranteed, so a later request on the same engine still works.

```python
async def ingest_predictions(rows: list[dict]) -> int:
    async with AsyncSessionLocal() as session:
        session.add_all([
            Prediction(model=r["model"], input_hash=r["input_hash"],
                       latency_ms=r["latency_ms"])
            for r in rows
        ])
        await session.commit()
        return len(rows)
```

---

## Common Mistakes to Avoid

### Mistake 1: Calling sync Session methods on an AsyncSession
```
# WRONG — blocks the loop; session.scalars is a coroutine here
rows = session.scalars(select(Prediction))          # coroutine, not rows
# CORRECT
rows = await session.scalars(select(Prediction))
```

### Mistake 2: Sharing one AsyncSession across tasks
```
# WRONG — interleaved transactions, corrupt identity map
session = AsyncSessionLocal()
task1 = asyncio.create_task(write(session)); task2 = asyncio.create_task(read(session))
# CORRECT — one session per task/request
```

### Mistake 3: Forgetting to dispose the engine on shutdown
```
# WRONG — aiosqlite worker threads keep the process alive (pytest hangs!)
# CORRECT
await async_engine.dispose()   # in finally / shutdown hook
```

### Mistake 4: Handling IntegrityError without closing the session
```
# WRONG — poisoned session reused by the next request
try:
    await session.commit()
except IntegrityError:
    pass
# CORRECT — the `async with` block closes on exception; rollback is automatic
```

### Mistake 5: Mixing sync engine and async session (or vice versa)
```
# WRONG — TypeError: AsyncSession with sync engine; or sync Session with async engine
# CORRECT — pair create_async_engine with AsyncSession/async_sessionmaker
```

---

## Best Practices

1. Pair `create_async_engine` with `AsyncSession`/`async_sessionmaker`
2. Await every DB operation; keep sync code inside `run_sync`
3. One session per task/request; never share across tasks
4. Use `expire_on_commit=False` to avoid post-commit lazy reloads
5. `await engine.dispose()` in shutdown/finally — worker threads are real
6. Handle errors at the session boundary (close/rollback before reusing)
7. Batch writes with `add_all` + one commit for ingest paths
8. Keep the URL dialect explicit: `sqlite+aiosqlite`, `postgresql+asyncpg`
9. Test async code with pytest-asyncio (`asyncio_mode = auto` here)
10. Mirror sync patterns: session-per-request maps 1:1 to async

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Async round trip | 1 await, non-blocking | O(1) | keep transactions short |
| run_sync bridge | greenlet switch overhead | O(1) | native async code where possible |
| Batch ingest | 1 round trip for N rows | O(N) params | chunk for huge N |
| engine.dispose | O(pool) | — | mandatory on shutdown |

**Cost note:** the win of async is **concurrency**, not speed per query: the
event loop overlaps DB waits with other work. That is why blocking the loop
with a sync call (Mistake 1) costs the whole service, not one request.

---

## AI Engineering Relevance

**Where this shows up:** FastAPI inference endpoints that store predictions,
async experiment trackers, streaming eval pipelines, and training
orchestrators that write metadata between steps.

| Concept here | Used for |
|---|---|
| AsyncSession | non-blocking prediction logging per request |
| async_sessionmaker | request-scoped sessions in async dependencies |
| run_sync | calling sync model helpers inside async code |
| batch ingest | flushing eval results without blocking the loop |

**Scale note:** at 200 concurrent inference requests, sync sessions would
serialize DB waits; async sessions overlap them. At 1M predictions/hour, batch
ingest (one commit per batch) is what keeps the DB write-amplification sane.

---

## Practice Exercises

### Exercise 1: Async Round Trip (Difficulty: Easy)
Create an async engine, run `SELECT 1`, and print the scalar. Confirm the
only change from sync is the `await`.

### Exercise 2: Write and Read Back (Difficulty: Easy)
Insert two predictions in one AsyncSession, then read them back in a second
session via `async_sessionmaker`. Print model + latency.

### Exercise 3: Greenlet Bridge (Difficulty: Medium)
Write a sync helper that counts rows, then call it via `session.run_sync`.
Verify the count equals what an awaited `select` returns.

### Exercise 4: Failure Recovery (Difficulty: Medium)
Insert a prediction, then attempt a duplicate `input_hash`. Catch
`IntegrityError`, then insert a fresh row and confirm the engine still works.

### Exercise 5: Async Request Simulation (Difficulty: Hard)
Implement `simulate_async_request` + `ingest_predictions` (sections 5-6) and
prove: rows persist, duplicate hashes raise, and the engine stays usable after
failures. (Challenge 07 tests exactly this.)

---

## Summary

| Concept | Description |
|---|---|
| AsyncEngine | `create_async_engine` + async dialect (aiosqlite/asyncpg) |
| AsyncSession | sync Session API with awaited DB operations |
| async_sessionmaker | request-scoped async sessions |
| run_sync | greenlet bridge for sync helpers |
| engine.dispose | shutdown cleanup; prevents hangs |
| batch ingest | `add_all` + one commit for throughput |

Async SQLAlchemy is the sync API plus `await`. Every pattern from topics
01-06 — sessions, relationships, eager loading — transfers directly once the
boundary discipline is understood.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Async engine | `create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)` |
| Session factory | `AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)` |
| Write | `async with AsyncSessionLocal() as s: s.add(x); await s.commit()` |
| Read | `rows = await s.scalars(select(M))` |
| Sync helper | `await s.run_sync(my_sync_fn)` |
| Shutdown | `await async_engine.dispose()` |

---

## Next Steps

Next: **[08 — Advanced Patterns](08-advanced-patterns-lecture.md)** — hybrid
properties, custom types, and optimistic locking.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
async SQLAlchemy in a FastAPI service.

Official docs:
- Async I/O: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- aiosqlite: https://aiosqlite.omnilib.dev/en/stable/
- asyncpg: https://magicstack.github.io/asyncpg/current/
