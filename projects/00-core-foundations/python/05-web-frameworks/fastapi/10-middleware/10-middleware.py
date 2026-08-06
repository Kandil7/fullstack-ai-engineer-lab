"""
10 - Middleware
================
Middleware runs before and after every request.
It can modify the request/response, add headers, log activity, measure timing, etc.

Run: uvicorn 10-middleware:app --reload
"""

import sys
import time
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

# CI-safe stdout: teaching prints contain non-ASCII (e.g. "->") which crashes
# on a cp1252 console; make encoding explicit and never raise on encode.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Middleware in FastAPI")


# ----- Custom middleware using @app.middleware("http") -----
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """
    Middleware that adds a unique request ID to every request/response.
    Middleware wraps every request — useful for tracing and logging.
    """
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id

    # Process the request
    response = await call_next(request)

    # Add header to response
    response.headers["X-Request-ID"] = request_id
    return response


# ----- Timing middleware -----
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    """Add response time header to every response."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response


# ----- Logging middleware -----
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log method, path, and status code for every request."""
    start = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start) * 1000
    print(
        f"[{request.method}] {request.url.path} → {response.status_code} ({duration:.2f}ms)"
    )
    return response


# ----- Security headers middleware -----
@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Add common security headers to responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# ----- CORS middleware (from starlette) -----
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- GZip compression middleware -----
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)


# ----- Base paths -----
@app.get("/")
def root():
    """Root endpoint — all middleware applies here."""
    return {
        "message": "Middleware Demo",
        "tips": [
            "Check response headers for X-Request-ID, X-Process-Time-Ms",
            "Security headers are added automatically",
            "CORS is configured for all origins",
        ],
    }


# ----- Endpoints to demonstrate middleware -----
@app.get("/slow")
async def slow_endpoint():
    """Endpoint that takes some time — timing middleware measures it."""
    await asyncio.sleep(0.5)  # Simulate slow work
    return {"message": "This was slow", "duration": "~500ms"}


@app.get("/fast")
def fast_endpoint():
    """Fast endpoint — timing middleware shows near-zero."""
    return {"message": "This was fast"}


@app.get("/error")
def error_endpoint():
    """Endpoint that returns an error — middleware still runs."""
    return JSONResponse(
        status_code=400,
        content={"error": "Something went wrong"},
    )


# ----- Middleware that can be toggled -----
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """
    Simple rate limiting middleware.
    In production, use Redis for distributed rate limiting.
    """
    client_ip = request.client.host if request.client else "unknown"
    # In production: check Redis counter for this IP
    # For demo, just pass through
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = "100"
    response.headers["X-RateLimit-Remaining"] = "99"
    return response


# ----- Need asyncio for the slow endpoint -----
import asyncio


"""
Testing with curl:
    curl -v http://127.0.0.1:8000/
    # Look for headers: X-Request-ID, X-Process-Time-Ms, X-Content-Type-Options

    curl -v http://127.0.0.1:8000/slow
    # X-Process-Time-Ms should be ~500ms

    curl -v http://127.0.0.1:8000/fast
    # X-Process-Time-Ms should be ~0ms

    curl -v http://127.0.0.1:8000/error
    # Even error responses get middleware headers
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)

    r = client.get("/")
    assert r.status_code == 200
    assert r.headers.get("X-Request-ID")  # custom middleware header
    assert r.headers.get("X-Content-Type-Options") == "nosniff"  # security headers

    r = client.get("/fast")
    assert r.status_code == 200
    assert r.json()["message"] == "This was fast"

    r = client.get("/error")
    assert r.status_code == 400
    assert r.headers.get("X-RateLimit-Limit") == "100"

    r = client.get("/slow")  # takes ~0.5s (teaching demo of timing middleware)
    assert r.status_code == 200
    assert r.headers.get("X-Process-Time-Ms")

    print("[OK] 10-middleware: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
