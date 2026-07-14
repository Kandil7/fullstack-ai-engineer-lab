"""
06 - Response Model
=====================
Response models let you control what data is sent back to the client.
They filter out internal fields, validate output, and generate better docs.

Run: uvicorn 06-response-model:app --reload
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="Response Models in FastAPI")


# ----- Models -----
class UserIn(BaseModel):
    """What the client sends (request body)."""
    name: str
    email: str
    password: str           # Sensitive — should NOT be in response
    age: int = Field(ge=0, le=150)


class UserDB(BaseModel):
    """Internal representation (includes stored data)."""
    id: int
    name: str
    email: str
    password: str           # Still stored internally
    age: int
    is_active: bool = True
    created_at: str
    updated_at: str | None = None


class UserOut(BaseModel):
    """What the client receives (response). password is excluded."""
    id: int
    name: str
    email: str
    age: int
    is_active: bool
    created_at: str


class UserOutWithMeta(BaseModel):
    """Response with additional metadata."""
    id: int
    name: str
    email: str
    age: int
    is_active: bool
    created_at: str
    profile_url: str = ""


class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str
    error_code: int
    timestamp: str


# In-memory DB
users_db: dict[int, dict] = {}
next_id = 1


@app.post("/users/", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    """
    response_model=UserOut ensures:
    1. The response only includes fields in UserOut (no password!)
    2. The response is validated against UserOut
    3. Swagger UI shows UserOut schema
    """
    global next_id
    now = datetime.now().isoformat()
    user_db = UserDB(
        id=next_id,
        name=user.name,
        email=user.email,
        password=user.password,  # Stored internally
        age=user.age,
        created_at=now,
    )
    users_db[next_id] = user_db.model_dump()
    next_id += 1
    return user_db  # FastAPI filters to UserOut fields only


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """GET with response_model filters output automatically."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.get("/users/", response_model=list[UserOut])
def list_users():
    """Response model works with lists too."""
    return list(users_db.values())


@app.get("/users/{user_id}/profile", response_model=UserOutWithMeta)
def get_user_profile(user_id: int):
    """Adding computed fields to the response."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[user_id].copy()
    user["profile_url"] = f"/users/{user_id}/profile"
    return user


# ----- Exclude unset fields -----
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/", response_model=Item, response_model_exclude_unset=True)
def create_item(item: Item):
    """
    response_model_exclude_unset=True means:
    Only fields that were explicitly set are included in the response.
    If description and tax were not sent, they won't appear in output.
    """
    return item


# ----- ExcludeNone / ExcludeDefaults / Exclude_unset -----
@app.get("/items/list", response_model=list[Item], response_model_exclude_none=True)
def list_items():
    """
    response_model_exclude_none=True means:
    Fields set to None won't appear in the response.
    """
    items = [
        Item(name="Laptop", description="A laptop", price=999.99, tax=89.99),
        Item(name="Phone", price=699.99),  # description and tax are None
        Item(name="Tablet", description="A tablet", price=499.99),
    ]
    return items


# ----- Error response model -----
@app.get("/error-demo")
def error_demo():
    """Demonstrates returning a structured error."""
    raise HTTPException(
        status_code=404,
        detail="Resource not found",
    )


# ----- Custom response using dict -----
@app.get("/custom-response")
def custom_response():
    """
    When you don't use response_model, you return raw dicts.
    No filtering or validation is applied to the response.
    """
    return {
        "message": "This is a raw dict response",
        "no_validation": True,
        "password_leaked": "should-not-be-here",  # Dangerous without response_model!
    }


# ----- Multiple response models -----
@app.get("/users/{user_id}/full", response_model=UserOut)
def get_user_full(user_id: int, include_metadata: bool = False):
    """
    Different response shapes based on query params.
    In production, use responses={} in @app.get() for multiple schemas.
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[user_id].copy()
    if include_metadata:
        user["profile_url"] = f"/users/{user_id}/profile"
    return user


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/users/ -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com", "password": "secret123", "age": 30}'
    # Notice: 'password' is NOT in the response

    curl http://127.0.0.1:8000/users/1

    curl http://127.0.0.1:8000/users/

    curl http://127.0.0.1:8000/users/1/profile

    curl -X POST http://127.0.0.1:8000/items/ -H "Content-Type: application/json" -d '{"name": "Widget", "price": 9.99}'
    # Notice: Only 'name' and 'price' appear (unset fields excluded)

    curl http://127.0.0.1:8000/items/list
    # Notice: None fields are excluded

    curl http://127.0.0.1:8000/custom-response
    # WARNING: No response_model — no filtering!
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
