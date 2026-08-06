"""
Challenge 14: query-optimization — Reference Solution
======================================================
"""

import sqlite3


def sargable_plan(conn: sqlite3.Connection) -> dict:
    """Prove sargability with EXPLAIN QUERY PLAN."""
    conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, ts INTEGER)")
    conn.executemany("INSERT INTO events (ts) VALUES (?)",
                     [(i,) for i in range(1, 5001)])
    conn.execute("CREATE INDEX idx_events_ts ON events(ts)")
    return {
        "sargable": [r[3] for r in conn.execute(
            "EXPLAIN QUERY PLAN SELECT * FROM events WHERE ts >= ?", (2500,))],
        "wrapped": [r[3] for r in conn.execute(
            "EXPLAIN QUERY PLAN SELECT * FROM events WHERE ts / 1000 >= ?", (2,))],
    }


def keyset_page(conn: sqlite3.Connection, after_id: int, limit: int) -> dict:
    """Keyset pagination via the primary key."""
    conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, name TEXT)")
    conn.executemany("INSERT INTO events (name) VALUES (?)",
                     [(f"e{i}",) for i in range(1, 5001)])
    rows = [tuple(r) for r in conn.execute(
        "SELECT id, name FROM events WHERE id > ? ORDER BY id LIMIT ?",
        (after_id, limit))]
    plan = [r[3] for r in conn.execute(
        "EXPLAIN QUERY PLAN SELECT id FROM events "
        "WHERE id > ? ORDER BY id LIMIT ?", (after_id, limit))]
    return {"rows": rows, "plan": plan}


def batch_fetch(conn: sqlite3.Connection, parent_ids: list[int], batch_size: int) -> dict:
    """Chunked IN queries with an executed-query counter."""
    conn.execute("CREATE TABLE children (id INTEGER PRIMARY KEY, parent_id INTEGER, value TEXT)")
    conn.executemany(
        "INSERT INTO children (parent_id, value) VALUES (?, ?)",
        [(pid, f"c{pid}-{i}") for pid in parent_ids for i in range(3)])

    count = {"n": 0}
    conn.set_trace_callback(lambda sql: count.__setitem__("n", count["n"] + 1))

    rows = []
    for i in range(0, len(parent_ids), batch_size):
        chunk = parent_ids[i:i + batch_size]
        placeholders = ",".join("?" * len(chunk))
        rows.extend(conn.execute(
            f"SELECT parent_id, value FROM children "
            f"WHERE parent_id IN ({placeholders}) ORDER BY parent_id, value",
            tuple(chunk)).fetchall())

    conn.set_trace_callback(None)
    return {"rows": [tuple(r) for r in rows], "queries": count["n"]}
