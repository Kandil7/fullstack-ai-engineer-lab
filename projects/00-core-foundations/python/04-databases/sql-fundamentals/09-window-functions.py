"""
SQL Fundamentals — 09: Window Functions
=========================================
Topics: OVER, PARTITION BY, ROW_NUMBER/RANK/DENSE_RANK, LAG/LEAD,
        running totals, frames

Why this matters for AI/backend engineering:
    Window functions compute per-group rankings, running totals, and
    previous-row values WITHOUT collapsing rows like GROUP BY. They are
    how eval systems rank models per dataset, how analytics compute
    cumulative metrics, and how feature pipelines build lag features.

Run:      python 09-window-functions.py
Verify:   python 09-window-functions.py --verify
Reference: https://www.sqlite.org/windowfunctions.html
"""

from __future__ import annotations

import sqlite3
import sys

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE evals (id INTEGER PRIMARY KEY, model TEXT, dataset TEXT, score REAL)")
conn.executemany(
    "INSERT INTO evals (model, dataset, score) VALUES (?, ?, ?)",
    [
        ("m1", "d1", 0.91), ("m1", "d2", 0.82),
        ("m2", "d1", 0.88), ("m2", "d2", 0.90),
        ("m3", "d1", 0.95), ("m3", "d2", 0.78),
    ],
)

# ============================================================
# 1. ROW_NUMBER() — rank WITHOUT ties
# ============================================================
print("=== 1. ROW_NUMBER ===")
rows = conn.execute(
    """
    SELECT model, dataset, score,
           ROW_NUMBER() OVER (PARTITION BY dataset ORDER BY score DESC) AS rn
    FROM evals
    ORDER BY dataset, rn
    """
).fetchall()
for r in rows:
    print(f"  {r[0]} on {r[1]}: {r[2]:.2f}  rank={r[3]}")
print("  -> per-dataset ranking; ties get distinct numbers")

# ============================================================
# 2. RANK vs DENSE_RANK — how ties are handled
# ============================================================
print("\n=== 2. RANK vs DENSE_RANK ===")
rows = conn.execute(
    """
    SELECT score,
           RANK() OVER (ORDER BY score DESC) AS rk,
           DENSE_RANK() OVER (ORDER BY score DESC) AS drk
    FROM (SELECT DISTINCT score FROM evals)
    ORDER BY score DESC
    """
).fetchall()
for r in rows:
    print(f"  score={r[0]:.2f}  rank={r[1]}  dense_rank={r[2]}")
print("  -> RANK skips numbers after ties; DENSE_RANK does not")

# ============================================================
# 3. LAG / LEAD — previous and next row
# ============================================================
print("\n=== 3. LAG / LEAD ===")
rows = conn.execute(
    """
    SELECT model, score,
           LAG(score) OVER (ORDER BY id) AS prev_score,
           LEAD(score) OVER (ORDER BY id) AS next_score
    FROM evals
    ORDER BY id
    """
).fetchall()
for r in rows:
    print(f"  {r[0]}: {r[1]:.2f}  prev={r[2] if r[2] is not None else '--':>5}  next={r[3] if r[3] is not None else '--':>5}")
print("  -> LAG/LEAD build lag features (time-series, deltas)")

# ============================================================
# 4. Running totals — cumulative sums with OVER
# ============================================================
print("\n=== 4. Running Total ===")
rows = conn.execute(
    """
    SELECT id, score,
           SUM(score) OVER (ORDER BY id) AS running_total
    FROM evals
    ORDER BY id
    """
).fetchall()
for r in rows:
    print(f"  id={r[0]}  score={r[1]:.2f}  running={r[2]:.2f}")
print("  -> no GROUP BY: every row survives, with its cumulative sum")

# ============================================================
# 5. Frames — the window inside the partition
# ============================================================
print("\n=== 5. Sliding Frame ===")
conn.execute("CREATE TABLE daily (day INTEGER PRIMARY KEY, metric REAL)")
conn.executemany("INSERT INTO daily (day, metric) VALUES (?, ?)",
                 [(1, 10.0), (2, 20.0), (3, 30.0), (4, 40.0), (5, 50.0)])
rows = conn.execute(
    """
    SELECT day, metric,
           AVG(metric) OVER (ORDER BY day ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS ma2
    FROM daily
    ORDER BY day
    """
).fetchall()
for r in rows:
    print(f"  day={r[0]}  metric={r[1]:.1f}  2-day MA={r[2]:.1f}")
print("  -> frame = rows 1 before through current: a moving average")

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: forgetting PARTITION BY -> one window over the whole table
# CORRECT: OVER (PARTITION BY dataset ...) for per-group windows
#
# MISTAKE: using ROW_NUMBER when ties should share a rank
# CORRECT: RANK() / DENSE_RANK() for tied scoring
#
# MISTAKE: thinking window functions collapse rows like GROUP BY
# CORRECT: they keep every row and ADD a computed column
#
# MISTAKE: ORDER BY inside OVER vs ORDER BY outside — different things
# CORRECT: OVER's ORDER BY defines the window order; the outer one sorts output

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE s (id INTEGER PRIMARY KEY, g TEXT, v INTEGER)")
        conn.executemany("INSERT INTO s (id, g, v) VALUES (?, ?, ?)",
                         [(1, "a", 30), (2, "a", 10), (3, "a", 10), (4, "b", 50)])

        # 1. ROW_NUMBER: unique per partition, no ties
        rows = conn.execute(
            "SELECT ROW_NUMBER() OVER (PARTITION BY g ORDER BY v DESC) FROM s ORDER BY id"
        ).fetchall()
        assert rows == [(1,), (2,), (3,), (1,)], \
            "ROW_NUMBER must be unique per partition (output ordered by id)"

        # 2. RANK vs DENSE_RANK with ties: RANK skips numbers after a tie
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v INTEGER)")
        conn.executemany("INSERT INTO t (id, v) VALUES (?, ?)",
                         [(1, 50), (2, 30), (3, 10), (4, 10), (5, 5)])
        rows = conn.execute(
            "SELECT DISTINCT RANK() OVER (ORDER BY v DESC), DENSE_RANK() OVER (ORDER BY v DESC) FROM t ORDER BY 1"
        ).fetchall()
        assert rows == [(1, 1), (2, 2), (3, 3), (5, 4)], \
            "tie at v=10: RANK skips 4, DENSE_RANK continues at 4"

        # 3. LAG/LEAD correctness
        rows = conn.execute(
            "SELECT LAG(v) OVER (ORDER BY id), LEAD(v) OVER (ORDER BY id) FROM s ORDER BY id"
        ).fetchall()
        assert rows[0] == (None, 10), "first row LAG must be NULL"
        assert rows[1] == (30, 10), "LAG must be the previous row's value"

        # 4. Running total keeps rows
        rows = conn.execute(
            "SELECT id, SUM(v) OVER (ORDER BY id) FROM s ORDER BY id"
        ).fetchall()
        assert [r[1] for r in rows] == [30, 40, 50, 100], "cumulative sums must accumulate"

        # 5. Frame: 2-day MA
        conn.execute("CREATE TABLE d (day INTEGER PRIMARY KEY, m REAL)")
        conn.executemany("INSERT INTO d (day, m) VALUES (?, ?)",
                         [(1, 10.0), (2, 20.0), (3, 30.0)])
        rows = conn.execute(
            "SELECT AVG(m) OVER (ORDER BY day ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) FROM d ORDER BY day"
        ).fetchall()
        assert rows == [(10.0,), (15.0,), (25.0,)], "frame MA must be (prev + cur) / 2"

        # 6. Partition isolation
        rows = conn.execute(
            "SELECT ROW_NUMBER() OVER (PARTITION BY g ORDER BY v DESC) FROM s WHERE g='b'"
        ).fetchall()
        assert rows == [(1,)], "each partition restarts numbering"
    finally:
        conn.close()
    print("[OK] 09-window-functions: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. OVER + PARTITION BY = per-group window without GROUP BY")
        print("2. ROW_NUMBER unique; RANK skips ties; DENSE_RANK doesn't")
        print("3. LAG/LEAD build lag features")
        print("4. Frames (ROWS BETWEEN) create moving averages")
        print("5. Window functions keep rows; GROUP BY collapses them")
        _verify()
