# Glossary: Lecture 09 — Dependency Injection

Alphabetical reference of all key terms from the Dependency Injection lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| Chained dependency | A dependency that depends on another dependency |
| Class-based dependency | A class used as a dependency (instantiated per request) |
| Cleanup | Code that runs after a request to release resources |
| Depends() | FastAPI function for declaring dependencies |
| Dependency | A reusable function/class that provides resources to endpoints |
| Dependency injection | Pattern where dependencies are provided to functions automatically |
| Dependency override | Replacing a real dependency with a fake for testing |
| DRY | Don't Repeat Yourself — reuse common logic |
| Function dependency | A function used as a dependency |
| Header() | Extracts HTTP header values as parameters |
| Lifecycle | Setup → Request → Cleanup flow of yield dependencies |
| Setup | Code that runs before a request in yield dependencies |
| Yield dependency | A dependency using yield for automatic cleanup |

---

## Detailed Term Definitions

### Chained Dependency

**Definition:** A dependency that itself depends on other dependencies. FastAPI resolves the entire dependency chain automatically.

**Example:**
```python
def get_db_session():
    """Level 1: Database session."""
    session = create_session()
    try:
        yield session
    finally:
        session.close()

def get_current_user(db = Depends(get_db_session)):
    """Level 2: Depends on get_db_session."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(401, "Not authenticated")
    return user

def get_permissions(user = Depends(get_current_user)):
    """Level 3: Depends on get_current_user."""
    return get_user_permissions(user.id)

@app.get("/admin/")
def admin(perms = Depends(get_permissions)):
    """Resolution: get_db_session → get_current_user → get_permissions"""
    if "admin" not in perms:
        raise HTTPException(403, "Not admin")
    return {"admin": True}
```

**Resolution order:**
1. `get_db_session()` is called
2. Result passed to `get_current_user()`
3. Result passed to `get_permissions()`
4. Final result passed to `admin()`

**Related terms:** Depends(), Lifecycle, Dependency

---

### Class-based Dependency

**Definition:** A class that FastAPI instantiates as a dependency. The class's `__init__` receives parameters (from query, path, headers, etc.), and the instance is passed to the endpoint.

**Example:**
```python
class PaginationParams:
    """Class-based dependency for pagination."""
    def __init__(self, page: int = 1, page_size: int = 20):
        self.page = max(1, page)
        self.page_size = min(max(1, page_size), 100)
        self.offset = (self.page - 1) * self.page_size
        self.limit = self.page_size

@app.get("/items/")
def list_items(params: PaginationParams = Depends()):
    # params is a PaginationParams instance
    return {
        "page": params.page,
        "offset": params.offset,
        "limit": params.limit,
    }

# GET /items/?page=2&page_size=10
# params.page = 2, params.offset = 10, params.limit = 10
```

**Key points:**
- `__init__` parameters come from query/path/header params
- Instance is created once per request
- Can have methods for computed properties
- Useful for complex parameter groups

**Related terms:** Depends(), Function Dependency, Query Parameters

---

### Cleanup

**Definition:** Code that runs after a request completes (or fails) to release resources. In FastAPI, cleanup is handled by code after `yield` in yield-based dependencies.

**Example:**
```python
def get_db():
    session = create_session()  # Setup
    try:
        yield session  # Request processing
    finally:
        session.close()  # Cleanup — always runs

@app.get("/users/")
def list_users(db = Depends(get_db)):
    return db.query(User).all()
    # After response: session.close() is called
```

**Cleanup runs even when:**
- The endpoint raises an exception
- The client disconnects
- The server shuts down

**Related terms:** Yield Dependency, Lifecycle, Setup

---

### Depends() Function

**Definition:** A FastAPI function that declares a parameter as a dependency. When FastAPI sees `Depends()`, it calls the specified function/class and passes the result to the endpoint.

**Example:**
```python
from fastapi import Depends

# Simple dependency
def get_settings():
    return {"debug": True}

@app.get("/settings/")
def read_settings(settings: dict = Depends(get_settings)):
    return settings

# Dependency with parameters
def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
def list_items(pagination: dict = Depends(get_pagination)):
    return pagination
```

**Parameters:**
```python
Depends(dependency=None, use_cache=True)
# dependency: The function/class to call
# use_cache: Cache result per request (default True)
```

**Related terms:** Dependency, Chained Dependency, Yield Dependency

---

### Dependency

**Definition:** A reusable function or class that provides resources (database sessions, authentication, configuration) to path operation functions. Dependencies are called by FastAPI and their results are injected into endpoints.

**Example:**
```python
# Simple dependency
def get_db():
    return create_database_connection()

# Yield dependency with cleanup
def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

# Auth dependency
def verify_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if not is_valid(token):
        raise HTTPException(401, "Invalid token")
    return token

# Using dependencies
@app.get("/users/")
def list_users(
    db = Depends(get_db),
    token: str = Depends(verify_token),
):
    return db.query(User).all()
```

**Types:**
1. **Function dependency**: Simple function
2. **Class-based dependency**: Class with `__init__`
3. **Yield dependency**: Function with `yield` for cleanup

**Related terms:** Depends(), DRY, Reuse

---

### Dependency Injection

**Definition:** A design pattern where a function receives its dependencies from outside rather than creating them internally. FastAPI implements this by calling dependency functions and passing their results to path operation functions.

**Without DI (tight coupling):**
```python
@app.get("/users/")
def list_users():
    db = create_database_connection()  # Created inside function
    return db.query(User).all()
```

**With DI (loose coupling):**
```python
def get_db():
    return create_database_connection()

@app.get("/users/")
def list_users(db = Depends(get_db)):  # Injected from outside
    return db.query(User).all()
```

**Benefits:**
- **Reusability**: Same dependency used by multiple endpoints
- **Testability**: Override with fakes for testing
- **Separation of concerns**: Infrastructure code separate from business logic
- **Maintainability**: Change dependency once, affects all endpoints

**Related terms:** Depends(), Dependency, DRY

---

### Dependency Override

**Definition:** The ability to replace a real dependency with a fake or mock implementation. Used extensively in testing to avoid hitting real databases, APIs, or external services.

**Example:**
```python
# Real dependency
def get_db():
    session = create_session()
    try:
        yield session
    finally:
        session.close()

# Fake dependency for testing
def fake_get_db():
    return {"connected": True, "test": True, "users": []}

# In test
def test_get_users():
    # Override real DB with fake
    app.dependency_overrides[get_db] = fake_get_db

    response = client.get("/users/")
    assert response.status_code == 200

    # Clear overrides after test
    app.dependency_overrides.clear()
```

**Override at different levels:**
```python
# App-level override
app.dependency_overrides[get_db] = fake_get_db

# Router-level override
router.dependency_overrides[get_db] = fake_get_db

# TestClient override
client = TestClient(app, dependencies=[Depends(fake_get_db)])
```

**Related terms:** Testing, Mock, Fake

---

### DRY (Don't Repeat Yourself)

**Definition:** A software engineering principle that states you should not repeat code. Dependencies are a primary mechanism for achieving DRY in FastAPI — extracting common patterns into reusable dependencies.

**Example:**
```python
# WITHOUT DRY: Repeated pagination logic
@app.get("/products/")
def list_products(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit, "items": products[skip:skip+limit]}

@app.get("/categories/")
def list_categories(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit, "items": categories[skip:skip+limit]}

# WITH DRY: Reusable dependency
def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/products/")
def list_products(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination, "items": products[pagination["skip"]:pagination["skip"]+pagination["limit"]]}

@app.get("/categories/")
def list_categories(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination, "items": categories[pagination["skip"]:pagination["skip"]+pagination["limit"]]}
```

**Related terms:** Dependency, Reuse, Code Quality

---

### Function Dependency

**Definition:** A regular Python function used as a dependency. The most common type of dependency in FastAPI.

**Example:**
```python
def get_db():
    """Simple function dependency."""
    db = Database()
    try:
        yield db
    finally:
        db.close()

def verify_auth(authorization: str = Header(...)):
    """Function dependency with parameter extraction."""
    token = authorization.replace("Bearer ", "")
    if not is_valid(token):
        raise HTTPException(401, "Invalid token")
    return decode_token(token)

@app.get("/users/")
def list_users(
    db = Depends(get_db),
    user = Depends(verify_auth),
):
    return db.query(User).all()
```

**Characteristics:**
- Can be sync or async
- Can accept parameters (from query, path, headers)
- Can use `yield` for cleanup
- Called once per request (unless cached)

**Related terms:** Class-based Dependency, Depends(), Yield Dependency

---

### Header() Function

**Definition:** A FastAPI function that extracts HTTP header values and makes them available as function parameters. Often used in authentication dependencies.

**Example:**
```python
from fastapi import Header, HTTPException

def verify_token(authorization: str = Header(...)):
    """Extract and validate Authorization header."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid header format")
    token = authorization.replace("Bearer ", "")
    if token != "valid-token-123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

def verify_api_key(x_api_key: str = Header(...)):
    """Extract and validate X-Api-Key header."""
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.get("/protected/")
def protected(token: str = Depends(verify_token)):
    return {"message": "Access granted"}

@app.get("/admin/")
def admin(
    token: str = Depends(verify_token),
    api_key: str = Depends(verify_api_key),
):
    return {"admin": True}

# curl -H "Authorization: Bearer valid-token-123" http://localhost:8000/protected/
# curl -H "Authorization: Bearer valid-token-123" -H "X-Api-Key: my-secret-key" http://localhost:8000/admin/
```

**Related terms:** Authentication, Depends(), HTTP Headers

---

### Lifecycle

**Definition:** The complete flow of a dependency: setup → request processing → cleanup. Yield-based dependencies manage this lifecycle automatically.

**Example:**
```python
def get_db():
    # 1. SETUP: Runs before the request
    print("Opening database connection")
    session = create_session()
    try:
        # 2. YIELD: Value passed to endpoint
        yield session
    finally:
        # 3. CLEANUP: Runs after the request (even on error)
        print("Closing database connection")
        session.close()
```

**Execution flow:**
```
Request arrives
    ↓
Setup code (before yield)
    ↓
Yield value → passed to endpoint
    ↓
Endpoint executes
    ↓
Response sent
    ↓
Cleanup code (after yield)
    ↓
Request complete
```

**Related terms:** Yield Dependency, Setup, Cleanup

---

### Setup

**Definition:** Code that runs before a request is processed in a yield-based dependency. Used to initialize resources like database connections, file handles, or external API clients.

**Example:**
```python
def get_db():
    # SETUP: Initialize resource
    print("Connecting to database...")
    session = create_session()
    session.connect()
    try:
        yield session
    finally:
        # CLEANUP: Release resource
        session.disconnect()

def get_cache():
    # SETUP: Initialize cache
    cache = RedisCache()
    cache.connect()
    try:
        yield cache
    finally:
        # CLEANUP: Clear cache
        cache.flush()
        cache.disconnect()
```

**Related terms:** Cleanup, Yield Dependency, Lifecycle

---

### Yield Dependency

**Definition:** A dependency function that uses `yield` instead of `return`. The yielded value is passed to the endpoint, and code after `yield` runs as cleanup when the request completes.

**Example:**
```python
from fastapi import Depends

def get_db():
    """Database session with automatic cleanup."""
    session = create_session()
    try:
        yield session  # Value passed to endpoint
    finally:
        session.close()  # Cleanup runs automatically

def get_cache():
    """Cache with lifecycle management."""
    cache = {}
    print("Cache initialized")
    try:
        yield cache  # Cache available during request
    finally:
        cache.clear()  # Cache cleared after request
        print("Cache cleared")

@app.get("/users/")
def list_users(db = Depends(get_db), cache = Depends(get_cache)):
    if "users" not in cache:
        cache["users"] = db.query(User).all()
    return cache["users"]
```

**vs Return dependency:**
```python
# Return dependency: No cleanup
def get_config():
    return {"debug": True}

# Yield dependency: With cleanup
def get_db():
    session = create_session()
    try:
        yield session
    finally:
        session.close()
```

**When to use yield:**
- Database connections
- File handles
- Network connections
- Cache initialization
- Lock acquisition
- Temporary resources

**Related terms:** Lifecycle, Cleanup, Setup

---

## Dependency Patterns

### Pattern: Simple Dependency
```python
def get_settings():
    return {"debug": True}

@app.get("/settings/")
def read_settings(settings: dict = Depends(get_settings)):
    return settings
```

### Pattern: Database Session
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def list_users(db = Depends(get_db)):
    return db.query(User).all()
```

### Pattern: Authentication
```python
def verify_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if not is_valid(token):
        raise HTTPException(401, "Invalid token")
    return decode_token(token)

@app.get("/protected/")
def protected(user = Depends(verify_token)):
    return {"user": user}
```

### Pattern: Pagination
```python
def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
def list_items(pagination: dict = Depends(get_pagination)):
    return pagination
```

### Pattern: Chained Dependencies
```python
def get_db():
    yield create_session()

def get_user(db = Depends(get_db)):
    return db.query(User).first()

@app.get("/profile/")
def profile(user = Depends(get_user)):
    return {"username": user.username}
```

### Pattern: Multiple Dependencies
```python
@app.get("/admin/")
def admin(
    token: str = Depends(verify_token),
    api_key: str = Depends(verify_api_key),
    db = Depends(get_db),
):
    return {"admin": True}
```

### Pattern: Dependency Override (Testing)
```python
def fake_get_db():
    return {"test": True}

def test_get_users():
    app.dependency_overrides[get_db] = fake_get_db
    response = client.get("/users/")
    assert response.status_code == 200
    app.dependency_overrides.clear()
```

---

*End of Glossary — Lecture 09: Dependency Injection*
