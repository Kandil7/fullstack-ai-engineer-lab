"""
W3Schools Python Tutorial - MySQL 01: Getting Started with MySQL in Python
============================================
Topics: MySQL connector concept, sqlite3 as stand-in, connection, cursor

Run: python 01-getting-started.py
Reference: https://www.w3schools.com/python/python_mysql_getstarted.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: MySQL Connector Concept
# ============================================================

# Example 1: Why sqlite3 as a stand-in
# In production, you would use: pip install mysql-connector-python
# Then import mysql.connector instead of sqlite3
# The API is very similar — both provide connection and cursor objects
print("=== MySQL Connector Concept ===")
print("In production: import mysql.connector")
print("For learning:  import sqlite3 (built-in, no install needed)")
print()

# ============================================================
# Section: Establishing a Connection
# ============================================================

# Example 2: Basic connection to a database (creates file if not exists)
conn = sqlite3.connect(":memory:")
print("Connection established successfully!")
print(f"Connection type: {type(conn)}")
print()

# Example 3: Connecting to a file-based database
# In MySQL: conn = mysql.connector.connect(host="localhost", user="root", password="password", database="mydb")
# In sqlite3: conn = sqlite3.connect("mydatabase.db")
conn_file = sqlite3.connect(":memory:")
print("File-based connection would use: sqlite3.connect('mydatabase.db')")
print()

# ============================================================
# Section: Creating a Cursor
# ============================================================

# Example 4: Creating a cursor object
cursor = conn.cursor()
print("Cursor created successfully!")
print(f"Cursor type: {type(cursor)}")
print()

# Example 5: Cursor methods overview
# cursor.execute(sql)       - Execute a single SQL query
# cursor.executemany(sql)   - Execute SQL with multiple parameter sets
# cursor.fetchone()         - Fetch one row
# cursor.fetchall()         - Fetch all rows
# cursor.fetchmany(size)    - Fetch specified number of rows
# cursor.rowcount           - Number of rows affected
print("Key cursor methods:")
print("  execute(sql)      - Run a SQL query")
print("  executemany(sql)  - Run SQL with multiple params")
print("  fetchone()        - Get one row")
print("  fetchall()        - Get all rows")
print("  fetchmany(size)   - Get N rows")
print("  rowcount          - Rows affected count")
print()

# ============================================================
# Section: Running Your First Query
# ============================================================

# Example 6: CREATE TABLE using cursor
cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    )
""")
print("Table 'users' created successfully!")
print()

# Example 7: INSERT data
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
conn.commit()
print("Inserted one row. Rows affected:", cursor.rowcount)
print()

# Example 8: SELECT data
cursor.execute("SELECT * FROM users")
result = cursor.fetchone()
print("Query result:", result)
print()

# ============================================================
# Section: Committing Changes
# ============================================================

# Example 9: Understanding commit and rollback
# In MySQL, you must commit after INSERT, UPDATE, DELETE
# sqlite3 works the same way
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
conn.commit()  # Save changes
print("Changes committed!")

# You can also rollback
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Charlie", 35))
conn.rollback()  # Undo changes
print("Changes rolled back!")
print()

# ============================================================
# Section: Closing Connection
# ============================================================

# Example 10: Properly closing the connection
cursor.close()
conn.close()
print("Connection closed.")
print()

# ============================================================
# Section: Complete Pattern
# ============================================================

# Example 11: Full try/except pattern for database operations
print("=== Complete Connection Pattern ===")
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
finally:
    if conn:
        conn.close()
        print("Connection closed in finally block.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. Use sqlite3.connect() to establish a connection")
print("2. Create a cursor with conn.cursor()")
print("3. Use cursor.execute() to run SQL queries")
print("4. Call conn.commit() after modifying data")
print("5. Use fetchone/fetchall/fetchmany to retrieve results")
print("6. Always close cursor and connection when done")
print("7. Wrap database operations in try/except for error handling")
print("=" * 60)
