"""
Challenge 10: indexes-and-plans — Reference Solution
=====================================================
"""

import sqlite3


def plan_for(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[str]:
    """Extract plan detail strings (column index 3)."""
    return [r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + sql, params)]


def sargable_vs_not(conn: sqlite3.Connection) -> dict:
    """Sargable predicate SEARCHes; wrapped column SCANs."""
    conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, ts INTEGER)")
    conn.executemany("INSERT INTO events (ts) VALUES (?)",
                     [(i,) for i in range(1, 5001)])
    conn.execute("CREATE INDEX idx_events_ts ON events(ts)")
    return {
        "sargable": plan_for(conn, "SELECT * FROM events WHERE ts >= ?", (2500,)),
        "wrapped": plan_for(conn, "SELECT * FROM events WHERE ts / 1000 >= ?", (2,)),
    }


def covering_vs_table(conn: sqlite3.Connection) -> dict:
    """Projection uses the covering index; SELECT * reads the table."""
    conn.execute(
        "CREATE TABLE events (id INTEGER PRIMARY KEY, model TEXT, latency REAL, payload TEXT)")
    conn.executemany(
        "INSERT INTO events (model, latency, payload) VALUES (?, ?, ?)",
        [(f"m{i % 3}", round(i * 0.01, 3), "x" * 20) for i in range(1, 5001)])
    conn.execute("CREATE INDEX idx_cover ON events(model, latency)")
    return {
        "covering": plan_for(
            conn, "SELECT model, latency FROM events WHERE model = ?", ("m1",)),
        "star": plan_for(
            conn, "SELECT * FROM events WHERE model = ?", ("m1",)),
    }


def index_strategy(conn: sqlite3.Connection) -> dict:
    """Composite (equality, range, sort) + partial index."""
    conn.execute(
        "CREATE TABLE events (id INTEGER PRIMARY KEY, model TEXT, latency REAL, "
        "created_at INT, status TEXT)")
    conn.executemany(
        "INSERT INTO events (model, latency, created_at, status) VALUES (?, ?, ?, ?)",
        [(f"m{i % 3}", round(i * 0.01, 3), 1700000000 + i,
          "active" if i % 2 else "archived") for i in range(1, 5001)])
    conn.execute(
        "CREATE INDEX idx_events_model_latency_created "
        "ON events(model, latency, created_at)")
    conn.execute(
        "CREATE INDEX idx_events_model_created ON events(model, created_at)")
    conn.execute(
        "CREATE INDEX idx_events_active ON events(status) WHERE status = 'active'")
    return {
        "equality_range": plan_for(
            conn, "SELECT * FROM events WHERE model = ? AND latency > ?", ("m1", 10.0)),
        "order_by": plan_for(
            conn, "SELECT id FROM events WHERE model = ? ORDER BY created_at", ("m1",)),
        "partial": plan_for(
            conn, "SELECT id FROM events WHERE status = 'active'", ()),
    }
