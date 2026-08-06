# SQL Fundamentals — 11: Transactions

## Topic Overview

A transaction groups statements into an all-or-nothing unit: either every
statement applies or none does. This is the mechanism behind money transfers,
billing, usage accounting, and model-registry promotion — any invariant that
must never be observed half-written. ACID (Atomicity, Consistency, Isolation,
Durability) is the contract; isolation levels are the dial between
consistency and concurrency; savepoints give partial rollback; deadlocks are
the failure mode you design around.

The mental model: a transaction is a unit of **invariant preservation**.
Transfer = debit + credit; if the process dies between the two, the world must
see neither.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain ACID and why atomicity protects invariants.
2. Wrap multi-statement units in BEGIN/COMMIT.
3. ROLLBACK a failed transaction without partial writes.
4. Use SAVEPOINT for partial rollback.
5. Name the isolation levels and their anomaly tradeoffs.
6. Explain dirty read, non-repeatable read, and phantom.
7. Recognize and prevent deadlocks (consistent lock order).
8. Choose short transactions to limit lock contention.

## Prerequisites

| Need | Where |
|---|---|
| DML (UPDATE/INSERT/DELETE) | `03-insert-update-delete-lecture.md` |
| Error handling | `30-try-except.py` |

---

## 1. Atomicity — the transfer

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)")
conn.executemany("INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)",
                 [(1, "ada", 100), (2, "bob", 50)])

def transfer(from_id, to_id, amount):
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
    conn.commit()

transfer(1, 2, 30)
print(conn.execute("SELECT id, balance FROM accounts ORDER BY id").fetchall())
```

```
[(1, 70), (2, 80)]
```

Both statements commit together — the invariant `sum(balances) = 150` holds at
every observable moment. Without the transaction, a crash between the two
statements leaves money created or destroyed.

## 2. Rollback — undo on failure

```python
def risky_transfer(from_id, to_id, amount):
    try:
        conn.execute("BEGIN")
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
        if amount > 100:
            raise ValueError("amount exceeds limit")
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
        conn.commit()
        return "committed"
    except Exception as e:
        conn.rollback()
        return f"rolled back: {e}"
```

```
rolled back: amount exceeds limit
[(1, 70), (2, 80)]    # unchanged — the debit was undone
```

The debit happened, then the check failed — rollback erases the whole unit.
This is why transaction boundaries wrap *validation plus effects*: any failure
leaves the world untouched.

## 3. Savepoints — partial rollback

```python
conn.execute("BEGIN")
conn.execute("UPDATE accounts SET balance = balance + 10 WHERE id = 1")
conn.execute("SAVEPOINT after_credit")
conn.execute("UPDATE accounts SET balance = balance - 5 WHERE id = 1")
conn.execute("ROLLBACK TO after_credit")   # undo only the -5
conn.commit()
```

```
[(1, 75), (2, 80)]   # +10 kept, -5 undone
```

Savepoints let a long transaction abandon a sub-step without discarding
everything before it — useful for batch processing where one bad row should
not kill the batch.

## 4. Isolation levels — the consistency dial

| Level | Guarantee | Anomaly allowed |
|---|---|---|
| READ UNCOMMITTED | nothing | dirty reads |
| READ COMMITTED | only committed data | non-repeatable reads |
| REPEATABLE READ | stable per-transaction reads | phantoms |
| SERIALIZABLE | as if run alone | none |

- **Dirty read**: see another transaction's uncommitted write.
- **Non-repeatable read**: the same row reads differently twice in one
  transaction (committed elsewhere in between).
- **Phantom**: a new row matching your predicate appears mid-transaction.

sqlite defaults to SERIALIZABLE (single writer); Postgres defaults to READ
COMMITTED. The dial is always consistency vs concurrency.

## 5. Deadlock — the design-around

```text
Txn A: UPDATE acct 1 -> wants acct 2 (held by B)
Txn B: UPDATE acct 2 -> wants acct 1 (held by A)
```

Each waits on the other — the engine aborts one. Prevention:

1. Acquire locks in a **consistent global order** (always the lower ID first).
2. Keep transactions **short** — less time holding locks, less contention.
3. Retry the aborted transaction; deadlock is a race, not a bug in the data.

## Common Mistakes to Avoid

### Mistake 1: Autocommit for multi-statement invariants

```python
# WRONG - two autocommitted statements: a crash between them corrupts
# CORRECT - BEGIN/COMMIT around the unit, ROLLBACK on failure
```

### Mistake 2: Long transactions

```python
# WRONG - holding locks across a slow external call
# CORRECT - do slow work outside; keep transactions short
```

### Mistake 3: Ignoring the engine's default isolation

```python
# WRONG - assuming every DB behaves like sqlite's serializable
# CORRECT - know your engine; choose levels by anomaly tolerance
```

### Mistake 4: No retry on deadlock

```python
# WRONG - deadlock abort treated as data corruption
# CORRECT - retry the aborted transaction; deadlocks are expected races
```

### Mistake 5: Inconsistent lock order

```python
# WRONG - A locks (1, 2), B locks (2, 1): guaranteed deadlock under load
# CORRECT - a global order (ascending IDs) breaks the cycle
```

## Best Practices

1. Wrap every multi-statement invariant in a transaction.
2. Keep transactions short — do I/O outside them.
3. Rollback on any exception; never swallow partial state.
4. Use savepoints for batch sub-step isolation.
5. Know your engine's isolation default and its anomalies.
6. Acquire locks in a consistent global order.
7. Retry deadlock-aborted transactions with backoff.
8. Commit explicitly; never rely on implicit autocommit timing.
9. Test failure injection (crash between statements) for invariants.
10. Monitor lock-wait duration — the leading indicator of contention.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Transaction begin/commit | O(1) per unit | batch many rows per transaction |
| Lock holding | contention per duration | short transactions |
| Savepoint | O(1) | — |
| Serializable isolation | highest contention | READ COMMITTED where safe |
| Deadlock retry | one aborted unit | consistent lock order |

The cost of transactions is concurrency, not compute. Short, ordered, batched
transactions keep correctness without paying the contention price.

## AI Engineering Relevance

**Where this shows up:** usage metering, billing for LLM calls, model-registry
promotions (register + promote must be atomic), and eval-store updates.

| Concept here | Used for |
|---|---|
| Atomicity | billing a call and incrementing usage together |
| Rollback | undoing a failed model promotion |
| Savepoints | batch eval-ingestion with per-batch rollback |
| Isolation | consistent reads while ingestion writes |
| Lock order | avoiding deadlocks in multi-table accounting |

**Scale note:** at high write rates, the transaction shape decides throughput —
short transactions and batching are what keep a billing service at 10k
transactions/sec instead of 100.

## Practice Exercises

### Exercise 1: Atomic transfer  (Difficulty: Easy)
Write a transfer that preserves the total balance; assert the invariant after.

### Exercise 2: Rollback on failure  (Difficulty: Easy)
Trigger a failure mid-transaction; assert balances are unchanged.

### Exercise 3: Savepoint  (Difficulty: Medium)
Apply two changes, roll back only the second via a savepoint; assert the first
persisted.

### Exercise 4: Isolation knowledge  (Difficulty: Medium)
For each isolation level, name the anomaly it allows and one scenario where it
matters. Assert the mapping.

### Exercise 5: Batch with savepoints  (Difficulty: Hard)
Insert 100 rows; on any failure, roll back to the last savepoint and skip the
bad row; assert 99 committed.

### Exercise 6: Deadlock design  (Difficulty: Hard)
Model two transactions with opposite lock orders; show the cycle and the fix
(consistent order). Assert the fixed version never deadlocks in simulation.

## Summary

| Concept | Description |
|---|---|
| Atomicity | all-or-nothing units protect invariants |
| ROLLBACK | undo a failed transaction completely |
| SAVEPOINT | partial rollback within a transaction |
| Isolation | the consistency/concurrency dial |
| Anomalies | dirty reads, non-repeatable reads, phantoms |
| Deadlock | prevented by lock order and short transactions |

Transactions are the invariant-preservation machinery of SQL. The discipline:
wrap the whole unit, roll back on failure, keep it short, and order your locks.

## Quick Reference

| Task | Idiom |
|---|---|
| Begin | `BEGIN` / `conn.execute("BEGIN")` |
| Commit | `COMMIT` / `conn.commit()` |
| Undo all | `ROLLBACK` |
| Undo part | `SAVEPOINT sp` ... `ROLLBACK TO sp` |
| Check default | `PRAGMA isolation_level` / `SHOW transaction_isolation` |
| Deadlock fix | consistent lock order + retry |

## Next Steps

Next: **[12 — Normalization](12-normalization-lecture.md)** — designing schemas that
don't fight the invariants.

Continues in: **[04-databases — Postgres 05 Transactions MVCC](../../04-databases/postgres/lectures/05-transactions-mvcc-lecture.md)** — MVCC in a real engine.

Official docs: https://www.sqlite.org/lang_transaction.html
