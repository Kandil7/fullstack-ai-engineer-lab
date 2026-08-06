"""
Challenge 03: Session Lifecycle — Starter Code
=================================================
Fill in the function bodies. Do not modify signatures.
Topic: Unit of Work, flush vs commit, identity map, rollback.
"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), default="annotator")


def save_user(session: Session, name: str) -> int:
    """Create and COMMIT a user; return the new primary key.

    The PK must be readable after commit — that is what makes request
    handlers able to return an id without re-querying.
    """
    raise NotImplementedError


def get_or_create(session: Session, name: str) -> tuple[User, bool]:
    """Return (user, created).

    created is True only when this call inserted the row. Loading an
    existing user must return THE SAME object the session already has
    (identity map) — never a fresh instance.
    """
    raise NotImplementedError


def guarded_commit(session: Session, name: str, fail: bool) -> int | None:
    """Commit a new user unless fail=True (then rollback, return None).

    A failed request must leave the database EXACTLY as it was — this
    is the transaction-boundary guarantee of session-per-request.
    """
    raise NotImplementedError
