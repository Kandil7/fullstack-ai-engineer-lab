# Lecture 22: CORS Configuration in FastAPI

## Overview

Cross-Origin Resource Sharing (CORS) is a security mechanism that controls how web applications can access resources from different origins. This lecture covers CORS fundamentals, configuration in FastAPI, and security best practices for handling cross-origin requests.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what CORS is and why it exists
2. Configure CORS middleware in FastAPI
3. Set appropriate CORS policies for different scenarios
4. Handle preflight requests properly
5. Debug CORS-related issues
6. Implement secure CORS configurations
7. Understand the security implications of CORS settings

---

## Key Concepts

### 1. What is CORS?

CORS is a browser security feature that restricts web pages from making requests to a different origin than the one that served the page.

**Same-Origin Policy**: Browsers block requests from one origin to another unless explicitly allowed.

**Origins**: An origin consists of:
- Protocol (http/https)
- Domain (example.com)
- Port (80, 443, 8080)

```
https://example.com:443
├── Protocol: https
├── Domain: example.com
└── Port: 443

http://localhost:3000
├── Protocol: http
├── Domain: localhost
└── Port: 3000
```

### 2. CORS Request Types

#### Simple Requests
```python
# Simple requests meet ALL criteria:
# 1. Method is GET, HEAD, or POST
# 2. No custom headers
# 3. Content-Type is one of:
#    - application/x-www-form-urlencoded
#    - multipart/form-data
#    - text/plain

# Example: Simple GET request
fetch('https://api.example.com/data')
```

#### Preflight Requests
```python
# Preflight requests are sent when:
# 1. Method is PUT, DELETE, PATCH, etc.
# 2. Custom headers are included
# 3. Content-Type is not simple

# Browser sends OPTIONS request first
OPTIONS /api/data
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization

# Server responds with allowed methods/headers
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

---

## Code Examples

### Example 1: Basic CORS Configuration

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Basic CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

### Example 2: Production CORS Configuration

```python
# main.py - Production setup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

app = FastAPI()

# Get allowed origins from environment
ALLOWED_ORIGINS: List[str] = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000"
).split(",")

# Production CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "OPTIONS"
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With"
    ],
    expose_headers=[
        "X-Total-Count",
        "X-Page-Count"
    ],
    max_age=600  # Cache preflight for 10 minutes
)

# CORS configuration class
class CORSSettings:
    def __init__(self):
        self.origins = ALLOWED_ORIGINS
        self.allow_credentials = True
        self.allow_methods = ["GET", "POST", "PUT", "DELETE"]
        self.allow_headers = ["Authorization", "Content-Type"]
        self.max_age = 600
    
    def to_dict(self):
        return {
            "allow_origins": self.origins,
            "allow_credentials": self.allow_credentials,
            "allow_methods": self.allow_methods,
            "allow_headers": self.allow_headers,
            "max_age": self.max_age
        }

# Use settings
cors_settings = CORSSettings()
app.add_middleware(CORSMiddleware, **cors_settings.to_dict())
```

### Example 3: Dynamic CORS Based on Environment

```python
# config.py
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

settings = get_settings()

if settings.ENVIRONMENT == "production":
    # Strict CORS for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
        max_age=600
    )
else:
    # Relaxed CORS for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
```

### Example 4: CORS with Multiple Origins

```python
# main.py - Multiple origins
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import re

app = FastAPI()

# List of allowed origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://app.example.com",
    "https://admin.example.com",
    "https://*.example.com"  # Wildcard subdomains
]

# Custom origin validator
def is_origin_allowed(origin: str) -> bool:
    """Check if origin is in allowed list, supporting wildcards"""
    if origin in ALLOWED_ORIGINS:
        return True
    
    # Check wildcard patterns
    for allowed in ALLOWED_ORIGINS:
        if "*" in allowed:
            pattern = allowed.replace("*", ".*")
            if re.match(pattern, origin):
                return True
    
    return False

# CORS middleware with validation
class CustomCORSMiddleware:
    def __init__(self, app, allowed_origins: List[str]):
        self.app = app
        self.allowed_origins = allowed_origins
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            origin = dict(scope.get("headers", [])).get(b"origin", b"").decode()
            
            if origin and is_origin_allowed(origin):
                # Add CORS headers
                headers = [
                    [b"access-control-allow-origin", origin.encode()],
                    [b"access-control-allow-credentials", b"true"]
                ]
                scope["headers"].extend(headers)
        
        return await self.app(scope, receive, send)

# Use custom middleware
app.add_middleware(CustomCORSMiddleware, allowed_origins=ALLOWED_ORIGINS)

# Or use standard middleware with callback
def custom_origin_validator(origin: str) -> bool:
    return is_origin_allowed(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_callback=custom_origin_validator,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### Example 5: CORS with Authentication

```python
# main.py - CORS + Auth
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import jwt

app = FastAPI()

# CORS configuration for authenticated endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,  # Required for auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Request-ID"]
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Auth dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
        return {"id": user_id}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401)

# Protected endpoint
@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "Hello", "user": current_user}
```

### Example 6: CORS Headers Explanation

```python
# Understanding CORS headers

# Request headers (sent by browser)
"""
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
"""

# Response headers (sent by server)
"""
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Expose-Headers: X-Total-Count
Access-Control-Max-Age: 86400
"""

# FastAPI configuration mapping
app.add_middleware(
    CORSMiddleware,
    # Access-Control-Allow-Origin
    allow_origins=["http://localhost:3000"],
    
    # Access-Control-Allow-Credentials
    allow_credentials=True,
    
    # Access-Control-Allow-Methods
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    
    # Access-Control-Allow-Headers
    allow_headers=["Content-Type", "Authorization"],
    
    # Access-Control-Expose-Headers
    expose_headers=["X-Total-Count", "X-Page-Count"],
    
    # Access-Control-Max-Age (seconds)
    max_age=600
)
```

---

## Common Mistakes to Avoid

### 1. Using Wildcard with Credentials

```python
# BAD: Cannot use wildcard with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Wildcard
    allow_credentials=True,  # Bad combination!
)

# GOOD: List specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://app.example.com"],
    allow_credentials=True,
)
```

### 2. Not Handling Preflight Requests

```python
# BAD: Missing OPTIONS handling
@app.post("/api/data")
async def create_data():
    return {"status": "created"}

# GOOD: Let FastAPI handle preflight automatically
# The CORSMiddleware handles OPTIONS requests automatically
app.add_middleware(CORSMiddleware, ...)

@app.post("/api/data")
async def create_data():
    return {"status": "created"}
```

### 3. Overly Permissive Configuration

```python
# BAD: Too permissive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# GOOD: Restrictive configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=600
)
```

---

## Best Practices

1. **Never Use Wildcard with Credentials**: Specify exact origins
2. **Limit Allowed Methods**: Only allow necessary HTTP methods
3. **Limit Allowed Headers**: Only allow required headers
4. **Set Max-Age**: Cache preflight results
5. **Use Environment Variables**: Don't hardcode origins
6. **Log CORS Decisions**: For debugging and security
7. **Test CORS Configuration**: Verify in browser DevTools
8. **Document CORS Policy**: Make it clear for frontend developers

---

## Debugging CORS Issues

```python
# Debug middleware
@app.middleware("http")
async def cors_debug_middleware(request, call_next):
    origin = request.headers.get("origin")
    print(f"CORS Request from: {origin}")
    print(f"Method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    print(f"Response headers: {dict(response.headers)}")
    return response
```

```javascript
// Browser DevTools check
// 1. Open Network tab
// 2. Make request
// 3. Check request/response headers
// 4. Look for Access-Control-* headers

// Common errors:
// - No 'Access-Control-Allow-Origin' header
// - Origin 'http://localhost:3000' is not allowed
// - The value of 'Access-Control-Allow-Credentials' is not 'true'
```

---

## Practice Exercises

### Exercise 1: Basic CORS Setup
Configure CORS for a development environment with:
- Multiple frontend origins
- All methods allowed
- All headers allowed
- Credentials support

### Exercise 2: Production CORS
Create a production CORS configuration with:
- Specific allowed origins
- Limited methods and headers
- Max-age caching
- Custom exposed headers

### Exercise 3: CORS + Auth
Implement CORS with authentication:
- JWT token support
- Protected routes
- Proper credential handling

---

## Summary

- CORS is a browser security feature
- FastAPI makes CORS configuration simple
- Never use wildcard with credentials
- Limit allowed origins, methods, and headers
- Use environment variables for configuration
- Test CORS in browser DevTools
- Document your CORS policy

**Next Lecture**: We'll explore exception handling patterns in FastAPI.
