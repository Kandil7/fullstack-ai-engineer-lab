"""
Challenge 13: sql-injection — Reference Solution
=================================================
"""

import sqlite3


def safe_login(conn: sqlite3.Connection, username: str) -> tuple | None:
    """Parameterized lookup: the input can never become syntax."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY, username TEXT UNIQUE, role TEXT)")
    return conn.execute(
        "SELECT id, username, role FROM users WHERE username = ?",
        (username,)).fetchone()


def safe_sort(conn: sqlite3.Connection, column_name: str, ascending: bool) -> list[tuple]:
    """Identifiers only through a whitelist; values only as parameters."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS models (id INTEGER PRIMARY KEY, name TEXT, metric REAL)")
    whitelist = {"name": "name", "metric": "metric"}
    if column_name not in whitelist:
        raise ValueError("unknown sort column")
    column = whitelist[column_name]
    direction = "ASC" if ascending else "DESC"
    # column and direction come from the closed whitelist — safe by construction
    sql = f"SELECT name, metric FROM models ORDER BY {column} {direction}"
    return [tuple(r) for r in conn.execute(sql)]


def secure_search(conn: sqlite3.Connection, term: str, limit: int) -> dict:
    """LIKE pattern as a parameter; limit validated; probe stacked input."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS models (id INTEGER PRIMARY KEY, name TEXT, metric REAL)")
    try:
        safe_limit = int(limit)
    except (TypeError, ValueError):
        safe_limit = 10
    if not 1 <= safe_limit <= 100:
        safe_limit = 10

    rows = [tuple(r) for r in conn.execute(
        "SELECT name, metric FROM models WHERE name LIKE ? ORDER BY name LIMIT ?",
        (f"%{term}%", safe_limit))]

    before = conn.execute("SELECT COUNT(*) FROM models").fetchone()[0]
    conn.execute(
        "SELECT name FROM models WHERE name LIKE ?",
        (f"%{term}'; DELETE FROM models; --%",))
    after = conn.execute("SELECT COUNT(*) FROM models").fetchone()[0]

    return {"rows": rows, "probe_ok": before == after}
