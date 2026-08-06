"""
SQL Fundamentals — 08: Subqueries and CTEs
============================================
Topics: scalar/row/table subqueries, correlated subqueries, WITH CTEs,
        recursive CTEs, readability

Why this matters for AI/backend engineering:
    Ranking documents, filtering by aggregates ("users with more than N
    orders"), and building evaluation cohorts all use subqueries. CTEs
    turn unreadable nested SQL into named, testable steps; recursive
    CTEs walk trees and threads. Correlated subqueries are the classic
    performance trap — know when they are O(n^2).

Run:      python 08-subqueries-ctes.py
Verify:   python 08-subqueries-ctes.py --verify
Reference: https://www.sqlite.org/lang_with.html
"""

from __future__ import annotations

import sqlite3
import sys

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL)")
conn.executemany("INSERT INTO users (id, name) VALUES (?, ?)",
                 [(1, "ada"), (2, "bob"), (3, "cyn"), (4, "dev")])
conn.executemany("INSERT INTO orders (id, user_id, amount) VALUES (?, ?, ?)",
                 [(1, 1, 100.0), (2, 1, 50.0), (3, 2, 75.0), (4, 2, 25.0),
                  (5, 3, 10.0), (6, None, 999.0)])

# ============================================================
# 1. Scalar subquery — one value used inline
# ============================================================
print("=== 1. Scalar Subquery ===")
row = conn.execute(
    "SELECT (SELECT AVG(amount) FROM orders) AS avg_order"
).fetchone()
print(f"  avg order: {row[0]:.2f}")

# ============================================================
# 2. Table subquery in FROM — query a query
# ============================================================
print("\n=== 2. Table Subquery (FROM) ===")
rows = conn.execute(
    """
    SELECT u.name, t.total
    FROM users u
    LEFT JOIN (
        SELECT user_id, SUM(amount) AS total
        FROM orders
        GROUP BY user_id
    ) t ON t.user_id = u.id
    ORDER BY u.id
    """
).fetchall()
for r in rows:
    print(f"  {r[0]}: {r[1]}")
print("  -> pre-aggregate in the subquery, then join = no row explosion")

# ============================================================
# 3. IN / NOT IN with a subquery — membership
# ============================================================
print("\n=== 3. IN Subquery ===")
rows = conn.execute(
    """
    SELECT name FROM users
    WHERE id IN (SELECT user_id FROM orders WHERE amount > 60)
    ORDER BY name
    """
).fetchall()
print(f"  users with big orders: {[r[0] for r in rows]}")

# ============================================================
# 4. Correlated subquery — per-row execution (the trap)
# ============================================================
print("\n=== 4. Correlated Subquery ===")
rows = conn.execute(
    """
    SELECT u.name,
           (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS n_orders
    FROM users u
    ORDER BY u.id
    """
).fetchall()
print(f"  {rows}")
print("  -> runs the subquery ONCE PER USER: O(users x orders) without an index")

# ============================================================
# 5. CTEs — named, reusable query steps
# ============================================================
print("\n=== 5. CTE (WITH) ===")
rows = conn.execute(
    """
    WITH user_totals AS (
        SELECT user_id, SUM(amount) AS total
        FROM orders
        GROUP BY user_id
    )
    SELECT u.name, COALESCE(ut.total, 0) AS total
    FROM users u
    LEFT JOIN user_totals ut ON ut.user_id = u.id
    ORDER BY u.id
    """
).fetchall()
for r in rows:
    print(f"  {r[0]}: {r[1]}")
print("  -> the same join, but the aggregate step has a NAME")

# ============================================================
# 6. Recursive CTE — walking trees
# ============================================================
print("\n=== 6. Recursive CTE ===")
conn.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)")
conn.executemany("INSERT INTO employees (id, name, manager_id) VALUES (?, ?, ?)",
                 [(1, "ceo", None), (2, "eng", 1), (3, "intern", 2), (4, "junior", 2)])
rows = conn.execute(
    """
    WITH RECURSIVE team AS (
        SELECT id, name, manager_id, 0 AS depth
        FROM employees WHERE manager_id IS NULL
        UNION ALL
        SELECT e.id, e.name, e.manager_id, t.depth + 1
        FROM employees e
        JOIN team t ON e.manager_id = t.id
    )
    SELECT name, depth FROM team ORDER BY depth, name
    """
).fetchall()
for r in rows:
    print(f"  {'  ' * r[1]}{r[0]}")
print("  -> anchors at the root, then UNION ALL walks each level")

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: correlated subquery in a hot loop -> O(n^2) scans
# CORRECT: JOIN + GROUP BY, or a CTE, when the subquery repeats per row
#
# MISTAKE: NOT IN with NULLs — a NULL in the subquery result makes
#   NOT IN return NO rows (three-valued logic)
# CORRECT: NOT EXISTS, or filter the subquery with WHERE col IS NOT NULL
#
# MISTAKE: recursive CTE without UNION ALL (infinite loop) or no anchor
# CORRECT: anchor SELECT ... UNION ALL recursive SELECT ... JOIN

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE a (id INTEGER PRIMARY KEY, g TEXT, v INTEGER)")
        conn.executemany("INSERT INTO a (id, g, v) VALUES (?, ?, ?)",
                         [(1, "x", 10), (2, "x", 20), (3, "y", 30), (4, "y", 40)])

        # 1. Scalar subquery
        assert conn.execute("SELECT (SELECT AVG(v) FROM a)").fetchone()[0] == 25.0, \
            "scalar subquery must return one value"

        # 2. Table subquery in FROM
        rows = conn.execute(
            "SELECT t.g, t.s FROM (SELECT g, SUM(v) AS s FROM a GROUP BY g) t ORDER BY t.g"
        ).fetchall()
        assert rows == [("x", 30), ("y", 70)], "table subquery must pre-aggregate"

        # 3. IN membership
        rows = conn.execute(
            "SELECT id FROM a WHERE id IN (SELECT id FROM a WHERE v > 25) ORDER BY id"
        ).fetchall()
        assert rows == [(3,), (4,)], "IN subquery must filter by membership"

        # 4. Correlated subquery correctness
        rows = conn.execute(
            "SELECT a.g, (SELECT COUNT(*) FROM a b WHERE b.g = a.g) FROM a GROUP BY a.g ORDER BY a.g"
        ).fetchall()
        assert rows == [("x", 2), ("y", 2)], "correlated count must be per-group"

        # 5. NOT IN vs NOT EXISTS with NULLs — the classic trap
        conn.execute("CREATE TABLE p (id INTEGER PRIMARY KEY, a_id INTEGER)")
        conn.executemany("INSERT INTO p (id, a_id) VALUES (?, ?)", [(1, 1), (2, None)])
        not_in = conn.execute(
            "SELECT id FROM a WHERE id NOT IN (SELECT a_id FROM p)"
        ).fetchall()
        not_exists = conn.execute(
            "SELECT id FROM a WHERE NOT EXISTS (SELECT 1 FROM p WHERE p.a_id = a.id)"
        ).fetchall()
        assert not_in == [], "NOT IN with a NULL in the set must return nothing"
        assert not_exists != [], "NOT EXISTS must ignore the NULL row"
        assert not_exists == [(2,), (3,), (4,)], "NOT EXISTS is the safe filter"

        # 6. Recursive CTE walks the tree
        conn.execute("CREATE TABLE e (id INTEGER PRIMARY KEY, mgr INTEGER)")
        conn.executemany("INSERT INTO e (id, mgr) VALUES (?, ?)",
                         [(1, None), (2, 1), (3, 2), (4, 1)])
        depth = conn.execute(
            """
            WITH RECURSIVE t AS (
                SELECT id, 0 AS d FROM e WHERE mgr IS NULL
                UNION ALL
                SELECT e.id, t.d + 1 FROM e JOIN t ON e.mgr = t.id
            )
            SELECT id, d FROM t ORDER BY id
            """
        ).fetchall()
        assert depth == [(1, 0), (2, 1), (3, 2), (4, 1)], \
            "recursive CTE must walk levels (ordered by id)"
    finally:
        conn.close()
    print("[OK] 08-subqueries-ctes: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Scalar/table/IN subqueries nest queries")
        print("2. Correlated subqueries run per row — the O(n^2) trap")
        print("3. CTEs name query steps for readability")
        print("4. Recursive CTEs walk trees (UNION ALL + anchor)")
        print("5. NOT IN breaks on NULLs; NOT EXISTS does not")
        _verify()
