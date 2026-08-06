# Challenge 03: insert-update-delete — CRUD & UPSERT

## 🥉 Bronze — Batch Insert (~20 min)

**Task:** Implement `insert_models(conn, rows)` that inserts model
checkpoint rows with `executemany` and returns the rowcount.

**Signature:**
```python
def insert_models(conn: sqlite3.Connection, rows: list[tuple]) -> int:
```

**Requirements:**
- Table `models(id PK, name TEXT UNIQUE, epoch INT, metric REAL)`
  created by the function if missing
- Use `executemany` (one compile, many executions — never a loop)
- Return `cursor.rowcount`

**Constraints:** n ≤ 10⁴. Must use parameterized queries.

| Input | Expected |
|-------|----------|
| 3 rows | `3` |
| 0 rows | `0` |

---

## 🥈 Silver — Upsert Sync (~35 min)

**Task:** Implement `sync_models(conn, rows)` that upserts model records
by `name`: existing names update `epoch`/`metric`, new names insert.
Return the final list of `(name, epoch)` sorted by name.

**Signature:**
```python
def sync_models(conn: sqlite3.Connection, rows: list[tuple]) -> list[tuple]:
```

**Requirements:**
- `INSERT ... ON CONFLICT(name) DO UPDATE SET epoch=excluded.epoch,
  metric=excluded.metric`
- Idempotent: running twice yields the same result

**Constraints:** n ≤ 10⁴.

| Setup | Input | Expected |
|-------|-------|----------|
| `bert` at epoch 1 | `[('bert', 2), ('gpt', 1)]` | `[('bert', 2), ('gpt', 1)]` |
| Re-run same sync | same | unchanged (idempotent) |

---

## 🥇 Gold — RETURNING Changeset (~50 min)

**Task:** Implement `apply_changeset(conn, ops)` that executes a list of
operations — `("insert", name, epoch)`, `("update", name, epoch)`,
`("delete", name)` — and returns the ids of every row affected, in
operation order, using `RETURNING` where the DML supports it.

**Signature:**
```python
def apply_changeset(conn: sqlite3.Connection, ops: list[tuple]) -> list[int]:
```

**Requirements:**
- INSERT/UPDATE/DELETE each use `RETURNING id`
- Skip rows that don't exist on DELETE (no crash)
- Return affected ids in operation order

**Constraints:** n ≤ 10³ ops.

| Ops | Expected |
|-----|----------|
| insert a, insert b, update a, delete b | `[1, 2, 1, 2]`-shaped ids in order |

**Follow-up:** Why RETURNING instead of a second SELECT? (Answer: one
round trip, no window for drift between write and read, and the ids are
guaranteed to be the ones just written.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/03-insert-update-delete/test_challenge.py -v
```

## Test File Structure

```
challenges/03-insert-update-delete/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
