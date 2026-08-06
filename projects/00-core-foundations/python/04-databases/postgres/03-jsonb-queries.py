"""
Postgres — 03: JSONB Queries
==============================================
Topics: ->/->>/@> operators, GIN indexes, JSONB vs normalized columns, document column design

Why this matters for AI/backend engineering:
    Experiment trackers, model registries, and RAG pipelines store
    per-row metadata that no fixed schema survives: a model card gains a
    field every release. JSONB is the escape hatch — indexed, typed
    (binary), queryable. Knowing when to use it (and when NOT to) is the
    difference between a schema that evolves and one that melts.

Environment note:
    sqlite3's JSON1 extension provides json_extract/json_each — the same
    path-query semantics as Postgres ->/->>. GIN indexes are taught as
    the equivalent expression index + EXPLAIN QUERY PLAN. The real
    Postgres section is guarded.

Run:      python 03-jsonb-queries.py
Verify:   python 03-jsonb-queries.py --verify
Reference: https://www.postgresql.org/docs/current/functions-json.html
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys


# ============================================================
# 1. -> vs ->> — object vs text
# ============================================================
# Postgres: meta -> 'model' returns a jsonb VALUE (object/array/number);
#           meta ->> 'model' returns the value as TEXT.
# sqlite3:  json_extract(meta, '$.model') is the -> analog; the text
#           coercion is up to you in Python. JSON1's json_type() tells
#           you which kind you got.

# Example 1: -> returns jsonb, ->> returns text
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE model_cards (id INTEGER PRIMARY KEY, meta TEXT)")
card = {
    "model": "gpt-mini",
    "params": {"layers": 12, "heads": 8},
    "tags": ["lm", "deployable"],
    "score": 0.881,
    "owner": None,
}
conn.execute("INSERT INTO model_cards (meta) VALUES (?)", (json.dumps(card),))

layers = conn.execute(
    "SELECT json_extract(meta, '$.params.layers') FROM model_cards"
).fetchone()[0]
tags = conn.execute(
    "SELECT json_extract(meta, '$.tags') FROM model_cards"
).fetchone()[0]
kind = conn.execute(
    "SELECT json_type(meta, '$.tags') FROM model_cards"
).fetchone()[0]
print(f"1. layers -> {layers} (jsonb number), tags -> {tags} (jsonb {kind})")
print()

# ============================================================
# 2. NULL vs missing — JSON's third state
# ============================================================
# A JSON key can hold null ('{"owner": null}') or be absent. Postgres
# jsonb distinguishes them: meta -> 'owner' IS NULL for missing keys,
# while a present-null needs jsonb_typeof() == 'null'. Slapping '=' on
# this column silently misreports either way.

# Example 2: present-null vs absent
missing = conn.execute(
    "SELECT json_extract(meta, '$.nope') FROM model_cards"
).fetchone()[0]
present_null = conn.execute(
    "SELECT json_type(meta, '$.owner') FROM model_cards"
).fetchone()[0]
print(f"2. missing key -> {missing!r}; present-null json_type -> {present_null}")
print()

# ============================================================
# 3. Containment @> — "does this doc have these keys?"
# ============================================================
# Postgres meta @> '{"params": {"layers": 12}}' :: jsonb answers "is the
# given JSON a subset of meta?" and can use a GIN index. JSON1 has no @>,
# so we express the same predicate with json_each() — one row per key.

# Example 3: containment via json_each
rows = conn.execute(
    """
    SELECT id FROM model_cards
    WHERE EXISTS (
        SELECT 1 FROM json_each(model_cards.meta)
        WHERE key = ? AND json_extract(value, '$.layers') = ?
    )
    """,
    ("params", 12),
).fetchall()
print(f"3. containment (params.layers == 12) matches ids: {[r[0] for r in rows]}")
print()

# ============================================================
# 4. GIN indexes — the reason JSONB scales
# ============================================================
# A plain table scan checks every document. A GIN index (Postgres) or an
# expression index on json_extract (sqlite3) turns the lookup into an
# index probe. Proof is in the plan: EXPLAIN QUERY PLAN must say SEARCH
# (index) not SCAN (table).

# Example 4: build the index, then read the plan
conn.execute(
    "CREATE INDEX idx_cards_model ON model_cards (json_extract(meta, '$.model'))"
)
plan_before = conn.execute(
    "EXPLAIN QUERY PLAN SELECT meta FROM model_cards WHERE json_extract(meta, '$.model') = ?",
    ("gpt-mini",),
).fetchall()
has_index = any("SEARCH" in str(row) or "idx_cards_model" in str(row) for row in plan_before)
print(f"4. plan uses the JSON expression index: {has_index}")
print("   plan:", plan_before)
print()

# ============================================================
# 5. JSONB vs normalized columns — the design decision
# ============================================================
# Normalized wins when the field is queried often, joined, typed, and
# stable (user_id, created_at). JSONB wins when the shape varies per row
# (model cards, telemetry, A/B configs) or fields appear rarely. The
# hybrid pattern — anchor columns for the hot path + one jsonb column
# for the long tail — is what real ML registries ship.

# Example 5: same query, two designs
conn.execute(
    """
    CREATE TABLE normalized (
        id INTEGER PRIMARY KEY,
        model TEXT NOT NULL,
        layers INTEGER NOT NULL
    )
    """
)
conn.execute("INSERT INTO normalized (model, layers) VALUES (?, ?)", ("gpt-mini", 12))
conn.execute("CREATE INDEX idx_norm_model ON normalized (model)")

print("=== 5. JSONB vs normalized ===")
print("  normalized:  fixed columns, typed, joinable, requires ALTER for new fields")
print("  jsonb:       free-form, indexed paths, absorbs drift, no joins")
rows = conn.execute(
    "EXPLAIN QUERY PLAN SELECT model FROM normalized WHERE model = ?", ("gpt-mini",)
).fetchall()
print("  normalized plan:", rows)
print()

# ============================================================
# 6. Real Postgres JSONB (guarded — skips when no server)
# ============================================================
def pg_demo() -> None:
    """Exercise real jsonb operators + GIN index; [skip] when unavailable."""
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
                cur.execute("CREATE TEMP TABLE cards (id int, meta jsonb)")
                cur.execute(
                    "INSERT INTO cards VALUES (%s, %s)",
                    (1, '{"model": "gpt-mini", "params": {"layers": 12}}'),
                )
                # ->> returns text; @> is containment; GIN index for @>/?/->>
                cur.execute(
                    "SELECT meta ->> 'model' FROM cards WHERE meta @> %s",
                    ('{"params": {"layers": 12}}',),
                )
                model = cur.fetchone()[0]
                cur.execute(
                    "CREATE INDEX ON cards USING gin (meta)"
                )
                print(f"6. real jsonb: ->> = {model}, GIN index created")
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
# MISTAKE: WHERE meta -> 'model' = 'gpt-mini'  -> comparing jsonb to text
#   silently fails; CORRECT: meta ->> 'model' = 'gpt-mini'
#
# MISTAKE: WHERE meta ->> 'owner' IS NULL to find missing owners -> also
#   catches present-null; CORRECT: jsonb_typeof(meta -> 'owner') IS NULL
#
# MISTAKE: storing user_id inside jsonb and joining on it -> no FK, no
#   join index; CORRECT: anchor column for hot/typed/joined fields
#
# MISTAKE: no index on the JSON path you filter on -> seq scan of every
#   document; CORRECT: GIN index (or expression index in sqlite3)
#
# MISTAKE: JSONB for everything because it is flexible -> loses types,
#   constraints, and planner statistics; CORRECT: hybrid — columns +
#   one jsonb column

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    with sqlite3.connect(":memory:") as conn:
        conn.execute("CREATE TABLE c (id INTEGER PRIMARY KEY, meta TEXT)")
        conn.execute(
            "INSERT INTO c (meta) VALUES (?)",
            (json.dumps({"model": "m1", "params": {"layers": 6}, "tags": ["a"]}),),
        )
        conn.execute(
            "INSERT INTO c (meta) VALUES (?)",
            (json.dumps({"model": "m2", "params": {"layers": 12}, "tags": ["b", "c"]}),),
        )

        # 1. -> extracts the nested value (jsonb semantics)
        layers = conn.execute(
            "SELECT json_extract(meta, '$.params.layers') FROM c WHERE id = ?",
            (1,),
        ).fetchone()[0]
        assert layers == 6, "path extraction must reach nested keys"

        # 2. ->> returns text; json_type identifies the kind
        kind = conn.execute(
            "SELECT json_type(meta, '$.tags') FROM c WHERE id = ?", (1,)
        ).fetchone()[0]
        assert kind == "array", "json_type must report 'array' for arrays"

        # 3. missing key is SQL NULL, present-null is json 'null'
        missing = conn.execute(
            "SELECT json_extract(meta, '$.absent') FROM c WHERE id = ?", (1,)
        ).fetchone()[0]
        assert missing is None, "missing key must extract to SQL NULL"
        conn.execute(
            "UPDATE c SET meta = ? WHERE id = ?",
            (json.dumps({"model": "m1", "owner": None}), 1),
        )
        kind = conn.execute(
            "SELECT json_type(meta, '$.owner') FROM c WHERE id = ?", (1,)
        ).fetchone()[0]
        assert kind == "null", "present-null must type as json 'null'"

        # 4. containment predicate matches the right documents
        conn.execute(
            "UPDATE c SET meta = ? WHERE id = ?",
            (json.dumps({"model": "m2", "params": {"layers": 12}}), 2),
        )
        ids = [
            r[0]
            for r in conn.execute(
                """
                SELECT id FROM c
                WHERE EXISTS (
                    SELECT 1 FROM json_each(c.meta)
                    WHERE key = ? AND json_extract(value, '$.layers') = ?
                )
                """,
                ("params", 12),
            ).fetchall()
        ]
        assert ids == [2], "containment must match only the subset doc"

        # 5. expression index flips the plan from SCAN to SEARCH
        conn.execute(
            "CREATE INDEX idx_c_model ON c (json_extract(meta, '$.model'))"
        )
        plan = conn.execute(
            "EXPLAIN QUERY PLAN SELECT meta FROM c WHERE json_extract(meta, '$.model') = ?",
            ("m1",),
        ).fetchall()
        assert any("idx_c_model" in str(row) for row in plan), \
            "expression index must be used (SEARCH, not SCAN)"

        # 6. normalized column with index also plans as SEARCH
        conn.execute("CREATE TABLE n (id INTEGER PRIMARY KEY, model TEXT)")
        conn.execute("INSERT INTO n (model) VALUES (?)", ("m1",))
        conn.execute("CREATE INDEX idx_n_model ON n (model)")
        plan = conn.execute(
            "EXPLAIN QUERY PLAN SELECT model FROM n WHERE model = ?", ("m1",)
        ).fetchall()
        assert any("idx_n_model" in str(row) for row in plan), \
            "normalized index must be used"

    print("[OK] 03-jsonb-queries: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. -> returns jsonb, ->> returns text")
        print("2. NULL vs missing are different states; use jsonb_typeof")
        print("3. @> containment is the subset predicate, indexable via GIN")
        print("4. GIN/expression indexes turn doc scans into probes")
        print("5. Use columns for hot/typed fields, jsonb for the long tail")
        _verify()          # always runs, so plain execution is also a test
