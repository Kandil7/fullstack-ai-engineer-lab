# Glossary: CORS Concepts in FastAPI

## Quick Reference Table

| Term | Definition | Related Terms |
|------|------------|---------------|
| Access-Control-Allow-Origin | Header specifying allowed origins | CORS, Origin |
| Access-Control-Allow-Methods | Header specifying allowed HTTP methods | CORS, Preflight |
| Access-Control-Allow-Headers | Header specifying allowed request headers | CORS, Preflight |
| Access-Control-Allow-Credentials | Header indicating if credentials are allowed | CORS, Auth |
| Access-Control-Max-Age | Header caching preflight results | CORS, Preflight |
| Access-Control-Expose-Headers | Header exposing response headers to browser | CORS |
| CORS | Cross-Origin Resource Sharing | Origin, Security |
| CORS Middleware | FastAPI middleware handling CORS | Middleware, FastAPI |
| Origin | Protocol + domain + port combination | URL, CORS |
| Preflight | OPTIONS request sent before actual request | CORS, OPTIONS |
| Simple Request | Request that doesn't require preflight | CORS, Preflight |
| Credentials | Authentication data (cookies, headers) | Auth, CORS |
| Same-Origin Policy | Browser security restricting cross-origin requests | CORS, Security |
| Wildcard | * character matching any value | CORS, Origin |
| Callback | Function to dynamically validate origins | CORS, Dynamic |

---

## Detailed Definitions

### Access-Control-Allow-Origin

**Definition**: Response header that indicates which origins can access the resource.

**Code Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Single origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"]
)
# Response header: Access-Control-Allow-Origin: http://localhost:3000

# Multiple origins (dynamic)
def dynamic_origin(request):
    allowed = ["http://localhost:3000", "https://app.example.com"]
    origin = request.headers.get("origin")
    return origin if origin in allowed else None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_origin_callback=dynamic_origin
)

# Wildcard (no credentials)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)
# Response header: Access-Control-Allow-Origin: *
```

**Related Terms**: CORS, Origin, Preflight

---

### Access-Control-Allow-Methods

**Definition**: Response header indicating which HTTP methods are allowed for cross-origin requests.

**Code Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow specific methods
app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST", "PUT", "DELETE"]
)
# Response header: Access-Control-Allow-Methods: GET, POST, PUT, DELETE

# Allow all methods (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"]
)

# Preflight response
"""
HTTP/1.1 204 No Content
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Max-Age: 86400
"""
```

**Related Terms**: CORS, Preflight, HTTP Methods

---

### Access-Control-Allow-Headers

**Definition**: Response header indicating which request headers are allowed in cross-origin requests.

**Code Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow specific headers
app.add_middleware(
    CORSMiddleware,
    allow_headers=["Authorization", "Content-Type", "Accept"]
)
# Response header: Access-Control-Allow-Headers: Authorization, Content-Type, Accept

# Common headers to allow
COMMON_HEADERS = [
    "Authorization",
    "Content-Type",
    "Accept",
    "Origin",
    "X-Requested-With",
    "X-CSRF-Token"
]

app.add_middleware(
    CORSMiddleware,
    allow_headers=COMMON_HEADERS
)

# Allow all headers (not recommended)
app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"]
)
```

**Related Terms**: CORS, Preflight, Headers

---

### Access-Control-Allow-Credentials

**Definition**: Response header indicating whether the request can include credentials (cookies, auth headers).

**Code Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True  # Required for cookies/auth
)
# Response header: Access-Control-Allow-Credentials: true

# Frontend request with credentials
"""
fetch('https://api.example.com/data', {
    credentials: 'include',  // Include cookies
    headers: {
        'Authorization': 'Bearer token123'
    }
})
"""

# BAD: Cannot use wildcard with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Error!
    allow_credentials=True
)

# GOOD: Specify exact origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True
)
```

**Related Terms**: CORS, Auth, Cookies

---

### Access-Control-Max-Age

**Definition**: Response header indicating how long preflight results can be cached (in seconds).

**Code Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cache preflight for 10 minutes
app.add_middleware(
    CORSMiddleware,
    max_age=600
)
# Response header: Access-Control-Max-Age: 600

# Cache for 24 hours
app.add_middleware(
    CORSMiddleware,
    max_age=86400
)

# Cache for 1 hour
app.add_middleware(
    CORSMiddleware,
    max_age=3600
)

# No caching (not recommended)
app.add_middleware(
    CORSMiddleware,
    max_age=0
)
```

**Related Terms**: CORS, Preflight, Cache

---

### Access-Control-Expose-Headers

**Definition**: Response header indicating which response headers can be read by the browser.

**Code Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Expose custom headers
app.add_middleware(
    CORSMiddleware,
    expose_headers=["X-Total-Count", "X-Page-Count", "X-Request-ID"]
)
# Response header: Access-Control-Expose-Headers: X-Total-Count, X-Page-Count, X-Request-ID

# Common exposed headers
EXPOSED_HEADERS = [
    "X-Total-Count",      # Total items for pagination
    "X-Page-Count",       # Total pages
    "X-Request-ID",       # Request tracking
    "Content-Disposition" # File download name
]

app.add_middleware(
    CORSMiddleware,
    expose_headers=EXPOSED_HEADERS
)

# Frontend access
"""
const response = await fetch('https://api.example.com/items');
const totalCount = response.headers.get('X-Total-Count');
"""
```

**Related Terms**: CORS, Headers, Response

---

### CORS (Cross-Origin Resource Sharing)

**Definition**: A security mechanism that allows or restricts web applications from accessing resources from different origins.

**Code Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Basic CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)

# How CORS works:
# 1. Browser sends request to different origin
# 2. For simple requests: Browser adds Origin header
# 3. For complex requests: Browser sends preflight OPTIONS
# 4. Server responds with CORS headers
# 5. Browser allows/blocks the request

@app.get("/api/data")
async def get_data():
    return {"data": "value"}

@app.post("/api/data")
async def create_data(data: dict):
    return {"created": True, "data": data}
```

**Related Terms**: Origin, Security, Middleware

---

### Origin

**Definition**: The combination of protocol, domain, and port that identifies where a request comes from.

**Code Example**:
```python
# Origin components
# https://app.example.com:443
# ├── Protocol: https
# ├── Domain: app.example.com
# └── Port: 443 (default for HTTPS)

# Different origins
origins = [
    "http://localhost:3000",      # Development frontend
    "https://app.example.com",    # Production frontend
    "https://api.example.com",    # API (different subdomain)
    "http://localhost:8080"       # Different port
]

# Same origin
# https://example.com/page1
# https://example.com/page2
# Same origin: https://example.com

# Different origins
# https://example.com
# http://example.com  (different protocol)
# https://api.example.com  (different subdomain)
# https://example.com:8080  (different port)
```

**Related Terms**: CORS, URL, Protocol

---

### Preflight

**Definition**: An OPTIONS request sent by the browser before the actual request to check if the real request is allowed.

**Code Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)

# Preflight request (browser sends automatically)
"""
OPTIONS /api/data HTTP/1.1
Host: api.example.com
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
"""

# Preflight response (server sends)
"""
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 600
"""

# Actual request (browser sends after preflight)
"""
POST /api/data HTTP/1.1
Host: api.example.com
Origin: http://localhost:3000
Content-Type: application/json
Authorization: Bearer token123
"""
```

**Related Terms**: CORS, OPTIONS, Request

---

### Simple Request

**Definition**: A cross-origin request that doesn't require a preflight check.

**Code Example**:
```python
# Simple request criteria:
# 1. Method is GET, HEAD, or POST
# 2. Only these headers:
#    - Accept
#    - Accept-Language
#    - Content-Language
#    - Content-Type (with restrictions)
# 3. Content-Type is one of:
#    - application/x-www-form-urlencoded
#    - multipart/form-data
#    - text/plain

# Examples of simple requests
"""
GET /api/data HTTP/1.1
Origin: http://localhost:3000

POST /api/data HTTP/1.1
Origin: http://localhost:3000
Content-Type: text/plain

Hello, world!
"""

# Non-simple request (requires preflight)
"""
POST /api/data HTTP/1.1
Origin: http://localhost:3000
Content-Type: application/json  # Not simple!
Authorization: Bearer token123  # Custom header!
"""
```

**Related Terms**: CORS, Preflight, Request

---

### Credentials

**Definition**: Authentication information included in requests (cookies, HTTP auth, client-side SSL certificates).

**Code Example**:
```python
from fastapi import FastAPI, Cookie, Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True  # Enable credentials
)

# Endpoint using cookies
@app.get("/api/profile")
async def get_profile(session_id: str = Cookie(None)):
    return {"session_id": session_id}

# Endpoint using auth header
@app.get("/api/user")
async def get_user(authorization: str = Header(None)):
    return {"authorization": authorization}

# Frontend request with credentials
"""
// Include cookies
fetch('https://api.example.com/api/profile', {
    credentials: 'include'
})

// Include auth header
fetch('https://api.example.com/api/user', {
    credentials: 'include',
    headers: {
        'Authorization': 'Bearer token123'
    }
})
"""
```

**Related Terms**: CORS, Auth, Cookies

---

### Same-Origin Policy

**Definition**: Browser security policy that restricts how documents or scripts from one origin can interact with resources from another origin.

**Code Example**:
```python
# Same-origin policy in action:
# https://app.example.com/page1

# Can access:
# https://app.example.com/page2  ✓ Same origin
# https://app.example.com/api    ✓ Same origin

# Cannot access (without CORS):
# https://api.example.com/data   ✗ Different subdomain
# http://app.example.com/data    ✗ Different protocol
# https://app.example.com:8080   ✗ Different port
# https://other.com/data         ✗ Different domain

# CORS relaxes same-origin policy:
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization"]
)

# Now https://app.example.com can access this API
@app.get("/api/data")
async def get_data():
    return {"data": "value"}
```

**Related Terms**: CORS, Security, Browser

---

### Callback

**Definition**: A function that dynamically determines whether to allow a request based on its origin.

**Code Example**:
```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Dynamic origin validation
def validate_origin(origin: str) -> bool:
    """Validate origin based on custom logic"""
    allowed_patterns = [
        "https://*.example.com",
        "http://localhost:*"
    ]
    
    import re
    for pattern in allowed_patterns:
        regex = pattern.replace("*", ".*")
        if re.match(regex, origin):
            return True
    
    return False

# Use callback
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Fallback
    allow_origin_callback=validate_origin,
    allow_credentials=True
)

# More complex callback
def dynamic_cors(request: Request) -> str:
    """Return allowed origin or None"""
    origin = request.headers.get("origin")
    
    # Check against database or config
    if origin in get_allowed_origins():
        return origin
    
    # Check subdomain
    if origin and origin.endswith(".example.com"):
        return origin
    
    return None

app.add_middleware(
    CORSMiddleware,
    allow_origin_callback=dynamic_cors
)
```

**Related Terms**: CORS, Origin, Dynamic

---

## CORS Headers Reference

| Header | Direction | Description |
|--------|-----------|-------------|
| Access-Control-Allow-Origin | Response | Allowed origins |
| Access-Control-Allow-Methods | Response | Allowed HTTP methods |
| Access-Control-Allow-Headers | Response | Allowed request headers |
| Access-Control-Allow-Credentials | Response | If credentials allowed |
| Access-Control-Expose-Headers | Response | Headers exposed to browser |
| Access-Control-Max-Age | Response | Preflight cache duration |
| Access-Control-Request-Method | Request | Method for preflight |
| Access-Control-Request-Headers | Request | Headers for preflight |
| Origin | Request | Request origin |

---

## Common CORS Errors

| Error | Cause | Solution |
|-------|-------|----------|
| No 'Access-Control-Allow-Origin' header | Origin not allowed | Add origin to allow_origins |
| Origin is not allowed | Wildcard with credentials | List specific origins |
| Method not allowed | Method not in allow_methods | Add method to allow_methods |
| Header not allowed | Header not in allow_headers | Add header to allow_headers |
| Credentials not allowed | allow_credentials=False | Set allow_credentials=True |

---

## Configuration Examples

### Development
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### Staging
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://staging.example.com",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=300
)
```

### Production
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.example.com",
        "https://admin.example.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Total-Count", "X-Request-ID"],
    max_age=600
)
```

---

## Summary

Understanding CORS is essential for building secure web applications. Key takeaways:

1. **CORS**: Browser security for cross-origin requests
2. **Origins**: Protocol + domain + port
3. **Preflight**: OPTIONS request for complex requests
4. **Credentials**: Authentication data handling
5. **Headers**: Control what's allowed/exposed
6. **Callbacks**: Dynamic origin validation
7. **Security**: Never use wildcard with credentials

**Next**: Move to the exception handling lecture to learn error management patterns.
