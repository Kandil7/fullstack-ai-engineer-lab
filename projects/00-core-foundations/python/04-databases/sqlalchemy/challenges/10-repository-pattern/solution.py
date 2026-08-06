"""
Challenge 10: Repository Pattern — Reference Solution
=======================================================
Why this approach: domain rules stay pure (testable without a DB),
repositories sit behind one Protocol (swap storage freely), and the
Unit of Work keeps transaction ownership with the caller.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    """A training/eval run. Pure persistence shape — NO business logic."""

    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    score: Mapped[float] = mapped_column(default=0.0)


PROMOTE_THRESHOLD = 0.9


def should_promote(score: float) -> bool:
    """Pure domain rule: is this run good enough to promote?"""
    return score >= PROMOTE_THRESHOLD


def best_model_name(experiments: list[Experiment]) -> str | None:
    """Pure domain query: model of the highest-scoring run, or None."""
    if not experiments:
        return None
    return max(experiments, key=lambda e: e.score).model


@runtime_checkable
class ExperimentRepository(Protocol):
    """Storage contract: how experiments are stored is an implementation detail."""

    def add(self, experiment: Experiment) -> int:
        """Persist an experiment; return its id."""
        ...

    def get(self, name: str) -> Experiment | None:
        """Fetch one experiment by name, or None."""
        ...

    def list_all(self) -> list[Experiment]:
        """Return every stored experiment."""
        ...

    def count(self) -> int:
        """Number of stored experiments."""
        ...

    def delete(self, name: str) -> bool:
        """Remove an experiment; True if it existed."""
        ...


class InMemoryExperimentRepository:
    """Repository backed by a plain dict (for unit tests)."""

    def __init__(self) -> None:
        self._store: dict[str, Experiment] = {}
        self._next_id = 1

    def add(self, experiment: Experiment) -> int:
        if experiment.name in self._store:
            raise ValueError(f"duplicate experiment name: {experiment.name}")
        experiment.id = self._next_id
        self._next_id += 1
        self._store[experiment.name] = experiment
        return experiment.id

    def get(self, name: str) -> Experiment | None:
        return self._store.get(name)

    def list_all(self) -> list[Experiment]:
        return list(self._store.values())

    def count(self) -> int:
        return len(self._store)

    def delete(self, name: str) -> bool:
        return self._store.pop(name, None) is not None


class SqlExperimentRepository:
    """Repository backed by SQLAlchemy. Session = injected Unit of Work."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, experiment: Experiment) -> int:
        self.session.add(experiment)
        self.session.flush()  # assign the PK; commit stays with the caller
        return experiment.id

    def get(self, name: str) -> Experiment | None:
        return self.session.scalars(
            select(Experiment).where(Experiment.name == name)
        ).first()

    def list_all(self) -> list[Experiment]:
        return list(self.session.scalars(select(Experiment).order_by(Experiment.id)))

    def count(self) -> int:
        return len(self.session.scalars(select(Experiment.id)).all())

    def delete(self, name: str) -> bool:
        experiment = self.get(name)
        if experiment is None:
            return False
        self.session.delete(experiment)
        self.session.flush()
        return True


def register_batch_with_transaction(
    session: Session, experiments: list[Experiment]
) -> list[int]:
    """All-or-nothing batch registration; raise ValueError on duplicates."""
    try:
        session.add_all(experiments)
        session.flush()  # duplicates surface here as IntegrityError
    except Exception:
        session.rollback()
        raise ValueError("duplicate experiment name in batch") from None
    session.commit()
    return [exp.id for exp in experiments]
