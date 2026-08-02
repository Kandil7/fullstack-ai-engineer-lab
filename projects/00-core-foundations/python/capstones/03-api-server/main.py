"""
API Server — Mini Project
===========================
Combines: FastAPI, Pydantic, HTTP methods, error handling, in-memory database

A simple task management API server.

Run: uvicorn projects/03-api-server/main:app --reload
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API built with FastAPI",
    version="1.0.0",
)


# ── Models ─────────────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["Buy groceries"])
    description: str = Field(default="", max_length=1000)
    priority: int = Field(default=1, ge=1, le=5, description="1=low, 5=high")
    completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    completed: Optional[bool] = None


class TaskResponse(TaskCreate):
    id: int
    created_at: str
    updated_at: str


# ── In-Memory Database ────────────────────────────────────────────────────

tasks_db: dict[int, dict] = {}
next_id = 1


@app.on_event("startup")
async def startup():
    """Seed with sample data."""
    global next_id
    samples = [
        ("Learn FastAPI", "Complete the FastAPI tutorial series", 3),
        ("Build a project", "Apply what I learned in a real project", 4),
        ("Write tests", "Add unit and integration tests", 2),
    ]
    for title, desc, priority in samples:
        tasks_db[next_id] = {
            "id": next_id,
            "title": title,
            "description": desc,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        next_id += 1


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Task Manager API",
        "docs": "/docs",
        "endpoints": {
            "GET /tasks": "List all tasks",
            "POST /tasks": "Create a task",
            "GET /tasks/{id}": "Get task by ID",
            "PUT /tasks/{id}": "Update task",
            "DELETE /tasks/{id}": "Delete task",
            "GET /stats": "Task statistics",
        },
    }


@app.get("/tasks", response_model=list[TaskResponse], tags=["Tasks"])
def list_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[int] = Query(None, ge=1, le=5, description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search in title"),
):
    """List all tasks with optional filtering."""
    results = list(tasks_db.values())

    if completed is not None:
        results = [t for t in results if t["completed"] == completed]
    if priority is not None:
        results = [t for t in results if t["priority"] == priority]
    if search:
        results = [t for t in results if search.lower() in t["title"].lower()]

    return results


@app.post("/tasks", response_model=TaskResponse, status_code=201, tags=["Tasks"])
def create_task(task: TaskCreate):
    """Create a new task."""
    global next_id
    now = datetime.now().isoformat()
    tasks_db[next_id] = {
        "id": next_id,
        **task.model_dump(),
        "created_at": now,
        "updated_at": now,
    }
    next_id += 1
    return tasks_db[next_id - 1]


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: int = Path(..., ge=1, description="Task ID")):
    """Get a task by ID."""
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task: TaskUpdate):
    """Update a task (partial update)."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    stored = tasks_db[task_id]
    update_data = task.model_dump(exclude_unset=True)
    stored.update(update_data)
    stored["updated_at"] = datetime.now().isoformat()
    tasks_db[task_id] = stored
    return stored


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int):
    """Delete a task."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    del tasks_db[task_id]


@app.get("/stats", tags=["Stats"])
def get_stats():
    """Get task statistics."""
    tasks = list(tasks_db.values())
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    priorities = {i: sum(1 for t in tasks if t["priority"] == i) for i in range(1, 6)}

    return {
        "total_tasks": total,
        "completed": completed,
        "pending": total - completed,
        "completion_rate": round(completed / total * 100, 1) if total else 0,
        "by_priority": priorities,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
