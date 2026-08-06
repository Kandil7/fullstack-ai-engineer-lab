# Glossary: FastAPI Middleware

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Middleware | Code that intercepts requests/responses | LoggingMiddleware |
| ASGI | Asynchronous Server Gateway Interface | uvicorn |
| CORS | Cross-Origin Resource Sharing | CORSMiddleware |
| LIFO | Last In, First Out execution order | Middleware stack |
| Request Object | HTTP request data container | `request: Request` |
| Response Object | HTTP response data container | `Response(content="...")` |
| Call Next | Function to invoke next middleware/endpoint | `await call_next(request)` |
| Dispatch | Method that processes request/response | `async def dispatch()` |
| BaseHTTPMiddleware | Base class for custom middleware | Class inheritance |
| Middleware Stack | Ordered collection of middleware | App middleware chain |
| Request State | Per-request data storage | `request.state` |
| Header Injection | Adding headers to request/response | `response.headers["X-Header"]` |
| Short-Circuit | Returning response before endpoint | Early response return |
| Trusted Host | Host validation middleware | TrustedHostMiddleware |
| GZip | Compression middleware | GZipMiddleware |

---

## Terms - Alphabetical Order

### API Key

**Definition:** A unique identifier used to authenticate a client making API requests. Often passed in headers.

**Example:**
```python
api_key = request.headers.get("X-API-Key")
if api_key != VALID_KEY:
    raise HTTPException(status_code=403, detail="Invalid API key")
```

**Related Terms:** Authentication, Headers, Security

---

### ASGI (Asynchronous Server Gateway Interface)

**Definition:** A spiritual successor to WSGI, designed for asynchronous Python web applications. FastAPI middleware uses ASGI under the hood.

**Example:**
```python
# ASGI app (what FastAPI creates)
app = FastAPI()

# Running with ASGI server
# uvicorn main:app --reload
```

**Related Terms:** WSGI, Uvicorn, Starlette

---

### BaseHTTPMiddleware

**Definition:** The base class from Starlette that you inherit from to create custom middleware in FastAPI.

**Example:**
```python
from starlette.middleware.base import BaseHTTPMiddleware

class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Process request
        response = await call_next(request)
        # Process response
        return response
```

**Related Terms:** Dispatch, Middleware, Starlette

---

### Call Next

**Definition:** The function passed to middleware's dispatch method that invokes the next middleware or endpoint in the chain.

**Example:**
```python
async def dispatch(self, request: Request, call_next):
    # Before processing
    response = await call_next(request)
    # After processing
    return response
```

**Related Terms:** Dispatch, Middleware Stack, Chain of Responsibility

---

### CORS (Cross-Origin Resource Sharing)

**Definition:** A security mechanism that allows or restricts web pages from one domain to access resources from another domain.

**Example:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

**Related Terms:** Origins, Methods, Headers, Security

---

### CORS Middleware

**Definition:** Built-in FastAPI middleware that handles CORS headers automatically.

**Example:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Related Terms:** CORS, Origins, Preflight Request

---

### Dispatch

**Definition:** The method in BaseHTTPMiddleware subclasses that processes each request/response pair.

**Example:**
```python
class TimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        return response
```

**Related Terms:** BaseHTTPMiddleware, Call Next, Middleware

---

### GZip Middleware

**Definition:** Built-in middleware that compresses response bodies using GZip compression to reduce bandwidth.

**Example:**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=500)
# Responses > 500 bytes will be compressed
```

**Related Terms:** Compression, Bandwidth, Response Size

---

### Header Injection

**Definition:** Adding custom headers to HTTP requests or responses within middleware.

**Example:**
```python
# Adding to response
response.headers["X-Request-ID"] = request_id
response.headers["X-Powered-By"] = "FastAPI"

# Adding to request (using Request object)
request.headers["Authorization"] = f"Bearer {token}"
```

**Related Terms:** Headers, Request, Response

---

### LIFO (Last In, First Out)

**Definition:** The execution order pattern where the last middleware added is the first to process the response.

**Example:**
```python
# Added first - executes first on request, last on response
app.add_middleware(MiddlewareA)
# Added second - executes second on both
app.add_middleware(MiddlewareB)
# Added last - executes last on request, first on response
app.add_middleware(MiddlewareC)
```

**Related Terms:** Middleware Stack, Execution Order

---

### Middleware

**Definition:** Software that sits between the client and server, processing requests and responses before they reach the application logic.

**Example:**
```python
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Incoming: {request.method} {request.url}")
        response = await call_next(request)
        print(f"Response: {response.status_code}")
        return response
```

**Related Terms:** ASGI, Dispatch, Call Next, Stack

---

### Middleware Order

**Definition:** The sequence in which middleware executes, which affects how requests and responses are processed.

**Example:**
```python
# CORRECT ORDER:
app.add_middleware(CORSMiddleware)      # 1st
app.add_middleware(TrustedHostMiddleware) # 2nd
app.add_middleware(LoggingMiddleware)    # 3rd
app.add_middleware(AuthMiddleware)       # 4th
```

**Related Terms:** LIFO, Middleware Stack, CORS

---

### Middleware Stack

**Definition:** The complete ordered collection of middleware that processes requests in your FastAPI application.

**Example:**
```python
app = FastAPI()
# Stack built bottom-up, processes top-down
app.add_middleware(A)  # Bottom of stack
app.add_middleware(B)  # Middle
app.add_middleware(C)  # Top of stack
```

**Related Terms:** LIFO, Execution Order, Middleware

---

### Preflight Request

**Definition:** A CORS request sent by browsers before the actual request to check if the server allows the cross-origin operation.

**Example:**
```python
# Browser sends OPTIONS request first
@app.options("/api/data")
async def options_handler():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST",
        }
    )
```

**Related Terms:** CORS, OPTIONS, Headers

---

### Request Object

**Definition:** The FastAPI/Starlette object containing all HTTP request data (headers, body, query params, etc.).

**Example:**
```python
@app.get("/items/{item_id}")
async def read_item(request: Request, item_id: int):
    # Access request data
    headers = request.headers
    query = request.query_params
    path = request.url.path
    client_ip = request.client.host
    return {"path": path, "client": client_ip}
```

**Related Terms:** Headers, Query Params, Client

---

### Request State

**Definition:** A per-request storage object for passing data between middleware and endpoint functions.

**Example:**
```python
class UserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Store user in request state
        request.state.user = get_current_user(request)
        return await call_next(request)

@app.get("/profile")
async def profile(request: Request):
    # Access stored user
    user = request.state.user
    return {"user": user}
```

**Related Terms:** Request, State, Middleware

---

### Response Object

**Definition:** The FastAPI/Starlette object representing the HTTP response to send back to the client.

**Example:**
```python
from starlette.responses import JSONResponse

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Modify response
        response.headers["X-Custom"] = "value"
        return response
```

**Related Terms:** Headers, Status Code, Content

---

### Short-Circuit

**Definition:** Returning a response from middleware before the request reaches the endpoint function.

**Example:**
```python
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Short-circuit if no auth header
        if "Authorization" not in request.headers:
            return JSONResponse(
                status_code=401,
                content={"error": "Missing auth"}
            )
        return await call_next(request)
```

**Related Terms:** Early Return, Authentication, Response

---

### Trusted Host Middleware

**Definition:** Built-in middleware that restricts which host headers are allowed, preventing host header attacks.

**Example:**
```python
from starlette.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

**Related Terms:** Host, Security, Host Header

---

### Uvicorn

**Definition:** An ASGI web server that runs FastAPI applications and processes middleware.

**Example:**
```bash
# Run FastAPI with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# With multiple workers
uvicorn main:app --workers 4
```

**Related Terms:** ASGI, Server, Workers

---

## Code Examples Collection

### Complete Middleware Setup

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

app = FastAPI()

# 1. CORS Middleware (outermost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. GZip Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 3. Custom Logging Middleware (innermost)
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        response.headers["X-Response-Time"] = f"{duration:.3f}"
        
        return response

app.add_middleware(LoggingMiddleware)

@app.get("/")
async def root():
    return {"message": "All middleware active"}
```

### Middleware with State Sharing

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

app = FastAPI()

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response

app.add_middleware(RequestIDMiddleware)

@app.get("/users")
async def get_users(request: Request):
    # Access request ID from state
    return {
        "request_id": request.state.request_id,
        "users": ["Alice", "Bob"]
    }
```

---

## Quick Reference Card

### Common Middleware Classes

```python
# CORS
from fastapi.middleware.cors import CORSMiddleware

# GZip Compression
from fastapi.middleware.gzip import GZipMiddleware

# Trusted Hosts
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Custom Middleware Base
from starlette.middleware.base import BaseHTTPMiddleware
```

### Middleware Methods

```python
class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Read request
        path = request.url.path
        headers = request.headers
        
        # Process request
        response = await call_next(request)
        
        # Modify response
        response.headers["X-Custom"] = "value"
        
        return response
```

### Request Properties

```python
request.url           # URL object
request.url.path      # "/api/users"
request.url.query     # "page=1"
request.method        # "GET", "POST", etc.
request.headers       # Headers dict
request.query_params  # Query parameters dict
request.path_params   # Path parameters dict
request.client        # Client info (host, port)
request.state         # Per-request state storage
```

### Response Properties

```python
response.status_code  # 200, 404, etc.
response.headers      # Headers dict
response.body         # Response body bytes
```

---

## Debugging Middleware

### Enable Middleware Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

class DebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.debug(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logging.debug(f"Response: {response.status_code}")
        return response
```

### Check Middleware Order

```python
@app.get("/debug/middleware")
async def debug_middleware():
    middleware_list = [
        str(m) for m in app.user_middleware
    ]
    return {"middleware_order": middleware_list}
```
