"""
Challenge 14: query-optimization — Hidden Tests
================================================
"""

import sqlite3
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

starter_spec = importlib.util.spec_from_file_location(
    "starter", Path(__file__).parent / "starter.py")
starter_module = importlib.util.module_from_spec(starter_spec)
starter_spec.loader.exec_module(starter_module)

solution_spec = importlib.util.spec_from_file_location(
    "solution", Path(__file__).parent / "solution.py")
solution_module = importlib.util.module_from_spec(solution_spec)
solution_spec.loader.exec_module(solution_module)

import pytest


class TestSargablePlan:
    def test_sargable_searches(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.sargable_plan(conn)
        assert any("SEARCH" in p for p in result["sargable"])

    def test_wrapped_scans(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.sargable_plan(conn)
        assert any("SCAN events" in p for p in result["wrapped"])

    def test_contrast(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.sargable_plan(conn)
        sarg = "".join(result["sargable"])
        wrap = "".join(result["wrapped"])
        assert "SEARCH" in sarg and "SEARCH" not in wrap


class TestKeysetPage:
    def test_next_page(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.keyset_page(conn, 100, 3)
        assert [r[0] for r in result["rows"]] == [101, 102, 103]

    def test_first_page(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.keyset_page(conn, 0, 2)
        assert [r[0] for r in result["rows"]] == [1, 2]

    def test_plan_searches_pk(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.keyset_page(conn, 100, 3)
        plan = "".join(result["plan"])
        assert "SEARCH" in plan
        assert "INTEGER PRIMARY KEY" in plan

    def test_page_beyond_end(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.keyset_page(conn, 99999, 10)
        assert result["rows"] == []


class TestBatchFetch:
    def _parents(self):
        return [1, 2, 3, 4, 5]

    def test_correctness(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.batch_fetch(conn, self._parents(), 2)
        assert len(result["rows"]) == 15
        parents = {r[0] for r in result["rows"]}
        assert parents == {1, 2, 3, 4, 5}

    def test_query_count_chunked(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.batch_fetch(conn, self._parents(), 2)
        assert result["queries"] == 3  # ceil(5 / 2)

    def test_query_count_single(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.batch_fetch(conn, self._parents(), 10)
        assert result["queries"] == 1

    def test_query_count_naive_batch(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.batch_fetch(conn, self._parents(), 1)
        assert result["queries"] == 5

    def test_empty_parents(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.batch_fetch(conn, [], 3)
        assert result["rows"] == []
        assert result["queries"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
