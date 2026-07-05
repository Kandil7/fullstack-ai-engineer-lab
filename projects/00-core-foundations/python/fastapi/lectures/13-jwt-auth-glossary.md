# Glossary: JWT Authentication

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| JWT | JSON Web Token | `eyJhbGci...` |
| Header | Token metadata (algorithm, type) | `{"alg": "HS256"}` |
| Payload | Token claims/data | `{"sub": "user123"}` |
| Signature | Cryptographic verification | HMAC-SHA256 |
| Access Token | Short-lived authentication token | Expires in 15 min |
| Refresh Token | Long-lived token for renewal | Expires in 7 days |
| Bearer Token | Token passed in Authorization header | `Bearer xxx` |
| Claims | Key-value pairs in payload | `sub`, `exp`, `iat` |
| Expiration (exp) | Timestamp when token expires | Unix timestamp |
| Issued At (iat) | When token was created | Unix timestamp |
| Subject (sub) | User identifier | User ID or username |
| Secret Key | Key used to sign tokens | 256-bit minimum |
| Algorithm | Signing method | HS256, RS256 |
| Blacklist | Revoked tokens list | Redis set |
| Token Type | Distinguishes access/refresh | `type` claim |

---

## Terms - Alphabetical Order

### Access Token

**Definition:** Short-lived JWT token used to authenticate API requests, typically expires in 15-30 minutes.

**Example:**
```python
from datetime import timedelta

def create_access_token(user_id: str):
    expire = datetime.utcnow() + timedelta(minutes=15)
    payload = {
        "sub": user_id,
        "exp": expire,
        "type": "access"  # Distinguish from refresh token
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Usage
token = create_access_token("user123")
# Returns: "eyJhbGciOiJIUzI1NiIs..."
```

**Related Terms:** Refresh Token, JWT, Expiration

---

### Algorithm

**Definition:** Cryptographic method used to sign and verify JWT tokens.

**Example:**
```python
from jose import jwt

# Symmetric (same key for sign/verify)
token = jwt.encode(payload, secret, algorithm="HS256")
decoded = jwt.decode(token, secret, algorithms=["HS256"])

# Asymmetric (public/private key pair)
token = jwt.encode(payload, private_key, algorithm="RS256")
decoded = jwt.decode(token, public_key, algorithms=["RS256"])
```

| Algorithm | Type | Use Case |
|-----------|------|----------|
| HS256 | Symmetric | Simple APIs, single server |
| RS256 | Asymmetric | Microservices, third-party |
| ES256 | Asymmetric | Mobile, IoT |

**Related Terms:** HMAC, RSA, Secret Key

---

### Aud (Audience)

**Definition:** JWT claim specifying the intended recipient(s) of the token.

**Example:**
```python
def create_token(user_id: str):
    payload = {
        "sub": user_id,
        "aud": "api.example.com",  # Validate audience
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verification
decoded = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"],
    audience="api.example.com"  # Validates audience
)
```

**Related Terms:** Claims, Validation, Issuer

---

### Bearer Token

**Definition:** Authentication token passed in the HTTP Authorization header with "Bearer" prefix.

**Example:**
```python
from fastapi import Security
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/protected/")
async def protected(credentials = Security(security)):
    token = credentials.credentials
    # token is the JWT without "Bearer " prefix
    return {"token": token[:20] + "..."}

# Client sends:
# Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Related Terms:** Authorization Header, Token, OAuth2

---

### Blacklist

**Definition:** Storage of revoked tokens that should no longer be accepted, used for logout functionality.

**Example:**
```python
from typing import Set

# In-memory blacklist (use Redis in production)
blacklisted_tokens: Set[str] = set()

def blacklist_token(token: str):
    """Add token to blacklist"""
    blacklisted_tokens.add(token)

def is_blacklisted(token: str) -> bool:
    """Check if token is blacklisted"""
    return token in blacklisted_tokens

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    blacklist_token(token)
    return {"message": "Logged out"}

# Check on each request
async def get_current_user(token: str = Depends(oauth2_scheme)):
    if is_blacklisted(token):
        raise HTTPException(401, "Token revoked")
    # ... validate token
```

**Related Terms:** Token Revocation, Logout, Redis

---

### Claims

**Definition:** Key-value pairs in JWT payload containing user data and metadata.

**Example:**
```python
def create_token(user):
    payload = {
        # Registered claims (standard)
        "sub": user.id,           # Subject
        "iat": datetime.utcnow(), # Issued at
        "exp": datetime.utcnow() + timedelta(hours=1),  # Expiration
        "iss": "myapp.com",       # Issuer
        "aud": "api.myapp.com",   # Audience
        "jti": str(uuid.uuid4()), # JWT ID
        
        # Custom claims
        "email": user.email,
        "roles": user.roles,
        "permissions": ["read", "write"]
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Related Terms:** Payload, Registered Claims, Custom Claims

---

### CORS (Cross-Origin Resource Sharing)

**Definition:** Security feature that controls which domains can access your API, relevant to JWT in browser contexts.

**Example:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourapp.com"],
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["Authorization"],  # Allow JWT header
)
```

**Related Terms:** Origin, Credentials, Headers

---

### Expiration (exp)

**Definition:** JWT claim containing timestamp when token becomes invalid.

**Example:**
```python
from datetime import datetime, timedelta

def create_token(user_id: str, expires_in: int = 30):
    """Create token with expiration"""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expires_in),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Token expires in 30 minutes
token = create_token("user123")

# Token expires in 1 hour
token = create_token("user123", expires_in=60)
```

**Related Terms:** Claims, Timestamp, Token Lifetime

---

### Header (JWT)

**Definition:** First part of JWT containing metadata about the token type and signing algorithm.

**Example:**
```python
# Example JWT Header (Base64 decoded)
{
    "alg": "HS256",    # Signing algorithm
    "typ": "JWT",      # Token type
    "kid": "key-id"    # Key ID (optional)
}

# Encode/Decode
import base64
import json

header = {"alg": "HS256", "typ": "JWT"}
encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
# Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
```

**Related Terms:** Algorithm, JWT, Payload

---

### HMAC

**Definition:** Hash-based Message Authentication Code, used for symmetric JWT signing (HS256, HS384, HS512).

**Example:**
```python
import hmac
import hashlib

def hmac_sign(message: str, secret: str) -> str:
    """HMAC signature"""
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

# In JWT context (handled by jose library)
token = jwt.encode(payload, secret, algorithm="HS256")  # Uses HMAC-SHA256
```

**Related Terms:** Symmetric, Secret Key, Algorithm

---

### Iss (Issuer)

**Definition:** JWT claim identifying who issued the token.

**Example:**
```python
def create_token(user_id: str):
    payload = {
        "sub": user_id,
        "iss": "https://auth.myapp.com",  # Issuer
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verification
decoded = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"],
    issuer="https://auth.myapp.com"  # Validates issuer
)
```

**Related Terms:** Claims, Validation, Trust

---

### Issued At (iat)

**Definition:** JWT claim containing timestamp when token was created.

**Example:**
```python
def create_token(user_id: str):
    now = datetime.utcnow()
    payload = {
        "sub": user_id,
        "iat": now,  # Issued at
        "exp": now + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Decode and check
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
created_at = datetime.fromtimestamp(decoded["iat"])
print(f"Token created: {created_at}")
```

**Related Terms:** Claims, Timestamp, Expiration

---

### JSON Web Token (JWT)

**Definition:** Compact, URL-safe token format for securely transmitting information as a JSON object.

**Example:**
```python
from jose import jwt
from datetime import datetime, timedelta

# Create token
payload = {
    "sub": "user123",
    "name": "John Doe",
    "exp": datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(payload, "secret-key", algorithm="HS256")
# Returns: "eyJhbGciOiJIUzI1NiIs..."

# Decode token
decoded = jwt.decode(token, "secret-key", algorithms=["HS256"])
# Returns: {"sub": "user123", "name": "John Doe", "exp": 1234567890}
```

**Related Terms:** Header, Payload, Signature

---

### JTI (JWT ID)

**Definition:** Unique identifier for each JWT token, used for token tracking and blacklisting.

**Example:**
```python
import uuid

def create_token(user_id: str):
    payload = {
        "sub": user_id,
        "jti": str(uuid.uuid4()),  # Unique token ID
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Store JTI for blacklisting
def blacklist_token(jti: str):
    # Store in Redis with TTL matching token expiration
    redis.setex(f"blacklist:{jti}", 1800, "revoked")

def is_blacklisted(jti: str) -> bool:
    return redis.exists(f"blacklist:{jti}")
```

**Related Terms:** UUID, Blacklist, Token ID

---

### Nbf (Not Before)

**Definition:** JWT claim specifying timestamp before which token should not be accepted.

**Example:**
```python
def create_token(user_id: str):
    now = datetime.utcnow()
    payload = {
        "sub": user_id,
        "nbf": now,  # Not valid before now
        "exp": now + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Token is valid immediately
# If nbf is in the future, token won't be valid until that time
```

**Related Terms:** Claims, Expiration, Validation

---

### OAuth2

**Definition:** Authorization framework that enables JWT-based authentication with third-party providers.

**Example:**
```python
from fastapi.security import OAuth2PasswordBearer

# JWT as OAuth2 bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/protected/")
async def protected(token: str = Depends(oauth2_scheme)):
    # token contains JWT
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return {"user": payload["sub"]}
```

**Related Terms:** Bearer, Token, Authorization

---

### Payload (JWT)

**Definition:** Second part of JWT containing claims (user data and metadata).

**Example:**
```python
# JWT Payload (Base64 decoded)
{
    "sub": "user123",           # Subject (user ID)
    "name": "John Doe",        # Custom claim
    "email": "john@example.com",# Custom claim
    "roles": ["admin"],         # Custom claim
    "iat": 1516239022,         # Issued at
    "exp": 1516242622,         # Expiration
    "iss": "myapp.com",        # Issuer
    "aud": "api.myapp.com"     # Audience
}
```

**Related Terms:** Claims, Header, Signature

---

### Refresh Token

**Definition:** Long-lived token used to obtain new access tokens without re-authentication.

**Example:**
```python
def create_tokens(user_id: str):
    access_token = jwt.encode(
        {
            "sub": user_id,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    
    refresh_token = jwt.encode(
        {
            "sub": user_id,
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    
    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/token/refresh")
async def refresh(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
    
    if payload["type"] != "refresh":
        raise HTTPException(401, "Invalid token type")
    
    # Create new tokens
    return create_tokens(payload["sub"])
```

**Related Terms:** Access Token, Token Rotation

---

### Secret Key

**Definition:** Cryptographic key used to sign and verify JWT tokens.

**Example:**
```python
import secrets
import os

# Generate strong secret (minimum 256 bits)
SECRET_KEY = secrets.token_urlsafe(32)

# Or from environment variable
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Sign token
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verify token
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

**Best Practices:**
- Minimum 256 bits (32 bytes)
- Never hardcode in source
- Store in environment variables
- Rotate periodically

**Related Terms:** HMAC, RSA, Signing

---

### Sub (Subject)

**Definition:** JWT claim identifying the principal user of the token.

**Example:**
```python
def create_token(user_id: str, username: str):
    payload = {
        "sub": user_id,  # User's unique ID
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Decode and get user
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
user_id = decoded["sub"]
user = get_user_by_id(user_id)
```

**Related Terms:** Claims, User ID, Authentication

---

### Token Blacklisting

**Definition:** Mechanism to invalidate tokens before their natural expiration, used for logout.

**Example:**
```python
# Redis-based blacklist
import redis

redis_client = redis.Redis()

def blacklist_token(token: str, ttl: int):
    """Blacklist token with TTL matching expiration"""
    jti = get_jti_from_token(token)
    redis_client.setex(f"blacklist:{jti}", ttl, "revoked")

def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted"""
    jti = get_jti_from_token(token)
    return redis_client.exists(f"blacklist:{jti}")

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Get token TTL
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    ttl = payload["exp"] - datetime.utcnow().seconds
    
    blacklist_token(token, ttl)
    return {"message": "Logged out"}
```

**Related Terms:** Logout, Redis, JTI

---

### Token Rotation

**Definition:** Practice of issuing new tokens when old ones are used, enhancing security.

**Example:**
```python
def rotate_tokens(refresh_token: str):
    """Issue new access and refresh tokens"""
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
    
    if payload["type"] != "refresh":
        raise HTTPException(401, "Invalid token type")
    
    # Blacklist old refresh token
    blacklist_token(refresh_token)
    
    # Create new token pair
    return create_tokens(payload["sub"])

@app.post("/token/refresh")
async def refresh(refresh_token: str):
    return rotate_tokens(refresh_token)
```

**Related Terms:** Refresh Token, Blacklist, Security

---

### WWW-Authenticate

**Definition:** HTTP header sent by server to indicate authentication is required.

**Example:**
```python
@app.get("/protected/")
async def protected(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["ALGORITHM"])
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": 'Bearer realm="api", error="invalid_token"'
            }
        )
```

**Related Terms:** HTTP Headers, 401 Unauthorized

---

## Code Examples Collection

### Complete JWT Authentication System

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Configuration
SECRET_KEY = "your-secret-key-keep-it-safe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

# Fake database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "john@example.com",
        "hashed_password": pwd_context.hash("secret123"),
        "disabled": False,
    }
}

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        return UserInDB(**db[username])

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
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

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Routes
@app.post("/token", response_model=Token)
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

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

### Token Refresh Implementation

```python
def create_tokens(user_id: str):
    """Create access and refresh token pair"""
    access_token = jwt.encode(
        {
            "sub": user_id,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    
    refresh_token = jwt.encode(
        {
            "sub": user_id,
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
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
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")
    
    return create_tokens(payload["sub"])
```

---

## Quick Reference Card

### JWT Structure

```
header.payload.signature

Example:
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U
```

### Common Claims

```python
payload = {
    "sub": "user123",      # Subject (required)
    "exp": 1234567890,     # Expiration (required)
    "iat": 1234567890,     # Issued at
    "nbf": 1234567890,     # Not before
    "iss": "myapp.com",    # Issuer
    "aud": "api.myapp.com", # Audience
    "jti": "unique-id",    # JWT ID
    "roles": ["admin"],    # Custom
    "permissions": ["read"] # Custom
}
```

### FastAPI Integration

```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return {"user": payload["sub"]}
```

### Error Handling

```python
from jose import JWTError

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
except JWTError as e:
    raise HTTPException(401, f"Invalid token: {e}")
```
