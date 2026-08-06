"""
Challenge 06: Eager Loading and the N+1 Problem — Hidden Tests
================================================================
The star challenge: these tests COUNT SQL statements. A lazy solution
returns the right rows but fails the query-count assertions.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, event, select
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


class QueryCounter:
    """Counts SQL statements executed on a given engine."""

    def __init__(self, engine) -> None:
        self.queries: list[str] = []
        event.listen(engine, "before_cursor_execute", self._on_execute)

    def _on_execute(self, conn, cursor, statement, parameters, context, executemany):
        self.queries.append(statement)

    def count(self) -> int:
        return len(self.queries)

    def reset(self) -> None:
        self.queries = []


@pytest.fixture()
def env():
    """Fresh engine + schema + seed per test; returns (session, counter)."""
    engine = create_engine("sqlite://", poolclass=StaticPool)
    solution.Base.metadata.create_all(engine)
    with Session(bind=engine) as session:
        _seed(session)
        session.expunge_all()          # drop identity map: every load hits SQL
        counter = QueryCounter(engine)
        yield session, counter
    engine.dispose()


def _seed(session: Session) -> None:
    for p in range(3):
        project = solution.Project(name=f"campaign-{p}")
        project.experiments.extend(
            [solution.Experiment(name=f"campaign-{p}-run-{k}") for k in range(2)]
        )
        session.add(project)
    strict = solution.StrictProject(name="strict-0")
    strict.experiments.append(solution.StrictExperiment(name="strict-0-run-0"))
    session.add(strict)
    session.commit()


class TestStarterRaises:
    def test_selectin_starter_raises(self, env):
        session, _ = env
        with pytest.raises(NotImplementedError):
            starter.load_projects(session)

    def test_joined_starter_raises(self, env):
        session, _ = env
        with pytest.raises(NotImplementedError):
            starter.load_projects_joined(session)

    def test_raise_guard_starter_raises(self, env):
        session, _ = env
        with pytest.raises(NotImplementedError):
            starter.lazy_access_raises(session)


class TestSelectinLoad:
    def test_shape_correct(self, env):
        session, _ = env
        result = solution.load_projects(session)
        assert [name for name, _ in result] == ["campaign-0", "campaign-1", "campaign-2"]
        assert all(len(runs) == 2 for _, runs in result)

    def test_exactly_two_queries(self, env):
        """The N+1 killer: 1 parent + 1 IN (...) — never 1 + N."""
        session, counter = env
        counter.reset()
        solution.load_projects(session)
        assert counter.count() == 2, \
            f"selectinload must fire exactly 2 queries, got {counter.count()}"

    def test_no_extra_query_on_traversal(self, env):
        """Accessing loaded children must not fire more SQL."""
        session, counter = env
        counter.reset()
        result = solution.load_projects(session)
        first = counter.count()
        _ = [len(runs) for _, runs in result]      # pure Python now
        assert counter.count() == first == 2


class TestJoinedLoad:
    def test_shape_correct(self, env):
        session, _ = env
        result = solution.load_projects_joined(session)
        assert [name for name, _ in result] == ["campaign-0", "campaign-1", "campaign-2"]
        assert all(len(runs) == 2 for _, runs in result)

    def test_no_duplicate_projects(self, env):
        """Without .unique() the parent repeats once per child (6 rows)."""
        session, _ = env
        result = solution.load_projects_joined(session)
        assert len(result) == 3, "joined collection loads MUST be deduplicated"

    def test_exactly_one_query(self, env):
        session, counter = env
        counter.reset()
        solution.load_projects_joined(session)
        assert counter.count() == 1, \
            f"joinedload must fire exactly 1 query, got {counter.count()}"


class TestFetchAndGuard:
    def test_fetch_at_most_two_queries(self, env):
        session, counter = env
        counter.reset()
        result = solution.fetch_projects_with_runs(session)
        assert len(result) == 3
        assert counter.count() <= 2

    def test_lazy_raise_guard(self, env):
        session, _ = env
        assert solution.lazy_access_raises(session) == "InvalidRequestError"
