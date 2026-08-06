"""
04-databases/sqlalchemy — 01: Core vs ORM
==============================================
Topics: two layers (Core vs ORM); text(); when Core beats ORM;
        Engine and dialects.

Why this matters for AI/backend engineering:
    Every AI service (model registry, prompt store, eval results, training
    metadata) reads and writes through a data-access layer. SQLAlchemy's
    Core layer is the SQL-first foundation: you use it directly for
    bulk loads, ad-hoc analytics, and migrations; the ORM layer (topics
    02-06) is what your services use for CRUD. Knowing which layer to
    reach for is the difference between 10-line and 100-line solutions.

Run:      python 01-core-vs-orm.py
Verify:   python 01-core-vs-orm.py --verify
Reference: https://docs.sqlalchemy.org/en/20/core/
"""

from __future__ import annotations

import sys
from typing import Any

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    select,
    text,
)

# ============================================================
# 1. Two Layers: Core and ORM
# ============================================================
# SQLAlchemy has two distinct APIs:
#   - Core: schema objects (Table/MetaData) + SQL expression language +
#     Connection. You write SQL-shaped expressions; the engine compiles
#     them to dialect-specific SQL.
#   - ORM: maps Python classes to tables, then adds a Session on top.
# The ORM is *built on* Core, so everything here is also what the ORM
# emits under the hood.
# Complexity: compilation is O(1) per statement; result iteration O(rows).

engine = create_engine("sqlite://")  # in-memory database
# NOTE: plain "sqlite://" creates a NEW in-memory DB per connection unless
# we pin a single pooled connection. For a single connection it is fine.

# Example 1: Core metadata defines a table without any Python class
meta = MetaData()
widgets = Table(
    "widgets",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("qty", Integer, nullable=False, default=0),
)
meta.create_all(engine)

# Example 2: Core insert via a Connection
with engine.connect() as conn:
    conn.execute(
        widgets.insert(),
        [{"name": "bolt", "qty": 12}, {"name": "nut", "qty": 300}],
    )
    conn.commit()  # Core connections do NOT auto-commit

# Example 3: Core select — rows come back as tuples / Row objects
with engine.connect() as conn:
    rows = conn.execute(select(widgets.c.name, widgets.c.qty)).all()
    for row in rows:
        print(f"row: {row.name} x{row.qty}")

# Output:
# row: bolt x12
# row: nut x300

# ============================================================
# 2. text(): Raw SQL when the expression language is overkill
# ============================================================
# text() wraps a raw SQL string. It is the escape hatch for SQL that is
# awkward to express (window functions, CTEs, dialect-specific features).
# ALWAYS bind parameters with :name — never f-string values.

# Example 4: parameterized raw SQL; :qty is a bound parameter
with engine.connect() as conn:
    rows = conn.execute(
        text("SELECT name, qty FROM widgets WHERE qty > :qty ORDER BY qty"),
        {"qty": 50},
    ).all()
    for row in rows:
        print(f"big stock: {row[0]} = {row[1]}")

# Output:
# big stock: nut = 300

# ============================================================
# 3. When Core beats the ORM
# ============================================================
# Core is the right tool when:
#   1. Bulk loads (insertmanyvalues) — no unit-of-work bookkeeping.
#   2. Ad-hoc analytics / reporting — pure SQL with no object mapping.
#   3. Migrations, ETL, and anything where "rows in, rows out" is enough.
# The ORM wins when you have object graphs, identity, and cascades.

# Example 5: bulk insert of 10_000 rows in one statement
BULK_N = 10_000
with engine.connect() as conn:
    conn.execute(
        widgets.insert(),
        [{"name": f"part-{i}", "qty": i} for i in range(BULK_N)],
    )
    conn.commit()

with engine.connect() as conn:
    total = conn.execute(select(widgets.c.qty).where(widgets.c.name.like("part-%"))).all()
    print(f"bulk inserted rows returned: {len(total)}")

# Output:
# bulk inserted rows returned: 10000

# ============================================================
# 4. Engine and dialects
# ============================================================
# The Engine is the factory for Connections; it owns the pool and the
# dialect. The dialect is the per-database compiler: "sqlite://" selects
# the sqlite dialect, "postgresql+psycopg://" the Postgres one. Same
# Core code compiles to different SQL per dialect — that is the point.
# sqlite-vs-Postgres divergence (honesty note): bound-parameter styles
# differ (':' in SQLAlchemy text() both places), and some types
# (JSONB, arrays) exist only on Postgres. See topic 08.

# Example 6: what the dialect says about the backend
print(f"dialect name: {engine.dialect.name}")
print(f"driver name:  {engine.dialect.driver}")

# Output:
# dialect name: sqlite
# driver name:  pysqlite

# Example 7: engine connect round-trip — SELECT 1 proves the pipe works
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1")).scalar_one()
    print(f"round-trip SELECT 1 -> {result}")

# Output:
# round-trip SELECT 1 -> 1

# ============================================================
# 5. Production Pattern: a tiny metrics loader
# ============================================================
# Real pattern from ML observability: nightly job bulk-loads eval metrics
# with Core, then analytics read them with plain selects. No ORM objects
# needed for a load-then-query pipeline — object overhead buys nothing.

def load_metrics(rows: list[dict[str, Any]]) -> int:
    """Bulk-insert metric rows, returning how many were written.

    Chosen over the ORM because unit-of-work tracking is pure overhead
    for a batch load: we want one INSERT statement for all rows.
    """
    with engine.connect() as conn:
        conn.execute(metrics.insert(), rows)
        conn.commit()
    return len(rows)


metrics = Table(
    "metrics",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("model", String(50), nullable=False),
    Column("metric", String(50), nullable=False),
    Column("value", Integer, nullable=False),
)
metrics.metadata.create_all(engine)


def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    with engine.connect() as conn:
        # 1. text() query returns correct rows (Core layer works)
        rows = conn.execute(
            text("SELECT name FROM widgets WHERE name = :name"),
            {"name": "bolt"},
        ).all()
        assert [r[0] for r in rows] == ["bolt"], "text() bound params must filter"

        # 2. Core select expression compiles and matches expected names
        names = conn.execute(
            select(widgets.c.name)
            .where(widgets.c.name.in_(["part-0", "part-1"]))
            .order_by(widgets.c.qty.desc())
        ).scalars().all()
        assert names == ["part-1", "part-0"], "Core select must order and filter"

        # 3. Bulk load actually inserted all rows
        count = conn.execute(
            select(widgets.c.id).where(widgets.c.name.like("part-%"))
        ).all()
        assert len(count) == BULK_N, "bulk insert must write every row"

        # 4. engine connect round-trip works (Connection is alive)
        assert conn.execute(text("SELECT 42")).scalar_one() == 42, \
            "round-trip SELECT must return the constant"

    # 5. Production pattern: load_metrics returns row count and rows land
    written = load_metrics(
        [
            {"model": "bert", "metric": "f1", "value": 89},
            {"model": "bert", "metric": "latency", "value": 12},
        ]
    )
    assert written == 2, "load_metrics must report rows written"
    with engine.connect() as conn:
        assert conn.execute(
            text("SELECT COUNT(*) FROM metrics")
        ).scalar_one() == 2, "metrics must be persisted"
        assert conn.execute(
            text("SELECT value FROM metrics WHERE metric = 'f1'")
        ).scalar_one() == 89, "metrics values must round-trip"

    print("[OK] 01-core-vs-orm: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Core = schema + SQL expressions + Connection; ORM builds on it")
        print("2. text() is the raw-SQL escape hatch; always bind parameters")
        print("3. Core beats ORM for bulk loads and analytics; ORM for object graphs")
        _verify()  # always runs, so plain execution is also a test
