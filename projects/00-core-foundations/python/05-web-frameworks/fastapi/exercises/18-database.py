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
from typing import Optional, List
import sqlite3
import os
import time
import re

app = FastAPI(title="Database Integration Exercises")

DATABASE_URL = "exercises_18.db"


# ============================================================
# Exercise 18.1: Basic Database Connection & Setup
# ============================================================

def get_db():
    """Dependency that yields a database connection, auto-closing after request."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_db_cursor(db: sqlite3.Connection = Depends(get_db)):
    """Dependency that yields a database cursor."""
    return db.cursor()


# Note: get_db_cursor is available but not used in these exercises.
# To use it: cursor = Depends(get_db_cursor)


@app.on_event("startup")
async def startup():
    """Create tasks table on application startup."""
    conn = sqlite3.connect(DATABASE_URL)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


@app.get("/health")
async def health_check(db: sqlite3.Connection = Depends(get_db)):
    """Verify database connectivity."""
    try:
        cursor = db.execute("SELECT 1")
        cursor.fetchone()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


# ============================================================
# Exercise 18.2: CRUD Operations for Tasks
# ============================================================

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: str


@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (task.title, task.description)
    )
    db.commit()
    task_id = cursor.lastrowid
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return TaskResponse(**dict(row))


@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    completed: Optional[bool] = None,
    search: Optional[str] = None,
    db: sqlite3.Connection = Depends(get_db)
):
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if completed is not None:
        query += " AND completed = ?"
        params.append(1 if completed else 0)

    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    # Get total count
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    total = db.execute(count_query, params).fetchone()[0]

    # Get paginated results
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, skip])

    rows = db.execute(query, params).fetchall()
    return [TaskResponse(**dict(r)) for r in rows]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**dict(row))


@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskUpdate, db: sqlite3.Connection = Depends(get_db)):
    existing = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Build dynamic UPDATE statement
    updates = {}
    if task.title is not None:
        updates["title"] = task.title
    if task.description is not None:
        updates["description"] = task.description
    if task.completed is not None:
        updates["completed"] = 1 if task.completed else 0

    if not updates:
        return TaskResponse(**dict(existing))

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [task_id]
    db.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
    db.commit()

    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return TaskResponse(**dict(row))


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    existing = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return {"message": "Task deleted"}


# ============================================================
# Exercise 18.3: Pagination and Filtering
# ============================================================
# (Already integrated into list_tasks endpoint above)


# ============================================================
# Exercise 18.4: Transactions and Bulk Operations
# ============================================================

class BulkTaskCreate(BaseModel):
    tasks: List[TaskCreate]


class BulkTaskResponse(BaseModel):
    created: List[TaskResponse]
    count: int


@app.post("/tasks/bulk", response_model=BulkTaskResponse, status_code=201)
async def bulk_create_tasks(bulk: BulkTaskCreate, db: sqlite3.Connection = Depends(get_db)):
    created = []
    try:
        for task in bulk.tasks:
            if not task.title.strip():
                raise ValueError("Task title cannot be empty")
            cursor = db.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (task.title, task.description)
            )
            task_id = cursor.lastrowid
            row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            created.append(TaskResponse(**dict(row)))
        db.commit()
        return BulkTaskResponse(created=created, count=len(created))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Bulk insert failed, no tasks were created: {str(e)}")


@app.post("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    existing = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return TaskResponse(**dict(row))


# ============================================================
# Exercise 18.5: Raw Query Endpoint (Advanced)
# ============================================================

class QueryRequest(BaseModel):
    query: str
    params: List = []


class QueryResponse(BaseModel):
    results: List[dict]
    row_count: int


@app.post("/admin/query", response_model=QueryResponse)
async def admin_query(
    query_req: QueryRequest,
    db: sqlite3.Connection = Depends(get_db)
):
    sql = query_req.query.strip().upper()

    # Only allow SELECT queries
    if not sql.startswith("SELECT"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")

    # Block dangerous keywords
    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", "TRUNCATE", "EXEC"]
    for keyword in dangerous:
        if re.search(rf"\b{keyword}\b", sql):
            raise HTTPException(status_code=400, detail=f"Dangerous keyword '{keyword}' not allowed")

    try:
        start = time.time()
        cursor = db.execute(query_req.query, query_req.params)

        # Limit results to 1000 rows
        rows = cursor.fetchmany(1000)
        duration = time.time() - start

        if duration > 5:
            raise HTTPException(status_code=408, detail="Query timeout")

        results = [dict(row) for row in rows]
        return QueryResponse(results=results, row_count=len(results))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid SQL query: {str(e)}")
