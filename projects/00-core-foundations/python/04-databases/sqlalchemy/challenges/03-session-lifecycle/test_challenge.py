"""
Challenge 03: Session Lifecycle — Hidden Tests
================================================
Commit/rollback semantics, identity map behavior, and the
transaction-boundary guarantee of the session-per-request pattern.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


def _load(name: str):
    """Load a sibling module under a UNIQUE name registered in sys.modules.

    Registration matters: SQLAlchemy resolves Mapped[...] annotations
    through the module's globals when a mapped class is configured.
    The unique name (challenge dir embedded) prevents collisions
    between the 10 challenge suites in one pytest process.
    """
    parent = Path(__file__).parent.name.replace("-", "_")
    modname = f"{name}_{parent}"
    spec = importlib.util.spec_from_file_location(
        modname, Path(__file__).parent / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module


starter = _load("starter")
solution = _load("solution")


@pytest.fixture()
def session():
    """Fresh engine + schema + session per test: no cross-test pollution."""
    engine = create_engine("sqlite://", poolclass=StaticPool)
    solution.Base.metadata.create_all(engine)
    with Session(bind=engine) as s:
        yield s
    engine.dispose()


def _count(session: Session, name: str) -> int:
    return len(
        session.scalars(select(solution.User).where(solution.User.name == name)).all()
    )


class TestStarterRaises:
    def test_save_user_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.save_user(session, "ada")

    def test_get_or_create_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.get_or_create(session, "ada")

    def test_guarded_commit_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.guarded_commit(session, "ada", fail=False)


class TestSaveUser:
    def test_returns_positive_int(self, session):
        assert isinstance(solution.save_user(session, "ada"), int)

    def test_commits_row(self, session):
        pk = solution.save_user(session, "ada")
        user = session.get(solution.User, pk)
        assert user is not None and user.name == "ada"

    def test_default_role_applied(self, session):
        pk = solution.save_user(session, "grace")
        assert session.get(solution.User, pk).role == "annotator"

    def test_duplicate_name_raises_integrity_error(self, session):
        solution.save_user(session, "ada")
        with pytest.raises(IntegrityError):
            solution.save_user(session, "ada")


class TestGetOrCreate:
    def test_creates_new(self, session):
        user, created = solution.get_or_create(session, "newbie")
        assert created is True and user.name == "newbie"
        assert _count(session, "newbie") == 1

    def test_existing_not_created(self, session):
        solution.save_user(session, "ada")
        user, created = solution.get_or_create(session, "ada")
        assert created is False and user.name == "ada"

    def test_identity_map_returns_same_object(self, session):
        first, _ = solution.get_or_create(session, "same")
        second, created = solution.get_or_create(session, "same")
        assert created is False and second is first, \
            "second load in the same session must hit the identity map"


class TestGuardedCommit:
    def test_success_returns_id_and_persists(self, session):
        pk = solution.guarded_commit(session, "good", fail=False)
        assert pk is not None and _count(session, "good") == 1

    def test_failure_returns_none(self, session):
        assert solution.guarded_commit(session, "bad", fail=True) is None

    def test_failure_leaves_no_ghost_row(self, session):
        solution.guarded_commit(session, "bad", fail=True)
        assert _count(session, "bad") == 0

    def test_failure_keeps_earlier_commits(self, session):
        solution.guarded_commit(session, "keep", fail=False)
        solution.guarded_commit(session, "bad", fail=True)
        assert _count(session, "keep") == 1
        assert _count(session, "bad") == 0

    def test_retry_after_rollback_works(self, session):
        """Rollback must leave the session usable for the next request."""
        solution.guarded_commit(session, "bad", fail=True)
        pk = solution.guarded_commit(session, "bad", fail=False)
        assert pk is not None and _count(session, "bad") == 1
