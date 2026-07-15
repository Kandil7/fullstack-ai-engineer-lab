"""
Exercise 18: Database Integration with FastAPI

Master SQLite database operations in FastAPI applications.
Topics: SQLite, async database connections, CRUD operations, connection pooling.

Prerequisites:
- SQLite basics, SQL CRUD operations
- FastAPI dependency injection (exercise 15)
- Pydantic models (exercise 03)

Estimated time: 60-90 minutes
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import sqlite3
import os

app = FastAPI(title="Database Integration Exercises")

DATABASE_URL = "exercises_18.db"

# ============================================================
# Exercise 18.1: Basic Database Connection & Setup
# ============================================================
"""
Problem:
    Create a FastAPI application that manages a "tasks" table in SQLite.
    Implement a startup event to create the table and a dependency
    to get database connections.

Table schema:
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )

Requirements:
    1. Create the table on application startup
    2. Write a get_db() dependency that yields a connection
    3. Write a get_db_cursor() dependency that yields a cursor
    4. Ensure connections are properly closed after each request
    5. Implement a GET /health endpoint that verifies DB connectivity

Hints:
    - Use @app.on_event("startup") for table creation
    - Use yield dependencies for automatic cleanup
    - Connection.cursor() returns a cursor from the connection
    - cursor.execute("SELECT 1") can verify connectivity

Expected behavior:
    GET /health -> {"status": "ok", "database": "connected"}
    GET /health (DB down) -> 500 Internal Server Error
"""

# TODO: Write your code below


# ============================================================
# Exercise 18.2: CRUD Operations for Tasks
# ============================================================
"""
Problem:
    Implement full CRUD (Create, Read, Update, Delete) for tasks.

Endpoints to implement:
    POST   /tasks          - Create a new task
    GET    /tasks          - List all tasks (with optional filter)
    GET    /tasks/{id}     - Get a single task by ID
    PUT    /tasks/{id}     - Update a task
    DELETE /tasks/{id}     - Delete a task

Request/Response Models:
    TaskCreate:  title (required), description (optional)
    TaskUpdate:  title (optional), description (optional), completed (optional)
    TaskResponse: id, title, description, completed, created_at

Hints:
    - Use cursor.execute("INSERT INTO tasks ...") for creation
    - cursor.lastrowid gives you the auto-incremented ID
    - Use cursor.fetchall() for list operations
    - Convert sqlite3.Row objects to dicts with dict(row)

Test cases:
    # Create a task
    POST /tasks {"title": "Learn FastAPI"}
    -> 201 {"id": 1, "title": "Learn FastAPI", "completed": false}

    # List tasks
    GET /tasks
    -> 200 [{"id": 1, "title": "Learn FastAPI", ...}]

    # Get single task
    GET /tasks/1
    -> 200 {"id": 1, "title": "Learn FastAPI", ...}

    # Get non-existent task
    GET /tasks/999
    -> 404 {"detail": "Task not found"}

    # Delete task
    DELETE /tasks/1
    -> 200 {"message": "Task deleted"}
"""

# TODO: Write your code below


# ============================================================
# Exercise 18.3: Pagination and Filtering
# ============================================================
"""
Problem:
    Add pagination and filtering to the tasks list endpoint.

New GET /tasks parameters:
    - skip: int = 0 (offset for pagination)
    - limit: int = 10 (max items per page)
    - completed: Optional[bool] = None (filter by status)
    - search: Optional[str] = None (search in title)

Response format:
    {
        "tasks": [...],
        "total": 15,
        "skip": 0,
        "limit": 10,
        "has_more": true
    }

Hints:
    - Use SQL WHERE clauses for filtering
    - Use LIMIT and OFFSET for pagination
    - Use COUNT(*) for total count
    - Use LIKE '%search%' for text search
    - has_more = (skip + limit) < total

Test cases:
    # Paginate
    GET /tasks?skip=0&limit=2
    -> {"tasks": [...2 items...], "total": 15, "has_more": true}

    # Filter by completed
    GET /tasks?completed=true
    -> {"tasks": [only completed tasks], ...}

    # Search
    GET /tasks?search=FastAPI
    -> {"tasks": [tasks with "FastAPI" in title], ...}

    # Combined
    GET /tasks?completed=false&search=learn&limit=5
"""

# TODO: Write your code below


# ============================================================
# Exercise 18.4: Transactions and Bulk Operations
# ============================================================
"""
Problem:
    Implement endpoints that use database transactions.

Endpoints:
    POST /tasks/bulk          - Create multiple tasks in one transaction
    POST /tasks/{id}/complete - Mark task and all its subtasks as complete

Requirements:
    1. /tasks/bulk accepts a list of tasks, inserts all atomically
    2. If any insert fails, roll back the entire batch
    3. /tasks/{id}/complete marks the task completed atomically
    4. Return proper status codes for partial failures

Request models:
    BulkTaskCreate: tasks: list[TaskCreate]
    BulkTaskResponse: created: list[TaskResponse], count: int

Hints:
    - connection.commit() finalizes a transaction
    - connection.rollback() undoes all changes in current transaction
    - Use try/except around database operations
    - cursor.executemany() inserts multiple rows at once

Test cases:
    # Bulk create
    POST /tasks/bulk {"tasks": [{"title": "Task 1"}, {"title": "Task 2"}]}
    -> 201 {"created": [...], "count": 2}

    # Bulk create with failure (empty title)
    POST /tasks/bulk {"tasks": [{"title": "OK"}, {"title": ""}]}
    -> 400 {"detail": "Bulk insert failed, no tasks were created"}

    # Complete task (should also complete subtasks if any)
    POST /tasks/1/complete
    -> 200 {"id": 1, "completed": true}
"""

# TODO: Write your code below


# ============================================================
# Exercise 18.5: Raw Query Endpoint (Advanced)
# ============================================================
"""
Problem:
    Build a safe, limited SQL query endpoint for admin use.

Endpoint:
    POST /admin/query

Request:
    {
        "query": "SELECT * FROM tasks WHERE completed = 1",
        "params": []
    }

Requirements:
    1. Only allow SELECT queries (block INSERT, UPDATE, DELETE, DROP, etc.)
    2. Limit query execution time to 5 seconds
    3. Limit result set to 1000 rows
    4. Log all queries for audit
    5. Return results as list of dicts

Security considerations:
    - Parse SQL to check it starts with SELECT
    - Block dangerous keywords: DROP, DELETE, UPDATE, INSERT, ALTER, CREATE
    - Never return connection or table schema info

Hints:
    - Use sqlparse library to properly parse SQL (pip install sqlparse)
    - Or use simple string checking: query.strip().upper().startswith("SELECT")
    - Check for dangerous keywords with regex or string matching
    - Use cursor.fetchmany(1000) to limit results
    - Use time.time() for timeout enforcement

Test cases:
    # Valid query
    POST /admin/query {"query": "SELECT COUNT(*) as total FROM tasks"}
    -> 200 [{"total": 15}]

    # Dangerous query
    POST /admin/query {"query": "DROP TABLE tasks"}
    -> 400 {"detail": "Only SELECT queries are allowed"}

    # SELECT with params
    POST /admin/query {
        "query": "SELECT * FROM tasks WHERE title LIKE ?",
        "params": ["%FastAPI%"]
    }
    -> 200 [matching tasks]

    # Invalid SQL
    POST /admin/query {"query": "SELCT * FORM tasks"}
    -> 400 {"detail": "Invalid SQL query"}
"""
