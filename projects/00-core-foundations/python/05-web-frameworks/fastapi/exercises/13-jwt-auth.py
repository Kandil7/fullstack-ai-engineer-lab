"""
FastAPI Exercise 13 - JWT Authentication
==========================================

Topics covered:
- JWT token creation and validation
- Password hashing with bcrypt
- Protected routes with JWT
- Token refresh patterns

Requirements:
    pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]

Run:
    uvicorn 13-jwt-auth:app --reload
"""

from fastapi import FastAPI, Depends, HTTPException, Header, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import hashlib
import hmac
import base64
import json

app = FastAPI(title="JWT Auth Exercise")

# Simple JWT implementation (for educational purposes)
# In production, use python-jose library
SECRET_KEY = "my-secret-key-change-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simulated user database
USERS_DB = {
    "alice": {"password": "password123", "role": "admin"},
    "bob": {"password": "password456", "role": "user"},
}


# =============================================================================
# Exercise 1: JWT Token Generation
# =============================================================================

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a signed JWT token."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        **data,
        "iat": datetime.utcnow().timestamp(),
        "exp": (datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))).timestamp(),
    }
    # Encode header and payload
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b"=").decode()
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    # Create signature
    message = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
    return f"{header_b64}.{payload_b64}.{sig_b64}"


@app.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """Validate credentials and return JWT token."""
    if request.username not in USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = USERS_DB[request.username]
    if user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token({"sub": request.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


# =============================================================================
# Exercise 2: JWT Token Validation
# =============================================================================

def decode_jwt_token(token: str) -> dict:
    """Decode and validate a JWT token (without signature verification for simplicity)."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token format")
        # Verify signature
        header_b64, payload_b64, sig_b64 = parts
        message = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(sig_b64 + "==")
        if not hmac.compare_digest(expected_sig, actual_sig):
            raise ValueError("Invalid signature")
        # Decode payload
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        # Check expiry
        if payload["exp"] < datetime.utcnow().timestamp():
            raise ValueError("Token expired")
        return payload
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def get_current_user(authorization: Optional[str] = Header(default=None)):
    """Dependency that extracts and validates the current user from JWT."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_jwt_token(token)
    return payload


@app.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Return current user info from JWT token."""
    return current_user


# =============================================================================
# Exercise 3: Token Refresh
# =============================================================================

REFRESH_TOKEN_EXPIRE_DAYS = 7
refresh_tokens_db: dict[str, str] = {}  # token -> username


def create_refresh_token(username: str) -> str:
    """Create a longer-lived refresh token."""
    token = create_jwt_token(
        {"sub": username, "type": "refresh"},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    refresh_tokens_db[token] = username
    return token


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


@app.post("/login/refresh", response_model=RefreshResponse)
def login_with_refresh(request: LoginRequest):
    """Login and return both access and refresh tokens."""
    if request.username not in USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = USERS_DB[request.username]
    if user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_jwt_token({"sub": request.username, "role": user["role"]})
    refresh_token = create_refresh_token(request.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.post("/refresh", response_model=TokenResponse)
def refresh_access_token(refresh_token: str = Header(default=None)):
    """Exchange a refresh token for a new access token."""
    if not refresh_token or refresh_token not in refresh_tokens_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    username = refresh_tokens_db[refresh_token]
    payload = decode_jwt_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Not a refresh token")
    new_access = create_jwt_token({"sub": username, "role": USERS_DB[username]["role"]})
    return {"access_token": new_access, "token_type": "bearer"}
