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

from fastapi import FastAPI, Form, HTTPException, Header
from typing import Optional


# =============================================================================
# Exercise 1: Basic Form Data
# =============================================================================

app1 = FastAPI(title="Exercise 7.1 - Basic Form Data")


@app1.post("/login")
def login_form(
    username: str = Form(...),
    password: str = Form(...),
):
    """Authenticate user from form data."""
    return {"username": username, "authenticated": True}


@app1.post("/feedback")
def submit_feedback(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    rating: int = Form(...),
):
    """Submit feedback via form data."""
    return {"received": True, "name": name, "rating": rating}


# =============================================================================
# Exercise 2: OAuth2 Password Flow
# =============================================================================

app2 = FastAPI(title="Exercise 7.2 - OAuth2 Password Flow")

VALID_USERS = {"alice": "secret123", "bob": "password456"}
VALID_TOKENS = {
    "alice": "fake-token-alice-123",
    "bob": "fake-token-bob-456",
}


@app2.post("/token")
def get_token(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: str = Form(default="password"),
):
    """Validate credentials and return access token."""
    if username not in VALID_USERS or VALID_USERS[username] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": VALID_TOKENS[username], "token_type": "bearer"}


@app2.get("/protected")
def protected_route(authorization: Optional[str] = Header(default=None)):
    """Validate Bearer token and return user info."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.replace("Bearer ", "")
    # Find user by token
    for user, tok in VALID_TOKENS.items():
        if tok == token:
            return {"message": "Welcome!", "user": user}
    raise HTTPException(status_code=401, detail="Invalid token")


# =============================================================================
# Exercise 3: Mixed Form and File-like Data
# =============================================================================

app3 = FastAPI(title="Exercise 7.3 - Mixed Form Data")


@app3.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    agree_terms: bool = Form(...),
):
    """Register user with terms agreement check."""
    if not agree_terms:
        raise HTTPException(status_code=400, detail="Must agree to terms")
    return {"registered": True, "username": username}


@app3.post("/settings")
def update_settings(
    theme: str = Form(...),
    language: str = Form(...),
    notifications: bool = Form(...),
    newsletter: bool = Form(...),
):
    """Update user settings from form data."""
    return {"settings": {
        "theme": theme,
        "language": language,
        "notifications": notifications,
        "newsletter": newsletter,
    }}
