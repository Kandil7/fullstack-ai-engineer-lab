# MySQL Lecture 01: Getting Started with MySQL in Python

## 🎯 Topic Overview

MySQL is one of the world's most popular open-source relational database management systems. When combined with Python, it provides a powerful stack for building data-driven applications. This lecture introduces the MySQL connector concept, establishing connections, creating cursors, and running basic queries using Python's `sqlite3` as a learning stand-in for MySQL.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the MySQL connector concept and its purpose
2. Establish a database connection in Python
3. Create and use cursor objects for query execution
4. Run basic SQL queries (CREATE, INSERT, SELECT)
5. Understand committing changes and the transaction lifecycle
6. Implement proper connection management with try/except/finally

---

## 1. MySQL Connector Concept

### What is a Database Connector?

A database connector is a software library that enables communication between Python and a database server. It translates Python function calls into database protocol commands and back.

### MySQL Connector Options

| Connector | Installation | Pros | Cons |
|-----------|-------------|------|------|
| `mysql-connector-python` | `pip install mysql-connector-python` | Official Oracle connector, pure Python | Slightly slower |
| `PyMySQL` | `pip install pymysql` | Pure Python, simple API | No C extension |
| `mysqlclient` | `pip install mysqlclient` | Fastest (C extension) | Requires C compiler |

### Why sqlite3 for Learning?

```python
# In production, you'd use:
# import mysql.connector
# conn = mysql.connector.connect(host="localhost", user="root", password="...")

# For learning, sqlite3 is built-in and SQL syntax is nearly identical:
import sqlite3
conn = sqlite3.connect(":memory:")
```

**Key insight:** SQL is SQL. MySQL and SQLite share ~90% of their syntax. Learning with sqlite3 teaches you skills that transfer directly to MySQL.

---

## 2. Establishing a Connection

### Connection Types

```python
import sqlite3

# In-memory database (temporary, fast for learning)
conn = sqlite3.connect(":memory:")

# File-based database (persistent)
# conn = sqlite3.connect("mydatabase.db")

# MySQL equivalent:
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="password",
#     database="mydb"
# )
```

### Connection Object

The connection object (`conn`) is your gateway to the database:

```python
print(type(conn))  # <class 'sqlite3.Connection'>

# Key connection methods:
# conn.cursor()     — Create a cursor
# conn.commit()     — Save changes
# conn.rollback()   — Undo pending changes
# conn.close()      — Close the connection
```

---

## 3. Creating a Cursor

A cursor is an object that executes SQL queries and fetches results.

```python
cursor = conn.cursor()
print(type(cursor))  # <class 'sqlite3.Cursor'>
```

### Cursor Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `execute(sql)` | Run a single SQL query | `cursor.execute("SELECT * FROM users")` |
| `executemany(sql, seq)` | Run SQL with multiple params | `cursor.executemany("INSERT ...", data)` |
| `fetchone()` | Get one result row | `row = cursor.fetchone()` |
| `fetchall()` | Get all result rows | `rows = cursor.fetchall()` |
| `fetchmany(size)` | Get N rows | `rows = cursor.fetchmany(5)` |
| `rowcount` | Rows affected by last operation | `cursor.rowcount` |

---

## 4. Running Your First Queries

### CREATE TABLE

```python
cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    )
""")
print("Table created!")
```

### INSERT

```python
# Using parameterized queries (safe from SQL injection)
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
conn.commit()
print(f"Inserted {cursor.rowcount} row(s)")
```

### SELECT

```python
cursor.execute("SELECT * FROM users")
row = cursor.fetchone()
print(f"Result: {row}")
```

---

## 5. Committing and Rolling Back

### The Transaction Lifecycle

```
BEGIN TRANSACTION (implicit)
    → Execute SQL statements
    → commit() — Save changes permanently
    → rollback() — Undo all pending changes
END TRANSACTION
```

```python
# Commit saves changes
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
conn.commit()  # Bob is now saved

# Rollback undoes pending changes
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Charlie", 35))
conn.rollback()  # Charlie is NOT saved
```

### Auto-Commit

By default, sqlite3 requires explicit `commit()`. You can enable auto-commit:

```python
conn = sqlite3.connect(":memory:", isolation_level=None)
# Now every statement commits immediately (like MySQL's auto-commit mode)
```

---

## 6. Complete Connection Pattern

Always use try/except/finally for database operations:

```python
try:
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, val TEXT)")
    cursor.execute("INSERT INTO test (val) VALUES (?)", ("hello",))
    conn.commit()
    
    cursor.execute("SELECT * FROM test")
    print("Result:", cursor.fetchone())
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    conn.rollback()  # Undo any partial changes
    
finally:
    if conn:
        conn.close()
        print("Connection closed.")
```

---

## 7. Common Mistakes

### Mistake 1: Forgetting to commit
```python
# WRONG — changes not saved!
cursor.execute("INSERT INTO users ...")
conn.close()

# RIGHT
cursor.execute("INSERT INTO users ...")
conn.commit()
conn.close()
```

### Mistake 2: SQL injection vulnerability
```python
# WRONG — string formatting is dangerous
name = "Alice'; DROP TABLE users;--"
cursor.execute(f"INSERT INTO users (name) VALUES ('{name}')")

# RIGHT — parameterized queries
cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
```

### Mistake 3: Not closing connections
```python
# WRONG — connection leak
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
# conn never closed!

# RIGHT — use context manager or finally
with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    # Connection auto-closes
```

---

## 8. Best Practices

1. **Always use parameterized queries** — never use string formatting for SQL
2. **Use context managers** — `with sqlite3.connect(...) as conn:` handles cleanup
3. **Commit explicitly** — control exactly when changes are saved
4. **Wrap operations in try/except** — handle database errors gracefully
5. **Close connections** — free database resources promptly
6. **Use `rowcount`** — verify operations affected the expected number of rows
7. **Separate SQL logic** — keep database code isolated from business logic

---

## 9. Practice Exercises

### Exercise 1: Connection Management
```python
# Write a function that:
# - Connects to an in-memory database
# - Creates a 'products' table with id, name, price columns
# - Inserts 3 products
# - Queries and prints all products
# - Handles errors and closes connection
```

### Exercise 2: Parameterized Queries
```python
# Create a function insert_user(name, age) that:
# - Takes name and age as parameters
# - Inserts into the users table
# - Returns the number of rows affected
# - Is safe from SQL injection
```

### Exercise 3: Transaction Demo
```python
# Write code that demonstrates:
# - A successful transaction (commit)
# - A rolled-back transaction (rollback after insert)
# - Verify the rolled-back data is not in the database
```

---

## 10. Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Connector** | Library bridging Python and MySQL |
| **Connection** | `sqlite3.connect()` / `mysql.connector.connect()` |
| **Cursor** | Object for executing SQL and fetching results |
| **Parameterized** | Always use `?` placeholders for safety |
| **Commit** | Required to persist changes |
| **Close** | Always close connections when done |

### Key Takeaways

1. MySQL connectors translate Python calls to database protocol
2. sqlite3 is a great learning tool — SQL skills transfer to MySQL
3. Cursors execute SQL and fetch results
4. Commit changes explicitly after INSERT, UPDATE, DELETE
5. Parameterized queries prevent SQL injection

---

## 📚 Next Lecture

→ [02-create-database-lecture.md](./02-create-database-lecture.md) — Creating and Managing Databases
