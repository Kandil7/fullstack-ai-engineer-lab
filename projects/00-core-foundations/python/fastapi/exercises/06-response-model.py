"""
FastAPI Exercise 06 - Response Models
======================================

Topics covered:
- Defining response models
- Filtering response fields
- Response status codes
- Multiple response types
- Response headers

Requirements:
    pip install fastapi uvicorn pydantic

Run any exercise:
    uvicorn 06-response-model:app1 --reload
    uvicorn 06-response-model:app2 --reload
    uvicorn 06-response-model:app3 --reload
"""

from fastapi import FastAPI, Response
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# =============================================================================
# Exercise 1: Basic Response Models
# =============================================================================
# Create an app with proper response models:
#   POST /users
#       - Body: {"name": str, "email": str, "password": str, "bio": str (optional)}
#       - Response (UserResponse): {"id": int, "name": str, "email": str, "bio": str}
#       - NOTE: password should NOT be in the response!
#
#   GET /users/{user_id}
#       - Response (UserResponse): same as above
#
# Hints:
#   - Create two models: UserCreate (input) and UserResponse (output)
#   - Use response_model=UserResponse in the decorator
#   - FastAPI auto-filters extra fields from the response
#   - The response_model is like a "filter" on what gets sent back
#
# Expected behavior:
#   POST /users with {"name": "Alice", "email": "a@b.com", "password": "secret123"}
#       -> {"id": 1, "name": "Alice", "email": "a@b.com", "bio": null}
#       (password is NOT returned!)
#
# Test with:
#   curl -X POST http://localhost:8000/users \
#     -H "Content-Type: application/json" \
#     -d '{"name": "Alice", "email": "a@b.com", "password": "secret123"}'
#   curl http://localhost:8000/users/1
# =============================================================================

app1 = FastAPI(title="Exercise 6.1 - Basic Response Models")


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    bio: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    bio: Optional[str] = None


users_db = []


@app1.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    pass  # TODO: Create user (add id), store in users_db, return it


@app1.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    pass  # TODO: Find user by id, return it


# =============================================================================
# Exercise 2: Response with Status Codes
# =============================================================================
# Create an app with proper status codes in responses:
#   POST /items
#       - Response model: ItemResponse
#       - Status code: 201
#       - Return the created item
#
#   DELETE /items/{item_id}
#       - Status code: 200
#       - Return: {"deleted": true, "id": item_id}
#
#   GET /items/{item_id}
#       - If found: 200 with ItemResponse
#       - If not found: 404 with {"detail": "Item not found"}
#
# Hints:
#   - Use status_code=201 in @app.post(...) decorator
#   - For 404, return ({"detail": "Item not found"}, 404)
#   - Or use: from fastapi.responses import JSONResponse
#
# Expected behavior:
#   POST /items -> 201 with item
#   GET /items/999 -> 404 with error message
#   DELETE /items/1 -> 200 with confirmation
#
# Test with:
#   curl -X POST http://localhost:8000/items \
#     -H "Content-Type: application/json" \
#     -d '{"name": "Widget", "price": 9.99}'
#   curl -i http://localhost:8000/items/999
# =============================================================================

app2 = FastAPI(title="Exercise 6.2 - Status Codes")


class ItemCreate(BaseModel):
    name: str
    price: float = Field(gt=0)


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float


items_db = []


@app2.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    pass  # TODO: Create item with id, store in items_db, return it


@app2.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    pass  # TODO: Find item, return 404 if not found


@app2.delete("/items/{item_id}")
def delete_item(item_id: int):
    pass  # TODO: Delete item, return {"deleted": True, "id": item_id}


# =============================================================================
# Exercise 3: Multiple Response Models and Headers
# =============================================================================
# Create an app with:
#   GET /users/{user_id}
#       - response_model=UserPublic (no email, no password)
#       - Add custom header: X-User-Count: <total users>
#
#   GET /users
#       - response_model=list[UserPublic]
#       - Add header: X-Total-Count: <count>
#       - Support query params: ?offset=0&limit=10
#
#   POST /users/login
#       - Body: {"email": str, "password": str}
#       - Return: {"token": "fake-jwt-token", "user": UserPublic}
#       - response_model=LoginResponse
#
# Hints:
#   - Create UserPublic (subset of User fields)
#   - Use response.headers["X-Count"] = str(count) to set headers
#   - Or use: from fastapi import Header; response: Response
#   - Multiple models: different endpoints can have different response_models
#
# Expected behavior:
#   GET /users/1 -> UserPublic (no email) + X-User-Count header
#   GET /users -> list of UserPublic + X-Total-Count header
#   POST /users/login -> {"token": ..., "user": UserPublic}
#
# Test with:
#   curl -i http://localhost:8000/users/1
#   curl -i "http://localhost:8000/users?offset=0&limit=5"
#   curl -X POST http://localhost:8000/users/login \
#     -H "Content-Type: application/json" \
#     -d '{"email": "a@b.com", "password": "secret"}'
# =============================================================================

app3 = FastAPI(title="Exercise 6.3 - Multiple Responses")


class UserPublic(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None


class LoginResponse(BaseModel):
    token: str
    user: UserPublic


users_store = []


@app3.get("/users/{user_id}", response_model=UserPublic)
def get_user_public(user_id: int, response: Response):
    pass  # TODO: Find user, set X-User-Count header, return UserPublic


@app3.get("/users", response_model=list[UserPublic])
def list_users(offset: int = 0, limit: int = 10, response: Response = None):
    pass  # TODO: Return paginated users, set X-Total-Count header


@app3.post("/users/login", response_model=LoginResponse)
def login(email: str = Body(...), password: str = Body(...)):
    pass  # TODO: Find user by email, return LoginResponse with fake token


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 06-response-model:app1 --reload
#    - Verify password is NOT in the response
#    - Verify response matches UserResponse schema
#
# 2. Run: uvicorn 06-response-model:app2 --reload
#    - Verify POST returns 201
#    - Verify GET returns 404 for missing items
#    - Verify DELETE returns confirmation
#
# 3. Run: uvicorn 06-response-model:app3 --reload
#    - Verify custom headers are set
#    - Verify UserPublic excludes email
#    - Verify login returns token + user
# =============================================================================
