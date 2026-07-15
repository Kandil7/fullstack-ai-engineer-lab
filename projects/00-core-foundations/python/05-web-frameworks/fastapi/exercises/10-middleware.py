"""
FastAPI Exercise 10 - Middleware
================================

Topics covered:
- Understanding middleware in FastAPI
- Creating custom middleware
- Middleware for logging, CORS, and authentication
- Exception handling middleware

Requirements:
    pip install fastapi uvicorn

Run any exercise:
    uvicorn 10-middleware:app1 --reload
    uvicorn 10-middleware:app2 --reload
    uvicorn 10-middleware:app3 --reload
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import uuid
from collections import defaultdict


# =============================================================================
# Exercise 1: Basic Request Logging Middleware
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Logging Middleware")


@app1.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request method, path, status code, and duration."""
    start = time.time()
    response = await call_next(request)
    elapsed = (time.time() - start) * 1000
    print(f"  {request.method} {request.url.path} - {response.status_code} - {elapsed:.2f}ms")
    return response


@app1.get("/hello")
def hello():
    return {"message": "Hello!"}


# =============================================================================
# Exercise 2: Custom Header Injection Middleware
# =============================================================================

app2 = FastAPI(title="Exercise 2 - Header Injection Middleware")


@app2.middleware("http")
async def add_headers(request: Request, call_next):
    """Add custom headers to every response."""
    response = await call_next(request)
    response.headers["X-App-Version"] = "1.0.0"
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    return response


@app2.get("/data")
def get_data():
    return {"data": "some data"}


# =============================================================================
# Exercise 3: Rate Limiting Middleware
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Rate Limiting Middleware")

# Track requests: {ip: [(timestamp,), ...]}
rate_limit_store: dict[str, list] = defaultdict(list)
MAX_REQUESTS = 5
WINDOW_SECONDS = 60


@app3.middleware("http")
async def rate_limit(request: Request, call_next):
    """Limit requests to 5 per minute per client IP."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    # Clean up old timestamps
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip]
        if now - t < WINDOW_SECONDS
    ]

    # Check limit
    if len(rate_limit_store[client_ip]) >= MAX_REQUESTS:
        remaining = 0
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests", "retry_after": WINDOW_SECONDS},
            headers={"X-RateLimit-Remaining": str(remaining)},
        )

    # Record request and compute remaining
    rate_limit_store[client_ip].append(now)
    remaining = MAX_REQUESTS - len(rate_limit_store[client_ip])

    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response


@app3.get("/api/resource")
def get_resource():
    return {"resource": "data"}


# =============================================================================
# Exercise 4: Exception Handling Middleware
# =============================================================================

app4 = FastAPI(title="Exercise 4 - Exception Handling Middleware")


@app4.middleware("http")
async def catch_errors(request: Request, call_next):
    """Catch all exceptions and return standardized JSON error response."""
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": str(exc),
                "type": exc.__class__.__name__,
            },
        )


@app4.get("/crash")
def crash():
    """Endpoint that raises an exception to test error handling."""
    raise ValueError("Something went wrong!")


@app4.get("/ok")
def ok():
    """Normal endpoint that should work with error handling middleware."""
    return {"status": "ok"}
