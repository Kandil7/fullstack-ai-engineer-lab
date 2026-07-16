# FastAPI Exercises

Hands-on practice problems for mastering FastAPI. Each exercise file contains 3-5 problems with descriptions, starter code, hints, expected behavior, and test cases.

**No solutions provided** - work through the problems yourself to build deep understanding.

---

## Directory Structure

```
exercises/
├── 01-routing.py          # Basic routing and path parameters
├── 02-methods.py          # HTTP methods (GET, POST, PUT, DELETE)
├── 03-pydantic.py         # Pydantic models and validation
├── 04-query-params.py     # Query parameters and string validation
├── 05-body.py             # Request body and nested models
├── 06-response.py         # Response models and status codes
├── 07-forms.py            # Form data and file uploads
├── 08-dependency.py       # Dependency injection basics
├── 09-security.py         # OAuth2, JWT tokens, API keys
├── 10-middleware.py        # Custom middleware and decorators
├── 11-error-handling.py   # HTTPException and error responses
├── 12-templates.py        # Jinja2 templates and HTML responses
├── 13-websockets.py       # WebSocket connections and real-time
├── 14-background.py       # Background tasks and async jobs
├── 15-advanced-di.py      # Advanced dependency injection patterns
├── 16-file-handling.py    # File upload/download and streaming
├── 17-openapi.py          # Custom OpenAPI docs and schema
├── 18-database.py         # SQLite database integration
├── 19-orm.py              # SQLAlchemy ORM with FastAPI
├── 20-testing.py          # Unit and integration testing
├── 21-async.py            # Async programming patterns
├── 22-cors.py             # CORS configuration and security
├── 23-exception-handling.py # Custom exceptions and error handling
├── 24-api-router.py       # Modular routing with APIRouter
├── 25-events.py           # App lifecycle and background events
└── README.md              # This file
```

---

## Topics by Category

### Core (Exercises 01-07)
| # | Topic | Key Concepts | Time |
|---|-------|-------------|------|
| 01 | Routing | Path params, static paths, URL design | 30 min |
| 02 | HTTP Methods | GET, POST, PUT, DELETE, PATCH | 30 min |
| 03 | Pydantic | Models, validation, serialization | 45 min |
| 04 | Query Params | QueryString, defaults, validation | 30 min |
| 05 | Request Body | JSON body, nested models, lists | 40 min |
| 06 | Responses | Response models, status codes, headers | 35 min |
| 07 | Forms & Files | Form data, file uploads, streaming | 40 min |

### Architecture (Exercises 08-17)
| # | Topic | Key Concepts | Time |
|---|-------|-------------|------|
| 08 | Dependency Injection | Basic DI, class dependencies | 45 min |
| 09 | Security | OAuth2, JWT, API key auth | 60 min |
| 10 | Middleware | Custom middleware, CORS, logging | 45 min |
| 11 | Error Handling | HTTPException, custom errors | 35 min |
| 12 | Templates | Jinja2, HTML responses, forms | 40 min |
| 13 | WebSockets | WebSocket connections, chat | 50 min |
| 14 | Background Tasks | BackgroundTasks, async jobs | 40 min |
| 15 | Advanced DI | Overrides, generators, context | 50 min |
| 16 | File Handling | Upload, download, streaming | 45 min |
| 17 | OpenAPI | Custom docs, schema, tags | 40 min |

### Production (Exercises 18-25)
| # | Topic | Key Concepts | Time |
|---|-------|-------------|------|
| 18 | Database | SQLite, CRUD, pagination | 60-90 min |
| 19 | ORM | SQLAlchemy, relationships, async | 75-100 min |
| 20 | Testing | pytest, fixtures, mocking | 60-80 min |
| 21 | Async | async/await, concurrency, rate limiting | 60-80 min |
| 22 | CORS | CORS middleware, origins, security | 30-45 min |
| 23 | Exceptions | Custom exceptions, handlers, logging | 45-60 min |
| 24 | APIRouter | Modular routing, versioning | 45-60 min |
| 25 | Events | Lifecycle, background tasks, health | 45-60 min |

---

## Getting Started

### Prerequisites
- Python 3.9+
- FastAPI installed: `pip install fastapi uvicorn`
- pytest installed: `pip install pytest`
- Basic Python knowledge (functions, classes, type hints)

### Installation
```bash
cd projects/00-core-foundations/python/fastapi
pip install fastapi uvicorn[standard] pytest httpx
```

### Running Exercises
```bash
# Navigate to exercises directory
cd projects/00-core-foundations/python/fastapi/exercises

# Run a specific exercise file
uvicorn 01-routing:app --reload --port 8000

# Open API docs
# http://localhost:8000/docs

# Run tests (for exercise 20)
pytest 20-testing.py -v
```

### Running in VS Code
1. Open the exercises folder in VS Code
2. Use the Python extension
3. Select "FastAPI" launch configuration
4. Press F5 to run with auto-reload

---

## Recommended Order

**Beginners** (start here):
1. Exercises 01-05 (Core routing and models)
2. Exercise 06 (Response models)
3. Exercise 08 (Basic dependency injection)

**Intermediate**:
4. Exercises 09-11 (Security, middleware, errors)
5. Exercises 12-14 (Templates, WebSockets, background)
6. Exercise 07 (Forms and files)

**Advanced**:
7. Exercises 15-17 (Advanced DI, files, OpenAPI)
8. Exercises 18-19 (Database and ORM)
9. Exercises 20-21 (Testing and async)

**Production**:
10. Exercises 22-25 (CORS, exceptions, routers, events)

---

## Exercise Format

Each exercise follows this structure:

```python
# ============================================================
# Exercise X.Y: Title
# ============================================================
"""
Problem:
    Clear description of what to build.

Requirements:
    1. Specific requirement
    2. Another requirement
    3. ...

Hints:
    - Helpful hint 1
    - Helpful hint 2

Test cases:
    # Description of test case
    GET /endpoint
    -> 200 expected_response

    # Another test case
    POST /endpoint {"data": "value"}
    -> 201 created_response
"""

# TODO: Write your code below
```

---

## Tips for Success

1. **Read the problem carefully** - Understand what's being asked before coding
2. **Start simple** - Get the basic case working first, then add complexity
3. **Use the hints** - They point you in the right direction without giving away the answer
4. **Test as you go** - Use curl, httpie, or the /docs page to test endpoints
5. **Check the test cases** - They show expected inputs and outputs
6. **Read the error messages** - FastAPI gives detailed validation errors
7. **Don't copy-paste** - Type the code yourself to build muscle memory

---

## Common Patterns

### Endpoint Pattern
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Request model
class ItemCreate(BaseModel):
    name: str
    price: float

# Response model
class ItemResponse(ItemCreate):
    id: int

# Endpoint
@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    # Your logic here
    return {"id": 1, **item.dict()}
```

### Dependency Pattern
```python
from fastapi import Depends

async def get_db():
    db = DatabaseConnection()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
async def list_items(db = Depends(get_db)):
    return db.query("SELECT * FROM items")
```

### Error Pattern
```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    return items[item_id]
```

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2 Docs](https://docs.pydantic.dev/)
- [Starlette Documentation](https://www.starlette.io/)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/)
- [pytest Documentation](https://docs.pytest.org/)

---

## Getting Help

If you're stuck:
1. Re-read the problem description and hints
2. Check the FastAPI docs link above
3. Look at the test cases for expected behavior
4. Search for similar patterns in other exercises
5. Ask in the project's GitHub Discussions

Remember: struggling is part of learning. Push through the frustration - the breakthrough will come!
