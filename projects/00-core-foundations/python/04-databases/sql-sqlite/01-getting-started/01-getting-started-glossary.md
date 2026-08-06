# MySQL Lecture 01: Getting Started — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Connector | Library that bridges Python and MySQL | `import mysql.connector` |
| Cursor | Object for executing SQL and fetching results | `cursor.execute("SELECT ...")` |
| Connection | Open session with a database | `conn = sqlite3.connect(":memory:")` |
| Commit | Permanently save pending changes | `conn.commit()` |
| Rollback | Undo pending changes since last commit | `conn.rollback()` |
| Parameterized | Using placeholders in SQL for safety | `"WHERE name = ?"` |
| fetchone | Get one result row | `cursor.fetchone()` |
| fetchall | Get all result rows | `cursor.fetchall()` |
| rowcount | Number of rows affected by last operation | `cursor.rowcount` |
| DDL | Data Definition Language (CREATE, ALTER, DROP) | `CREATE TABLE` |
| DML | Data Manipulation Language (INSERT, UPDATE, DELETE) | `INSERT INTO` |
| DQL | Data Query Language (SELECT) | `SELECT * FROM` |

## Key Terms

### Commit
Permanently saving all pending database changes. In MySQL (with InnoDB), changes are not visible to other connections until committed.
```python
conn.commit()
```

### Cursor
A database cursor that executes SQL statements and retrieves results. Always create via `conn.cursor()`.
```python
cursor = conn.cursor()
cursor.execute("SELECT 1")
```

### Parameterized Query
Using `?` placeholders instead of string formatting to prevent SQL injection.
```python
# Safe
cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
# Dangerous
cursor.execute(f"INSERT INTO users (name) VALUES ('{name}')")
```

### Rollback
Discard all pending changes since the last commit. Useful in error recovery.
```python
try:
    # ... database operations ...
    conn.commit()
except:
    conn.rollback()
```
