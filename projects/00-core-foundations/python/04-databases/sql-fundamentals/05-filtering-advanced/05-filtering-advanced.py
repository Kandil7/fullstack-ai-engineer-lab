"""
SQL Fundamentals — 05: Advanced Filtering
=============================================
Topics: IN / BETWEEN / LIKE, IS NULL, boolean logic, three-valued logic traps

Why this matters for AI/backend engineering:
    Filtering is where data-quality bugs hide. "Score NOT IN (1, NULL)"
    silently returning nothing has shipped more empty dashboards and
    missing training sets than any other SQL trap. A feature-store query
    with a NULL sneaking into a NOT IN is an evaluation bug you cannot see
    until metrics collapse.

Run:      python 05-filtering-advanced.py
Verify:   python 05-filtering-advanced.py --verify
Reference: https://www.sqlite.org/lang_expr.html
"""

from __future__ import annotations

import sqlite3
import sys

conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        stock INTEGER        -- NULL means "unknown", not "zero"
    )
    """
)
conn.executemany(
    "INSERT INTO items (name, category, price, stock) VALUES (?, ?, ?, ?)",
    [
        ("widget", "tools", 9.99, 12),
        ("gadget", "tools", 15.50, 0),
        ("bolt", "hardware", 0.25, 500),
        ("sensor", "electronics", 45.00, None),
        ("cable", "electronics", 3.25, 80),
        ("lens", "optics", 120.00, None),
    ],
)

# ============================================================
# 1. IN and BETWEEN
# ============================================================
# IN is a set-membership test; BETWEEN is inclusive on both ends. Both are
# syntactic sugar the planner turns into range/OR lookups — IN with a long
# list can be slower than a join; BETWEEN is not (x BETWEEN a AND b) ==
# (x >= a AND x <= b).

# Example 1: IN and BETWEEN
print("=== 1. IN / BETWEEN ===")
r = conn.execute("SELECT name FROM items WHERE category IN (?, ?) ORDER BY id", ("tools", "optics")).fetchall()
print(f"IN (tools, optics): {[x[0] for x in r]}")
r = conn.execute("SELECT name FROM items WHERE price BETWEEN ? AND ? ORDER BY id", (1.0, 50.0)).fetchall()
print(f"BETWEEN 1.0 AND 50.0: {[x[0] for x in r]}")
print()

# ============================================================
# 2. LIKE — pattern matching
# ============================================================
# % matches any run, _ matches exactly one character. LIKE is case-
# insensitive for ASCII by default in sqlite; the same patterns exist in
# Postgres (ILIKE for case-insensitive). A leading % (LIKE '%x') cannot
# use a B-tree index — see topics 10 and 14.

# Example 2: LIKE patterns
print("=== 2. LIKE ===")
r = conn.execute("SELECT name FROM items WHERE name LIKE ? ORDER BY id", ("%et",)).fetchall()
print(f"LIKE '%et': {[x[0] for x in r]}")
r = conn.execute("SELECT name FROM items WHERE name LIKE ? ORDER BY id", ("w_dg_t",)).fetchall()
print(f"LIKE 'w_dg_t' (one wildcard each): {[x[0] for x in r]}")
print()

# ============================================================
# 3. IS NULL — the only correct NULL test
# ============================================================
# NULL is UNKNOWN. `= NULL`, `!= NULL`, `IN (NULL)` all yield UNKNOWN and
# therefore exclude the row. IS NULL / IS NOT NULL are the only correct
# tests. stock IS NULL means "no inventory data" — different from stock = 0.

# Example 3: IS NULL vs = 0
print("=== 3. IS NULL ===")
r = conn.execute("SELECT name FROM items WHERE stock IS NULL ORDER BY id").fetchall()
print(f"stock IS NULL: {[x[0] for x in r]}")
r = conn.execute("SELECT name FROM items WHERE stock = ? ORDER BY id", (0,)).fetchall()
print(f"stock = 0:      {[x[0] for x in r]}")
print()

# ============================================================
# 4. Boolean logic — AND, OR, NOT
# ============================================================
# WHERE combines predicates with AND/OR; NOT flips truth but NOT of UNKNOWN
# is still UNKNOWN. Parenthesize OR groups — AND binds tighter than OR.

# Example 4: boolean combinations
print("=== 4. Boolean Logic ===")
r = conn.execute(
    "SELECT name FROM items WHERE (category = ? OR category = ?) AND price > ? ORDER BY id",
    ("tools", "electronics", 3.0),
).fetchall()
print(f"(tools OR electronics) AND price>3: {[x[0] for x in r]}")
r = conn.execute(
    "SELECT name FROM items WHERE NOT (stock IS NULL) AND stock < ? ORDER BY id",
    (100,),
).fetchall()
print(f"NOT NULL-stock AND stock<100: {[x[0] for x in r]}")
print()

# ============================================================
# 5. Three-valued logic traps
# ============================================================
# The classic: WHERE x NOT IN (1, NULL). For a row with x=2 the test is
# (2 <> 1) AND (2 <> NULL) -> TRUE AND UNKNOWN -> UNKNOWN -> row dropped.
# Result: the query returns NOTHING, silently. The fix: exclude NULLs or
# use NOT EXISTS.

# Example 5: the NOT IN (NULL) trap
print("=== 5. Three-Valued Logic ===")
conn.execute("INSERT INTO items (name, category, price, stock) VALUES (?, ?, ?, NULL)", ("mystery", "?", 1.0))
trap = conn.execute(
    "SELECT name FROM items WHERE category NOT IN (?, ?) AND category IS NOT NULL",
    ("tools", "electronics"),
).fetchall()
print(f"category NOT IN (tools, electronics) IS NOT NULL: {[x[0] for x in trap]}")
# UNKNOWN propagates through arithmetic too
val = conn.execute("SELECT 5 + NULL").fetchone()[0]
print(f"5 + NULL = {val}  <- NULL propagates")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: WHERE stock = NULL            -> matches nothing, no error
# CORRECT: WHERE stock IS NULL
#
# MISTAKE: WHERE category NOT IN (?, NULL)  -> matches nothing (UNKNOWN)
# CORRECT: WHERE category NOT IN (?, ?) AND category IS NOT NULL
#          or use NOT EXISTS with a subquery
#
# MISTAKE: BETWEEN is inclusive: BETWEEN 1.0 AND 50.0 includes 50.0 —
#          people write x BETWEEN 0 AND 100 expecting [0,100)
# CORRECT: x >= 0 AND x < 100 when you mean half-open
#
# MISTAKE: forgetting parentheses: WHERE a = 1 OR a = 2 AND b = 3
#          means a = 1 OR (a = 2 AND b = 3) — AND binds tighter
# CORRECT: WHERE (a = 1 OR a = 2) AND b = 3

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, cat TEXT, price REAL, stock INTEGER)")
        conn.executemany(
            "INSERT INTO t (cat, price, stock) VALUES (?, ?, ?)",
            [("a", 10.0, 5), ("b", 20.0, None), ("c", 30.0, 0), ("d", 40.0, None)],
        )

        # 1. IN returns exactly the matching rows
        r = conn.execute("SELECT id FROM t WHERE cat IN (?, ?) ORDER BY id", ("a", "c")).fetchall()
        assert [x[0] for x in r] == [1, 3], "IN must match set membership"

        # 2. BETWEEN is inclusive
        r = conn.execute("SELECT id FROM t WHERE price BETWEEN ? AND ? ORDER BY id", (10.0, 20.0)).fetchall()
        assert [x[0] for x in r] == [1, 2], "BETWEEN must include both bounds"

        # 3. IS NULL vs = 0 are different predicates
        assert conn.execute("SELECT COUNT(*) FROM t WHERE stock IS NULL").fetchone()[0] == 2, \
            "IS NULL counts only NULLs"
        assert conn.execute("SELECT COUNT(*) FROM t WHERE stock = ?", (0,)).fetchone()[0] == 1, \
            "= 0 counts only zeros"

        # 4. NULL comparison trap: x != NULL matches nothing
        assert conn.execute("SELECT COUNT(*) FROM t WHERE stock != ?", (None,)).fetchone()[0] == 0, \
            "!= NULL must match nothing (three-valued logic)"

        # 5. NOT IN with a NULL in the list matches nothing
        rows = conn.execute(
            "SELECT id FROM t WHERE cat NOT IN (?, ?)", ("a", None)
        ).fetchall()
        assert rows == [], "NOT IN (a, NULL) must silently match nothing"

        # 6. NOT IN is safe once NULLs are excluded from the subject column
        rows = conn.execute(
            "SELECT id FROM t WHERE cat NOT IN (?, ?) AND cat IS NOT NULL ORDER BY id",
            ("a", "b"),
        ).fetchall()
        assert [x[0] for x in rows] == [3, 4], "NOT IN with NULL-exclusion must work"

        # 7. LIKE wildcards
        conn.execute("INSERT INTO t (cat) VALUES (?)", ("gadget",))
        r = conn.execute("SELECT id FROM t WHERE cat LIKE ?", ("%get",)).fetchall()
        assert [x[0] for x in r] == [5], "LIKE '%get' must match suffix"
    finally:
        conn.close()
    print("[OK] 05-filtering-advanced: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. IN/BETWEEN/LIKE are range and pattern predicates with defined semantics")
        print("2. IS NULL is the only NULL test; = NULL never matches")
        print("3. UNKNOWN propagates: NOT IN (x, NULL) matches nothing")
        print("4. AND binds tighter than OR - parenthesize")
        _verify()          # always runs, so plain execution is also a test
