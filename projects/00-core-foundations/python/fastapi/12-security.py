"""
12 - Security
===============
Security basics: API keys, password hashing, OAuth2 password flow,
and security best practices.

Requires: pip install passlib[bcrypt] python-jose[cryptography]

Run: uvicorn 12-security:app --reload
"""

from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI(title="Security in FastAPI")


# ----- Configuration -----
SECRET_KEY = "your-secret-key-keep-it-safe-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ----- Password hashing -----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ----- Models -----
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# ----- In-memory user DB -----
users_db: dict[str, dict] = {}
next_id = 1


def get_user(username: str) -> dict | None:
    return users_db.get(username)


def authenticate_user(username: str, password: str) -> dict | None:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


# ----- JWT Token creation -----
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----- OAuth2 scheme -----
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Decode JWT and return current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


# ----- Registration -----
@app.post("/register/", status_code=201)
def register(user: UserCreate):
    """Register a new user with hashed password."""
    global next_id
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already taken")

    users_db[user.username] = {
        "id": next_id,
        "username": user.username,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "is_active": True,
    }
    next_id += 1
    return {"message": "User registered successfully", "username": user.username}


# ----- Login (OAuth2 compatible) -----
@app.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint compatible with OAuth2 password flow.
    Swagger UI can use this for the "Authorize" button.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ----- Protected endpoint -----
@app.get("/me/")
def get_me(current_user: dict = Depends(get_current_user)):
    """Returns the current authenticated user's profile."""
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
    }


# ----- API Key authentication -----
API_KEYS = {"admin-key-123": "admin", "user-key-456": "user"}


def verify_api_key(x_api_key: str = Header(...)):
    """Simple API key authentication."""
    role = API_KEYS.get(x_api_key)
    if not role:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return {"role": role, "key": x_api_key}


@app.get("/api-key-protected/")
def api_key_endpoint(auth: dict = Depends(verify_api_key)):
    """Endpoint protected by API key."""
    return {"message": "Access granted", "role": auth["role"]}


# ----- Password change -----
@app.post("/change-password/")
def change_password(
    old_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user),
):
    """Change password with verification."""
    if not verify_password(old_password, current_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    users_db[current_user["username"]]["hashed_password"] = hash_password(new_password)
    return {"message": "Password updated successfully"}


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/register/ -H "Content-Type: application/json" -d '{"username": "alice", "email": "alice@test.com", "password": "secret123"}'

    curl -X POST http://127.0.0.1:8000/login/ -d "username=alice&password=secret123"

    # Use the token from login:
    curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/me/

    curl -H "X-Api-Key: admin-key-123" http://127.0.0.1:8000/api-key-protected/
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
