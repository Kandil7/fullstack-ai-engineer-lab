"""
SQL Fundamentals — 01: The Relational Model
=================================================
Topics: tables, rows, keys, relations, NULL semantics, set thinking

Why this matters for AI/backend engineering:
    Every feature store, training-data warehouse, and vector-store metadata
    table is a relational structure. Understanding keys and relations is what
    lets you join model predictions to ground truth, deduplicate training rows,
    and reason about NULLs in production data pipelines — NULL bugs silently
    corrupt evaluation metrics and downstream feature tables.

Run:      python 01-relational-model.py
Verify:   python 01-relational-model.py --verify
Reference: https://www.sqlite.org/lang_table.html
"""

from __future__ import annotations

import sqlite3
import sys

# ============================================================
# 1. Tables, Rows, Columns
# ============================================================
# A relational database is a collection of TABLES. Each table is a set of
# ROWS with a fixed set of COLUMNS. A row is one record; a column is one
# attribute. SQL is a set-oriented language: you describe WHAT you want,
# not HOW to get it.

conn = sqlite3.connect(":memory:")
# PRAGMA foreign_keys must be set BEFORE any transaction starts: inside a
# transaction it is silently ignored (sqlite docs: "no-op within a
# transaction"). Postgres/MySQL enforce FKs by default; sqlite does not.
conn.execute("PRAGMA foreign_keys = ON")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (1, "alice", 30))
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (2, "bob", 25))
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (3, "carol", 35))

# Example 1: read the whole table — the rows come back in insert order
# (no ORDER BY means NO guaranteed order; do not depend on it)
rows = conn.execute("SELECT id, name, age FROM users").fetchall()
print("=== 1. Tables ===")
print(f"All users: {rows}")
print(f"Row count: {len(rows)}, columns per row: {len(rows[0])}")
print()

# ============================================================
# 2. Primary Keys and Uniqueness
# ============================================================
# The PRIMARY KEY uniquely identifies a row. The database ENFORCES this:
# a duplicate insert raises IntegrityError. Never design a table without
# one — you cannot reliably join, deduplicate, or upsert without it.

# Example 2: duplicate PK is rejected by the engine
print("=== 2. Primary Key ===")
try:
    conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (1, "evil", 99))
    print("duplicate accepted (BAD)")
except sqlite3.IntegrityError as exc:
    print(f"duplicate PK rejected: {exc}")
# ... but a new id is fine
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (4, "dave", 40))
print(f"After adding dave: {conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]} rows")
print()

# ============================================================
# 3. Foreign Keys and Relations
# ============================================================
# A FOREIGN KEY column references another table's primary key, expressing a
# relation (1:1, 1:N, N:M). sqlite keeps FK checks OFF by default — you must
# enable them per connection with PRAGMA (done above, before any DML). In
# Postgres/MySQL they are on by default; always write code that assumes they
# are enforced.

conn.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(id), title TEXT)")
conn.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (1, "hello world"))
conn.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (1, "second post"))

# Example 3: an orphan post (user_id = 999) must be rejected
print("=== 3. Foreign Keys ===")
try:
    conn.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (999, "orphan"))
    print("orphan accepted (BAD)")
except sqlite3.IntegrityError as exc:
    print(f"orphan FK rejected: {exc}")

# One-to-many: one user -> many posts
post_rows = conn.execute(
    "SELECT p.title FROM posts p JOIN users u ON p.user_id = u.id WHERE u.name = ?",
    ("alice",),
).fetchall()
print(f"alice's posts (1:N): {post_rows}")

# Many-to-many needs a junction (associative) table
conn.execute("CREATE TABLE tags (id INTEGER PRIMARY KEY, name TEXT)")
conn.execute("CREATE TABLE post_tags (post_id INTEGER REFERENCES posts(id), tag_id INTEGER REFERENCES tags(id), PRIMARY KEY (post_id, tag_id))")
conn.execute("INSERT INTO tags (name) VALUES (?)", ("sql",))
conn.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)", (1, 1))
print("Junction table post_tags links posts <-> tags (N:M)")
print()

# ============================================================
# 4. NULL Semantics — NULL is not a value
# ============================================================
# NULL means "unknown / missing", NOT zero and NOT empty string. The killer
# rule: any comparison with NULL yields NULL (which is falsy in WHERE), so
# `x = NULL` NEVER matches — not even `NULL = NULL`. You must use IS NULL.

# Example 4: three-valued logic in action
print("=== 4. NULL Semantics ===")
print(f"NULL = NULL is {conn.execute('SELECT NULL = NULL').fetchone()[0]}")
print(f"NULL IS NULL is {conn.execute('SELECT NULL IS NULL').fetchone()[0]}")
print(f"1 = NULL is {conn.execute('SELECT 1 = NULL').fetchone()[0]}")
print(f"NULL OR TRUE is {conn.execute('SELECT NULL OR TRUE').fetchone()[0]}")
print(f"NULL OR FALSE is {conn.execute('SELECT NULL OR FALSE').fetchone()[0]}")

# Example 5: NULL columns are invisible to equality in WHERE
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, NULL)", (5, "erin"))
found = conn.execute("SELECT name FROM users WHERE age = ?", (None,)).fetchall()
print(f"WHERE age = NULL finds: {found}   <- empty, always")
found = conn.execute("SELECT name FROM users WHERE age IS NULL").fetchall()
print(f"WHERE age IS NULL finds: {found}")
print()

# ============================================================
# 5. Set Thinking — bag semantics vs set semantics
# ============================================================
# SELECT returns a BAG (multiset): duplicates are kept unless you say
# DISTINCT. Thinking in whole sets ("which rows satisfy P?") instead of
# row-by-row ("for each row...") is the single biggest mental shift of SQL.

# Example 6: duplicates survive by default, DISTINCT collapses them
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (6, "alice", 30))
print("=== 5. Set Thinking ===")
names = conn.execute("SELECT name FROM users").fetchall()
print(f"All names (bag):  {[n[0] for n in names]}")
names = conn.execute("SELECT DISTINCT name FROM users").fetchall()
print(f"Names (set):      {[n[0] for n in names]}")

# A row is a member of a set by its VALUES, not by its position.
young = conn.execute("SELECT name FROM users WHERE age < ?", (35,)).fetchall()
print(f"age < 35 (set of rows): {[n[0] for n in young]}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: comparing to NULL with '=':
#   WHERE age = NULL          -> matches nothing, no error, silent bug
# CORRECT:
#   WHERE age IS NULL         -> matches NULLs
#   WHERE age IS NOT NULL     -> matches everything else
#
# MISTAKE: assuming SELECT order is meaningful:
#   SELECT name FROM users    -> 'alice, bob, ...' today, maybe not tomorrow
# CORRECT:
#   SELECT name FROM users ORDER BY id ASC
#
# MISTAKE: skipping the primary key on a table you will join or upsert:
#   CREATE TABLE log (msg TEXT)   -> cannot deduplicate, cannot upsert
# CORRECT:
#   CREATE TABLE log (id INTEGER PRIMARY KEY, msg TEXT)

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Throwaway schema, parameterized queries, explicit cleanup.
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("PRAGMA foreign_keys = ON")  # before any DML, or it is a no-op
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

        # 1. NULL comparison is never true (NULL != NULL)
        assert conn.execute("SELECT 1 WHERE NULL = NULL").fetchone() is None, \
            "NULL = NULL must be UNKNOWN, not true"

        # 2. IS NULL is the correct test
        conn.execute("INSERT INTO t (name, age) VALUES (?, ?)", ("a", None))
        assert conn.execute("SELECT COUNT(*) FROM t WHERE age IS NULL").fetchone()[0] == 1, \
            "IS NULL must match the NULL row"
        assert conn.execute("SELECT COUNT(*) FROM t WHERE age = ?", (None,)).fetchone()[0] == 0, \
            "= NULL must match nothing"

        # 3. PRIMARY KEY uniqueness is enforced by the engine
        conn.execute("INSERT INTO t (name, age) VALUES (?, ?)", ("b", 1))
        try:
            conn.execute("INSERT INTO t (id, name, age) VALUES (?, ?, ?)", (1, "dup", 2))
            raise AssertionError("duplicate PK must raise IntegrityError")
        except sqlite3.IntegrityError:
            pass

        # 4. FOREIGN KEY enforcement rejects orphans when PRAGMA is on
        conn.execute("CREATE TABLE child (id INTEGER PRIMARY KEY, t_id INTEGER REFERENCES t(id))")
        try:
            conn.execute("INSERT INTO child (t_id) VALUES (?)", (999,))
            raise AssertionError("orphan FK must raise IntegrityError")
        except sqlite3.IntegrityError:
            pass

        # 5. Set thinking: DISTINCT collapses bags into sets
        conn.execute("INSERT INTO t (name, age) VALUES (?, ?)", ("a", 2))
        all_rows = conn.execute("SELECT name FROM t").fetchall()
        distinct_rows = conn.execute("SELECT DISTINCT name FROM t").fetchall()
        assert len(all_rows) == 3, "bag keeps duplicates"
        assert len(distinct_rows) == 2, "set collapses duplicates"

        # 6. SQL is set-oriented: filtering returns whole result sets
        rows = conn.execute("SELECT name FROM t WHERE age IS NOT NULL").fetchall()
        assert [r[0] for r in rows] == ["b", "a"], "IS NOT NULL must exclude only NULLs"
    finally:
        conn.close()
    print("[OK] 01-relational-model: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Tables are sets of rows; rows are fixed-column records")
        print("2. PRIMARY KEY uniqueness and FOREIGN KEY integrity are engine-enforced")
        print("3. NULL is UNKNOWN: use IS NULL / IS NOT NULL, never = NULL")
        print("4. SELECT returns a bag; DISTINCT converts it to a set")
        _verify()          # always runs, so plain execution is also a test
