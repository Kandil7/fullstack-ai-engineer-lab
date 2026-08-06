"""
Challenge 08: Advanced Patterns — Reference Solution
======================================================
Why this approach: hybrids keep one business rule in two contexts,
TypeDecorator hides binary encoding, the window function ranks in
SQL, and the version guard refuses stale writes.
"""

from __future__ import annotations

import array

from sqlalchemy import String, event, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import LargeBinary, TypeDecorator


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    score: Mapped[float] = mapped_column(default=0.0)
    version: Mapped[int] = mapped_column(default=1)

    @hybrid_property
    def is_leader(self) -> bool:
        """Python-side: score at or above the deployment bar."""
        return self.score >= 0.90

    @is_leader.expression
    def is_leader(cls) -> bool:
        """SQL-side: the SAME rule, compiled into WHERE clauses."""
        return cls.score >= 0.90


@event.listens_for(Experiment, "before_update")
def _bump_version(mapper, connection, target) -> None:
    """Increment version for any mapped update to an Experiment."""
    target.version += 1


class VectorType(TypeDecorator):
    """Stores an embedding (list[float]) as raw float32 bytes."""

    impl = LargeBinary
    cache_ok = True

    def __init__(self, dim: int = 8) -> None:
        self.dim = dim
        super().__init__()

    def bind_processor(self, dialect):
        def to_bytes(value: list[float] | None) -> bytes | None:
            if value is None:
                return None
            return array.array("f", value).tobytes()

        return to_bytes

    def result_processor(self, dialect, coltype):
        def to_list(raw: bytes | None) -> list[float] | None:
            if raw is None:
                return None
            return list(array.array("f", raw))

        return to_list


class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    chunk_id: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    vector: Mapped[list[float] | None] = mapped_column(VectorType(dim=8))


def promotable_experiments(session: Session) -> list[str]:
    """Names of experiments whose SQL-side is_leader is true, sorted."""
    stmt = (
        select(Experiment.name)
        .where(Experiment.is_leader)          # hybrid expression in SQL
        .order_by(Experiment.name)
    )
    return list(session.scalars(stmt).all())


def store_embedding(session: Session, chunk_id: str, vector: list[float]) -> int:
    """Store an embedding through VectorType; return the new id."""
    embedding = Embedding(chunk_id=chunk_id, vector=vector)
    session.add(embedding)
    session.commit()
    return embedding.id


def top_per_model(session: Session, k: int = 1) -> list[tuple[str, str, float]]:
    """Top-k experiments per model via row_number(); (name, model, score)."""
    rank = (
        func.row_number()
        .over(partition_by=Experiment.model, order_by=Experiment.score.desc())
        .label("rk")
    )
    ranked = select(
        Experiment.name,
        Experiment.model,
        Experiment.score,
        rank,
    ).subquery()
    stmt = (
        select(ranked.c.name, ranked.c.model, ranked.c.score)
        .where(ranked.c.rk <= k)
        .order_by(ranked.c.model, ranked.c.rk)
    )
    return [(n, m, s) for n, m, s in session.execute(stmt)]


def update_if_version(
    session: Session, experiment_id: int, expected_version: int, new_score: float
) -> bool:
    """Optimistic update: succeed only when the version still matches."""
    exp = session.get(Experiment, experiment_id)
    if exp is None or exp.version != expected_version:
        return False
    exp.score = new_score
    session.commit()  # before_update event bumps version in the same tx
    return True
