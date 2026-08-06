"""
Challenge 09: Testing with a Database — Hidden Tests
======================================================
Factory defaults, schema resets, and the rollback-isolation guarantee.
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
def engine():
    """Fresh in-memory engine with schema applied, per test."""
    eng = create_engine("sqlite://", poolclass=StaticPool)
    solution.Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


def _count(eng) -> int:
    with Session(bind=eng) as s:
        return len(s.scalars(select(solution.Experiment.id)).all())


class TestStarterRaises:
    def test_factory_starter_raises(self):
        with pytest.raises(NotImplementedError):
            starter.make_experiment("a")

    def test_transactional_starter_raises(self, engine):
        with pytest.raises(NotImplementedError):
            gen = starter.transactional_session(engine)
            next(gen)

    def test_isolated_starter_raises(self, engine):
        with pytest.raises(NotImplementedError):
            starter.run_isolated_tests(engine)


class TestMakeExperiment:
    def test_defaults_applied(self):
        exp = solution.make_experiment("a")
        assert exp.score == 0.0 and exp.config == {}

    def test_overrides_win(self):
        exp = solution.make_experiment("a", score=0.5, config={"lr": 1e-4})
        assert exp.score == 0.5 and exp.config == {"lr": 1e-4}

    def test_factory_object_persists(self, engine):
        exp = solution.make_experiment("factory-run", score=0.75)
        with Session(bind=engine) as s:
            s.add(exp)
            s.commit()
        with Session(bind=engine) as s:
            loaded = s.scalars(
                select(solution.Experiment).where(
                    solution.Experiment.name == "factory-run"
                )
            ).one()
            assert loaded.score == 0.75 and loaded.config == {}

    def test_unique_name_enforced(self, engine):
        with Session(bind=engine) as s:
            s.add(solution.make_experiment("dupe"))
            s.commit()
        with Session(bind=engine) as s:
            s.add(solution.make_experiment("dupe"))
            with pytest.raises(IntegrityError):
                s.commit()


class TestResetSchema:
    def test_clears_rows(self, engine):
        with Session(bind=engine) as s:
            s.add_all([solution.make_experiment("r1"), solution.make_experiment("r2")])
            s.commit()
        assert _count(engine) == 2
        solution.reset_schema(engine)
        assert _count(engine) == 0

    def test_engine_usable_after_reset(self, engine):
        solution.reset_schema(engine)
        with Session(bind=engine) as s:
            s.add(solution.make_experiment("fresh"))
            s.commit()
        assert _count(engine) == 1


class TestTransactionalSession:
    def test_rows_visible_during_test(self, engine):
        gen = solution.transactional_session(engine)
        session = next(gen)
        try:
            session.add_all(
                [solution.make_experiment("t1-a"), solution.make_experiment("t1-b")]
            )
            seen = len(session.scalars(select(solution.Experiment.id)).all())
            assert seen == 2, "rows must be visible inside the test"
        finally:
            gen.close()

    def test_rollback_after_close(self, engine):
        gen = solution.transactional_session(engine)
        session = next(gen)
        session.add_all(
            [solution.make_experiment("t1-a"), solution.make_experiment("t1-b")]
        )
        gen.close()
        assert _count(engine) == 0, "closing the fixture must roll back writes"

    def test_engine_stays_usable(self, engine):
        gen = solution.transactional_session(engine)
        session = next(gen)
        session.add(solution.make_experiment("ghost"))
        gen.close()
        with Session(bind=engine) as s:
            s.add(solution.make_experiment("real"))
            s.commit()
        assert _count(engine) == 1


class TestRunIsolatedTests:
    def test_two_tests_see_expected_rows(self, engine):
        assert solution.run_isolated_tests(engine) == (2, 0)

    def test_engine_empty_afterwards(self, engine):
        solution.run_isolated_tests(engine)
        assert _count(engine) == 0

    def test_works_on_reset_engine(self, engine):
        solution.reset_schema(engine)
        assert solution.run_isolated_tests(engine) == (2, 0)
