"""
SQL Fundamentals — 14: Query Optimization
============================================
Topics: Reading plans (EXPLAIN), sargable predicates, avoiding SELECT *,
keyset vs offset pagination, N+1 queries, batching

Why this matters for AI/backend engineering:
    The difference between a 5ms and a 5s query is rarely hardware — it is
    whether the query is *sargable* (index-usable), returns only the columns
    needed, and fetches rows in batches instead of one-by-one. N+1 query
    storms are the classic slow-path of every ORM-backed API and RAG
    pipeline that joins a collection to its embeddings.

Run:      python 14-query-optimization.py
Verify:   python 14-query-optimization.py --verify
Reference: https://www.sqlite.org/lang_explain.html
"""

from __future__ import annotations

import sqlite3
import sys
import time

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, user_id INTEGER, kind TEXT, ts REAL)")
conn.executemany(
    "INSERT INTO events (user_id, kind, ts) VALUES (?, ?, ?)",
    [(i % 50, "click" if i % 2 else "view", i * 0.01) for i in range(2_000)],
)
conn.execute("CREATE INDEX idx_events_user ON events(user_id)")

# ============================================================
# 1. Reading plans — EXPLAIN QUERY PLAN
# ============================================================
# The optimizer picks a strategy; the plan shows whether an index is used.
# "SEARCH ... USING INDEX" = good. "SCAN" = reads everything.

print("=== 1. Reading plans ===")
plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM events WHERE user_id = 7").fetchall()
print("indexed lookup :", plan[0][3])
plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM events WHERE kind = 'click'").fetchall()
print("no index      :", plan[0][3])
print()

# ============================================================
# 2. Sargable predicates — let the index work
# ============================================================
# Sargable = "Search ARGument ABLE": the indexed column stands alone on one
# side of the comparison. Wrapping it in a function kills the index.

def lookup_by_prefix(user_id_prefix: int) -> list:
    # NOT sargable: function around the indexed column
    return conn.execute(
        "SELECT id FROM events WHERE CAST(user_id AS TEXT) LIKE ?", (f"{user_id_prefix}%",)
    ).fetchall()


def lookup_by_range(lo: int, hi: int) -> list:
    # Sargable: bare column compared to bounds — index range scan
    return conn.execute(
        "SELECT id FROM events WHERE user_id >= ? AND user_id < ?", (lo, hi)
    ).fetchall()


plan_bad = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM events WHERE CAST(user_id AS TEXT) LIKE '1%'"
).fetchall()
plan_good = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM events WHERE user_id >= 10 AND user_id < 20"
).fetchall()
print("=== 2. Sargable predicates ===")
print("function-wrapped:", plan_bad[0][3])
print("bare comparison :", plan_good[0][3])
print(f"range scan returns {len(lookup_by_range(10, 20))} rows; prefix fn returns {len(lookup_by_prefix(1))}")
print()

# ============================================================
# 3. Avoid SELECT * — fetch only what you need
# ============================================================
# SELECT * drags every column across the wire and prevents covering-index
# optimization. Ask for the columns the code actually uses.

print("=== 3. Avoid SELECT * ===")
star = conn.execute("SELECT * FROM events WHERE user_id = 3 LIMIT 1").fetchone()
cols = conn.execute("SELECT id, kind FROM events WHERE user_id = 3 LIMIT 1").fetchone()
print(f"SELECT * -> {len(star)} columns fetched vs {len(cols)} needed")
print()

# ============================================================
# 4. Pagination — keyset vs offset
# ============================================================
# OFFSET pagination rescans and discards skipped rows each page (O(offset)).
# Keyset pagination remembers the last seen key and continues from there —
# an indexed range scan, O(page size).

def offset_page(limit: int, offset: int) -> list:
    return conn.execute(
        "SELECT id FROM events ORDER BY id LIMIT ? OFFSET ?", (limit, offset)
    ).fetchall()


def keyset_page(limit: int, after_id: int | None) -> list:
    if after_id is None:
        return conn.execute("SELECT id FROM events ORDER BY id LIMIT ?", (limit,)).fetchall()
    return conn.execute(
        "SELECT id FROM events WHERE id > ? ORDER BY id LIMIT ?", (after_id, limit)
    ).fetchall()


print("=== 4. Keyset vs offset pagination ===")
print(f"offset page 3 (LIMIT 50 OFFSET 100): first id={offset_page(50, 100)[0][0]}")
ks = keyset_page(50, 100)
print(f"keyset after id 100:                 first id={ks[0][0]}  (same page)")
print("keyset is an indexed range scan; offset re-scans skipped rows")
print()

# ============================================================
# 5. N+1 queries — fetch in bulk instead
# ============================================================
# N+1: one query for the list, then one query PER ROW. With N rows that is
# N+1 round trips. Fix: one query with a JOIN / IN-list.

def n_plus_1(user_ids: list[int]) -> int:
    """BROKEN pattern: per-row round trips. Returns rows counted."""
    total = 0
    for uid in user_ids:
        total += conn.execute("SELECT COUNT(*) FROM events WHERE user_id = ?", (uid,)).fetchone()[0]
    return total


def batched(user_ids: list[int]) -> int:
    """One round trip for the whole batch."""
    marks = ",".join("?" for _ in user_ids)
    return conn.execute(
        f"SELECT COUNT(*) FROM events WHERE user_id IN ({marks})", user_ids
    ).fetchone()[0]


ids = list(range(50))
start = time.perf_counter(); n1 = n_plus_1(ids); t_n1 = time.perf_counter() - start
start = time.perf_counter(); bt = batched(ids); t_batch = time.perf_counter() - start
print("=== 5. N+1 vs batching ===")
print(f"N+1  : {n1} rows in {t_n1*1000:.2f}ms ({len(ids)+1} round trips)")
print(f"batch: {bt} rows in {t_batch*1000:.2f}ms (1 round trip)")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: WHERE DATE(created_at) = 'today' — function around the column
#   disables the index; store/range over [start, next_day)
# CORRECT: created_at >= ? AND created_at < ?
#
# MISTAKE: LIMIT x OFFSET y on deep pages — the offset is re-scanned
# CORRECT: keyset pagination with WHERE id > last_id
#
# MISTAKE: looping a query inside a for loop (N+1)
# CORRECT: one IN-list / JOIN, then group in Python
#
# MISTAKE: SELECT * and filtering in application code
# CORRECT: select needed columns; push filters into SQL

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, cat TEXT, v INTEGER)")
        db.executemany("INSERT INTO items (cat, v) VALUES (?, ?)",
                       [("a", i) for i in range(10)] + [("b", i) for i in range(5)])
        db.execute("CREATE INDEX idx_items_cat ON items(cat)")

        # 1. Plan uses the index for a sargable predicate
        plan = db.execute(
            "EXPLAIN QUERY PLAN SELECT v FROM items WHERE cat = 'a'"
        ).fetchall()
        assert any("INDEX" in row[3] for row in plan), "indexed predicate must use the index"

        # 2. Function-wrapped predicate loses the index
        plan = db.execute(
            "EXPLAIN QUERY PLAN SELECT v FROM items WHERE upper(cat) = 'A'"
        ).fetchall()
        assert all("INDEX" not in row[3] for row in plan), \
            "function-wrapped predicate must not use the index"

        # 3. Keyset pagination returns exactly the offset page content
        db.executemany("INSERT INTO items (cat, v) VALUES ('c', ?)", range(20))
        page1 = db.execute("SELECT id FROM items ORDER BY id LIMIT 5").fetchall()
        page2 = db.execute("SELECT id FROM items ORDER BY id LIMIT 5 OFFSET 5").fetchall()
        keyset2 = db.execute(
            "SELECT id FROM items WHERE id > ? ORDER BY id LIMIT 5",
            (page1[-1][0],),
        ).fetchall()
        assert [r[0] for r in keyset2] == [r[0] for r in page2], \
            "keyset after last-id must equal the next offset page"

        # 4. IN-list batching equals per-row aggregation
        batch = db.execute(
            "SELECT COUNT(*) FROM items WHERE cat IN ('a', 'b')"
        ).fetchone()[0]
        assert batch == 15, "batched IN must count both categories"

        # 5. SELECT of needed columns has fewer fields than SELECT *
        row_star = db.execute("SELECT * FROM items LIMIT 1").fetchone()
        row_cols = db.execute("SELECT id, v FROM items LIMIT 1").fetchone()
        assert len(row_cols) < len(row_star), "projecting columns must fetch fewer"
    finally:
        db.close()
    print("[OK] 14-query-optimization: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. EXPLAIN QUERY PLAN shows whether the index is used")
        print("2. Sargable predicates keep the index; wrappers kill it")
        print("3. Project needed columns; never SELECT *")
        print("4. Keyset beats offset for deep pages")
        print("5. Batch with IN/JOIN instead of N+1 round trips")
        _verify()          # always runs, so plain execution is also a test
