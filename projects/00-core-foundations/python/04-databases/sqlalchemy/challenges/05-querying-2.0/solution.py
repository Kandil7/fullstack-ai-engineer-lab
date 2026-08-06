"""
Challenge 05: Querying with select() — Reference Solution
===========================================================
Why this approach: scalars() unwraps ORM objects, execute() exposes
projections and aggregates, and join-then-filter is the shape every
leaderboard query uses. All filtering happens in SQL, not Python.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, and_, func, select
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
    stmt = (
        select(Experiment.name)
        .where(Experiment.status == "done")
        .order_by(Experiment.name)
    )
    return list(session.scalars(stmt).all())


def best_f1_per_model(session: Session) -> list[tuple[str, float]]:
    """(model, max f1) per model with at least one f1 metric, by model."""
    stmt = (
        select(Experiment.model, func.max(EvalMetric.value))
        .join(EvalMetric, EvalMetric.experiment_id == Experiment.id)
        .where(EvalMetric.metric == "f1")       # narrow BEFORE grouping
        .group_by(Experiment.model)
        .order_by(Experiment.model)
    )
    return [(model, max_f1) for model, max_f1 in session.execute(stmt)]


def metric_leaderboard(
    session: Session, metric: str, min_value: float, limit: int
) -> list[tuple[str, float]]:
    """(experiment_name, value) where value >= min_value, value DESC, limited."""
    stmt = (
        select(Experiment.name, EvalMetric.value)
        .join(EvalMetric, EvalMetric.experiment_id == Experiment.id)
        .where(and_(EvalMetric.metric == metric, EvalMetric.value >= min_value))
        .order_by(EvalMetric.value.desc())
        .limit(limit)
    )
    return [(name, value) for name, value in session.execute(stmt)]
