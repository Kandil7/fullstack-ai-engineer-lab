# MySQL Lecture 10: Dropping Tables

## 🎯 Topic Overview

Dropping Tables — DROP TABLE

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Understand the syntax and purpose of dropping tables
2. Write correct SQL statements
3. Combine with other SQL clauses
4. Handle edge cases and common errors
5. Apply best practices

---

## 1. Introduction

This lecture covers dropping tables in MySQL using Python's sqlite3 as a learning companion.

---

## 2. Core Concepts

### 1. DROP TABLE

`DROP TABLE users;` permanently removes table and data. Irreversible!

### 2. TRUNCATE TABLE

`TRUNCATE TABLE users;` removes all rows but keeps table structure.

### 3. DROP vs TRUNCATE vs DELETE

DROP removes table+data. TRUNCATE removes data only. DELETE removes rows with WHERE.

### 4. Foreign Keys

Cannot DROP a table referenced by a FOREIGN KEY without dropping constraints first.

---

## 3. Common Mistakes

### Forgetting to commit
Always commit after INSERT, UPDATE, or DELETE:
```python
# WRONG
cursor.execute("INSERT ...")
conn.close()  # Changes lost!

# RIGHT
cursor.execute("INSERT ...")
conn.commit()
conn.close()
```

### SQL Injection vulnerability
Never use string formatting for SQL queries:
```python
# WRONG - string concatenation is dangerous
name_input = "Alice' OR '1'='1"
query = "SELECT * FROM users WHERE name = '" + name_input + "'"
# Executes: SELECT * FROM users WHERE name = 'Alice' OR '1'='1'

# RIGHT - parameterized queries are safe
cursor.execute("SELECT * FROM users WHERE name = ?", (name_input,))
```

### Not handling errors
Always wrap database operations in try/except/finally:
```python
try:
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Error: {e}")
    if conn: conn.rollback()
finally:
    if conn: conn.close()
```

---

## 4. Best Practices

1. Always use **parameterized queries** to prevent SQL injection
2. **Commit** only when all operations succeed - use transactions
3. **Close connections** with try/finally or context managers
4. **Validate input** before database operations
5. Use **appropriate indexes** for query performance
6. **Test with in-memory databases** before using real ones

---

## 5. Practice Exercises

### Exercise 1: Basic Operations
Write code that connects to an in-memory database, creates a table, inserts 5 sample rows, queries them, and properly cleans up.

### Exercise 2: Advanced Queries
Using the same table, write queries that filter with WHERE, sort with ORDER BY, and limit results with LIMIT.

### Exercise 3: Error Handling
Write a function that executes any SQL query safely with error handling and always closes the connection.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Syntax | Standard SQL patterns work across databases |
| Safety | Parameterized queries prevent SQL injection |
| Transactions | Commit saves changes, rollback undoes them |
| Error Handling | Always use try/except/finally
| Cleanup | Close connections to free resources
