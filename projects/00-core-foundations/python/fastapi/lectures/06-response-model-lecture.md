# Lecture 06: Response Model

## Topic Overview

Response models control what data is sent back to the client. They are essential for security (filtering out sensitive fields like passwords), documentation (generating accurate response schemas), and data transformation (adding computed fields). FastAPI applies response models automatically when you specify `response_model` in the path operation decorator.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `response_model` to control API response shape
2. Filter sensitive fields (like passwords) from responses
3. Apply `response_model_exclude_unset`, `response_model_exclude_none`, and `response_model_exclude_defaults`
4. Define separate request and response models
5. Use computed fields and response metadata
6. Understand when and when NOT to use response models
7. Create standard error response models

---

## Key Concepts

### 1. The response_model Parameter

When you specify `response_model` in a decorator, FastAPI:
1. Takes the return value from your function
2. Filters it to only include fields defined in the response model
3. Validates the filtered data against the response model
4. Serializes it to JSON
5. Generates the correct OpenAPI schema

```python
@app.post("/users/", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    # Even though we return user_db (with password),
    # response_model filters to UserOut fields only
    return user_db
```

### 2. Separate Request and Response Models

The standard pattern is to have different models for input and output:

```python
class UserIn(BaseModel):
    """Client sends this."""
    name: str
    email: str
    password: str  # Sensitive — only in request

class UserDB(BaseModel):
    """Internal representation."""
    id: int
    name: str
    email: str
    password: str  # Stored internally
    is_active: bool
    created_at: str

class UserOut(BaseModel):
    """Client receives this."""
    id: int
    name: str
    email: str
    is_active: bool
    created_at: str
    # No password!
```

### 3. response_model_exclude_unset

Only returns fields that were explicitly set (not defaults):

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/", response_model=Item, response_model_exclude_unset=True)
def create_item(item: Item):
    return item
    # If description and tax were not sent, they won't appear in response
```

### 4. response_model_exclude_none

Excludes fields with `None` values from the response:

```python
@app.get("/items/list", response_model=list[Item], response_model_exclude_none=True)
def list_items():
    items = [
        Item(name="Laptop", description="A laptop", price=999.99),
        Item(name="Phone", price=699.99),  # description is None
    ]
    return items
    # Phone's description field is omitted from response
```

### 5. Response Model with Lists

```python
@app.get("/users/", response_model=list[UserOut])
def list_users():
    return list(users_db.values())
    # Each item in the list is validated against UserOut
```

### 6. Computed/Added Fields

You can add fields in your function that the response model includes:

```python
class UserOutWithMeta(BaseModel):
    id: int
    name: str
    email: str
    profile_url: str = ""  # Computed field

@app.get("/users/{user_id}/profile", response_model=UserOutWithMeta)
def get_user_profile(user_id: int):
    user = users_db[user_id].copy()
    user["profile_url"] = f"/users/{user_id}/profile"  # Added
    return user
```

### 7. Standard Error Response Model

Define a consistent error shape:

```python
class ErrorResponse(BaseModel):
    detail: str
    error_code: int
    timestamp: str

@app.get("/error-demo")
def error_demo():
    raise HTTPException(
        status_code=404,
        detail="Resource not found",
    )
```

### 8. When NOT to Use response_model

- When you need to return arbitrary data shapes
- When you're streaming responses
- When you need raw `Response` objects
- When the response shape varies significantly

```python
from fastapi.responses import JSONResponse

@app.get("/raw")
def raw_response():
    # No response_model — raw dict
    return {"message": "This has no filtering or validation"}
```

---

## Code Examples

### Example 1: Complete Response Model Pattern

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

class UserIn(BaseModel):
    name: str
    email: str
    password: str
    age: int = Field(ge=0, le=150)

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    age: int
    created_at: str

users_db: dict[int, dict] = {}
next_id = 1

@app.post("/users/", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    global next_id
    now = datetime.now().isoformat()
    user_dict = user.model_dump()
    user_dict["id"] = next_id
    user_dict["created_at"] = now
    users_db[next_id] = user_dict
    next_id += 1
    return user_dict  # Password filtered by response_model

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.get("/users/", response_model=list[UserOut])
def list_users():
    return list(users_db.values())
```

### Example 2: Exclude Unset Fields

```python
@app.post("/items/", response_model=Item, response_model_exclude_unset=True)
def create_item(item: Item):
    """Only explicitly set fields appear in response."""
    return item

# Request: {"name": "Widget", "price": 9.99}
# Response: {"name": "Widget", "price": 9.99}
# (description and tax omitted because they weren't sent)
```

### Example 3: Exclude None Values

```python
@app.get("/items/list", response_model=list[Item], response_model_exclude_none=True)
def list_items():
    return [
        Item(name="Laptop", description="A laptop", price=999.99),
        Item(name="Phone", price=699.99),  # description=None, tax=None
    ]
# Response: [
#   {"name": "Laptop", "description": "A laptop", "price": 999.99},
#   {"name": "Phone", "price": 699.99}  # No description/tax fields
# ]
```

### Example 4: Computed Fields

```python
class UserOutWithMeta(BaseModel):
    id: int
    name: str
    email: str
    profile_url: str = ""

@app.get("/users/{user_id}/profile", response_model=UserOutWithMeta)
def get_user_profile(user_id: int):
    user = users_db[user_id].copy()
    user["profile_url"] = f"/users/{user_id}/profile"
    return user
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting response_model leaks data
```python
# DANGEROUS: No response_model
@app.post("/users/")
def create_user(user: UserIn):
    return user.model_dump()  # Includes password!

# Safe: response_model filters output
@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn):
    return user.model_dump()  # Password excluded
```

### Mistake 2: Using response_model when returning raw Response
```python
# Wrong: Can't use response_model with Response objects
from fastapi.responses import Response

@app.get("/raw", response_model=SomeModel)
def raw():
    return Response(content="raw")  # Conflict!

# Fix: Don't use response_model with Response
@app.get("/raw")
def raw():
    return Response(content="raw")
```

### Mistake 3: Confusing response_model with return type hint
```python
# Return type hint is for documentation only
@app.get("/items/")
def list_items() -> list[Item]:  # Just a hint, no filtering!
    return items_db.values()

# response_model actually filters
@app.get("/items/", response_model=list[Item])
def list_items():
    return items_db.values()  # Actually filtered
```

---

## Best Practices

1. **Always use response_model** for API endpoints that return data
2. **Define separate models** for request (UserIn) and response (UserOut)
3. **Never return passwords or secrets** in responses
4. **Use response_model_exclude_unset=True** for PATCH endpoints
5. **Use response_model_exclude_none=True** to clean up optional fields
6. **Add profile_url and metadata** to response models for HATEOAS
7. **Define a standard ErrorResponse** model for error responses
8. **Document response models** in Swagger for client code generation

---

## Practice Exercises

### Exercise 1: Secure User API
Create UserIn (with password) and UserOut (without password) models. Implement create and list endpoints with response_model.

### Exercise 2: Item Response
Create ItemIn and ItemOut models. Use response_model_exclude_unset=True for POST and response_model_exclude_none=True for GET.

### Exercise 3: Profile Endpoint
Create a UserOutWithMeta that adds a computed `profile_url` field.

### Exercise 4: List Response
Create a paginated list endpoint with response_model=list[Item] and pagination metadata.

### Exercise 5: Error Model
Create a standard ErrorResponse model and use it in a custom error handler.

---

## Summary

| Concept | Description |
|---------|-------------|
| `response_model` | Controls what fields appear in the response |
| `UserIn` / `UserOut` | Separate models for input vs output |
| `exclude_unset` | Only explicitly set fields |
| `exclude_none` | Omit None values |
| `exclude_defaults` | Omit default values |
| Computed fields | Add extra fields in the function |
| Security | Filter sensitive data from responses |
| Documentation | Generates accurate OpenAPI schemas |

Response models are your API's security guard and documentation engine. Always use them to protect sensitive data and provide accurate API documentation.

---

## Quick Reference

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserIn(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

# Filter response
@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn):
    return {"id": 1, **user.model_dump()}

# Exclude unset
@app.post("/items/", response_model=Item, response_model_exclude_unset=True)
def create_item(item: Item):
    return item

# Exclude None
@app.get("/items/", response_model=list[Item], response_model_exclude_none=True)
def list_items():
    return items
```
