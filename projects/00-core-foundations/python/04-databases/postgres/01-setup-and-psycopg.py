"""
Postgres — 01: Setup and psycopg Connection
=============================================
Topics: connection lifecycle, DSN anatomy, cursors, with blocks, server vs client cursors

Why this matters for AI/backend engineering:
    Every ML service that reads features or writes logs goes through a
    connection: retry a broken pool at the wrong layer and you stall an
    inference endpoint; hold a cursor open too long and you exhaust
    Postgres' connection budget. This file builds the mental model of
    connect -> cursor -> execute -> close that every ORM and feature
    store wraps for you.

Environment note:
    No Postgres server on this machine, so the teaching body uses sqlite3
    (identical connect/cursor semantics). The final section contains REAL
    psycopg3 code that connects to a real server when one is available and
    prints [skip] otherwise. Nothing here ever crashes on a missing dep.

Run:      python 01-setup-and-psycopg.py
Verify:   python 01-setup-and-psycopg.py --verify
Reference: https://www.psycopg.org/psycopg3/docs/basic/connect.html
"""

from __future__ import annotations

import os
import sqlite3
import sys
from typing import Any, Iterator


# ============================================================
# 1. The connection lifecycle — connect, work, close
# ============================================================
# A connection is a network session with the database server. Postgres
# allows a limited number of them (default max_connections = 100), so a
# leaked connection is a production incident waiting to happen. The
# universal pattern is: create, use, ALWAYS close.

# Example 1: manual lifecycle (sqlite3 :memory: is the zero-setup stand-in)
conn = sqlite3.connect(":memory:")
print(f"1. opened connection, type={type(conn).__name__}")
conn.close()
print("   closed connection")
print()

# ============================================================
# 2. DSN anatomy — how a client finds the server
# ============================================================
# psycopg3 accepts a DSN (Data Source Name). Every field has a default;
# you only specify what differs. Credentials belong in the environment
# or a secret manager, never in source code.

# Example 2: parse a Postgres DSN into its parts
def dsn_parts(dsn: str) -> dict[str, str]:
    """Split a Postgres DSN into its named components.

    Handles postgres://user:pass@host:port/dbname and the older
    key=value form. Raises ValueError on an unknown scheme.
    """
    if dsn.startswith("postgres://") or dsn.startswith("postgresql://"):
        rest = dsn.split("://", 1)[1]
        userinfo, _, hostport = rest.partition("@")
        user, _, password = userinfo.partition(":")
        host, _, port_db = hostport.partition(":")
        port, _, dbname = port_db.partition("/")
        parts = {
            "user": user or "postgres",
            "password": password,
            "host": host,
            "port": port or "5432",
            "dbname": dbname or "postgres",
        }
    else:
        parts = {}
        for chunk in dsn.split():
            key, _, value = chunk.partition("=")
            parts[key] = value
    return parts


print("=== 2. DSN anatomy ===")
print("postgres://ml_user:secret@db.internal:5432/features ->", end=" ")
parts = dsn_parts("postgres://ml_user:secret@db.internal:5432/features")
print(parts)
print()

# ============================================================
# 3. Cursors — execute SQL, fetch results
# ============================================================
# A cursor is a handle into a result set. psycopg3 cursors are context
# managers too: `with conn.cursor() as cur:` guarantees the cursor is
# closed even on error. NEVER interpolate values into SQL — always bind
# parameters (psycopg3 uses %s, sqlite3 uses ?).

# Example 3: parameterized DDL + DML + query through one cursor
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute(
    """
    CREATE TABLE model_runs (
        run_id INTEGER PRIMARY KEY,
        model TEXT NOT NULL,
        acc REAL
    )
    """
)
cur.execute(
    "INSERT INTO model_runs (model, acc) VALUES (?, ?)",
    ("bert-base", 0.9231),          # parameterized — never f-string SQL
)
print("   rows affected by INSERT:", cur.rowcount)   # read BEFORE the next query
conn.commit()
cur.execute("SELECT model, acc FROM model_runs")
row = cur.fetchone()
print(f"3. first run: model={row[0]}, acc={row[1]}")
cur.close()
print()

# ============================================================
# 4. with blocks — what each driver's context manager guarantees
# ============================================================
# sqlite3: `with conn:` commits on success / rolls back on error, but
#          does NOT close the connection — close() stays your job.
# psycopg3: `with psycopg.connect(...) as conn:` DOES close on exit,
#          but never commits for you (call conn.commit() explicitly).
# Both guarantee *something* on exit — the details differ. Read the docs
# of the driver you ship.

# Example 4: sqlite3 transaction guard, then explicit close
conn = sqlite3.connect(":memory:")
with conn:                          # transaction guard: commit or rollback
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
    conn.execute("INSERT INTO t (v) VALUES (?)", ("hello",))
n = conn.execute("SELECT COUNT(*) FROM t").fetchone()[0]
print(f"4. rows after with-block commit: {n}  (connection still open)")
conn.close()                        # explicit close — the with-block did not do it
print()

# ============================================================
# 5. Server cursors vs client cursors
# ============================================================
# A CLIENT cursor pulls the whole result set into memory on execute.
# A SERVER cursor (psycopg3: conn.cursor(name="x")) leaves the rows on
# the server and fetches them in chunks — the right tool for a 10M-row
# scan you only need a window of. sqlite3 has no server-side cursor, so
# we simulate the CHUNKING pattern with fetchmany.

# Example 5: chunked reading, the shape of a server-cursor loop
with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE evals (id INTEGER PRIMARY KEY, score REAL)")
    conn.executemany(
        "INSERT INTO evals (score) VALUES (?)",
        [(float(i) / 100.0,) for i in range(25)],   # one tuple per row!
    )
    cur = conn.cursor()
    cur.execute("SELECT id, score FROM evals ORDER BY id")
    chunk_size = 10
    total = 0
    while True:
        chunk = cur.fetchmany(chunk_size)
        if not chunk:
            break
        total += sum(1 for _ in chunk)
    print(f"5. read {total} rows in chunks of {chunk_size} (server-cursor pattern)")
print()

# ============================================================
# 6. Real Postgres via psycopg3 (guarded — skips when no server)
# ============================================================
# This is the ACTUAL production code path. It is valid psycopg3 +
# Postgres SQL; it simply cannot run here because no server exists.
# When you have Docker: `docker compose up -d postgres` (see
# infra/docker/docker-compose.yml) and this block runs for real.

def pg_demo() -> None:
    """Connect to a real Postgres; print [skip] when unavailable."""
    dsn = os.environ.get(
        "PGDSN", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    try:
        import psycopg  # psycopg3 — installed on this machine, harmless
    except ImportError:
        print("[skip] psycopg not installed — pip install 'psycopg[binary]'")
        return
    try:
        with psycopg.connect(dsn, connect_timeout=2) as pg_conn:
            with pg_conn.cursor() as pg_cur:
                pg_cur.execute("SELECT version()")
                version = pg_cur.fetchone()[0]
                print(f"6. connected to Postgres: {version}")
                # Server cursor — rows stay on the server
                with pg_conn.cursor(name="big_scan") as server_cur:
                    server_cur.execute("SELECT 1")   # real named-cursor query
                    print("   server cursor (named) created")
    except Exception as exc:  # noqa: BLE001 — any connection failure = skip
        print(
            "[skip] real Postgres demo: %s -- requires a Postgres server "
            "(install: docker compose up -d postgres)" % exc
        )


pg_demo()
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: conn = sqlite3.connect(...) and never close -> file locks on
#   Windows (PermissionError), exhausted pools on Postgres
# CORRECT: with sqlite3.connect(...) as conn: ...  (auto-close)
#
# MISTAKE: f"SELECT * FROM users WHERE id = {user_id}" -> SQL injection
# CORRECT: cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
#
# MISTAKE: assuming psycopg3's `with conn:` commits (it only closes)
# CORRECT: call conn.commit() explicitly; use `with conn:` for closing
#
# MISTAKE: cur.fetchall() on a 50M-row scan -> gigabytes in RAM
# CORRECT: named server cursor + fetchmany chunking

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. DSN parsing handles the URI form
    parts = dsn_parts("postgresql://ml:secret@db.internal:5432/features")
    assert parts == {
        "user": "ml",
        "password": "secret",
        "host": "db.internal",
        "port": "5432",
        "dbname": "features",
    }, "DSN URI form must parse into named parts"

    # 2. DSN parsing handles key=value form and defaults
    parts = dsn_parts("host=localhost dbname=postgres")
    assert parts["host"] == "localhost" and parts["dbname"] == "postgres", \
        "key=value DSN must parse"

    # 3. Parameterized insert + fetch round-trips data
    with sqlite3.connect(":memory:") as conn:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        conn.execute("INSERT INTO t (v) VALUES (?)", ("safe",))
        conn.commit()
        assert conn.execute("SELECT v FROM t").fetchone()[0] == "safe", \
            "parameterized INSERT must round-trip"

    # 4. Chunked fetchmany reads every row exactly once
    with sqlite3.connect(":memory:") as conn:
        conn.execute("CREATE TABLE e (id INTEGER PRIMARY KEY, x REAL)")
        conn.executemany("INSERT INTO e (x) VALUES (?)", [(float(i),) for i in range(37)])
        cur = conn.cursor()
        cur.execute("SELECT x FROM e")
        seen = 0
        while True:
            chunk = cur.fetchmany(10)
            if not chunk:
                break
            seen += len(chunk)
        assert seen == 37, "fetchmany chunking must visit every row"

    # 5. sqlite3's with-block commits but does NOT close — close() is explicit
    conn = sqlite3.connect(":memory:")
    with conn:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        conn.execute("INSERT INTO t (v) VALUES (?)", ("x",))
    assert conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 1, \
        "with-block must commit the insert"
    conn.close()                  # the with-block left the connection open
    try:
        conn.execute("SELECT 1")
        closed = False
    except sqlite3.ProgrammingError:
        closed = True
    assert closed, "explicit close() must invalidate the connection"

    # 6. rowcount reflects the rows affected by the last DML
    with sqlite3.connect(":memory:") as conn:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        cur = conn.cursor()
        cur.executemany("INSERT INTO t (v) VALUES (?)", [("a",), ("b",), ("c",)])
        assert cur.rowcount == 3, "executemany rowcount must report 3 inserts"

    print("[OK] 01-setup-and-psycopg: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. A connection is a limited, closable session with the server")
        print("2. DSNs name host/port/db/user; credentials come from the environment")
        print("3. Cursors execute SQL and fetch rows; always bind parameters")
        print("4. with-blocks guarantee cleanup; psycopg3 needs explicit commit()")
        print("5. Server cursors chunk huge scans; client cursors buffer everything")
        _verify()          # always runs, so plain execution is also a test
