"""
SQL Fundamentals — 07: Joins
=============================
Topics: INNER/LEFT/RIGHT/FULL/CROSS joins, self-joins, multi-joins,
        join cardinality and row explosion

Why this matters for AI/backend engineering:
    Retrieval systems join documents to embeddings, users to sessions,
    models to experiments. Getting the join TYPE wrong silently
    duplicates or drops rows; the row-explosion trap (join cardinality)
    is how dashboards and eval sets get corrupted numbers.

Run:      python 07-joins.py
Verify:   python 07-joins.py --verify
Reference: https://www.sqlite.org/lang_select.html
"""

from __future__ import annotations

import sqlite3
import sys

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL)")
conn.executemany("INSERT INTO users (id, name) VALUES (?, ?)",
                 [(1, "ada"), (2, "bob"), (3, "cyn")])
conn.executemany("INSERT INTO orders (id, user_id, amount) VALUES (?, ?, ?)",
                 [(1, 1, 100.0), (2, 1, 50.0), (3, 2, 75.0), (4, None, 25.0)])  # order w/o user

# ============================================================
# 1. INNER JOIN — rows matching on BOTH sides only
# ============================================================
print("=== 1. INNER JOIN ===")
rows = conn.execute(
    """
    SELECT u.name, o.amount
    FROM users u
    INNER JOIN orders o ON o.user_id = u.id
    ORDER BY o.amount
    """
).fetchall()
print(f"  {rows}")
print("  -> users with no orders (cyn) and orders with no user are dropped")

# ============================================================
# 2. LEFT JOIN — all LEFT rows, matched or NULL
# ============================================================
print("\n=== 2. LEFT JOIN ===")
rows = conn.execute(
    """
    SELECT u.name, o.amount
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
    ORDER BY u.id
    """
).fetchall()
print(f"  {rows}")
print("  -> cyn appears with NULL amount (no order)")

# ============================================================
# 3. RIGHT / FULL JOIN — sqlite lacks them; emulate with LEFT
# ============================================================
print("\n=== 3. RIGHT/FULL emulation ===")
rows = conn.execute(
    """
    SELECT u.name, o.amount
    FROM orders o
    LEFT JOIN users u ON o.user_id = u.id
    ORDER BY o.id
    """
).fetchall()
print(f"  right-ish (all orders): {rows}")
print("  -> order 4 has user NULL; FULL JOIN = LEFT + RIGHT minus overlap")

# ============================================================
# 4. SELF JOIN — a table joined to itself (manager/employee)
# ============================================================
conn.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)")
conn.executemany("INSERT INTO employees (id, name, manager_id) VALUES (?, ?, ?)",
                 [(1, "ceo", None), (2, "eng1", 1), (3, "eng2", 1), (4, "intern", 2)])
print("\n=== 4. SELF JOIN ===")
rows = conn.execute(
    """
    SELECT e.name AS employee, m.name AS manager
    FROM employees e
    LEFT JOIN employees m ON e.manager_id = m.id
    ORDER BY e.id
    """
).fetchall()
print(f"  {rows}")

# ============================================================
# 5. CROSS JOIN + join cardinality (row explosion)
# ============================================================
print("\n=== 5. CROSS JOIN ===")
print(f"  users x orders = {len(conn.execute('SELECT * FROM users CROSS JOIN orders').fetchall())} rows")
print("  -> every row pair; only for small sets or deliberate generation")

# Row explosion demo: joining on a NON-unique key multiplies rows
conn.execute("CREATE TABLE teams (id INTEGER PRIMARY KEY, name TEXT, user_id INTEGER)")
conn.executemany("INSERT INTO teams (id, name, user_id) VALUES (?, ?, ?)",
                 [(1, "ml", 1), (2, "backend", 1), (3, "data", 2)])
print("\n  join cardinality:")
for join_type, sql in [
    ("INNER (users->teams)", "SELECT COUNT(*) FROM users u INNER JOIN teams t ON t.user_id = u.id"),
    ("CROSS", "SELECT COUNT(*) FROM users CROSS JOIN teams"),
]:
    print(f"    {join_type}: {conn.execute(sql).fetchone()[0]} rows")

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: INNER JOIN when you need all users -> cyn vanishes silently
# CORRECT: LEFT JOIN and check for NULLs on the right side
#
# MISTAKE: joining on a non-unique key -> row explosion (1 user x 2 teams)
# CORRECT: check join cardinality; join on unique keys when possible
#
# MISTAKE: forgetting the ON condition -> accidental CROSS JOIN
# CORRECT: always write the join predicate explicitly

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE a (id INTEGER PRIMARY KEY, v TEXT)")
        conn.execute("CREATE TABLE b (id INTEGER PRIMARY KEY, a_id INTEGER, w TEXT)")
        conn.executemany("INSERT INTO a (id, v) VALUES (?, ?)", [(1, "x"), (2, "y"), (3, "z")])
        conn.executemany("INSERT INTO b (id, a_id, w) VALUES (?, ?, ?)",
                         [(1, 1, "m"), (2, 1, "n"), (3, 2, "o")])

        # 1. INNER drops unmatched on either side; matches fan out
        rows = conn.execute(
            "SELECT a.v FROM a INNER JOIN b ON b.a_id = a.id ORDER BY a.v"
        ).fetchall()
        assert rows == [("x",), ("x",), ("y",)], \
            "INNER must keep every match (x twice) and drop z"

        # 2. LEFT keeps all a rows, NULL-padded
        rows = conn.execute(
            "SELECT a.v, b.w FROM a LEFT JOIN b ON b.a_id = a.id ORDER BY a.v"
        ).fetchall()
        assert rows == [("x", "m"), ("x", "n"), ("y", "o"), ("z", None)], \
            "LEFT must keep z with NULL"

        # 3. CROSS JOIN cardinality = |a| x |b|
        assert conn.execute("SELECT COUNT(*) FROM a CROSS JOIN b").fetchone()[0] == 9, \
            "CROSS must produce product cardinality"

        # 4. Non-unique join key explodes rows
        rows = conn.execute(
            "SELECT COUNT(*) FROM a INNER JOIN b ON b.a_id = a.id"
        ).fetchone()[0]
        assert rows == 3, "row count = sum of matches per key"

        # 5. Self join resolves a hierarchy
        conn.execute("CREATE TABLE e (id INTEGER PRIMARY KEY, name TEXT, mgr INTEGER)")
        conn.executemany("INSERT INTO e (id, name, mgr) VALUES (?, ?, ?)",
                         [(1, "boss", None), (2, "mid", 1), (3, "grunt", 2)])
        rows = conn.execute(
            "SELECT e.name, m.name FROM e LEFT JOIN e m ON e.mgr = m.id ORDER BY e.id"
        ).fetchall()
        assert rows == [("boss", None), ("mid", "boss"), ("grunt", "mid")], \
            "self join must resolve the hierarchy"
    finally:
        conn.close()
    print("[OK] 07-joins: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. INNER: matched rows only; LEFT: all left rows, NULL-padded")
        print("2. RIGHT/FULL emulate with reversed LEFT joins")
        print("3. Self joins resolve hierarchies (manager/employee)")
        print("4. CROSS = product; non-unique keys explode rows")
        _verify()
