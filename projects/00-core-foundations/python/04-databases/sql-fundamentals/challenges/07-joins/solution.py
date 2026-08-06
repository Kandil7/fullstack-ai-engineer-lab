"""
Challenge 07: joins — Reference Solution
=========================================
"""

import sqlite3


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS posts ("
        "id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT)")


def inner_join_pairs(conn: sqlite3.Connection) -> list[tuple]:
    """INNER JOIN: only writers and their posts."""
    _ensure_schema(conn)
    return [tuple(r) for r in conn.execute(
        "SELECT u.name, p.title FROM users u "
        "INNER JOIN posts p ON p.user_id = u.id "
        "ORDER BY u.name, p.title")]


def left_join_with_nulls(conn: sqlite3.Connection) -> dict:
    """LEFT JOIN keeps everyone; IS NULL finds the unmatched."""
    _ensure_schema(conn)
    counts = [tuple(r) for r in conn.execute(
        "SELECT u.name, COUNT(p.id) FROM users u "
        "LEFT JOIN posts p ON p.user_id = u.id "
        "GROUP BY u.id ORDER BY u.name")]
    inactive = [r[0] for r in conn.execute(
        "SELECT u.name FROM users u "
        "LEFT JOIN posts p ON p.user_id = u.id "
        "WHERE p.id IS NULL ORDER BY u.name")]
    return {"counts": counts, "inactive_names": inactive}


def self_join_report(conn: sqlite3.Connection) -> dict:
    """Self LEFT JOIN with depth levels; DISTINCT fixes fan-out."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS employees ("
        "id INTEGER PRIMARY KEY, name TEXT, mgr_id INTEGER)")
    rows = [tuple(r) for r in conn.execute(
        "SELECT e.name, COALESCE(m.name, 'ROOT'), "
        "CASE WHEN e.mgr_id IS NULL THEN 0 "
        "     WHEN m.mgr_id IS NULL THEN 1 ELSE 2 END "
        "FROM employees e "
        "LEFT JOIN employees m ON m.id = e.mgr_id "
        "LEFT JOIN employees mm ON mm.id = m.mgr_id "
        "ORDER BY e.id")]
    teams = [tuple(r) for r in conn.execute(
        "SELECT m.name, COUNT(DISTINCT e.id) "
        "FROM employees e JOIN employees m ON m.id = e.mgr_id "
        "GROUP BY m.id ORDER BY m.name")]
    return {"rows": rows, "distinct_teams": teams}
