"""
Challenge 01: Core vs ORM — Reference Solution
================================================
Why this approach: Core is the right layer for bulk loads — no
unit-of-work bookkeeping, one INSERT per call. Batches bound the
statement size so the loader scales past the parameter limit.
"""

from __future__ import annotations

from sqlalchemy import Column, Float, Integer, MetaData, String, Table, text


metrics_table = Table(
    "metrics",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("model", String(50), nullable=False),
    Column("metric", String(50), nullable=False),
    Column("value", Float, nullable=False),
)


def bulk_insert_metrics(conn, rows: list[dict]) -> int:
    """Bulk-insert metric rows via Core; return rows written."""
    if not rows:
        return 0
    conn.execute(metrics_table.insert(), rows)
    return len(rows)


def query_above(conn, threshold: float) -> list[tuple[int, str, float]]:
    """Return (id, metric, value) for rows with value > threshold.

    text() + bound parameter: the DB filters, Python only consumes.
    """
    stmt = text(
        "SELECT id, metric, value FROM metrics "
        "WHERE value > :threshold ORDER BY value DESC"
    )
    return [(row[0], row[1], row[2]) for row in conn.execute(stmt, {"threshold": threshold})]


def safe_upsert_metrics(conn, rows: list[dict], batch_size: int = 500) -> int:
    """Insert rows in committed batches of batch_size; return total written.

    Single pass over rows: each batch is inserted and committed before
    the next is built, so memory stays O(batch_size) regardless of the
    input length.
    """
    total = 0
    for start in range(0, len(rows), batch_size):
        batch = rows[start : start + batch_size]
        conn.execute(metrics_table.insert(), batch)
        conn.commit()
        total += len(batch)
    return total
