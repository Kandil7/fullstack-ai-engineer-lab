"""
04-databases/sqlalchemy — 02: Declarative Models
==================================================
Topics: DeclarativeBase; Mapped/mapped_column (2.0 typed style);
        constraints; __table_args__.

Why this matters for AI/backend engineering:
    The models you declare here ARE your schema contract — every table
    in an AI service (runs, models, datasets, eval results) starts as a
    mapped class. The 2.0 `Mapped[...]` style makes the column type
    explicit at the Python level so a FutureWarning-free codebase is
    also a self-documenting one. Constraints (unique, not-null, check)
    are where data integrity lives; the ORM will not silently fix bad
    data for you.

Run:      python 02-declarative-models.py
Verify:   python 02-declarative-models.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
"""

from __future__ import annotations

import sys
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    create_engine,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# ============================================================
# 1. DeclarativeBase — the 2.0 way to start a mapping
# ============================================================
# One Base per application. Every model inherits from it; the class
# attributes become table columns. 1.x style used `declarative_base()`
# with `Column(...)` everywhere; 2.0 prefers `Mapped[...]` + 
# `mapped_column(...)` so the type is checked twice (Python + DB).


class Base(DeclarativeBase):
    """Application-wide declarative base (SQLAlchemy 2.0 style)."""


class Experiment(Base):
    """One ML training/eval run. Constraints enforce data honesty."""

    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    model: Mapped[str] = mapped_column(String(60), nullable=False)
    # Optional columns are declared as Optional[...] — NULL is allowed.
    notes: Mapped[Optional[str]] = mapped_column(String(200))
    # Python-side default; the DB also gets a DEFAULT clause.
    score: Mapped[float] = mapped_column(default=0.0)

    # __table_args__ holds table-level constraints and indexes.
    __table_args__ = (
        CheckConstraint("score >= 0.0 AND score <= 1.0", name="ck_score_range"),
        Index("ix_experiments_model", "model"),
    )


# ============================================================
# 2. Mapped[...] and mapped_column(...)
# ============================================================
# Plain `name: Mapped[str]` maps to VARCHAR (unbounded text on
# SQLite/Postgres 'text'). Add mapped_column(...) when you need length,
# defaults, or constraints. `id: Mapped[int] = mapped_column(primary_key=True)`
# is the minimal PK; integer PKs auto-increment on SQLite and Postgres.

# Example 1: create the schema from the model metadata
engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

# Example 2: inspect what the model actually declared
from sqlalchemy import inspect  # noqa: E402

insp = inspect(engine)
table = insp.get_table_names()
print(f"tables created: {table}")

# Output:
# tables created: ['experiments']

cols = {c["name"]: c for c in insp.get_columns("experiments")}
print(f"columns: {sorted(cols)}")

# Output:
# columns: ['id', 'model', 'name', 'notes', 'score']

assert cols["notes"]["nullable"] is True, "notes must be nullable"
print(f"notes nullable: {cols['notes']['nullable']}")

# Output:
# notes nullable: True

# ============================================================
# 3. Constraints enforced by the database, not just Python
# ============================================================
# Unique, NOT NULL, and CHECK constraints are enforced at the DB layer.
# The ORM will happily try to insert anything you give it; the database
# says no. This is why constraints live in the schema, not in validation.

def _fresh_session() -> Session:
    """Return a session bound to a fresh in-memory DB with the schema."""
    return Session(bind=engine)


# Example 1: create the schema from the model metadata
# (called AFTER all models are defined so every table is created)
Base.metadata.create_all(engine)


with _fresh_session() as session:
    session.add(Experiment(name="run-1", model="bert", score=0.91))
    session.commit()

# Example 3: duplicate name -> IntegrityError (UNIQUE constraint)
try:
    with _fresh_session() as session:
        session.add(Experiment(name="run-1", model="gpt", score=0.5))
        session.commit()
except IntegrityError as exc:
    print(f"duplicate name rejected: {type(exc).__name__}")

# Output:
# duplicate name rejected: IntegrityError

# Example 4: missing model -> IntegrityError (NOT NULL constraint)
try:
    with _fresh_session() as session:
        session.add(Experiment(name="run-2", score=0.4))
        session.commit()
except IntegrityError as exc:
    print(f"missing model rejected: {type(exc).__name__}")

# Output:
# missing model rejected: IntegrityError

# Example 5: out-of-range score -> IntegrityError (CHECK constraint)
try:
    with _fresh_session() as session:
        session.add(Experiment(name="run-3", model="bert", score=1.5))
        session.commit()
except IntegrityError as exc:
    print(f"bad score rejected: {type(exc).__name__}")

# Output:
# bad score rejected: IntegrityError

# ============================================================
# 4. __table_args__: unique together and composite indexes
# ============================================================
# Some constraints span multiple columns. `UniqueConstraint` makes
# (a, b) unique as a PAIR; a single column can repeat. Composite
# indexes serve queries that filter on both columns at once.

from sqlalchemy import Column, Integer, UniqueConstraint as UC  # noqa: E402


class TrainingStep(Base):
    __tablename__ = "training_steps"
    __table_args__ = (UC("experiment_id", "step", name="uq_step_per_experiment"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.id"), nullable=False
    )
    step: Mapped[int] = mapped_column(Integer, nullable=False)
    loss: Mapped[float] = mapped_column(default=0.0)


Base.metadata.create_all(engine)

with _fresh_session() as session:
    session.add(TrainingStep(experiment_id=1, step=0, loss=2.4))
    session.add(TrainingStep(experiment_id=1, step=1, loss=1.9))
    session.commit()

# Example 6: same (experiment, step) pair is rejected, but step may repeat
#            for a different experiment_id.
try:
    with _fresh_session() as session:
        session.add(TrainingStep(experiment_id=1, step=0, loss=0.1))
        session.commit()
except IntegrityError as exc:
    print(f"duplicate (experiment, step) rejected: {type(exc).__name__}")

# Output:
# duplicate (experiment, step) rejected: IntegrityError

with _fresh_session() as session:
    session.add(TrainingStep(experiment_id=1, step=2, loss=1.5))
    session.commit()

with _fresh_session() as session:
    steps = session.scalars(select(TrainingStep.step).order_by(TrainingStep.step)).all()
    print(f"allowed steps: {steps}")

# Output:
# allowed steps: [0, 1, 2]

# ============================================================
# 5. Production Pattern: model versioning table
# ============================================================
# A real pattern from MLOps registries: model versions must be unique
# per (model_name, version), with a versioned payload column and a
# check that keeps version numbers sane.

class ModelVersion(Base):
    __tablename__ = "model_versions"
    __table_args__ = (
        UC("model_name", "version", name="uq_model_version"),
        CheckConstraint("version >= 1", name="ck_version_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(String(80), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    artifact_uri: Mapped[str] = mapped_column(String(300), nullable=False)


# create_all is idempotent (checkfirst=True); create the last model's table.
Base.metadata.create_all(engine)


def register_version(model_name: str, version: int, artifact_uri: str) -> ModelVersion:
    """Register a model version; lets IntegrityError propagate to caller.

    commit() expires every attribute (see topic 03), so refresh() loads
    them back before the session closes — otherwise the caller gets a
    DetachedInstanceError on first attribute access.
    """
    with _fresh_session() as session:
        mv = ModelVersion(
            model_name=model_name, version=version, artifact_uri=artifact_uri
        )
        session.add(mv)
        session.commit()
        session.refresh(mv)  # re-load expired attributes while attached
        return mv


def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. Declared metadata matches the created table
    assert set(inspect(engine).get_table_names()) == {
        "experiments",
        "training_steps",
        "model_versions",
    }, "metadata must create exactly the declared tables"

    # 2. Mapped columns carry the right nullability (Optional -> NULL)
    assert inspect(engine).get_columns("experiments")[3]["name"] == "notes"
    notes_col = [c for c in inspect(engine).get_columns("experiments")
                 if c["name"] == "notes"][0]
    assert notes_col["nullable"] is True, "Optional[...] columns must be nullable"

    # 3. UNIQUE constraint fires on duplicate name
    try:
        with _fresh_session() as session:
            session.add(Experiment(name="run-1", model="x", score=0.5))
            session.commit()
        raise AssertionError("duplicate name must raise IntegrityError")
    except IntegrityError:
        pass

    # 4. NOT NULL constraint fires on missing required column
    try:
        with _fresh_session() as session:
            session.add(Experiment(name="run-x", score=0.5))  # no model
            session.commit()
        raise AssertionError("missing model must raise IntegrityError")
    except IntegrityError:
        pass

    # 5. CHECK constraint fires on out-of-range score
    try:
        with _fresh_session() as session:
            session.add(Experiment(name="run-y", model="m", score=-1.0))
            session.commit()
        raise AssertionError("negative score must raise IntegrityError")
    except IntegrityError:
        pass

    # 6. Composite unique constraint permits repeats of a single column
    with _fresh_session() as session:
        session.add(TrainingStep(experiment_id=1, step=5, loss=0.2))
        session.commit()

    # 7. Production pattern works end to end
    mv = register_version("bert", 1, "s3://models/bert/v1")
    assert mv.version == 1 and mv.model_name == "bert", "register must persist"
    try:
        register_version("bert", 1, "s3://models/bert/v1-dupe")
        raise AssertionError("duplicate (model_name, version) must fail")
    except IntegrityError:
        pass

    print("[OK] 02-declarative-models: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. DeclarativeBase + Mapped[...] = typed, self-documenting schema")
        print("2. Constraints live in the DB; IntegrityError is the DB saying no")
        print("3. __table_args__ = multi-column unique + composite indexes")
        _verify()  # always runs, so plain execution is also a test
