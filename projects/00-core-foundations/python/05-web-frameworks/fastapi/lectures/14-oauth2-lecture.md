# Lecture 14: OAuth2 in FastAPI

## Topic Overview

OAuth2 is an authorization framework that enables third-party applications to obtain limited access to user accounts on HTTP services. FastAPI provides excellent built-in support for OAuth2 flows, making it easy to implement both password-based and third-party OAuth2 authentication.

**Why OAuth2 Matters:**
- **Third-party integration** - Allow apps to access user data from Google, GitHub, etc.
- **Delegated authorization** - Users grant limited access without sharing passwords
- **Standard protocol** - Industry-standard with broad support
- **Granular permissions** - Scope-based access control
- **Secure** - Tokens replace passwords for API access

**OAuth2 Grant Types:**
```
1. Authorization Code - Most secure, for web apps
2. Implicit - Legacy, not recommended
3. Resource Owner Password - Direct username/password
4. Client Credentials - Machine-to-machine
```

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand OAuth2 flows** - Different grant types and when to use them
2. **Implement password flow** - Direct authentication for first-party apps
3. **Implement authorization code flow** - Secure flow for third-party apps
4. **Use FastAPI OAuth2 utilities** - Leverage built-in security classes
5. **Create OAuth2 with JWT** - Combine OAuth2 with JWT tokens
6. **Handle token refresh** - Implement token refresh patterns
7. **Implement scopes** - Control access levels
8. **Integrate third-party providers** - Connect with Google, GitHub, etc.

---

## Key Concepts

### 1. OAuth2 Roles

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Resource   │     │    Client    │     │ Authorization│
│    Owner     │     │   (App)     │     │   Server     │
│   (User)    │     │             │     │   (AuthZ)    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │  1. User grants   │                   │
       │     permission    │                   │
       │──────────────────▶│                   │
       │                   │ 2. Request        │
       │                   │    authorization  │
       │                   │──────────────────▶│
       │                   │                   │
       │  3. User authenticates               │
       │◀──────────────────│──────────────────▶│
       │                   │                   │
       │  4. User grants   │                   │
       │     consent       │                   │
       │──────────────────▶│ 5. Auth code      │
       │                   │◀──────────────────│
       │                   │                   │
       │                   │ 6. Exchange code  │
       │                   │    for token      │
       │                   │──────────────────▶│
       │                   │                   │
       │                   │ 7. Access token   │
       │                   │◀──────────────────│
       │                   │                   │
       │ 8. Access resource│                   │
       │◀──────────────────│                   │
```

### 2. OAuth2 Grant Types

| Grant Type | Use Case | Security |
|------------|----------|----------|
| Authorization Code | Web apps, SPAs | High |
| Implicit | Legacy SPAs | Low (deprecated) |
| Password | First-party apps | Medium |
| Client Credentials | M2M communication | High |

### 3. OAuth2 vs JWT

```
OAuth2                         JWT
─────────                      ─────
Authorization framework        Token format
Defines flows/grants           Defines token structure
Can use JWT for tokens         Can be used by OAuth2
Focus: "Who can access what"   Focus: "Who is this user"
```

---

## Code Examples

### Example 1: OAuth2 Password Flow

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

app = FastAPI()

# Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

# Fake user database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "john@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not fakehashedsecret(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### Example 2: OAuth2 with Scopes

```python
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Define scopes
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "read": "Read access to resources",
        "write": "Write access to resources",
        "admin": "Admin access"
    }
)

class User(BaseModel):
    username: str
    scopes: List[str] = []

async def get_current_user(
    security_scopes: SecurityScopes = Depends(),
    token: str = Depends(oauth2_scheme)
):
    # Decode token and get user
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user_scopes = payload.get("scopes", [])
    
    # Check required scopes
    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: requires scope '{scope}'"
            )
    
    return User(username=username, scopes=user_scopes)

@app.get("/read-only/")
async def read_only(user: User = Security(get_current_user, scopes=["read"])):
    return {"message": "Read access granted"}

@app.get("/write-only/")
async def write_only(user: User = Security(get_current_user, scopes=["write"])):
    return {"message": "Write access granted"}

@app.get("/admin-only/")
async def admin_only(user: User = Security(get_current_user, scopes=["admin"])):
    return {"message": "Admin access granted"}

@app.post("/token")
async def login(username: str, password: str):
    # Validate credentials
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token with scopes
    access_token = create_access_token(
        data={
            "sub": username,
            "scopes": ["read", "write"]  # User's scopes
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### Example 3: OAuth2 Authorization Code Flow

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
import secrets
from urllib.parse import urlencode

app = FastAPI()

# GitHub OAuth2 configuration
GITHUB_CLIENT_ID = "your-client-id"
GITHUB_CLIENT_SECRET = "your-client-secret"
GITHUB_REDIRECT_URI = "http://localhost:8000/callback"

# Store state for CSRF protection
oauth_states = {}

@app.get("/login/github")
async def login_github():
    """Redirect to GitHub authorization page"""
    state = secrets.token_urlsafe(32)
    oauth_states[state] = True  # Store state
    
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "state": state,
        "scope": "user:email"
    }
    
    github_auth_url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url=github_auth_url)

@app.get("/callback")
async def github_callback(code: str, state: str):
    """Handle GitHub OAuth callback"""
    # Validate state (CSRF protection)
    if state not in oauth_states:
        raise HTTPException(400, "Invalid state parameter")
    del oauth_states[state]
    
    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI
            },
            headers={"Accept": "application/json"}
        )
        
        if token_response.status_code != 200:
            raise HTTPException(400, "Failed to get access token")
        
        token_data = token_response.json()
        access_token = token_data["access_token"]
    
    # Get user info
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
        )
        
        user_data = user_response.json()
    
    # Create JWT for your application
    app_token = create_access_token(
        data={
            "sub": str(user_data["id"]),
            "username": user_data["login"],
            "github_token": access_token
        }
    )
    
    return {"access_token": app_token, "token_type": "bearer"}

@app.get("/users/me")
async def get_current_user(request: Request):
    # Get token from request
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    
    token = auth_header.split(" ")[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Get user from GitHub using stored token
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {payload['github_token']}",
                "Accept": "application/json"
            }
        )
        return user_response.json()
```

### Example 4: OAuth2 Client Credentials Flow

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta
import secrets

app = FastAPI()

security = HTTPBasic()

# Service accounts
SERVICE_ACCOUNTS = {
    "service-a": {
        "secret": "hashed-secret-a",
        "scopes": ["read", "write"]
    },
    "service-b": {
        "secret": "hashed-secret-b",
        "scopes": ["read"]
    }
}

def verify_client_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify client credentials for machine-to-machine auth"""
    client_id = credentials.username
    client_secret = credentials.password
    
    if client_id not in SERVICE_ACCOUNTS:
        raise HTTPException(status_code=401, detail="Invalid client")
    
    stored_secret = SERVICE_ACCOUNTS[client_id]["secret"]
    if not secrets.compare_digest(client_secret, stored_secret):
        raise HTTPException(status_code=401, detail="Invalid secret")
    
    return {
        "client_id": client_id,
        "scopes": SERVICE_ACCOUNTS[client_id]["scopes"]
    }

@app.post("/token")
async def get_client_token(client = Depends(verify_client_credentials)):
    """Issue token for client credentials grant"""
    access_token = create_access_token(
        data={
            "sub": client["client_id"],
            "grant_type": "client_credentials",
            "scopes": client["scopes"]
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/data")
async def get_data(token: str = Depends(oauth2_scheme)):
    """Protected endpoint requiring client credentials"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    if payload.get("grant_type") != "client_credentials":
        raise HTTPException(403, "Invalid grant type")
    
    return {"data": "sensitive data"}
```

### Example 5: Complete OAuth2 Server

```python
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import secrets

app = FastAPI()

# Configuration
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class Client(BaseModel):
    client_id: str
    client_secret: str
    redirect_uris: List[str]
    scopes: List[str]

class User(BaseModel):
    id: str
    username: str
    email: str

class AuthorizationCode(BaseModel):
    code: str
    client_id: str
    redirect_uri: str
    scope: str
    user_id: str
    expires_at: datetime

# Storage (use database in production)
clients_db = {}
auth_codes_db = {}
users_db = {}

# OAuth2 endpoints
@app.post("/oauth/authorize")
async def authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str = "read",
    state: Optional[str] = None
):
    """Authorization endpoint"""
    # Validate client
    client = clients_db.get(client_id)
    if not client:
        raise HTTPException(400, "Invalid client_id")
    
    if redirect_uri not in client.redirect_uris:
        raise HTTPException(400, "Invalid redirect_uri")
    
    # In real app, show consent screen and authenticate user
    # For demo, assume user is authenticated
    user_id = "user123"
    
    # Generate authorization code
    code = secrets.token_urlsafe(32)
    auth_codes_db[code] = AuthorizationCode(
        code=code,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        user_id=user_id,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    
    # Redirect with code
    redirect_url = f"{redirect_uri}?code={code}"
    if state:
        redirect_url += f"&state={state}"
    
    return RedirectResponse(url=redirect_url)

@app.post("/oauth/token")
async def token(
    grant_type: str,
    code: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    refresh_token: Optional[str] = None
):
    """Token endpoint"""
    if grant_type == "authorization_code":
        # Exchange code for tokens
        auth_code = auth_codes_db.get(code)
        if not auth_code:
            raise HTTPException(400, "Invalid code")
        
        if auth_code.expires_at < datetime.utcnow():
            raise HTTPException(400, "Code expired")
        
        if auth_code.redirect_uri != redirect_uri:
            raise HTTPException(400, "Invalid redirect_uri")
        
        # Create tokens
        access_token = create_access_token(
            data={"sub": auth_code.user_id, "scope": auth_code.scope}
        )
        
        # Delete used code
        del auth_codes_db[code]
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,
            "scope": auth_code.scope
        }
    
    elif grant_type == "refresh_token":
        # Refresh token logic
        pass
    
    else:
        raise HTTPException(400, "Unsupported grant_type")

@app.get("/api/userinfo")
async def userinfo(token: str = Depends(oauth2_scheme)):
    """Protected resource endpoint"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = users_db.get(user_id)
        if not user:
            raise HTTPException(401, "User not found")
        return user
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Validating Redirect URI

```python
# ❌ WRONG - Open redirect vulnerability
@app.get("/authorize")
async def authorize(redirect_uri: str):
    # Attacker could set redirect_uri to malicious site
    return RedirectResponse(f"{redirect_uri}?code=abc")

# ✅ CORRECT - Validate against whitelist
ALLOWED_REDIRECTS = ["https://yourapp.com/callback"]

@app.get("/authorize")
async def authorize(redirect_uri: str):
    if redirect_uri not in ALLOWED_REDIRECTS:
        raise HTTPException(400, "Invalid redirect URI")
    return RedirectResponse(f"{redirect_uri}?code=abc")
```

### Mistake 2: Not Using State Parameter

```python
# ❌ WRONG - Vulnerable to CSRF
@app.get("/authorize")
async def authorize(client_id: str, redirect_uri: str):
    return RedirectResponse(f"{redirect_uri}?code=abc")

# ✅ CORRECT - Generate and validate state
@app.get("/authorize")
async def authorize(client_id: str, redirect_uri: str):
    state = secrets.token_urlsafe(32)
    oauth_states[state] = True
    return RedirectResponse(f"{redirect_uri}?code=abc&state={state}")
```

### Mistake 3: Exposing Client Secret

```python
# ❌ WRONG - Hardcoded secrets
CLIENT_SECRET = "my-secret-key"

# ✅ CORRECT - Use environment variables
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
```

---

## Best Practices

1. **Use HTTPS always** - OAuth2 requires encrypted connections
2. **Validate redirect URIs** - Prevent open redirect attacks
3. **Use state parameter** - Prevent CSRF attacks
4. **Short-lived codes** - Authorization codes should expire quickly
5. **Secure token storage** - Don't expose tokens in URLs or logs
6. **Implement token refresh** - Seamless user experience
7. **Use scopes** - Implement least-privilege access
8. **Validate all inputs** - Prevent injection attacks

---

## Practice Exercises

### Exercise 1: GitHub OAuth Integration
Implement GitHub OAuth2 login:
- Redirect to GitHub
- Handle callback
- Get user info
- Create application JWT

### Exercise 2: OAuth2 with Scopes
Build an OAuth2 system with:
- Multiple scopes (read, write, admin)
- Scope validation
- Permission-based endpoints

### Exercise 3: OAuth2 Server
Create a complete OAuth2 authorization server:
- Authorization endpoint
- Token endpoint
- Refresh tokens
- Client registration

### Exercise 4: OAuth2 Proxy
Build an OAuth2 proxy that:
- Handles multiple providers
- Unified token format
- Provider abstraction

### Exercise 5: OAuth2 with PKCE
Implement OAuth2 with PKCE for SPAs:
- Code verifier/challenge generation
- PKCE validation
- Secure SPA authentication

---

## Summary

- **OAuth2** is the standard for delegated authorization
- **Password flow** is for first-party apps
- **Authorization code flow** is for third-party apps
- **Client credentials** is for machine-to-machine
- **Always validate** redirect URIs and state
- **Use scopes** for granular permissions
- **Implement refresh tokens** for better UX
- **Secure everything** with HTTPS

---

## Further Reading

- [FastAPI OAuth2 Documentation](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [OAuth 2.0 Simplified](https://aaronparecki.com/oauth-2-simplified/)
