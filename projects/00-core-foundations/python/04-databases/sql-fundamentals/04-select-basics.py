"""
SQL Fundamentals — 04: SELECT Basics
========================================
Topics: projection, WHERE, ORDER BY, LIMIT/OFFSET, DISTINCT, aliases

Why this matters for AI/backend engineering:
    Every model-serving endpoint, evaluation query, and analytics dashboard
    starts as a SELECT. Projection discipline (name the columns you need)
    is what keeps feature queries fast; correct ORDER BY + LIMIT is what
    makes pagination and "top-k" results deterministic; aliases keep
    multi-join feature queries readable.

Run:      python 04-select-basics.py
Verify:   python 04-select-basics.py --verify
Reference: https://www.sqlite.org/lang_select.html
"""

from __future__ import annotations

import sqlite3
import sys

conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE samples (
        id INTEGER PRIMARY KEY,
        label TEXT,
        score REAL
    )
    """
)
conn.executemany(
    "INSERT INTO samples (label, score) VALUES (?, ?)",
    [
        ("cat", 0.95),
        ("dog", 0.88),
        ("cat", 0.62),
        ("bird", 0.40),
        ("dog", 0.91),
        ("cat", 0.99),
    ],
)

# ============================================================
# 1. Projection — choose columns, not SELECT *
# ============================================================
# Projection picks columns; the WHERE clause picks rows. Selecting only the
# columns you consume is the cheapest performance win in SQL — and the
# most ignored (SELECT * ships a whole row when one float was needed).

# Example 1: project two columns; fetchall returns tuples
print("=== 1. Projection ===")
result = conn.execute("SELECT label, score FROM samples").fetchall()
print(f"projected rows: {result}")
print()

# ============================================================
# 2. WHERE — row filtering
# ============================================================
# WHERE filters before ORDER BY and LIMIT run. The order of evaluation
# (filter -> sort -> limit) is why LIMIT on a big table without a filter
# still scans everything.

# Example 2: filter rows
print("=== 2. WHERE ===")
high = conn.execute("SELECT label FROM samples WHERE score > ?", (0.9,)).fetchall()
print(f"score > 0.9: {[r[0] for r in high]}")
print()

# ============================================================
# 3. ORDER BY — and NULL ordering
# ============================================================
# ORDER BY gives rows a defined order (default ASC). In sqlite NULLs sort
# first in ASC; in Postgres they sort last — never rely on NULL position
# without NULLS FIRST/LAST (sqlite 3.30+ supports NULLS FIRST/LAST too).

# Example 3: sort deterministically
print("=== 3. ORDER BY ===")
top3 = conn.execute(
    "SELECT label, score FROM samples ORDER BY score DESC LIMIT ?", (3,)
).fetchall()
print(f"top 3 by score: {top3}")
print()

# ============================================================
# 4. LIMIT / OFFSET — pagination
# ============================================================
# LIMIT n OFFSET m returns n rows after skipping m. Works, but OFFSET pages
# re-read the skipped rows every time — O(offset) work per page (see topic
# 14 for keyset pagination, the fix).

# Example 4: page 2 of size 2
print("=== 4. LIMIT / OFFSET ===")
page = conn.execute(
    "SELECT label, score FROM samples ORDER BY id LIMIT ? OFFSET ?", (2, 2)
).fetchall()
print(f"page 2 (size 2): {page}")
print()

# ============================================================
# 5. DISTINCT — set semantics
# ============================================================
# DISTINCT collapses duplicates across the projected columns. It is NOT a
# cheap operation (sort/hash), so ask for it only when you need the set.

# Example 5: distinct labels
print("=== 5. DISTINCT ===")
labels = conn.execute("SELECT DISTINCT label FROM samples ORDER BY label").fetchall()
print(f"distinct labels: {[r[0] for r in labels]}")
print()

# ============================================================
# 6. Aliases — readability and computed columns
# ============================================================
# Aliases rename a column or expression. They matter in real queries where
# computed features get names that downstream code (or the next join) can
# reference.

# Example 6: computed column with alias
print("=== 6. Aliases ===")
rows = conn.execute(
    "SELECT label, ROUND(score * 100, 1) AS confidence_pct FROM samples WHERE id = ?",
    (1,),
).fetchall()
print(f"aliased computed column: {rows}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: SELECT * when two columns are enough
#   -> more I/O, more bytes over the wire, harder to change the table
# CORRECT: SELECT label, score FROM samples
#
# MISTAKE: relying on default order (no ORDER BY) — row order is not stable
# CORRECT: always add ORDER BY when the consumer cares about order
#
# MISTAKE: WHERE score > 0.9 ORDER BY id LIMIT 3 — forgetting the ORDER BY
#   makes LIMIT 3 return an arbitrary 3 rows
# CORRECT: ORDER BY ... LIMIT ...
#
# MISTAKE: DISTINCT (label, score) != DISTINCT label — DISTINCT applies to
#   the full projected row, not column by column

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, label TEXT, score REAL)")
        conn.executemany(
            "INSERT INTO t (label, score) VALUES (?, ?)",
            [("cat", 0.9), ("dog", 0.7), ("cat", 0.5), ("bird", 0.3)],
        )

        # 1. Projection returns only the requested columns
        rows = conn.execute("SELECT label FROM t").fetchall()
        assert len(rows[0]) == 1, "projection must return one column per row"

        # 2. WHERE filters rows by value
        rows = conn.execute("SELECT label FROM t WHERE score > ?", (0.6,)).fetchall()
        assert [r[0] for r in rows] == ["cat", "dog"], "WHERE must return matching rows"

        # 3. ORDER BY is stable and respected
        rows = conn.execute("SELECT label FROM t ORDER BY score DESC").fetchall()
        assert [r[0] for r in rows] == ["cat", "dog", "cat", "bird"], \
            "ORDER BY DESC must order from high to low"

        # 4. LIMIT/OFFSET slice the ordered result
        rows = conn.execute("SELECT id FROM t ORDER BY id LIMIT ? OFFSET ?", (2, 1)).fetchall()
        assert [r[0] for r in rows] == [2, 3], "LIMIT/OFFSET must slice exactly"

        # 5. DISTINCT collapses duplicates
        rows = conn.execute("SELECT DISTINCT label FROM t").fetchall()
        assert [r[0] for r in rows] == ["cat", "dog", "bird"], "DISTINCT must dedupe"

        # 6. Aliases name computed expressions
        rows = conn.execute(
            "SELECT ROUND(score * 100, 1) AS pct FROM t WHERE id = ?", (1,)
        ).fetchall()
        assert rows[0][0] == 90.0, "aliased expression must compute the value"

        # 7. All queries parameterized: hostile values never break the query
        conn.execute("INSERT INTO t (label, score) VALUES (?, ?)", ("x' OR '1'='1", 0.1))
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 5, \
            "parameterized insert stores the literal"
    finally:
        conn.close()
    print("[OK] 04-select-basics: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Projection picks columns; WHERE picks rows")
        print("2. ORDER BY + LIMIT makes top-k deterministic")
        print("3. OFFSET pagination is simple but scales poorly (see topic 14)")
        print("4. DISTINCT is a set operation, not a column modifier")
        _verify()          # always runs, so plain execution is also a test
