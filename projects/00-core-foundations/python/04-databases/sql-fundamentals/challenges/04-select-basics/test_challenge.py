"""
Challenge 04: select-basics — Hidden Tests
===========================================
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


def fresh_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE models (id INTEGER PRIMARY KEY, name TEXT, epoch INT, metric REAL)")
    conn.executemany(
        "INSERT INTO models (name, epoch, metric) VALUES (?, ?, ?)",
        [("bert", 1, 0.9), ("gpt", 2, 0.8), ("llm", 3, 0.7), ("t5", 4, 0.85)])
    return conn


class TestTopN:
    def test_top_two(self):
        conn = fresh_conn()
        assert solution_module.top_n(conn, 2) == [("bert", 0.9), ("t5", 0.85)]

    def test_all(self):
        conn = fresh_conn()
        result = solution_module.top_n(conn, 10)
        assert [name for name, _ in result] == ["bert", "t5", "gpt", "llm"]

    def test_tie_break_by_name(self):
        conn = fresh_conn()
        conn.execute(
            "INSERT INTO models (name, epoch, metric) VALUES ('aaa', 9, 0.8)")
        result = solution_module.top_n(conn, 5)
        # bert 0.9, t5 0.85, aaa 0.8, gpt 0.8, llm 0.7 — aaa before gpt on the tie
        assert [name for name, _ in result] == ["bert", "t5", "aaa", "gpt", "llm"]

    def test_empty_table(self):
        conn = sqlite3.connect(":memory:")
        assert solution_module.top_n(conn, 3) == []


class TestMetricReport:
    def test_report_with_scores(self):
        conn = fresh_conn()
        result = solution_module.metric_report(conn)
        assert result["report"] == [
            ("bert", 90.0), ("t5", 85.0), ("gpt", 80.0), ("llm", 70.0)]
        assert result["distinct_names"] == 4

    def test_distinct_names(self):
        conn = fresh_conn()
        conn.execute(
            "INSERT INTO models (name, epoch, metric) VALUES ('bert', 5, 0.99)")
        result = solution_module.metric_report(conn)
        assert result["distinct_names"] == 4

    def test_empty(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.metric_report(conn)
        assert result["report"] == []
        assert result["distinct_names"] == 0


class TestPaginate:
    def test_first_page(self):
        conn = fresh_conn()
        result = solution_module.paginate(conn, 2, 1)
        assert [name for name, _ in result["rows"]] == ["bert", "t5"]
        assert result["total"] == 4
        assert result["has_next"] is True

    def test_last_page(self):
        conn = fresh_conn()
        result = solution_module.paginate(conn, 2, 3)
        assert result["rows"] == []
        assert result["total"] == 4
        assert result["has_next"] is False

    def test_page_out_of_range(self):
        conn = fresh_conn()
        result = solution_module.paginate(conn, 3, 2)
        assert [name for name, _ in result["rows"]] == ["llm"]
        assert result["has_next"] is False

    def test_page_zero_treated_as_one(self):
        conn = fresh_conn()
        result = solution_module.paginate(conn, 2, 0)
        assert [name for name, _ in result["rows"]] == ["bert", "t5"]

    def test_negative_page_treated_as_one(self):
        conn = fresh_conn()
        result = solution_module.paginate(conn, 4, -3)
        assert len(result["rows"]) == 4
        assert result["has_next"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
