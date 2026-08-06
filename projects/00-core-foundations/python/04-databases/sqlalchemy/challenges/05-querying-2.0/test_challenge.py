"""
Challenge 05: Querying with select() — Hidden Tests
=====================================================
Filtering, join-then-aggregate correctness, and leaderboard limits.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
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
    """Fresh engine + schema + seed data per test."""
    engine = create_engine("sqlite://", poolclass=StaticPool)
    solution.Base.metadata.create_all(engine)
    with Session(bind=engine) as s:
        _seed(s)
        yield s
    engine.dispose()


def _seed(session: Session) -> None:
    bert = solution.Experiment(name="bert-finetune-1", model="bert", status="done")
    gpt = solution.Experiment(name="gpt-finetune-1", model="gpt2", status="done")
    running = solution.Experiment(name="bert-finetune-2", model="bert", status="running")
    session.add_all([bert, gpt, running])
    session.commit()
    session.add_all(
        [
            solution.EvalMetric(experiment_id=bert.id, metric="f1", value=0.89),
            solution.EvalMetric(experiment_id=bert.id, metric="latency", value=12.5),
            solution.EvalMetric(experiment_id=gpt.id, metric="f1", value=0.93),
            solution.EvalMetric(experiment_id=gpt.id, metric="latency", value=21.0),
            solution.EvalMetric(experiment_id=running.id, metric="f1", value=0.81),
        ]
    )
    session.commit()


class TestStarterRaises:
    def test_done_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.done_experiments(session)

    def test_best_f1_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.best_f1_per_model(session)

    def test_leaderboard_starter_raises(self, session):
        with pytest.raises(NotImplementedError):
            starter.metric_leaderboard(session, "f1", 0.0, 5)


class TestDoneExperiments:
    def test_returns_sorted_done_names(self, session):
        assert solution.done_experiments(session) == [
            "bert-finetune-1",
            "gpt-finetune-1",
        ]

    def test_excludes_running(self, session):
        assert "bert-finetune-2" not in solution.done_experiments(session)

    def test_empty_db_returns_empty(self):
        engine = create_engine("sqlite://", poolclass=StaticPool)
        solution.Base.metadata.create_all(engine)
        with Session(bind=engine) as s:
            assert solution.done_experiments(s) == []
        engine.dispose()


class TestBestF1PerModel:
    def test_returns_model_max_f1(self, session):
        assert solution.best_f1_per_model(session) == [
            ("bert", 0.89),
            ("gpt2", 0.93),
        ]

    def test_ignores_other_metrics(self, session):
        """latency (12.5/21.0) must never leak into the f1 aggregate."""
        pairs = solution.best_f1_per_model(session)
        for model, best in pairs:
            assert best in (0.89, 0.93), f"non-f1 metric leaked into {model}: {best}"

    def test_empty_db_returns_empty(self):
        engine = create_engine("sqlite://", poolclass=StaticPool)
        solution.Base.metadata.create_all(engine)
        with Session(bind=engine) as s:
            assert solution.best_f1_per_model(s) == []
        engine.dispose()


class TestMetricLeaderboard:
    def test_filters_by_min_value(self, session):
        assert solution.metric_leaderboard(session, "f1", 0.90, 5) == [
            ("gpt-finetune-1", 0.93)
        ]

    def test_sorts_descending_and_limits(self, session):
        assert solution.metric_leaderboard(session, "f1", 0.80, 2) == [
            ("gpt-finetune-1", 0.93),
            ("bert-finetune-1", 0.89),
        ]

    def test_lower_bar_includes_more(self, session):
        names = [n for n, _ in solution.metric_leaderboard(session, "f1", 0.0, 10)]
        assert names == ["gpt-finetune-1", "bert-finetune-1", "bert-finetune-2"]

    def test_metric_filter_is_exact(self, session):
        """A 'f1-micro' metric must not match metric == 'f1'."""
        session.add(solution.EvalMetric(experiment_id=1, metric="f1-micro", value=0.99))
        session.commit()
        assert solution.metric_leaderboard(session, "f1", 0.90, 5) == [
            ("gpt-finetune-1", 0.93)
        ]

    def test_empty_result_when_nothing_qualifies(self, session):
        assert solution.metric_leaderboard(session, "f1", 1.0, 5) == []
