"""
Challenge 10: Repository Pattern — Hidden Tests
=================================================
Pure domain rules, in-memory + SQL repositories behind ONE Protocol,
and the all-or-nothing Unit of Work.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
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


def _exp(name: str, model: str = "bert", score: float = 0.5) -> solution.Experiment:
    return solution.Experiment(name=name, model=model, score=score)


class TestStarterRaises:
    def test_domain_starter_raises(self):
        with pytest.raises(NotImplementedError):
            starter.should_promote(0.9)

    def test_inmemory_starter_raises(self):
        repo = starter.InMemoryExperimentRepository()
        with pytest.raises(NotImplementedError):
            repo.add(_exp("x"))

    def test_sql_starter_raises(self):
        engine = create_engine("sqlite://", poolclass=StaticPool)
        with Session(bind=engine) as s:
            with pytest.raises(NotImplementedError):
                starter.SqlExperimentRepository(s).add(_exp("x"))
        engine.dispose()

    def test_batch_starter_raises(self):
        engine = create_engine("sqlite://", poolclass=StaticPool)
        with Session(bind=engine) as s:
            with pytest.raises(NotImplementedError):
                starter.register_batch_with_transaction(s, [])
        engine.dispose()


class TestDomainRules:
    def test_promote_threshold_inclusive(self):
        assert solution.should_promote(0.9) is True
        assert solution.should_promote(0.89) is False

    def test_best_model_name(self):
        low = _exp("low", model="bert", score=0.7)
        high = _exp("high", model="gpt2", score=0.95)
        assert solution.best_model_name([low, high]) == "gpt2"

    def test_best_model_name_empty(self):
        assert solution.best_model_name([]) is None


class TestInMemoryRepository:
    @pytest.fixture()
    def repo(self):
        return solution.InMemoryExperimentRepository()

    def test_conforms_to_protocol(self, repo):
        assert isinstance(repo, solution.ExperimentRepository)

    def test_add_get_round_trip(self, repo):
        pk = repo.add(_exp("run-1", score=0.8))
        assert isinstance(pk, int)
        assert repo.get("run-1").score == 0.8

    def test_duplicate_raises(self, repo):
        repo.add(_exp("run-1"))
        with pytest.raises(ValueError):
            repo.add(_exp("run-1"))

    def test_list_count(self, repo):
        repo.add(_exp("a"))
        repo.add(_exp("b"))
        assert repo.count() == 2 and len(repo.list_all()) == 2

    def test_delete(self, repo):
        repo.add(_exp("a"))
        assert repo.delete("a") is True
        assert repo.delete("a") is False
        assert repo.count() == 0


class TestSqlRepository:
    @pytest.fixture()
    def env(self):
        engine = create_engine("sqlite://", poolclass=StaticPool)
        solution.Base.metadata.create_all(engine)
        yield engine
        engine.dispose()

    def test_conforms_to_protocol(self, env):
        with Session(bind=env) as s:
            assert isinstance(solution.SqlExperimentRepository(s), solution.ExperimentRepository)

    def test_add_flushes_without_committing(self, env):
        with Session(bind=env) as s:
            repo = solution.SqlExperimentRepository(s)
            pk = repo.add(_exp("pending", score=0.9))
            assert pk > 0  # PK assigned by flush...
        with Session(bind=env) as s:
            # ...but the caller never committed: a fresh session sees nothing
            assert s.scalars(select(solution.Experiment)).all() == []

    def test_caller_commit_persists(self, env):
        with Session(bind=env) as s:
            repo = solution.SqlExperimentRepository(s)
            repo.add(_exp("kept", score=0.9))
            s.commit()
        with Session(bind=env) as s:
            repo = solution.SqlExperimentRepository(s)
            assert repo.get("kept").score == 0.9
            assert repo.count() == 1

    def test_delete(self, env):
        with Session(bind=env) as s:
            repo = solution.SqlExperimentRepository(s)
            repo.add(_exp("gone"))
            s.commit()
            assert repo.delete("gone") is True
            assert repo.delete("gone") is False
            s.commit()
        with Session(bind=env) as s:
            assert s.scalars(select(solution.Experiment)).all() == []


class TestBatchUnitOfWork:
    @pytest.fixture()
    def env(self):
        engine = create_engine("sqlite://", poolclass=StaticPool)
        solution.Base.metadata.create_all(engine)
        yield engine
        engine.dispose()

    def _count(self, env) -> int:
        with Session(bind=env) as s:
            return len(s.scalars(select(solution.Experiment.id)).all())

    def test_clean_batch_commits_all(self, env):
        with Session(bind=env) as s:
            ids = solution.register_batch_with_transaction(
                s, [_exp("a"), _exp("b"), _exp("c")]
            )
            assert len(ids) == 3 and all(isinstance(i, int) for i in ids)
        assert self._count(env) == 3

    def test_duplicate_raises_value_error(self, env):
        with Session(bind=env) as s:
            solution.register_batch_with_transaction(s, [_exp("dup")])
        with Session(bind=env) as s:
            with pytest.raises(ValueError):
                solution.register_batch_with_transaction(
                    s, [_exp("fresh"), _exp("dup")]
                )

    def test_failed_batch_leaves_no_partial_rows(self, env):
        """All-or-nothing: the 'fresh' row must NOT survive with 'dup'."""
        with Session(bind=env) as s:
            solution.register_batch_with_transaction(s, [_exp("dup")])
        with Session(bind=env) as s:
            try:
                solution.register_batch_with_transaction(
                    s, [_exp("fresh"), _exp("dup")]
                )
            except ValueError:
                pass
        assert self._count(env) == 1, "rollback must remove the whole batch"
        with Session(bind=env) as s:
            assert s.scalars(select(solution.Experiment.name)).all() == ["dup"]

    def test_engine_usable_after_failed_batch(self, env):
        with Session(bind=env) as s:
            solution.register_batch_with_transaction(s, [_exp("dup")])
        with Session(bind=env) as s:
            with pytest.raises(ValueError):
                solution.register_batch_with_transaction(s, [_exp("dup")])
        with Session(bind=env) as s:
            ids = solution.register_batch_with_transaction(s, [_exp("after")])
            assert len(ids) == 1
        assert self._count(env) == 2
