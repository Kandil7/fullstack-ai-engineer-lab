"""
Challenge 09: window-functions — Hidden Tests
==============================================
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


def runs_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE runs (id INTEGER PRIMARY KEY, model TEXT, run_ts INT, metric REAL)")
    conn.executemany(
        "INSERT INTO runs (model, run_ts, metric) VALUES (?, ?, ?)",
        [("bert", 1, 0.9), ("bert", 2, 0.9), ("bert", 3, 0.8),
         ("gpt", 1, 0.7), ("gpt", 2, 0.75)])
    return conn


class TestRankRows:
    def test_bert_ties(self):
        conn = runs_conn()
        bert = [r for r in solution_module.rank_rows(conn) if r[0] == "bert"]
        # (model, metric, rn, rank, dense)
        assert bert[0][1:5] == (0.9, 1, 1, 1)
        assert bert[1][1:5] == (0.9, 2, 1, 1)
        assert bert[2][1:5] == (0.8, 3, 3, 2)

    def test_partition_restart(self):
        conn = runs_conn()
        gpt = [r for r in solution_module.rank_rows(conn) if r[0] == "gpt"]
        assert gpt[0][2] == 1  # ROW_NUMBER restarts at 1 per model

    def test_row_count(self):
        conn = runs_conn()
        assert len(solution_module.rank_rows(conn)) == 5


class TestLagDelta:
    def test_delta_computation(self):
        conn = runs_conn()
        bert = [r for r in solution_module.lag_delta(conn) if r[0] == "bert"]
        assert bert[0][3] is None
        assert bert[1][3] == pytest.approx(0.0)
        assert bert[2][3] == pytest.approx(-0.1)

    def test_partition_boundary_null(self):
        conn = runs_conn()
        gpt = [r for r in solution_module.lag_delta(conn) if r[0] == "gpt"]
        assert gpt[0][3] is None

    def test_order_by_run_ts(self):
        conn = runs_conn()
        rows = solution_module.lag_delta(conn)
        bert = [r for r in rows if r[0] == "bert"]
        assert [r[1] for r in bert] == [1, 2, 3]


class TestFramesReport:
    def test_running_total(self):
        conn = runs_conn()
        bert = [r for r in solution_module.frames_report(conn) if r[0] == "bert"]
        assert [r[3] for r in bert] == [pytest.approx(0.9), pytest.approx(1.8),
                                        pytest.approx(2.6)]

    def test_moving_average_edges(self):
        conn = runs_conn()
        bert = [r for r in solution_module.frames_report(conn) if r[0] == "bert"]
        assert bert[0][4] == pytest.approx(0.9)
        assert bert[1][4] == pytest.approx(0.9)
        assert bert[2][4] == pytest.approx((0.9 + 0.9 + 0.8) / 3)

    def test_partition_isolation(self):
        conn = runs_conn()
        rows = solution_module.frames_report(conn)
        gpt = [r for r in rows if r[0] == "gpt"]
        # First gpt row's running total must not include bert rows
        assert gpt[0][3] == pytest.approx(0.7)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
