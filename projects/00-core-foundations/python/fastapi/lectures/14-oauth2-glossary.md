# Glossary: OAuth2

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| OAuth2 | Authorization framework | Delegated access |
| Authorization Code | Secure grant type for web apps | `/authorize` |
| Implicit | Legacy grant type (deprecated) | Fragment response |
| Password Grant | Direct credentials grant | Username/password |
| Client Credentials | M2M authentication | Service accounts |
| Access Token | Token for API access | Bearer token |
| Refresh Token | Long-lived renewal token | Token refresh |
| Authorization Server | Issues tokens | GitHub OAuth |
| Resource Server | Protected API | Your API |
| Resource Owner | User granting access | End user |
| Client | Application requesting access | SPA, mobile app |
| Scope | Permission level | `read`, `write` |
| Redirect URI | Callback URL | `/callback` |
| State | CSRF prevention parameter | Random string |
| PKCE | Proof Key for Code Exchange | SPA security |
| Consent Screen | User permission approval | Authorization page |

---

## Terms - Alphabetical Order

### Access Token

**Definition:** Credential issued by authorization server to access protected resources, typically short-lived.

**Example:**
```python
def create_access_token(user_id: str, scopes: list):
    payload = {
        "sub": user_id,
        "scopes": scopes,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "token_type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Client uses token
headers = {"Authorization": f"Bearer {access_token}"}
response = await client.get("https://api.example.com/data", headers=headers)
```

**Related Terms:** Refresh Token, Bearer Token, JWT

---

### Authorization Code

**Definition:** Temporary code exchanged for access token, used in Authorization Code grant flow.

**Example:**
```python
@app.get("/authorize")
async def authorize(client_id: str, redirect_uri: str, state: str):
    # Validate client
    if client_id not in registered_clients:
        raise HTTPException(400, "Invalid client")
    
    # Generate authorization code
    code = secrets.token_urlsafe(32)
    auth_codes[code] = {
        "client_id": client_id,
        "user_id": "user123",
        "redirect_uri": redirect_uri,
        "expires": datetime.utcnow() + timedelta(minutes=10)
    }
    
    # Redirect with code
    return RedirectResponse(f"{redirect_uri}?code={code}&state={state}")

@app.post("/token")
async def exchange_code(code: str, client_id: str, redirect_uri: str):
    # Validate code
    auth_code = auth_codes.get(code)
    if not auth_code or auth_code["expires"] < datetime.utcnow():
        raise HTTPException(400, "Invalid or expired code")
    
    # Issue tokens
    return create_tokens(auth_code["user_id"])
```

**Related Terms:** Authorization Code Flow, Token Exchange

---

### Authorization Code Flow

**Definition:** OAuth2 grant type where authorization code is exchanged for tokens, most secure for web apps.

**Example:**
```
1. Client redirects to /authorize
2. User authenticates and consents
3. Server redirects to redirect_uri with ?code=xxx
4. Client exchanges code for tokens at /token
5. Client uses access token for API calls
```

```python
# Step 1: Redirect to authorization
@app.get("/login")
async def login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "state": generate_state(),
        "scope": "read write"
    }
    return RedirectResponse(f"{AUTH_URL}?{urlencode(params)}")

# Step 2: Handle callback
@app.get("/callback")
async def callback(code: str, state: str):
    # Validate state
    if not validate_state(state):
        raise HTTPException(400, "Invalid state")
    
    # Exchange code for token
    token = await exchange_code(code)
    return {"access_token": token}
```

**Related Terms:** Authorization Code, Redirect URI, State

---

### Authorization Server

**Definition:** Server that authenticates users and issues tokens after obtaining consent.

**Example:**
```python
# Authorization server endpoints
@app.post("/oauth/authorize")
async def authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str = "read",
    state: str = None
):
    # Validate request
    # Show consent screen (or auto-approve for trusted apps)
    # Generate authorization code
    code = generate_auth_code(client_id, scope)
    
    # Redirect with code
    return RedirectResponse(f"{redirect_uri}?code={code}&state={state}")

@app.post("/oauth/token")
async def token(
    grant_type: str,
    code: str,
    client_id: str,
    client_secret: str
):
    # Validate client
    # Exchange code for tokens
    # Return access_token and refresh_token
```

**Related Terms:** Token Endpoint, Consent Screen, Client

---

### Bearer Token

**Definition:** OAuth2 token type passed in HTTP Authorization header to access protected resources.

**Example:**
```python
from fastapi import Security
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/data")
async def get_data(credentials = Security(security)):
    token = credentials.credentials
    # Verify token
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return {"data": "sensitive", "user": payload["sub"]}

# Client sends:
# Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Related Terms:** Authorization Header, Token, OAuth2

---

### Client

**Definition:** Application requesting access to protected resources on behalf of the resource owner.

**Example:**
```python
# Client registration
class OAuthClient(BaseModel):
    client_id: str
    client_secret: str
    name: str
    redirect_uris: List[str]
    grant_types: List[str]  # ["authorization_code", "refresh_token"]

# Store registered clients
clients_db = {
    "client-123": OAuthClient(
        client_id="client-123",
        client_secret="hashed-secret",
        name="My Web App",
        redirect_uris=["https://myapp.com/callback"],
        grant_types=["authorization_code"]
    )
}

@app.post("/oauth/register")
async def register_client(client: OAuthClientCreate):
    # Register new client
    new_client = OAuthClient(
        client_id=str(uuid.uuid4()),
        client_secret=hash_secret(secrets.token_urlsafe(32)),
        **client.dict()
    )
    clients_db[new_client.client_id] = new_client
    return {"client_id": new_client.client_id}
```

**Related Terms:** Client ID, Client Secret, Redirect URI

---

### Client Credentials

**Definition:** OAuth2 grant type for machine-to-machine authentication without user involvement.

**Example:**
```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.post("/token")
async def client_credentials(
    credentials: HTTPBasicCredentials = Depends(security)
):
    # Validate client credentials
    client = clients_db.get(credentials.username)
    if not client or not verify_secret(credentials.password, client.client_secret):
        raise HTTPException(401, "Invalid client credentials")
    
    # Issue token for machine-to-machine
    token = create_access_token(
        data={
            "sub": client.client_id,
            "grant_type": "client_credentials",
            "scopes": ["read", "write"]
        }
    )
    return {"access_token": token, "token_type": "bearer"}
```

**Related Terms:** Service Account, Machine-to-Machine

---

### Consent Screen

**Definition:** UI shown to users asking them to approve requested permissions before granting access.

**Example:**
```python
@app.get("/authorize")
async def authorize(
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str
):
    client = clients_db[client_id]
    
    # In real app, show HTML consent page
    # For API, return consent data
    return {
        "client_name": client.name,
        "requested_scopes": scope.split(),
        "message": f"{client.name} wants to access your data"
    }

@app.post("/authorize/consent")
async def authorize_consent(
    client_id: str,
    approved: bool,
    state: str
):
    if not approved:
        return RedirectResponse(f"{redirect_uri}?error=access_denied&state={state}")
    
    # Generate code
    code = secrets.token_urlsafe(32)
    # ... store code ...
    
    return RedirectResponse(f"{redirect_uri}?code={code}&state={state}")
```

**Related Terms:** Authorization, Scopes, User Consent

---

### Grant Type

**Definition:** OAuth2 flow type specifying how tokens are obtained (authorization_code, password, client_credentials, etc.).

**Example:**
```python
@app.post("/token")
async def token_endpoint(
    grant_type: str,
    # Different parameters based on grant_type
    code: Optional[str] = None,           # authorization_code
    redirect_uri: Optional[str] = None,   # authorization_code
    username: Optional[str] = None,       # password
    password: Optional[str] = None,       # password
    client_id: Optional[str] = None,      # client_credentials
    client_secret: Optional[str] = None,  # client_credentials
    refresh_token: Optional[str] = None   # refresh_token
):
    if grant_type == "authorization_code":
        return await handle_auth_code(code, redirect_uri)
    elif grant_type == "password":
        return await handle_password(username, password)
    elif grant_type == "client_credentials":
        return await handle_client_credentials(client_id, client_secret)
    elif grant_type == "refresh_token":
        return await handle_refresh_token(refresh_token)
    else:
        raise HTTPException(400, "Unsupported grant type")
```

**Related Terms:** Authorization Code, Password Grant, Client Credentials

---

### Implicit Grant

**Definition:** Legacy OAuth2 flow where tokens are returned directly in URL fragment (deprecated due to security concerns).

**Example:**
```python
# NOT RECOMMENDED - Showing for reference only
@app.get("/authorize")
async def authorize_implicit(
    client_id: str,
    redirect_uri: str,
    response_type: str = "token",  # "token" instead of "code"
    scope: str = "read",
    state: str = None
):
    if response_type != "token":
        raise HTTPException(400, "Invalid response_type")
    
    # Directly issue token in URL fragment
    token = create_access_token(user_id="user123")
    return RedirectResponse(
        f"{redirect_uri}#access_token={token}&token_type=bearer&state={state}"
    )
```

**Related Terms:** Deprecated, Security Risk, Authorization Code

---

### Offline Access

**Definition:** OAuth2 scope requesting refresh token for long-term access without user interaction.

**Example:**
```python
@app.get("/authorize")
async def authorize(scope: str):
    # Add offline_access to scope
    if "offline_access" not in scope:
        scope += " offline_access"
    
    # ... rest of authorization flow

@app.post("/token")
async def token(grant_type: str, code: str):
    auth_code = validate_code(code)
    
    # Include refresh token if offline_access was requested
    response = {
        "access_token": create_access_token(auth_code["user_id"]),
        "token_type": "bearer"
    }
    
    if "offline_access" in auth_code["scope"]:
        response["refresh_token"] = create_refresh_token(auth_code["user_id"])
    
    return response
```

**Related Terms:** Refresh Token, Scope, Long-lived Access

---

### PKCE (Proof Key for Code Exchange)

**Definition:** Security extension for OAuth2 that protects authorization code flow for public clients (SPAs, mobile apps).

**Example:**
```python
import hashlib
import base64
import secrets

def create_pkce_pair():
    """Create code verifier and challenge"""
    code_verifier = secrets.token_urlsafe(32)  # 43-128 chars
    
    # SHA256 hash of verifier
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
    
    return code_verifier, code_challenge

@app.get("/authorize")
async def authorize(client_id: str, code_challenge: str, code_challenge_method: str = "S256"):
    # Store code_challenge with session
    session["code_challenge"] = code_challenge
    session["code_challenge_method"] = code_challenge_method
    
    # Include in authorization request
    # ... redirect to auth server

@app.post("/token")
async def token(code: str, code_verifier: str):
    # Validate PKCE
    stored_challenge = session["code_challenge"]
    
    # Compute challenge from verifier
    digest = hashlib.sha256(code_verifier.encode()).digest()
    computed_challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
    
    if computed_challenge != stored_challenge:
        raise HTTPException(400, "Invalid code_verifier")
    
    # Issue tokens
    return create_tokens(user_id)
```

**Related Terms:** Code Verifier, Code Challenge, SPA Security

---

### Redirect URI

**Definition:** Endpoint where authorization server sends user after granting/denying access.

**Example:**
```python
# Client registration with redirect URIs
class OAuthClient(BaseModel):
    client_id: str
    redirect_uris: List[str]  # Registered URIs

@app.get("/authorize")
async def authorize(client_id: str, redirect_uri: str):
    client = clients_db.get(client_id)
    if not client:
        raise HTTPException(400, "Invalid client")
    
    # Validate redirect_uri matches registered URIs
    if redirect_uri not in client.redirect_uris:
        raise HTTPException(400, "Invalid redirect_uri")
    
    # Proceed with authorization
    code = generate_auth_code(client_id, redirect_uri)
    return RedirectResponse(f"{redirect_uri}?code={code}")
```

**Related Terms:** Callback URL, Client Registration, Open Redirect

---

### Refresh Token

**Definition:** Long-lived token used to obtain new access tokens without user re-authentication.

**Example:**
```python
def create_tokens(user_id: str):
    access_token = jwt.encode(
        {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "token_type": "access"
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    
    refresh_token = jwt.encode(
        {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=7),
            "token_type": "refresh"
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/token/refresh")
async def refresh(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
    
    if payload["token_type"] != "refresh":
        raise HTTPException(401, "Invalid token type")
    
    # Issue new tokens
    return create_tokens(payload["sub"])
```

**Related Terms:** Access Token, Token Rotation

---

### Resource Owner

**Definition:** User who owns the protected resources and can grant access to them.

**Example:**
```python
@app.get("/authorize")
async def authorize(client_id: str, redirect_uri: str):
    # Resource Owner is the logged-in user
    current_user = get_current_user()  # From session/cookie
    
    # Show consent screen to Resource Owner
    return {
        "user": current_user.username,
        "client": client_id,
        "message": "Do you want to grant access?"
    }

@app.post("/authorize/consent")
async def consent(approved: bool):
    if approved:
        # Resource Owner approved access
        code = generate_auth_code(current_user.id)
        return RedirectResponse(f"{redirect_uri}?code={code}")
    else:
        # Resource Owner denied access
        return RedirectResponse(f"{redirect_uri}?error=access_denied")
```

**Related Terms:** User Consent, Authorization, End User

---

### Resource Server

**Definition:** Server hosting protected resources that accepts and validates access tokens.

**Example:**
```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Resource server validates token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["ALGORITHM"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(401, "Invalid token")

@app.get("/api/resource")
async def get_resource(user_id: str = Depends(get_current_user)):
    """Protected resource on Resource Server"""
    return {"resource": "sensitive data", "user": user_id}
```

**Related Terms:** Protected Resource, Token Validation, API

---

### Scope

**Definition:** Permission level requested/granted in OAuth2, controlling what actions the client can perform.

**Example:**
```python
# Define scopes
SCOPES = {
    "read": "Read access to resources",
    "write": "Write access to resources",
    "delete": "Delete access to resources",
    "admin": "Full administrative access"
}

# Request with scopes
@app.get("/authorize")
async def authorize(scope: str = "read"):
    # scope = "read write" (space-separated)
    requested_scopes = scope.split()
    return {"requested_scopes": requested_scopes}

# Token with scopes
def create_token(user_id: str, granted_scopes: list):
    return jwt.encode(
        {
            "sub": user_id,
            "scopes": granted_scopes,
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

# Validate scopes
@app.get("/api/write")
async def write_endpoint(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["ALGORITHM"])
    if "write" not in payload.get("scopes", []):
        raise HTTPException(403, "Insufficient scope")
    return {"written": True}
```

**Related Terms:** Permissions, Access Control, Least Privilege

---

### State

**Definition:** Random parameter used to prevent CSRF attacks in OAuth2 flows.

**Example:**
```python
import secrets

# Generate state
@app.get("/authorize")
async def authorize(client_id: str, redirect_uri: str):
    state = secrets.token_urlsafe(32)
    
    # Store state in session
    request.session["oauth_state"] = state
    
    # Include in authorization URL
    auth_url = f"{AUTH_SERVER}/authorize?"
    auth_url += f"client_id={client_id}"
    auth_url += f"&redirect_uri={redirect_uri}"
    auth_url += f"&state={state}"
    auth_url += f"&response_type=code"
    
    return RedirectResponse(auth_url)

# Validate state
@app.get("/callback")
async def callback(code: str, state: str):
    stored_state = request.session.get("oauth_state")
    
    if state != stored_state:
        raise HTTPException(400, "Invalid state parameter - possible CSRF attack")
    
    # State valid, proceed
    del request.session["oauth_state"]
    return exchange_code(code)
```

**Related Terms:** CSRF Protection, Random Value, Session

---

### Token Endpoint

**Definition:** OAuth2 endpoint where clients exchange credentials for access tokens.

**Example:**
```python
@app.post("/oauth/token")
async def token_endpoint(
    grant_type: str,
    code: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    client_id: str = None,
    client_secret: str = None,
    refresh_token: Optional[str] = None,
    scope: Optional[str] = None
):
    """OAuth2 Token Endpoint"""
    
    if grant_type == "authorization_code":
        # Validate authorization code
        auth_code = validate_code(code, client_id, redirect_uri)
        user_id = auth_code["user_id"]
        
    elif grant_type == "client_credentials":
        # Validate client credentials
        if not validate_client(client_id, client_secret):
            raise HTTPException(401, "Invalid client")
        user_id = client_id
        
    elif grant_type == "refresh_token":
        # Validate refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["token_type"] != "refresh":
            raise HTTPException(401, "Invalid token type")
        user_id = payload["sub"]
        
    else:
        raise HTTPException(400, "Unsupported grant_type")
    
    # Issue tokens
    tokens = create_tokens(user_id, scope)
    return tokens
```

**Related Terms:** Token Exchange, Grant Types, Authorization Server

---

### Token Revocation

**Definition:** Mechanism to invalidate tokens before their natural expiration.

**Example:**
```python
# Token blacklist (use Redis in production)
revoked_tokens = set()

@app.post("/oauth/revoke")
async def revoke_token(token: str):
    """Revoke an access or refresh token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        
        if jti:
            revoked_tokens.add(jti)
            return {"message": "Token revoked"}
    except JWTError:
        pass
    
    return {"message": "Token revoked"}  # Always return success per RFC

async def validate_token(token: str):
    """Check if token is revoked"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    if payload.get("jti") in revoked_tokens:
        raise HTTPException(401, "Token revoked")
    
    return payload
```

**Related Terms:** Token Revocation, Blacklist, Logout

---

## Code Examples Collection

### Complete OAuth2 Server

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import secrets

app = FastAPI()

# Models
class Client(BaseModel):
    client_id: str
    client_secret: str
    redirect_uris: List[str]
    name: str

class User(BaseModel):
    id: str
    username: str

# Storage
clients = {}
auth_codes = {}
tokens = {}

# OAuth2 Endpoints
@app.post("/oauth/register")
async def register_client(client: Client):
    clients[client.client_id] = client
    return {"client_id": client.client_id}

@app.get("/oauth/authorize")
async def authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str = "read",
    state: Optional[str] = None
):
    if client_id not in clients:
        raise HTTPException(400, "Invalid client_id")
    
    if redirect_uri not in clients[client_id].redirect_uris:
        raise HTTPException(400, "Invalid redirect_uri")
    
    # Generate code
    code = secrets.token_urlsafe(32)
    auth_codes[code] = {
        "client_id": client_id,
        "user_id": "user123",
        "scope": scope,
        "expires": datetime.utcnow() + timedelta(minutes=10)
    }
    
    redirect_url = f"{redirect_uri}?code={code}"
    if state:
        redirect_url += f"&state={state}"
    
    return RedirectResponse(url=redirect_url)

@app.post("/oauth/token")
async def token(
    grant_type: str,
    code: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    refresh_token: Optional[str] = None
):
    if grant_type == "authorization_code":
        if code not in auth_codes:
            raise HTTPException(400, "Invalid code")
        
        auth_code = auth_codes.pop(code)
        if auth_code["expires"] < datetime.utcnow():
            raise HTTPException(400, "Code expired")
        
        user_id = auth_code["user_id"]
        
    elif grant_type == "refresh_token":
        # Validate refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["sub"]
        
    else:
        raise HTTPException(400, "Unsupported grant_type")
    
    # Create tokens
    access_token = jwt.encode(
        {"sub": user_id, "exp": datetime.utcnow() + timedelta(minutes=15)},
        SECRET_KEY,
        algorithm="HS256"
    )
    
    refresh = jwt.encode(
        {"sub": user_id, "exp": datetime.utcnow() + timedelta(days=7)},
        SECRET_KEY,
        algorithm="HS256"
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": 900
    }
```

---

## Quick Reference Card

### OAuth2 Grant Types

| Grant Type | Use Case | Flow |
|------------|----------|------|
| authorization_code | Web apps, SPAs | Redirect-based |
| password | First-party apps | Direct credentials |
| client_credentials | M2M | Service accounts |
| implicit | Legacy SPAs | Deprecated |

### OAuth2 Endpoints

```python
# Authorization
GET /oauth/authorize

# Token
POST /oauth/token

# Revocation
POST /oauth/revoke

# User Info
GET /oauth/userinfo
```

### Required Parameters

```python
# Authorization Request
response_type=code
client_id=xxx
redirect_uri=xxx
scope=read write
state=random_string

# Token Exchange
grant_type=authorization_code
code=xxx
redirect_uri=xxx
client_id=xxx
client_secret=xxx
```

### Security Checklist

- [ ] Use HTTPS only
- [ ] Validate redirect URIs
- [ ] Implement state parameter
- [ ] Use PKCE for SPAs
- [ ] Short-lived access tokens
- [ ] Implement token refresh
- [ ] Validate all inputs
- [ ] Log authorization events
