"""
04-databases/sqlalchemy — 09: Testing with a Database
=======================================================
Topics: transactional rollback fixtures; per-test schema;
        factories; testcontainers; sqlite-vs-Postgres divergence.

Why this matters for AI/backend engineering:
    Tests that touch the DB are where ML backends rot: state leaks
    between tests, the schema drifts from the models, and CI runs
    against sqlite while production runs Postgres. This exercise
    shows the three load-bearing patterns — transactional rollback
    fixtures (zero cleanup code), per-test schema (no shared state),
    and factories (no fixture spaghetti) — and then demonstrates
    honestly where sqlite and Postgres DIVERGE so you know exactly
    which bugs sqlite tests cannot catch.

Run:      python 09-testing-with-db.py
Verify:   python 09-testing-with-db.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/session_transaction.html
"""

from __future__ import annotations

import sys

from sqlalchemy import JSON, String, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.pool import StaticPool

# ============================================================
# 0. Engine + model under test
# ============================================================
# Every test in this file gets a FRESH engine (per-test schema).
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    score: Mapped[float] = mapped_column(default=0.0)
    config: Mapped[dict] = mapped_column(JSON, default=dict)


Base.metadata.create_all(engine)  # module-level schema for the demos below


# ============================================================
# 1. Transactional rollback fixture (the workhorse pattern)
# ============================================================
# The session is bound to a CONNECTION that holds an outer
# transaction; the session joins it via SAVEPOINTs. When the
# test ends we roll the whole outer transaction back — every
# INSERT/UPSERT the test made vanishes WITHOUT any cleanup code.
# This is the pattern pytest plugins and FastAPI test clients use.

def make_engine() -> object:
    """Create a brand-new in-memory engine with the schema applied."""
    eng = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(eng)
    return eng


def transactional_session(eng):
    """Yield a session whose writes roll back when the generator ends.

    Usage (inside pytest):
        def test_something(eng=fixture_engine):
            gen = transactional_session(eng)
            session = next(gen)
            try:
                ... assert ...
            finally:
                gen.close()   # <- rolls back everything
    """
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


def commit_session(eng) -> Session:
    """Plain committed session (for tests that must persist)."""
    return Session(bind=eng)


# ============================================================
# 2. Simulated test run: isolation between tests
# ============================================================
# Two "tests" run against the SAME engine. The first writes rows
# inside a rollback fixture; the second sees NONE of them. This is
# the guarantee that makes DB tests parallelizable and repeatable.

def simulate_rollback_isolation(eng) -> tuple[int, int]:
    """Run two fake tests; return (rows_test1_saw, rows_test2_saw)."""
    # "test 1": insert two rows, expect them visible DURING the test
    gen = transactional_session(eng)
    session = next(gen)
    session.add_all(
        [
            Experiment(name="t1-a", score=0.9),
            Experiment(name="t1-b", score=0.8),
        ]
    )
    session.flush()
    visible_in_test1 = len(session.scalars(select(Experiment)).all())
    gen.close()  # rollback: rows disappear

    # "test 2": fresh session, must start EMPTY
    with commit_session(eng) as session2:
        visible_in_test2 = len(session2.scalars(select(Experiment)).all())
    return visible_in_test1, visible_in_test2


# ============================================================
# 3. Factories: object builders with sane defaults
# ============================================================
# A factory centralizes "a valid row" so tests express only what
# they care about. Counter-based names keep them unique without
# wall-clock or random sources.

_factory_counter = [0]


def make_experiment(name: str | None = None, **overrides) -> Experiment:
    """Build an Experiment with unique default name; merge overrides.

    config is set explicitly because column defaults apply at FLUSH
    time, not construction time — a factory must produce rows that
    are complete before they touch a session.
    """
    _factory_counter[0] += 1
    defaults = {
        "name": name or f"factory-{_factory_counter[0]}",
        "score": 0.5,
        "config": {},
    }
    defaults.update(overrides)
    return Experiment(**defaults)


# ============================================================
# 4. Per-test schema: drop + create for absolute isolation
# ============================================================
# Rollback fixtures are fast but cannot undo DDL. When tests
# exercise schema behavior (constraints, indexes, migrations),
# create_all/drop_all per test is the honest answer.

def reset_schema(eng) -> None:
    """Drop and recreate every table — per-test schema isolation."""
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)


# ============================================================
# 5. testcontainers: real Postgres in CI (the honest option)
# ============================================================
# When the test needs Postgres semantics (JSONB, enums, FTS),
# sqlite cannot substitute. testcontainers spins a disposable
# Postgres inside Docker for the test run:
#
#   from testcontainers.postgres import PostgresContainer
#   with PostgresContainer("postgres:16") as pg:
#       eng = create_engine(pg.get_connection_url())
#       ... run the suite against REAL Postgres ...
#
# Not executed here: it needs Docker. The engine API is identical,
# which is exactly the point — swap sqlite for Postgres by changing
# the URL, and the tests keep working.

# ============================================================
# 6. sqlite-vs-Postgres divergence (measured, not imagined)
# ============================================================
# sqlite tests are fast and free; they are NOT equivalent. Three
# concrete divergences, demonstrated:

# 6a. VARCHAR length: sqlite IGNORES String(10) — a 200-char value
#     inserts fine. Postgres raises "value too long for type
#     character varying(10)". Length bugs pass sqlite CI.
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO experiments (name, score, config) VALUES (:n, :s, :c)"),
        {"n": "x" * 200, "s": 0.1, "c": "{}"},
    )
    conn.commit()
    conn.execute(text("DELETE FROM experiments WHERE name LIKE 'x%'"))
    conn.commit()
print("sqlite accepts 200 chars into String(10) -> True")

# 6b. JSON: sqlite stores the JSON column as TEXT without
#     validation; Postgres JSONB validates structure and supports
#     containment queries (@>). The same code runs on both, but
#     what the database DOES with it differs.
with Session(bind=engine) as session:
    session.add(Experiment(name="json-demo", config={"lr": 1e-4}))
    session.commit()
    raw = session.execute(
        text("SELECT config FROM experiments WHERE name = 'json-demo'")
    ).scalar_one()
    print(f"sqlite JSON stored as: {type(raw).__name__} (no @> operator)")

# Output:
# sqlite accepts 200 chars into String(10) -> True
# sqlite JSON stored as: str (no @> operator)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: cleanup via DELETE in teardown.
#   def teardown(): session.execute(delete(Experiment))
# CORRECT: transactional rollback — no cleanup code at all.
#
# MISTAKE: sharing one engine+session across the whole suite and
#          hoping tests don't collide.
# CORRECT: fresh engine per test (per-test schema) or rollback
#          fixtures per test.
#
# MISTAKE: believing sqlite tests prove Postgres behavior.
#   # sqlite: String(10) accepts 200 chars; no JSONB; no enums
# CORRECT: run a Postgres smoke layer (testcontainers) for the
#          features sqlite cannot model.


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    eng = make_engine()

    # 1. Rollback fixture: rows visible DURING the test, gone after
    seen1, seen2 = simulate_rollback_isolation(eng)
    assert seen1 == 2, "rows must be visible inside the test transaction"
    assert seen2 == 0, "rollback fixture must leave zero trace"

    # 2. Committed writes DO persist across sessions
    with commit_session(eng) as session:
        session.add(Experiment(name="persisted", score=0.7))
        session.commit()
    with commit_session(eng) as session:
        assert session.scalars(
            select(Experiment).where(Experiment.name == "persisted")
        ).first() is not None, "committed writes must survive"

    # 3. Factory produces unique, override-aware rows
    a = make_experiment()
    b = make_experiment()
    assert a.name != b.name, "factory must generate unique names"
    c = make_experiment(score=0.99)
    assert c.score == 0.99 and c.config == {}, "overrides must merge"

    # 4. Per-test schema reset gives a clean slate (DDL isolation)
    with commit_session(eng) as session:
        session.add(Experiment(name="pre-reset", score=0.1))
        session.commit()
    reset_schema(eng)
    with commit_session(eng) as session:
        rows = session.scalars(select(Experiment)).all()
        assert rows == [], "drop_all/create_all must wipe all data"

    # 5. sqlite divergence: String(10) accepts oversized values
    with commit_session(eng) as session:
        session.add(Experiment(name="big" * 30, score=0.1))  # 90 chars
        session.commit()
        saved = session.scalars(select(Experiment)).all()
        assert len(saved) == 1, "sqlite must store the oversized name"

    # 6. sqlite divergence: JSON columns come back as TEXT, and the
    #    JSONB containment operator does not exist on this dialect
    with commit_session(eng) as session:
        session.add(Experiment(name="cfg", config={"lr": 0.001}))
        session.commit()
        raw = session.execute(
            text("SELECT config FROM experiments WHERE name = 'cfg'")
        ).scalar_one()
        assert isinstance(raw, str), "sqlite JSON must be stored as text"
        try:
            session.execute(
                text("SELECT config @> '{\"lr\": 0.001}' FROM experiments")
            )
            jsonb_works = True
        except Exception:
            jsonb_works = False
        assert jsonb_works is False, \
            "sqlite must NOT support the Postgres JSONB containment operator"

    # 7. Transactions: rollback inside a session undoes flushes
    with Session(bind=eng) as session:
        session.add(Experiment(name="ghost-row", score=0.0))
        session.flush()
        session.rollback()
    with commit_session(eng) as session:
        ghosts = session.scalars(
            select(Experiment).where(Experiment.name == "ghost-row")
        ).all()
        assert ghosts == [], "session rollback must undo flushed rows"

    print("[OK] 09-testing-with-db: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Rollback fixtures kill cleanup code; per-test schema kills state")
        print("2. Factories keep tests expressive; testcontainers bring real PG")
        print("3. sqlite divergence: length ignored, JSON is text, no JSONB @>")
        _verify()  # always runs, so plain execution is also a test
