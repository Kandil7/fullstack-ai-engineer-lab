# Lecture 01: Introduction to FastAPI

## Topic Overview

FastAPI is a modern, high-performance Python web framework for building APIs. Created by Sebastián Ramírez (tiangolo), it leverages Python type hints to provide automatic validation, serialization, and API documentation. FastAPI is built on top of Starlette (for the web parts) and Pydantic (for the data parts), and it uses uvicorn as its ASGI server.

This lecture introduces the foundational concepts of FastAPI: what it is, why it exists, how it compares to alternatives, and how to create your very first API endpoint.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what FastAPI is and its core advantages
2. Install FastAPI and its dependencies
3. Create a basic FastAPI application with an `app` instance
4. Define path operations using HTTP method decorators (`@app.get`, `@app.post`, etc.)
5. Return JSON responses from endpoints
6. Use path parameters for dynamic URLs
7. Run the application with uvicorn
8. Access the auto-generated API documentation (Swagger UI and ReDoc)

---

## Key Concepts

### 1. What is FastAPI?

FastAPI is a Python web framework designed specifically for building APIs. It stands out from other frameworks like Flask and Django because of:

- **Performance**: On par with Node.js and Go, thanks to Starlette's async capabilities
- **Type Safety**: Uses Python type hints for validation, serialization, and documentation
- **Auto-Documentation**: Generates interactive API docs (Swagger UI and ReDoc) automatically
- **Developer Experience**: Excellent IDE support with autocompletion and inline error detection
- **Standards-Based**: Built on OpenAPI and JSON Schema standards

### 2. The FastAPI Application Object

The `FastAPI()` constructor creates the main application instance. This object is the entry point for defining routes, middleware, and other configuration.

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="A description of my API",
    version="1.0.0",
)
```

**Key parameters for `FastAPI()`:**
- `title` — The title of the API (appears in docs)
- `description` — A longer description of the API
- `version` — The version string
- `docs_url` — Path for Swagger UI (default: `/docs`)
- `redoc_url` — Path for ReDoc (default: `/redoc`)
- `openapi_url` — Path for the OpenAPI JSON schema (default: `/openapi.json`)

### 3. Path Operations and Decorators

A "path operation" is an HTTP request handler defined by a decorator and a function. The decorator specifies the HTTP method and URL path.

```python
@app.get("/")          # Handles GET requests to /
@app.post("/items")    # Handles POST requests to /items
@app.put("/items/{id}")# Handles PUT requests to /items/{id}
@app.delete("/items/{id}") # Handles DELETE requests to /items/{id}
@app.patch("/items/{id}")  # Handles PATCH requests to /items/{id}
```

**How FastAPI processes a request:**
1. Receives the HTTP request
2. Matches the URL path to a registered path operation
3. Extracts parameters from the path, query, headers, or body
4. Validates data using type hints and Pydantic
5. Calls your function with validated data
6. Converts the return value to JSON
7. Sends the HTTP response

### 4. Path Parameters

Path parameters are variables embedded in the URL path. They are defined using curly braces `{}` in the route and as function parameters with type hints.

```python
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}
```

FastAPI automatically:
- Extracts the value from the URL
- Converts it to the declared type (`str`, `int`, `float`, `UUID`, etc.)
- Validates the type
- Returns a 422 error if the type is wrong

### 5. Returning JSON Responses

FastAPI automatically converts Python dicts and lists to JSON. You can also use `Response` objects for more control.

```python
@app.get("/server-info")
def server_info():
    return {
        "framework": "FastAPI",
        "features": ["Type hints", "Auto docs"],
        "is_awesome": True,
    }
```

**Rules for return values:**
- `dict` → Automatically serialized to JSON
- `list` → Automatically serialized to JSON array
- Pydantic model → Serialized to JSON with field filtering
- `str`, `int`, `float` → Wrapped in a JSON response
- `Response` object → Used as-is

### 6. Multiple HTTP Methods

You can define multiple HTTP methods on the same path by stacking decorators or using `app.api_route()`:

```python
@app.get("/submit")
def submit_get():
    return {"method": "GET"}

@app.post("/submit")
def submit_post():
    return {"method": "POST"}
```

### 7. Uvicorn ASGI Server

Uvicorn is a lightning-fast ASGI server used to run FastAPI applications. It supports:
- Hot reloading with `--reload`
- Multi-worker deployment
- TLS/SSL
- Unix sockets

```bash
# Development
uvicorn module_name:app --reload

# Production
uvicorn module_name:app --host 0.0.0.0 --port 8000 --workers 4
```

### 8. Auto-Generated Documentation

FastAPI generates three documentation endpoints automatically:

| Endpoint | Description |
|----------|-------------|
| `/docs` | Swagger UI — Interactive API explorer |
| `/redoc` | ReDoc — Alternative documentation format |
| `/openapi.json` | Raw OpenAPI 3.1 JSON schema |

You can disable docs in production:
```python
app = FastAPI(docs_url=None, redoc_url=None)
```

---

## Code Examples

### Example 1: Minimal FastAPI App

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}
```

**Run:**
```bash
uvicorn main:app --reload
```

**Test:**
```bash
curl http://127.0.0.1:8000/
# Output: {"message":"Hello, World!"}
```

### Example 2: Multiple Endpoints

```python
from fastapi import FastAPI

app = FastAPI(title="My First API")

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/users/{name}")
def greet_user(name: str):
    return {"greeting": f"Hello, {name}!"}

@app.post("/data")
def receive_data():
    return {"status": "received"}
```

### Example 3: Returning Complex Data

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/server-info")
def server_info():
    return {
        "framework": "FastAPI",
        "language": "Python",
        "version": "0.100+",
        "features": [
            "Type hints",
            "Auto documentation",
            "Async support",
            "Data validation",
        ],
        "is_awesome": True,
    }
```

### Example 4: Using `if __name__ == "__main__"`

```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

This allows you to run the file directly: `python main.py`

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting the `uvicorn` dependency
```bash
# Wrong: ModuleNotFoundError
uvicorn main:app --reload

# Fix: Install both packages
pip install fastapi uvicorn
```

### Mistake 2: Wrong module path in uvicorn
```bash
# If your file is main.py at the root:
uvicorn main:app --reload

# If your file is at src/main.py:
uvicorn src.main:app --reload
```

### Mistake 3: Not using `--reload` in development
```bash
# Without --reload, changes require manual restart
uvicorn main:app --reload  # Always use this in dev
```

### Mistake 4: Confusing path parameters with query parameters
```python
# Path parameter (in the URL):
@app.get("/users/{user_id}")
def get_user(user_id: int): ...

# Query parameter (after ?):
@app.get("/users/")
def list_users(limit: int = 10): ...
```

### Mistake 5: Returning non-serializable objects
```python
# Wrong: datetime is not JSON-serializable
@app.get("/time")
def get_time():
    return {"time": datetime.now()}  # Error!

# Fix: Convert to string
from datetime import datetime
@app.get("/time")
def get_time():
    return {"time": datetime.now().isoformat()}
```

---

## Best Practices

1. **Always install both `fastapi` and `uvicorn`**
   ```bash
   pip install fastapi uvicorn
   ```

2. **Use descriptive API metadata** in the `FastAPI()` constructor for better documentation

3. **Use `--reload` in development** for hot reloading

4. **Name your path operation functions descriptively** — they appear in the OpenAPI docs

5. **Always include type hints** on path operation parameters for automatic validation

6. **Disable docs in production**:
   ```python
   app = FastAPI(docs_url=None, redoc_url=None)
   ```

7. **Use proper HTTP methods**: GET for reading, POST for creating, PUT for full updates, PATCH for partial updates, DELETE for removal

8. **Structure your project** — don't put everything in one file for production apps

---

## Practice Exercises

### Exercise 1: Hello World
Create a FastAPI app with a single endpoint `GET /` that returns `{"message": "Hello, World!"}`.

### Exercise 2: Multiple Endpoints
Create endpoints for:
- `GET /` — Welcome message
- `GET /about` — Returns `{"name": "My API", "version": "1.0.0"}`
- `POST /echo` — Returns `{"status": "received"}`

### Exercise 3: Path Parameter
Create a `GET /greet/{name}` endpoint that returns `{"greeting": "Hello, <name>!"}`.

### Exercise 4: Complex Response
Create a `GET /status` endpoint that returns a dictionary with at least 5 fields including a list and a boolean.

### Exercise 5: Run and Test
Run your app, open `/docs` in the browser, and test each endpoint using the interactive Swagger UI.

---

## Summary

| Concept | Description |
|---------|-------------|
| `FastAPI()` | Creates the application instance |
| `@app.get()` | Decorator for GET path operations |
| `@app.post()` | Decorator for POST path operations |
| Path parameters | Variables in the URL: `{name}` |
| Type hints | Provide automatic validation |
| `uvicorn` | ASGI server to run the app |
| `/docs` | Swagger UI interactive docs |
| `/redoc` | Alternative documentation format |
| `return dict` | Automatically serialized to JSON |

FastAPI's design philosophy is "the less you have to think about, the better." By leveraging Python type hints, it eliminates boilerplate for validation, serialization, and documentation — letting you focus on your business logic.

---

## Quick Reference

```bash
# Install
pip install fastapi uvicorn

# Run development server
uvicorn main:app --reload

# Test endpoints
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/docs

# Key imports
from fastapi import FastAPI
```
