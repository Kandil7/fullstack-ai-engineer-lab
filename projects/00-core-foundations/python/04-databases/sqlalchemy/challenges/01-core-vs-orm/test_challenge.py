"""
Challenge 01: Core vs ORM — Hidden Tests
==========================================
Correctness, edge cases, and the performance guard for the Gold tier.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select, text
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
def conn():
    engine = create_engine("sqlite://", poolclass=StaticPool)
    solution.metrics_table.metadata.create_all(engine)
    with engine.connect() as connection:
        yield connection
    engine.dispose()


class TestStarterRaises:
    """The starter must fail until the learner implements it."""

    def test_bulk_insert_starter_raises(self, conn):
        with pytest.raises(NotImplementedError):
            starter.bulk_insert_metrics(conn, [{"model": "b", "metric": "f1", "value": 1}])

    def test_query_starter_raises(self, conn):
        with pytest.raises(NotImplementedError):
            starter.query_above(conn, 1.0)

    def test_upsert_starter_raises(self, conn):
        with pytest.raises(NotImplementedError):
            starter.safe_upsert_metrics(conn, [], 500)


class TestBulkInsert:
    def test_basic_insert_count(self, conn):
        rows = [{"model": "bert", "metric": "f1", "value": 89}]
        assert solution.bulk_insert_metrics(conn, rows) == 1

    def test_empty_input(self, conn):
        assert solution.bulk_insert_metrics(conn, []) == 0

    def test_multi_row(self, conn):
        rows = [{"model": "m", "metric": f"k{i}", "value": i} for i in range(10)]
        assert solution.bulk_insert_metrics(conn, rows) == 10

    def test_rows_actually_persist(self, conn):
        solution.bulk_insert_metrics(conn, [{"model": "m", "metric": "f1", "value": 1}])
        count = conn.execute(text("SELECT COUNT(*) FROM metrics")).scalar_one()
        assert count == 1


class TestQueryAbove:
    @pytest.fixture(autouse=True)
    def _seed(self, conn):
        solution.bulk_insert_metrics(
            conn,
            [
                {"model": "bert", "metric": "f1", "value": 89},
                {"model": "bert", "metric": "acc", "value": 95},
                {"model": "bert", "metric": "loss", "value": 90},
            ],
        )
        conn.commit()

    def test_threshold_filter(self, conn):
        rows = solution.query_above(conn, 90.0)
        assert [(r[1], r[2]) for r in rows] == [("acc", 95.0)]

    def test_strictly_above_boundary(self, conn):
        rows = solution.query_above(conn, 89.0)
        assert [(r[1], r[2]) for r in rows] == [("acc", 95.0), ("loss", 90.0)]

    def test_order_desc(self, conn):
        rows = solution.query_above(conn, 0.0)
        values = [r[2] for r in rows]
        assert values == sorted(values, reverse=True)

    def test_no_matches_returns_empty(self, conn):
        assert solution.query_above(conn, 10_000.0) == []

    def test_bound_parameter_not_literal(self, conn):
        import inspect
        source = inspect.getsource(solution.query_above)
        assert ":threshold" in source, "must use a named bound parameter"


class TestSafeUpsert:
    def test_small_batch(self, conn):
        rows = [{"model": "m", "metric": f"k{i}", "value": i} for i in range(10)]
        assert solution.safe_upsert_metrics(conn, rows, batch_size=3) == 10

    def test_all_rows_persist_after_batches(self, conn):
        rows = [{"model": "m", "metric": f"k{i}", "value": i} for i in range(10)]
        solution.safe_upsert_metrics(conn, rows, batch_size=3)
        count = conn.execute(text("SELECT COUNT(*) FROM metrics")).scalar_one()
        assert count == 10

    def test_empty(self, conn):
        assert solution.safe_upsert_metrics(conn, [], batch_size=2) == 0

    def test_odd_remainder(self, conn):
        rows = [{"model": "m", "metric": f"k{i}", "value": i} for i in range(7)]
        assert solution.safe_upsert_metrics(conn, rows, batch_size=4) == 7

    def test_performance_chunking(self, conn):
        """Gold guard: a 2000-row load with batch 250 must not blow up."""
        rows = [{"model": "m", "metric": f"k{i}", "value": i} for i in range(2000)]
        assert solution.safe_upsert_metrics(conn, rows, batch_size=250) == 2000
        count = conn.execute(text("SELECT COUNT(*) FROM metrics")).scalar_one()
        assert count == 2000
