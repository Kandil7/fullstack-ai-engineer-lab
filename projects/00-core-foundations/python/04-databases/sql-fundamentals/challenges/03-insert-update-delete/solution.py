"""
Challenge 03: insert-update-delete — Reference Solution
========================================================
"""

import sqlite3


def insert_models(conn: sqlite3.Connection, rows: list[tuple]) -> int:
    """Batch insert via executemany; return rowcount."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS models ("
        "id INTEGER PRIMARY KEY, name TEXT UNIQUE, epoch INT, metric REAL)")
    cur = conn.executemany(
        "INSERT INTO models (name, epoch, metric) VALUES (?, ?, ?)", rows)
    return cur.rowcount


def sync_models(conn: sqlite3.Connection, rows: list[tuple]) -> list[tuple]:
    """Upsert by name; return sorted (name, epoch)."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS models ("
        "id INTEGER PRIMARY KEY, name TEXT UNIQUE, epoch INT, metric REAL)")
    conn.executemany(
        "INSERT INTO models (name, epoch, metric) VALUES (?, ?, ?) "
        "ON CONFLICT(name) DO UPDATE SET epoch = excluded.epoch, "
        "metric = excluded.metric",
        rows,
    )
    return [tuple(r) for r in conn.execute(
        "SELECT name, epoch FROM models ORDER BY name")]


def apply_changeset(conn: sqlite3.Connection, ops: list[tuple]) -> list[int]:
    """Apply insert/update/delete ops; collect RETURNING ids in order."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS models ("
        "id INTEGER PRIMARY KEY, name TEXT UNIQUE, epoch INT, metric REAL)")
    ids: list[int] = []
    for op in ops:
        kind = op[0]
        if kind == "insert":
            _, name, epoch = op
            row = conn.execute(
                "INSERT INTO models (name, epoch, metric) VALUES (?, ?, ?) "
                "RETURNING id", (name, epoch, 0.0)).fetchone()
            ids.append(row[0])
        elif kind == "update":
            _, name, epoch = op
            row = conn.execute(
                "UPDATE models SET epoch = ? WHERE name = ? RETURNING id",
                (epoch, name)).fetchone()
            if row is not None:
                ids.append(row[0])
        elif kind == "delete":
            _, name = op
            row = conn.execute(
                "DELETE FROM models WHERE name = ? RETURNING id",
                (name,)).fetchone()
            if row is not None:
                ids.append(row[0])
    return ids
