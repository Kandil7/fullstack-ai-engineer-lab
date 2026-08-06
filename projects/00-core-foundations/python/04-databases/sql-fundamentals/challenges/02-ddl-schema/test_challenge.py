"""
Challenge 02: ddl-schema — Hidden Tests
========================================
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


class TestCreateProductsTable:
    def test_negative_price_rejected(self):
        conn = fresh_conn()
        solution_module.create_products_table(conn)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO products (sku, price) VALUES ('A', -5)")

    def test_null_sku_rejected(self):
        conn = fresh_conn()
        solution_module.create_products_table(conn)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO products (sku, price) VALUES (NULL, 1.0)")

    def test_duplicate_sku_rejected(self):
        conn = fresh_conn()
        solution_module.create_products_table(conn)
        conn.execute("INSERT INTO products (sku, price) VALUES ('A', 1.0)")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO products (sku, price) VALUES ('A', 2.0)")

    def test_default_stock_zero(self):
        conn = fresh_conn()
        solution_module.create_products_table(conn)
        conn.execute("INSERT INTO products (sku, price) VALUES ('A', 1.0)")
        stock = conn.execute(
            "SELECT stock FROM products WHERE sku = 'A'").fetchone()[0]
        assert stock == 0

    def test_table_actually_exists(self):
        conn = fresh_conn()
        solution_module.create_products_table(conn)
        names = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")]
        assert "products" in names


class TestAddStatusAndBackfill:
    def _setup(self, conn, n=2500, premium=800):
        solution_module.create_products_table(conn)
        rows = [(f"sku{i}", 100.0 if i < premium else 10.0) for i in range(n)]
        conn.executemany(
            "INSERT INTO products (sku, price) VALUES (?, ?)", rows)

    def test_full_backfill(self):
        conn = fresh_conn()
        self._setup(conn)
        result = solution_module.add_status_and_backfill(conn)
        assert result["rows"] == 2500
        assert result["premium"] == 800

    def test_empty_table(self):
        conn = fresh_conn()
        solution_module.create_products_table(conn)
        result = solution_module.add_status_and_backfill(conn)
        assert result == {"rows": 0, "premium": 0}

    def test_batching_respects_chunk_boundary(self):
        conn = fresh_conn()
        self._setup(conn, n=2500, premium=2500)
        result = solution_module.add_status_and_backfill(conn)
        assert result["premium"] == 2500

    def test_no_null_left_behind(self):
        conn = fresh_conn()
        self._setup(conn)
        solution_module.add_status_and_backfill(conn)
        nulls = conn.execute(
            "SELECT COUNT(*) FROM products WHERE status IS NULL").fetchone()[0]
        assert nulls == 0


class TestCreateAuditSchema:
    def test_cascade_deletes_items(self):
        conn = fresh_conn()
        result = solution_module.create_audit_schema(conn)
        assert result["items"] == 0

    def test_generated_total(self):
        conn = fresh_conn()
        result = solution_module.create_audit_schema(conn)
        assert result["generated"] == pytest.approx(14.5)

    def test_generated_column_is_stored(self):
        conn = fresh_conn()
        solution_module.create_audit_schema(conn)
        cols = conn.execute("PRAGMA table_xinfo(order_items)").fetchall()
        total_col = [c for c in cols if c[1] == "total"]
        assert len(total_col) == 1
        assert "REAL" in total_col[0][2].upper()
        # hidden = 3 means STORED generated (table_info hides it entirely)
        assert total_col[0][6] == 3

    def test_engine_computes_total_not_python(self):
        """Direct INSERT must yield the engine-computed total."""
        conn = fresh_conn()
        solution_module.create_audit_schema(conn)
        conn.execute("INSERT INTO orders DEFAULT VALUES")
        oid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            "INSERT INTO order_items (order_id, qty, unit_price) VALUES (?, ?, ?)",
            (oid, 3, 2.0))
        total = conn.execute(
            "SELECT total FROM order_items WHERE order_id = ?", (oid,)).fetchone()[0]
        assert total == pytest.approx(6.0)

    def test_items_existed_before_delete(self):
        conn = fresh_conn()
        solution_module.create_audit_schema(conn)
        assert conn.execute(
            "SELECT COUNT(*) FROM order_items").fetchone()[0] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
