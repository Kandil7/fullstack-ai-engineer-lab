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


# =============================================================================
# Exercise 1: Basic Request Logging Middleware
# =============================================================================
# Create a middleware that logs:
#   - Request method
#   - Request path
#   - Response status code
#   - Time taken (in milliseconds)
#
# Hints:
#   - Use @app.middleware("http") decorator
#   - Call await call_next(request) to continue the request chain
#   - Time the request using time.time()
#
# Expected behavior:
#   GET http://localhost:8000/hello
#   Console output: "GET /hello - 200 - 12.34ms"
#
# Test with:
#   curl http://localhost:8000/hello
# =============================================================================

app1 = FastAPI(title="Exercise 1 - Logging Middleware")


@app1.middleware("http")
async def log_requests(request: Request, call_next):
    # TODO: Implement logging middleware
    # 1. Record start time
    # 2. Call call_next(request)
    # 3. Record end time
    # 4. Log method, path, status, and duration
    pass


@app1.get("/hello")
def hello():
    return {"message": "Hello!"}


# =============================================================================
# Exercise 2: Custom Header Injection Middleware
# =============================================================================
# Create a middleware that adds these headers to EVERY response:
#   - X-App-Version: "1.0.0"
#   - X-Request-ID: a unique ID for each request
#
# Hints:
#   - Use uuid.uuid4() to generate unique request IDs
#   - Modify response.headers after calling call_next()
#   - Headers are case-insensitive
#
# Expected behavior:
#   GET http://localhost:8000/data
#   Response headers include:
#     X-App-Version: 1.0.0
#     X-Request-ID: <unique-uuid>
#
# Test with:
#   curl -v http://localhost:8000/data
# =============================================================================

app2 = FastAPI(title="Exercise 2 - Header Injection Middleware")


@app2.middleware("http")
async def add_headers(request: Request, call_next):
    # TODO: Implement header injection middleware
    pass


@app2.get("/data")
def get_data():
    return {"data": "some data"}


# =============================================================================
# Exercise 3: Rate Limiting Middleware
# =============================================================================
# Create a middleware that limits requests:
#   - Allow maximum 5 requests per minute per client IP
#   - Return 429 "Too Many Requests" if limit exceeded
#   - Include X-RateLimit-Remaining header with remaining count
#
# Hints:
#   - Use a dict to track requests: {ip: [timestamps]}
#   - Clean up old timestamps (> 60 seconds old)
#   - Client IP is in request.client.host
#
# Expected behavior:
#   GET http://localhost:8000/api/resource (1st-5th) -> 200 OK
#   GET http://localhost:8000/api/resource (6th) -> 429 Too Many Requests
#
# Test with:
#   for i in {1..6}; do curl http://localhost:8000/api/resource; done
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Rate Limiting Middleware")

# TODO: Create a storage for rate limiting


@app3.middleware("http")
async def rate_limit(request: Request, call_next):
    # TODO: Implement rate limiting logic
    pass


@app3.get("/api/resource")
def get_resource():
    return {"resource": "data"}


# =============================================================================
# Exercise 4: Exception Handling Middleware
# =============================================================================
# Create a middleware that catches ALL exceptions and returns a
# standardized JSON error response:
#   {
#     "error": true,
#     "message": "<exception message>",
#     "type": "<exception type name>"
#   }
#
# Hints:
#   - Wrap call_next in a try/except block
#   - Return JSONResponse with status_code=500
#   - Use exception.__class__.__name__ for type
#
# Expected behavior:
#   GET http://localhost:8000/crash
#   Response: {"error": true, "message": "...", "type": "ValueError"}
#   Status code: 500
#
# Test with:
#   curl http://localhost:8000/crash
# =============================================================================

app4 = FastAPI(title="Exercise 4 - Exception Handling Middleware")


@app4.middleware("http")
async def catch_errors(request: Request, call_next):
    # TODO: Implement exception handling middleware
    pass


@app4.get("/crash")
def crash():
    raise ValueError("Something went wrong!")


@app4.get("/ok")
def ok():
    return {"status": "ok"}


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 10-middleware:app1 --reload
#    - Check console output for request logging
#    - Verify method, path, status, and time are logged
#
# 2. Run: uvicorn 10-middleware:app2 --reload
#    - Use curl -v to verify custom headers are present
#    - Verify X-Request-ID is unique for each request
#
# 3. Run: uvicorn 10-middleware:app3 --reload
#    - Send 6 rapid requests; 6th should be 429
#    - Wait 60s and verify counter resets
#
# 4. Run: uvicorn 10-middleware:app4 --reload
#    - GET /crash should return standardized error JSON
#    - GET /ok should work normally
# =============================================================================
