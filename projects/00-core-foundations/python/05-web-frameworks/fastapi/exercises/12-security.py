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
from pydantic import BaseModel
from typing import Optional


# =============================================================================
# Exercise 1: API Key Authentication
# =============================================================================
# Create an API that requires an API key for access:
#   - Define an API key header: "X-API-Key"
#   - Valid keys: ["secret123", "key456", "key789"]
#   - GET /api/data requires valid API key
#   - GET /api/public returns data without authentication
#
# Hints:
#   - Use APIKeyHeader from fastapi.security
#   - Create a dependency function to validate the key
#   - Return 403 for invalid/missing API keys
#
# Expected behavior:
#   GET http://localhost:8000/api/public -> 200 OK
#   GET http://localhost:8000/api/data (with X-API-Key: secret123) -> 200 OK
#   GET http://localhost:8000/api/data (no header) -> 403
#   GET http://localhost:8000/api/data (wrong key) -> 403
#
# Test with:
#   curl http://localhost:8000/api/public
#   curl -H "X-API-Key: secret123" http://localhost:8000/api/data
# =============================================================================

app1 = FastAPI(title="Exercise 1 - API Key Auth")

API_KEYS = ["secret123", "key456", "key789"]

api_key_header = APIKeyHeader(name="X-API-Key")


# TODO: Create a dependency to validate API key
def verify_api_key(api_key: str = Security(api_key_header)):
    # TODO: Validate the API key
    pass


@app1.get("/api/public")
def public_data():
    return {"data": "This is public"}


@app1.get("/api/data")
def protected_data(api_key: str = Depends(verify_api_key)):
    return {"data": "This is protected", "key_valid": True}


# =============================================================================
# Exercise 2: HTTP Basic Authentication
# =============================================================================
# Create an API with HTTP Basic Auth:
#   - Users: {"admin": "admin123", "user1": "pass1"}
#   - GET /dashboard requires admin credentials
#   - GET /profile requires any valid user
#   - Return proper WWW-Authenticate header on failure
#
# Hints:
#   - Use HTTPBasic from fastapi.security
#   - Access credentials via credentials.username and credentials.password
#   - Use HTTPException with 401 status for auth failures
#
# Expected behavior:
#   GET http://localhost:8000/dashboard (admin:admin123) -> 200 OK
#   GET http://localhost:8000/dashboard (user1:pass1) -> 403 Forbidden
#   GET http://localhost:8000/profile (user1:pass1) -> 200 OK
#   GET http://localhost:8000/dashboard (no credentials) -> 401
#
# Test with:
#   curl -u admin:admin123 http://localhost:8000/dashboard
#   curl -u user1:pass1 http://localhost:8000/dashboard
# =============================================================================

app2 = FastAPI(title="Exercise 2 - HTTP Basic Auth")

security = HTTPBasic()

USERS = {
    "admin": "admin123",
    "user1": "pass1",
}


# TODO: Create dependency for basic auth
def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    # TODO: Validate credentials against USERS dict
    pass


# TODO: Create dependency for admin-only access
def require_admin(credentials: HTTPBasicCredentials = Depends(security)):
    # TODO: Verify user is admin
    pass


@app2.get("/dashboard")
def dashboard(admin: str = Depends(require_admin)):
    return {"dashboard": "Admin panel", "user": admin}


@app2.get("/profile")
def profile(user: str = Depends(verify_basic_auth)):
    return {"profile": "User profile", "user": user}


# =============================================================================
# Exercise 3: Role-Based Access Control
# =============================================================================
# Create an API with role-based access:
#   - Roles: "admin", "editor", "viewer"
#   - Users: {"admin": "admin123", "editor": "edit123", "viewer": "view123"}
#   - GET /users -> requires "admin" role
#   - GET /posts -> requires "editor" or "admin" role
#   - GET /comments -> any authenticated user
#
# Hints:
#   - Pass the required role to the dependency
#   - Use APIKeyHeader for simplicity
#   - Return 403 when user lacks required role
#
# Expected behavior:
#   GET http://localhost:8000/users (admin key) -> 200 OK
#   GET http://localhost:8000/users (editor key) -> 403
#   GET http://localhost:8000/posts (editor key) -> 200 OK
#   GET http://localhost:8000/comments (viewer key) -> 200 OK
#
# Test with:
#   curl -H "X-User-Role: admin" http://localhost:8000/users
#   curl -H "X-User-Role: editor" http://localhost:8000/posts
#   curl -H "X-User-Role: viewer" http://localhost:8000/comments
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Role-Based Access Control")


def role_required(allowed_roles: list[str]):
    # TODO: Create a dependency that checks user role
    # This should return a function that validates role
    pass


@app3.get("/users")
def list_users(role: str = Depends(role_required(["admin"]))):
    return {"users": ["admin", "editor", "viewer"]}


@app3.get("/posts")
def list_posts(role: str = Depends(role_required(["admin", "editor"]))):
    return {"posts": ["post1", "post2"]}


@app3.get("/comments")
def list_comments(role: str = Depends(role_required(["admin", "editor", "viewer"]))):
    return {"comments": ["comment1", "comment2"]}


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 12-security:app1 --reload
#    - Test public endpoint (no auth needed)
#    - Test protected endpoint with valid/invalid API keys
#
# 2. Run: uvicorn 12-security:app2 --reload
#    - Test admin-only dashboard
#    - Test profile with different users
#    - Verify 401/403 responses
#
# 3. Run: uvicorn 12-security:app3 --reload
#    - Test each role against each endpoint
#    - Verify admin has full access
#    - Verify viewer only has read access to comments
# =============================================================================
