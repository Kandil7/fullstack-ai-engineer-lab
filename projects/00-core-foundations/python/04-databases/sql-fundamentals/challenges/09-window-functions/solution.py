"""
Challenge 09: window-functions — Reference Solution
====================================================
"""

import sqlite3


def _ensure_runs(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS runs ("
        "id INTEGER PRIMARY KEY, model TEXT, run_ts INT, metric REAL)")


def rank_rows(conn: sqlite3.Connection) -> list[tuple]:
    """ROW_NUMBER, RANK, DENSE_RANK over metric DESC per model."""
    _ensure_runs(conn)
    return [tuple(r) for r in conn.execute(
        "SELECT model, metric, "
        "ROW_NUMBER() OVER (PARTITION BY model ORDER BY metric DESC) AS rn, "
        "RANK() OVER (PARTITION BY model ORDER BY metric DESC) AS r, "
        "DENSE_RANK() OVER (PARTITION BY model ORDER BY metric DESC) AS d "
        "FROM runs ORDER BY model, rn")]


def lag_delta(conn: sqlite3.Connection) -> list[tuple]:
    """Delta vs previous run of the same model."""
    _ensure_runs(conn)
    return [tuple(r) for r in conn.execute(
        "SELECT model, run_ts, metric, "
        "metric - LAG(metric, 1) OVER (PARTITION BY model ORDER BY run_ts) "
        "FROM runs ORDER BY model, run_ts")]


def frames_report(conn: sqlite3.Connection) -> list[tuple]:
    """Running total and 3-row moving average per model."""
    _ensure_runs(conn)
    return [tuple(r) for r in conn.execute(
        "SELECT model, run_ts, metric, "
        "SUM(metric) OVER (PARTITION BY model ORDER BY run_ts "
        "  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total, "
        "AVG(metric) OVER (PARTITION BY model ORDER BY run_ts "
        "  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg "
        "FROM runs ORDER BY model, run_ts")]
