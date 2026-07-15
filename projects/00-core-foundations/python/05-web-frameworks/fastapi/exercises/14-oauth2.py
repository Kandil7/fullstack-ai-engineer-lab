"""
FastAPI Exercise 14 - OAuth2
============================

Topics covered:
- OAuth2 with FastAPI
- Password flow implementation
- Token-based authentication
- Client credentials flow

Requirements:
    pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart

Run any exercise:
    uvicorn 14-oauth2:app1 --reload
    uvicorn 14-oauth2:app2 --reload
    uvicorn 14-oauth2:app3 --reload
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional


# =============================================================================
# Exercise 1: OAuth2 Password Flow Setup
# =============================================================================
# Implement OAuth2 with password flow:
#   - POST /token accepts form data (username, password)
#   - Use OAuth2PasswordRequestForm
#   - Valid users: {"admin": "admin123", "user1": "pass1"}
#   - Return {"access_token": "...", "token_type": "bearer"}
#
# Hints:
#   - OAuth2PasswordRequestForm has username and password fields
#   - The form uses OAuth2 content type: application/x-www-form-urlencoded
#   - Token URL should be "token" (for Swagger UI integration)
#
# Expected behavior:
#   POST http://localhost:8000/token
#   Content-Type: application/x-www-form-urlencoded
#   Body: username=admin&password=admin123
#   Response: {"access_token": "eyJ...", "token_type": "bearer"}
#
# Test with:
#   curl -X POST http://localhost:8000/token \
#     -d "username=admin&password=admin123"
# =============================================================================

app1 = FastAPI(title="Exercise 1 - OAuth2 Password Flow")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

USERS = {
    "admin": "admin123",
    "user1": "pass1",
}


# TODO: Create OAuth2 scheme with tokenUrl
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    # TODO: Implement JWT token creation (simplified)
    pass


@app1.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: Validate credentials and return token
    pass


@app1.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    # TODO: Validate token and return user info
    pass


# =============================================================================
# Exercise 2: OAuth2 with User Object
# =============================================================================
# Create a more complete OAuth2 system:
#   - Pydantic models: User, Token, TokenData
#   - POST /token returns Token model
#   - GET /users/me returns User model (no password)
#   - GET /users/{user_id} returns user info (requires auth)
#   - Include user role in token
#
# Hints:
#   - Create separate Pydantic models for response
#   - Include "role" in token data for RBAC
#   - Use model_dump(exclude={"password"}) to hide password
#
# Expected behavior:
#   POST /token -> Token(access_token, token_type)
#   GET /users/me -> User(username, email, role)
#   GET /users/admin -> User (if requester is admin)
#   GET /users/admin (without token) -> 401
#
# Test with:
#   curl -X POST http://localhost:8000/token -d "username=admin&password=admin123"
#   curl -H "Authorization: Bearer <token>" http://localhost:8000/users/me
# =============================================================================

app2 = FastAPI(title="Exercise 2 - OAuth2 with User Model")


class User(BaseModel):
    username: str
    email: str
    role: str


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


# Database
users_db = {
    "admin": UserInDB(username="admin", email="admin@example.com", role="admin", hashed_password="admin123"),
    "user1": UserInDB(username="user1", email="user1@example.com", role="user", hashed_password="pass1"),
}


# TODO: Create function to get user from DB
def get_user(username: str):
    # TODO: Look up user in users_db
    pass


# TODO: Create function to authenticate user
def authenticate_user(username: str, password: str):
    # TODO: Verify credentials
    pass


# TODO: Create token with role data
def create_token_with_role(user: User):
    # TODO: Include username and role in token
    pass


@app2.post("/token", response_model=Token)
async def login_v2(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: Authenticate and return token
    pass


@app2.get("/users/me", response_model=User)
async def get_current_user_v2(token: str = Depends(oauth2_scheme)):
    # TODO: Decode token and return user
    pass


@app2.get("/users/{username}", response_model=User)
async def get_user_by_name(username: str, token: str = Depends(oauth2_scheme)):
    # TODO: Return user info (requires authentication)
    pass


# =============================================================================
# Exercise 3: Client Credentials Flow
# =============================================================================
# Implement OAuth2 client credentials flow:
#   - POST /token accepts client_id and client_secret
#   - Clients: {"app1": "secret1", "app2": "secret2"}
#   - Each client has specific scopes: ["read", "write", "admin"]
#   - GET /data requires "read" scope
#   - POST /data requires "write" scope
#   - DELETE /data requires "admin" scope
#
# Hints:
#   - Use OAuth2PasswordRequestForm with username=client_id, password=client_secret
#   - Include scopes in token data
#   - Validate required scopes before allowing access
#
# Expected behavior:
#   POST /token (client_id=app1&client_secret=secret1) -> token with scopes
#   GET /data (with valid token) -> 200 OK
#   POST /data (with "read" scope only) -> 403 Forbidden
#
# Test with:
#   curl -X POST http://localhost:8000/token \
#     -d "username=app1&password=secret1"
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Client Credentials Flow")

CLIENTS = {
    "app1": {"secret": "secret1", "scopes": ["read", "write"]},
    "app2": {"secret": "secret2", "scopes": ["read"]},
}


# TODO: Create function to validate client and get scopes
def validate_client(client_id: str, client_secret: str):
    # TODO: Verify client credentials and return scopes
    pass


# TODO: Create dependency to check required scope
def require_scope(required_scope: str):
    # TODO: Return a dependency that checks if token has the required scope
    pass


@app3.post("/token")
async def client_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: Validate client and return token with scopes
    pass


@app3.get("/data")
async def get_data(scope: str = Depends(require_scope("read"))):
    return {"data": ["item1", "item2"]}


@app3.post("/data")
async def create_data(scope: str = Depends(require_scope("write"))):
    return {"message": "Data created"}


@app3.delete("/data")
async def delete_data(scope: str = Depends(require_scope("admin"))):
    return {"message": "Data deleted"}


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 14-oauth2:app1 --reload
#    - POST /token with form data
#    - Use token to access /users/me
#    - Verify Swagger UI "Authorize" button works
#
# 2. Run: uvicorn 14-oauth2:app2 --reload
#    - Test User model responses
#    - Test role-based user access
#
# 3. Run: uvicorn 14-oauth2:app3 --reload
#    - Test different clients with different scopes
#    - Verify scope-based access control
# =============================================================================
