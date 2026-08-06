"""
Postgres — 04: Indexes
==============================================
Topics: B-tree, GIN, GiST, BRIN, Hash; partial and expression indexes; EXPLAIN; pg_stat_user_indexes

Why this matters for AI/backend engineering:
    Feature lookup, deduplication, and vector-adjacent metadata filters
    all live or die on index choice. A missing index turns an endpoint
    into a table scan; an unused index burns write latency and disk on
    every INSERT. The senior skill is reading the plan and the stats, not
    "adding indexes until it is fast."

Environment note:
    sqlite3 gives us real B-tree indexes, expression indexes, PARTIAL
    indexes (WHERE clause), and EXPLAIN QUERY PLAN — enough to teach
    every decision. Where sqlite's planner differs from Postgres (it
    uses indexes more eagerly on small tables), the file says so.
    GIN/GiST/BRIN/Hash are taught by decision rule and exercised in the
    guarded real-Postgres section.

Run:      python 04-indexes-postgres.py
Verify:   python 04-indexes-postgres.py --verify
Reference: https://www.postgresql.org/docs/current/indexes.html
"""

from __future__ import annotations

import os
import sqlite3
import sys


# ============================================================
# 1. The index menu — which access method for which query
# ============================================================
# B-tree: equality + range + ORDER BY (the default, 90% of cases)
# GIN:    containment: jsonb @>, array @>, full-text tsvector
# GiST:   geometric / range overlap, nearest-neighbour (also vector in PG16+)
# BRIN:   huge append-only tables, naturally sorted (logs, events)
# Hash:   equality only, rarely better than B-tree
# The rule: B-tree first; GIN for contains/array/jsonb; BRIN for
# append-only giants; Hash almost never.

# Example 1: before any index, a lookup is a full table SCAN
conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE events (
        id INTEGER PRIMARY KEY,
        tenant_id INTEGER NOT NULL,
        model TEXT NOT NULL,
        latency_ms REAL,
        created_at TEXT NOT NULL
    )
    """
)
conn.executemany(
    "INSERT INTO events (tenant_id, model, latency_ms, created_at) VALUES (?, ?, ?, ?)",
    [
        (t % 5, f"model-{t % 3}", float(t % 7) * 10.0, f"2026-08-{(t % 28) + 1:02d}T00:00:00Z")
        for t in range(12000)
    ],
)
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM events WHERE tenant_id = ?", (3,)
).fetchall()
print(f"1. before index: {plan}  <- SCAN, reads every row")
print()

# ============================================================
# 2. B-tree — the workhorse
# ============================================================
# A B-tree keeps keys sorted, so =, <, <=, >, >=, BETWEEN, and ORDER BY
# all use it. A composite B-tree index serves queries whose WHERE
# clauses use its columns left-to-right — equality first, then range,
# then sort. This order rule is the #1 interview question.

# Example 2: composite index (equality -> range)
conn.execute("CREATE INDEX idx_events_tenant_time ON events (tenant_id, created_at)")
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM events WHERE tenant_id = ? AND created_at > ?",
    (3, "2026-08-10T00:00:00Z"),
).fetchall()
print(f"2. composite index used: {any('idx_events_tenant_time' in str(r) for r in plan)}")
# ORDER BY created_at alone cannot use it: created_at is the SECOND key,
# so the planner must still sort (see the USE TEMP B-TREE step below).
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM events ORDER BY created_at"
).fetchall()
print("   ORDER BY created_at alone (needs the FIRST key for equality first):")
print("   ", plan)
print()

# ============================================================
# 3. Partial indexes — index only the rows that matter
# ============================================================
# CREATE INDEX ... ON t (col) WHERE <condition> shrinks the index to the
# hot subset: smaller, faster, cheaper to write. Postgres and sqlite3
# both support it. The classic ML example: index only ACTIVE feature
# rows, not the archived millions. Note: the planner needs the query
# predicate to IMPLY the index condition — use the same comparison.

# Example 3: partial index on the hot subset
conn.execute(
    """
    CREATE INDEX idx_events_active
    ON events (tenant_id)
    WHERE latency_ms > 500.0
    """
)
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM events WHERE latency_ms > 500.0 AND tenant_id = ?",
    (2,),
).fetchall()
print(f"3. partial index chosen for the hot subset: {any('idx_events_active' in str(r) for r in plan)}")
print("   plan:", plan)
print()

# ============================================================
# 4. Expression indexes — index what you query, not the raw column
# ============================================================
# WHERE lower(email) = ... cannot use an index on email. You index the
# EXPRESSION: CREATE INDEX ON users (lower(email)). Same for jsonb paths
# (seen in 03) and for mixed-case model names.

# Example 4: expression index on a transformed value
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT)")
conn.executemany(
    "INSERT INTO users (email) VALUES (?)",
    [(f"User{t}@Example.com",) for t in range(50)],
)
conn.execute("CREATE INDEX idx_users_email_lower ON users (lower(email))")
plan = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM users WHERE lower(email) = ?",
    ("user3@example.com",),
).fetchall()
print(f"4. expression index used: {any('idx_users_email_lower' in str(r) for r in plan)}")
print()

# ============================================================
# 5. Selectivity — the planner decides, not the index
# ============================================================
# An index exists does not mean the planner will use it: if a predicate
# matches most rows, reading most of the table through the index is
# slower than a straight scan. Postgres estimates row counts from
# ANALYZE statistics; sqlite's smaller cost model uses indexes more
# eagerly. The universal lesson: EXPLAIN on the REAL engine, keep
# statistics fresh with ANALYZE, and treat "add an index" as a
# hypothesis, not a fix.

# Example 5: same index, rare vs common value — read what the planner does
conn.execute("CREATE TABLE flags (id INTEGER PRIMARY KEY, flag INTEGER)")
conn.executemany(
    "INSERT INTO flags (flag) VALUES (?)",
    [(1,) for _ in range(95000)] + [(0,) for _ in range(5000)],
)
conn.execute("CREATE INDEX idx_flags_flag ON flags (flag)")
plan_common = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM flags WHERE flag = ?", (1,)
).fetchall()
plan_rare = conn.execute(
    "EXPLAIN QUERY PLAN SELECT id FROM flags WHERE flag = ?", (0,)
).fetchall()
print("5. flag=1 (95% of rows):", plan_common)
print("   flag=0 (5% of rows): ", plan_rare)
print("   sqlite uses the index for both here; on Postgres the 95% query")
print("   usually becomes a seq scan once ANALYZE updates the statistics.")
print()

# ============================================================
# 6. Unused indexes — the write-cost tradeoff
# ============================================================
# Every index slows INSERT/UPDATE/DELETE and eats disk. Postgres tracks
# usage in pg_stat_user_indexes: idx_scan = 0 means dead weight. Locally
# we replicate the audit: run the queries your app really runs and find
# the indexes no plan references.

# Example 6: audit which indexes the real query workload uses
conn.execute("CREATE TABLE features (id INTEGER PRIMARY KEY, model TEXT, is_active INTEGER, latency_ms REAL)")
conn.executemany(
    "INSERT INTO features (model, is_active, latency_ms) VALUES (?, ?, ?)",
    [("m" + str(t % 10), 1, float(t % 100)) for t in range(20000)],
)
conn.execute("CREATE INDEX idx_feat_model ON features (model)")
conn.execute("CREATE INDEX idx_feat_active ON features (model) WHERE is_active = 1")
conn.execute("CREATE INDEX idx_feat_never ON features (latency_ms)")  # no query uses it

workload = [
    ("SELECT id FROM features WHERE model = ?", ("m3",)),
    ("SELECT id FROM features WHERE is_active = 1 AND model = ?", ("m5",)),
]
candidates = ["idx_feat_model", "idx_feat_active", "idx_feat_never"]
referenced: set[str] = set()
for sql, params in workload:
    plan = conn.execute("EXPLAIN QUERY PLAN " + sql, params).fetchall()
    for idx in candidates:
        if any(idx in str(r) for r in plan):
            referenced.add(idx)
unused = [i for i in candidates if i not in referenced]
print(f"6. indexes referenced by the workload: {sorted(referenced)}")
print(f"   unused candidates (pg_stat_user_indexes.idx_scan = 0 analog): {unused}")
print()

# ============================================================
# 7. Real Postgres index zoo (guarded — skips when no server)
# ============================================================
def pg_demo() -> None:
    """Create GIN/GiST/BRIN/Hash indexes + read EXPLAIN; [skip] when down."""
    dsn = os.environ.get(
        "PGDSN", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    try:
        import psycopg
    except ImportError:
        print("[skip] psycopg not installed — pip install 'psycopg[binary]'")
        return
    try:
        with psycopg.connect(dsn, connect_timeout=1) as pg:
            with pg.cursor() as cur:
                cur.execute("CREATE TEMP TABLE docs (id int, tags text[], body text)")
                cur.execute("CREATE INDEX ON docs USING gin (tags)")
                cur.execute("CREATE INDEX ON docs USING gin (to_tsvector('english', body))")
                cur.execute("CREATE INDEX ON docs USING btree (id) WHERE id > 0")
                # EXPLAIN with BUFFERS proves plan + IO cost
                cur.execute(
                    "EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) "
                    "SELECT id FROM docs WHERE id = 1"
                )
                plan_json = cur.fetchone()[0][0]
                node = plan_json["Plan"]
                print(f"7. real EXPLAIN: node type={node['Node Type']}, "
                      f"actual rows={node['Actual Rows']}")
                # Unused-index audit — the pg_stat_user_indexes query
                cur.execute(
                    "SELECT indexrelname FROM pg_stat_user_indexes WHERE idx_scan = 0"
                )
                print("   indexes with idx_scan = 0:", [r[0] for r in cur.fetchall()])
    except Exception as exc:  # noqa: BLE001
        print(
            "[skip] real Postgres demo: %s -- requires a Postgres server "
            "(install: docker compose up -d postgres)" % exc
        )


pg_demo()
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: composite index (a, b) and then filtering on b alone -> the
#   index is useless for that query; CORRECT: separate (b) index
#
# MISTAKE: WHERE lower(email) = ... with index on email -> planner cannot
#   use it; CORRECT: index the expression lower(email)
#
# MISTAKE: partial index condition not implied by the query predicate ->
#   planner ignores it; CORRECT: match the comparison exactly
#
# MISTAKE: six indexes per table "just in case" -> write amplification
#   and disk bloat; CORRECT: measure idx_scan, drop zeros
#
# MISTAKE: B-tree for jsonb containment -> does not work; CORRECT: GIN

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Each concept gets its own table so the planner has ONE candidate.
    def _seed(
        conn: sqlite3.Connection, g: str = "g", v: str = "v"
    ) -> None:
        conn.execute(
            f"CREATE TABLE t (id INTEGER PRIMARY KEY, {g} TEXT, {v} REAL)"
        )
        conn.executemany(
            f"INSERT INTO t ({g}, {v}) VALUES (?, ?)",
            [(f"{g}{i % 4}", float(i) % 10.0) for i in range(12000)],
        )

    # 1. B-tree composite index serves prefix equality + range
    conn = sqlite3.connect(":memory:")
    try:
        _seed(conn)
        conn.execute("CREATE INDEX idx_t_g_v ON t (g, v)")
        plan = conn.execute(
            "EXPLAIN QUERY PLAN SELECT id FROM t WHERE g = ? AND v > ?",
            ("g1", 3.0),
        ).fetchall()
        assert any("idx_t_g_v" in str(r) for r in plan), \
            "composite index must be used for prefix equality + range"

        # 2. Partial index (only candidate) is used for its subset
        conn.execute("DROP INDEX idx_t_g_v")
        conn.execute("CREATE INDEX idx_t_big ON t (g) WHERE v > 5.0")
        plan = conn.execute(
            "EXPLAIN QUERY PLAN SELECT id FROM t WHERE v > 5.0 AND g = ?",
            ("g2",),
        ).fetchall()
        assert any("idx_t_big" in str(r) for r in plan), \
            "partial index must match the predicate"
    finally:
        conn.close()

    # 3. Expression index is used on the transformed value
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE u (id INTEGER PRIMARY KEY, email TEXT)")
        conn.executemany(
            "INSERT INTO u (email) VALUES (?)", [(f"U{i}@X.com",) for i in range(30)]
        )
        conn.execute("CREATE INDEX idx_u_lower ON u (lower(email))")
        plan = conn.execute(
            "EXPLAIN QUERY PLAN SELECT id FROM u WHERE lower(email) = ?",
            ("u1@x.com",),
        ).fetchall()
        assert any("idx_u_lower" in str(r) for r in plan), \
            "expression index must be used"
    finally:
        conn.close()

    # 4. Rare-value query uses the index; plans are deterministic
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE f (id INTEGER PRIMARY KEY, flag INTEGER)")
        conn.executemany(
            "INSERT INTO f (flag) VALUES (?)",
            [(1,) for _ in range(9500)] + [(0,) for _ in range(500)],
        )
        conn.execute("CREATE INDEX idx_f_flag ON f (flag)")
        plan_rare = conn.execute(
            "EXPLAIN QUERY PLAN SELECT id FROM f WHERE flag = ?", (0,)
        ).fetchall()
        plan_rare_2 = conn.execute(
            "EXPLAIN QUERY PLAN SELECT id FROM f WHERE flag = ?", (0,)
        ).fetchall()
        assert any("idx_f_flag" in str(r) for r in plan_rare), \
            "rare-value predicate must reference the index"
        assert str(plan_rare) == str(plan_rare_2), \
            "the planner must be deterministic for identical queries"
    finally:
        conn.close()

    # 5. Unused-index audit: workload query never touches idx_t_never
    conn = sqlite3.connect(":memory:")
    try:
        _seed(conn)
        conn.execute("CREATE INDEX idx_t_g_v ON t (g, v)")
        conn.execute("CREATE INDEX idx_t_never ON t (v)")
        plan = conn.execute(
            "EXPLAIN QUERY PLAN SELECT id FROM t WHERE g = ?", ("g1",)
        ).fetchall()
        assert any("idx_t_g_v" in str(r) for r in plan), \
            "workload query must use its index"
        assert not any("idx_t_never" in str(r) for r in plan), \
            "idx_t_never must appear in no plan (unused index)"

        # 6. ANALYZE runs and does not change the chosen plan
        conn.execute("ANALYZE")
        plan_after = conn.execute(
            "EXPLAIN QUERY PLAN SELECT id FROM t WHERE g = ? AND v > ?",
            ("g1", 3.0),
        ).fetchall()
        assert any("idx_t_g_v" in str(r) for r in plan_after), \
            "ANALYZE must not break the composite-index plan"
    finally:
        conn.close()

    print("[OK] 04-indexes-postgres: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. B-tree by default; GIN for containment; BRIN for giants")
        print("2. Composite index order: equality -> range -> sort")
        print("3. Partial indexes shrink to the hot subset")
        print("4. Expression indexes match transformed predicates")
        print("5. Read the plan on the real engine; ANALYZE; drop idx_scan = 0")
        _verify()          # always runs, so plain execution is also a test
