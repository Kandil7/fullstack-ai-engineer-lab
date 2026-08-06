"""
Challenge 10: Repository Pattern — Starter Code
=================================================
Fill in the bodies. Do not modify signatures or the Protocol.
Topic: domain rules, repository contract, Unit of Work.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from sqlalchemy import String
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
    raise NotImplementedError


def best_model_name(experiments: list[Experiment]) -> str | None:
    """Pure domain query: model of the highest-scoring run, or None."""
    raise NotImplementedError


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

    def add(self, experiment: Experiment) -> int:
        raise NotImplementedError

    def get(self, name: str) -> Experiment | None:
        raise NotImplementedError

    def list_all(self) -> list[Experiment]:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def delete(self, name: str) -> bool:
        raise NotImplementedError


class SqlExperimentRepository:
    """Repository backed by SQLAlchemy. Session = injected Unit of Work."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, experiment: Experiment) -> int:
        raise NotImplementedError

    def get(self, name: str) -> Experiment | None:
        raise NotImplementedError

    def list_all(self) -> list[Experiment]:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def delete(self, name: str) -> bool:
        raise NotImplementedError


def register_batch_with_transaction(
    session: Session, experiments: list[Experiment]
) -> list[int]:
    """All-or-nothing batch registration; raise ValueError on duplicates."""
    raise NotImplementedError
