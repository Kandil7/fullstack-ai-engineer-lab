"""
13 - JWT Authentication
=========================
JSON Web Tokens (JWT) for stateless authentication.
Includes access tokens, refresh tokens, and token blacklisting.

Requires: pip install python-jose[cryptography] passlib[bcrypt]

Run: uvicorn 13-jwt-auth:app --reload
"""

from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI(title="JWT Authentication in FastAPI")


# ----- Config -----
SECRET_KEY = "super-secret-jwt-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ----- Password hashing -----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----- Models -----
class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str  # "access" or "refresh"


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# ----- In-memory storage -----
users_db: dict[str, dict] = {}
refresh_tokens_db: set[str] = set()  # For refresh token tracking
next_id = 1


# ----- Helper functions -----
def create_token(data: dict, expires_delta: timedelta, token_type: str = "access") -> str:
    """Create a JWT with expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_token_pair(username: str) -> TokenPair:
    """Create both access and refresh tokens."""
    access_token = create_token(
        {"sub": username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "access",
    )
    refresh_token = create_token(
        {"sub": username},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh",
    )
    refresh_tokens_db.add(refresh_token)
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


def decode_token(token: str, expected_type: str = "access") -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token type. Expected {expected_type}",
            )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ----- OAuth2 scheme -----
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Get the current user from access token."""
    payload = decode_token(token, "access")
    username = payload.get("sub")
    if username is None or username not in users_db:
        raise HTTPException(status_code=401, detail="User not found")
    return users_db[username]


# ----- Endpoints -----
@app.post("/register/", status_code=201)
def register(user: UserCreate):
    """Register a new user."""
    global next_id
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username taken")
    users_db[user.username] = {
        "id": next_id,
        "username": user.username,
        "email": user.email,
        "hashed_password": pwd_context.hash(user.password),
    }
    next_id += 1
    return {"message": "Registered", "username": user.username}


@app.post("/login/", response_model=TokenPair)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and receive access + refresh tokens."""
    user = users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return create_token_pair(form_data.username)


@app.post("/refresh/", response_model=TokenPair)
def refresh_token(refresh_token: str):
    """Exchange refresh token for new token pair."""
    if refresh_token not in refresh_tokens_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    payload = decode_token(refresh_token, "refresh")
    username = payload.get("sub")

    # Revoke old refresh token (token rotation)
    refresh_tokens_db.discard(refresh_token)

    # Issue new pair
    return create_token_pair(username)


@app.post("/logout/")
def logout(refresh_token: str):
    """Logout by revoking the refresh token."""
    refresh_tokens_db.discard(refresh_token)
    return {"message": "Logged out"}


@app.get("/me/")
def get_me(current_user: dict = Depends(get_current_user)):
    """Protected: get current user profile."""
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
    }


@app.get("/protected-data/")
def protected_data(current_user: dict = Depends(get_current_user)):
    """Protected: access sensitive data."""
    return {
        "secret": "This is protected data",
        "user": current_user["username"],
        "timestamp": datetime.now().isoformat(),
    }


# ----- Token info endpoint -----
@app.get("/token/info/")
def token_info(token: str):
    """Decode and display token info (for debugging)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "payload": payload}
    except JWTError as e:
        return {"valid": False, "error": str(e)}


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/register/ -H "Content-Type: application/json" -d '{"username": "alice", "email": "alice@test.com", "password": "secret123"}'

    curl -X POST http://127.0.0.1:8000/login/ -d "username=alice&password=secret123"
    # Save the access_token and refresh_token from response

    curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:8000/me/

    curl -X POST "http://127.0.0.1:8000/refresh/?refresh_token=<REFRESH_TOKEN>"
    # Get new token pair

    curl -X POST "http://127.0.0.1:8000/logout/?refresh_token=<OLD_REFRESH_TOKEN>"
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
