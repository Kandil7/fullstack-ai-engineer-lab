"""
Challenge 02: Declarative Models — Hidden Tests
================================================
Schema shape, DB-enforced constraints, and the Gold-tier event rule.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session
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
def env():
    class Base(DeclarativeBase):
        pass

    model = solution.build_model_versions_model(Base)
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    return {"engine": engine, "Base": Base, "model": model}


def _add(engine, model, **kwargs):
    with Session(bind=engine) as session:
        session.add(model(**kwargs))
        session.commit()


class TestStarterRaises:
    def test_starter_raises(self):
        class Base(DeclarativeBase):
            pass

        with pytest.raises(NotImplementedError):
            starter.build_model_versions_model(Base)


class TestSchemaShape:
    def test_table_name(self, env):
        assert env["model"].__tablename__ == "model_versions"

    def test_columns_exist(self, env):
        cols = {c["name"] for c in inspect(env["engine"]).get_columns("model_versions")}
        assert {"id", "model_name", "version", "artifact_uri"} <= cols

    def test_required_columns_not_null(self, env):
        cols = {
            c["name"]: c for c in inspect(env["engine"]).get_columns("model_versions")
        }
        assert cols["model_name"]["nullable"] is False
        assert cols["artifact_uri"]["nullable"] is False

    def test_create_all_is_idempotent(self, env):
        env["Base"].metadata.create_all(env["engine"])  # second call: no error


class TestUniqueConstraint:
    def test_duplicate_pair_rejected(self, env):
        _add(env["engine"], env["model"], model_name="bert", version=1, artifact_uri="s3://a")
        with pytest.raises(IntegrityError):
            _add(env["engine"], env["model"], model_name="bert", version=1, artifact_uri="s3://b")

    def test_same_name_different_version_ok(self, env):
        _add(env["engine"], env["model"], model_name="bert", version=1, artifact_uri="s3://a")
        _add(env["engine"], env["model"], model_name="bert", version=2, artifact_uri="s3://b")

    def test_different_name_same_version_ok(self, env):
        _add(env["engine"], env["model"], model_name="bert", version=1, artifact_uri="s3://a")
        _add(env["engine"], env["model"], model_name="gpt", version=1, artifact_uri="s3://b")


class TestCheckConstraint:
    def test_zero_version_rejected(self, env):
        with pytest.raises(IntegrityError):
            _add(env["engine"], env["model"], model_name="bert", version=0, artifact_uri="s3://a")

    def test_negative_version_rejected(self, env):
        with pytest.raises(IntegrityError):
            _add(env["engine"], env["model"], model_name="bert", version=-3, artifact_uri="s3://a")

    def test_positive_version_accepted(self, env):
        _add(env["engine"], env["model"], model_name="bert", version=1, artifact_uri="s3://a")


class TestEventRule:
    def test_non_s3_uri_raises_value_error(self, env):
        with pytest.raises(ValueError):
            _add(env["engine"], env["model"], model_name="bert", version=1, artifact_uri="local/path")

    def test_s3_uri_accepted(self, env):
        _add(env["engine"], env["model"], model_name="bert", version=1, artifact_uri="s3://models/bert/v1")

    def test_event_fires_on_flush_not_commit(self, env):
        """The ValueError must surface during flush, inside the session."""
        with Session(bind=env["engine"]) as session:
            session.add(
                env["model"](model_name="x", version=1, artifact_uri="bad")
            )
            with pytest.raises(ValueError):
                session.flush()

    def test_no_rows_written_after_rejection(self, env):
        try:
            _add(env["engine"], env["model"], model_name="bert", version=1, artifact_uri="bad")
        except ValueError:
            pass
        with Session(bind=env["engine"]) as session:
            rows = session.scalars(select(env["model"])).all()
            assert rows == []
