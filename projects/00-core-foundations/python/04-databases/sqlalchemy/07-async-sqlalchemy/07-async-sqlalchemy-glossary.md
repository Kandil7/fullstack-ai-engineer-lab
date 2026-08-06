# Async SQLAlchemy — Glossary 07

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| aiosqlite | Driver | The asyncio-compatible sqlite driver (`sqlite+aiosqlite://`) |
| asyncpg | Driver | The asyncio-compatible Postgres driver (`postgresql+asyncpg://`) |
| AsyncEngine | Engine | `create_async_engine` — the async sibling of `Engine` |
| AsyncSession | Session | Sync `Session` API with awaited DB operations |
| async_sessionmaker | Factory | Request-scoped `AsyncSession` factory for async apps |
| Await boundary | Concept | Every blocking DB call gains `await`; statements otherwise identical |
| Event loop | Concept | The single thread that schedules coroutines; must never block |
| expire_on_commit | Session | `False` keeps objects usable after commit (no lazy reload) |
| Greenlet bridge | Technique | `session.run_sync(fn)` running sync ORM code inside async |
| IntegrityError | Failure | Constraint violation; the `async with` block rolls back on exit |
| Session-per-request | Pattern | One fresh `AsyncSession` per request/task, closed in `finally` |
| StaticPool | Pool | Pins one connection so all async sessions share one in-memory DB |

## Detailed Definitions

### aiosqlite
**Definition**: The asyncio driver for sqlite used by SQLAlchemy's async
dialect — the URL is `sqlite+aiosqlite://`.
**Related**: AsyncEngine

### asyncpg
**Definition**: The asyncio driver for Postgres (`postgresql+asyncpg://`) —
the production counterpart to aiosqlite.
**Related**: AsyncEngine

### AsyncEngine
**Definition**: Created by `create_async_engine`; runs statements through an
async dialect. Core work: `async with engine.connect()` + `await conn.execute(...)`.
**Example**:
```python
async_engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
```
**Related**: aiosqlite

### AsyncSession
**Definition**: The async mirror of `Session` — `add`/`commit`/`rollback`/
`scalars` are coroutines and must be awaited. Never call the sync methods on
it; never share it across tasks.
**Related**: Await boundary

### async_sessionmaker
**Definition**: The async sibling of `sessionmaker` — a factory producing a
fresh `AsyncSession` per request/task; the production pattern for async
endpoints.
**Example**:
```python
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
```
**Related**: Session-per-request

### Await boundary
**Definition**: The discipline that sync and async SQLAlchemy share the same
statement API; only the DB operations change (adding `await`). Forgetting
the boundary blocks the loop and stalls the whole service.
**Related**: Event loop

### Event loop
**Definition**: The single thread that schedules asyncio coroutines; any
blocking call inside it stalls every concurrent request — the reason async
DB access must never block.
**Related**: Await boundary

### expire_on_commit
**Definition**: When `False`, objects keep their loaded state after commit —
avoiding post-commit lazy reloads that fire unexpected SQL (or block in
async code).
**Related**: AsyncSession

### Greenlet bridge
**Definition**: `session.run_sync(sync_fn)` executes a synchronous ORM helper
inside the async loop via a greenlet — the escape hatch for sync-only model
code.
**Example**:
```python
await session.run_sync(_count_models_sync)
```
**Related**: AsyncSession

### IntegrityError
**Definition**: A constraint violation (e.g. duplicate unique key) raised
during flush/commit; because the session lives in an `async with` block, the
exception closes it and the engine stays usable for the next request.
**Related**: Session-per-request

### Session-per-request
**Definition**: The production lifecycle — an async generator dependency
yields one `AsyncSession` per request and closes it in `finally`; never share
sessions across tasks.
**Related**: async_sessionmaker

### StaticPool
**Definition**: A connection pool pinning a single connection — the async
equivalent of the shared-engine trick, letting every `AsyncSession` see the
same in-memory database.
**Related**: AsyncEngine

## Key Concepts Summary

### The async discipline
- Pair `create_async_engine` with `AsyncSession`/`async_sessionmaker`.
- Await every DB operation; sync code goes inside `run_sync`.
- One session per task/request; never share across tasks.
- `expire_on_commit=False` avoids post-commit surprises.
- `await engine.dispose()` on shutdown — worker threads are real.

### The win is concurrency, not speed
- Async overlaps DB waits with other work.
- One blocking call stalls every concurrent request.
- Batch writes (`add_all` + one commit) keep the write path efficient.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The async sqlite driver — ___
2. One fresh session per request, closed in finally — ___
3. Running sync ORM code inside async — ___
4. Every DB call gains this — ___
5. The factory for request-scoped async sessions — ___
6. Never block this — ___
7. Shutdown cleanup that prevents hangs — ___
8. `False` prevents post-commit lazy reloads — ___

**Answers:** 1-aiosqlite, 2-session-per-request, 3-greenlet bridge (run_sync),
4-await boundary, 5-async_sessionmaker, 6-event loop, 7-engine.dispose(),
8-expire_on_commit
