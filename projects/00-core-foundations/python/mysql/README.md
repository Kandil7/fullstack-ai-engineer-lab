# Python MySQL Tutorial

W3Schools-style Python MySQL tutorial using sqlite3 as a stand-in for MySQL.

All examples use Python's built-in `sqlite3` module — no pip install required. The SQL syntax is nearly identical to MySQL.

## Files

| File | Title | Topics |
|------|-------|--------|
| `01-getting-started.py` | Getting Started | MySQL connector concept, sqlite3 as stand-in, connection, cursor |
| `02-create-database.py` | Create Database | CREATE DATABASE concept, CREATE TABLE, data types |
| `03-create-table.py` | Create Table | Column types, constraints, PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| `04-insert.py` | Insert Data | INSERT single/multiple, parameterized queries, executemany, lastrowid |
| `05-select.py` | Select Data | SELECT *, SELECT columns, fetchone/fetchall/fetchmany |
| `06-where.py` | Where Clause | WHERE operators (=, <>, >, <, LIKE, IN, BETWEEN), AND/OR, NULL |
| `07-order-by.py` | Order By | ORDER BY ASC/DESC, multi-column sort |
| `08-delete.py` | Delete Data | DELETE FROM, WHERE clause, caution about deleting all rows |
| `09-update.py` | Update Data | UPDATE SET, WHERE clause, updating multiple columns |
| `10-drop-table.py` | Drop Table | DROP TABLE, IF EXISTS, ALTER TABLE basics |
| `11-join.py` | Joins | INNER JOIN, LEFT JOIN, creating related tables |
| `12-union.py` | Union | UNION, UNION ALL, combining SELECT results |

## How to Run

```bash
# Run any file directly
python 01-getting-started.py

# Run all files in order
for f in *.py; do python "$f"; done
```

## Prerequisites

- Python 3.6+
- No external packages required (sqlite3 is built-in)

## Reference

- [W3Schools Python MySQL Tutorial](https://www.w3schools.com/python/python_mysql_getstarted.asp)
- [sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
