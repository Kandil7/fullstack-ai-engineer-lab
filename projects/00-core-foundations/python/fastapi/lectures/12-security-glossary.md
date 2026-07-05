# Glossary: FastAPI Security

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Authentication | Verifying user identity | Login/password |
| Authorization | Checking permissions | Role-based access |
| HTTPS | Encrypted HTTP connection | TLS/SSL |
| JWT | JSON Web Token | Bearer token |
| OAuth2 | Authorization framework | Google login |
| API Key | Secret identifier for APIs | X-API-Key header |
| Password Hashing | One-way password encryption | bcrypt |
| CORS | Cross-Origin Resource Sharing | allow_origins |
| CSRF | Cross-Site Request Forgery | Token validation |
| XSS | Cross-Site Scripting | Input sanitization |
| SQL Injection | Database attack via queries | Parameterized queries |
| Rate Limiting | Request throttling | 100 req/min |
| Security Headers | HTTP response headers | X-Frame-Options |
| TLS | Transport Layer Security | HTTPS certificate |
| Salt | Random data added to password hash | bcrypt salt |

---

## Terms - Alphabetical Order

### API Key

**Definition:** A secret token used to authenticate API requests, typically passed in headers.

**Example:**
```python
from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/api/")
async def api_endpoint(api_key: str = Security(api_key_header)):
    if api_key != "valid-key":
        raise HTTPException(status_code=403)
    return {"data": "secret"}
```

**Related Terms:** Authentication, Headers, Token

---

### Argon2

**Definition:** Modern, secure password hashing algorithm winner of the Password Hashing Competition.

**Example:**
```python
from passlib.hash import argon2

# Hash password
hashed = argon2.hash("mypassword")

# Verify password
is_valid = argon2.verify("mypassword", hashed)
```

**Related Terms:** Password Hashing, bcrypt, Passlib

---

### Authorization

**Definition:** The process of determining what resources a user is allowed to access.

**Example:**
```python
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

def check_permission(required_role: Role):
    def permission_checker(role: Role = Depends(get_user_role)):
        if role != required_role:
            raise HTTPException(status_code=403)
        return role
    return permission_checker

@app.get("/admin/")
async def admin_only(role: Role = Depends(check_permission(Role.ADMIN))):
    return {"message": "Admin area"}
```

**Related Terms:** Authentication, Role, Permission

---

### Bcrypt

**Definition:** Adaptive password hashing function designed to be slow and resistant to brute-force attacks.

**Example:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("password123")

# Verify password
is_valid = pwd_context.verify("password123", hashed)
```

**Related Terms:** Password Hashing, Salt, Passlib

---

### Bearer Token

**Definition:** Authentication token passed in the Authorization header with "Bearer" prefix.

**Example:**
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/protected/")
async def protected(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    # Validate token
    return {"message": f"Authenticated with token: {token[:10]}..."}
```

**Related Terms:** JWT, Authorization Header, Token

---

### Content Security Policy (CSP)

**Definition:** Security header that helps prevent XSS attacks by controlling which resources can be loaded.

**Example:**
```python
class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:;"
        )
        return response
```

**Related Terms:** XSS, Security Headers, Script-src

---

### CORS (Cross-Origin Resource Sharing)

**Definition:** Mechanism that allows or restricts web applications from making requests to different domains.

**Example:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

**Related Terms:** Origin, Preflight, Access-Control

---

### CSRF (Cross-Site Request Forgery)

**Definition:** Attack that forces users to submit unwanted requests to web applications they're authenticated to.

**Example:**
```python
import secrets
from fastapi import Request, Response

csrf_tokens = {}

@app.middleware("http")
async def csrf_protection(request: Request, call_next):
    if request.method in ["POST", "PUT", "DELETE"]:
        token = request.headers.get("X-CSRF-Token")
        session_id = request.cookies.get("session_id")
        
        if not token or token != csrf_tokens.get(session_id):
            return Response(status_code=403, content="CSRF token invalid")
    
    return await call_next(request)
```

**Related Terms:** Token, Session, Forgery

---

### Defense in Depth

**Definition:** Security strategy using multiple layers of protection so that if one layer fails, others provide protection.

**Example:**
```python
# Layer 1: Input validation
@app.post("/users/")
async def create_user(user: UserInput):
    # Layer 2: Authentication
    # (handled by auth middleware)
    
    # Layer 3: Authorization
    if not current_user.is_admin:
        raise HTTPException(403)
    
    # Layer 4: SQL injection prevention
    db.execute(text("INSERT..."), {"name": user.name})
    
    # Layer 5: Output encoding
    return {"message": escape_html(user.name)}
```

**Related Terms:** Security Layers, Multi-factor

---

### Hardcoded Secrets

**Definition:** Security anti-pattern of embedding sensitive data directly in source code.

**Example:**
```python
# ❌ WRONG
API_KEY = "sk_live_abc123"
DATABASE_PASSWORD = "admin123"

# ✅ CORRECT
import os
API_KEY = os.getenv("API_KEY")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
```

**Related Terms:** Environment Variables, Secrets Management

---

### Hashing

**Definition:** One-way transformation of data that cannot be reversed, used for password storage.

**Example:**
```python
import hashlib

# Simple hash (don't use for passwords)
data = "hello"
hash_value = hashlib.sha256(data.encode()).hexdigest()

# For passwords, use specialized algorithms
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])
hashed = pwd_context.hash("mypassword")
```

**Related Terms:** Password, Bcrypt, Salt

---

### HTTPS (HTTP Secure)

**Definition:** Encrypted version of HTTP that protects data in transit using TLS/SSL.

**Example:**
```python
# Redirect HTTP to HTTPS
@app.middleware("http")
async def https_redirect(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url=url, status_code=301)
    return await call_next(request)

# Or configure at server level
# uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

**Related Terms:** TLS, SSL, Certificate

---

### JWT (JSON Web Token)

**Definition:** Compact, URL-safe token format for securely transmitting information between parties.

**Example:**
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

**Related Terms:** Token, Claims, Expiration

---

### OAuth2

**Definition:** Authorization framework that enables applications to obtain limited access to user accounts.

**Example:**
```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    return user
```

**Related Terms:** Authorization, Token, Scopes

---

### Origin

**Definition:** The combination of protocol, domain, and port that makes a web request (e.g., https://example.com:443).

**Example:**
```python
# CORS configuration with allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Development
        "https://app.example.com",  # Production
    ],
    allow_credentials=True,
)
```

**Related Terms:** CORS, Domain, Protocol

---

### Passlib

**Definition:** Python library for password hashing that supports multiple algorithms.

**Example:**
```python
from passlib.context import CryptContext

# Configure with bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt", "argon2"],
    default="bcrypt",
    deprecated="auto"
)

# Hash password
hashed = pwd_context.hash("mypassword")

# Verify password
is_valid = pwd_context.verify("mypassword", hashed)
```

**Related Terms:** Bcrypt, Argon2, Hashing

---

### Parameterized Query

**Definition:** SQL query using placeholders instead of string concatenation to prevent injection attacks.

**Example:**
```python
# ❌ WRONG - SQL Injection vulnerability
query = f"SELECT * FROM users WHERE name = '{user_input}'"
db.execute(query)

# ✅ CORRECT - Parameterized query
from sqlalchemy import text
query = text("SELECT * FROM users WHERE name = :name")
db.execute(query, {"name": user_input})
```

**Related Terms:** SQL Injection, Prepared Statement

---

### Password Hashing

**Definition:** Process of securely storing passwords using one-way hash functions with salt.

**Example:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password with random salt"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain, hashed)

# Usage
hashed = hash_password("mypassword")  # Includes random salt
is_valid = verify_password("mypassword", hashed)  # True
```

**Related Terms:** Bcrypt, Salt, Argon2

---

### Permission

**Definition:** Specific action or resource access granted to a user or role.

**Example:**
```python
from enum import Enum

class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

user_permissions = [Permission.READ, Permission.WRITE]

def require_permission(permission: Permission):
    def checker(perms: list = Depends(get_user_permissions)):
        if permission not in perms:
            raise HTTPException(403, "Insufficient permissions")
        return permission
    return checker

@app.delete("/items/{id}")
async def delete_item(
    id: int,
    _: Permission = Depends(require_permission(Permission.DELETE))
):
    return {"deleted": id}
```

**Related Terms:** Authorization, Role, Access Control

---

### Rate Limiting

**Definition:** Technique to control the number of requests a client can make within a time period.

**Example:**
```python
from collections import defaultdict
import time

rate_limit_store = defaultdict(list)

def rate_limit(request: Request, max_requests: int = 100, window: int = 60):
    client_ip = request.client.host
    current_time = time.time()
    
    # Remove old requests
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip]
        if current_time - t < window
    ]
    
    if len(rate_limit_store[client_ip]) >= max_requests:
        raise HTTPException(429, "Rate limit exceeded")
    
    rate_limit_store[client_ip].append(current_time)

@app.get("/api/")
async def api(request: Request):
    rate_limit(request)
    return {"data": "rate limited"}
```

**Related Terms:** Throttle, Quota, Sliding Window

---

### Role

**Definition:** Named set of permissions assigned to users for access control.

**Example:**
```python
from enum import Enum
from functools import wraps

class Role(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"

role_permissions = {
    Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE],
    Role.MODERATOR: [Permission.READ, Permission.WRITE],
    Role.USER: [Permission.READ],
    Role.GUEST: [],
}

def get_user_role(request: Request) -> Role:
    # Get role from token/session
    return Role.USER

def require_role(required_role: Role):
    def role_checker(role: Role = Depends(get_user_role)):
        if role != required_role:
            raise HTTPException(403, f"Requires {required_role} role")
        return role
    return role_checker

@app.get("/admin/")
async def admin_panel(role: Role = Depends(require_role(Role.ADMIN))):
    return {"message": "Admin panel"}
```

**Related Terms:** RBAC, Permission, Authorization

---

### Salt

**Definition:** Random data added to a password before hashing to prevent rainbow table attacks.

**Example:**
```python
import bcrypt

password = "mypassword".encode()

# Bcrypt automatically adds salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# Verify with salt included in hash
is_valid = bcrypt.checkpw(password, hashed)

# Different hashes for same password (different salts)
hash1 = bcrypt.hashpw(password, bcrypt.gensalt())
hash2 = bcrypt.hashpw(password, bcrypt.gensalt())
# hash1 != hash2, but both verify correctly
```

**Related Terms:** Hashing, Bcrypt, Rainbow Table

---

### Security Headers

**Definition:** HTTP response headers that help protect against common web attacks.

**Example:**
```python
class SecurityHeaders(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # HSTS
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        
        return response
```

**Related Terms:** HSTS, CSP, X-Frame-Options

---

### SQL Injection

**Definition:** Attack where malicious SQL code is inserted into queries via user input.

**Example:**
```python
# ❌ VULNERABLE to SQL injection
@app.get("/users/")
async def get_users(name: str):
    query = f"SELECT * FROM users WHERE name = '{name}'"
    # Attacker could input: ' OR '1'='1'; DROP TABLE users;--
    return db.execute(query)

# ✅ SAFE - Parameterized query
@app.get("/users/")
async def get_users(name: str):
    query = text("SELECT * FROM users WHERE name = :name")
    return db.execute(query, {"name": name})

# ✅ SAFE - ORM (SQLAlchemy)
@app.get("/users/")
async def get_users(name: str):
    return db.query(User).filter(User.name == name).all()
```

**Related Terms:** Injection, Parameterized Query, ORM

---

### TLS (Transport Layer Security)

**Definition:** Cryptographic protocol that provides secure communication over a network, successor to SSL.

**Example:**
```bash
# Generate self-signed certificate for development
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with TLS
uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

```python
# Check if request is over TLS
@app.get("/secure/")
async def secure_check(request: Request):
    is_secure = request.url.scheme == "https"
    return {"secure": is_secure}
```

**Related Terms:** HTTPS, Certificate, SSL

---

### Token

**Definition:** Temporary credential used for authentication after initial login.

**Example:**
```python
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30  # minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token/")
async def login(credentials: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
```

**Related Terms:** JWT, Bearer, Expiration

---

### XSS (Cross-Site Scripting)

**Definition:** Attack where malicious scripts are injected into web pages viewed by other users.

**Example:**
```python
from markupsafe import escape

@app.get("/profile/")
async def profile(name: str):
    # Escape user input to prevent XSS
    safe_name = escape(name)
    return {
        "html": f"<h1>Welcome, {safe_name}</h1>",
        "message": f"Hello, {safe_name}"
    }

# Content Security Policy header
class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response
```

**Related Terms:** CSP, Escape, Sanitize

---

## Code Examples Collection

### Complete Security Setup

```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

app = FastAPI()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

@app.post("/token/")
async def login(username: str, password: str):
    user = fake_user_db.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(401, "Invalid credentials")
    
    token = create_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected/")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}"}
```

### Input Validation Security

```python
from pydantic import BaseModel, EmailStr, validator
import re

class SecureUserInput(BaseModel):
    username: str
    email: EmailStr
    bio: str
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', v):
            raise ValueError('Invalid username format')
        return v
    
    @validator('bio')
    def sanitize_bio(cls, v):
        # Remove potentially dangerous HTML
        return re.sub(r'<[^>]+>', '', v)

@app.post("/users/")
async def create_user(user: SecureUserInput):
    return {"user": user}
```

---

## Quick Reference Card

### Security Checklist

```python
# 1. Password Security
pwd_context = CryptContext(schemes=["bcrypt"])
hashed = pwd_context.hash(password)

# 2. JWT Tokens
token = jwt.encode({"sub": username}, SECRET_KEY, algorithm="HS256")

# 3. CORS Configuration
app.add_middleware(CORSMiddleware, allow_origins=["..."])

# 4. Security Headers
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"

# 5. Rate Limiting
# Implement per-IP request tracking

# 6. Input Validation
@validator('field')
def validate_field(cls, v):
    if not safe_condition(v):
        raise ValueError("Invalid input")
    return v

# 7. Parameterized Queries
db.execute(text("SELECT * WHERE id = :id"), {"id": user_id})
```

### Common Vulnerabilities Prevention

| Vulnerability | Prevention |
|--------------|------------|
| SQL Injection | Parameterized queries, ORM |
| XSS | Output encoding, CSP headers |
| CSRF | CSRF tokens, SameSite cookies |
| Brute Force | Rate limiting, account lockout |
| Session Fixation | Regenerate session IDs |
| Insecure Direct Object References | Authorization checks |
