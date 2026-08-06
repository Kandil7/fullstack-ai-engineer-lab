"""
Challenge 12: normalization — Hidden Tests
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


class TestSplitCsvColumn:
    def test_splits_csv(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE contacts (id INTEGER PRIMARY KEY, email TEXT, tags_csv TEXT)")
        conn.executemany("INSERT INTO contacts (id, email, tags_csv) VALUES (?, ?, ?)",
                         [(1, "a@x.com", "ml,db"), (2, "b@x.com", "sql")])
        result = solution_module.split_csv_column(conn)
        assert result == [(1, "db"), (1, "ml"), (2, "sql")]

    def test_empty_tags(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE contacts (id INTEGER PRIMARY KEY, email TEXT, tags_csv TEXT)")
        conn.execute("INSERT INTO contacts (id, email, tags_csv) VALUES (1, 'a@x.com', '')")
        result = solution_module.split_csv_column(conn)
        assert result == []

    def test_creates_tables(self):
        conn = sqlite3.connect(":memory:")
        assert solution_module.split_csv_column(conn) == []


class TestSplitDepartments:
    def test_distinct_departments(self):
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, "
            "dept_name TEXT, dept_location TEXT)")
        conn.executemany(
            "INSERT INTO employees (name, dept_name, dept_location) VALUES (?, ?, ?)",
            [("ana", "eng", "floor1"), ("bob", "eng", "floor1"),
             ("cam", "ml", "floor2")])
        result = solution_module.split_departments(conn)
        assert result["departments"] == 2
        assert result["employees"] == 3
        assert result["locations"] == ["floor1", "floor2"]

    def test_department_count_not_employee_count(self):
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, "
            "dept_name TEXT, dept_location TEXT)")
        conn.executemany(
            "INSERT INTO employees (name, dept_name, dept_location) VALUES (?, ?, ?)",
            [("a", "eng", "f1"), ("b", "eng", "f1"), ("c", "eng", "f1")])
        result = solution_module.split_departments(conn)
        assert result["departments"] == 1
        assert result["employees"] == 3


class TestBuildStarSchema:
    def _log(self):
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE events_log (date TEXT, user TEXT, product TEXT, amount REAL)")
        conn.executemany(
            "INSERT INTO events_log (date, user, product, amount) VALUES (?, ?, ?, ?)",
            [("2026-08-01", "ana", "gpu", 10.0), ("2026-08-01", "ana", "cpu", 5.0),
             ("2026-08-02", "bob", "gpu", 7.5)])
        return conn

    def test_fact_count(self):
        conn = self._log()
        result = solution_module.build_star_schema(conn)
        assert result["facts"] == 3

    def test_dimension_counts(self):
        conn = self._log()
        result = solution_module.build_star_schema(conn)
        assert result["dims"]["date"] == 2
        assert result["dims"]["user"] == 2
        assert result["dims"]["product"] == 2

    def test_reconstructed_equals_log(self):
        conn = self._log()
        result = solution_module.build_star_schema(conn)
        assert len(result["reconstructed"]) == 3
        amounts = sorted(r[3] for r in result["reconstructed"])
        assert amounts == [5.0, 7.5, 10.0]

    def test_empty_log(self):
        conn = sqlite3.connect(":memory:")
        result = solution_module.build_star_schema(conn)
        assert result["facts"] == 0
        assert result["reconstructed"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
