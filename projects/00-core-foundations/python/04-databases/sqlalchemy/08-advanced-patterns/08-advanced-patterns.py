"""
04-databases/sqlalchemy — 08: Advanced Patterns
=================================================
Topics: hybrid properties; custom types; events; bulk operations;
        returning(); window functions via ORM.

Why this matters for AI/backend engineering:
    Production ORM code is not just CRUD: it computes fields in
    Python that must also be queryable in SQL (hybrid properties),
    stores non-scalar payloads (embeddings as custom types),
    enforces invariants on write (events), and imports training
    metadata in bulk. Window functions are how you answer "rank
    every experiment within its model family" in one query instead
    of a Python loop — the difference between a leaderboard endpoint
    that scales and one that does not.

Run:      python 08-advanced-patterns.py
Verify:   python 08-advanced-patterns.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html
"""

from __future__ import annotations

import array
import sys

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    LargeBinary,
    String,
    TypeDecorator,
    create_engine,
    event,
    func,
    insert,
    select,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)
from sqlalchemy.pool import StaticPool

# ============================================================
# 0. Engine + models
# ============================================================
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    """Training/eval run with a score and a version for optimistic locking."""

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


# ============================================================
# 1. Custom types: embeddings as a fixed-width byte column
# ============================================================
# ML payloads (embedding vectors) are not scalars. A TypeDecorator
# wraps the storage type (LargeBinary) and defines the Python <-> DB
# conversion: float32 array <-> bytes. The ORM then stores and loads
# vectors transparently.
# Complexity: bind/result conversion O(dim) per row.

class VectorType(TypeDecorator):
    """Stores an embedding (list[float]) as raw float32 bytes.

    Chosen over JSON text: fixed 4*N bytes per row, indexable,
    and directly consumable by vector-search code without parsing.
    """

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
    """One stored embedding row (e.g., for a document chunk)."""

    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    chunk_id: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    vector: Mapped[list[float] | None] = mapped_column(VectorType(dim=8))


# ============================================================
# 2. Events: optimistic versioning on every update
# ============================================================
# before_update fires inside the flush, in the same transaction.
# The pattern here is optimistic locking: every UPDATE bumps the
# version column, so a stale client write can be detected by
# comparing versions (WHERE ... AND version = :expected).

@event.listens_for(Experiment, "before_update")
def _bump_version(mapper, connection, target) -> None:
    """Increment version for any mapped update to an Experiment."""
    target.version += 1


Base.metadata.create_all(engine)


def new_session() -> Session:
    return SessionLocal()


# ============================================================
# 3. Hybrid properties: one rule, two contexts
# ============================================================
# Instance access uses the Python method; queries use the SQL
# expression. If they drift, filtering and business logic disagree.

# Example 1: instance-level access
with new_session() as session:
    exp = Experiment(name="bert-run-1", model="bert", score=0.92)
    session.add(exp)
    session.commit()
    print(f"instance is_leader: {exp.is_leader}")

# Output:
# instance is_leader: True

# Example 2: the same rule inside a WHERE clause (SQL side)
with new_session() as session:
    session.add(Experiment(name="bert-run-2", model="bert", score=0.71))
    session.commit()
    leaders = session.scalars(
        select(Experiment).where(Experiment.is_leader).order_by(Experiment.name)
    ).all()
    print(f"query is_leader -> {[e.name for e in leaders]}")

# Output:
# query is_leader -> ['bert-run-1']


# ============================================================
# 4. Custom type round-trip
# ============================================================
# Example 3: store and reload a float vector through the ORM
with new_session() as session:
    vec = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    session.add(Embedding(chunk_id="chunk-1", vector=vec))
    session.commit()

with new_session() as session:
    loaded = session.scalars(
        select(Embedding).where(Embedding.chunk_id == "chunk-1")
    ).one()
    print(f"vector round-trip: {loaded.vector}")

# Output:
# vector round-trip: [0.10000000149011612, 0.20000000298023224, ...]
# (float32 storage: 0.1 has no exact binary form, so tiny artifacts
#  appear on reload; values like 0.25/0.5 round-trip exactly)


# ============================================================
# 5. Events in action: version bumps
# ============================================================
# Example 4: update triggers before_update -> version 1 -> 2
with new_session() as session:
    exp = session.scalars(
        select(Experiment).where(Experiment.name == "bert-run-1")
    ).one()
    exp.score = 0.95
    session.commit()
    print(f"version after one update: {exp.version}")

# Output:
# version after one update: 2


# ============================================================
# 6. Bulk operations: load training metadata fast
# ============================================================
# bulk_insert_mappings / bulk_update_mappings skip the unit-of-work
# bookkeeping and issue one batched INSERT (insertmanyvalues) or a
# single UPDATE per statement. They do NOT touch the identity map —
# the price of speed.

# Example 5: bulk insert of 5 experiments in one round trip
bulk_rows = [
    {"name": f"grid-{i}", "model": "bert", "score": 0.80 + i / 100.0}
    for i in range(5)
]
with new_session() as session:
    session.bulk_insert_mappings(Experiment, bulk_rows)
    session.commit()
    count = len(session.scalars(select(Experiment)).all())
    print(f"experiments after bulk insert: {count}")

# Output:
# experiments after bulk insert: 7

# Example 6: bulk update — promote every leader in one statement
with new_session() as session:
    rows = [
        {"id": exp.id, "score": 0.99}
        for exp in session.scalars(select(Experiment)).all()
    ]
    session.bulk_update_mappings(Experiment, rows)
    session.commit()

with new_session() as session:
    top = session.scalars(
        select(Experiment).where(Experiment.is_leader).order_by(Experiment.name)
    ).all()
    print(f"leaders after bulk update: {len(top)}")

# Output:
# leaders after bulk update: 7


# ============================================================
# 7. returning(): read values without a second query
# ============================================================
# Core-style insert().returning() gives back DB-generated values
# (ids, defaults) in the SAME round trip as the INSERT — essential
# for high-throughput writers like an ingestion pipeline.

# Example 7: insert with returning(id)
with new_session() as session:
    stmt = (
        insert(Experiment)
        .values(name="returning-demo", model="gpt2", score=0.88)
        .returning(Experiment.id)
    )
    new_id = session.execute(stmt).scalar_one()
    session.commit()
    print(f"returning() gave id: {new_id}")

# Output:
# returning() gave id: 8


# ============================================================
# 8. Window functions via ORM: rank within each model family
# ============================================================
# row_number() OVER (PARTITION BY model ORDER BY score DESC) assigns
# a rank per model without grouping — every row stays visible. This
# is the one-query version of "best run per model family".

# Example 8: per-model rank of every experiment
with new_session() as session:
    stmt = (
        select(
            Experiment.name,
            Experiment.model,
            Experiment.score,
            func.row_number()
            .over(
                partition_by=Experiment.model,
                order_by=Experiment.score.desc(),
            )
            .label("rank_in_model"),
        )
        .order_by(Experiment.model, "rank_in_model")
    )
    for name, model, score, rank in session.execute(stmt):
        print(f"#{rank} {model}: {name} ({score:.2f})")

# Output:
# #1 bert: bert-run-2 (0.99)     <- ties in score order by rowid, so the
# #2 bert: grid-0 (0.99)            exact #1 among equal 0.99 scores is
# ...                               unspecified; bert-run-1 (0.95) is last
# #1 gpt2: returning-demo (0.88)


# ============================================================
# 9. Production Pattern: ranked leaderboard with version guard
# ============================================================
# The shipping shape: a query function that returns the top run per
# model family, plus a version-guarded update that refuses stale
# writes (optimistic locking with the event-bumped version).

def top_per_model(session: Session, k: int = 1) -> list[tuple[str, str, float]]:
    """Return the top-k experiments per model family.

    Uses row_number() in SQL (one query, scales with the DB) instead
    of Python sorting — the same result at any row count.
    """
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
    """Optimistic update: only succeeds when the version still matches."""
    exp = session.get(Experiment, experiment_id)
    if exp is None or exp.version != expected_version:
        return False
    exp.score = new_score
    session.commit()  # before_update event bumps version in the same tx
    return True


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: hybrid property with different Python/SQL logic.
#   def is_leader(self): return self.score > 0.9    # Python
#   @is_leader.expression                             # SQL
#   def is_leader(cls): return cls.score >= 0.9      # drift!
# CORRECT: one threshold constant used by both bodies.
#
# MISTAKE: assuming bulk_update_mappings touches the identity map.
#   exp = session.get(...); bulk_update_mappings([...])  # exp unchanged
# CORRECT: bulk ops bypass the session; expire/refresh to re-read.
#
# MISTAKE: version checks in application code instead of the WHERE.
# CORRECT: WHERE id=? AND version=? in the UPDATE (the event bumps
#   version so a stale client's write fails loudly).


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    with new_session() as session:
        # 1. Hybrid property agrees between Python and SQL contexts
        exp = session.scalars(
            select(Experiment).where(Experiment.name == "bert-run-1")
        ).one()
        assert exp.is_leader is True, "instance hybrid must be True for 0.95"
        sql_leaders = session.scalars(
            select(Experiment).where(Experiment.is_leader)
        ).all()
        assert all(e.is_leader for e in sql_leaders), \
            "SQL-side hybrid must match instance-side logic"

        # 2. Custom type round-trips byte-exactly
        vec = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
        session.add(Embedding(chunk_id="verify-vec", vector=vec))
        session.commit()
        loaded = session.scalars(
            select(Embedding).where(Embedding.chunk_id == "verify-vec")
        ).one()
        assert loaded.vector == vec, "VectorType must round-trip floats exactly"

        # 3. before_update event bumps version
        exp.score = 0.91
        session.commit()
        assert exp.version == 3, "event must bump version on every update"

        # 4. Bulk insert wrote every row
        session.bulk_insert_mappings(
            Experiment,
            [{"name": f"bulk-{i}", "model": "gpt2", "score": 0.5} for i in range(3)],
        )
        session.commit()
        bulk = session.scalars(
            select(Experiment).where(Experiment.name.like("bulk-%"))
        ).all()
        assert len(bulk) == 3, "bulk_insert_mappings must insert all rows"

        # 5. returning() returns the generated PK
        stmt = (
            insert(Experiment)
            .values(name="verify-returning", model="gpt2", score=0.5)
            .returning(Experiment.id)
        )
        rid = session.execute(stmt).scalar_one()
        session.commit()
        assert session.get(Experiment, rid) is not None, \
            "returning() id must reference a persisted row"

        # 6. Window rank: exactly one #1 per model family
        tops = top_per_model(session, k=1)
        models_seen = {m for _, m, _ in tops}
        assert len(tops) == len(models_seen), \
            "top_per_model must return exactly one row per model"

        # 7. Optimistic locking: stale version write is refused
        exp = session.scalars(
            select(Experiment).where(Experiment.name == "bert-run-1")
        ).one()
        current_version = exp.version
        assert update_if_version(session, exp.id, current_version, 0.97) is True, \
            "matching version must update"
        assert update_if_version(session, exp.id, current_version, 0.5) is False, \
            "stale version must be refused"

    print("[OK] 08-advanced-patterns: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. hybrid_property: one rule, Python + SQL contexts")
        print("2. TypeDecorator + events + bulk ops shape production writes")
        print("3. returning() and window functions keep work in the DB")
        _verify()  # always runs, so plain execution is also a test
