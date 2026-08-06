# Database Async — Glossary 33

Companion lecture: `33-database-async-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Async driver | Mechanism | Await-based DB client (asyncpg, aiosqlite) |
| Async session | Pattern | A session acquired and released per request |
| Checked out | Pool | A connection currently held by a request |
| Connection pool | Resource | The fixed set of DB connections shared by requests |
| Engine | Resource | The single DB factory created once at startup |
| Leaked session | Failure | A session never returned to the pool |
| max_overflow | Pool | Extra connections for burst headroom |
| Pool exhaustion | Failure | All connections busy; requests queue or fail |
| Pool utilization | Monitoring | The fraction of connections checked out |
| Session-per-request | Pattern | yield dependency scoping one session per request |
| Timeout | Resource | The bound on waiting for a connection |
| Transaction scope | Pattern | One begin/commit per request |
| Worker | Runtime | One uvicorn process handling requests |
| 503 | Failure | Service unavailable — the pool-exhaustion symptom |
| Async SQLAlchemy | Mechanism | SQLAlchemy's asyncio extension (AsyncEngine) |
| finally | Pattern | The guarantee that sessions are released |

## Detailed Definitions

### Async driver
**Definition**: A database client with await-based I/O — asyncpg, aiosqlite,
async SQLAlchemy — the correct companion to async handlers.
**Related**: Async SQLAlchemy

### Async session
**Definition**: A database session acquired for one request and released in
`finally`; the unit of work for async endpoints.
**Related**: Session-per-request

### Checked out
**Definition**: A connection currently held by a request — the state that
counts against pool utilization.
**Related**: Connection pool

### Connection pool
**Definition**: The fixed set of database connections created at startup and
shared across requests, avoiding per-request connection cost.
**Related**: Engine, Pool exhaustion

### Engine
**Definition**: The single database factory (SyncEngine/AsyncEngine) created
once at startup; pools live here.
**Related**: Connection pool

### Leaked session
**Definition**: A session acquired but never returned — a bug that silently
drains the pool until exhaustion.
**Related**: Pool exhaustion

### max_overflow
**Definition**: The pool option allowing extra connections beyond pool_size
for bursts; reserve for headroom, not routine capacity.
**Related**: Connection pool

### Pool exhaustion
**Definition**: The state where every connection is checked out; new requests
queue and eventually fail with 503s/timeouts.
**Related**: 503, Pool utilization

### Pool utilization
**Definition**: The fraction of pool connections checked out — sustained 100%
under normal load signals a sizing bug or leaked sessions.
**Related**: Pool exhaustion

### Session-per-request
**Definition**: The DI pattern acquiring one session per request via a `yield`
dependency and releasing it in `finally`.
**Example**:
```python
async def get_db():
    await db.connect()
    try:
        yield db
    finally:
        await db.close()
```
**Related**: Async session

### Timeout
**Definition**: The bound on waiting for a connection; without it, exhausted
pools stack requests indefinitely.
**Related**: Pool exhaustion

### Transaction scope
**Definition**: The rule that a transaction spans exactly one request —
begin/commit or rollback within the handler.
**Related**: Session-per-request

### Worker
**Definition**: One uvicorn process; the pool must cover all workers' peak
concurrency combined.
**Related**: Connection pool

### 503
**Definition**: Service Unavailable — the classic symptom of pool exhaustion
as waits exceed limits.
**Related**: Pool exhaustion

### Async SQLAlchemy
**Definition**: SQLAlchemy's asyncio extension — `create_async_engine` and
`AsyncSession` — letting ORM code run under async handlers.
**Related**: Async driver

### finally
**Definition**: The clause guaranteeing session release even when the handler
raises — the backbone of session-per-request.
**Related**: Session-per-request

## Key Concepts Summary

### The pairing rule
- Async handlers need async drivers; sync drivers belong in threads.
- Engine created once; sessions per request.

### Pool discipline
- Size = workers x concurrent requests per worker.
- max_overflow for bursts; monitor utilization.
- Leaked sessions are the silent killer; finally prevents them.

### Failure recognition
- 503s + timeouts under load = suspect the pool before the database.
- 100% utilization = sizing or leak problem.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The fixed set of connections shared by requests — ___
2. One session acquired and released per request — ___
3. A session never returned to the pool — ___
4. All connections busy; requests queue — ___
5. The single DB factory created at startup — ___
6. Extra connections for bursts — ___
7. The pool-exhaustion symptom — ___
8. The clause guaranteeing release — ___

**Answers:** 1-connection pool, 2-session-per-request, 3-leaked session,
4-pool exhaustion, 5-engine, 6-max_overflow, 7-503, 8-finally
