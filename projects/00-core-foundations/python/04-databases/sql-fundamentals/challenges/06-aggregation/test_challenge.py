"""
Challenge 06: aggregation — Hidden Tests
=========================================
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
        "CREATE TABLE runs (id INTEGER PRIMARY KEY, model TEXT, experiment TEXT, metric REAL)")
    conn.executemany(
        "INSERT INTO runs (model, experiment, metric) VALUES (?, ?, ?)",
        [("bert", "e1", 0.9), ("bert", "e1", 0.8), ("gpt", "e1", 0.7)])
    return conn


def test_data_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE runs (id INTEGER PRIMARY KEY, model TEXT, experiment TEXT, metric REAL)")
    conn.executemany(
        "INSERT INTO runs (model, experiment, metric) VALUES (?, ?, ?)",
        [("bert", "e1", 0.9), ("bert", "e1", 0.1), ("bert", "e2", 0.8),
         ("gpt", "e1", 0.6), ("gpt", "e2", 0.3)])
    return conn


class TestGroupTotals:
    def test_basic_totals(self):
        conn = fresh_conn()
        result = solution_module.group_totals(conn)
        assert result[0][0] == "bert"
        assert result[0][1] == 2
        assert result[0][2] == pytest.approx(1.7)
        assert result[0][3] == pytest.approx(0.85)
        assert result[1] == ("gpt", 1, 0.7, 0.7)

    def test_ordered_by_avg_desc(self):
        conn = fresh_conn()
        result = solution_module.group_totals(conn)
        avgs = [r[3] for r in result]
        assert avgs == sorted(avgs, reverse=True)

    def test_empty(self):
        conn = sqlite3.connect(":memory:")
        assert solution_module.group_totals(conn) == []


class TestHavingFilter:
    def test_requires_min_runs(self):
        conn = fresh_conn()
        result = solution_module.having_filter(conn, 2, 0.0)
        assert [r[0] for r in result] == ["bert"]

    def test_requires_min_avg(self):
        conn = fresh_conn()
        result = solution_module.having_filter(conn, 1, 0.75)
        assert [r[0] for r in result] == ["bert"]

    def test_both_conditions(self):
        conn = fresh_conn()
        result = solution_module.having_filter(conn, 2, 0.75)
        assert result[0][0] == "bert"
        assert result[0][1] == 2
        assert result[0][2] == pytest.approx(0.85)

    def test_no_match(self):
        conn = fresh_conn()
        assert solution_module.having_filter(conn, 10, 0.0) == []


class TestAggregateReport:
    def test_distinct_experiments(self):
        conn = test_data_conn()
        result = solution_module.aggregate_report(conn)
        bert = [r for r in result["rows"] if r[0] == "bert"][0]
        assert bert[1] == 2  # e1, e2
        assert bert[2] == 2  # 0.1 filtered out by WHERE >= 0.5
        assert bert[3] == pytest.approx(0.9)

    def test_global_avg(self):
        conn = test_data_conn()
        result = solution_module.aggregate_report(conn)
        # filtered rows: 0.9, 0.8, 0.6 -> avg 0.7666...
        assert result["global_avg"] == pytest.approx(0.7666666666666666)

    def test_order_by_best(self):
        conn = test_data_conn()
        result = solution_module.aggregate_report(conn)
        assert result["rows"][0][0] == "bert"

    def test_empty(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.aggregate_report(conn)
        assert result["rows"] == []
        assert result["global_avg"] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
