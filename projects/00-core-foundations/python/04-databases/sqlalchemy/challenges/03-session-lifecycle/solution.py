"""
Challenge 03: Session Lifecycle — Reference Solution
======================================================
Why this approach: the session is the transaction boundary. Committing
ends the transaction and persists the work; rolling back discards it.
The PK survives expiry, which is why returning an id after commit works.
"""

from __future__ import annotations

from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), default="annotator")


def save_user(session: Session, name: str) -> int:
    """Create and COMMIT a user; return the new primary key."""
    user = User(name=name)
    session.add(user)
    session.commit()      # flush + COMMIT: the transaction ends here
    return user.id        # PK survives expiry — no refresh needed


def get_or_create(session: Session, name: str) -> tuple[User, bool]:
    """Return (user, created); existing rows come back from the identity map."""
    user = session.scalars(
        select(User).where(User.name == name)
    ).first()
    if user is not None:
        return user, False
    user = User(name=name)
    session.add(user)
    session.commit()
    return user, True


def guarded_commit(session: Session, name: str, fail: bool) -> int | None:
    """Commit a new user unless fail=True (then rollback, return None)."""
    user = User(name=name)
    session.add(user)
    if fail:
        session.rollback()   # pending INSERT is discarded, not committed
        return None
    session.commit()
    return user.id
