# Challenge 11: transactions — Atomicity, Rollback, Savepoints

## 🥉 Bronze — Atomic Transfer (~20 min)

**Task:** Implement `atomic_transfer(conn, from_id, to_id, amount)` that
moves money between `accounts(id, balance)` inside ONE transaction and
returns the new balances. If any constraint fails, everything must roll
back (total balance invariant preserved).

**Signature:**
```python
def atomic_transfer(conn: sqlite3.Connection, from_id: int, to_id: int, amount: float) -> dict:
```

**Requirements:**
- Use a `CHECK (balance >= 0)`; a negative result raises and rolls back
- Return `{"from": balance, "to": balance}` after commit
- On failure, return `{"rolled_back": True, "total": original_total}`

**Constraints:** n ≤ 10³ accounts.

| Setup | Input | Expected |
|-------|-------|----------|
| a=100, b=0 | transfer 30 | `{"from": 70, "to": 30}` |
| a=100, b=0 | transfer 200 | rolled back; total still 100 |

---

## 🥈 Silver — All-or-Nothing Batch (~35 min)

**Task:** Implement `rollback_on_error(conn, ops)` that applies a list of
`(account_id, delta)` updates. If ANY update would make a balance
negative (CHECK violation), ALL updates roll back — no partial writes.

**Signature:**
```python
def rollback_on_error(conn: sqlite3.Connection, ops: list[tuple]) -> dict:
```

**Requirements:**
- One transaction; the first IntegrityError rolls back everything
- Return `{"applied": n, "final_balances": {...}}` on success, or
  `{"rolled_back": True, "final_balances": {...}}` on failure

**Constraints:** n ≤ 10³ ops.

| Setup | Ops | Expected |
|-------|-----|----------|
| a=100, b=50 | `[(1,-40),(2,-20)]` | applied 2; a=60, b=30 |
| a=100, b=50 | `[(1,-40),(2,-60)]` | rolled back; a=100, b=50 |

---

## 🥇 Gold — Savepoint Rescue (~50 min)

**Task:** Implement `savepoint_partial(conn, ops)` that processes a
list of `(account_id, delta)` ops with a SAVEPOINT before each op:
if an op violates the CHECK, roll back ONLY that op and continue; the
final state keeps every successful op.

**Signature:**
```python
def savepoint_partial(conn: sqlite3.Connection, ops: list[tuple]) -> dict:
```

**Requirements:**
- `SAVEPOINT s` / `ROLLBACK TO s` / `RELEASE s` per op
- Failed ops are skipped, successful ops persist
- Return `{"applied": n, "failed": n, "final_balances": {...}}`

**Constraints:** n ≤ 10³ ops.

| Setup | Ops | Expected |
|-------|-----|----------|
| a=100, b=50 | `[(1,-40),(2,-60),(1,-10)]` | applied 2, failed 1; a=50, b=50 |

**Follow-up:** Why does the failing op not kill the transaction?
(Answer: ROLLBACK TO a savepoint discards only work since that marker —
the surrounding transaction stays alive.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/11-transactions/test_challenge.py -v
```

## Test File Structure

```
challenges/11-transactions/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
