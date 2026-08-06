"""
SQL Fundamentals — 06: Aggregation
======================================
Topics: COUNT/SUM/AVG/MIN/MAX, GROUP BY, HAVING vs WHERE, COUNT(*) vs COUNT(col)

Why this matters for AI/backend engineering:
    Training-data profiling, evaluation aggregation, and drift monitoring
    are GROUP BY queries: per-label accuracy, per-bucket recall, per-model
    latency percentiles. The COUNT(*) vs COUNT(col) NULL difference is a
    silent metric bug; HAVING vs WHERE misuse filters at the wrong stage
    and corrupts group-level statistics.

Run:      python 06-aggregation.py
Verify:   python 06-aggregation.py --verify
Reference: https://www.sqlite.org/lang_aggfunc.html
"""

from __future__ import annotations

import sqlite3
import sys

conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE predictions (
        id INTEGER PRIMARY KEY,
        model TEXT NOT NULL,
        correct INTEGER,          -- 1 = right, 0 = wrong
        latency_ms REAL,
        confidence REAL           -- NULL = abstained
    )
    """
)
conn.executemany(
    "INSERT INTO predictions (model, correct, latency_ms, confidence) VALUES (?, ?, ?, ?)",
    [
        ("v1", 1, 12.0, 0.91),
        ("v1", 0, 15.0, 0.62),
        ("v1", 1, 11.0, 0.97),
        ("v2", 1, 30.0, 0.80),
        ("v2", 1, 28.0, 0.85),
        ("v2", 0, 33.0, 0.55),
        ("v2", 0, 29.0, None),   # abstained -> confidence NULL
    ],
)

# ============================================================
# 1. Whole-table aggregates — COUNT, SUM, AVG, MIN, MAX
# ============================================================
# Aggregates collapse many rows into one number. AVG/SUM ignore NULLs
# (they are computed over the non-NULL subset). COUNT(*) counts rows;
# COUNT(col) counts NON-NULL values of that column — a different number
# whenever the column has NULLs.

# Example 1: one-row summaries
print("=== 1. Whole-Table Aggregates ===")
row = conn.execute(
    "SELECT COUNT(*), COUNT(correct), SUM(correct), AVG(latency_ms), MIN(latency_ms), MAX(latency_ms) FROM predictions"
).fetchone()
print(f"rows={row[0]} non-null correct={row[1]} correct_sum={row[2]} avg_lat={row[3]:.1f} min={row[4]} max={row[5]}")
row = conn.execute("SELECT COUNT(*), COUNT(confidence) FROM predictions").fetchone()
print(f"COUNT(*)={row[0]} vs COUNT(confidence)={row[1]}  <- NULLs dropped by COUNT(col)")
print()

# ============================================================
# 2. GROUP BY — per-group aggregates
# ============================================================
# GROUP BY splits rows into groups; each aggregate runs per group. This is
# the "for each model" query pattern of evaluation code.

# Example 2: per-model accuracy and latency
print("=== 2. GROUP BY ===")
rows = conn.execute(
    """
    SELECT model,
           COUNT(*) AS n,
           SUM(correct) AS correct,
           ROUND(100.0 * SUM(correct) / COUNT(*), 1) AS acc_pct,
           ROUND(AVG(latency_ms), 1) AS avg_lat
    FROM predictions
    GROUP BY model
    ORDER BY model
    """
).fetchall()
for r in rows:
    print(f"  {r[0]}: n={r[1]} correct={r[2]} acc={r[3]}% avg_lat={r[4]}ms")
print()

# ============================================================
# 3. HAVING vs WHERE — which stage filters what
# ============================================================
# WHERE filters ROWS before grouping; HAVING filters GROUPS after
# aggregation. You cannot write per-group conditions in WHERE — the group
# does not exist yet. And HAVING without GROUP BY treats the whole table
# as one group.

# Example 3: WHERE (rows) then HAVING (groups)
print("=== 3. HAVING vs WHERE ===")
rows = conn.execute(
    """
    SELECT model, COUNT(*) AS n
    FROM predictions
    WHERE latency_ms < ?      -- filters rows FIRST
    GROUP BY model
    HAVING COUNT(*) >= ?      -- filters groups AFTER
    ORDER BY model
    """,
    (32.0, 2),
).fetchall()
print(f"models with >=2 fast rows (lat<32): {rows}")
print()

# ============================================================
# 4. GROUP BY pitfalls — grouping by non-grouped columns
# ============================================================
# Any selected column must be either a group key or inside an aggregate.
# sqlite silently allows bare columns (returns an arbitrary row's value);
# Postgres raises an error. Write portable SQL: only keys + aggregates.

# Example 4: sqlite's permissive bare column
print("=== 4. GROUP BY Pitfall ===")
row = conn.execute(
    "SELECT model, latency_ms FROM predictions GROUP BY model ORDER BY model"
).fetchall()
print(f"bare latency_ms per group (arbitrary!): {row}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: COUNT(confidence) when you meant COUNT(*) — one NULL and your
#   "how many predictions" number silently shrinks
# CORRECT: COUNT(*) for rows; COUNT(col) deliberately for non-null values
#
# MISTAKE: WHERE SUM(correct) > 1  -> SQL error (aggregate in WHERE)
# CORRECT: HAVING SUM(correct) > 1
#
# MISTAKE: AVG(confidence) over abstained rows — AVG ignores NULLs, so the
#   average is over the non-abstained subset. If you want NULLs counted as
#   0, say COALESCE(confidence, 0) inside the aggregate
# CORRECT: AVG(COALESCE(confidence, 0))
#
# MISTAKE: GROUP BY with SELECT * — group keys and aggregates only

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, g TEXT, v INTEGER)")
        conn.executemany(
            "INSERT INTO t (g, v) VALUES (?, ?)",
            [("a", 1), ("a", 2), ("a", 3), ("a", None), ("b", 10), ("b", 20)],
        )

        # 1. COUNT(*) vs COUNT(col) differ when NULLs exist
        row = conn.execute("SELECT COUNT(*), COUNT(v) FROM t").fetchone()
        assert (row[0], row[1]) == (6, 5), "COUNT(col) must exclude NULLs"

        # 2. SUM/AVG ignore NULLs
        assert conn.execute("SELECT SUM(v) FROM t").fetchone()[0] == 36, \
            "SUM must add non-NULL values"
        assert conn.execute("SELECT AVG(v) FROM t").fetchone()[0] == 7.2, \
            "AVG must divide by the non-NULL count (36 / 5)"

        # 3. MIN/MAX are NULL-aware
        assert conn.execute("SELECT MIN(v), MAX(v) FROM t").fetchone() == (1, 20), \
            "MIN/MAX must ignore NULLs"

        # 4. GROUP BY computes per-group aggregates
        rows = conn.execute("SELECT g, COUNT(*) FROM t GROUP BY g ORDER BY g").fetchall()
        assert rows == [("a", 4), ("b", 2)], "GROUP BY must bucket rows"

        # 5. HAVING filters groups, WHERE filters rows
        rows = conn.execute(
            "SELECT g, COUNT(*) AS n FROM t WHERE v IS NOT NULL GROUP BY g HAVING COUNT(*) > ? ORDER BY g",
            (2,),
        ).fetchall()
        assert rows == [("a", 3)], "HAVING must filter after grouping"
        rows = conn.execute(
            "SELECT g, COUNT(*) AS n FROM t WHERE v > ? GROUP BY g ORDER BY g", (5,)
        ).fetchall()
        assert rows == [("b", 2)], "WHERE must filter before grouping"

        # 6. COALESCE makes AVG treat NULLs as a chosen value
        assert conn.execute("SELECT AVG(COALESCE(v, 0)) FROM t").fetchone()[0] == 6.0, \
            "COALESCE inside aggregate must substitute NULLs (36 / 6)"
    finally:
        conn.close()
    print("[OK] 06-aggregation: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. COUNT(*) counts rows; COUNT(col) counts non-NULL values")
        print("2. GROUP BY runs aggregates per group")
        print("3. WHERE filters rows, HAVING filters groups")
        print("4. AVG/SUM ignore NULLs unless you COALESCE them")
        _verify()          # always runs, so plain execution is also a test
