# Databases (SQLAlchemy) — 03: Session Lifecycle

## Topic Overview

The `Session` is the heart of the ORM: it is the **Unit of Work** (it tracks
every object you add or mutate and decides what SQL to emit), the **identity
map** (one row maps to one Python object), and the **transaction boundary**
(everything inside one session is one transaction). Understanding the Session
is what separates "I wrote code that mostly works" from "I know exactly what
SQL ran and when."

For AI/backend engineers the Session is the transaction boundary of every
request: in a FastAPI/Django service it wraps the train/eval metadata writes,
and in ML tooling it wraps experiment-tracking inserts. Misunderstanding
`flush` vs `commit` causes the classic "I committed but the row is gone"
and `DetachedInstanceError` in serializers. The identity map is why loading
the same row twice gives you the *same* object — the reason `==` (and even
`is`) works on ORM instances at all.

This lecture covers the Unit of Work, the identity map, `flush` vs `commit`,
expiry and detachment, and the session-per-request pattern that production
services use.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the Session as Unit of Work: what it tracks and when it emits SQL
2. Use the identity map to reason about object identity across loads
3. Distinguish `flush()` (SQL emitted, transaction open) from `commit()` (persisted)
4. Predict what a query inside a session sees before commit (autoflush)
5. Explain expiry (`expire_on_commit`) and why attributes reload lazily
6. Recognize detached instances and predict `DetachedInstanceError`
7. Know which attributes survive detachment (the primary key)
8. Implement the session-per-request pattern with guaranteed close
9. Use rollback to leave the database exactly as it was
10. Debug the classic "row is gone" and "detached instance" failures

---

## Prerequisites

| Need | Where |
|---|---|
| Mapped models | `02-declarative-models-lecture.md` |
| Core transactions | `01-core-vs-orm-lecture.md` |
| Generators (`yield`) | `02-advanced-python/lectures/02-generators-lecture.md` |

---

## 1. The Unit of Work

You add objects and mutate attributes; the Session decides what to
INSERT/UPDATE/DELETE at flush time. You never write the SQL. A mutation
followed by a commit results in one INSERT — the change is folded in, not
written twice.

```python
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), default="annotator")

Base.metadata.create_all(engine)

with Session(bind=engine) as session:
    ada = User(name="ada", role="annotator")
    session.add(ada)          # pending: no SQL yet
    ada.role = "reviewer"     # still pending; change is tracked
    session.commit()          # INSERT users ... (with the final role)
    print(f"committed user id={ada.id} role={ada.role}")
# Output:
# committed user id=1 role=reviewer
```

## 2. The Identity Map

Within a session, a primary key maps to exactly **one** instance. Loading the
same row twice returns the same object — identity, not just equality. This
makes `a is b` true and prevents the ORM from materializing conflicting copies
of the same row.

```python
with Session(bind=engine) as session:
    first = session.get(User, 1)
    second = session.get(User, 1)   # no SQL: served from the identity map
    print(f"same object: {first is second}")
# Output:
# same object: True
```

Two **different** sessions have two different identity maps: the same row is
two objects (`is` is False), even though both represent the same database row.

## 3. flush vs commit

- `flush()` — emit SQL to the database; the transaction stays **open**, so
  `rollback()` can still undo it.
- `commit()` — flush, then `COMMIT` (transaction ends), then expire attributes.

Autoflush: any query inside the session flushes pending changes first, so the
query can see them — even before you call `flush()` yourself.

```python
with Session(bind=engine) as session:
    grace = User(name="grace")
    session.add(grace)
    session.flush()                        # INSERT issued NOW
    found = session.scalars(
        select(User).where(User.name == "grace")
    ).first()
    print(f"flush-then-query found pending row: {found is grace}")
    session.rollback()                     # undo the INSERT
# Output:
# flush-then-query found pending row: True
```

Without a flush (or commit), the query would not see the pending row — and a
rollback leaves the database exactly as it was:

```python
with Session(bind=engine) as session:
    ghost = User(name="ghost")
    session.add(ghost)
    session.rollback()
print(f"ghost rows after rollback: {len(
    Session(bind=engine).scalars(select(User).where(User.name == "ghost")).all())}")
# Output:
# ghost rows after rollback: 0
```

## 4. Expiry and Detached Instances

`commit()` expires loaded attributes (`expire_on_commit=True` is the default):
their values are dropped so the next access reloads fresh from the DB. That
reload needs a live session. Once the session is **closed**, the instance is
**detached** — and touching an expired attribute raises
`DetachedInstanceError`.

```python
def detached_error_demo(name: str) -> str:
    session = Session(bind=engine)
    u = User(name=name)
    session.add(u)
    session.commit()          # expiry: attribute values dropped
    session.close()           # now u is detached
    try:
        _ = u.role            # expired + detached -> DetachedInstanceError
    except Exception as exc:
        return type(exc).__name__
    return "no error"

print(f"detached expired attribute -> {detached_error_demo('bob')}")
# Output:
# detached expired attribute -> DetachedInstanceError
```

The **primary key survives detachment**: it is the object's identity, not an
expired value. That is why you can pass ids around safely after a session
closes.

```python
with Session(bind=engine) as session:
    u = session.get(User, 1)
    pk = u.id
    session.close()
print(f"pk readable while detached: {pk}")
# Output:
# pk readable while detached: 1
```

## 5. Session-per-Request (FastAPI Pattern)

Production services create **one session per HTTP request**, close it in a
`finally` block, and never share sessions across requests or threads. Each
request gets its own transaction boundary.

```python
def get_db():
    """FastAPI dependency generator: one session per request."""
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()  # guaranteed: no leaked connections

def handle_request(session: Session, name: str) -> int:
    user = User(name=name)
    session.add(user)
    session.commit()
    return user.id  # PK survives commit expiry; no refresh needed
```

Two simulated requests write independently; both rows persist, each in its own
transaction.

## 6. Production Pattern: Rollback on Failure

The transaction boundary also means: when a request fails, `rollback()` leaves
the database exactly as it was — no half-written experiments, no ghost rows.
This is the guarantee tests exploit (topic 09) and services rely on.

```python
def guarded_write(session: Session, name: str, fail: bool) -> int | None:
    user = User(name=name)
    session.add(user)
    if fail:
        session.rollback()
        return None
    session.commit()
    return user.id
```

---

## Common Mistakes to Avoid

### Mistake 1: Holding one session for the whole app
```
# WRONG — shared session: identity map leaks, stale reads, thread chaos
session = Session(bind=engine)          # created once at import time
# CORRECT — one per request, closed in finally
def get_db():
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()
```

### Mistake 2: Serializing ORM objects after the session closed
```
# WRONG — DetachedInstanceError in the serializer
data = {"name": user.name}              # after session.close()
# CORRECT — serialize inside the session, or re-load with session.get
```

### Mistake 3: Assuming flush() persists
```
# WRONG — "I flushed, why is the row gone in the other process?"
session.flush()                          # SQL sent, transaction OPEN
# CORRECT — commit() ends the transaction
session.commit()
```

### Mistake 4: Catching IntegrityError and continuing on the same session
```
# WRONG — session is in a failed state; later writes misbehave
try:
    session.commit()
except IntegrityError:
    session.add(other)                   # poisoned transaction
# CORRECT — rollback (or close) before reusing
except IntegrityError:
    session.rollback()
```

### Mistake 5: Forgetting autoflush surprises with bulk operations
```
# WRONG — pending objects flushed mid-query; rows "appear" unexpectedly
session.add(u); session.scalars(select(User)).all()   # autoflush fires first
# CORRECT — commit/flush before the read if that is the intent
```

---

## Best Practices

1. One session per request/operation; close it in `finally`
2. Never share a session across threads or async tasks
3. Let `commit()` be the only "persist" verb in service code
4. Use `flush()` when you need the PK before commit (e.g., graph writes)
5. Keep the identity map small: `expunge_all()` before long-running reads
6. Return PKs from handlers, not detached objects
7. Roll back and close after any exception involving the session
8. Rely on the transaction boundary: failures leave no partial state
9. Serialize inside the session scope; never after close
10. Test commit/rollback semantics explicitly (challenge 03 does exactly this)

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Identity map lookup | O(1) | O(active objects) | — (it is the point) |
| flush() of N dirty objects | O(N) SQL work | O(N) | batch operations for bulk |
| Lazy reload after expiry | 1 extra SELECT | O(1) | `expire_on_commit=False` |
| Session close | O(1) | releases objects | — |

**Cost note:** expiry costs a SELECT per touched attribute on a *new* session —
for hot read paths set `expire_on_commit=False` or re-query once. The identity
map's memory grows with the objects you keep alive; long jobs should commit
and `expunge` periodically.

---

## AI Engineering Relevance

**Where this shows up:** every FastAPI endpoint that records a training run,
stores an eval metric, or registers a model version runs inside one session.
Experiment-tracker backends are literally "session-per-request over a metadata
DB".

| Concept here | Used for |
|---|---|
| Unit of Work | one endpoint writing experiment + metrics + tags atomically |
| flush() | assigning ids mid-graph (experiment -> children) |
| identity map | caching loaded rows within a request |
| DetachedInstanceError | the serializer bug that bites every API at some point |
| rollback boundary | failed eval writes leave no partial rows |

**Scale note:** at 200 concurrent requests, session-per-request plus
connection pooling is what keeps the DB sane. At 1M rows, keeping sessions
short (commit + close fast) is what keeps the identity map from eating memory.

---

## Practice Exercises

### Exercise 1: Trace the SQL (Difficulty: Easy)
Using the `User` model, add a user, change the role, and commit. Print the
final role. Then predict: how many INSERT statements ran? (Answer: one.)

### Exercise 2: Identity Across Sessions (Difficulty: Easy)
Load `User` 1 in two separate sessions. Print `a is b` and `a == b`. Explain
why they differ.

### Exercise 3: Flush for PKs (Difficulty: Medium)
Create two users where the second must reference the first's `id`. Use
`flush()` to obtain the first id, then build the second. Commit once.

### Exercise 4: Detachment Boundaries (Difficulty: Medium)
Write a function that commits, closes, and returns `(user.id, user.role)`
inside a try/except. Confirm the id works and the role raises
`DetachedInstanceError`.

### Exercise 5: Request Failure Simulation (Difficulty: Hard)
Implement `guarded_write` (section 6) and prove: after `fail=True`, the
database has no ghost row and a subsequent `fail=False` call on a *fresh*
session succeeds. This is the shape Challenge 03 tests.

---

## Summary

| Concept | Description |
|---|---|
| Unit of Work | Session tracks changes; flush emits the SQL |
| Identity map | one row -> one object per session |
| flush vs commit | SQL sent (open tx) vs persisted (tx ended) |
| Autoflush | queries see pending changes automatically |
| Expiry | commit drops values; reload happens lazily |
| Detached | closed session; PK survives, attributes raise |
| Session-per-request | one session per request, closed in finally |

The Session wraps the Core transaction boundary from topic 01 with object
tracking. Master flush/commit and detachment, and the relationships of topic
04 — which also run inside sessions — become predictable.

---

## Quick Reference

| Task | Idiom |
|---|---|
| One session per request | `def get_db(): session = Session(bind=engine); try: yield session; finally: session.close()` |
| Persist changes | `session.add(obj); session.commit()` |
| Get PK before commit | `session.flush(); obj.id` |
| Undo pending work | `session.rollback()` |
| Load by PK | `session.get(User, 1)` |
| Drop identity map | `session.expunge_all()` |
| Check attached | touch attribute inside session; expect `DetachedInstanceError` outside |

---

## Next Steps

Next: **[04 — Relationships](04-relationships-lecture.md)** — navigate object
graphs inside the session with `relationship()`, back_populates, and cascades.

Continues in: **[Phase 05 — Databases](../../05-web-frameworks/fastapi/19-orm.py)** —
sessions wired into FastAPI dependencies.

Official docs:
- Session basics: https://docs.sqlalchemy.org/en/20/orm/session_basics.html
- Unit of Work: https://docs.sqlalchemy.org/en/20/orm/unitofwork.html
- Session FAQ (detached instances): https://docs.sqlalchemy.org/en/20/orm/faq/sessions.html
