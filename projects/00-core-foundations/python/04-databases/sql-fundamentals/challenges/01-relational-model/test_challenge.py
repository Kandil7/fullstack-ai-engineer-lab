"""
Challenge 01: relational-model — Hidden Tests
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


def fresh_conn() -> sqlite3.Connection:
    return sqlite3.connect(":memory:")


class TestCreateRelationalSchema:
    def test_tables_created(self):
        conn = fresh_conn()
        tables = solution_module.create_relational_schema(conn)
        assert tables == ["courses", "enrollments", "students"]

    def test_students_primary_key(self):
        conn = fresh_conn()
        solution_module.create_relational_schema(conn)
        conn.execute("INSERT INTO students (name) VALUES ('ana')")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO students (id, name) VALUES (1, 'dupe')")

    def test_students_not_null(self):
        conn = fresh_conn()
        solution_module.create_relational_schema(conn)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO students (name) VALUES (NULL)")

    def test_enrollments_composite_pk(self):
        conn = fresh_conn()
        solution_module.create_relational_schema(conn)
        conn.execute("INSERT INTO students (name) VALUES ('ana')")
        conn.execute("INSERT INTO courses (title) VALUES ('sql')")
        conn.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (1, 1)")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO enrollments (student_id, course_id) VALUES (1, 1)")

    def test_enrollments_foreign_keys(self):
        conn = fresh_conn()
        solution_module.create_relational_schema(conn)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO enrollments (student_id, course_id) VALUES (999, 1)")


class TestEnforceKeys:
    def test_full_summary(self):
        conn = fresh_conn()
        solution_module.create_relational_schema(conn)
        result = solution_module.enforce_keys(conn)
        assert result["rows"] == 1
        assert result["dup_rejected"] is True
        assert result["orphan_rejected"] is True

    def test_works_on_existing_schema(self):
        conn = fresh_conn()
        solution_module.create_relational_schema(conn)
        result = solution_module.enforce_keys(conn)
        assert result["rows"] == 1

    def test_never_raises_on_bad_input(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT)")
        conn.execute(
            "CREATE TABLE enrollments (student_id INTEGER, course_id INTEGER)")
        # No FK enforcement available; function must still return a dict.
        result = solution_module.enforce_keys(conn)
        assert isinstance(result, dict)
        assert "rows" in result


class TestPurgeAbandonedCourses:
    def _setup(self, conn):
        solution_module.create_relational_schema(conn)
        conn.executemany("INSERT INTO courses (title) VALUES (?)",
                         [("c1",), ("c2",), ("c3",)])
        conn.execute("INSERT INTO students (name) VALUES ('ana')")
        conn.execute("INSERT INTO enrollments (student_id, course_id) VALUES (1, 1)")

    def test_purges_abandoned(self):
        conn = fresh_conn()
        self._setup(conn)
        remaining = solution_module.purge_abandoned_courses(conn)
        assert remaining == ["c1"]

    def test_deletes_rows(self):
        conn = fresh_conn()
        self._setup(conn)
        solution_module.purge_abandoned_courses(conn)
        count = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        assert count == 1

    def test_keeps_all_when_everyone_enrolled(self):
        conn = fresh_conn()
        solution_module.create_relational_schema(conn)
        conn.executemany("INSERT INTO courses (title) VALUES (?)",
                         [("a",), ("b",)])
        conn.execute("INSERT INTO students (name) VALUES ('ana')")
        conn.execute("INSERT INTO enrollments (student_id, course_id) VALUES (1, 1)")
        conn.execute("INSERT INTO enrollments (student_id, course_id) VALUES (1, 2)")
        assert solution_module.purge_abandoned_courses(conn) == ["a", "b"]

    def test_handles_null_enrollment_rows(self):
        conn = fresh_conn()
        self._setup(conn)
        conn.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (1, NULL)")
        remaining = solution_module.purge_abandoned_courses(conn)
        assert remaining == ["c1"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
