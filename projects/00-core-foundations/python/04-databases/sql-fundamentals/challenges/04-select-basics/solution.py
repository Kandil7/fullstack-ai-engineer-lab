"""
Challenge 04: select-basics — Reference Solution
=================================================
"""

import sqlite3


def _ensure_models(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS models ("
        "id INTEGER PRIMARY KEY, name TEXT, epoch INT, metric REAL)")


def top_n(conn: sqlite3.Connection, n: int) -> list[tuple]:
    """Top-n by metric DESC then name ASC, via SQL LIMIT."""
    _ensure_models(conn)
    return [tuple(r) for r in conn.execute(
        "SELECT name, metric FROM models ORDER BY metric DESC, name ASC LIMIT ?",
        (n,))]


def metric_report(conn: sqlite3.Connection) -> dict:
    """Aliased expression + DISTINCT count."""
    _ensure_models(conn)
    report = [tuple(r) for r in conn.execute(
        "SELECT DISTINCT name, metric * 100 AS score "
        "FROM models ORDER BY score DESC")]
    distinct = conn.execute(
        "SELECT COUNT(DISTINCT name) FROM models").fetchone()[0]
    return {"report": report, "distinct_names": distinct}


def paginate(conn: sqlite3.Connection, page_size: int, page: int) -> dict:
    """LIMIT/OFFSET pagination with total and has_next."""
    _ensure_models(conn)
    if page < 1:
        page = 1
    offset = (page - 1) * page_size
    rows = [tuple(r) for r in conn.execute(
        "SELECT name, metric FROM models "
        "ORDER BY metric DESC, name ASC LIMIT ? OFFSET ?",
        (page_size, offset))]
    total = conn.execute("SELECT COUNT(*) FROM models").fetchone()[0]
    has_next = offset + page_size < total
    return {"rows": rows, "total": total, "has_next": has_next}
