# Transactions — Glossary 11

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| ACID | Concept | Atomicity, Consistency, Isolation, Durability |
| Atomicity | ACID | All-or-nothing application of a unit |
| BEGIN | Mechanism | The statement starting a transaction |
| COMMIT | Mechanism | Making the transaction's changes permanent |
| Consistency | ACID | Invariants preserved across transactions |
| Deadlock | Failure | Two transactions each waiting on the other's lock |
| Dirty read | Anomaly | Reading another transaction's uncommitted write |
| Durability | ACID | Committed changes survive crashes |
| Isolation | ACID | Transactions do not interfere |
| Isolation level | Mechanism | The consistency/concurrency dial |
| Lock | Mechanism | The grant of exclusive access held by a transaction |
| Lock order | Design | The consistent global sequence of acquiring locks |
| Non-repeatable read | Anomaly | Same row reads differently within one transaction |
| Phantom | Anomaly | A new row appears matching a predicate mid-transaction |
| READ COMMITTED | Isolation | Sees only committed data; non-repeatable reads possible |
| REPEATABLE READ | Isolation | Stable reads; phantoms possible |
| ROLLBACK | Mechanism | Undoing the current transaction |
| SAVEPOINT | Mechanism | A marked point for partial rollback |
| SERIALIZABLE | Isolation | As if transactions ran alone |
| READ UNCOMMITTED | Isolation | May see uncommitted writes |

## Detailed Definitions

### ACID
**Definition**: The transaction contract — Atomicity, Consistency, Isolation,
Durability — guaranteeing that transactions preserve database invariants.
**Related**: Atomicity

### Atomicity
**Definition**: The ACID property that a transaction applies completely or not
at all — no partial writes observable.
**Related**: ROLLBACK

### BEGIN
**Definition**: The statement opening a transaction; all subsequent statements
are part of the unit until COMMIT or ROLLBACK.
**Example**:
```sql
BEGIN;
UPDATE accounts SET balance = balance - 30 WHERE id = 1;
COMMIT;
```
**Related**: COMMIT

### COMMIT
**Definition**: Making a transaction's changes permanent and releasing its
locks.
**Related**: BEGIN

### Consistency
**Definition**: The ACID property that transactions move the database between
valid states — every invariant holds before and after.
**Related**: ACID

### Deadlock
**Definition**: A cycle of lock waits — A holds what B wants and vice versa;
the engine aborts one transaction.
**Related**: Lock order

### Dirty read
**Definition**: Reading a row written by an uncommitted transaction — allowed
only at READ UNCOMMITTED.
**Related**: READ UNCOMMITTED

### Durability
**Definition**: The ACID property that committed changes survive crashes —
written to durable storage.
**Related**: ACID

### Isolation
**Definition**: The ACID property that concurrent transactions do not
interfere; dialed by isolation levels.
**Related**: Isolation level

### Isolation level
**Definition**: The setting controlling which anomalies a transaction may
observe — READ UNCOMMITTED to SERIALIZABLE.
**Related**: READ COMMITTED

### Lock
**Definition**: Exclusive access a transaction holds over rows/pages until it
ends — the source of contention and deadlock.
**Related**: Deadlock

### Lock order
**Definition**: The consistent global sequence of lock acquisition (e.g.
ascending IDs) that prevents deadlock cycles.
**Related**: Deadlock

### Non-repeatable read
**Definition**: The same row reading differently twice within one transaction
because another committed in between — allowed under READ COMMITTED.
**Related**: REPEATABLE READ

### Phantom
**Definition**: A new row matching the transaction's predicate appearing
mid-transaction — allowed under REPEATABLE READ.
**Related**: SERIALIZABLE

### READ COMMITTED
**Definition**: The isolation level seeing only committed data; non-repeatable
reads possible. Postgres' default.
**Related**: Non-repeatable read

### REPEATABLE READ
**Definition**: The isolation level with stable reads per transaction; phantom
rows possible.
**Related**: Phantom

### ROLLBACK
**Definition**: Undoing the current transaction — reverting every statement in
the unit.
**Example**:
```sql
BEGIN;
UPDATE ...;
ROLLBACK;
```
**Related**: SAVEPOINT

### SAVEPOINT
**Definition**: A marked point inside a transaction allowing
`ROLLBACK TO sp` to undo only the statements after it.
**Example**:
```sql
SAVEPOINT sp; UPDATE ...; ROLLBACK TO sp;
```
**Related**: ROLLBACK

### SERIALIZABLE
**Definition**: The strongest isolation — transactions behave as if run alone;
no anomalies, lowest concurrency.
**Related**: Phantom

### READ UNCOMMITTED
**Definition**: The weakest isolation — may read uncommitted writes (dirty
reads).
**Related**: Dirty read

## Key Concepts Summary

### The ACID contract
- Atomicity: all or nothing.
- Consistency: invariants preserved.
- Isolation: no interference.
- Durability: committed changes survive.

### The isolation dial
- READ UNCOMMITTED: dirty reads possible.
- READ COMMITTED: non-repeatable reads possible.
- REPEATABLE READ: phantoms possible.
- SERIALIZABLE: nothing.

### The design rules
- Short transactions: less contention.
- Consistent lock order: no deadlock cycles.
- Rollback on failure; savepoints for partial undo.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. All-or-nothing application — ___
2. Undoing the current transaction — ___
3. A marked point for partial rollback — ___
4. Reading an uncommitted write — ___
5. Two transactions waiting on each other's locks — ___
6. Sees only committed data — ___
7. A new row appearing mid-transaction — ___
8. The statement making changes permanent — ___

**Answers:** 1-atomicity, 2-ROLLBACK, 3-SAVEPOINT, 4-dirty read, 5-deadlock,
6-READ COMMITTED, 7-phantom, 8-COMMIT
