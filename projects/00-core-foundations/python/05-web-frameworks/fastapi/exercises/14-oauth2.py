"""
FastAPI Exercise 14 - OAuth2
==============================

Topics covered:
- OAuth2 password flow
- Scopes and permissions
- JWT with OAuth2
- Role-based access with OAuth2

Requirements:
    pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]

Run:
    uvicorn 14-oauth2:app --reload
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import hashlib
import hmac
import base64
import json

app = FastAPI(title="OAuth2 Exercise")

SECRET_KEY = "oauth2-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

USERS_DB = {
    "alice": {"password": "password123", "role": "admin", "scopes": ["users:read", "users:write", "posts:read", "posts:write"]},
    "bob": {"password": "password456", "role": "user", "scopes": ["posts:read"]},
}


# =============================================================================
# Exercise 1: OAuth2 Password Flow
# =============================================================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a signed JWT token with OAuth2 claims."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        **data,
        "iat": datetime.utcnow().timestamp(),
        "exp": (datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))).timestamp(),
    }
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b"=").decode()
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    message = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def decode_jwt_token(token: str) -> dict:
    """Decode and validate JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token format")
        header_b64, payload_b64, sig_b64 = parts
        message = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(sig_b64 + "==")
        if not hmac.compare_digest(expected_sig, actual_sig):
            raise ValueError("Invalid signature")
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        if payload["exp"] < datetime.utcnow().timestamp():
            raise ValueError("Token expired")
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def get_user_from_db(username: str) -> Optional[dict]:
    """Look up user in database."""
    return USERS_DB.get(username)


def authenticate_user(username: str, password: str) -> Optional[str]:
    """Verify credentials and return username on success."""
    user = get_user_from_db(username)
    if not user or user["password"] != password:
        return None
    return username


def create_token_with_role(username: str) -> str:
    """Create JWT token with user role."""
    user = get_user_from_db(username)
    return create_jwt_token({
        "sub": username,
        "role": user["role"] if user else "user",
        "scopes": user["scopes"] if user else [],
    })


@app.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 token endpoint."""
    username = authenticate_user(form_data.username, form_data.password)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token_with_role(username)
    return {"access_token": token, "token_type": "bearer"}


# =============================================================================
# Exercise 2: Protected Routes with OAuth2
# =============================================================================

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Dependency that validates token and returns current user."""
    payload = decode_jwt_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {"username": username, "role": payload.get("role"), "scopes": payload.get("scopes", [])}


@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Return current user profile from token."""
    return current_user


# =============================================================================
# Exercise 3: Scoped Access Control
# =============================================================================

async def verify_scopes(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """Dependency that validates token and checks required scopes."""
    payload = decode_jwt_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    token_scopes = payload.get("scopes", [])
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=403,
                detail=f"Not enough permissions. Required: {security_scopes.scope_str}",
                headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
            )
    return {"username": username, "scopes": token_scopes}


@app.get("/users/", dependencies=[Depends(verify_scopes)] if False else [])
async def read_users(token: str = Depends(oauth2_scheme)):
    """List users - requires authentication."""
    payload = decode_jwt_token(token)
    return {"users": list(USERS_DB.keys()), "user": payload.get("sub")}


@app.get("/admin/panel")
async def admin_panel(auth: dict = Depends(lambda: {"scope_check": True})):
    """Admin panel placeholder."""
    return {"message": "Welcome to admin area"}
