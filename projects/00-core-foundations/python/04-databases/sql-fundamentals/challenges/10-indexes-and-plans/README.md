# Challenge 10: indexes-and-plans — Plans & Index Strategy

## 🥉 Bronze — Plan Reader (~20 min)

**Task:** Implement `plan_for(conn, sql, params)` that returns the
EXPLAIN QUERY PLAN detail strings for a query, and
`sargable_vs_not(conn)` that creates a 5000-row `events(ts)` table with
an index and returns the plans for `ts >= ?` and `ts / 1000 >= ?`.

**Signature:**
```python
def plan_for(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[str]:
def sargable_vs_not(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- `plan_for` extracts only the plan `detail` (column 3)
- The sargable query must SEARCH; the wrapped query must SCAN
- Return `{"sargable": [...], "wrapped": [...]}`

**Constraints:** n ≤ 10⁴ rows.

| Query | Expected detail |
|-------|-----------------|
| `WHERE ts >= ?` | contains `SEARCH events USING INDEX` |
| `WHERE ts / 1000 >= ?` | contains `SCAN events` |

---

## 🥈 Silver — Covering Index (~35 min)

**Task:** Implement `covering_vs_table(conn)` on a
`events(id, model, latency, payload)` table: create index
`(model, latency)` and return the plans for
`SELECT model, latency WHERE model = ?` (covered) vs
`SELECT * WHERE model = ?` (table read).

**Signature:**
```python
def covering_vs_table(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Projected query plan must contain `COVERING INDEX`
- SELECT * plan must NOT contain `COVERING`
- Return `{"covering": [...], "star": [...]}`

**Constraints:** n ≤ 10⁴ rows.

| Query | Expected |
|-------|----------|
| `SELECT model, latency ...` | `SEARCH ... USING COVERING INDEX` |
| `SELECT * ...` | `SEARCH ... USING INDEX` (no COVERING) |

---

## 🥇 Gold — Index Strategist (~50 min)

**Task:** Implement `index_strategy(conn)` that, given the workload —
equality on `model`, range on `latency`, sort by `created_at`, and a
hot partial set `WHERE status = 'active'` — creates a composite index,
a dedicated `(model, created_at)` order index, then a partial index,
and returns the plans proving each query now SEARCHes (or uses an
index for the ORDER BY).

**Signature:**
```python
def index_strategy(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Composite index `(model, latency, created_at)` — equality, range, sort
- Dedicated `(model, created_at)` index so the ORDER BY avoids a temp sort
  (a range column in the middle of a composite blocks ORDER BY reuse)
- Partial index on `status` for `status = 'active'`
- Return `{"equality_range": [...], "order_by": [...], "partial": [...]}`
  with each plan SEARCHing (or using the index for ORDER BY)

**Constraints:** n ≤ 10⁴ rows.

| Query | Expected |
|-------|----------|
| `WHERE model = ? AND latency > ?` | `SEARCH ... idx_model_latency_created` |
| `ORDER BY created_at` (with model filter) | no `TEMP B-TREE` |
| `WHERE status = 'active'` | `SEARCH ... idx_active` (partial) |

**Follow-up:** Why partial index for the hot subset? (Answer: much
smaller B-tree — faster lookups and cheaper writes than indexing every
row.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/10-indexes-and-plans/test_challenge.py -v
```

## Test File Structure

```
challenges/10-indexes-and-plans/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
