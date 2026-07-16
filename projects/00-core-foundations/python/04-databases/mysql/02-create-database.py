"""
W3Schools Python Tutorial - MySQL 02: Create Database
============================================
Topics: CREATE DATABASE concept, CREATE TABLE with sqlite3, data types (INT, VARCHAR, TEXT, etc.)

Run: python 02-create-database.py
Reference: https://www.w3schools.com/python/python_mysql_create_db.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: CREATE DATABASE Concept
# ============================================================

# Example 1: In MySQL, you would create a database like this:
# CREATE DATABASE mydatabase;
# In sqlite3, the database is created automatically when you connect
print("=== CREATE DATABASE Concept ===")
print("MySQL:   CREATE DATABASE mydatabase;")
print("sqlite3: sqlite3.connect('mydatabase.db')  # auto-creates file")
print()

# Example 2: Creating a connection (equivalent to CREATE DATABASE)
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
print("Database connection established (in-memory).")
print()

# ============================================================
# Section: Data Types in MySQL vs sqlite3
# ============================================================

# Example 3: MySQL data types
print("=== MySQL Data Types ===")
mysql_types = {
    "INT": "Integer number",
    "VARCHAR(n)": "Variable-length string (max n chars)",
    "TEXT": "Long text string",
    "FLOAT": "Floating-point number",
    "DOUBLE": "Double-precision float",
    "DATE": "Date (YYYY-MM-DD)",
    "DATETIME": "Date and time",
    "BOOLEAN": "True/False (stored as 0/1)",
    "DECIMAL(p,s)": "Exact decimal with precision",
    "BLOB": "Binary large object",
}
for dtype, desc in mysql_types.items():
    print(f"  {dtype:<18} - {desc}")
print()

# Example 4: sqlite3 type affinity (maps to MySQL types)
print("=== sqlite3 Type Affinity ===")
print("sqlite3 uses type affinity instead of strict types:")
print("  INTEGER  -> maps to MySQL INT, BIGINT, etc.")
print("  REAL     -> maps to MySQL FLOAT, DOUBLE, DECIMAL")
print("  TEXT     -> maps to MySQL VARCHAR, TEXT, CHAR")
print("  BLOB     -> maps to MySQL BLOB, VARBINARY")
print("  NUMERIC  -> maps to MySQL DECIMAL, BOOLEAN")
print()

# ============================================================
# Section: CREATE TABLE with Data Types
# ============================================================

# Example 5: Creating a table with various MySQL-like data types
cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        salary REAL,
        department TEXT,
        hire_date TEXT,
        is_active INTEGER DEFAULT 1
    )
""")
print("Table 'employees' created with various data types!")
print()

# Example 6: Inserting data matching the types
employees = [
    (1, "John", "Doe", 30, 75000.50, "Engineering", "2023-01-15", 1),
    (2, "Jane", "Smith", 28, 82000.00, "Marketing", "2022-06-20", 1),
    (3, "Bob", "Johnson", 35, 65000.75, "Sales", "2021-03-10", 1),
    (4, "Alice", "Williams", 32, 90000.00, "Engineering", "2020-08-01", 1),
    (5, "Charlie", "Brown", 40, 55000.25, "HR", "2019-11-30", 0),
]

cursor.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    employees
)
conn.commit()
print(f"Inserted {len(employees)} employees.")
print()

# ============================================================
# Section: CREATE TABLE with Constraints
# ============================================================

# Example 7: MySQL constraints (using sqlite3 equivalents)
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER DEFAULT 0,
        category TEXT CHECK(length(category) > 0)
    )
""")
print("Table 'products' created with constraints!")
print()

# Example 8: Common constraints overview
print("=== MySQL Constraints ===")
constraints = {
    "PRIMARY KEY": "Unique identifier for each row",
    "NOT NULL": "Column cannot have NULL value",
    "DEFAULT value": "Default value if none specified",
    "UNIQUE": "All values in column must be different",
    "CHECK (condition)": "Values must satisfy a condition",
    "FOREIGN KEY": "References another table's column",
    "AUTO_INCREMENT": "Automatically generate sequential numbers",
}
for constraint, desc in constraints.items():
    print(f"  {constraint:<22} - {desc}")
print()

# ============================================================
# Section: Using SHOW TABLES Equivalent
# ============================================================

# Example 9: List all tables (sqlite3 equivalent of SHOW TABLES)
cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name
""")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")
print()

# ============================================================
# Section: DESCRIBE TABLE Equivalent
# ============================================================

# Example 10: Get table structure (equivalent to DESCRIBE table)
cursor.execute("PRAGMA table_info(employees)")
columns = cursor.fetchall()
print("Structure of 'employees' table:")
print(f"  {'ID':<5} {'Name':<15} {'Type':<10} {'NotNull':<10} {'Default':<10} {'PK':<5}")
for col in columns:
    print(f"  {col[0]:<5} {col[1]:<15} {col[2]:<10} {col[3]:<10} {str(col[4]):<10} {col[5]:<5}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

# Example 11: Drop tables to clean up
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("DROP TABLE IF EXISTS products")
conn.commit()
print("Tables dropped for cleanup.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. MySQL uses CREATE DATABASE; sqlite3 auto-creates on connect")
print("2. Key data types: INT, VARCHAR, TEXT, FLOAT, DATE, BOOLEAN")
print("3. sqlite3 uses type affinity: INTEGER, REAL, TEXT, BLOB")
print("4. Constraints: PRIMARY KEY, NOT NULL, DEFAULT, UNIQUE, CHECK")
print("5. Use sqlite_master to list tables (SHOW TABLES equivalent)")
print("6. Use PRAGMA table_info to describe table structure")
print("7. Always clean up test tables when done")
print("=" * 60)

# Close connection
conn.close()
