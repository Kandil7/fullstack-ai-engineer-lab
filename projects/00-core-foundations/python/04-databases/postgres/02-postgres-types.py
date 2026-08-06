"""
Postgres — 02: Postgres Types
==============================================
Topics: JSONB, arrays, UUID, ENUM, NUMERIC vs float, TIMESTAMPTZ, ranges, text vs varchar

Why this matters for AI/backend engineering:
    Type choice is correctness: storing a probability or a price as float
    instead of NUMERIC loses digits; storing model metadata as a fixed
    column grid instead of JSONB forces a migration every time a model
    card gains a field. Feature stores, experiment trackers, and RAG
    metadata tables live or die on the types below.

Environment note:
    No Postgres server here, so the body uses sqlite3 (JSON stored via
    the JSON1 extension, timestamps as ISO text, UUID as TEXT). The real
    Postgres section at the end is guarded and prints [skip] without a
    server. Both teach the same decision rules.

Run:      python 02-postgres-types.py
Verify:   python 02-postgres-types.py --verify
Reference: https://www.postgresql.org/docs/current/datatype.html
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import uuid


# ============================================================
# 1. text vs varchar — the shortest-lived debate in Postgres
# ============================================================
# In Postgres, `text` and `varchar(n)` behave almost identically except
# varchar(n) enforces a length limit. Modern Postgres style: use `text`
# and put length limits in CHECK constraints or the application layer.
# In sqlite3 there is no difference at all (all are TEXT affinity).

# Example 1: varchar vs text are the same storage in sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE models (name text, provider varchar(20))")
conn.execute("INSERT INTO models (name, provider) VALUES (?, ?)", ("bert", "hf"))
print("1. text and varchar(n) both store:",
      conn.execute("SELECT name, provider FROM models").fetchone())
print()

# ============================================================
# 2. NUMERIC vs float — money and metrics must not drift
# ============================================================
# float is binary floating point: 0.1 is not exact. NUMERIC(10, 4) stores
# an exact decimal. Use NUMERIC for prices, billing, probabilities you
# must round-trip; use double precision for embeddings and distances
# where speed and range matter and tiny error is noise. sqlite3 has no
# NUMERIC storage — the exact-decimal lesson is shown in Python.

# Example 2: the 0.1 + 0.2 trap
print("=== 2. NUMERIC vs float ===")
print(f"float sum: 0.1 + 0.2 = {0.1 + 0.2!r}  <- not 0.3!")
from decimal import Decimal
exact = Decimal("0.1") + Decimal("0.2")
print(f"Decimal:   Decimal('0.1') + Decimal('0.2') = {exact}  <- exactly 0.3")
print()

# ============================================================
# 3. TIMESTAMPTZ — store instants, not wall clocks
# ============================================================
# Postgres TIMESTAMPTZ stores an instant in UTC and renders it in the
# session timezone. TIMESTAMP WITHOUT TIME ZONE stores whatever you gave
# it — ambiguous at DST boundaries. Golden rule: write UTC, store
# timestamptz, render in the client. sqlite3 has no date type; ISO-8601
# text sorted lexicographically IS a timestamp ordering.

# Example 3: ISO-8601 text sorts as time in sqlite3
conn.execute("CREATE TABLE runs (run_id INTEGER PRIMARY KEY, started_at TEXT)")
conn.executemany(
    "INSERT INTO runs (started_at) VALUES (?)",
    [("2026-08-06T10:15:30+00:00",), ("2026-08-05T23:59:59+00:00",)],
)
latest = conn.execute(
    "SELECT started_at FROM runs ORDER BY started_at DESC LIMIT 1"
).fetchone()[0]
print(f"3. lexicographic sort of ISO text finds latest: {latest}")
print()

# ============================================================
# 4. UUID — ids that survive sharding and merging
# ============================================================
# Serial ids leak row counts and collide when databases merge. UUIDs are
# 128-bit, merge-safe, and Postgres stores them in 16 bytes. UUIDv7 is
# time-ordered, so it also sorts by creation time (index-friendly). In
# sqlite3 we store the canonical 36-char text form.

# Example 4: generate and store a UUID
experiment_id = str(uuid.uuid4())
conn.execute("CREATE TABLE exps (exp_id TEXT PRIMARY KEY, name TEXT)")
conn.execute("INSERT INTO exps (exp_id, name) VALUES (?, ?)", (experiment_id, "exp-1"))
stored = conn.execute("SELECT exp_id FROM exps").fetchone()[0]
print(f"4. uuid stored as text, {len(stored)} chars, round-trip ok: {experiment_id == stored}")
print()

# ============================================================
# 5. JSONB — semi-structured model metadata
# ============================================================
# Postgres JSONB stores a binary, de-duplicated JSON document that can be
# indexed with GIN and queried with ->/->>. It is the type of choice for
# metadata that varies per row (model cards, hyperparameters, evaluation
# extras). sqlite3's JSON1 extension gives us the same operators.

# Example 5: JSON document column via JSON1
conn.execute(
    "CREATE TABLE model_cards (id INTEGER PRIMARY KEY, meta TEXT)"
)
card = {
    "model": "gpt-mini",
    "params": {"layers": 12, "heads": 8},
    "tags": ["lm", "deployable"],
    "score": 0.881,
}
conn.execute("INSERT INTO model_cards (meta) VALUES (?)", (json.dumps(card),))
layers = conn.execute(
    "SELECT json_extract(meta, '$.params.layers') FROM model_cards"
).fetchone()[0]
print(f"5. json_extract('$.params.layers') -> {layers} (JSONB-style path query)")
print()

# ============================================================
# 6. Arrays and ENUM — ordered lists and fixed vocabularies
# ============================================================
# Postgres arrays (TEXT[]) hold ordered values in one column; ENUM types
# (CREATE TYPE mood AS ENUM ('sad','ok','happy')) restrict values to a
# fixed vocabulary — safer than a typo-prone string. sqlite3 has neither:
# arrays are simulated with JSON arrays, enums with CHECK constraints.

# Example 6: enum via CHECK + array via JSON
conn.execute(
    """
    CREATE TABLE prompts (
        id INTEGER PRIMARY KEY,
        stage TEXT CHECK (stage IN ('draft', 'eval', 'prod')),
        labels TEXT
    )
    """
)
conn.execute(
    "INSERT INTO prompts (stage, labels) VALUES (?, ?)",
    ("eval", json.dumps(["toxic", "helpful"])),
)
stage, labels = conn.execute("SELECT stage, labels FROM prompts").fetchone()
print(f"6. enum-like stage={stage}, array-like labels={json.loads(labels)}")
try:
    conn.execute("INSERT INTO prompts (stage) VALUES (?)", ("produciton",))
    print("   CHECK failed to fire (unexpected)")
except sqlite3.IntegrityError:
    print("   CHECK constraint rejected 'produciton' - the ENUM point")
print()

# ============================================================
# 7. Ranges — intervals as first-class values
# ============================================================
# Postgres range types (tsrange, int4range) store an interval and answer
# "does X overlap this interval?" with an index. sqlite3 has no range
# type; the overlap logic is demonstrated in Python, the type decision
# taught for real Postgres.

# Example 7: interval overlap logic (what tsrange && tsrange does)
def overlaps(
    a_start: str, a_end: str, b_start: str, b_end: str
) -> bool:
    """Return True when [a_start, a_end) and [b_start, b_end) overlap."""
    return a_start < b_end and b_start < a_end


print(
    "7. tsrange overlap: [09:00,10:00) && [09:30,09:45) ->",
    overlaps("09:00", "10:00", "09:30", "09:45"),
)
print()

# ============================================================
# 8. Real Postgres type catalog (guarded — skips when no server)
# ============================================================
def pg_demo() -> None:
    """Query the real pg_type catalog; print [skip] when unavailable."""
    dsn = os.environ.get(
        "PGDSN", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    try:
        import psycopg
    except ImportError:
        print("[skip] psycopg not installed — pip install 'psycopg[binary]'")
        return
    try:
        with psycopg.connect(dsn, connect_timeout=1) as pg_conn:
            with pg_conn.cursor() as cur:
                # Types that ship with every Postgres (parametrized query!)
                cur.execute(
                    "SELECT typname FROM pg_type WHERE typname IN (%s, %s, %s) ORDER BY typname",
                    ("jsonb", "timestamptz", "uuid"),
                )
                rows = [r[0] for r in cur.fetchall()]
                print(f"8. built-in types confirmed: {rows}")
                # JSONB literal + ->/->> behave as documented
                cur.execute(
                    "SELECT %s::jsonb -> 'a' AS arrow, %s::jsonb ->> 'a' AS text_arrow",
                    ('{"a": 1}', '{"a": 1}'),
                )
                print("   jsonb -> gives jsonb, ->> gives text:", cur.fetchone())
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
# MISTAKE: DECIMAL-less float column for prices -> 0.1+0.2 rounding leaks
#   into billing; CORRECT: NUMERIC(10,2) for money
#
# MISTAKE: TIMESTAMP instead of TIMESTAMPTZ -> same instant renders
#   differently per server timezone; CORRECT: always timestamptz
#
# MISTAKE: serial id + merging two databases -> PK collisions
#   CORRECT: uuid (or uuidv7) primary keys
#
# MISTAKE: adding a column for every new hyperparameter -> ALTER TABLE
#   storm; CORRECT: JSONB metadata column + GIN index
#
# MISTAKE: varchar(255) everywhere out of MySQL habit -> pointless in PG
#   CORRECT: text, plus CHECK when a real limit exists

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    from decimal import Decimal

    # 1. float is inexact for 0.1 + 0.2; Decimal is exact
    assert 0.1 + 0.2 != 0.3, "float addition must be inexact for 0.1+0.2"
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3"), \
        "Decimal must be exact"

    # 2. ISO-8601 text orders as time (UTC offset preserved)
    with sqlite3.connect(":memory:") as c:
        c.execute("CREATE TABLE r (t TEXT)")
        c.executemany(
            "INSERT INTO r (t) VALUES (?)",
            [("2026-08-05T23:59:59+00:00",), ("2026-08-06T00:00:01+00:00",)],
        )
        last = c.execute("SELECT t FROM r ORDER BY t DESC LIMIT 1").fetchone()[0]
        assert last == "2026-08-06T00:00:01+00:00", "ISO text must sort as time"

    # 3. JSON1 path extraction reaches nested keys
    with sqlite3.connect(":memory:") as c:
        c.execute("CREATE TABLE m (id INTEGER PRIMARY KEY, meta TEXT)")
        c.execute("INSERT INTO m (meta) VALUES (?)",
                  (json.dumps({"params": {"layers": 12, "heads": 8}}),))
        layers = c.execute(
            "SELECT json_extract(meta, '$.params.layers') FROM m"
        ).fetchone()[0]
        assert layers == 12, "json_extract must reach nested paths"

    # 4. CHECK constraint enforces the enum vocabulary
    with sqlite3.connect(":memory:") as c:
        c.execute(
            "CREATE TABLE p (id INTEGER PRIMARY KEY, stage TEXT "
            "CHECK (stage IN ('draft', 'eval', 'prod')))"
        )
        try:
            c.execute("INSERT INTO p (stage) VALUES (?)", ("bad",))
            raised = False
        except sqlite3.IntegrityError:
            raised = True
        assert raised, "CHECK must reject out-of-vocabulary values"

    # 5. UUIDs are unique at scale and fixed-length text
    ids = {str(uuid.uuid4()) for _ in range(1000)}
    assert len(ids) == 1000, "UUIDs must not collide"
    assert all(len(i) == 36 for i in ids), "UUID text must be 36 chars"

    # 6. Range overlap semantics match tsrange && tsrange
    assert overlaps("09:00", "10:00", "09:30", "09:45") is True, \
        "contained interval must overlap"
    assert overlaps("09:00", "10:00", "10:00", "11:00") is False, \
        "half-open [start,end) intervals sharing an endpoint do not overlap"

    print("[OK] 02-postgres-types: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. text beats varchar(n) in Postgres; enforce limits with CHECK")
        print("2. NUMERIC for exact decimals, float for vectors and distances")
        print("3. timestamptz stores instants; write UTC everywhere")
        print("4. UUIDv7 ids survive merging and sharding")
        print("5. JSONB absorbs schema drift in model metadata")
        _verify()          # always runs, so plain execution is also a test
