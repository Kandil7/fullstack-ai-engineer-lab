"""
14 - OAuth2
=============
OAuth2 implementation with FastAPI: authorization code flow,
password flow, and third-party provider simulation.

Requires: pip install python-jose[cryptography] passlib[bcrypt]

Run: uvicorn 14-oauth2:app --reload
"""

import sys
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
import secrets

# Guarded import: lets the file load (and smoke-test [skip]) when python-jose
# is not installed, while keeping the teaching code unchanged.
try:
    from jose import JWTError, jwt
    JOSE_AVAILABLE = True
except ImportError:
    JWTError = Exception
    jwt = None
    JOSE_AVAILABLE = False

app = FastAPI(title="OAuth2 in FastAPI")


# ----- Config -----
SECRET_KEY = "oauth2-secret-key-change-in-production"
ALGORITHM = "HS256"


# ----- Password hashing -----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----- Models -----
class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None = None
    disabled: bool = False


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthorizationCode(BaseModel):
    code: str
    client_id: str
    redirect_uri: str
    code_verifier: str | None = None  # For PKCE


# ----- In-memory storage -----
users_db: dict[str, UserInDB] = {}
authorization_codes: dict[str, dict] = {}
oauth_clients = {
    "my-app": {
        "client_secret": "app-secret-123",
        "redirect_uris": ["http://localhost:8000/callback"],
    }
}
next_id = 1


# ----- OAuth2 schemes -----
# Password flow (for first-party apps)
oauth2_password_scheme = OAuth2PasswordBearer(tokenUrl="oauth/token")

# Authorization code flow (for third-party apps)
oauth2_auth_code_scheme = OAuth2PasswordBearer(tokenUrl="oauth/token")


# ----- Helper functions -----
def get_user(username: str) -> UserInDB | None:
    return users_db.get(username)


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----- User dependency -----
def get_current_user(token: str = Depends(oauth2_password_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
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


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ----- Registration -----
@app.post("/register/", status_code=201)
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(default=""),
):
    """Register a new user."""
    global next_id
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username taken")
    users_db[username] = UserInDB(
        id=next_id,
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=pwd_context.hash(password),
    )
    next_id += 1
    return {"message": "User registered", "username": username}


# ----- Password Grant (RFC 6749 §4.3) -----
@app.post("/oauth/token", response_model=Token)
def oauth_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 Password Grant token endpoint.
    Compatible with Swagger UI's Authorize button.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=60),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ----- Authorization Code Grant simulation -----
@app.get("/oauth/authorize")
def authorize(
    client_id: str,
    redirect_uri: str,
    response_type: str = "code",
    state: str = "",
):
    """
    OAuth2 Authorization Code endpoint.
    In production, this would show a consent screen.
    """
    if client_id not in oauth_clients:
        raise HTTPException(status_code=400, detail="Unknown client")
    if redirect_uri not in oauth_clients[client_id]["redirect_uris"]:
        raise HTTPException(status_code=400, detail="Invalid redirect URI")

    # Generate authorization code
    code = secrets.token_urlsafe(32)
    authorization_codes[code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "created_at": datetime.now().isoformat(),
        "used": False,
    }
    return {
        "authorization_code": code,
        "state": state,
        "redirect_to": f"{redirect_uri}?code={code}&state={state}",
    }


@app.post("/oauth/token-code", response_model=Token)
def token_from_code(
    code: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
):
    """
    Exchange authorization code for access token.
    """
    if code not in authorization_codes:
        raise HTTPException(status_code=400, detail="Invalid code")

    code_data = authorization_codes[code]
    if code_data["used"]:
        raise HTTPException(status_code=400, detail="Code already used")

    # Validate client
    if client_id not in oauth_clients:
        raise HTTPException(status_code=400, detail="Unknown client")
    if oauth_clients[client_id]["client_secret"] != client_secret:
        raise HTTPException(status_code=401, detail="Invalid client secret")
    if code_data["redirect_uri"] != redirect_uri:
        raise HTTPException(status_code=400, detail="Redirect URI mismatch")

    # Mark code as used (one-time use)
    authorization_codes[code]["used"] = True

    # Issue token
    access_token = create_access_token(
        data={"sub": "authorized_user"},
        expires_delta=timedelta(minutes=60),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ----- Protected endpoints -----
@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user profile (requires valid token)."""
    return current_user


@app.get("/users/me/items/")
def read_own_items(current_user: User = Depends(get_current_active_user)):
    """Get current user's items."""
    return {"items": [{"item_id": 1, "owner": current_user.username}]}


# ----- Scopes simulation -----
SCOPES = {
    "read": "Read access to resources",
    "write": "Write access to resources",
    "admin": "Full admin access",
}


def verify_scope(required_scope: str):
    """Dependency factory for scope checking."""
    def scope_checker(current_user: User = Depends(get_current_active_user)):
        # In production, scopes would be in the JWT
        # For demo, admin users get all scopes
        if current_user.username == "admin":
            return current_user
        if required_scope == "read":
            return current_user
        raise HTTPException(status_code=403, detail=f"Scope '{required_scope}' required")
    return scope_checker


@app.get("/admin/stats/")
def admin_stats(user: User = Depends(verify_scope("admin"))):
    """Admin-only endpoint requiring 'admin' scope."""
    return {"stats": {"users": len(users_db), "total_items": 100}}


"""
Testing with curl:
    curl -X POST http://127.0.0.1:8000/register/ -d "username=alice&email=alice@test.com&password=secret123"

    curl -X POST http://127.0.0.1:8000/oauth/token -d "username=alice&password=secret123"

    curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/users/me/

    # Authorization Code flow:
    curl "http://127.0.0.1:8000/oauth/authorize?client_id=my-app&redirect_uri=http://localhost:8000/callback"
    curl -X POST "http://127.0.0.1:8000/oauth/token-code?code=<CODE>&client_id=my-app&client_secret=app-secret-123&redirect_uri=http://localhost:8000/callback"
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return
    if not JOSE_AVAILABLE:
        print("[skip] python-jose not installed (pip install python-jose[cryptography])")
        return
    try:
        pwd_context.hash("verify-password")
    except Exception:
        print("[skip] password hashing unavailable (passlib/bcrypt issue: pip install passlib[bcrypt])")
        return

    client = TestClient(app)

    r = client.post(
        "/register/",
        data={"username": "alice", "email": "alice@test.com", "password": "secret123"},
    )
    assert r.status_code == 201

    r = client.post(
        "/register/",
        data={"username": "admin", "email": "admin@test.com", "password": "admin123"},
    )
    assert r.status_code == 201

    # Password Grant flow
    r = client.post("/oauth/token", data={"username": "alice", "password": "secret123"})
    assert r.status_code == 200
    alice_token = r.json()["access_token"]

    r = client.post("/oauth/token", data={"username": "alice", "password": "wrong"})
    assert r.status_code == 401

    r = client.get("/users/me/")
    assert r.status_code == 401  # No token

    r = client.get("/users/me/", headers={"Authorization": f"Bearer {alice_token}"})
    assert r.status_code == 200
    assert r.json()["username"] == "alice"

    r = client.get(
        "/users/me/items/",
        headers={"Authorization": f"Bearer {alice_token}"},
    )
    assert r.status_code == 200
    assert len(r.json()["items"]) == 1

    # Authorization Code flow
    r = client.get(
        "/oauth/authorize",
        params={"client_id": "my-app", "redirect_uri": "http://localhost:8000/callback"},
    )
    assert r.status_code == 200
    code = r.json()["authorization_code"]

    r = client.post(
        "/oauth/token-code",
        params={
            "code": code,
            "client_id": "my-app",
            "client_secret": "app-secret-123",
            "redirect_uri": "http://localhost:8000/callback",
        },
    )
    assert r.status_code == 200
    assert "access_token" in r.json()

    r = client.get("/oauth/authorize", params={"client_id": "unknown"})
    assert r.status_code == 400

    # Scope enforcement: alice is not admin
    r = client.get("/admin/stats/", headers={"Authorization": f"Bearer {alice_token}"})
    assert r.status_code == 403

    admin_token = client.post(
        "/oauth/token", data={"username": "admin", "password": "admin123"}
    ).json()["access_token"]
    r = client.get("/admin/stats/", headers={"Authorization": f"Bearer {admin_token}"})
    assert r.status_code == 200
    assert "stats" in r.json()

    print("[OK] 14-oauth2: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
