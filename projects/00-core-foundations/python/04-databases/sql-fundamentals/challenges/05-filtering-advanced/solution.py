"""
Challenge 05: filtering-advanced — Reference Solution
======================================================
"""

import sqlite3


def _ensure_models(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS models ("
        "id INTEGER PRIMARY KEY, name TEXT, epoch INT, metric REAL)")


def filter_range(conn: sqlite3.Connection, lo: float, hi: float) -> list[str]:
    """Inclusive range via AND, sorted by name."""
    _ensure_models(conn)
    return [r[0] for r in conn.execute(
        "SELECT name FROM models WHERE metric >= ? AND metric <= ? "
        "ORDER BY name", (lo, hi))]


def pattern_match(conn: sqlite3.Connection, pattern: str) -> dict:
    """SQL LIKE semantics; % any run, _ exactly one char."""
    _ensure_models(conn)
    names = [r[0] for r in conn.execute(
        "SELECT name FROM models WHERE name LIKE ? ORDER BY name", (pattern,))]
    # % and _ are wildcards; ESCAPE '\' makes '_' a literal underscore
    single = conn.execute(
        "SELECT COUNT(*) FROM models WHERE name LIKE '%\\_%' ESCAPE '\\'"
    ).fetchone()[0]
    return {"names": names, "single_underscore": single}


def null_aware_report(conn: sqlite3.Connection) -> dict:
    """CASE buckets + EXISTS run membership."""
    _ensure_models(conn)
    conn.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, model_id INTEGER)")

    buckets = {"ok": 0, "missing": 0}
    for row in conn.execute(
        "SELECT CASE WHEN metric IS NULL THEN 'missing' ELSE 'ok' END AS b, "
        "COUNT(*) FROM models GROUP BY b"):
        buckets[row[0]] = row[1]

    with_runs = [r[0] for r in conn.execute(
        "SELECT name FROM models m WHERE EXISTS "
        "(SELECT 1 FROM runs r WHERE r.model_id = m.id) ORDER BY name")]
    return {"buckets": buckets, "with_runs": with_runs}
