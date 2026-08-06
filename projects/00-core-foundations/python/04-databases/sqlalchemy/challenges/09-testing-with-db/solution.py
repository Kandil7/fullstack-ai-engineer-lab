"""
Challenge 09: Testing with a Database — Reference Solution
============================================================
Why this approach: the rollback fixture makes tests self-cleaning —
an outer transaction + SAVEPOINTs discards every write on close.
Factories apply column defaults explicitly so tests read intent,
not ORM timing.
"""

from __future__ import annotations

from sqlalchemy import JSON, String, create_engine, select
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
    experiment = Experiment(name=name, score=0.0, config={})
    for key, value in overrides.items():
        setattr(experiment, key, value)
    return experiment


def reset_schema(engine) -> None:
    """Drop all tables and recreate them from the metadata."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def transactional_session(eng):
    """Yield a session whose writes roll back when the generator ends."""
    connection = eng.connect()
    outer = connection.begin()  # outer transaction: never committed
    session = Session(
        bind=connection, join_transaction_mode="create_savepoint"
    )
    try:
        yield session
    finally:
        session.close()
        outer.rollback()  # discard every write the test made
        connection.close()


def run_isolated_tests(eng) -> tuple[int, int]:
    """Simulate two tests on one engine; return (rows_test1_saw, rows_test2_saw)."""
    # "test 1": writes inside a rollback fixture, counts what it can see
    gen = transactional_session(eng)
    session = next(gen)
    session.add_all([make_experiment("t1-a"), make_experiment("t1-b")])
    seen_test1 = len(session.scalars(select(Experiment.id)).all())
    gen.close()  # rollback: rows vanish

    # "test 2": a plain committed session must see NONE of test 1's rows
    with Session(bind=eng) as fresh:
        seen_test2 = len(fresh.scalars(select(Experiment.id)).all())
    return seen_test1, seen_test2
