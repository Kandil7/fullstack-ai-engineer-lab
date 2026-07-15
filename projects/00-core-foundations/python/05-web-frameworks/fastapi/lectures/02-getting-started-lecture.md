# Lecture 02: Getting Started with FastAPI

## Topic Overview

Building on the introduction, this lecture dives into practical FastAPI development. You will learn how to work with Pydantic models for structured data, implement CRUD (Create, Read, Update, Delete) operations, handle different response status codes, and manage in-memory data stores. This is where FastAPI's power truly becomes apparent — automatic validation, serialization, and documentation all working together seamlessly.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define and use Pydantic `BaseModel` classes for request/response data
2. Implement full CRUD operations (GET, POST, PUT, DELETE)
3. Use query parameters with default values
4. Handle request body data with automatic validation
5. Set custom HTTP status codes for responses
6. Use `model_dump()` to convert Pydantic models to dictionaries
7. Build a simple in-memory API with realistic data structures

---

## Key Concepts

### 1. Pydantic BaseModel

Pydantic models are the backbone of FastAPI's data handling. They define the shape of your data with automatic validation.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
```

**Key features:**
- **Automatic validation**: Rejects invalid data with clear error messages
- **Type conversion**: Coerces compatible types (e.g., `"3.14"` → `3.14`)
- **Serialization**: Converts to/from JSON automatically
- **Documentation**: Generates OpenAPI schemas automatically
- **Optional fields**: Use `| None = None` for optional values
- **Default values**: `tags: list[str] = []` provides defaults

### 2. Request Body with Pydantic

When a function parameter has a Pydantic model type, FastAPI reads the request body as JSON and validates it against the model schema.

```python
@app.post("/items/")
def create_item(item: Item):
    # 'item' is automatically validated and parsed from JSON
    item_dict = item.model_dump()
    return item_dict
```

**How it works:**
1. Client sends JSON in the request body
2. FastAPI reads the body and parses it as JSON
3. Validates against the Pydantic model schema
4. If valid, creates a Python object and passes it to your function
5. If invalid, returns a 422 Unprocessable Entity error

### 3. Path Parameters vs Query Parameters

```python
# Path parameter: embedded in the URL
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Query parameter: comes after ? in the URL
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Both together
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**Rules:**
- Path parameters are **required** and part of the URL
- Query parameters are **optional** if they have default values
- Query parameters are **required** if they have no default value

### 4. CRUD Operations Pattern

A standard CRUD API follows this pattern:

| Operation | HTTP Method | Path | Purpose |
|-----------|------------|------|---------|
| Create | POST | `/items/` | Add a new item |
| Read (one) | GET | `/items/{id}` | Get a specific item |
| Read (list) | GET | `/items/` | Get all items |
| Update | PUT | `/items/{id}` | Replace an item |
| Delete | DELETE | `/items/{id}` | Remove an item |

### 5. Response Status Codes

FastAPI returns 200 by default, but you can override it:

```python
# Using the status_code parameter
@app.post("/items/", status_code=201)
def create_item(item: Item):
    return item

# Using HTTPException for error responses
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

### 6. model_dump() Method

`model_dump()` converts a Pydantic model to a Python dictionary. This is essential for manipulating data before storing or returning it.

```python
@app.post("/items/")
def create_item(item: Item):
    item_dict = item.model_dump()  # Convert to dict
    item_dict["id"] = 1  # Add extra field
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

### 7. In-Memory Data Store

For learning and prototyping, storing data in a Python list or dict is common:

```python
# In-memory "database"
fake_items_db: list[dict] = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 699.99},
]

# Reading from it
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 1 or item_id > len(fake_items_db):
        return {"error": "Item not found"}
    return fake_items_db[item_id - 1]
```

### 8. Health Check Endpoint

A health check endpoint is a standard pattern in production APIs:

```python
from datetime import datetime

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }
```

---

## Code Examples

### Example 1: Complete CRUD API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Items API")

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

# In-memory database
items_db: list[dict] = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Items API", "tips": ["Use /docs for interactive docs"]}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """Get a single item by ID."""
    if item_id < 1 or item_id > len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id - 1]

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    """Get a list of items with pagination."""
    return items_db[skip : skip + limit]

@app.post("/items/", status_code=201)
def create_item(item: Item) -> dict:
    """Create a new item."""
    item_dict = item.model_dump()
    item_dict["id"] = len(items_db) + 1
    items_db.append(item_dict)
    return item_dict

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an existing item."""
    if item_id < 1 or item_id > len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    items_db[item_id - 1] = item_dict
    return item_dict

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id < 1 or item_id > len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    deleted = items_db.pop(item_id - 1)
    return {"deleted": deleted, "remaining": len(items_db)}
```

### Example 2: Pydantic Model with Optional Fields

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
    bio: str | None = None  # Optional
    is_active: bool = True  # Has default
    tags: list[str] = []    # Has default

# Valid requests:
# {"name": "Alice", "email": "alice@test.com", "age": 30}
# {"name": "Bob", "email": "bob@test.com", "age": 25, "bio": "Hi!"}
```

### Example 3: Custom Status Codes

```python
@app.post("/items/multi-status/", status_code=201)
def create_item_status(item: Item):
    """POST returning 201 Created status code."""
    item_dict = item.model_dump()
    item_dict["id"] = len(items_db) + 1
    items_db.append(item_dict)
    return item_dict
```

### Example 4: Query Parameters with Pagination

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    """
    Pagination pattern:
    /items/?skip=0&limit=2 → first 2 items
    /items/?skip=2&limit=2 → items 3-4
    """
    return fake_items_db[skip : skip + limit]
```

---

## Common Mistakes to Avoid

### Mistake 1: Mixing path and query parameters incorrectly
```python
# Wrong: Can't have a query param before a path param
@app.get("/items/{item_id}/?q=search")

# Correct: Path params come first, query params after
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Mistake 2: Forgetting to handle missing items
```python
# Wrong: No error handling
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return fake_items_db[item_id - 1]  # IndexError if not found!

# Correct: Validate existence
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 1 or item_id > len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id - 1]
```

### Mistake 3: Not using `model_dump()`
```python
# Wrong: Can't serialize Pydantic model directly
@app.post("/items/")
def create_item(item: Item):
    items_db.append(item)  # TypeError!

# Correct: Convert to dict first
@app.post("/items/")
def create_item(item: Item):
    item_dict = item.model_dump()
    items_db.append(item_dict)
    return item_dict
```

### Mistake 4: Confusing PUT and PATCH
```python
# PUT = full replacement (all fields required)
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    # Client must send ALL fields
    ...

# PATCH = partial update (only changed fields)
@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    # Client can send only the fields to update
    ...
```

---

## Best Practices

1. **Use Pydantic models** for all request bodies — never parse JSON manually
2. **Define separate models** for request input vs response output
3. **Always validate item existence** before updating or deleting
4. **Use appropriate HTTP status codes** (201 for creation, 404 for not found)
5. **Include pagination** for list endpoints
6. **Add docstrings** to path operations — they appear in Swagger UI
7. **Use `model_dump()`** when you need to manipulate data as a dict
8. **Return consistent response shapes** across your API

---

## Practice Exercises

### Exercise 1: Users API
Create a Users API with:
- `POST /users/` — Create a user (returns 201)
- `GET /users/{user_id}` — Get a user
- `GET /users/` — List users with skip/limit
- `PUT /users/{user_id}` — Update a user
- `DELETE /users/{user_id}` — Delete a user

### Exercise 2: Advanced Model
Create a Pydantic model `Product` with:
- `name: str` (required)
- `price: float` (required, must be > 0)
- `description: str | None` (optional)
- `category: str` (required)
- `in_stock: bool` (default: True)
- `tags: list[str]` (default: [])

### Exercise 3: Search Endpoint
Create a `GET /search?q=term` endpoint that searches items by name.

### Exercise 4: Health Check
Create a `GET /health` endpoint returning status, timestamp, version, and uptime.

### Exercise 5: Error Handling
Add proper error handling to all endpoints — use HTTPException with appropriate status codes.

---

## Summary

| Concept | Description |
|---------|-------------|
| `BaseModel` | Define data shapes with validation |
| `model_dump()` | Convert Pydantic model to dict |
| `status_code=201` | Custom response status codes |
| `HTTPException` | Raise errors with specific status codes |
| Query parameters | Optional params with defaults |
| Path parameters | Required params in URL |
| CRUD pattern | Standard Create/Read/Update/Delete operations |
| In-memory store | List/dict for prototyping |

The Getting Started lecture establishes the foundation for all FastAPI development: defining data models, handling requests, and returning responses. Master these patterns and you can build any API.

---

## Quick Reference

```python
# Imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Pydantic model
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

# CRUD operations
@app.get("/items/{item_id}")      # Read one
@app.get("/items/")               # Read many
@app.post("/items/", status_code=201)  # Create
@app.put("/items/{item_id}")      # Update
@app.delete("/items/{item_id}")   # Delete

# Error handling
raise HTTPException(status_code=404, detail="Not found")

# Convert model to dict
item_dict = item.model_dump()
```
