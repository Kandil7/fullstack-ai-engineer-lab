"""
Challenge 08: Advanced Patterns — Hidden Tests
================================================
Hybrid SQL/instance agreement, byte-exact vector round-trips,
SQL-side ranking, and optimistic-version guards.
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
    """Fresh engine + schema + seed per test."""
    engine = create_engine("sqlite://", poolclass=StaticPool)
    solution.Base.metadata.create_all(engine)
    with Session(bind=engine) as s:
        _seed(s)
        yield s
    engine.dispose()


def _seed(session: Session) -> None:
    session.add_all(
        [
            solution.Experiment(name="bert-run-1", model="bert", score=0.92),
            solution.Experiment(name="bert-run-2", model="bert", score=0.85),
            solution.Experiment(name="gpt-run-1", model="gpt2", score=0.93),
            solution.Experiment(name="gpt-run-2", model="gpt2", score=0.88),
        ]
    )
    session.commit()


class TestStarterRaises:
    def test_promotable_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.promotable_experiments(session)

    def test_embedding_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.store_embedding(session, "c1", [0.5])

    def test_top_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.top_per_model(session)

    def test_update_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.update_if_version(session, 1, 1, 0.99)


class TestPromotable:
    def test_returns_leader_names_sorted(self, session):
        assert solution.promotable_experiments(session) == [
            "bert-run-1",
            "gpt-run-1",
        ]

    def test_threshold_is_inclusive(self, session):
        session.add(solution.Experiment(name="edge", model="edge", score=0.90))
        session.commit()
        assert "edge" in solution.promotable_experiments(session)

    def test_sql_matches_instance_rule(self, session):
        """The WHERE clause and Python evaluation must agree."""
        ids = solution.promotable_experiments(session)
        for exp in session.scalars(select(solution.Experiment)).all():
            assert (exp.name in ids) == (exp.is_leader), \
                "SQL-side hybrid drifted from the instance-side rule"


class TestStoreEmbedding:
    def test_returns_id(self, session):
        assert isinstance(
            solution.store_embedding(session, "chunk-a", [0.25, 0.5, 0.75, 1.0]),
            int,
        )

    def test_round_trip_exact_for_representable_floats(self, session):
        vec = [0.25, 0.5, 0.75, 1.0, -0.5, 2.0]
        pk = solution.store_embedding(session, "chunk-a", vec)
        loaded = session.get(solution.Embedding, pk).vector
        assert loaded == vec, "float32 stores these values exactly"

    def test_round_trip_approx_for_arbitrary_floats(self, session):
        vec = [0.1, 0.2, 0.3, 0.123456]
        pk = solution.store_embedding(session, "chunk-a", vec)
        loaded = session.get(solution.Embedding, pk).vector
        assert len(loaded) == len(vec)
        for a, b in zip(loaded, vec):
            assert abs(a - b) < 1e-6, "float32 round-trip must be approx-equal"

    def test_duplicate_chunk_id_raises(self, session):
        solution.store_embedding(session, "chunk-a", [0.5])
        with pytest.raises(IntegrityError):
            solution.store_embedding(session, "chunk-a", [0.5])


class TestTopPerModel:
    def test_top1_per_model(self, session):
        assert solution.top_per_model(session, 1) == [
            ("bert-run-1", "bert", 0.92),
            ("gpt-run-1", "gpt2", 0.93),
        ]

    def test_top2_returns_all(self, session):
        result = solution.top_per_model(session, 2)
        assert [r[0] for r in result] == [
            "bert-run-1",
            "bert-run-2",
            "gpt-run-1",
            "gpt-run-2",
        ]

    def test_ordered_by_score_inside_model(self, session):
        result = solution.top_per_model(session, 2)
        bert = [r for r in result if r[1] == "bert"]
        assert [r[2] for r in bert] == [0.92, 0.85], \
            "rows within a model must be ranked by score DESC"


class TestUpdateIfVersion:
    def test_success_updates_score(self, session):
        exp = session.get(solution.Experiment, 1)
        assert solution.update_if_version(session, exp.id, exp.version, 0.99) is True
        assert session.get(solution.Experiment, 1).score == 0.99

    def test_success_bumps_version(self, session):
        exp = session.get(solution.Experiment, 1)
        v0 = exp.version
        solution.update_if_version(session, exp.id, v0, 0.99)
        assert session.get(solution.Experiment, 1).version == v0 + 1

    def test_stale_version_is_rejected(self, session):
        exp = session.get(solution.Experiment, 1)
        solution.update_if_version(session, exp.id, exp.version, 0.99)   # v1 -> v2
        before = session.get(solution.Experiment, 1)
        # now try to write with the OLD version 1: must refuse
        assert solution.update_if_version(session, exp.id, 1, 0.10) is False
        after = session.get(solution.Experiment, 1)
        assert after.score == before.score == 0.99, "stale write must not land"

    def test_missing_experiment_is_false(self, session):
        assert solution.update_if_version(session, 9999, 1, 0.5) is False
