"""
Challenge 06: aggregation — Reference Solution
===============================================
"""

import sqlite3


def _ensure_runs(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS runs ("
        "id INTEGER PRIMARY KEY, model TEXT, experiment TEXT, metric REAL)")


def group_totals(conn: sqlite3.Connection) -> list[tuple]:
    """Per-model COUNT/SUM/AVG, ordered by avg DESC."""
    _ensure_runs(conn)
    return [tuple(r) for r in conn.execute(
        "SELECT model, COUNT(*) AS runs, SUM(metric) AS total, AVG(metric) AS avg "
        "FROM runs GROUP BY model ORDER BY avg DESC")]


def having_filter(conn: sqlite3.Connection, min_runs: int, min_avg: float) -> list[tuple]:
    """HAVING-only conditions on aggregates."""
    _ensure_runs(conn)
    return [tuple(r) for r in conn.execute(
        "SELECT model, COUNT(*) AS runs, AVG(metric) AS avg "
        "FROM runs GROUP BY model "
        "HAVING COUNT(*) >= ? AND AVG(metric) >= ? "
        "ORDER BY avg DESC", (min_runs, min_avg))]


def aggregate_report(conn: sqlite3.Connection) -> dict:
    """WHERE pre-filter + per-model aggregates + global scalar subquery."""
    _ensure_runs(conn)
    rows = [tuple(r) for r in conn.execute(
        "SELECT model, COUNT(DISTINCT experiment) AS experiments, "
        "COUNT(*) AS runs, MAX(metric) AS best "
        "FROM runs WHERE metric >= 0.5 "
        "GROUP BY model ORDER BY best DESC")]
    global_avg = conn.execute(
        "SELECT AVG(metric) FROM runs WHERE metric >= 0.5").fetchone()[0]
    return {"rows": rows, "global_avg": global_avg}
