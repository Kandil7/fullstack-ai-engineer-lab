"""
Challenge 08: subqueries-ctes — Hidden Tests
=============================================
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


def cust_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL)")
    conn.executemany("INSERT INTO customers (name) VALUES (?)", [("ana",), ("bob",), ("cam",)])
    conn.executemany(
        "INSERT INTO orders (customer_id, amount) VALUES (?, ?)",
        [(1, 10.0), (1, 20.0), (2, 30.0)])
    return conn


class TestScalarReport:
    def test_spend_order(self):
        conn = cust_conn()
        result = solution_module.scalar_report(conn)
        assert result["rows"] == [("ana", 30.0), ("bob", 30.0), ("cam", 0.0)]

    def test_avg_spend(self):
        conn = cust_conn()
        result = solution_module.scalar_report(conn)
        assert result["avg_spend"] == pytest.approx(20.0)

    def test_empty_orders(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.scalar_report(conn)
        assert result["rows"] == []
        assert result["avg_spend"] is None


class TestAntiJoin:
    def test_both_lists_agree(self):
        conn = cust_conn()
        result = solution_module.anti_join(conn)
        assert result["not_exists"] == ["cam"]
        assert result["left_join"] == ["cam"]
        assert result["identical"] is True

    def test_no_customers_without_orders(self):
        conn = cust_conn()
        conn.execute("INSERT INTO orders (customer_id, amount) VALUES (3, 5.0)")
        result = solution_module.anti_join(conn)
        assert result["not_exists"] == []
        assert result["identical"] is True

    def test_creates_tables(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.anti_join(conn)
        assert result["identical"] is True


class TestRecursiveSpine:
    def test_zero_fill(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, date TEXT)")
        conn.executemany("INSERT INTO events (date) VALUES (?)",
                         [("2026-08-01",), ("2026-08-03",)])
        result = solution_module.recursive_spine(conn, "2026-08-01", "2026-08-03")
        assert result == [
            ("2026-08-01", 1), ("2026-08-02", 0), ("2026-08-03", 1)]

    def test_single_day(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, date TEXT)")
        conn.execute("INSERT INTO events (date) VALUES ('2026-08-01')")
        result = solution_module.recursive_spine(conn, "2026-08-01", "2026-08-01")
        assert result == [("2026-08-01", 1)]

    def test_creates_table(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.recursive_spine(conn, "2026-01-01", "2026-01-03")
        assert len(result) == 3
        assert result[0] == ("2026-01-01", 0)

    def test_long_span_bounded(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, date TEXT)")
        result = solution_module.recursive_spine(conn, "2026-01-01", "2026-12-31")
        assert len(result) == 365


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
