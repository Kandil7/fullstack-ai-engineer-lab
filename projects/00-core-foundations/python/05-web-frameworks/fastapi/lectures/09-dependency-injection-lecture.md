# Lecture 09: Dependency Injection

## Topic Overview

Dependency Injection (DI) is a design pattern where FastAPI "injects" dependencies into your path operation functions. Instead of creating resources (database sessions, auth checks, configuration) inside each function, you define them as dependencies and FastAPI calls them automatically. This enables code reuse, cleaner separation of concerns, and easy testing through dependency overrides.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the Dependency Injection pattern and its benefits
2. Use `Depends()` to declare dependencies
3. Create function-based dependencies with parameters
4. Implement yield-based dependencies with cleanup (lifecycle management)
5. Chain dependencies (dependencies that depend on other dependencies)
6. Create class-based dependencies
7. Use dependency overrides for testing
8. Combine multiple dependencies on a single endpoint
9. Extract common patterns (auth, pagination, DB sessions) as dependencies

---

## Key Concepts

### 1. What is Dependency Injection?

Dependency Injection is a pattern where:
1. You define a function that produces a resource
2. You declare that your endpoint needs that resource
3. FastAPI calls the dependency function and passes the result to your endpoint

```python
from fastapi import Depends

def get_db():
    """This is a dependency — it produces a database session."""
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def list_users(db: DatabaseSession = Depends(get_db)):
    """FastAPI calls get_db() and passes the result to 'db'."""
    return db.query(User).all()
```

**Benefits:**
- **Code reuse**: One dependency used by many endpoints
- **Separation of concerns**: Business logic separated from infrastructure
- **Testability**: Override dependencies with fakes for testing
- **Documentation**: Dependencies appear in Swagger UI
- **Automatic cleanup**: Yield dependencies handle resource lifecycle

### 2. Basic Dependency with Depends()

The `Depends()` function declares that a parameter should be populated by calling a dependency function:

```python
from fastapi import Depends

def get_common_query():
    return {"skip": 0, "limit": 10, "sort": "name"}

@app.get("/items/")
def list_items(common: dict = Depends(get_common_query)):
    return {"filters": common, "items": ["item1", "item2"]}
```

**How it works:**
1. FastAPI sees `Depends(get_common_query)`
2. It calls `get_common_query()`
3. It passes the return value to `common`
4. Your function receives the result

### 3. Dependencies with Parameters

Dependencies can accept the same parameters as path operations:

```python
def get_pagination(skip: int = 0, limit: int = 10):
    """Reusable pagination dependency."""
    return {"skip": skip, "limit": limit}

@app.get("/products/")
def list_products(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination, "products": []}

@app.get("/categories/")
def list_categories(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination, "categories": []}

# GET /products/?skip=5&limit=5
# pagination = {"skip": 5, "limit": 5}
```

### 4. Yield Dependencies (Lifecycle Management)

Use `yield` in dependencies to set up and tear down resources:

```python
def get_db_session():
    """Database session with automatic cleanup."""
    session = create_session()
    try:
        yield session  # Session is available during request
    finally:
        session.close()  # Cleanup after request

@app.get("/users/")
def list_users(db = Depends(get_db_session)):
    return db.query(User).all()
    # After response, session.close() is called automatically
```

**Execution flow:**
1. Code before `yield` runs (setup)
2. `yield` value is passed to the endpoint
3. Endpoint executes
4. Code after `yield` runs (cleanup) — even if endpoint raises exception

### 5. Chained Dependencies

Dependencies can depend on other dependencies:

```python
def get_db_session():
    session = create_session()
    try:
        yield session
    finally:
        session.close()

def get_current_user(db = Depends(get_db_session)):
    """Depends on get_db_session — chained dependency."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@app.get("/my-profile/")
def get_profile(user = Depends(get_current_user)):
    # Chained: get_db_session → get_current_user → get_profile
    return {"username": user.username}
```

### 6. Authentication Dependency

A common pattern for protecting endpoints:

```python
def verify_token(authorization: str = Header(...)):
    """Check for valid Authorization header."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid header")
    token = authorization.replace("Bearer ", "")
    if token != "valid-token-123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/protected/")
def protected_endpoint(token: str = Depends(verify_token)):
    return {"message": "Access granted", "token": token[:10] + "..."}
```

### 7. Class-Based Dependencies

Classes can also be dependencies. FastAPI instantiates them once per request:

```python
class QueryParams:
    def __init__(self, q: str = "", page: int = 1, per_page: int = 20):
        self.q = q
        self.page = max(1, page)
        self.per_page = min(max(1, per_page), 100)
        self.offset = (self.page - 1) * self.per_page

@app.get("/search/")
def search(params: QueryParams = Depends()):
    return {
        "query": params.q,
        "page": params.page,
        "offset": params.offset,
    }
```

### 8. Dependency Overrides for Testing

Override dependencies with fake implementations for testing:

```python
def get_db():
    session = create_session()
    try:
        yield session
    finally:
        session.close()

def fake_get_db():
    """Fake DB for testing — no real database needed."""
    return {"connected": True, "test": True}

# In tests:
# app.dependency_overrides[get_db] = fake_get_db
```

### 9. Multiple Dependencies

An endpoint can have multiple dependencies:

```python
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.get("/admin/stats/")
def admin_stats(
    token: str = Depends(verify_token),
    api_key: str = Depends(verify_api_key),
    db: dict = Depends(get_db_session),
):
    return {
        "authorized": True,
        "api_key_valid": True,
        "db_connected": db["connected"],
    }
```

---

## Code Examples

### Example 1: Simple Dependency

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_common_query():
    return {"skip": 0, "limit": 10, "sort": "name"}

@app.get("/items/")
def list_items(common: dict = Depends(get_common_query)):
    return {"filters": common, "items": ["item1", "item2"]}
```

### Example 2: Reusable Pagination

```python
def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/products/")
def list_products(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination, "products": []}

@app.get("/categories/")
def list_categories(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination, "categories": []}
```

### Example 3: Database Session with Cleanup

```python
from datetime import datetime

def get_db_session():
    """Simulated database session with lifecycle."""
    session = {"connected": True, "created_at": datetime.now().isoformat()}
    try:
        yield session  # Available during request
    finally:
        session["connected"] = False  # Cleanup

@app.get("/my-profile/")
def get_profile(db: dict = Depends(get_db_session)):
    return {"db_connected": db["connected"], "since": db["created_at"]}
```

### Example 4: Authentication Dependency

```python
from fastapi import Header

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid header")
    token = authorization.replace("Bearer ", "")
    if token != "valid-token-123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/protected/")
def protected(token: str = Depends(verify_token)):
    return {"message": "Access granted", "token": token[:10] + "..."}

# Test:
# curl -H "Authorization: Bearer valid-token-123" http://localhost:8000/protected/
```

### Example 5: Class-Based Dependency

```python
class QueryParams:
    def __init__(self, q: str = "", page: int = 1, per_page: int = 20):
        self.q = q
        self.page = max(1, page)
        self.per_page = min(max(1, per_page), 100)
        self.offset = (self.page - 1) * self.per_page

@app.get("/search/")
def search(params: QueryParams = Depends()):
    return {"query": params.q, "page": params.page, "offset": params.offset}
```

### Example 6: Multiple Dependencies

```python
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.get("/admin/stats/")
def admin_stats(
    token: str = Depends(verify_token),
    api_key: str = Depends(verify_api_key),
    db: dict = Depends(get_db_session),
):
    return {"authorized": True, "db_connected": db["connected"]}

# Test:
# curl -H "Authorization: Bearer valid-token-123" \
#      -H "X-Api-Key: my-secret-key" \
#      http://localhost:8000/admin/stats/
```

---

## Common Mistakes to Avoid

### Mistake 1: Not using `yield` for cleanup
```python
# Wrong: No cleanup for database session
def get_db():
    session = create_session()
    return session  # Never closed!

# Fix: Use yield for automatic cleanup
def get_db():
    session = create_session()
    try:
        yield session
    finally:
        session.close()
```

### Mistake 2: Forgetting the Depends() wrapper
```python
# Wrong: This is just a regular parameter, not a dependency
@app.get("/items/")
def list_items(db: dict = get_db()):
    ...

# Fix: Wrap in Depends()
@app.get("/items/")
def list_items(db: dict = Depends(get_db)):
    ...
```

### Mistake 3: Doing too much in a dependency
```python
# Wrong: Business logic in dependency
def get_user_data():
    user = get_current_user()
    orders = get_orders(user.id)
    return {"user": user, "orders": orders}

# Fix: Keep dependencies focused
def get_current_user():
    return authenticate_user()

@app.get("/profile/")
def get_profile(user = Depends(get_current_user)):
    # Business logic in the endpoint
    orders = get_orders(user.id)
    return {"user": user, "orders": orders}
```

### Mistake 4: Not testing with dependency overrides
```python
# Wrong: Tests hit real database
def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200

# Fix: Override dependencies in tests
def test_get_users():
    app.dependency_overrides[get_db] = fake_get_db
    response = client.get("/users/")
    assert response.status_code == 200
    app.dependency_overrides.clear()
```

---

## Best Practices

1. **Use yield dependencies** for resources that need cleanup (DB sessions, connections)
2. **Keep dependencies focused** — one responsibility per dependency
3. **Chain dependencies** when you need layered abstractions (DB → Auth → Endpoint)
4. **Use class-based dependencies** for complex parameter handling
5. **Always override dependencies** in tests with fakes
6. **Add `Header()` dependencies** for authentication and API key validation
7. **Document dependencies** — they appear in Swagger UI automatically
8. **Use `app.dependency_overrides`** for test configuration

---

## Practice Exercises

### Exercise 1: Pagination Dependency
Create a `get_pagination` dependency that accepts `skip` and `limit` query parameters. Use it on two endpoints.

### Exercise 2: Database Session
Create a `get_db` yield dependency that simulates a database session with setup and cleanup.

### Exercise 3: Authentication
Create a `verify_token` dependency that checks for a Bearer token in the Authorization header.

### Exercise 4: Chained Dependencies
Create: `get_db` → `get_current_user` → `get_profile` dependency chain.

### Exercise 5: Dependency Override
Write a test that overrides the database dependency with a fake.

---

## Summary

| Concept | Description |
|---------|-------------|
| `Depends()` | Declares a dependency |
| `yield` | Lifecycle management (setup/cleanup) |
| Chained deps | Dependencies that depend on other dependencies |
| Class-based deps | Complex parameter handling |
| `Header()` | Extract header values as dependencies |
| Override | Replace dependencies for testing |
| Multiple deps | Combine multiple dependencies on one endpoint |
| DRY | Don't Repeat Yourself — reuse common logic |

Dependencies are FastAPI's most powerful feature for building maintainable, testable applications. They let you extract common patterns into reusable, composable units.

---

## Quick Reference

```python
from fastapi import FastAPI, Depends, Header

app = FastAPI()

# Simple dependency
def get_settings():
    return {"debug": True}

@app.get("/settings/")
def read_settings(settings: dict = Depends(get_settings)):
    return settings

# Yield dependency (lifecycle)
def get_db():
    db = create_session()
    try:
        yield db
    finally:
        db.close()

# Auth dependency
def verify_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if token != "valid":
        raise HTTPException(401, "Invalid token")
    return token

@app.get("/protected/")
def protected(token: str = Depends(verify_token)):
    return {"message": "OK"}

# Multiple dependencies
@app.get("/admin/")
def admin(
    token: str = Depends(verify_token),
    db = Depends(get_db),
):
    return {"admin": True}
```
