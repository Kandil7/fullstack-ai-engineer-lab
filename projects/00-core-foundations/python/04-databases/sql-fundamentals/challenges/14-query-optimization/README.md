# Challenge 14: query-optimization — Plans, Keyset, Batching

## 🥉 Bronze — Sargable Plan (~20 min)

**Task:** Implement `sargable_plan(conn)` that builds a 5000-row
`events(ts)` table with an index and returns the plan strings proving
`sargable` uses SEARCH while `wrapped` (function on the column) SCANs.

**Signature:**
```python
def sargable_plan(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- `EXPLAIN QUERY PLAN` for both predicates
- Return `{"sargable": [...], "wrapped": [...]}`

**Constraints:** n ≤ 10⁴ rows.

| Predicate | Expected |
|-----------|----------|
| `ts >= ?` | `SEARCH events USING INDEX` |
| `ts / 1000 >= ?` | `SCAN events` |

---

## 🥈 Silver — Keyset Page (~35 min)

**Task:** Implement `keyset_page(conn, after_id, limit)` returning the
next page of `events(id, name)` with `WHERE id > ? ORDER BY id LIMIT ?`,
plus the plan proving it SEARCHes the primary key.

**Signature:**
```python
def keyset_page(conn: sqlite3.Connection, after_id: int, limit: int) -> dict:
```

**Requirements:**
- Keyset pagination only — no OFFSET
- Return `{"rows": [(id, name)...], "plan": [strings]}`

**Constraints:** n ≤ 10⁴ rows.

| Input | Expected |
|-------|----------|
| `after_id=100, limit=3` | next 3 rows by id |
| `after_id=0, limit=2` | first 2 rows; plan contains SEARCH |

---

## 🥇 Gold — Batch Reader (~50 min)

**Task:** Implement `batch_fetch(conn, parent_ids, batch_size)` that
loads all children of the given parents with chunked IN queries
(max `batch_size` ids per query) and returns the children plus the
query count — proving batching beats N+1.

**Signature:**
```python
def batch_fetch(conn: sqlite3.Connection, parent_ids: list[int], batch_size: int) -> dict:
```

**Requirements:**
- Count executed queries with a wrapper around `conn.execute`
- Chunk `parent_ids` into slices of `batch_size`
- Return `{"rows": [(parent_id, child, value)...], "queries": n}`

**Constraints:** n ≤ 10⁴ children; `batch_size` ≥ 1.

| Setup | Input | Expected |
|-------|-------|----------|
| 5 parents, 3 children each | `(ids, 2)` | 15 rows; `queries == 3` (ceil(5/2)) |
| 5 parents | `(ids, 10)` | 15 rows; `queries == 1` |

**Follow-up:** Why not one query per parent? (Answer: 1 + 5 round trips
vs 3 — batching trades a bounded number of round trips for the whole
child set.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/14-query-optimization/test_challenge.py -v
```

## Test File Structure

```
challenges/14-query-optimization/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
