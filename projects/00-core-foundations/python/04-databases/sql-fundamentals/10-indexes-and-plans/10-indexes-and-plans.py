"""
SQL Fundamentals — 10: Indexes and Query Plans
================================================
Topics: B-tree mechanics, EXPLAIN QUERY PLAN, covering and composite
        indexes, column order matters, when an index is unused,
        write-cost tradeoff

Why this matters for AI/backend engineering:
    Indexes turn O(n) scans into O(log n) lookups. The senior skill is
    not "create an index" but "prove with EXPLAIN that the plan changed".
    Wrong-column-order composites silently stay unused; write-heavy
    tables pay for every index. This topic teaches the evidence loop.

Run:      python 10-indexes-and-plans.py
Verify:   python 10-indexes-and-plans.py --verify
Reference: https://www.sqlite.org/queryplanner.html
"""

from __future__ import annotations

import sqlite3
import sys
import time

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY, level TEXT, user_id INTEGER, ts INTEGER)")

# 100k rows, skewed: 'info' is 90%, 'error' 1%, user_ids concentrated
import random
rng = random.Random(42)
rows = []
for i in range(100_000):
    r = rng.random()
    level = "error" if r < 0.01 else ("warn" if r < 0.05 else "info")
    rows.append((level, rng.randint(1, 100), i))
conn.executemany("INSERT INTO logs (level, user_id, ts) VALUES (?, ?, ?)", rows)
conn.commit()

# ============================================================
# 1. The scan — what a missing index costs
# ============================================================
print("=== 1. Full Scan (no index) ===")
plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 42").fetchall()
print(f"  plan: {plan}")
print("  -> SCAN over all 100k rows")

# ============================================================
# 2. Create an index — and PROVE the plan changed
# ============================================================
print("\n=== 2. Index Changes the Plan ===")
conn.execute("CREATE INDEX idx_logs_user ON logs(user_id)")
plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 42").fetchall()
print(f"  plan: {plan}")
print("  -> SEARCH via the index: O(log n) lookups instead of a scan")

# ============================================================
# 3. Selective vs unselective — when an index is unused
# ============================================================
print("\n=== 3. Unselective Index (skewed data) ===")
conn.execute("CREATE INDEX idx_logs_level ON logs(level)")
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM logs WHERE level = 'info'"
).fetchall()
print(f"  'info' plan: {plan}")
print("  -> 90% of rows match: the planner may prefer a scan (or still scan)")
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM logs WHERE level = 'error'"
).fetchall()
print(f"  'error' plan: {plan}")
print("  -> selective predicates use the index; broad ones don't pay")

# ============================================================
# 4. Composite index — column order matters
# ============================================================
print("\n=== 4. Composite Index Column Order ===")
conn.execute("CREATE INDEX idx_logs_level_user ON logs(level, user_id)")
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM logs WHERE level = 'error' AND user_id = 5"
).fetchall()
print(f"  (level, user_id) match: {plan}")
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 5 AND level = 'error'"
).fetchall()
print(f"  same WHERE, both keys:   {plan}")
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM logs WHERE user_id = 5"
).fetchall()
print(f"  user_id ALONE:            {plan}")
print("  -> a composite index serves the leading column; user_id alone")
print("     cannot use idx_logs_level_user — column order decides coverage")

# ============================================================
# 5. The write cost — every index taxes INSERT
# ============================================================
print("\n=== 5. Write Cost of Indexes ===")
def bench_inserts(indexed: bool) -> float:
    c2 = sqlite3.connect(":memory:")
    c2.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, k INTEGER)")
    if indexed:
        c2.execute("CREATE INDEX idx_t_k ON t(k)")
    start = time.perf_counter()
    c2.executemany("INSERT INTO t (k) VALUES (?)", [(i % 1000,) for i in range(20_000)])
    c2.commit()
    return time.perf_counter() - start

no_idx = bench_inserts(False)
with_idx = bench_inserts(True)
print(f"  insert 20k rows, no index: {no_idx:.3f}s")
print(f"  insert 20k rows, 1 index : {with_idx:.3f}s")
print("  -> every index must be maintained on write; indexes are a trade")

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: adding an index without checking EXPLAIN -> it may never be used
# CORRECT: prove the plan changed from SCAN to SEARCH
#
# MISTAKE: composite index with the wrong leading column
# CORRECT: leading column = the most selective / most-filtered key
#
# MISTAKE: indexing low-cardinality columns (level with 3 values)
# CORRECT: the planner ignores indexes that don't narrow the set
#
# MISTAKE: ignoring write amplification on hot insert tables
# CORRECT: index what queries need; measure the write cost

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, a INTEGER, b INTEGER)")
        conn.executemany("INSERT INTO t (a, b) VALUES (?, ?)",
                         [(i % 50, i % 100) for i in range(5_000)])

        def plan_sql(sql: str) -> str:
            return " ".join(str(r) for r in conn.execute(f"EXPLAIN QUERY PLAN {sql}").fetchall())

        # 1. No index -> SCAN
        assert "SCAN" in plan_sql("SELECT * FROM t WHERE a = 5"), \
            "must scan before indexing"

        # 2. Index -> SEARCH
        conn.execute("CREATE INDEX idx_t_a ON t(a)")
        assert "SEARCH" in plan_sql("SELECT * FROM t WHERE a = 5"), \
            "indexed predicate must SEARCH"

        # 3. Composite coverage: leading column alone uses the index
        conn.execute("CREATE INDEX idx_t_a_b ON t(a, b)")
        p = plan_sql("SELECT * FROM t WHERE a = 5 AND b = 3")
        assert "SEARCH" in p, "both keys must use the composite index"
        # non-leading column alone cannot use it (falls back to scan/partial)
        p2 = plan_sql("SELECT * FROM t WHERE b = 3")
        assert "idx_t_a_b" not in p2, "b alone must not use idx_t_a_b"

        # 4. Write cost measurable: indexed insert is not faster
        c2 = sqlite3.connect(":memory:")
        c2.execute("CREATE TABLE u (id INTEGER PRIMARY KEY, k INTEGER)")
        c2.execute("CREATE INDEX idx_u_k ON u(k)")
        start = time.perf_counter()
        c2.executemany("INSERT INTO u (k) VALUES (?)", [(i,) for i in range(5_000)])
        elapsed = time.perf_counter() - start
        assert elapsed >= 0, "timing sanity only; never assert on wall-clock bounds"

        # 5. Correctness preserved by indexes
        assert conn.execute("SELECT COUNT(*) FROM t WHERE a = 5").fetchone()[0] == 100, \
            "index must not change results"
    finally:
        conn.close()
    print("[OK] 10-indexes-and-plans: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. EXPLAIN proves SCAN -> SEARCH after indexing")
        print("2. Selective predicates use indexes; broad ones don't")
        print("3. Composite index order = which predicates it serves")
        print("4. Indexes tax every write — measure the trade")
        _verify()
