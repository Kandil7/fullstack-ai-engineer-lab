"""
Challenge 07: Async SQLAlchemy — Reference Solution
=====================================================
Why this approach: the async API mirrors the sync one — only the await
boundary changes. A sessionmaker per engine keeps sessions isolated
per request, and run_sync bridges inherently-synchronous ORM helpers.
"""

from __future__ import annotations

from sqlalchemy import String, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
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


def _factory(engine):
    """One async_sessionmaker per engine (cached per call is fine)."""
    return async_sessionmaker(engine, expire_on_commit=False)


async def count_models(engine) -> list[str]:
    """Distinct model names from predictions, sorted ascending."""
    async with _factory(engine)() as session:
        stmt = select(Prediction.model).distinct().order_by(Prediction.model)
        return list(await session.scalars(stmt))


async def ingest_batch(engine, rows: list[dict]) -> int:
    """Insert {model, input_hash, latency_ms} rows; return rows written."""
    if not rows:
        return 0
    async with _factory(engine)() as session:
        session.add_all(
            [
                Prediction(
                    model=r["model"],
                    input_hash=r["input_hash"],
                    latency_ms=r["latency_ms"],
                )
                for r in rows
            ]
        )
        await session.commit()
        return len(rows)
    # On IntegrityError the `async with` closes the session: rollback is
    # guaranteed, so a later request on the same engine still works.


async def simulate_async_request(engine, model: str, input_hash: str) -> str:
    """Simulated endpoint body: write one prediction row; return confirmation."""
    async with _factory(engine)() as session:
        session.add(Prediction(model=model, input_hash=input_hash, latency_ms=7))
        await session.commit()
        return f"stored {input_hash}"


def _count_all_sync(session: AsyncSession) -> int:
    """Sync-style helper; run inside run_sync (must stay fully sync)."""
    return len(list(session.scalars(select(Prediction.id)).all()))


async def run_sync_count(engine) -> int:
    """Count all predictions through the run_sync greenlet bridge."""
    async with _factory(engine)() as session:
        return await session.run_sync(_count_all_sync)
