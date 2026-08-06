"""
Challenge 05: Querying with select() — Starter Code
=====================================================
Fill in the function bodies. Do not modify signatures.
Topic: select(), scalars(), joins, aggregates, ordering.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(12), default="running")


class EvalMetric(Base):
    __tablename__ = "eval_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.id"), nullable=False
    )
    metric: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)


def done_experiments(session: Session) -> list[str]:
    """Names of experiments with status == 'done', sorted ascending."""
    raise NotImplementedError


def best_f1_per_model(session: Session) -> list[tuple[str, float]]:
    """(model, max f1) per model with at least one f1 metric, by model."""
    raise NotImplementedError


def metric_leaderboard(
    session: Session, metric: str, min_value: float, limit: int
) -> list[tuple[str, float]]:
    """(experiment_name, value) where value >= min_value, value DESC, limited."""
    raise NotImplementedError
