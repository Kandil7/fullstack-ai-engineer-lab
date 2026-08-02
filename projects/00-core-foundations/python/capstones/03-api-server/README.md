# 🌐 Project 03: Task Manager API

A RESTful API for task management built with FastAPI, featuring CRUD operations, filtering, and statistics.

## What This Project Practices

| Skill | Phase | Details |
|-------|-------|---------|
| FastAPI | Phase 5 | Routes, path/query params, status codes |
| Pydantic | Phase 5 | Request/response models, validation |
| HTTP Methods | Phase 1 | GET, POST, PUT, DELETE |
| Error Handling | Phase 1 | HTTPException, 404 handling |
| Type Hints | Phase 2 | Annotations on all endpoints |
| Dictionaries | Phase 1 | In-memory data store |
| Datetime | Phase 1 | ISO timestamps |
| API Design | Phase 5 | RESTful patterns |
| Auto-docs | Phase 5 | Swagger UI at /docs |

## How to Run

```bash
# Terminal 1: Start the server
uvicorn projects/03-api-server/main:app --reload

# Then open http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/tasks` | List tasks (with filtering) |
| POST | `/tasks` | Create task |
| GET | `/tasks/{id}` | Get task by ID |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/stats` | Task statistics |

## Testing with curl

```bash
# List all tasks
curl http://127.0.0.1:8000/tasks

# Create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": 4}'

# Get stats
curl http://127.0.0.1:8000/stats
```
