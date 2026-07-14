"""
FastAPI Exercise 13 - JWT Authentication
=========================================

Topics covered:
- JWT (JSON Web Tokens) concepts
- Creating and verifying JWT tokens
- Token expiration and refresh
- Protecting routes with JWT

Requirements:
    pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]

Run any exercise:
    uvicorn 13-jwt-auth:app1 --reload
    uvicorn 13-jwt-auth:app2 --reload
    uvicorn 13-jwt-auth:app3 --reload
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import json


# =============================================================================
# Exercise 1: Basic JWT Token Creation
# =============================================================================
# Create a simple JWT token system:
#   - POST /login accepts {"username": "...", "password": "..."}
#   - Valid users: {"admin": "admin123", "user": "user123"}
#   - Return {"access_token": "<jwt>", "token_type": "bearer"}
#   - Token should expire in 30 minutes
#
# Hints:
#   - Use jose.jwt.encode() to create tokens
#   - Include "sub" (subject) and "exp" (expiration) claims
#   - Secret key: "your-secret-key" (use env var in production)
#   - Algorithm: "HS256"
#
# Expected behavior:
#   POST http://localhost:8000/login
#   Body: {"username": "admin", "password": "admin123"}
#   Response: {"access_token": "eyJ...", "token_type": "bearer"}
#
# Test with:
#   curl -X POST http://localhost:8000/login \
#     -H "Content-Type: application/json" \
#     -d '{"username": "admin", "password": "admin123"}'
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Basic JWT Creation")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

USERS = {
    "admin": "admin123",
    "user": "user123",
}


class LoginRequest(BaseModel):
    username: str
    password: str


# TODO: Create a function to generate JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # TODO: Implement token creation
    pass


@app1.post("/login")
async def login(request: LoginRequest):
    # TODO: Validate credentials and return JWT
    pass


# =============================================================================
# Exercise 2: JWT Token Verification
# =============================================================================
# Extend exercise 1 to verify tokens:
#   - POST /login (from exercise 1)
#   - GET /protected requires valid JWT in Authorization header
#   - GET /me returns current user info from token
#   - Return 401 for invalid/expired tokens
#
# Hints:
#   - Use OAuth2PasswordBearer for token extraction
#   - Use jose.jwt.decode() to verify tokens
#   - Pass token to a dependency function
#
# Expected behavior:
#   POST http://localhost:8000/login -> {"access_token": "..."}
#   GET http://localhost:8000/protected (with valid token) -> 200 OK
#   GET http://localhost:8000/protected (no token) -> 401
#   GET http://localhost:8000/me (with valid token) -> {"username": "admin"}
#
# Test with:
#   TOKEN=$(curl -s -X POST http://localhost:8000/login \
#     -H "Content-Type: application/json" \
#     -d '{"username": "admin", "password": "admin123"}' | jq -r '.access_token')
#   curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/me
# =============================================================================

app2 = FastAPI(title="Exercise 2 - JWT Verification")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# TODO: Create a dependency to get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: Decode and validate the JWT token
    pass


@app2.post("/login")
async def login_v2(request: LoginRequest):
    # TODO: Implement login (same as exercise 1)
    pass


@app2.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "You have access!", "user": user["username"]}


@app2.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    # TODO: Return user info from token
    pass


# =============================================================================
# Exercise 3: Token Refresh
# =============================================================================
# Implement token refresh mechanism:
#   - POST /login returns access_token (15 min) and refresh_token (7 days)
#   - GET /protected requires valid access_token
#   - POST /refresh accepts {"refresh_token": "..."} and returns new access_token
#   - Reject expired refresh tokens
#
# Hints:
#   - Include "type": "access" or "refresh" in token data
#   - Use different expiry times for each token type
#   - Validate token type before accepting refresh
#
# Expected behavior:
#   POST /login -> {"access_token": "...", "refresh_token": "..."}
#   POST /refresh with valid refresh_token -> {"access_token": "new_token"}
#   POST /refresh with expired refresh_token -> 401
#
# Test with:
#   curl -X POST http://localhost:8000/login -d '{"username":"admin","password":"admin123"}'
#   curl -X POST http://localhost:8000/refresh -d '{"refresh_token":"..."}'
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Token Refresh")

REFRESH_TOKEN_EXPIRE_DAYS = 7


# TODO: Create function for refresh tokens
def create_refresh_token(data: dict):
    # TODO: Create token with longer expiry
    pass


@app3.post("/login")
async def login_with_refresh(request: LoginRequest):
    # TODO: Return both access and refresh tokens
    pass


@app3.get("/protected")
async def protected_v3(user: dict = Depends(get_current_user)):
    return {"message": "Protected content", "user": user["username"]}


@app3.post("/refresh")
async def refresh_token(refresh_token: str):
    # TODO: Validate refresh token and return new access token
    pass


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 13-jwt-auth:app1 --reload
#    - Test login with valid/invalid credentials
#    - Verify returned token is valid JWT format
#
# 2. Run: uvicorn 13-jwt-auth:app2 --reload
#    - Test /protected with valid token
#    - Test /protected without token (should be 401)
#    - Test /me to see user info from token
#
# 3. Run: uvicorn 13-jwt-auth:app3 --refresh --reload
#    - Login to get both tokens
#    - Use refresh_token to get new access_token
#    - Verify old access_token still works until expiry
# =============================================================================
