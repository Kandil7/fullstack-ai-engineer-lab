"""
FastAPI Exercise 07 - Form Data
================================

Topics covered:
- Receiving form data with Form()
- Form vs JSON body
- OAuth2 with form data (password flow)
- Handling checkboxes and multiple values

Requirements:
    pip install fastapi uvicorn python-multipart

Run any exercise:
    uvicorn 07-form-data:app1 --reload
    uvicorn 07-form-data:app2 --reload
    uvicorn 07-form-data:app3 --reload
"""

from fastapi import FastAPI, Form, Body
from pydantic import BaseModel
from typing import Optional


# =============================================================================
# Exercise 1: Basic Form Data
# =============================================================================
# Create an app that receives form data:
#   POST /login
#       - Form fields: username: str, password: str
#       - Return: {"username": username, "authenticated": true}
#
#   POST /feedback
#       - Form fields: name: str, email: str, message: str, rating: int
#       - Return: {"received": true, "name": name, "rating": rating}
#
# Hints:
#   - Use Form(...) instead of Body(...)
#   - Form fields are sent as application/x-www-form-urlencoded
#   - You CANNOT combine Form() with JSON body in the same endpoint
#   - The python-multipart package is required for form handling
#
# Expected behavior:
#   POST /login with form data -> {"username": "alice", "authenticated": true}
#   POST /feedback with form data -> {"received": true, "name": "Alice", "rating": 5}
#
# Test with:
#   curl -X POST http://localhost:8000/login \
#     -d "username=alice&password=secret123"
#   curl -X POST http://localhost:8000/feedback \
#     -d "name=Alice&email=alice@example.com&message=Great+app!&rating=5"
# =============================================================================

app1 = FastAPI(title="Exercise 7.1 - Basic Form Data")


@app1.post("/login")
def login_form(
    username: str = Form(...),
    password: str = Form(...),
):
    pass  # TODO: Return {"username": username, "authenticated": True}


@app1.post("/feedback")
def submit_feedback(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    rating: int = Form(...),
):
    pass  # TODO: Return {"received": True, "name": name, "rating": rating}


# =============================================================================
# Exercise 2: OAuth2 Password Flow
# =============================================================================
# Create an app with OAuth2-style login:
#   POST /token
#       - Form fields: username: str, password: str, grant_type: str = "password"
#       - If valid: return {"access_token": "fake-token-123", "token_type": "bearer"}
#       - If invalid: return 401 with {"detail": "Invalid credentials"}
#
#   GET /protected
#       - Accept header: Authorization: Bearer <token>
#       - Return: {"message": "Welcome!", "user": username}
#       - If no token: return 401
#
# Hints:
#   - For /token, use Form(...) for all fields
#   - For /protected, use Header to read Authorization
#   - Validate: token == "fake-token-123"
#   - Extract username from token (or hardcode for this exercise)
#
# Expected behavior:
#   POST /token with username=alice&password=secret
#       -> {"access_token": "fake-token-123", "token_type": "bearer"}
#   GET /protected with Authorization: Bearer fake-token-123
#       -> {"message": "Welcome!", "user": "alice"}
#   GET /protected without token -> 401
#
# Test with:
#   curl -X POST http://localhost:8000/token \
#     -d "username=alice&password=secret&grant_type=password"
#   curl http://localhost:8000/protected \
#     -H "Authorization: Bearer fake-token-123"
#   curl http://localhost:8000/protected  # should fail
# =============================================================================

from fastapi import Header

app2 = FastAPI(title="Exercise 7.2 - OAuth2 Password Flow")

VALID_USERS = {"alice": "secret123", "bob": "password456"}


@app2.post("/token")
def get_token(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: str = Form(default="password"),
):
    pass  # TODO: Validate credentials, return token or 401


@app2.get("/protected")
def protected_route(authorization: Optional[str] = Header(default=None)):
    pass  # TODO: Validate Bearer token, return user info or 401


# =============================================================================
# Exercise 3: Mixed Form and File-like Data
# =============================================================================
# Create an app that handles:
#   POST /register
#       - Form fields: username, email, password, agree_terms (bool)
#       - If agree_terms is false: return 400 with {"error": "Must agree to terms"}
#       - If valid: return {"registered": true, "username": username}
#
#   POST /settings
#       - Form fields: theme (light/dark), language (en/es/zh),
#         notifications (bool), newsletter (bool)
#       - Return: {"settings": {all values}}
#
# Hints:
#   - Boolean form fields: ?notifications=true or ?notifications=1
#   - For validation: use if not agree_terms: return error
#   - Or use a Pydantic model with validator (but Forms don't support it directly)
#   - Alternative: validate in the endpoint logic
#
# Expected behavior:
#   POST /register with agree_terms=true -> {"registered": true, ...}
#   POST /register with agree_terms=false -> 400 error
#   POST /settings with all fields -> {"settings": {...}}
#
# Test with:
#   curl -X POST http://localhost:8000/register \
#     -d "username=alice&email=alice@example.com&password=secret&agree_terms=true"
#   curl -X POST http://localhost:8000/settings \
#     -d "theme=dark&language=en&notifications=true&newsletter=false"
# =============================================================================

app3 = FastAPI(title="Exercise 7.3 - Mixed Form Data")


@app3.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    agree_terms: bool = Form(...),
):
    pass  # TODO: Validate agree_terms, return result


@app3.post("/settings")
def update_settings(
    theme: str = Form(...),
    language: str = Form(...),
    notifications: bool = Form(...),
    newsletter: bool = Form(...),
):
    pass  # TODO: Return {"settings": {"theme": theme, "language": language, ...}}


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 07-form-data:app1 --reload
#    - Test login with form data
#    - Test feedback submission
#    - Verify content-type: application/x-www-form-urlencoded
#
# 2. Run: uvicorn 07-form-data:app2 --reload
#    - Test token generation
#    - Test protected route with valid token
#    - Test protected route without token (should 401)
#
# 3. Run: uvicorn 07-form-data:app3 --reload
#    - Test registration with terms agreement
#    - Test registration without terms (should 400)
#    - Test settings update
# =============================================================================
