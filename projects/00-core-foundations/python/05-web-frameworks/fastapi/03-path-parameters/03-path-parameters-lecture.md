# Lecture 03: Path Parameters

## Topic Overview

Path parameters are variable segments embedded directly in the URL path. They are one of the most fundamental concepts in REST API design, allowing you to identify specific resources (users, products, orders) by their unique identifiers. FastAPI makes path parameters powerful by providing automatic type conversion, validation, and documentation through Python type hints and the `Path()` function.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define path parameters in URL paths using `{}` syntax
2. Use type hints to automatically validate and convert path parameters
3. Work with multiple path parameters in a single URL
4. Constrain path parameters to predefined values using `Enum`
5. Apply advanced validation using the `Path()` function
6. Handle special path types like `:path` for file paths
7. Work with UUID path parameters
8. Raise `HTTPException` for invalid path parameters

---

## Key Concepts

### 1. Basic Path Parameters

Path parameters are defined by placing a variable name in curly braces `{}` within the URL path. The corresponding function parameter must have a type hint.

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User {user_id}"}
```

**How it works:**
1. FastAPI sees `{user_id}` in the path and `user_id: int` in the function
2. It extracts the value from the URL
3. It converts the string to an `int`
4. It validates the conversion (non-numeric strings cause 422 error)
5. It passes the validated integer to your function

### 2. Type Conversion

FastAPI automatically converts path parameter strings to the declared Python type:

| Type | Example URL | Converted Value |
|------|------------|-----------------|
| `int` | `/items/42` | `42` |
| `float` | `/items/3.14` | `3.14` |
| `str` | `/items/hello` | `"hello"` |
| `bool` | `/items/true` | `True` |
| `UUID` | `/items/550e8400-...` | `UUID('550e8400-...')` |

### 3. Multiple Path Parameters

You can have multiple path parameters in a single URL:

```python
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id,
        "content": f"Post {post_id} by User {user_id}",
    }
```

**Important:** The parameter names in the URL must match the function parameter names exactly.

### 4. Enum for Predefined Values

Use Python's `Enum` class to constrain path parameters to a fixed set of allowed values:

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name is ModelName.resnet:
        return {"model_name": model_name, "message": "Residual Learning FTW!"}
```

**Benefits:**
- Only allowed values are accepted; others return 422
- Swagger UI shows a dropdown of valid values
- Type-safe comparisons (`is ModelName.alexnet`)

### 5. Path() for Advanced Validation

The `Path()` function provides additional validation and documentation options:

```python
from fastapi import Path

@app.get("/products/{product_id}")
def get_product(
    product_id: int = Path(
        ...,                                    # Required (no default)
        title="Product ID",                    # Display name in docs
        description="The unique identifier",   # Description in docs
        ge=1,                                  # Greater than or equal to 1
        le=1000,                               # Less than or equal to 1000
    )
):
    return {"product_id": product_id}
```

**Path() validation constraints:**

| Constraint | Description |
|-----------|-------------|
| `gt` | Greater than (exclusive) |
| `ge` | Greater than or equal |
| `lt` | Less than (exclusive) |
| `le` | Less than or equal |
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `pattern` | Regex pattern for strings |
| `title` | Human-readable name in docs |
| `description` | Description in docs |

### 6. The :path Type Converter

The `:path` converter allows slashes `/` within the parameter value, making it suitable for file paths:

```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path, "exists": True}

# URL: /files/home/user/document.txt
# file_path = "home/user/document.txt"
```

Without `:path`, the parameter stops at the first `/`.

### 7. UUID Path Parameters

FastAPI natively supports UUID type conversion:

```python
from uuid import UUID

@app.get("/orders/{order_id}")
def get_order(order_id: UUID):
    return {"order_id": str(order_id), "status": "shipped"}

# URL: /orders/550e8400-e29b-41d4-a716-446655440000
# order_id = UUID('550e8400-e29b-41d4-a716-446655440000')
```

### 8. Custom Validation with HTTPException

For business logic validation beyond type constraints:

```python
from fastapi import HTTPException

@app.get("/categories/{category_name}")
def get_category(category_name: str):
    allowed = ["electronics", "books", "clothing", "home", "sports"]
    if category_name.lower() not in allowed:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category_name}' not found. Allowed: {allowed}",
        )
    return {"category": category_name.lower(), "item_count": 42}
```

---

## Code Examples

### Example 1: Basic Path Parameter

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User {user_id}"}

# Test:
# GET /users/42     → {"user_id": 42, "name": "User 42"}
# GET /users/abc    → 422 Validation Error
```

### Example 2: Multiple Path Parameters

```python
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id,
    }

# Test:
# GET /users/5/posts/10 → {"user_id": 5, "post_id": 10}
```

### Example 3: Enum Constrained Path

```python
from enum import Enum

class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"

@app.get("/colors/{color}")
def get_color(color: Color):
    return {"color": color, "hex": {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"}[color]}

# Test:
# GET /colors/red    → 200 OK
# GET /colors/yellow → 422 Validation Error
```

### Example 4: Path Validation with Path()

```python
from fastapi import Path

@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., title="Item ID", ge=1, le=1000000)
):
    return {"item_id": item_id}

# Test:
# GET /items/42     → 200 OK
# GET /items/0      → 422 Validation Error (ge=1)
# GET /items/9999999 → 422 Validation Error (le=1000000)
```

### Example 5: File Path Parameter

```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}

# Test:
# GET /files/home/user/document.txt
# → {"file_path": "home/user/document.txt"}
```

---

## Common Mistakes to Avoid

### Mistake 1: Duplicate path parameter names
```python
# Wrong: Two parameters with the same name
@app.get("/items/{item_id}/{item_id}")
def get_item(item_id: int, item_id: str):  # SyntaxError!
    ...

# Fix: Use different names
@app.get("/items/{item_id}/versions/{version_id}")
def get_item_version(item_id: int, version_id: int): ...
```

### Mistake 2: Wrong order with static paths
```python
# Wrong: This catches /users/me as user_id="me"
@app.get("/users/{user_id}")
def get_user(user_id: int): ...

# Fix: Put /users/me BEFORE /users/{user_id}
@app.get("/users/me")
def get_current_user():
    return {"user_id": "current"}

@app.get("/users/{user_id}")
def get_user(user_id: int): ...
```

### Mistake 3: Not using Enum for fixed values
```python
# Wrong: Manual validation in the function body
@app.get("/status/{code}")
def get_status(code: str):
    if code not in ["200", "404", "500"]:
        return {"error": "Invalid"}  # Manual check

# Fix: Use Enum for automatic validation
class StatusCode(str, Enum):
    ok = "200"
    not_found = "404"
    server_error = "500"

@app.get("/status/{code}")
def get_status(code: StatusCode):
    # Only valid codes reach here
    ...
```

### Mistake 4: Forgetting type conversion
```python
# Without type hint, no conversion happens
@app.get("/items/{item_id}")
def get_item(item_id):  # item_id is always a string!
    return {"id": item_id + 1}  # TypeError!

# With type hint, conversion is automatic
@app.get("/items/{item_id}")
def get_item(item_id: int):  # item_id is an int
    return {"id": item_id + 1}  # Works!
```

---

## Best Practices

1. **Use descriptive parameter names** — `user_id` is better than `id`
2. **Always specify types** — enables automatic validation
3. **Use Enum for fixed values** — better docs and validation
4. **Use Path() for constraints** — `ge`, `le`, `min_length`, etc.
5. **Order routes carefully** — static paths before parameterized ones
6. **Use `:path` for file paths** — allows slashes in the parameter
7. **Use UUID for unique identifiers** — more secure than sequential integers
8. **Add `title` and `description`** to Path() for better Swagger docs

---

## Practice Exercises

### Exercise 1: User Profile
Create `GET /users/{user_id}/profile` returning user profile data.

### Exercise 2: Book Chapters
Create `GET /books/{book_id}/chapters/{chapter_id}` returning chapter info.

### Exercise 3: Enum Colors
Create a `Color` enum (red, green, blue, yellow) and `GET /colors/{color}` that returns the hex code.

### Exercise 4: File Download
Create `GET /download/{file_path:path}` that simulates file download.

### Exercise 5: Validation
Create `GET /products/{product_id}` with `product_id` constrained to `ge=1, le=999999`.

---

## Summary

| Concept | Description |
|---------|-------------|
| `{param}` | Defines a path parameter in the URL |
| Type hints | Enable automatic conversion and validation |
| Multiple params | Can have several path parameters per URL |
| `Enum` | Constrains to a fixed set of allowed values |
| `Path()` | Adds validation constraints and documentation |
| `:path` type | Allows slashes within the parameter |
| `UUID` | Native support for UUID path parameters |
| `HTTPException` | For business logic validation errors |

Path parameters are the building blocks of resource identification in REST APIs. Master them and you can design clean, type-safe, well-documented API routes.

---

## Quick Reference

```python
from fastapi import FastAPI, Path, HTTPException
from enum import Enum
from uuid import UUID

app = FastAPI()

# Basic
@app.get("/items/{item_id}")
def get_item(item_id: int): ...

# Multiple
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int): ...

# Enum
class Color(str, Enum):
    red = "red"
    green = "green"

@app.get("/colors/{color}")
def get_color(color: Color): ...

# Validation
@app.get("/products/{product_id}")
def get_product(product_id: int = Path(..., ge=1, le=10000)): ...

# File path
@app.get("/files/{file_path:path}")
def read_file(file_path: str): ...

# UUID
@app.get("/orders/{order_id}")
def get_order(order_id: UUID): ...
```
