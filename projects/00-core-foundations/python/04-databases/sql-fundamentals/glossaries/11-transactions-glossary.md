# Transactions — Glossary 11

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| ACID | Properties | Atomicity, Consistency, Isolation, Durability |
| Atomicity | Properties | All-or-nothing: partial writes roll back |
| Autocommit | Engine | Each statement its own transaction (isolation_level=None) |
| BEGIN | Control | Starts a transaction explicitly |
| COMMIT | Control | Permanently applies the transaction |
| Consistency | Properties | Constraints stay satisfied before and after |
| Durability | Properties | Committed data survives crashes |
| Isolation | Properties | Concurrent transactions behave as if serialized |
| Locking | Concurrency | Writes block other writers until commit/rollback |
| Deferred | Control | Read-only until the first write (SQLite default) |
| Immediate | Control | Acquires a write reservation at BEGIN |
| WAL mode | Engine | journal_mode=WAL: concurrent readers + one writer |
| Write-ahead log | Engine | The journal file that enables WAL |
| Atomic commit | Engine | SQLite's all-or-nothing journal protocol |
| Two-phase | Theory | Prepare + commit phases of distributed transactions |
| Rollback | Control | Undoes everything since BEGIN |
| Savepoint | Control | A nested rollback point inside a transaction |
| Snapshot | Engine | WAL readers see a consistent point-in-time view |
| Exclusive | Control | Locks out readers and writers |
| Lock contention | Concurrency | Writers waiting on each other's locks |
| Integrity | Properties | The database is never left in a broken state |

## Detailed Definitions

### ACID
**Definition**: The four guarantees of transactions: Atomicity
(all-or-nothing), Consistency (constraints hold), Isolation
(concurrent transactions don't interfere), Durability (committed data
survives crashes).
**Related**: Atomicity, Durability

### Atomicity
**Definition**: Every statement in a transaction commits or none do. A
crash mid-way rolls back the whole unit.
**Example**:
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT UNIQUE)")
try:
    with conn:  # transaction block
        conn.execute("INSERT INTO t (v) VALUES (?)", ("a",))
        conn.execute("INSERT INTO t (v) VALUES (?)", ("a",))  # violates UNIQUE
except sqlite3.IntegrityError:
    pass
print(conn.execute("SELECT COUNT(*) FROM t").fetchone()[0])
```
```text
0
```
**Related**: Rollback, COMMIT

### Autocommit
**Definition**: `sqlite3.connect(..., isolation_level=None)` — every
statement commits immediately; there is no open transaction to
rollback. Useful for PRAGMA switches; dangerous for multi-step logic.
**Related**: BEGIN, COMMIT

### BEGIN / COMMIT / ROLLBACK
**Definition**: BEGIN opens a unit of work; COMMIT applies it
permanently; ROLLBACK discards it. Python's `with conn:` commits on
success and rolls back on exception.
**Example**:
```python
conn.execute("BEGIN")
conn.execute("INSERT INTO t (v) VALUES (?)", ("b",))
conn.execute("ROLLBACK")
print(conn.execute("SELECT COUNT(*) FROM t").fetchone()[0])
```
```text
0
```
**Related**: Atomicity, Savepoint

### Consistency
**Definition**: The database never transitions from one valid state to
an invalid one — constraints, FKs, and CHECKs hold at every commit.
**Related**: ACID, Atomicity

### Durability
**Definition**: Once committed, data survives crashes and restarts —
the commit marker is on disk before the transaction reports success.
**Related**: ACID, Write-ahead log

### Isolation
**Definition**: Concurrent transactions appear to run one after another;
the default (and WAL) behavior keeps readers from seeing partial
writes.
**Related**: ACID, WAL mode

### Locking
**Definition**: The mechanism enforcing serialized writes: a writer
holds the write lock until commit/rollback; a second writer waits
(BUSY/lock contention).
**Related**: Lock contention, Exclusive

### Deferred / Immediate
**Definition**: BEGIN DEFERRED (SQLite default): the transaction stays
read-only until the first write. BEGIN IMMEDIATE reserves the write
lock upfront — avoids deadlock-style upgrade waits.
**Related**: Locking, Lock contention

### WAL mode
**Definition**: `PRAGMA journal_mode=WAL` — writes append to a
write-ahead log instead of overwriting the database file: readers
never block, one writer proceeds.
**Example**:
```python
import tempfile, os
tmp = tempfile.NamedTemporaryFile(delete=False)
db_path = tmp.name
tmp.close()
conn = sqlite3.connect(db_path)
print(conn.execute("PRAGMA journal_mode=WAL").fetchone()[0])
conn.close()
for suffix in ("", "-wal", "-shm"):
    if os.path.exists(db_path + suffix):
        os.unlink(db_path + suffix)
```
```text
wal
```
**Related**: Snapshot, Write-ahead log

### Write-ahead log
**Definition**: The -wal file holding recent commits; checkpoints merge
it back into the main database file.
**Related**: WAL mode, Durability

### Rollback
**Definition**: Undoes all uncommitted changes since BEGIN — the "none"
half of all-or-nothing.
**Related**: Atomicity, Savepoint

### Savepoint
**Definition**: `SAVEPOINT name` marks a point; `ROLLBACK TO name` undoes
work after it while keeping earlier work — nested error recovery.
**Example**:
```python
conn.execute("BEGIN")
conn.execute("INSERT INTO t (v) VALUES (?)", ("c",))
conn.execute("SAVEPOINT sp1")
conn.execute("INSERT INTO t (v) VALUES (?)", ("d",))
conn.execute("ROLLBACK TO sp1")
conn.execute("COMMIT")
print(conn.execute("SELECT v FROM t ORDER BY v").fetchall())
```
```text
[('c',)]
```
**Related**: BEGIN, Rollback

### Snapshot
**Definition**: A WAL reader's consistent view: it sees the database
as of its start, regardless of later commits — read isolation without
locking.
**Related**: WAL mode, Isolation

### Exclusive
**Definition**: The strongest lock — blocks readers and writers; used
by schema changes and some PRAGMA operations.
**Related**: Locking, Deferred

### Lock contention
**Definition**: Time a writer spends waiting for another writer's lock
— visible as sqlite3.OperationalError: database is locked. Mitigate
with short transactions, retry/backoff, and WAL.
**Related**: Locking, WAL mode

### Integrity
**Definition**: The state of never exposing partial or corrupt results;
atomicity + constraints produce integrity.
**Related**: ACID, Consistency

## Key Concepts Summary

### The four guarantees
- Atomicity: all-or-nothing.
- Consistency: constraints hold at every boundary.
- Isolation: concurrent transactions behave serialized.
- Durability: committed data survives crashes.

### Control flow
- BEGIN / COMMIT / ROLLBACK; Python `with conn:` handles errors.
- Savepoints allow partial rollback.
- Autocommit mode: one transaction per statement.

### SQLite specifics
- Deferred by default; IMMEDIATE reserves the write lock.
- WAL: readers never block the writer; one writer at a time.
- Lock contention -> short transactions, retries, WAL.

## Practice Terms

Match each term to its definition.

1. Atomicity — ___
2. Savepoint — ___
3. WAL mode — ___
4. Snapshot — ___
5. Autocommit — ___
6. Locking — ___
7. Durability — ___
8. Deferred — ___

A. All-or-nothing execution
B. Nested rollback point
C. Concurrent readers + one writer
D. Consistent read view without blocking
E. One transaction per statement
F. Writers block writers until commit
G. Committed data survives crashes
H. Read-only until the first write

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H
