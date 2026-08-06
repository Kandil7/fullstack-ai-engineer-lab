"""
Challenge 09: Testing with a Database — Starter Code
======================================================
Fill in the function bodies. Do not modify signatures.
Topic: test isolation, rollback fixtures, schema resets.
"""

from __future__ import annotations

from sqlalchemy import JSON, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    score: Mapped[float] = mapped_column(default=0.0)
    config: Mapped[dict] = mapped_column(JSON, default=dict)


def make_experiment(name: str, **overrides) -> Experiment:
    """Build an Experiment with column defaults applied, plus overrides."""
    raise NotImplementedError


def reset_schema(engine) -> None:
    """Drop all tables and recreate them from the metadata."""
    raise NotImplementedError


def transactional_session(eng):
    """Yield a session whose writes roll back when the generator ends.

    Bind the session to a connection holding an OUTER transaction and
    join it via SAVEPOINTs; on close, roll the outer transaction back.
    """
    raise NotImplementedError


def run_isolated_tests(eng) -> tuple[int, int]:
    """Simulate two tests on one engine; return (rows_test1_saw, rows_test2_saw)."""
    raise NotImplementedError
