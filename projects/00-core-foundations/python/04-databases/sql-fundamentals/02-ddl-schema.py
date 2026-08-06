"""
SQL Fundamentals — 02: DDL — Schema Definition
==================================================
Topics: CREATE/ALTER/DROP, types, NOT NULL, DEFAULT, CHECK, keys

Why this matters for AI/backend engineering:
    Feature-store tables, evaluation-result tables, and ML-metadata schemas
    live or die by their DDL. Constraints (NOT NULL, CHECK, UNIQUE) are the
    database's own data-quality checks: they catch bad training rows at
    write time instead of corrupting your datasets at read time. Knowing DDL
    is what lets you design a schema that stays correct as data grows.

Run:      python 02-ddl-schema.py
Verify:   python 02-ddl-schema.py --verify
Reference: https://www.sqlite.org/lang_createtable.html
"""

from __future__ import annotations

import sqlite3
import sys

# ============================================================
# 1. CREATE TABLE — columns and types
# ============================================================
# sqlite has 5 storage classes: INTEGER, REAL, TEXT, BLOB, NULL (the NUMERIC
# affinity coerce others toward them). Postgres has more precise types;
# the DDL *concepts* transfer. A column declared NOT NULL refuses NULLs;
# DEFAULT fills the value when the INSERT omits it.

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")

conn.execute(
    """
    CREATE TABLE events (
        id        INTEGER PRIMARY KEY,        -- row identity
        name      TEXT NOT NULL,              -- no NULL allowed
        severity  INTEGER NOT NULL DEFAULT 0, -- missing value -> 0
        score     REAL CHECK (score BETWEEN 0.0 AND 1.0),  -- range guard
        payload   TEXT
    )
    """
)

# Example 1: DEFAULT supplies a value; CHECK rejects out-of-range
print("=== 1. CREATE TABLE ===")
conn.execute("INSERT INTO events (name) VALUES (?)", ("anomaly",))
print(f"severity defaulted to 0: {conn.execute('SELECT name, severity FROM events').fetchall()}")
try:
    conn.execute("INSERT INTO events (name, score) VALUES (?, ?)", ("bad", 1.5))
    print("out-of-range CHECK accepted (BAD)")
except sqlite3.IntegrityError as exc:
    print(f"CHECK rejected score=1.5: {exc}")
try:
    conn.execute("INSERT INTO events (name) VALUES (NULL)")
    print("NULL name accepted (BAD)")
except sqlite3.IntegrityError as exc:
    print(f"NOT NULL rejected NULL name: {exc}")
print()

# ============================================================
# 2. Table metadata — the schema is queryable data
# ============================================================
# Every table is described in sqlite_master; column details come from
# PRAGMA table_info. Tooling (migrations, ORMs, feature-store registries)
# reads this metadata instead of hardcoding column lists.

# Example 2: inspect the schema
print("=== 2. Schema Metadata ===")
master = conn.execute(
    "SELECT type, name FROM sqlite_master WHERE type = ? AND name = ? ORDER BY name",
    ("table", "events"),
).fetchall()
print(f"sqlite_master: {master}")
for col in conn.execute("PRAGMA table_info(events)").fetchall():
    print(f"  column: {col}")
print()

# ============================================================
# 3. Keys — PRIMARY KEY and UNIQUE
# ============================================================
# PRIMARY KEY is UNIQUE + NOT NULL (except in sqlite where INTEGER PRIMARY
# KEY can be NULL auto-assigned as rowid alias). UNIQUE alone still allows
# one NULL (NULLs are never equal to each other). This asymmetry is a
# classic bug source in dedup pipelines.

# Example 3: UNIQUE allows at most one NULL
print("=== 3. Keys ===")
conn.execute("CREATE TABLE dedup (token TEXT UNIQUE)")
conn.execute("INSERT INTO dedup (token) VALUES (?)", ("emb-a",))
conn.execute("INSERT INTO dedup (token) VALUES (NULL)")
conn.execute("INSERT INTO dedup (token) VALUES (NULL)")  # second NULL is fine!
print(f"UNIQUE with two NULLs: {conn.execute('SELECT * FROM dedup').fetchall()}")
try:
    conn.execute("INSERT INTO dedup (token) VALUES (?)", ("emb-a",))
    print("duplicate UNIQUE accepted (BAD)")
except sqlite3.IntegrityError as exc:
    print(f"duplicate UNIQUE rejected: {exc}")
print()

# ============================================================
# 4. FOREIGN KEY with ON DELETE behavior
# ============================================================
# FKs express relations and their lifecycle. ON DELETE CASCADE removes
# child rows with the parent; ON DELETE SET NULL nulls the reference.
# Choosing the wrong one leaks orphaned rows into joins.

conn.execute(
    "CREATE TABLE model_runs (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
)
conn.execute(
    """
    CREATE TABLE metrics (
        id INTEGER PRIMARY KEY,
        run_id INTEGER NOT NULL REFERENCES model_runs(id) ON DELETE CASCADE,
        metric TEXT NOT NULL,
        value REAL NOT NULL
    )
    """
)
conn.execute("INSERT INTO model_runs (name) VALUES (?)", ("run-A",))
conn.execute("INSERT INTO metrics (run_id, metric, value) VALUES (?, ?, ?)", (1, "f1", 0.91))

# Example 4: deleting a parent cascades to its metrics
print("=== 4. Foreign Keys ===")
conn.execute("DELETE FROM model_runs WHERE name = ?", ("run-A",))
print(f"metrics after cascade: {conn.execute('SELECT * FROM metrics').fetchall()}  <- gone")
print()

# ============================================================
# 5. ALTER and DROP — evolving a live schema
# ============================================================
# ALTER TABLE ADD COLUMN is metadata-only and cheap; backfilling the new
# column is a separate step. sqlite can also RENAME COLUMN/TABLE. DROP TABLE
# removes the table AND its indexes — irreversible without a backup.

# Example 5: evolve, populate, then drop
print("=== 5. ALTER / DROP ===")
conn.execute("ALTER TABLE events ADD COLUMN created_at TEXT")
conn.execute("UPDATE events SET created_at = ? WHERE created_at IS NULL", ("2026-08-06",))
print(f"after ALTER + backfill: {conn.execute('SELECT name, created_at FROM events').fetchall()}")
conn.execute("DROP TABLE dedup")
remaining = conn.execute(
    "SELECT name FROM sqlite_master WHERE type = ? AND name = ?", ("table", "dedup")
).fetchall()
print(f"dedup still listed? {remaining}  <- gone after DROP")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: declaring a column that must be unique as UNIQUE but relying on
#   it to reject NULLs:  token TEXT UNIQUE   -> NULLs slip through
# CORRECT:               token TEXT NOT NULL UNIQUE
#
# MISTAKE: FK with no ON DELETE clause, then deleting parents and silently
#   accumulating orphans in child tables
# CORRECT: ON DELETE CASCADE (children die with parent) or
#          ON DELETE SET NULL (keep rows, null the link) — pick deliberately
#
# MISTAKE: CHECK with a column-only condition (cannot reference other rows)
#   CHECK (score <= 1.0) is fine; "score <= avg(score)" is not expressible
#
# MISTAKE: forgetting PRAGMA foreign_keys = ON per connection in sqlite —
#   FKs silently do nothing otherwise
# CORRECT: execute the PRAGMA before any DML on every new connection

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("PRAGMA foreign_keys = ON")

        # 1. NOT NULL is enforced
        conn.execute("CREATE TABLE a (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        try:
            conn.execute("INSERT INTO a (name) VALUES (NULL)")
            raise AssertionError("NOT NULL must raise IntegrityError")
        except sqlite3.IntegrityError:
            pass

        # 2. DEFAULT fills omitted values
        conn.execute("CREATE TABLE b (id INTEGER PRIMARY KEY, level INTEGER DEFAULT 3)")
        conn.execute("INSERT INTO b (id) VALUES (1)")
        assert conn.execute("SELECT level FROM b WHERE id = 1").fetchone()[0] == 3, \
            "DEFAULT must fill omitted values"

        # 3. CHECK is enforced
        conn.execute("CREATE TABLE c (id INTEGER PRIMARY KEY, pct REAL CHECK (pct >= 0 AND pct <= 100))")
        try:
            conn.execute("INSERT INTO c (pct) VALUES (?)", (101,))
            raise AssertionError("CHECK must raise IntegrityError")
        except sqlite3.IntegrityError:
            pass

        # 4. PRIMARY KEY uniqueness is enforced
        conn.execute("INSERT INTO c (id, pct) VALUES (1, 50)")
        try:
            conn.execute("INSERT INTO c (id, pct) VALUES (1, 60)")
            raise AssertionError("PK duplicate must raise IntegrityError")
        except sqlite3.IntegrityError:
            pass

        # 5. FK rejects orphans and cascades deletes
        conn.execute("CREATE TABLE p (id INTEGER PRIMARY KEY)")
        conn.execute("CREATE TABLE k (id INTEGER PRIMARY KEY, pid INTEGER REFERENCES p(id) ON DELETE CASCADE)")
        conn.execute("INSERT INTO p (id) VALUES (1)")
        conn.execute("INSERT INTO k (pid) VALUES (1)")
        try:
            conn.execute("INSERT INTO k (pid) VALUES (?)", (99,))
            raise AssertionError("orphan FK must raise IntegrityError")
        except sqlite3.IntegrityError:
            pass
        conn.execute("DELETE FROM p WHERE id = 1")
        assert conn.execute("SELECT COUNT(*) FROM k").fetchone()[0] == 0, \
            "ON DELETE CASCADE must remove children"

        # 6. schema metadata is queryable (sqlite_master + PRAGMA)
        names = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = ? ORDER BY name", ("table",)
        ).fetchall()
        flat = [n[0] for n in names]
        assert flat == ["a", "b", "c", "k", "p"], "sqlite_master must list tables"
        cols = conn.execute("PRAGMA table_info(k)").fetchall()
        assert len(cols) == 2, "PRAGMA table_info must report all columns"
    finally:
        conn.close()
    print("[OK] 02-ddl-schema: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. DDL is code: NOT NULL, DEFAULT, CHECK, UNIQUE are data-quality guards")
        print("2. Schema is data: sqlite_master + PRAGMA power migrations and registries")
        print("3. FK actions (CASCADE/SET NULL) decide what happens to children")
        print("4. ALTER is cheap metadata work; backfill and DROP are separate steps")
        _verify()          # always runs, so plain execution is also a test
