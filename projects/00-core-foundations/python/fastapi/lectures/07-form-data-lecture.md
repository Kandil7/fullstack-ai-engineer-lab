# Lecture 07: Form Data

## Topic Overview

HTML forms submit data as `application/x-www-form-urlencoded` or `multipart/form-data`, not JSON. FastAPI handles form data using the `Form()` function. This lecture covers form-based login, registration forms, contact forms, file + form combinations, and serving HTML forms from FastAPI.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `Form()` to declare form data parameters
2. Handle required and optional form fields
3. Apply validation constraints to form fields
4. Serve HTML forms from FastAPI endpoints
5. Combine form data with file uploads
6. Use `HTMLResponse` for serving HTML content
7. Understand when to use forms vs JSON request bodies

---

## Key Concepts

### 1. Form() Function

When a function parameter is a simple type (str, int, bool) without `Body()`, `Query()`, or `Path()`, FastAPI treats it as a form field. However, you must explicitly use `Form()` to indicate form data.

```python
from fastapi import Form

@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    # Content-Type: application/x-www-form-urlencoded
    # username=admin&password=secret
    return {"username": username}
```

**Important:** You must install `python-multipart` for form handling:
```bash
pip install python-multipart
```

### 2. Required vs Optional Form Fields

```python
# Required (uses ...)
@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    ...

# Optional (has default)
@app.post("/contact/")
def contact(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(default="General Inquiry"),
    message: str = Form(...),
):
    ...
```

### 3. Form Field Validation

Apply constraints using `Form()` parameters:

```python
@app.post("/register/")
def register(
    username: str = Form(..., min_length=3, max_length=20),
    email: str = Form(...),
    password: str = Form(..., min_length=8),
    role: str = Form(default="user"),
):
    ...
```

### 4. Boolean Form Fields

```python
@app.post("/feedback/")
def feedback(
    rating: int = Form(..., ge=1, le=5),
    comment: str = Form(default=""),
    recommend: bool = Form(default=True),
):
    ...
```

### 5. Serving HTML Forms

Use `HTMLResponse` to serve HTML content:

```python
from fastapi.responses import HTMLResponse

@app.get("/form", response_class=HTMLResponse)
def get_form():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Login Form</title></head>
    <body>
        <h1>Login</h1>
        <form action="/login/" method="post">
            <input type="text" name="username" required><br><br>
            <input type="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """
```

### 6. Form + Response Model

Use Pydantic models for structured responses:

```python
from pydantic import BaseModel

class RegistrationResult(BaseModel):
    username: str
    email: str
    role: str
    message: str

@app.post("/register/", response_model=RegistrationResult)
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    role: str = Form(default="user"),
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    return RegistrationResult(
        username=username,
        email=email,
        role=role,
        message="Registration successful!",
    )
```

### 7. Form Data vs JSON

| Feature | Form Data | JSON |
|---------|-----------|------|
| Content-Type | `application/x-www-form-urlencoded` | `application/json` |
| File upload | Yes (multipart) | No |
| Nested data | No | Yes |
| Complex types | No | Yes |
| Browser forms | Native | Requires JS |
| FastAPI syntax | `Form(...)` | Pydantic model |

---

## Code Examples

### Example 1: Login Form

```python
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret":
        return {"message": "Login successful", "username": "username"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/form", response_class=HTMLResponse)
def get_form():
    return """
    <form action="/login/" method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    """
```

### Example 2: Contact Form

```python
@app.post("/contact/")
def contact_form(
    name: str = Form(..., min_length=1),
    email: str = Form(...),
    subject: str = Form(default="General Inquiry"),
    message: str = Form(..., min_length=10),
    subscribe: bool = Form(default=False),
):
    return {
        "status": "received",
        "name": name,
        "email": email,
        "subject": subject,
        "message_length": len(message),
        "subscribed": subscribe,
    }
```

### Example 3: Registration with Validation

```python
@app.post("/register/")
def register_user(
    username: str = Form(..., min_length=3, max_length=20),
    email: str = Form(...),
    password: str = Form(..., min_length=8),
    confirm_password: str = Form(...),
    role: str = Form(default="user"),
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    valid_roles = ["user", "admin", "moderator"]
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role")

    return {"username": username, "role": role, "message": "Success!"}
```

### Example 4: Feedback Form

```python
@app.post("/feedback/")
def submit_feedback(
    rating: int = Form(..., ge=1, le=5),
    comment: str = Form(default=""),
    recommend: bool = Form(default=True),
):
    return {
        "rating": rating,
        "stars": "★" * rating + "☆" * (5 - rating),
        "would_recommend": recommend,
    }
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting python-multipart
```bash
# Wrong: ImportError
from fastapi import Form

# Fix: Install the package
pip install python-multipart
```

### Mistake 2: Not using Form() for form data
```python
# Wrong: FastAPI treats this as a query parameter
@app.post("/login/")
def login(username: str, password: str):
    ...

# Fix: Use Form() explicitly
@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    ...
```

### Mistake 3: Mixing Form() and Body() in same endpoint
```python
# Wrong: Can't mix form data with JSON body
@app.post("/mixed/")
def mixed(item: Item, name: str = Form(...)):
    ...

# Fix: Use one or the other
@app.post("/json/")
def json_only(item: Item): ...

@app.post("/form/")
def form_only(name: str = Form(...)): ...
```

### Mistake 4: Not validating form data
```python
# Wrong: No validation on form fields
@app.post("/register/")
def register(username: str = Form(...)):
    ...

# Fix: Add validation constraints
@app.post("/register/")
def register(username: str = Form(..., min_length=3, max_length=20)):
    ...
```

---

## Best Practices

1. **Always install `python-multipart`** when using forms
2. **Use `Form(...)` explicitly** for form data parameters
3. **Add validation constraints** to form fields
4. **Serve HTML forms** for browser-based testing
5. **Use `HTMLResponse`** for serving HTML content
6. **Validate passwords match** in registration forms
7. **Use response_model** for structured form responses
8. **Don't mix Form() and Body()** in the same endpoint

---

## Practice Exercises

### Exercise 1: Login Form
Create a login endpoint with username and password form fields. Include an HTML form.

### Exercise 2: Registration Form
Create a registration form with: username, email, password, confirm_password, role (select). Validate all fields.

### Exercise 3: Contact Form
Create a contact form with: name, email, subject (dropdown), message (textarea), subscribe (checkbox).

### Exercise 4: Feedback Form
Create a feedback form with: rating (1-5), comment, recommend (yes/no).

### Exercise 5: Multi-Form Page
Create an HTML page with both login and registration forms on the same page.

---

## Summary

| Concept | Description |
|---------|-------------|
| `Form(...)` | Declares a required form field |
| `Form(default=...)` | Declares an optional form field |
| `python-multipart` | Required package for form handling |
| `HTMLResponse` | Serves HTML content from endpoints |
| Form validation | Using constraints in Form() |
| Form + JSON | Cannot mix both in same endpoint |
| HTML forms | Served from GET endpoints |

Form data is essential for traditional web applications and browser-based forms. FastAPI handles it seamlessly with the `Form()` function.

---

## Quick Reference

```python
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

# Required form field
@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)): ...

# With validation
@app.post("/register/")
def register(
    username: str = Form(..., min_length=3),
    password: str = Form(..., min_length=8),
    role: str = Form(default="user"),
): ...

# Serve HTML form
@app.get("/form", response_class=HTMLResponse)
def get_form():
    return '<form action="/login/" method="post">...</form>'
```
