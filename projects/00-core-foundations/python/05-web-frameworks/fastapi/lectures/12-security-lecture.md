# Lecture 12: FastAPI Security

## Topic Overview

Security in FastAPI encompasses the practices and mechanisms used to protect your API from unauthorized access, data breaches, and common web vulnerabilities. FastAPI provides excellent built-in security features while also supporting industry-standard protocols like OAuth2 and JWT.

**Why Security Matters:**
- **Protect user data** - Prevent unauthorized access to sensitive information
- **Maintain trust** - Users expect their data to be secure
- **Compliance** - Meet regulatory requirements (GDPR, HIPAA, SOC2)
- **Prevent attacks** - Defend against common vulnerabilities
- **Business continuity** - Security breaches can destroy businesses

**Common Security Concerns:**
- Authentication (who are you?)
- Authorization (what can you do?)
- Data encryption (protecting data in transit and at rest)
- Input validation (preventing injection attacks)
- Rate limiting (preventing abuse)

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand security fundamentals** - Core concepts of API security
2. **Implement authentication** - Verify user identity
3. **Apply authorization** - Control access to resources
4. **Use HTTPS** - Encrypt data in transit
5. **Handle secrets safely** - Manage API keys and passwords
6. **Validate input** - Prevent injection attacks
7. **Implement rate limiting** - Prevent abuse
8. **Apply security headers** - Protect against common attacks

---

## Key Concepts

### 1. Authentication vs Authorization

```
Authentication (AuthN)          Authorization (AuthZ)
─────────────────────          ────────────────────
"Who are you?"                 "What can you do?"
Verify identity                Check permissions
Login/password                 Role-based access
Tokens, certificates          Access control lists
```

### 2. Defense in Depth

Multiple layers of security:
```
┌─────────────────────────────────────┐
│  Layer 1: Network Security          │
│  (Firewall, DDoS protection)        │
├─────────────────────────────────────┤
│  Layer 2: Transport Security        │
│  (HTTPS/TLS)                        │
├─────────────────────────────────────┤
│  Layer 3: Application Security      │
│  (Input validation, CORS)           │
├─────────────────────────────────────┤
│  Layer 4: Authentication            │
│  (Verify identity)                  │
├─────────────────────────────────────┤
│  Layer 5: Authorization             │
│  (Check permissions)                │
├─────────────────────────────────────┤
│  Layer 6: Data Security             │
│  (Encryption at rest)               │
└─────────────────────────────────────┘
```

### 3. OWASP Top 10

Common web application security risks:
1. Broken Access Control
2. Cryptographic Failures
3. Injection (SQL, NoSQL, Command)
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging Failures
10. Server-Side Request Forgery (SSRF)

---

## Code Examples

### Example 1: Password Hashing

```python
from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime

app = FastAPI()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    created_at: datetime

# In-memory storage (use database in production)
users_db = {}

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/register/", response_model=User)
async def register(user: UserCreate):
    # Check if user exists
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash password before storing
    hashed_password = hash_password(user.password)
    
    # Store user (never store plain text passwords!)
    user_db = User(
        id=len(users_db) + 1,
        username=user.username,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    users_db[user.username] = user_db
    
    return user_db

@app.post("/login/")
async def login(username: str, password: str):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}
```

### Example 2: API Key Authentication

```python
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
import os

app = FastAPI()

# API Key security scheme
API_KEY = os.getenv("API_KEY", "secret-api-key-123")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key from header"""
    if api_key is None:
        raise HTTPException(
            status_code=403,
            detail="API key required"
        )
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

@app.get("/api/data/")
async def get_data(api_key: str = Security(verify_api_key)):
    return {"data": "secret information", "authenticated": True}

# Multiple API keys for different services
SERVICE_KEYS = {
    "service-a": "key-a-123",
    "service-b": "key-b-456",
}

async def verify_service_key(api_key: str = Security(api_key_header)):
    """Verify service-specific API key"""
    if api_key not in SERVICE_KEYS.values():
        raise HTTPException(status_code=403, detail="Invalid service key")
    return api_key
```

### Example 3: Basic Security Headers Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        return response

app.add_middleware(SecurityHeadersMiddleware)

@app.get("/")
async def root():
    return {"message": "Secure API"}
```

### Example 4: Rate Limiting

```python
from fastapi import FastAPI, Request, HTTPException
from collections import defaultdict
import time

app = FastAPI()

# In-memory rate limiter (use Redis in production)
rate_limit_store = defaultdict(list)

RATE_LIMIT = 100  # requests
RATE_WINDOW = 60  # seconds

def rate_limit(request: Request):
    """Simple rate limiting decorator"""
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old requests
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip]
        if current_time - t < RATE_WINDOW
    ]
    
    # Check rate limit
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
    
    # Add current request
    rate_limit_store[client_ip].append(current_time)
    return True

@app.get("/api/data/")
async def get_data(request: Request):
    rate_limit(request)
    return {"data": "rate limited endpoint"}
```

### Example 5: Input Validation

```python
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, EmailStr, validator
import re

app = FastAPI()

class UserInput(BaseModel):
    username: str
    email: EmailStr
    age: int
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', v):
            raise ValueError(
                'Username must be 3-20 characters, alphanumeric and underscore only'
            )
        return v
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v

@app.post("/users/")
async def create_user(user: UserInput):
    # Input is validated automatically
    return {"user": user}

@app.get("/search/")
async def search(
    q: str = Query(..., min_length=1, max_length=100),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    # Query parameters validated
    return {"query": q, "page": page, "limit": limit}
```

### Example 6: CORS Configuration

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Strict CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://yourdomain.com",  # Production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Request-ID"],
    max_age=600,  # Cache preflight for 10 minutes
)

@app.get("/api/data/")
async def get_data():
    return {"data": "CORS protected"}
```

### Example 7: HTTPS Redirection

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

app = FastAPI()

class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Redirect HTTP to HTTPS
        if request.url.scheme == "http":
            https_url = request.url.replace(scheme="https")
            return RedirectResponse(url=https_url, status_code=301)
        
        return await call_next(request)

# Uncomment in production
# app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def root():
    return {"message": "HTTPS only"}
```

### Example 8: SQL Injection Prevention

```python
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./secure.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@app.get("/users/")
async def search_users(name: str = Query(...)):
    db = SessionLocal()
    try:
        # ✅ CORRECT - Parameterized query
        result = db.execute(
            text("SELECT * FROM users WHERE name = :name"),
            {"name": name}
        )
        users = result.fetchall()
        return {"users": [dict(u) for u in users]}
    finally:
        db.close()

# ❌ WRONG - SQL Injection vulnerability
# @app.get("/users/bad/")
# async def search_users_bad(name: str):
#     query = f"SELECT * FROM users WHERE name = '{name}'"
#     # Attacker could input: ' OR '1'='1
#     result = db.execute(text(query))
```

---

## Common Mistakes to Avoid

### Mistake 1: Storing Passwords in Plain Text

```python
# ❌ WRONG - Never store plain text passwords!
def save_user(user: UserCreate):
    db.save({"password": user.password})

# ✅ CORRECT - Always hash passwords
def save_user(user: UserCreate):
    hashed = hash_password(user.password)
    db.save({"password": hashed})
```

### Mistake 2: Exposing Sensitive Data

```python
# ❌ WRONG - Leaking sensitive info in error messages
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found in database users table"  # ❌
        )
    return user

# ✅ CORRECT - Generic error messages
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Mistake 3: Hardcoded Secrets

```python
# ❌ WRONG - Never hardcode secrets!
API_KEY = "sk_live_abc123xyz"
DATABASE_PASSWORD = "admin123"

# ✅ CORRECT - Use environment variables
import os
API_KEY = os.getenv("API_KEY")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
```

---

## Best Practices

1. **Always use HTTPS** - Encrypt all data in transit
2. **Hash passwords** - Use bcrypt or Argon2
3. **Validate all input** - Never trust user data
4. **Use parameterized queries** - Prevent SQL injection
5. **Implement rate limiting** - Prevent abuse
6. **Add security headers** - Protect against common attacks
7. **Use environment variables** - Never hardcode secrets
8. **Implement CORS properly** - Restrict cross-origin requests
9. **Log security events** - Monitor for suspicious activity
10. **Regular security audits** - Test for vulnerabilities

---

## Practice Exercises

### Exercise 1: Implement JWT Authentication
Create a complete JWT authentication system with:
- User registration with hashed passwords
- Login endpoint that returns JWT token
- Protected endpoint that requires valid token
- Token refresh functionality

### Exercise 2: Role-Based Access Control
Implement RBAC with:
- Admin, User, and Guest roles
- Middleware that checks permissions
- Protected routes based on roles

### Exercise 3: Rate Limiting System
Build a rate limiter that:
- Limits by IP address
- Allows different limits per endpoint
- Returns proper retry-after headers

### Exercise 4: Security Headers
Create middleware that adds:
- CSP (Content Security Policy)
- HSTS (HTTP Strict Transport Security)
- X-Frame-Options
- Custom security headers

### Exercise 5: Input Validation
Build a validation system that:
- Validates email format
- Sanitizes user input
- Prevents XSS attacks
- Handles unicode safely

---

## Summary

- **Security is multi-layered** - Defense in depth approach
- **Authentication verifies identity** - Who are you?
- **Authorization controls access** - What can you do?
- **Always hash passwords** - Use bcrypt/Argon2
- **Validate all input** - Don't trust user data
- **Use HTTPS everywhere** - Encrypt data in transit
- **Implement rate limiting** - Prevent abuse
- **Add security headers** - Protect against common attacks
- **Keep secrets safe** - Use environment variables
- **Monitor and log** - Track security events

---

## Further Reading

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
