# MySQL Lecture 02: Creating and Managing Databases

## 🎯 Topic Overview

CREATE DATABASE syntax, USE database, DROP DATABASE, and viewing databases with SHOW DATABASES.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Create new databases using CREATE DATABASE
2. Select and switch between databases with USE
3. Drop databases safely with DROP DATABASE
4. List available databases
5. Understand sqlite3 vs MySQL database creation differences

---

## 1. Introduction

This lecture covers creating and managing databases in MySQL using Python's sqlite3 as a learning companion.

---

## 2. Core Concepts

### 1. CREATE DATABASE

In MySQL, databases are created explicitly: `CREATE DATABASE mydb;`. In sqlite3, databases are created automatically when you connect: `sqlite3.connect('mydb.db')`.

```python
import sqlite3
# This creates a database file if it doesn't exist
conn = sqlite3.connect('mydatabase.db')
print("Database created (or opened) successfully!")
```

### 2. USE Database

In MySQL, `USE mydb;` selects which database to operate on. In sqlite3, you select the database at connection time — you can't switch databases without creating a new connection.

### 3. DROP DATABASE

`DROP DATABASE mydb;` permanently removes a database. In sqlite3, you simply delete the .db file.

```python
# For sqlite3, dropping a database means closing the connection
# and deleting the file
conn.close()
import os
os.remove('mydatabase.db')
print("Database deleted.")
```

### 4. SHOW DATABASES

`SHOW DATABASES;` lists all databases on the MySQL server. In sqlite3, this doesn't apply — each .db file is a separate database.

---

## 3. Common Mistakes

### Forgetting to close connections
```python
# WRONG
conn = sqlite3.connect('test.db')
# ... work ...
# conn never closed!

# RIGHT
conn = sqlite3.connect('test.db')
try:
    # ... work ...
finally:
    conn.close()
```

### Using reserved words as database names
```python
# WRONG
conn = sqlite3.connect('select.db')  # 'select' is a reserved word

# RIGHT
conn = sqlite3.connect('my_select_data.db')
```

---

## 4. Best Practices

1. Use descriptive database names
2. Always close connections when done
3. Use in-memory databases for testing
4. Handle database creation errors
5. Use IF NOT EXISTS / IF EXISTS for safety

---

## 5. Practice Exercises

### Exercise 1: Create and Connect
Create a new database file, connect to it, create a simple table, insert data, query it, and close the connection.

### Exercise 2: Error Handling
Write a function that attempts to connect to a database and handles FileNotFoundError or sqlite3.OperationalError gracefully.

### Exercise 3: Multiple Databases
Create two separate database files, insert data into each, and prove they are independent by querying both.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| CREATE DATABASE | Explicit in MySQL, automatic in sqlite3 |
| USE | Switch databases in MySQL, set at connect in sqlite3 |
| DROP DATABASE | Permanent deletion — use with extreme caution |
| SHOW DATABASES | List available databases |
| Cleanup | Always close connections to avoid corruption |
