# Glossary: API Router Concepts in FastAPI

## Quick Reference Table

| Term | Definition | Related Terms |
|------|------------|---------------|
| APIRouter | Class for grouping related endpoints | Router, Endpoints |
| Prefix | URL path prepended to all routes | Route, Path |
| Tags | Labels for grouping endpoints in docs | Documentation, Swagger |
| Include | Method to add a router to app | Router, App |
| Dependencies | Shared dependencies for router routes | Dependency Injection |
| Nested Router | Router included within another router | Sub-router, Hierarchy |
| Versioning | API version management | v1, v2, Backwards Compatible |
| Route | Individual API endpoint | Endpoint, Path |
| Middleware | Processing layer for requests | Router Middleware |
| Response Model | Pydantic model for response validation | Schema, Documentation |
| Status Code | HTTP response code | 200, 404, 500 |
| Summary | Brief endpoint description | Documentation |
| Description | Detailed endpoint explanation | Documentation |
| Operation ID | Unique identifier for endpoint | Swagger, OpenAPI |
| Exception Handler | Error handling for router routes | Error, Handler |

---

## Detailed Definitions

### APIRouter

**Definition**: FastAPI class that groups related endpoints together for modular organization.

**Code Example**:
```python
from fastapi import APIRouter

# Create router
router = APIRouter()

# Add endpoints
@router.get("/")
async def root():
    return {"message": "Hello"}

@router.post("/items/")
async def create_item(item: dict):
    return item

# Router with configuration
router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
    responses={404: {"description": "Not found"}}
)

# Include in app
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)
```

**Related Terms**: FastAPI, Endpoints, Prefix

---

### Prefix

**Definition**: A URL path that is automatically prepended to all routes in a router.

**Code Example**:
```python
from fastapi import APIRouter

# Router with prefix
users_router = APIRouter(prefix="/users")

@router.get("/")  # Becomes /users/
async def list_users():
    return []

@router.get("/{user_id}")  # Becomes /users/{user_id}
async def get_user(user_id: int):
    return {"id": user_id}

# Nested prefixes
api_router = APIRouter(prefix="/api")
api_router.include_router(users_router, prefix="/v1")
# Result: /api/v1/users/

# Multiple levels
app.include_router(api_router, prefix="/v2")
# Result: /v2/api/v1/users/
```

**Related Terms**: Route, Path, URL

---

### Tags

**Definition**: Labels that group related endpoints in API documentation (Swagger/ReDoc).

**Code Example**:
```python
from fastapi import APIRouter

# Router with tags
router = APIRouter(
    tags=["users"]  # Groups all endpoints under "users" tag
)

@router.get("/", summary="List users")
async def list_users():
    """List all users"""
    return []

@router.post("/", summary="Create user")
async def create_user(user: dict):
    """Create a new user"""
    return user

# Multiple tags
router = APIRouter(tags=["users", "admin"])

# Per-endpoint tags
@router.get("/", tags=["list", "read"])
async def list_users():
    return []

# In Swagger UI:
# - Users section contains all /users/ endpoints
# - Admin section contains admin-only endpoints
```

**Related Terms**: Documentation, Swagger, Group

---

### Include

**Definition**: Method to add a router's endpoints to the main application or another router.

**Code Example**:
```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# Create routers
users_router = APIRouter(prefix="/users")
items_router = APIRouter(prefix="/items")
admin_router = APIRouter(prefix="/admin")

# Add endpoints to routers
@users_router.get("/")
async def list_users():
    return []

@items_router.get("/")
async def list_items():
    return []

@admin_router.get("/")
async def admin_dashboard():
    return {}

# Include routers in app
app.include_router(users_router)
app.include_router(items_router)
app.include_router(admin_router)

# Include with additional prefix
app.include_router(users_router, prefix="/api/v1")

# Include with tags override
app.include_router(items_router, tags=["catalog"])

# Include multiple routers
api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(items_router)
app.include_router(api_router, prefix="/api")
```

**Related Terms**: Router, App, Mount

---

### Dependencies

**Definition**: Shared dependencies that apply to all routes in a router.

**Code Example**:
```python
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

# Define dependency
async def verify_token(token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    return token

async def verify_admin(user = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not admin")
    return user

# Router-level dependencies
router = APIRouter(dependencies=[Depends(verify_token)])

@router.get("/users/")
async def list_users():
    return []  # Requires valid token

# Multiple dependencies
router = APIRouter(dependencies=[
    Depends(verify_token),
    Depends(rate_limit)
])

# Per-route overrides
@router.get("/admin/", dependencies=[Depends(verify_admin)])
async def admin_route():
    return {}  # Requires admin

# Override router dependency
@router.get("/public/", dependencies=[])  # No dependencies
async def public_route():
    return {}  # No auth required
```

**Related Terms**: Dependency Injection, Authentication

---

### Nested Router

**Definition**: A router that is included within another router, creating hierarchical URL structures.

**Code Example**:
```python
from fastapi import APIRouter

# Parent router
products_router = APIRouter(prefix="/products")

# Child routers
reviews_router = APIRouter()
variants_router = APIRouter()

# Add endpoints to children
@reviews_router.get("/")
async def list_reviews(product_id: int):
    return []

@reviews_router.post("/")
async def create_review(product_id: int, review: dict):
    return review

@variants_router.get("/")
async def list_variants(product_id: int):
    return []

# Nest children under parent
products_router.include_router(reviews_router, prefix="/{product_id}/reviews")
products_router.include_router(variants_router, prefix="/{product_id}/variants")

# Add parent endpoints
@products_router.get("/")
async def list_products():
    return []

@products_router.get("/{product_id}")
async def get_product(product_id: int):
    return {"id": product_id}

# Resulting endpoints:
# GET /products/
# GET /products/{product_id}
# GET /products/{product_id}/reviews/
# POST /products/{product_id}/reviews/
# GET /products/{product_id}/variants/
```

**Related Terms**: Hierarchy, Parent, Child

---

### Versioning

**Definition**: Managing multiple API versions to maintain backwards compatibility.

**Code Example**:
```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# V1 router
v1_router = APIRouter()

@v1_router.get("/users/")
async def list_users_v1():
    """V1: Basic user list"""
    return [{"id": 1, "name": "John"}]

# V2 router
v2_router = APIRouter()

@v2_router.get("/users/")
async def list_users_v2():
    """V2: Paginated user list"""
    return {
        "data": [{"id": 1, "name": "John"}],
        "total": 100,
        "page": 1
    }

# Include versioned routers
app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")

# Version-specific dependencies
async def v1_auth():
    return {"version": "1"}

async def v2_auth():
    return {"version": "2"}

v1_router = APIRouter(dependencies=[Depends(v1_auth)])
v2_router = APIRouter(dependencies=[Depends(v2_auth)])
```

**Related Terms**: Backwards Compatible, Migration

---

### Response Model

**Definition**: Pydantic model that defines and validates the response structure.

**Code Example**:
```python
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

# Response model
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    data: List[UserResponse]
    total: int
    page: int

router = APIRouter()

# Single response
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    return {"id": user_id, "name": "John", "email": "john@example.com"}

# List response
@router.get("/users/", response_model=UserListResponse)
async def list_users():
    return {
        "data": [{"id": 1, "name": "John"}],
        "total": 1,
        "page": 1
    }

# Multiple response models
@router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found"}
    }
)
async def get_item(item_id: int):
    return {"id": item_id, "name": "Item"}
```

**Related Terms**: Schema, Validation, Documentation

---

### Status Code

**Definition**: HTTP response code indicating the result of a request.

**Code Example**:
```python
from fastapi import APIRouter, status

router = APIRouter()

# Default 200
@router.get("/items/")
async def list_items():
    return []

# Explicit status code
@router.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: dict):
    return item

# No content (204)
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None

# Custom status codes
from fastapi.responses import JSONResponse

@router.post("/items/")
async def create_item(item: dict):
    if item_exists(item["name"]):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Item already exists"}
        )
    return item

# Common status codes
"""
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
429 Too Many Requests
500 Internal Server Error
"""
```

**Related Terms**: HTTP, Response, Code

---

### Summary

**Definition**: A brief description of an endpoint shown in API documentation.

**Code Example**:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/users/",
    summary="List all users",
    description="Retrieve a paginated list of all users in the system"
)
async def list_users():
    """
    List all users.
    
    This endpoint returns a paginated list of users.
    Only authenticated users can access this endpoint.
    """
    return []

# Summary in Swagger UI:
# GET /users/ - List all users

# Without summary:
# GET /users/ - list_users
```

**Related Terms**: Documentation, Description

---

### Exception Handler

**Definition**: A function that catches and handles exceptions for a router.

**Code Example**:
```python
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter()

# Router-level exception handler
@router.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@router.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@router.get("/items/")
async def list_items():
    # These exceptions will be handled by router handlers
    raise ValueError("Invalid data")
    return []
```

**Related Terms**: Error, Handler, Exception

---

## Router Configuration Options

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",           # URL prefix
    tags=["api"],               # Documentation tags
    responses={404: {"description": "Not found"}},  # Default responses
    dependencies=[Depends(verify_token)],  # Shared dependencies
    default_response_class=JSONResponse,   # Response class
    responses={500: {"description": "Server error"}},  # Error responses
    include_in_schema=True,     # Show in docs
    deprecated=False,           # Mark as deprecated
)
```

---

## Common Patterns

### Pattern: Router Factory
```python
def create_router(prefix: str, tags: list) -> APIRouter:
    return APIRouter(prefix=prefix, tags=tags)

users_router = create_router("/users", ["users"])
items_router = create_router("/items", ["items"])
```

### Pattern: Conditional Routes
```python
router = APIRouter()

if settings.DEBUG:
    @router.get("/debug/")
    async def debug():
        return {"debug": True}

@router.get("/health/")
async def health():
    return {"status": "ok"}
```

### Pattern: Router Composition
```python
api_router = APIRouter()

# Group related routers
auth_router = APIRouter()
auth_router.include_router(login_router)
auth_router.include_router(register_router)

api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(users_router, prefix="/users")
api_router.include_router(items_router, prefix="/items")

app.include_router(api_router, prefix="/api/v1")
```

---

## Summary

Understanding API routers is essential for organizing FastAPI applications. Key takeaways:

1. **APIRouter**: Group related endpoints
2. **Prefix**: Organize URL structure
3. **Tags**: Group endpoints in docs
4. **Dependencies**: Share logic across routes
5. **Nested Routers**: Create hierarchical APIs
6. **Versioning**: Maintain backwards compatibility
7. **Response Models**: Document and validate responses

**Next**: Move to the events lecture for lifecycle management.
