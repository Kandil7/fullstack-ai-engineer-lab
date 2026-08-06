"""
Challenge 08: subqueries-ctes — Reference Solution
===================================================
"""

import sqlite3


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS orders ("
        "id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL)")


def scalar_report(conn: sqlite3.Connection) -> dict:
    """Per-customer spend + global average as a scalar subquery."""
    _ensure_schema(conn)
    rows = [tuple(r) for r in conn.execute(
        "SELECT c.name, COALESCE(SUM(o.amount), 0.0) AS spend "
        "FROM customers c LEFT JOIN orders o ON o.customer_id = c.id "
        "GROUP BY c.id ORDER BY spend DESC, c.name ASC")]
    avg_spend = conn.execute(
        "SELECT (SELECT AVG(amount) FROM orders)").fetchone()[0]
    return {"rows": rows, "avg_spend": avg_spend}


def anti_join(conn: sqlite3.Connection) -> dict:
    """Two NULL-safe anti-joins must agree."""
    _ensure_schema(conn)
    not_exists = [r[0] for r in conn.execute(
        "SELECT c.name FROM customers c WHERE NOT EXISTS "
        "(SELECT 1 FROM orders o WHERE o.customer_id = c.id) ORDER BY c.name")]
    left_join = [r[0] for r in conn.execute(
        "SELECT c.name FROM customers c "
        "LEFT JOIN orders o ON o.customer_id = c.id "
        "WHERE o.id IS NULL ORDER BY c.name")]
    return {"not_exists": not_exists, "left_join": left_join,
            "identical": not_exists == left_join}


def recursive_spine(conn: sqlite3.Connection, start: str, end: str) -> list[tuple]:
    """Daily counts with zero-fill via a recursive date spine."""
    conn.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, date TEXT)")
    rows = [tuple(r) for r in conn.execute(
        "WITH RECURSIVE days(d) AS ("
        "SELECT ? UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < ?) "
        "SELECT days.d, COALESCE(COUNT(events.id), 0) "
        "FROM days LEFT JOIN events ON events.date = days.d "
        "GROUP BY days.d ORDER BY days.d", (start, end))]
    return rows
