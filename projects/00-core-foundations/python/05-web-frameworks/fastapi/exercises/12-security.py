"""
FastAPI Exercise 12 - Security
===============================

Topics covered:
- Security concepts in FastAPI
- API Key authentication
- OAuth2 password flow basics
- Security dependencies

Requirements:
    pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]

Run any exercise:
    uvicorn 12-security:app1 --reload
    uvicorn 12-security:app2 --reload
    uvicorn 12-security:app3 --reload
"""

from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from typing import Optional


# =============================================================================
# Exercise 1: API Key Authentication
# =============================================================================

app1 = FastAPI(title="Exercise 1 - API Key Auth")

API_KEYS = ["secret123", "key456", "key789"]

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: Optional[str] = Security(api_key_header)):
    """Dependency that validates the API key."""
    if not api_key or api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
    return api_key


@app1.get("/api/public")
def public_data():
    """Public endpoint - no authentication required."""
    return {"data": "This is public"}


@app1.get("/api/data")
def protected_data(api_key: str = Depends(verify_api_key)):
    """Protected endpoint - requires valid API key."""
    return {"data": "This is protected", "key_valid": True}


# =============================================================================
# Exercise 2: HTTP Basic Authentication
# =============================================================================

app2 = FastAPI(title="Exercise 2 - HTTP Basic Auth")

security = HTTPBasic()

USERS = {
    "admin": "admin123",
    "user1": "pass1",
}


def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """Dependency for basic auth - validates any valid user."""
    user = credentials.username
    if user not in USERS or USERS[user] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


def require_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Dependency for admin-only access."""
    user = credentials.username
    if user not in USERS or USERS[user] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    if user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


@app2.get("/dashboard")
def dashboard(admin: str = Depends(require_admin)):
    """Admin-only dashboard."""
    return {"dashboard": "Admin panel", "user": admin}


@app2.get("/profile")
def profile(user: str = Depends(verify_basic_auth)):
    """User profile - any valid user can access."""
    return {"profile": "User profile", "user": user}


# =============================================================================
# Exercise 3: Role-Based Access Control
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Role-Based Access Control")


# User database with roles
ROLE_USERS = {
    "admin": "admin123",
    "editor": "edit123",
    "viewer": "view123",
}

USER_ROLES = {
    "admin": "admin",
    "editor": "editor",
    "viewer": "viewer",
}


def role_required(allowed_roles: list[str]):
    """Factory that creates a dependency checking for a specific role."""
    def role_checker(x_api_key: Optional[str] = Header(default=None)):
        if not x_api_key:
            raise HTTPException(status_code=401, detail="Missing X-API-Key header")
        # Validate key and determine user
        username = None
        for user, key in ROLE_USERS.items():
            if key == x_api_key:
                username = user
                break
        if not username:
            raise HTTPException(status_code=401, detail="Invalid API key")
        # Check role
        user_role = USER_ROLES[username]
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail=f"Role '{user_role}' not allowed")
        return username
    return role_checker


@app3.get("/users")
def list_users(role: str = Depends(role_required(["admin"]))):
    """Admin-only - list all users."""
    return {"users": list(ROLE_USERS.keys())}


@app3.get("/posts")
def list_posts(role: str = Depends(role_required(["admin", "editor"]))):
    """Editor+ access - list posts."""
    return {"posts": ["post1", "post2"]}


@app3.get("/comments")
def list_comments(role: str = Depends(role_required(["admin", "editor", "viewer"]))):
    """All authenticated users - list comments."""
    return {"comments": ["comment1", "comment2"]}
