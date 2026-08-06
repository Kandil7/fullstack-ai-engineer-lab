"""
04-databases/sqlalchemy — 07: Async SQLAlchemy
================================================
Topics: AsyncEngine/AsyncSession; async with; greenlet bridge;
        async pooling; FastAPI integration.

Why this matters for AI/backend engineering:
    Async inference services and FastAPI endpoints share a problem:
    the event loop must NEVER block on a database round-trip. Async
    SQLAlchemy (AsyncEngine + AsyncSession, driven by aiosqlite or
    asyncpg) keeps the loop free so one process can serve hundreds
    of concurrent requests — including batch prediction endpoints
    that each write their results row. The greenlet bridge is the
    trick that lets the ORM's synchronous internals run inside an
    async application.

Run:      python 07-async-sqlalchemy.py
Verify:   python 07-async-sqlalchemy.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
"""

from __future__ import annotations

import asyncio
import sys

try:
    import aiosqlite  # noqa: F401  (the asyncio driver for SQLite)
except ImportError:
    print("[skip] aiosqlite not installed -- pip install aiosqlite")
    sys.exit(0)

from sqlalchemy import String, select, text  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

# ============================================================
# 0. Async engine + model
# ============================================================
# The URL differs from the sync one: "sqlite+aiosqlite://".
# StaticPool pins ONE connection so every AsyncSession sees the
# same in-memory database (the async equivalent of topic 03's
# shared-engine trick).
async_engine = create_async_engine(
    "sqlite+aiosqlite://",
    poolclass=StaticPool,
)


class Base(DeclarativeBase):
    pass


class Prediction(Base):
    """One model inference result — the row an async endpoint writes."""

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    latency_ms: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(12), default="ok")


# ============================================================
# 1. AsyncEngine: Core statements await the same way
# ============================================================
# Everything that touched a sync Connection now awaits inside
# "async with engine.connect()". The statement API is identical —
# only the await boundary changed.

async def demo_core_roundtrip() -> int:
    """SELECT 1 through the async engine; returns the scalar."""
    async with async_engine.connect() as conn:
        return (await conn.execute(text("SELECT 1"))).scalar_one()


# ============================================================
# 2. AsyncSession: await every database operation
# ============================================================
# AsyncSession mirrors the sync Session: add/commit/rollback are
# now coroutines. The one rule: never share an AsyncSession across
# tasks, and never call sync Session methods on it.

async def demo_async_session() -> None:
    """Insert rows via AsyncSession and read them back."""
    async with AsyncSession(async_engine) as session:
        session.add(
            Prediction(model="bert", input_hash="hash-0001", latency_ms=42)
        )
        await session.commit()

        rows = await session.scalars(select(Prediction))
        for row in rows:
            print(f"async read: {row.model} {row.input_hash} {row.latency_ms}ms")

    # Output:
    # async read: bert hash-0001 42ms


# ============================================================
# 3. async_sessionmaker: the production session factory
# ============================================================
# async_sessionmaker is the async sibling of sessionmaker: one
# factory, fresh AsyncSession per request/task.

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def demo_sessionmaker() -> list[str]:
    """Two independent async sessions write and read the same rows."""
    async with AsyncSessionLocal() as session:
        session.add(
            Prediction(model="gpt2", input_hash="hash-0002", latency_ms=88)
        )
        await session.commit()

    async with AsyncSessionLocal() as session:
        names = await session.scalars(
            select(Prediction.model).order_by(Prediction.model)
        )
        return list(names)


# ============================================================
# 4. run_sync: the greenlet bridge
# ============================================================
# Some ORM code is inherently synchronous (custom mixins, legacy
# helpers). session.run_sync() hands a sync function the AsyncSession
# and executes it inside a greenlet — the bridge that lets sync
# ORM internals run on the async loop without deadlocking it.

def _count_models_sync(session: AsyncSession) -> int:
    """Sync-style helper; run inside run_sync."""
    return len(list(session.scalars(select(Prediction.model)).all()))


async def demo_greenlet_bridge() -> int:
    """Count rows through run_sync — the greenlet bridge in action."""
    async with AsyncSessionLocal() as session:
        return await session.run_sync(_count_models_sync)


# ============================================================
# 5. Async session-per-request (FastAPI pattern, simulated)
# ============================================================
# The FastAPI dependency for async apps is an async generator that
# yields one AsyncSession per request and closes it in finally:
#
#   async def get_async_db():
#       session = AsyncSessionLocal()
#       try:
#           yield session
#       finally:
#           await session.close()
#
# FastAPI awaits that teardown for you. No server is started here —
# the lifecycle is simulated by simulate_async_request below, which
# mirrors exactly what an endpoint body does.

async def simulate_async_request(model: str, input_hash: str) -> str:
    """Simulated endpoint body: write one prediction row."""
    async with AsyncSessionLocal() as session:
        session.add(
            Prediction(model=model, input_hash=input_hash, latency_ms=7)
        )
        await session.commit()
        return f"stored {input_hash}"


# ============================================================
# 6. Production Pattern: batch async ingest
# ============================================================
# An async endpoint that stores N prediction rows concurrently is a
# temptation to fire N sessions. The right shape: ONE session, ONE
# transaction, all rows buffered — batching beats concurrency for
# writes because the commit is the expensive part.

async def ingest_predictions(rows: list[dict]) -> int:
    """Insert rows in one async transaction; return stored count."""
    async with AsyncSessionLocal() as session:
        session.add_all(Prediction(**row) for row in rows)
        await session.commit()
        return len(rows)


# ============================================================
# 7. main(): the async entry point
# ============================================================
async def main() -> None:
    """Run every demo in order; prints stay ASCII-safe."""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        one = await demo_core_roundtrip()
        print(f"async round-trip SELECT 1 -> {one}")

        await demo_async_session()

        models = await demo_sessionmaker()
        print(f"models after two sessions: {models}")

        count = await demo_greenlet_bridge()
        print(f"run_sync count: {count}")

        print(await simulate_async_request("llama", "hash-0003"))

        stored = await ingest_predictions(
            [
                {"model": "bert", "input_hash": "hash-0010", "latency_ms": 10},
                {"model": "bert", "input_hash": "hash-0011", "latency_ms": 11},
                {"model": "gpt2", "input_hash": "hash-0012", "latency_ms": 12},
            ]
        )
        print(f"batch ingested: {stored}")
    finally:
        await async_engine.dispose()

    # Output:
    # async round-trip SELECT 1 -> 1
    # async read: bert hash-0001 42ms
    # models after two sessions: ['bert', 'gpt2']
    # run_sync count: 2
    # stored hash-0003
    # batch ingested: 3


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: awaiting sync Session methods.
#   await session.query(Prediction).all()   # AttributeError: no await
# CORRECT: use the 2.0 select() API and await scalars()/execute().
#
# MISTAKE: sharing one AsyncSession across concurrent tasks.
#   results = await gather(session.get(...), session.get(...))
# CORRECT: one AsyncSession per task/request — sessions are not
#   safe to share, exactly like sync sessions.
#
# MISTAKE: blocking the loop with a sync driver on the same engine.
# CORRECT: pick an async driver (aiosqlite/asyncpg) AND remember
#   aiosqlite is not a speed-up — it is a non-blocking driver; the
#   win is concurrency, not raw throughput.


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
async def _verify_async() -> None:
    """Assert every claim this file makes. Silent on success."""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # 1. Async Core round-trip works
        assert await demo_core_roundtrip() == 1, "async Core SELECT 1 must work"

        # 2. AsyncSession insert + read back
        async with AsyncSession(async_engine) as session:
            session.add(
                Prediction(model="verify-model", input_hash="v-hash-1", latency_ms=5)
            )
            await session.commit()
            found = await session.scalars(
                select(Prediction).where(Prediction.input_hash == "v-hash-1")
            )
            assert found.one().model == "verify-model", "async session must persist"

        # 3. async_sessionmaker: the SECOND session sees the FIRST session's
        #    commit — sessions are independent, the database is shared
        models = await demo_sessionmaker()
        assert "gpt2" in models and "verify-model" in models, \
            "sessionmaker must share the DB across sessions"

        # 4. Greenlet bridge returns sync-helper results
        #    (rows so far: verify-model + gpt2 = 2)
        assert await demo_greenlet_bridge() == 2, "run_sync must count rows"

        # 5. Simulated request lifecycle persists its row
        msg = await simulate_async_request("llama", "v-hash-2")
        assert msg == "stored v-hash-2", "simulated request must store the row"

        # 6. Batch ingest stores every row in one transaction
        stored = await ingest_predictions(
            [
                {"model": "bert", "input_hash": "v-hash-3", "latency_ms": 1},
                {"model": "bert", "input_hash": "v-hash-4", "latency_ms": 2},
            ]
        )
        assert stored == 2, "batch ingest must return rows stored"

        # 7. Unique constraint on input_hash is enforced (dedupe guard)
        try:
            await ingest_predictions(
                [{"model": "bert", "input_hash": "v-hash-3", "latency_ms": 9}]
            )
            raise AssertionError("duplicate input_hash must raise IntegrityError")
        except Exception as exc:
            assert "UNIQUE" in str(exc) or "Integrity" in type(exc).__name__, \
                "duplicate input_hash must be rejected by the DB"

        print("[OK] 07-async-sqlalchemy: all checks passed")
    finally:
        # aiosqlite runs one worker thread per connection; dispose() closes
        # them so the process can exit on Windows (no lingering handles)
        await async_engine.dispose()


def _verify() -> None:
    """Sync wrapper so the file keeps the mandatory _verify() shape."""
    asyncio.run(_verify_async())


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. AsyncEngine/AsyncSession move the await boundary to the DB")
        print("2. run_sync is the greenlet bridge for sync ORM helpers")
        print("3. One AsyncSession per request; batch writes in one transaction")
        _verify()  # always runs, so plain execution is also a test
