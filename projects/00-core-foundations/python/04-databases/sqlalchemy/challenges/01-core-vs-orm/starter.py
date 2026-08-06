"""
Challenge 01: Core vs ORM — Starter Code
==========================================
Fill in the function bodies. Do not modify signatures.
The metrics table is created for you; use it via Core only.
"""

from __future__ import annotations

from sqlalchemy import Column, Float, Integer, MetaData, String, Table


metrics_table = Table(
    "metrics",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("model", String(50), nullable=False),
    Column("metric", String(50), nullable=False),
    Column("value", Float, nullable=False),
)


def bulk_insert_metrics(conn, rows: list[dict]) -> int:
    """Bulk-insert metric rows via Core; return rows written.

    Use metrics_table.insert(). Do not commit.
    """
    raise NotImplementedError


def query_above(conn, threshold: float) -> list[tuple[int, str, float]]:
    """Return (id, metric, value) for rows with value > threshold.

    Must use text() with a bound parameter, ordered by value DESC.
    """
    raise NotImplementedError


def safe_upsert_metrics(conn, rows: list[dict], batch_size: int = 500) -> int:
    """Insert rows in committed batches of batch_size; return total written."""
    raise NotImplementedError
