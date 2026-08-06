"""
Challenge 05: filtering-advanced — Hidden Tests
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


def fresh_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE models (id INTEGER PRIMARY KEY, name TEXT, epoch INT, metric REAL)")
    conn.executemany(
        "INSERT INTO models (id, name, epoch, metric) VALUES (?, ?, ?, ?)",
        [(1, "bert", 1, 0.9), (2, "gpt", 2, 0.8), (3, "llm", 3, 0.7),
         (4, "t5", 4, None)])
    return conn


class TestFilterRange:
    def test_inclusive_bounds(self):
        conn = fresh_conn()
        result = solution_module.filter_range(conn, 0.7, 0.8)
        assert result == ["gpt", "llm"]

    def test_nulls_excluded(self):
        conn = fresh_conn()
        result = solution_module.filter_range(conn, 0.0, 10.0)
        assert "t5" not in result
        assert len(result) == 3

    def test_sorted_names(self):
        conn = fresh_conn()
        result = solution_module.filter_range(conn, 0.79, 0.91)
        assert result == ["bert", "gpt"]

    def test_no_matches(self):
        conn = fresh_conn()
        assert solution_module.filter_range(conn, 100.0, 200.0) == []


class TestPatternMatch:
    def test_percent_wildcard(self):
        conn = fresh_conn()
        result = solution_module.pattern_match(conn, "b%")
        assert result["names"] == ["bert"]

    def test_underscore_single_char(self):
        conn = fresh_conn()
        conn.execute("INSERT INTO models (id, name, epoch, metric) VALUES (5, 'bertX', 5, 0.5)")
        result = solution_module.pattern_match(conn, "bert_")
        assert result["names"] == ["bertX"]

    def test_single_underscore_count(self):
        conn = fresh_conn()
        conn.executemany(
            "INSERT INTO models (id, name, epoch, metric) VALUES (?, ?, ?, ?)",
            [(5, "bert_v2", 5, 0.5), (6, "gpt_3", 6, 0.5),
             (7, "plain", 7, 0.5), (8, "a_b_c", 8, 0.5)])
        result = solution_module.pattern_match(conn, "%")
        assert result["single_underscore"] == 3  # bert_v2, gpt_3, a_b_c

    def test_exact_match(self):
        conn = fresh_conn()
        result = solution_module.pattern_match(conn, "gpt")
        assert result["names"] == ["gpt"]


class TestNullAwareReport:
    def test_buckets(self):
        conn = fresh_conn()
        result = solution_module.null_aware_report(conn)
        assert result["buckets"] == {"ok": 3, "missing": 1}

    def test_with_runs(self):
        conn = fresh_conn()
        conn.execute("CREATE TABLE runs (id INTEGER PRIMARY KEY, model_id INTEGER)")
        conn.executemany("INSERT INTO runs (model_id) VALUES (?)", [(1,), (3,)])
        result = solution_module.null_aware_report(conn)
        assert result["with_runs"] == ["bert", "llm"]

    def test_empty_runs(self):
        conn = fresh_conn()
        conn.execute("CREATE TABLE runs (id INTEGER PRIMARY KEY, model_id INTEGER)")
        result = solution_module.null_aware_report(conn)
        assert result["with_runs"] == []

    def test_all_null(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE models (id INTEGER PRIMARY KEY, name TEXT, epoch INT, metric REAL)")
        conn.executemany(
            "INSERT INTO models (id, name, epoch, metric) VALUES (?, ?, ?, NULL)",
            [(1, "a", 1), (2, "b", 2)])
        result = solution_module.null_aware_report(conn)
        assert result["buckets"] == {"ok": 0, "missing": 2}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
