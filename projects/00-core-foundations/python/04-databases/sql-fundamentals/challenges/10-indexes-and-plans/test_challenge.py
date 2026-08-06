"""
Challenge 10: indexes-and-plans — Hidden Tests
===============================================
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


class TestPlanFor:
    def test_returns_details(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        conn.execute("CREATE INDEX idx_t_v ON t(v)")
        # enough rows that the planner prefers the index over a scan
        conn.executemany("INSERT INTO t (v) VALUES (?)",
                         [(f"v{i % 7}",) for i in range(2000)])
        plans = solution_module.plan_for(conn, "SELECT * FROM t WHERE v = ?", ("v3",))
        assert any("SEARCH t USING" in p and "idx_t_v" in p for p in plans)

    def test_scan_without_index(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        plans = solution_module.plan_for(conn, "SELECT * FROM t")
        assert any("SCAN t" in p for p in plans)


class TestSargableVsNot:
    def test_sargable_searches(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.sargable_vs_not(conn)
        assert any("SEARCH" in p for p in result["sargable"])

    def test_wrapped_scans(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.sargable_vs_not(conn)
        assert any("SCAN events" in p for p in result["wrapped"])

    def test_contrast(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.sargable_vs_not(conn)
        sarg = "".join(result["sargable"])
        wrap = "".join(result["wrapped"])
        assert "SEARCH" in sarg and "SEARCH" not in wrap


class TestCoveringVsTable:
    def test_projection_covered(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.covering_vs_table(conn)
        assert any("COVERING INDEX" in p for p in result["covering"])

    def test_star_not_covered(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.covering_vs_table(conn)
        assert not any("COVERING INDEX" in p for p in result["star"])

    def test_star_still_searches(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.covering_vs_table(conn)
        assert any("SEARCH events USING INDEX" in p for p in result["star"])


class TestIndexStrategy:
    def test_equality_range_searches(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.index_strategy(conn)
        plan = "".join(result["equality_range"])
        assert "SEARCH" in plan
        assert "idx_events_model_latency_created" in plan

    def test_order_by_no_temp_btree(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.index_strategy(conn)
        plan = "".join(result["order_by"])
        assert "TEMP B-TREE" not in plan
        assert "SEARCH" in plan

    def test_partial_index_used(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.index_strategy(conn)
        plan = "".join(result["partial"])
        assert "SEARCH" in plan
        assert "idx_events_active" in plan

    def test_row_counts_sane(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.index_strategy(conn)
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 5000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
