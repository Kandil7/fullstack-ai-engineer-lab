"""
23 - Exception Handling
=========================
Custom exception handlers, HTTPException, and error responses.
Proper error handling is critical for API usability.

Run: uvicorn 23-exception-handling:app --reload
"""

import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

app = FastAPI(title="Exception Handling in FastAPI")


# ----- Custom Exception Classes -----
class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, status_code: int = 500, error_code: str = "UNKNOWN"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class NotFoundError(AppError):
    """Resource not found."""
    def __init__(self, resource: str, resource_id: int | str):
        super().__init__(
            message=f"{resource} with id '{resource_id}' not found",
            status_code=404,
            error_code="NOT_FOUND",
        )


class ValidationError_(AppError):
    """Business validation error."""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=422, error_code="VALIDATION_ERROR")


class RateLimitError(AppError):
    """Rate limit exceeded."""
    def __init__(self):
        super().__init__(
            message="Rate limit exceeded. Try again later.",
            status_code=429,
            error_code="RATE_LIMITED",
        )


# ----- Exception Handlers -----
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """Handle custom AppError with structured JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url),
            }
        },
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler for all not-found routes."""
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "ROUTE_NOT_FOUND",
                "message": f"Route {request.url.path} not found",
                "suggestion": "Check /docs for available endpoints",
            }
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler — don't leak internals in production."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "timestamp": datetime.now().isoformat(),
            }
        },
    )


@app.exception_handler(ValidationError)
async def pydantic_error_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors with cleaner messages."""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({"field": field, "message": error["msg"]})
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors,
            }
        },
    )


# ----- Models -----
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str
    age: int = Field(..., ge=0, le=150)


# In-memory store
users_db: dict[int, dict] = {}
next_id = 1


# ----- Endpoints with error handling -----
@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    """Create user with validation."""
    global next_id
    # Business validation
    if any(u["email"] == user.email for u in users_db.values()):
        raise ValidationError_(f"Email '{user.email}' is already registered")

    users_db[next_id] = {"id": next_id, **user.model_dump()}
    next_id += 1
    return users_db[next_id - 1]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Get user — raises custom NotFoundError."""
    if user_id not in users_db:
        raise NotFoundError("User", user_id)
    return users_db[user_id]


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete user with proper error handling."""
    if user_id not in users_db:
        raise NotFoundError("User", user_id)
    del users_db[user_id]
    return {"deleted": True, "id": user_id}


@app.get("/users/")
def list_users():
    """List all users."""
    return {"users": list(users_db.values()), "count": len(users_db)}


# ----- HTTPException with headers -----
@app.get("/rate-limited/")
def rate_limited():
    """Demonstrate HTTPException with custom headers."""
    raise HTTPException(
        status_code=429,
        detail="Too many requests",
        headers={"Retry-After": "60", "X-RateLimit-Limit": "100"},
    )


# ----- Multiple error scenarios -----
@app.get("/error/{error_type}")
def demo_errors(error_type: str):
    """Demonstrate different error types."""
    errors = {
        "not-found": lambda: (_ for _ in ()).throw(NotFoundError("Item", 42)),
        "validation": lambda: (_ for _ in ()).throw(ValidationError_("Invalid input")),
        "rate-limit": lambda: (_ for _ in ()).throw(RateLimitError()),
        "http": lambda: (_ for _ in ()).throw(
            HTTPException(status_code=403, detail="Forbidden")
        ),
        "division": lambda: 1 / 0,
    }

    if error_type not in errors:
        return {"available_errors": list(errors.keys())}

    try:
        errors[error_type]()
    except ZeroDivisionError:
        raise HTTPException(status_code=500, detail="Internal computation error")


# ----- Catch-all handler -----
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catch-all handler for unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "UNHANDLED",
                "message": "An unexpected error occurred",
                "type": type(exc).__name__,
                "timestamp": datetime.now().isoformat(),
            }
        },
    )


"""
Testing with curl:
    curl http://127.0.0.1:8000/users/999  # Custom 404
    curl -X POST http://127.0.0.1:8000/users/ -H "Content-Type: application/json" -d '{"name": "Alice", "email": "a@test.com", "age": 30}'
    curl -X POST http://127.0.0.1:8000/users/ -H "Content-Type: application/json" -d '{"name": "Alice", "email": "a@test.com", "age": 30}'
    # Duplicate email error

    curl http://127.0.0.1:8000/error/not-found
    curl http://127.0.0.1:8000/error/validation
    curl http://127.0.0.1:8000/error/rate-limit
    curl http://127.0.0.1:8000/rate-limited/
    curl http://127.0.0.1:8000/nonexistent  # Custom 404 handler
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)

    r = client.post("/users/", json={"name": "Alice", "email": "a@test.com", "age": 30})
    assert r.status_code == 201

    r = client.post("/users/", json={"name": "Alice2", "email": "a@test.com", "age": 30})
    assert r.status_code == 422  # Duplicate email -> custom business validation
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"

    r = client.post("/users/", json={"name": "Bob", "email": "b@test.com", "age": 999})
    assert r.status_code == 422  # Pydantic validation handler

    r = client.get("/users/999")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "NOT_FOUND"

    r = client.get("/rate-limited/")
    assert r.status_code == 429
    assert r.headers.get("Retry-After") == "60"

    r = client.get("/error/not-found")
    assert r.status_code == 404

    r = client.get("/error/validation")
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"

    r = client.get("/error/rate-limit")
    assert r.status_code == 429
    assert r.json()["error"]["code"] == "RATE_LIMITED"

    r = client.get("/error/division")
    assert r.status_code == 500

    r = client.get("/nonexistent")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "ROUTE_NOT_FOUND"

    r = client.get("/error/unknown-type")
    assert r.status_code == 200
    assert "available_errors" in r.json()

    print("[OK] 23-exception-handling: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
