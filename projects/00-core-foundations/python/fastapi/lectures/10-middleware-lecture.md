# Lecture 10: FastAPI Middleware

## Topic Overview

Middleware in FastAPI is a powerful mechanism that allows you to intercept and modify HTTP requests and responses as they flow through your application. Think of middleware as a series of "layers" that every request passes through before reaching your endpoint functions and again on the way back to the client.

Middleware operates on a principle similar to onion layers in software architecture - each request passes through each middleware layer twice: once on the way in (request processing) and once on the way out (response processing).

**Why Middleware Matters:**
- Cross-cutting concerns like logging, authentication, and CORS handling
- Request/response transformation
- Performance monitoring and metrics collection
- Security headers injection
- Request validation and sanitization

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand middleware architecture** - How middleware layers work in FastAPI
2. **Create custom middleware** - Build your own middleware using the decorator pattern
3. **Implement middleware classes** - Use class-based middleware for complex logic
4. **Handle CORS** - Configure Cross-Origin Resource Sharing properly
5. **Add security headers** - Inject security headers into responses
6. **Implement logging middleware** - Track all incoming requests and responses
7. **Apply middleware selectively** - Use middleware on specific routes or groups
8. **Debug middleware issues** - Identify and fix common middleware problems

---

## Key Concepts

### 1. What is Middleware?

Middleware is code that runs before and after each request to your application. It can:

- **Read the request** - Access headers, body, query parameters
- **Modify the request** - Add data, transform content, validate inputs
- **Short-circuit the response** - Return early without hitting the endpoint
- **Read the response** - Access the response before sending to client
- **Modify the response** - Add headers, transform content, log data

### 2. The Middleware Stack

FastAPI processes middleware in a stack (LIFO - Last In, First Out):

```
Client Request
     │
     ▼
┌─────────────────┐
│  Middleware 1    │ ← First to process request
│  (Request)      │ ← Last to process response
├─────────────────┤
│  Middleware 2    │ ← Second to process request
│  (Request)      │ ← Second to process response
├─────────────────┤
│  Middleware 3    │ ← Last to process request
│  (Request)      │ ← First to process response
├─────────────────┤
│  Endpoint        │
└─────────────────┘
     │
     ▼
Client Response
```

### 3. Middleware Execution Order

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Middleware execution order (LIFO):
# 1. add_middleware(A) - executes first on request, last on response
# 2. add_middleware(B) - executes second on request, second on response
# 3. add_middleware(C) - executes last on request, first on response

app.add_middleware(A)  # Outer layer
app.add_middleware(B)  # Middle layer
app.add_middleware(C)  # Inner layer
```

---

## Code Examples

### Example 1: Simple Custom Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

app = FastAPI()

class SimpleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Process request
        start_time = time.time()
        
        # Call the next middleware or endpoint
        response = await call_next(request)
        
        # Process response
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

app.add_middleware(SimpleMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Example 2: Logging Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        logger.info(f"Request: {request.method} {request.url.path}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Process request
        response = await call_next(request)
        
        # Log response details
        logger.info(f"Response: {response.status_code}")
        
        return response

app = FastAPI()
app.add_middleware(LoggingMiddleware)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

### Example 3: Authentication Middleware

```python
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for certain paths
        if request.url.path in ["/docs", "/openapi.json", "/health"]:
            return await call_next(request)
        
        # Check for authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail="Authorization header required"
            )
        
        # Validate token (simplified)
        token = auth_header.replace("Bearer ", "")
        if not self.validate_token(token):
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        
        # Continue to endpoint
        return await call_next(request)
    
    def validate_token(self, token: str) -> bool:
        # Simplified token validation
        return len(token) > 0

app = FastAPI()
app.add_middleware(AuthMiddleware)

@app.get("/protected")
async def protected_route():
    return {"message": "You have access!"}
```

### Example 4: CORS Middleware

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CORS enabled!"}
```

### Example 5: Request ID Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Add to request state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response

app = FastAPI()
app.add_middleware(RequestIDMiddleware)

@app.get("/")
async def root(request: Request):
    return {"request_id": request.state.request_id}
```

### Example 6: GZip Compression Middleware

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Enable GZip compression for responses > 1000 bytes
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/large-data")
async def large_data():
    # This response will be compressed
    return {"data": "x" * 10000}
```

### Example 7: Trusted Host Middleware

```python
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# Only allow requests from specific hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "www.example.com", "localhost"]
)

@app.get("/")
async def root():
    return {"message": "Trusted host only!"}
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting to Call `call_next()`

```python
# ❌ WRONG - Never calls the endpoint
class BadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return Response(content="Blocked")

# ✅ CORRECT - Properly calls next middleware
class GoodMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response
```

### Mistake 2: Middleware Order Issues

```python
# ❌ WRONG - CORS middleware added too late
app = FastAPI()
app.add_middleware(AuthMiddleware)
app.add_middleware(CORSMiddleware, ...)  # CORS won't work properly

# ✅ CORRECT - CORS should be added first
app = FastAPI()
app.add_middleware(CORSMiddleware, ...)  # CORS first
app.add_middleware(AuthMiddleware)       # Then auth
```

### Mistake 3: Not Handling Exceptions

```python
# ❌ WRONG - Exceptions not caught
class FragileMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response

# ✅ CORRECT - Proper exception handling
class RobustMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            return Response(
                content=f"Error: {str(e)}",
                status_code=500
            )
```

---

## Best Practices

1. **Keep middleware lightweight** - Don't add heavy processing that slows down every request
2. **Use async/await** - Always use async operations in middleware for better performance
3. **Order matters** - Add CORS middleware first, then authentication, then other middleware
4. **Handle exceptions** - Always wrap `call_next()` in try/except
5. **Use request.state** - Store data in request state to pass between middleware and endpoints
6. **Don't modify request body** - Read body only once; use request.state for cached data
7. **Add meaningful headers** - Include request ID, timing, and other useful headers
8. **Test middleware independently** - Unit test middleware logic separately

---

## Practice Exercises

### Exercise 1: Rate Limiting Middleware
Create middleware that limits requests to 100 per minute per client IP. Return 429 status when exceeded.

### Exercise 2: API Key Validation Middleware
Build middleware that validates API keys from the `X-API-Key` header and rejects invalid keys.

### Exercise 3: Response Time Tracking Middleware
Create middleware that logs response times and adds warnings for slow responses (>500ms).

### Exercise 4: Request Logging Middleware
Implement middleware that logs full request details (method, path, headers, body) and response status.

### Exercise 5: Security Headers Middleware
Build middleware that adds security headers like `X-Content-Type-Options`, `X-Frame-Options`, and `X-XSS-Protection`.

---

## Summary

- **Middleware** intercepts requests and responses at the application level
- **Execution order** follows LIFO (Last In, First Out) principle
- **Use cases** include logging, authentication, CORS, compression, and security
- **BaseHTTPMiddleware** is the primary way to create custom middleware in FastAPI
- **Always call `call_next()`** to continue the request chain
- **Order matters** - CORS should be first, then security, then other middleware
- **Keep it lightweight** - Don't add heavy processing to middleware

---

## Further Reading

- [FastAPI Official Documentation - Middleware](https://fastapi.tiangolo.com/advanced/middleware/)
- [Starlette Middleware](https://www.starlette.io/middleware/)
- [ASGI Middleware](https://asgi.readthedocs.io/en/latest/specs/www.html)
