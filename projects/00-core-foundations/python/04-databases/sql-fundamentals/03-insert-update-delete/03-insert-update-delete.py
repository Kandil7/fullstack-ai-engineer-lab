"""
SQL Fundamentals — 03: DML — INSERT / UPDATE / DELETE
===========================================================
Topics: INSERT, RETURNING, upsert (ON CONFLICT), bulk insert, portable
        DELETE with LIMIT

Why this matters for AI/backend engineering:
    Ingestion pipelines are DML: feature rows arrive by the million, are
    upserted into feature stores, and partially cleaned. RETURNING hands
    you the rows you just wrote (needed to sync IDs to downstream systems);
    ON CONFLICT makes ingestion idempotent (re-running a pipeline must not
    duplicate data); portable LIMIT+DELETE is how you purge without holding
    a million-row lock.

Run:      python 03-insert-update-delete.py
Verify:   python 03-insert-update-delete.py --verify
Reference: https://www.sqlite.org/lang_insert.html
"""

from __future__ import annotations

import sqlite3
import sys

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
conn.execute(
    "CREATE TABLE features (id INTEGER PRIMARY KEY, entity TEXT NOT NULL UNIQUE, value REAL NOT NULL)"
)

# ============================================================
# 1. INSERT and RETURNING
# ============================================================
# RETURNING (sqlite 3.35+) returns the row as written — id, defaults, and
# all. This is how you avoid a second SELECT after an insert, and how
# ingestion hands the created key to a message queue or cache.

# Example 1: single insert, capture the generated id
print("=== 1. INSERT ... RETURNING ===")
row = conn.execute(
    "INSERT INTO features (entity, value) VALUES (?, ?) RETURNING id, entity",
    ("user_42", 0.87),
).fetchone()
print(f"RETURNING gave us: {row}  (no second SELECT needed)")
print()

# ============================================================
# 2. Upsert — ON CONFLICT DO UPDATE
# ============================================================
# The ingestion workhorse: try to insert; if the unique key already exists,
# update instead. Idempotent by construction — run the pipeline twice and
# the table still holds one row per entity. (sqlite 3.24+; Postgres has the
# same syntax.)

# Example 2a: fresh insert then re-run -> update, not duplicate
print("=== 2. Upsert ===")
conn.execute(
    """
    INSERT INTO features (entity, value) VALUES (?, ?)
    ON CONFLICT (entity) DO UPDATE SET value = excluded.value
    """,
    ("user_42", 0.92),
)
conn.execute(
    """
    INSERT INTO features (entity, value) VALUES (?, ?)
    ON CONFLICT (entity) DO UPDATE SET value = excluded.value
    """,
    ("user_42", 0.92),
)  # re-run: idempotent
rows = conn.execute("SELECT entity, value FROM features WHERE entity = ?", ("user_42",)).fetchall()
print(f"after upsert x2: {rows}  <- still ONE row, value updated")

# Example 2b: DO NOTHING — first writer wins (e.g., dedup of raw logs)
conn.execute(
    "INSERT INTO features (entity, value) VALUES (?, ?) ON CONFLICT (entity) DO NOTHING",
    ("user_42", 0.1),
)
rows = conn.execute("SELECT value FROM features WHERE entity = ?", ("user_42",)).fetchall()
print(f"after DO NOTHING: {rows}  <- first value kept")
print()

# ============================================================
# 3. Bulk insert — executemany
# ============================================================
# Executing one INSERT per row in a Python loop is a round trip per row.
# executemany sends the same statement with many parameter tuples; sqlite
# compiles the statement once and reuses it (parameter caching).

# Example 3: 500 rows in one call
print("=== 3. Bulk Insert ===")
batch = [(f"entity_{i}", float(i) / 100.0) for i in range(500)]
conn.executemany(
    "INSERT INTO features (entity, value) VALUES (?, ?) ON CONFLICT (entity) DO NOTHING",
    batch,
)
count = conn.execute("SELECT COUNT(*) FROM features").fetchone()[0]
print(f"rows after bulk insert: {count}")
print()

# ============================================================
# 4. UPDATE — with and without RETURNING
# ============================================================
# UPDATE without a WHERE clause touches every row — the data-loss classic.
# Always parameterize the WHERE; use RETURNING to see what changed.

# Example 4: targeted update + returning
print("=== 4. UPDATE ===")
updated = conn.execute(
    "UPDATE features SET value = value * 2 WHERE entity = ? RETURNING entity, value",
    ("user_42",),
).fetchall()
print(f"doubled user_42: {updated}")
print()

# ============================================================
# 5. DELETE with LIMIT — the portable pattern
# ============================================================
# MySQL supports DELETE ... LIMIT n; sqlite and Postgres do NOT. The
# portable form deletes a bounded batch by rowid selected in a subquery.
# Bounded batches keep transactions short and locks small on big tables.

# Example 5: delete exactly one oldest row per call
print("=== 5. Portable DELETE ... LIMIT ===")
conn.execute(
    "DELETE FROM features WHERE rowid IN (SELECT rowid FROM features WHERE value > ? ORDER BY rowid LIMIT ?)",
    (0.9, 1),
)
count = conn.execute("SELECT COUNT(*) FROM features WHERE value > ?", (0.9,)).fetchone()[0]
print(f"rows with value > 0.9 after deleting 1: {count}")

# purge in bounded loops: 10 rows at a time until empty
total_deleted = 0
while True:
    cur = conn.execute(
        "DELETE FROM features WHERE rowid IN (SELECT rowid FROM features WHERE value > ? ORDER BY rowid LIMIT ?)",
        (0.5, 10),
    )
    if cur.rowcount == 0:
        break
    total_deleted += cur.rowcount
print(f"purged {total_deleted} rows in batches of 10")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: UPDATE without WHERE:  UPDATE features SET value = 0
#   -> every row zeroed, no warning, no undo
# CORRECT: UPDATE features SET value = ? WHERE entity = ?
#
# MISTAKE: DELETE ... LIMIT 1 (MySQL-only; crashes on sqlite/Postgres)
# CORRECT: DELETE FROM t WHERE rowid IN (SELECT rowid FROM t WHERE cond LIMIT 1)
#
# MISTAKE: row-by-row INSERT in a Python loop for bulk loads (slow round trips)
# CORRECT: conn.executemany(stmt, batch)
#
# MISTAKE: upsert without the conflict target: ON CONFLICT DO UPDATE ... alone
#   requires a UNIQUE/PK to conflict on; always name it: ON CONFLICT (entity)

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, k TEXT NOT NULL UNIQUE, v INTEGER NOT NULL)")

        # 1. RETURNING returns the written row, including generated id
        row = conn.execute(
            "INSERT INTO t (k, v) VALUES (?, ?) RETURNING id, v", ("a", 1)
        ).fetchone()
        assert row is not None and row[1] == 1, "RETURNING must give the written row"

        # 2. Upsert inserts on first run...
        conn.execute(
            "INSERT INTO t (k, v) VALUES (?, ?) ON CONFLICT (k) DO UPDATE SET v = excluded.v",
            ("a", 5),
        )
        assert conn.execute("SELECT v FROM t WHERE k = ?", ("a",)).fetchone()[0] == 5, \
            "upsert must update on conflict"

        # 3. ...and is idempotent on re-run (still one row)
        conn.execute(
            "INSERT INTO t (k, v) VALUES (?, ?) ON CONFLICT (k) DO UPDATE SET v = excluded.v",
            ("a", 5),
        )
        assert conn.execute("SELECT COUNT(*) FROM t WHERE k = ?", ("a",)).fetchone()[0] == 1, \
            "upsert re-run must not duplicate rows"

        # 4. DO NOTHING keeps the first writer's value
        conn.execute("INSERT INTO t (k, v) VALUES (?, ?) ON CONFLICT (k) DO NOTHING", ("a", 9))
        assert conn.execute("SELECT v FROM t WHERE k = ?", ("a",)).fetchone()[0] == 5, \
            "DO NOTHING must keep the original value"

        # 5. Bulk insert inserts all rows
        conn.executemany("INSERT INTO t (k, v) VALUES (?, ?)", [(f"k{i}", i) for i in range(100)])
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 101, \
            "executemany must insert the full batch"

        # 6. Portable DELETE with LIMIT removes exactly the requested number
        conn.execute(
            "DELETE FROM t WHERE rowid IN (SELECT rowid FROM t WHERE v >= ? ORDER BY rowid LIMIT ?)",
            (50, 10),
        )
        assert conn.execute("SELECT COUNT(*) FROM t WHERE v >= 50").fetchone()[0] == 40, \
            "portable DELETE must delete exactly LIMIT rows"

        # 7. Parameterized statements are safe by construction (no crash on quotes)
        conn.execute("INSERT INTO t (k, v) VALUES (?, ?)", ("O'Reilly; DROP TABLE t; --", 0))
        assert conn.execute("SELECT COUNT(*) FROM t WHERE k = ?", ("O'Reilly; DROP TABLE t; --",)).fetchone()[0] == 1, \
            "parameterized insert must store hostile text as data"
    finally:
        conn.close()
    print("[OK] 03-insert-update-delete: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. RETURNING returns written rows; no second SELECT")
        print("2. ON CONFLICT makes ingestion idempotent (upsert)")
        print("3. executemany bulk-loads; never loop single inserts")
        print("4. Portable DELETE...LIMIT bounds transactions and locks")
        _verify()          # always runs, so plain execution is also a test
