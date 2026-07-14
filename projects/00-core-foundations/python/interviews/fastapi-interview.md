# FastAPI Interview Guide

> Comprehensive interview preparation for FastAPI and async Python web development.  
> Covers fundamentals, advanced patterns, and production best practices.

---

## Table of Contents

1. [Topic Overview](#topic-overview)
2. [Interview Questions](#interview-questions)
3. [Coding Challenges](#coding-challenges)
4. [Follow-Up Questions](#follow-up-questions)
5. [Tips for Answering](#tips-for-answering)

---

## Topic Overview

FastAPI is a modern, high-performance Python web framework for building APIs. It leverages Python 3.6+ type hints, async/await syntax, and automatic API documentation generation.

### Core Concepts

| Concept | Description | Importance |
|---------|-------------|------------|
| Path Parameters | URL segments that become function arguments | 🔴 Critical |
| Query Parameters | URL query string parameters | 🔴 Critical |
| Request Body | JSON payload sent by clients | 🔴 Critical |
| Response Model | Pydantic models for response validation | 🟡 Important |
| Dependency Injection | Reusable components injected into endpoints | 🔴 Critical |
| Async/Await | Non-blocking concurrent request handling | 🔴 Critical |
| Middleware | Request/response processing layers | 🟡 Important |
| Exception Handling | Custom error responses | 🟡 Important |
| Background Tasks | Deferred execution after response | 🟢 Nice to Know |
| WebSocket | Real-time bidirectional communication | 🟢 Nice to Know |

---

## Interview Questions

### FastAPI Fundamentals

**Q1: What makes FastAPI different from Flask or Django?** 🟢

**Answer:**
FastAPI offers several advantages:
1. **Automatic API documentation** — Swagger UI and ReDoc generated automatically
2. **Type hint validation** — Uses Pydantic for automatic request/response validation
3. **Native async support** — Built on Starlette with full async/await support
4. **High performance** — Comparable to Node.js and Go for raw throughput
5. **Type safety** — Catches errors at development time, not runtime

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Flask equivalent requires manual validation
# FastAPI does it automatically with type hints
class User(BaseModel):
    name: str
    email: str
    age: int  # Will reject strings automatically

@app.post("/users/")
async def create_user(user: User):
    return {"user": user, "status": "created"}
```

**Follow-up:** "When would you choose Flask over FastAPI?"
- Simple, synchronous APIs with minimal dependencies
- Projects requiring mature ecosystem (Flask has been around longer)
- Teams more familiar with Flask patterns

---

**Q2: Explain the difference between `@app.get()` and `@app.post()`. When would you use each?** 🟢

**Answer:**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """GET: Retrieve data, idempotent, no side effects"""
    return {"user_id": user_id}

@app.post("/users/")
async def create_user(user: User):
    """POST: Create new resource, not idempotent"""
    return {"user": user, "status": "created"}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    """PUT: Replace entire resource, idempotent"""
    return {"user_id": user_id, "user": user}

@app.patch("/users/{user_id}")
async def partial_update(user_id: int, user: User):
    """PATCH: Partial update"""
    return {"user_id": user_id, "user": user}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """DELETE: Remove resource, idempotent"""
    return {"status": "deleted"}
```

**Follow-up:** "What does idempotent mean?"
An operation is idempotent if performing it multiple times produces the same result as doing it once.

---

**Q3: How does FastAPI handle automatic API documentation?** 🟡

**Answer:**
FastAPI uses the OpenAPI standard to generate documentation:
1. Analyzes all route decorators and type hints
2. Generates OpenAPI schema automatically
3. Serves Swagger UI at `/docs`
4. Serves ReDoc at `/redoc`
5. Provides raw OpenAPI JSON at `/openapi.json`

```python
app = FastAPI(
    title="My API",
    description="A sample FastAPI application",
    version="1.0.0"
)

@app.get("/items/", tags=["items"], summary="Get all items")
async def get_items(
    skip: int = 0,
    limit: int = 10,
    description: Number of items to return
):
    """
    Retrieve a list of items.

    - **skip**: Number of items to skip
    - **limit**: Maximum items to return
    """
    return {"items": []}
```

The `tags`, `summary`, `description`, and docstrings all appear in the generated docs.

---

**Q4: What is the purpose of `response_model` in FastAPI?** 🟡

**Answer:**
`response_model` controls what data is serialized and returned to the client:

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # Client sends this

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    # password is NOT included

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Password is never exposed in response
    db_user = save_to_database(user)
    return db_user  # Only id, name, email returned
```

Benefits:
1. **Security** — Prevents leaking sensitive fields
2. **Documentation** — Shows correct response shape in docs
3. **Validation** — Ensures response matches declared schema
4. **Serialization** — Converts ORM models to JSON properly

---

### Path and Query Parameters

**Q5: How do you validate path parameters with constraints?** 🟡

**Answer:**
Use `Path` function with validation parameters:

```python
from fastapi import Path, Query

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., gt=0, description="Item ID must be positive")
):
    return {"item_id": item_id}

@app.get("/items/")
async def list_items(
    skip: int = Query(0, ge=0, description="Items to skip"),
    limit: int = Query(10, gt=0, le=100, description="Max items")
):
    return {"items": [], "skip": skip, "limit": limit}
```

Validation constraints:
- `gt`: greater than
- `ge`: greater than or equal
- `lt`: less than
- `le`: less than or equal
- `min_length`, `max_length`: for strings
- `regex`: pattern matching

---

**Q6: How do you handle optional query parameters?** 🟢

**Answer:**
```python
from typing import Optional
from fastapi import Query

@app.get("/search/")
async def search(
    q: str,
    category: Optional[str] = None,  # Optional parameter
    sort_by: str = Query(default="created_at", description="Sort field"),
    order: str = Query(default="desc", regex="^(asc|desc)$")
):
    filters = {"q": q}
    if category:
        filters["category"] = category
    return {"filters": filters, "sort": sort_by, "order": order}
```

---

**Q7: How do you handle multiple HTTP methods on the same path?** 🟡

**Answer:**
```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"status": "deleted"}
```

Each method is a separate function with its own route decorator.

---

### Request and Response Models

**Q8: Explain Pydantic model inheritance and field customization.** 🟡

**Answer:**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class BaseUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserCreate(BaseUser):
    password: str = Field(..., min_length=8)
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(BaseUser):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Allow ORM model conversion

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v and len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return v.strip() if v else v
```

---

**Q9: How do you handle file uploads in FastAPI?** 🟡

**Answer:**
```python
from fastapi import File, UploadFile
from typing import List

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type
    }

@app.post("/upload-multiple/")
async def upload_files(files: List[UploadFile] = File(...)):
    return [{"filename": f.filename} for f in files]
```

---

**Q10: How do you return different response types from a single endpoint?** 🔴

**Answer:**
```python
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse

@app.get("/item/{item_id}")
async def get_item(item_id: int, format: str = "json"):
    if format == "file":
        return FileResponse(f"items/{item_id}.json")
    elif format == "html":
        html_content = f"<h1>Item {item_id}</h1>"
        return HTMLResponse(content=html_content)
    else:
        return {"item_id": item_id}
```

---

### Dependency Injection

**Q11: What is dependency injection and why is it important in FastAPI?** 🔴

**Answer:**
Dependency injection (DI) allows you to:
1. **Share logic** across multiple endpoints
2. **Test easily** by replacing dependencies with mocks
3. **Manage resources** like database connections
4. **Enforce authentication** consistently

```python
from fastapi import Depends, HTTPException, status
from typing import Optional

# Simple dependency
async def get_db():
    db = DatabaseSession()
    try:
        yield db
    finally:
        await db.close()

# Authentication dependency
async def get_current_user(
    token: str = Header(...),
    db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user

# Use in endpoints
@app.get("/profile/")
async def get_profile(user: User = Depends(get_current_user)):
    return {"user": user}

@app.get("/orders/")
async def get_orders(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {"orders": db.query(Order).filter(Order.user_id == user.id).all()}
```

---

**Q12: How do you create dependencies with parameters?** 🟡

**Answer:**
```python
from typing import List

def require_role(allowed_roles: List[str]):
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker

@app.get("/admin/dashboard/")
async def admin_dashboard(user: User = Depends(require_role(["admin"]))):
    return {"message": "Welcome, admin"}

@app.get("/moderator/tools/")
async def moderator_tools(user: User = Depends(require_role(["admin", "moderator"]))):
    return {"message": "Moderator tools"}
```

---

**Q13: What is the difference between `yield` dependencies and regular dependencies?** 🔴

**Answer:**
```python
# Regular dependency (runs completely before endpoint)
async def get_user(user_id: int):
    return fetch_user_from_db(user_id)

# Yield dependency (has setup and teardown)
async def get_db_connection():
    # Setup: runs before endpoint
    conn = await create_connection()
    try:
        yield conn  # This value is injected
    finally:
        # Teardown: runs after endpoint (even if endpoint fails)
        await conn.close()

@app.get("/data/")
async def get_data(db = Depends(get_db_connection)):
    return await db.fetch("SELECT * FROM items")
```

Yield dependencies are essential for:
- Database connections
- File handles
- External service clients
- Any resource needing cleanup

---

### Authentication and Authorization

**Q14: How do you implement JWT authentication in FastAPI?** 🔴

**Answer:**
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

---

### Async/Await

**Q15: When should you use `async def` vs regular `def` in FastAPI?** 🟡

**Answer:**
```python
# Use async def for:
# - Database queries (with async driver)
# - HTTP requests to external services
# - File I/O operations
# - Any I/O-bound operation

@app.get("/users/")
async def get_users():
    # Async database query
    users = await db.execute(select(User))
    return users.all()

@app.get("/external/")
async def call_external_api():
    # Async HTTP request
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
    return response.json()

# Use regular def for:
# - CPU-bound operations
# - Synchronous libraries that don't support async
# - Simple data transformation

@app.get("/compute/")
def heavy_computation():
    # CPU-bound work (blocks the event loop)
    result = sum(i**2 for i in range(10_000_000))
    return {"result": result}
```

**Key rule:** If you're doing I/O, use `async def`. If you're doing CPU work, use `def` (or run in a thread pool).

---

### Testing FastAPI

**Q16: How do you write unit tests for FastAPI endpoints?** 🟡

**Answer:**
```python
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "name": "John",
        "email": "john@example.com",
        "age": 30
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John"
    assert "id" in data

def test_create_user_invalid_email():
    response = client.post("/users/", json={
        "name": "John",
        "email": "not-an-email",
        "age": 30
    })
    assert response.status_code == 422  # Validation error

def test_get_user_not_found():
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
```

For async testing:
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users/", json={
            "name": "John",
            "email": "john@example.com"
        })
    assert response.status_code == 200
```

---

### Database Integration

**Q17: How do you integrate SQLAlchemy with FastAPI?** 🔴

**Answer:**
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
```

---

## Coding Challenges

### Challenge 1: Build a URL Shortener API 🟡

**Problem:** Create a URL shortener with create and redirect endpoints.

```python
"""
Build a URL shortener API with:
1. POST /shorten - Accepts a URL, returns a short code
2. GET /{code} - Redirects to original URL
3. GET /stats/{code} - Returns click count and creation date
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
import hashlib
import string

app = FastAPI(title="URL Shortener")

# In-memory storage
url_db = {}

class URLCreate(BaseModel):
    url: HttpUrl
    custom_code: Optional[str] = None

class URLResponse(BaseModel):
    short_url: str
    original_url: str
    created_at: datetime

# Solution
@app.post("/shorten", response_model=URLResponse)
async def shorten_url(url_data: URLCreate):
    if url_data.custom_code:
        code = url_data.custom_code
        if code in url_db:
            raise HTTPException(400, "Custom code already taken")
    else:
        code = hashlib.md5(str(url_data.url).encode()).hexdigest()[:6]

    url_db[code] = {
        "url": str(url_data.url),
        "clicks": 0,
        "created_at": datetime.now()
    }
    return URLResponse(
        short_url=f"http://localhost:8000/{code}",
        original_url=str(url_data.url),
        created_at=datetime.now()
    )

@app.get("/{code}")
async def redirect_url(code: str):
    if code not in url_db:
        raise HTTPException(404, "URL not found")
    url_db[code]["clicks"] += 1
    return RedirectResponse(url=url_db[code]["url"])

@app.get("/stats/{code}")
async def get_stats(code: str):
    if code not in url_db:
        raise HTTPException(404, "URL not found")
    data = url_db[code]
    return {"code": code, "clicks": data["clicks"], "created_at": data["created_at"]}
```

**Test cases:**
```python
def test_shorten_url():
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data

def test_redirect():
    # First create
    create_resp = client.post("/shorten", json={"url": "https://example.com"})
    code = create_resp.json()["short_url"].split("/")[-1]

    # Then redirect (follow_redirects=False to check status)
    redirect_resp = client.get(f"/{code}", follow_redirects=False)
    assert redirect_resp.status_code == 307
```

---

### Challenge 2: Authentication Middleware 🟡

**Problem:** Create JWT authentication middleware that protects certain routes.

```python
"""
Build authentication system with:
1. POST /register - Create new user
2. POST /login - Get JWT token
3. GET /protected - Requires valid JWT token
4. GET /admin - Requires admin role
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        return TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

def require_role(role: str):
    async def role_checker(user: TokenData = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker

@app.post("/login")
async def login(username: str, password: str):
    # Verify credentials (simplified)
    user = verify_user(username, password)
    if not user:
        raise HTTPException(status_code=401)

    access_token = jwt.encode(
        {"sub": username, "role": user.role, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token}

@app.get("/protected")
async def protected_route(user: TokenData = Depends(get_current_user)):
    return {"message": f"Hello {user.username}"}

@app.get("/admin")
async def admin_route(user: TokenData = Depends(require_role("admin"))):
    return {"message": "Welcome, admin"}
```

---

### Challenge 3: Real-time Chat WebSocket 🟡

**Problem:** Build a WebSocket chat room.

```python
"""
Build a chat application with:
1. WebSocket connection at /ws/{room}
2. Broadcast messages to all connected clients
3. Handle user join/leave notifications
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        self.active_connections[room].remove(websocket)
        if not self.active_connections[room]:
            del self.active_connections[room]

    async def broadcast(self, message: str, room: str):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        # Notify others
        await manager.broadcast(f"User joined room {room}", room)

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await manager.broadcast(
                json.dumps({"user": message["user"], "text": message["text"]}),
                room
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.broadcast(f"User left room {room}", room)
```

---

### Challenge 4: Rate Limiting Middleware 🟡

**Problem:** Implement rate limiting to prevent abuse.

```python
"""
Build a rate limiter that:
1. Limits requests per IP address
2. Returns 429 Too Many Requests when exceeded
3. Includes rate limit headers in responses
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> tuple[bool, dict]:
        now = time.time()
        window_start = now - self.window_seconds

        # Remove old requests
        self.requests[key] = [
            t for t in self.requests[key] if t > window_start
        ]

        remaining = self.max_requests - len(self.requests[key])
        allowed = remaining > 0

        if allowed:
            self.requests[key].append(now)
            remaining -= 1

        headers = {
            "X-RateLimit-Limit": str(self.max_requests),
            "X-RateLimit-Remaining": str(max(0, remaining)),
            "X-RateLimit-Reset": str(int(window_start + self.window_seconds))
        }
        return allowed, headers

limiter = RateLimiter(max_requests=100, window_seconds=60)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    allowed, headers = limiter.is_allowed(client_ip)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"},
            headers=headers
        )

    response = await call_next(request)
    for key, value in headers.items():
        response.headers[key] = value
    return response
```

---

### Challenge 5: File Upload with Processing 🟡

**Problem:** Build an endpoint that accepts CSV files and returns analysis.

```python
"""
Build an endpoint that:
1. Accepts CSV file upload
2. Validates the file
3. Returns basic statistics
"""
from fastapi import File, UploadFile, HTTPException
import io
import csv

@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "File must be CSV")

    contents = await file.read()
    text = contents.decode('utf-8')

    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)

    if not rows:
        raise HTTPException(400, "CSV is empty")

    # Analyze numeric columns
    numeric_stats = {}
    for column in rows[0].keys():
        try:
            values = [float(row[column]) for row in rows if row[column]]
            numeric_stats[column] = {
                "count": len(values),
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "sum": sum(values)
            }
        except (ValueError, KeyError):
            continue

    return {
        "filename": file.filename,
        "total_rows": len(rows),
        "columns": list(rows[0].keys()),
        "numeric_stats": numeric_stats,
        "sample_rows": rows[:5]
    }
```

---

### Challenge 6: Database CRUD with Pagination 🟡

**Problem:** Build a complete CRUD API with pagination support.

```python
"""
Build a Todo API with:
1. Create, Read, Update, Delete operations
2. Pagination (skip/limit)
3. Filtering by status
4. Sorting by created_at
"""
from fastapi import Query
from typing import Optional, List
from datetime import datetime

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoResponse(TodoCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@app.post("/todos/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict(), created_at=datetime.now(), updated_at=datetime.now())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[TodoResponse])
async def list_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    completed: Optional[bool] = None,
    sort_by: str = Query("created_at", regex="^(created_at|title)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    # Sorting
    sort_column = getattr(Todo, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    todos = query.offset(skip).limit(limit).all()
    return todos

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoCreate,
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")

    for key, value in todo_update.dict().items():
        setattr(todo, key, value)
    todo.updated_at = datetime.now()

    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    db.delete(todo)
    db.commit()
    return {"status": "deleted"}
```

---

### Challenge 7: Background Tasks 🔴

**Problem:** Implement background task processing for long-running operations.

```python
"""
Build an endpoint that:
1. Accepts a task request
2. Processes it in the background
3. Provides a status endpoint to check progress
"""
from fastapi import BackgroundTasks
import uuid
import time

task_store = {}

def process_task(task_id: str, data: dict):
    """Simulate long-running task"""
    task_store[task_id]["status"] = "processing"
    time.sleep(5)  # Simulate work
    task_store[task_id]["status"] = "completed"
    task_store[task_id]["result"] = {"processed": True}

@app.post("/tasks/")
async def create_task(data: dict, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task_store[task_id] = {"status": "pending", "data": data}
    background_tasks.add_task(process_task, task_id, data)
    return {"task_id": task_id, "status": "pending"}

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in task_store:
        raise HTTPException(404, "Task not found")
    return task_store[task_id]
```

---

### Challenge 8: API Versioning 🟡

**Problem:** Implement API versioning strategy.

```python
"""
Build versioned API with:
1. /api/v1/items/ - Original version
2. /api/v2/items/ - New version with additional fields
3. Backward compatibility
"""
from fastapi import APIRouter

# Version 1
v1_router = APIRouter(prefix="/api/v1")

class ItemV1(BaseModel):
    name: str
    price: float

@v1_router.get("/items/{item_id}")
async def get_item_v1(item_id: int):
    return {"id": item_id, "name": "Item", "price": 9.99}

# Version 2
v2_router = APIRouter(prefix="/api/v2")

class ItemV2(BaseModel):
    name: str
    price: float
    category: str
    tags: List[str]

@v2_router.get("/items/{item_id}")
async def get_item_v2(item_id: int):
    return {
        "id": item_id,
        "name": "Item",
        "price": 9.99,
        "category": "electronics",
        "tags": ["sale", "new"]
    }

# Register routers
app.include_router(v1_router)
app.include_router(v2_router)
```

---

## Follow-Up Questions

### Authentication Follow-ups
1. "How do you handle token refresh?"
2. "What's the difference between JWT and session-based auth?"
3. "How do you implement role-based access control (RBAC)?"

### Performance Follow-ups
1. "How would you optimize database queries in FastAPI?"
2. "When would you use Redis caching?"
3. "How do you handle 10,000 concurrent WebSocket connections?"

### Architecture Follow-ups
1. "How do you structure a large FastAPI application?"
2. "When would you choose FastAPI over Django REST Framework?"
3. "How do you implement microservices with FastAPI?"

### Testing Follow-ups
1. "How do you test database-dependent endpoints?"
2. "What's the difference between `TestClient` and `AsyncClient`?"
3. "How do you mock external services in tests?"

---

## Tips for Answering

### Before the Interview

1. **Know the Basics**
   - HTTP methods and their semantics
   - RESTful API design principles
   - Python async/await fundamentals
   - Pydantic model validation

2. **Practice Building**
   - Create a simple CRUD API
   - Implement authentication
   - Write tests with pytest
   - Deploy to production (Docker, cloud)

3. **Review Common Patterns**
   - Dependency injection
   - Middleware implementation
   - Error handling
   - Background tasks

### During the Interview

1. **Clarify Requirements**
   - "Should I handle error cases?"
   - "What's the expected request volume?"
   - "Do I need authentication for this endpoint?"

2. **Explain Your Approach**
   - Mention Pydantic for validation
   - Discuss async vs sync tradeoffs
   - Talk about dependency injection benefits

3. **Write Clean Code**
   - Use type hints consistently
   - Add docstrings to endpoints
   - Handle errors gracefully
   - Follow RESTful conventions

4. **Discuss Tradeoffs**
   - In-memory storage vs database
   - Sync vs async operations
   - Validation strictness

### Common Mistakes to Avoid

1. **Not using async properly**
   ```python
   # Wrong: blocking in async function
   @app.get("/data/")
   async def get_data():
       result = requests.get("https://api.example.com")  # Blocks!
       return result.json()

   # Correct: use async client
   @app.get("/data/")
   async def get_data():
       async with httpx.AsyncClient() as client:
           result = await client.get("https://api.example.com")
       return result.json()
   ```

2. **Forgetting error handling**
   ```python
   # Wrong: no error handling
   @app.get("/users/{user_id}")
   async def get_user(user_id: int):
       return db.query(User).filter(User.id == user_id).first()

   # Correct: handle not found
   @app.get("/users/{user_id}")
   async def get_user(user_id: int):
       user = db.query(User).filter(User.id == user_id).first()
       if not user:
           raise HTTPException(status_code=404, detail="User not found")
       return user
   ```

3. **Leaking sensitive data in responses**
   ```python
   # Wrong: returning password
   @app.post("/users/")
   async def create_user(user: UserCreate):
       return user  # Includes password!

   # Correct: use response model
   @app.post("/users/", response_model=UserResponse)
   async def create_user(user: UserCreate):
       return user  # Excludes password
   ```

---

## Quick Reference Card

### Essential Imports

```python
from fastapi import (
    FastAPI, Depends, HTTPException, status,
    Path, Query, Header, File, UploadFile,
    BackgroundTasks, WebSocket, WebSocketDisconnect,
    APIRouter, Request, Response
)
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime
```

### Common Patterns

```python
# Dependency injection
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Error handling
raise HTTPException(status_code=404, detail="Not found")

# Response model
@app.get("/items/", response_model=List[ItemResponse])

# Query parameters with validation
q: str = Query(..., min_length=1, max_length=100)

# Path parameters with constraints
item_id: int = Path(..., gt=0)
```

---

## Additional Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Starlette Documentation](https://www.starlette.io/)
- [Real Python - FastAPI Tutorial](https://realpython.com/fastapi-python-web-apis/)
