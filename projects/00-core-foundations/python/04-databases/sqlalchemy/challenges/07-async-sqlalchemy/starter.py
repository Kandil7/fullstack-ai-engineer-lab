"""
Challenge 07: Async SQLAlchemy — Starter Code
===============================================
Fill in the function bodies. Do not modify signatures.
Topic: AsyncEngine, AsyncSession, async_sessionmaker, run_sync.
"""

from __future__ import annotations

from sqlalchemy import String
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


async def count_models(engine) -> list[str]:
    """Distinct model names from predictions, sorted ascending."""
    raise NotImplementedError


async def ingest_batch(engine, rows: list[dict]) -> int:
    """Insert {model, input_hash, latency_ms} rows; return rows written."""
    raise NotImplementedError


async def simulate_async_request(engine, model: str, input_hash: str) -> str:
    """Simulated endpoint body: write one prediction row; return confirmation."""
    raise NotImplementedError


async def run_sync_count(engine) -> int:
    """Count all predictions through the run_sync greenlet bridge."""
    raise NotImplementedError
