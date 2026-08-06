"""
04-databases/sqlalchemy — 03: Session Lifecycle
==================================================
Topics: Unit of Work; identity map; flush vs commit; expiry;
        detached instances; session-per-request.

Why this matters for AI/backend engineering:
    The Session is the transaction boundary of every request in a
    FastAPI/Django service — and in ML services it wraps train/eval
    metadata writes. Misunderstanding flush vs commit causes lost
    updates ("I committed but the row is gone") and the dreaded
    DetachedInstanceError in serializers. The identity map is why
    loading the same row twice gives you the SAME Python object:
    that is what makes `==` work on ORM instances at all.

Run:      python 03-session-lifecycle.py
Verify:   python 03-session-lifecycle.py --verify
Reference: https://docs.sqlalchemy.org/en/20/orm/session_basics.html
"""

from __future__ import annotations

import sys

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm.exc import DetachedInstanceError

# ============================================================
# 0. Shared in-memory database
# ============================================================
# StaticPool pins ONE connection so every Session in this process sees
# the same in-memory database. (In production each request gets its own
# session but they share a real database server.)
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), default="annotator")


Base.metadata.create_all(engine)


def new_session() -> Session:
    """Shortcut: fresh session bound to the shared engine."""
    return Session(bind=engine)


# ============================================================
# 1. Unit of Work: the session tracks changes for you
# ============================================================
# You add objects and change attributes; the Session (the Unit of Work)
# decides what to INSERT/UPDATE/DELETE when you flush. You do not write
# the UPDATE statements.

# Example 1: add + mutate + commit — one transaction, two SQL statements
with new_session() as session:
    ada = User(name="ada", role="annotator")
    session.add(ada)          # pending: no SQL yet
    ada.role = "reviewer"     # still pending; change is tracked
    session.commit()          # INSERT users ... ; then nothing to update
    print(f"committed user id={ada.id} role={ada.role}")

# Output:
# committed user id=1 role=reviewer

# ============================================================
# 2. Identity map: one row -> one Python object
# ============================================================
# Within a session, a primary key maps to exactly ONE instance. Loading
# the same row twice returns the same object (identity, not equality).
# Complexity: identity-map lookup O(1) dict access; no extra SQL if the
# object is already loaded.

# Example 2: two loads, one object
with new_session() as session:
    first = session.get(User, 1)
    second = session.get(User, 1)   # no SQL: served from identity map
    print(f"same object: {first is second}")

# Output:
# same object: True

# Example 3: identity map keeps two sessions isolated
with new_session() as session_a, new_session() as session_b:
    a = session_a.get(User, 1)
    b = session_b.get(User, 1)
    print(f"cross-session same object: {a is b}")

# Output:
# cross-session same object: False

# ============================================================
# 3. flush vs commit
# ============================================================
# flush()  -> emit SQL to the DB, transaction still OPEN, rollback-able
# commit() -> flush + COMMIT (transaction ends), then expire attributes
# Autoflush: queries inside the session flush pending changes first so
# the query can see them.

# Example 4: flush-then-query sees pending (uncommitted) data
with new_session() as session:
    grace = User(name="grace")
    session.add(grace)
    session.flush()                        # INSERT issued now
    found = session.scalars(
        select(User).where(User.name == "grace")
    ).first()
    print(f"flush-then-query found pending row: {found is grace}")
    session.rollback()                     # undo the INSERT

# Output:
# flush-then-query found pending row: True

# Example 5: without flush/commit the query would NOT see it — rollback
#            leaves the DB exactly as before.
with new_session() as session:
    ghost = User(name="ghost")
    session.add(ghost)
    session.rollback()
count_ghost = len(
    new_session().scalars(select(User).where(User.name == "ghost")).all()
)
print(f"ghost rows after rollback: {count_ghost}")

# Output:
# ghost rows after rollback: 0

# ============================================================
# 4. Expiry and detached instances
# ============================================================
# commit() expires loaded attributes (expire_on_commit=True): the values
# are dropped so the next access reloads fresh from the DB. That reload
# needs a live session. Once the session is CLOSED the instance becomes
# DETACHED, and touching an expired attribute raises
# DetachedInstanceError.

# Example 6: expiry — value is reloaded lazily (still attached)
with new_session() as session:
    u = session.get(User, 1)
    session.expire(u)                  # drop loaded attribute values
    print(f"reloaded after expire: {u.role}")   # re-SELECT happens here

# Output:
# reloaded after expire: reviewer

# Example 7: detached instance — expired attribute access raises
def _detached_error_demo(name: str) -> str:
    """Commit, close the session, then touch an expired attribute."""
    session = new_session()
    u = User(name=name)
    session.add(u)
    session.commit()          # expiry: attribute values dropped
    session.close()           # now u is detached
    try:
        _ = u.role            # expired + detached -> DetachedInstanceError
    except DetachedInstanceError as exc:
        return type(exc).__name__
    return "no error"


print(f"detached expired attribute -> {_detached_error_demo('bob')}")

# Output:
# detached expired attribute -> DetachedInstanceError

# The PRIMARY KEY survives detachment (it is the object's identity, not
# an expired value). This is why you can pass ids around safely:
with new_session() as session:
    u = session.get(User, 1)
    pk = u.id
    session.close()
print(f"pk readable while detached: {pk}")

# Output:
# pk readable while detached: 1

# ============================================================
# 5. Session-per-request (FastAPI pattern, simulated)
# ============================================================
# Real services create ONE session per HTTP request, close it in a
# finally block, and never share sessions across requests or threads.
# This gives each request its own transaction boundary.

def get_db():
    """FastAPI dependency generator: one session per request."""
    session = new_session()
    try:
        yield session
    finally:
        session.close()  # guaranteed: no leaked connections


def handle_request(session: Session, name: str) -> int:
    """Simulated endpoint: write one row in its own transaction."""
    user = User(name=name)
    session.add(user)
    session.commit()
    return user.id  # PK survives commit expiry; no refresh needed


def simulate_two_requests(name_a: str, name_b: str) -> list[str]:
    """Two independent request lifecycles against the same DB."""
    results: list[str] = []
    gen = get_db()
    session = next(gen)
    results.append(f"request-1 wrote user id={handle_request(session, name_a)}")
    gen.close()

    gen2 = get_db()
    session2 = next(gen2)
    results.append(f"request-2 wrote user id={handle_request(session2, name_b)}")
    gen2.close()
    return results


# Example 8: each request commits independently; both rows persist
for line in simulate_two_requests("linus", "torvalds"):
    print(line)

# Output:
# request-1 wrote user id=3
# request-2 wrote user id=4


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: holding a session open across requests / threads.
#   session = Session()          # created once at import time
#   # ... shared by every request: identity map leaks, stale reads
# CORRECT:
#   def get_db():                # one per request, closed in finally
#       session = new_session()
#       try:
#           yield session
#       finally:
#           session.close()
#
# MISTAKE: serializing ORM objects after the session is closed.
#   data = {"name": user.name}   # after request -> DetachedInstanceError
# CORRECT: serialize INSIDE the session, or load fresh with session.get.


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. Identity map: same session, same object; no double-loading
    with new_session() as session:
        a = session.get(User, 1)
        b = session.get(User, 1)
        assert a is b, "identity map must return the same instance"

    # 2. Flush-then-query sees pending rows (unit of work visibility)
    with new_session() as session:
        alan = User(name="alan")
        session.add(alan)
        session.flush()
        found = session.scalars(
            select(User).where(User.name == "alan")
        ).first()
        assert found is alan, "flush must make pending rows queryable"
        session.rollback()

    # 3. Commit persists; a NEW session sees the row
    with new_session() as session:
        session.add(User(name="persist-me"))
        session.commit()
    persisted = new_session().scalars(
        select(User).where(User.name == "persist-me")
    ).first()
    assert persisted is not None, "commit must persist across sessions"

    # 4. Rollback leaves no trace
    with new_session() as session:
        session.add(User(name="ghost"))
        session.rollback()
    ghosts = new_session().scalars(
        select(User).where(User.name == "ghost")
    ).all()
    assert ghosts == [], "rollback must undo pending inserts"

    # 5. Detached + expired attribute raises DetachedInstanceError
    assert _detached_error_demo("bob-verify") == "DetachedInstanceError", \
        "expired attribute access on detached instance must raise"

    # 6. Primary key survives detachment
    with new_session() as session:
        u = session.get(User, 1)
        pk = u.id
        session.close()
    assert pk == 1, "PK must be readable on a detached instance"

    # 7. Session-per-request: each simulated request commits independently
    outcomes = simulate_two_requests("ada-lovelace", "grace-hopper")
    assert len(outcomes) == 2, "both requests must complete"
    names = new_session().scalars(select(User.name)).all()
    assert "ada-lovelace" in names and "grace-hopper" in names, \
        "each request's commit must persist"

    print("[OK] 03-session-lifecycle: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Session = Unit of Work + identity map + transaction boundary")
        print("2. flush emits SQL inside the transaction; commit ends it")
        print("3. Detached instances keep their PK but lose expired attributes")
        _verify()  # always runs, so plain execution is also a test
