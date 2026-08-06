# Session Lifecycle — Glossary 03

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| autoflush | Session | Queries flush pending changes first so they can see them |
| commit() | Session | Flush + COMMIT: the transaction ends and changes persist |
| detached | Session | An instance whose session is closed; expired attrs raise |
| DetachedInstanceError | Error | Raised when touching an expired attribute on a detached instance |
| expire | Session | Drops loaded attribute values so the next access reloads |
| expire_on_commit | Session | Commit drops attribute values by default (reload on access) |
| flush() | Session | Emits SQL inside the open transaction; rollback still possible |
| identity map | Session | One row -> one Python object per session |
| pending | Session | An added object with no SQL emitted yet |
| rollback() | Session | Undoes all pending work; the transaction boundary fails safe |
| session-per-request | Pattern | One session per request, closed in finally |
| Session | Session | Unit of Work + identity map + transaction boundary |
| unit of work | Session | The session tracking changes and deciding the SQL |
| transaction | Session | The open work unit; commit ends it, rollback discards it |
| get() | Session | Loads a row by primary key (identity-map aware) |
| add() | Session | Registers an object with the unit of work |
| scalars() | Session | Executes a select and unwraps ORM objects |

## Detailed Definitions

### autoflush
**Definition**: Before a query executes, the session flushes pending changes
so the query can see them — even without an explicit `flush()`. Predictable
unless you are deep in an initialization path (use `no_autoflush` then).
**Example**:
```python
with Session(bind=engine) as session:
    session.add(User(name="ada"))
    found = session.scalars(select(User).where(User.name == "ada")).first()
    print(found is not None)
# Output:
# True
```
**Related**: flush(), unit of work

### commit()
**Definition**: Flush + COMMIT. The transaction ends, changes persist, and
attributes are expired (unless `expire_on_commit=False`). The only verb that
persists.
**Example**:
```python
session.add(User(name="ada"))
session.commit()      # INSERT + COMMIT
print(session.get(User, 1).name)
# Output:
# ada
```
**Related**: flush(), rollback(), expire_on_commit

### detached
**Definition**: An instance whose session has been closed. The primary key
survives (it is identity, not state); expired attributes raise on access.
**Example**:
```python
u = User(name="ada"); session.add(u); session.commit(); session.close()
print(u.id)          # PK survives
# Output:
# 1
```
**Related**: DetachedInstanceError, expire

### DetachedInstanceError
**Definition**: Raised when code touches an expired attribute of a detached
instance. The classic "serialized the ORM object after the request" bug.
**Example**:
```python
try:
    _ = u.role        # expired + detached
except DetachedInstanceError as exc:
    print(type(exc).__name__)
# Output:
# DetachedInstanceError
```
**Related**: detached, expire

### expire
**Definition**: Drops an object's loaded attribute values; the next access
re-SELECTs them. `commit()` expires by default; you can expire explicitly.
**Related**: expire_on_commit, detached

### expire_on_commit
**Definition**: Session option (default True): commit drops attribute values
so the next access reloads. Hot read paths set it False to avoid surprise
SELECTs after commit.
**Example**:
```python
Session(bind=engine, expire_on_commit=False)
```
**Related**: commit(), expire

### flush()
**Definition**: Emits SQL (INSERT/UPDATE/DELETE) while the transaction stays
OPEN — rollback can still undo it. Needed when you want PKs before commit.
**Example**:
```python
user = User(name="ada"); session.add(user); session.flush()
print(user.id)        # PK assigned, transaction still open
# Output:
# 1
```
**Related**: commit(), autoflush, pending

### identity map
**Definition**: The session's dict from primary key to instance: loading the
same row twice returns the SAME object. Identity, not just equality.
**Example**:
```python
a = session.get(User, 1)
b = session.get(User, 1)
print(a is b)
# Output:
# True
```
**Complexity**: O(1) lookup.
**Related**: get(), Session

### pending
**Definition**: An object added to the session with no SQL emitted yet —
nothing exists in the DB until flush/commit.
**Related**: flush(), add()

### rollback()
**Definition**: Discards all pending work in the current transaction — the
transaction boundary fails safe. After a failed commit, rollback (or close)
before reusing the session.
**Example**:
```python
session.add(User(name="ghost")); session.rollback()
print(len(session.scalars(select(User).where(User.name == "ghost")).all()))
# Output:
# 0
```
**Related**: commit(), transaction

### session-per-request
**Definition**: The production pattern: one session per HTTP request, closed
in `finally`; never shared across requests or threads.
**Example**:
```python
def get_db():
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()
```
**Related**: Session, transaction

### Session
**Definition**: The ORM workhorse: Unit of Work + identity map + transaction
boundary. Created per request/operation; never at import time.
**Related**: unit of work, identity map, session-per-request

### unit of work
**Definition**: The session's tracking of added/mutated/deleted objects; at
flush it decides the exact SQL. You never write the statements.
**Related**: Session, flush()

### transaction
**Definition**: The open work unit on the session's connection. `commit()`
ends it permanently; `rollback()` discards it. One request = one transaction.
**Related**: commit(), rollback(), session-per-request

### get()
**Definition**: Loads a row by primary key, consulting the identity map
first — no SQL when the object is already loaded.
**Example**:
```python
user = session.get(User, 1)
```
**Related**: identity map

### add()
**Definition**: Registers an object (and its relationships) with the unit of
work. No SQL until flush/commit.
**Related**: pending, unit of work

### scalars()
**Definition**: Executes a `select()` and unwraps single-column results into
values or ORM objects.
**Example**:
```python
users = session.scalars(select(User)).all()
```
**Related**: Session, identity map

## Key Concepts Summary

### The Session as Transaction Boundary
- add -> pending; flush -> SQL inside the open transaction
- commit ends the transaction; rollback discards it
- one session per request, closed in finally

### Identity and Detachment
- identity map: one row -> one object
- PK survives detachment; expired attributes do not
- DetachedInstanceError is the serializer bug

### flush vs commit
- flush: SQL emitted, transaction open, rollback-able
- commit: flush + COMMIT + expiry
- autoflush makes queries see pending work

## Practice Terms

Match each term to its definition (answers at the bottom).

1. flush() — ___
2. identity map — ___
3. DetachedInstanceError — ___
4. pending — ___
5. session-per-request — ___
6. rollback() — ___

A) One row -> one Python object per session
B) SQL emitted, transaction still open
C) Touching an expired attribute after close
D) An added object with no SQL yet
E) Discards the current transaction's work
F) One session per request, closed in finally

**Answers:** 1-B, 2-A, 3-C, 4-D, 5-F, 6-E
