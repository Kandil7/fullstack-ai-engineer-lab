# Lecture 24: API Routers in FastAPI

## Overview

API routers are essential for organizing large FastAPI applications into modular, maintainable components. This lecture covers how to use APIRouter to structure your endpoints, implement versioning, create nested routers, and build scalable API architectures.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create and use APIRouter for modular endpoints
2. Organize routes into separate files and directories
3. Implement API versioning
4. Use router prefixes and tags effectively
5. Create nested routers for complex APIs
6. Implement route dependencies
7. Build scalable API architectures
8. Handle router-level middleware

---

## Key Concepts

### 1. What is APIRouter?

APIRouter allows you to group related endpoints together and include them in your main application.

```python
from fastapi import APIRouter

# Create a router
router = APIRouter()

# Add endpoints to the router
@router.get("/users/")
async def get_users():
    return [{"name": "John"}, {"name": "Jane"}]

@router.post("/users/")
async def create_user(user: dict):
    return {"name": user["name"]}

# Include in main app
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)
```

### 2. Router Organization

```
app/
├── main.py
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── users.py
│   │   ├── items.py
│   │   └── auth.py
│   └── v2/
│       ├── __init__.py
│       ├── router.py
│       └── users.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── item.py
└── schemas/
    ├── __init__.py
    ├── user.py
    └── item.py
```

---

## Code Examples

### Example 1: Basic Router Setup

```python
# api/users.py
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[dict])
async def list_users():
    """List all users"""
    return [{"id": 1, "name": "John"}]

@router.get("/{user_id}")
async def get_user(user_id: int):
    """Get user by ID"""
    if user_id == 1:
        return {"id": 1, "name": "John"}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", status_code=201)
async def create_user(user: dict):
    """Create a new user"""
    return {"id": 2, **user}

@router.put("/{user_id}")
async def update_user(user_id: int, user: dict):
    """Update a user"""
    return {"id": user_id, **user}

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """Delete a user"""
    return None

# main.py
from fastapi import FastAPI
from api.users import router as users_router

app = FastAPI()
app.include_router(users_router)
```

### Example 2: Multiple Routers

```python
# api/items.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}}
)

@router.get("/")
async def list_items():
    return [{"id": 1, "name": "Laptop"}]

@router.get("/{item_id}")
async def get_item(item_id: int):
    return {"id": item_id, "name": "Laptop"}

# api/categories.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/")
async def list_categories():
    return [{"id": 1, "name": "Electronics"}]

# api/__init__.py
from fastapi import APIRouter

api_router = APIRouter()

# Include all routers
from .users import router as users_router
from .items import router as items_router
from .categories import router as categories_router

api_router.include_router(users_router)
api_router.include_router(items_router)
api_router.include_router(categories_router)

# main.py
from fastapi import FastAPI
from api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api")
```

### Example 3: API Versioning

```python
# api/v1/router.py
from fastapi import APIRouter

v1_router = APIRouter()

from .users import router as users_router
from .items import router as items_router

v1_router.include_router(users_router, prefix="/users", tags=["v1-users"])
v1_router.include_router(items_router, prefix="/items", tags=["v1-items"])

# api/v1/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_users_v1():
    """V1: List users with basic info"""
    return [{"id": 1, "name": "John"}]

@router.get("/{user_id}")
async def get_user_v1(user_id: int):
    """V1: Get user by ID"""
    return {"id": user_id, "name": "John"}

# api/v2/router.py
from fastapi import APIRouter

v2_router = APIRouter()

from .users import router as users_router

v2_router.include_router(users_router, prefix="/users", tags=["v2-users"])

# api/v2/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_users_v2():
    """V2: List users with pagination"""
    return {
        "data": [{"id": 1, "name": "John"}],
        "total": 1,
        "page": 1,
        "per_page": 10
    }

@router.get("/{user_id}")
async def get_user_v2(user_id: int):
    """V2: Get user with profile"""
    return {
        "id": user_id,
        "name": "John",
        "profile": {"bio": "Developer"}
    }

# main.py
from fastapi import FastAPI
from api.v1.router import v1_router
from api.v2.router import v2_router

app = FastAPI()

# Version 1 routes
app.include_router(v1_router, prefix="/api/v1")

# Version 2 routes
app.include_router(v2_router, prefix="/api/v2")
```

### Example 4: Router Dependencies

```python
# api/admin.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

# Dependency for admin authentication
async def verify_admin(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# All routes in this router require admin
router.dependencies.append(Depends(verify_admin))

@router.get("/users/")
async def admin_list_users():
    return [{"id": 1, "name": "John"}]

@router.delete("/users/{user_id}")
async def admin_delete_user(user_id: int):
    return {"deleted": True}

# Per-route dependency
@router.get("/stats/", dependencies=[Depends(verify_admin)])
async def get_stats():
    return {"users": 100, "items": 500}

# main.py
app.include_router(router, prefix="/api")
```

### Example 5: Nested Routers

```python
# api/products/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

from .reviews import router as reviews_router
from .variants import router as variants_router

# Include sub-routers
router.include_router(reviews_router, prefix="/{product_id}/reviews")
router.include_router(variants_router, prefix="/{product_id}/variants")

@router.get("/")
async def list_products():
    return [{"id": 1, "name": "Laptop"}]

@router.get("/{product_id}")
async def get_product(product_id: int):
    return {"id": product_id, "name": "Laptop"}

# api/products/reviews.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_reviews(product_id: int):
    return [{"id": 1, "rating": 5, "comment": "Great!"}]

@router.post("/")
async def create_review(product_id: int, review: dict):
    return {"product_id": product_id, **review}

# api/products/variants.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_variants(product_id: int):
    return [{"id": 1, "color": "Black", "price": 999}]

# Resulting endpoints:
# GET /products/
# GET /products/{product_id}
# GET /products/{product_id}/reviews/
# POST /products/{product_id}/reviews/
# GET /products/{product_id}/variants/
```

### Example 6: Router with Tags and Docs

```python
# api/users.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Forbidden"}
    }
)

@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List all users",
    description="Retrieve a list of all users with pagination",
    responses={
        200: {"description": "Successful response"},
        401: {"description": "Not authenticated"}
    }
)
async def list_users(
    skip: int = 0,
    limit: int = 100
):
    """
    List all users.
    
    - **skip**: Number of users to skip
    - **limit**: Maximum number of users to return
    """
    return []

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "User not found"}
    }
)
async def get_user(user_id: int):
    """Get a specific user by their ID."""
    return {"id": user_id}

# main.py
app = FastAPI(
    title="My API",
    description="API with organized routers",
    version="1.0.0"
)

app.include_router(users_router, prefix="/api/v1")

# Access docs at /docs to see organized endpoints
```

---

## Common Mistakes to Avoid

### 1. Circular Imports

```python
# BAD: Circular import
# api/users.py
from api.items import router as items_router  # Circular!

# GOOD: Use late imports or separate shared code
# api/shared.py
from fastapi import APIRouter
shared_router = APIRouter()

# api/users.py
from api.shared import shared_router
```

### 2. Forgetting Prefix

```python
# BAD: Missing prefix
users_router = APIRouter()

@router.get("/users/")  # Endpoint will be /users/
async def list_users():
    return []

# GOOD: Use prefix
users_router = APIRouter(prefix="/users")

@router.get("/")  # Endpoint will be /users/
async def list_users():
    return []
```

### 3. Duplicate Route Paths

```python
# BAD: Duplicate paths
router = APIRouter()

@router.get("/users/")
async def list_users():
    return []

@router.get("/users/")  # Conflict!
async def get_all_users():
    return []

# GOOD: Use different paths
router = APIRouter()

@router.get("/users/")
async def list_users():
    return []

@router.get("/users/all")  # Different path
async def get_all_users():
    return []
```

---

## Best Practices

1. **Use Prefixes**: Keep routes organized with clear prefixes
2. **Add Tags**: Group endpoints in documentation
3. **Use Dependencies**: Share authentication/authorization logic
4. **Version Your API**: Use version prefixes for backwards compatibility
5. **Keep Routers Focused**: One router per resource/domain
6. **Use Response Models**: Document response schemas
7. **Add Summaries**: Help documentation readability
8. **Handle Errors Consistently**: Use router-level error handlers

---

## Practice Exercises

### Exercise 1: Blog API Router
Create routers for a blog application:
- Posts router (CRUD)
- Comments router (nested under posts)
- Tags router
- Authors router

### Exercise 2: API Versioning
Implement versioned API:
- v1: Basic functionality
- v2: Enhanced features
- Backwards compatibility

### Exercise 3: Router Dependencies
Create router with dependencies:
- Authentication dependency
- Rate limiting
- Request validation

---

## Summary

- APIRouter organizes endpoints into modules
- Use prefixes and tags for clarity
- Implement versioning for backwards compatibility
- Share logic with router dependencies
- Keep routers focused and maintainable
- Use response models for documentation

**Next Lecture**: We'll explore lifecycle events in FastAPI.
