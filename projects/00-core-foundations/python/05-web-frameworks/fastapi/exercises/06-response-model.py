"""
FastAPI Exercise 06 - Response Model
======================================

Topics covered:
- Response model for output representation
- Different models for input vs output
- Status codes in responses
- Response headers
- Pagination patterns

Run:
    uvicorn 06-response-model:app --reload
"""

from fastapi import FastAPI, HTTPException, Header, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Response Model Exercise")

# In-memory stores
users_db: dict[int, dict] = {}
items_db: dict[int, dict] = {}
next_user_id = 1
next_item_id = 1


# =============================================================================
# Exercise 1: Different Input/Output Models
# =============================================================================
class UserCreate(BaseModel):
    """Input model - includes password."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """Output model - excludes password."""
    id: int
    username: str
    email: str
    is_active: bool = True


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """Create user - password in request, not in response."""
    global next_user_id
    user_data = {"id": next_user_id, "username": user.username, "email": user.email, "is_active": True}
    users_db[next_user_id] = user_data
    next_user_id += 1
    return UserResponse(**user_data)


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get user by ID."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**users_db[user_id])


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    """Create item."""
    global next_item_id
    item_data = {"id": next_item_id, **item.model_dump()}
    items_db[next_item_id] = item_data
    next_item_id += 1
    return ItemResponse(**item_data)


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    """Get item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse(**items_db[item_id])


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """Delete item - returns no content."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]


# =============================================================================
# Exercise 2: Response Headers and Pagination
# =============================================================================
class UserPublic(BaseModel):
    """Public user info."""
    id: int
    username: str


class LoginResponse(BaseModel):
    """Login success response."""
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


@app.get("/users", response_model=list[UserPublic])
def list_users(response: Response):
    """List users with custom header."""
    users = [UserPublic(**u) for u in users_db.values()]
    response.headers["X-User-Count"] = str(len(users))
    return users


@app.post("/login", response_model=LoginResponse)
def login(email: str, password: str):
    """Simple login returning token and user info."""
    # Find user by email (simplified)
    for uid, u in users_db.items():
        if u.get("email") == email:
            return LoginResponse(
                access_token="fake-jwt-token",
                user=UserPublic(id=uid, username=u["username"])
            )
    raise HTTPException(status_code=401, detail="Invalid credentials")
