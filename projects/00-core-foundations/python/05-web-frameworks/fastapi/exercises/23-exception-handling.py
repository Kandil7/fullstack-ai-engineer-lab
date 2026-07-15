"""
Exercise 23: Exception Handling in FastAPI

Master custom exceptions, handlers, and error response patterns.
Topics: HTTPException, custom exceptions, exception handlers, error logging.

Prerequisites:
- FastAPI basics
- Python exception handling
- HTTP status codes

Estimated time: 45-60 minutes
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import logging
import traceback
import time
import asyncio
import random

app = FastAPI(title="Exception Handling Exercises")


# ============================================================
# Exercise 23.1: Custom Exception Classes
# ============================================================

class BankingError(Exception):
    """Base exception for all banking errors."""
    status_code: int = 500
    error_code: str = "BANKING_ERROR"
    message: str = "An unexpected banking error occurred"

    def __init__(self, message: str = None, **context):
        self.message = message or self.__class__.message
        self.context = context
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.error_code}] {self.message}"


class InsufficientFundsError(BankingError):
    status_code: int = 400
    error_code: str = "INSUFFICIENT_FUNDS"
    message: str = "Insufficient funds for this transaction"

    def __init__(self, amount: float, available: float):
        self.amount = amount
        self.available = available
        self.required = amount - available
        super().__init__(
            message=f"Need ${self.required:.2f} more",
            amount=amount, available=available, required=self.required
        )


class AccountNotFoundError(BankingError):
    status_code: int = 404
    error_code: str = "ACCOUNT_NOT_FOUND"
    message: str = "Account not found"

    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(message=f"Account {account_id} not found", account_id=account_id)


class AccountFrozenError(BankingError):
    status_code: int = 403
    error_code: str = "ACCOUNT_FROZEN"
    message: str = "Account is frozen"

    def __init__(self, account_id: str, reason: str):
        self.account_id = account_id
        self.reason = reason
        super().__init__(
            message=f"Account {account_id} is frozen: {reason}",
            account_id=account_id, reason=reason
        )


class TransactionLimitError(BankingError):
    status_code: int = 400
    error_code: str = "TRANSACTION_LIMIT"
    message: str = "Transaction exceeds limit"

    def __init__(self, limit: float, attempted: float):
        self.limit = limit
        self.attempted = attempted
        super().__init__(
            message=f"Transaction ${attempted:.2f} exceeds limit of ${limit:.2f}",
            limit=limit, attempted=attempted
        )


class AuthenticationError(BankingError):
    status_code: int = 401
    error_code: str = "AUTHENTICATION_ERROR"
    message: str = "Authentication failed"

    def __init__(self, message: str = None):
        super().__init__(message=message or "Authentication failed")


class AuthorizationError(BankingError):
    status_code: int = 403
    error_code: str = "AUTHORIZATION_ERROR"
    message: str = "Not authorized"

    def __init__(self, action: str, role: str):
        self.action = action
        self.role = role
        super().__init__(
            message=f"Role '{role}' cannot perform '{action}'",
            action=action, role=role
        )


# ============================================================
# Exercise 23.2: Exception Handler Registration
# ============================================================

@app.exception_handler(BankingError)
async def banking_error_handler(request: Request, exc: BankingError):
    """Handle all BankingError subclasses with a consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.context,
                "status": exc.status_code,
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request.headers.get("x-request-id", "unknown"),
            }
        }
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions gracefully without exposing internals."""
    # Log full error for debugging
    print(f"[CRITICAL] Unhandled exception: {type(exc).__name__}: {exc}")
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "status": 500,
                "timestamp": datetime.utcnow().isoformat(),
            }
        }
    )


# ============================================================
# Exercise 23.3: Validation Error Formatting
# ============================================================

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, pattern=r"^[a-zA-Z0-9_]+$")
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(..., ge=0, le=150)
    password: str = Field(..., min_length=8)
    bio: Optional[str] = Field(None, max_length=500)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Custom validation error handler with user-friendly field messages."""
    errors = {}
    for error in exc.errors():
        # Extract field name from loc tuple
        field_parts = [str(loc) for loc in error["loc"] if loc not in ("body", "query", "path", "header")]
        field = ".".join(field_parts) if field_parts else str(error["loc"][-1])

        # Convert error type to user-friendly message
        error_type = error.get("type", "")
        msg = error.get("msg", "Invalid value")

        errors[field] = msg

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "fields": errors,
                "status": 422,
                "timestamp": datetime.utcnow().isoformat(),
            }
        }
    )


@app.post("/users/register")
async def register_user(user: UserRegistration):
    """Register a new user with validation."""
    return {
        "message": "User registered successfully",
        "user": {
            "username": user.username,
            "email": user.email,
            "age": user.age,
        }
    }


# ============================================================
# Exercise 23.4: Error Recovery Patterns
# ============================================================

# --- Retry with Fallback ---
async def unstable_operation() -> dict:
    """Simulate an operation that fails 60% of the time."""
    await asyncio.sleep(0.1)
    if random.random() < 0.6:
        raise ConnectionError("Service temporarily unavailable")
    return {"status": "success", "data": "Operation completed"}


async def fallback_operation() -> dict:
    """Fallback that always succeeds."""
    await asyncio.sleep(0.2)
    return {"status": "fallback", "data": "Fallback data used"}


@app.get("/resilient/retry")
async def retry_with_fallback():
    """Try operation up to 3 times, then use fallback."""
    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            result = await unstable_operation()
            return {**result, "attempts": attempt + 1, "strategy": "primary"}
        except Exception as e:
            last_error = str(e)
            await asyncio.sleep(0.1 * (attempt + 1))  # Exponential backoff

    # Fallback
    fallback = await fallback_operation()
    return {**fallback, "error": last_error, "attempts": max_retries, "strategy": "fallback"}


# --- Circuit Breaker ---
class CircuitBreaker:
    """Simple circuit breaker pattern implementation."""

    def __init__(self, failure_threshold: int = 3, reset_timeout: int = 30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed, open, half-open

    async def call(self, func, *args, **kwargs):
        now = time.time()

        if self.state == "open":
            if self.last_failure_time and (now - self.last_failure_time) > self.reset_timeout:
                self.state = "half-open"
                print(f"[CircuitBreaker] State: closed -> half-open (timeout elapsed)")
            else:
                raise HTTPException(
                    status_code=503,
                    detail={
                        "message": "Service temporarily unavailable",
                        "circuit_state": "open",
                        "retry_after_seconds": int(self.reset_timeout - (now - self.last_failure_time)) if self.last_failure_time else self.reset_timeout
                    }
                )

        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
                print(f"[CircuitBreaker] State: half-open -> closed (success)")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                print(f"[CircuitBreaker] State: closed -> open (failures: {self.failure_count})")
            raise


circuit_breaker = CircuitBreaker(failure_threshold=3, reset_timeout=30)


async def fragile_service() -> dict:
    """Simulate a service that fails frequently."""
    await asyncio.sleep(0.1)
    if random.random() < 0.7:  # 70% failure rate
        raise RuntimeError("Service failure")
    return {"status": "ok", "data": "from fragile service"}


@app.get("/resilient/circuit")
async def circuit_breaker_endpoint():
    """Endpoint protected by circuit breaker."""
    try:
        result = await circuit_breaker.call(fragile_service)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Graceful Degradation ---
cache_store: dict = {}


def get_cached_response(key: str) -> Optional[dict]:
    """Get cached response if available and not expired."""
    cached = cache_store.get(key)
    if cached:
        if time.time() < cached.get("expires_at", 0):
            return cached["data"]
    return None


def set_cached_response(key: str, data: dict, ttl: int = 60):
    """Cache a response with TTL."""
    cache_store[key] = {
        "data": data,
        "expires_at": time.time() + ttl
    }


@app.get("/resilient/degraded")
async def graceful_degradation():
    """Try best quality, fall back to cache, then default."""
    cache_key = "resilient_data"

    # Try primary source
    try:
        result = await unstable_operation()
        set_cached_response(cache_key, result)
        return {**result, "quality": "full", "source": "primary"}
    except Exception:
        pass

    # Try cache
    cached = get_cached_response(cache_key)
    if cached:
        return {**cached, "quality": "degraded", "source": "cache"}

    # Default response
    return {
        "status": "default",
        "data": "Default fallback data",
        "quality": "minimal",
        "source": "default"
    }


# ============================================================
# Exercise 23.5: Structured Error Logging
# ============================================================

# Configure structured logger
logger = logging.getLogger("api.errors")
logger.setLevel(logging.DEBUG)

# Add console handler with formatting
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def log_error(
    error: Exception,
    request: Request = None,
    user_id: str = None,
    extra_context: dict = None
) -> dict:
    """Create structured error log entry with context."""
    log_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "path": request.url.path if request else "unknown",
        "method": request.method if request else "unknown",
        "client_ip": request.client.host if request and request.client else "unknown",
        "user_id": user_id or "anonymous",
        "timestamp": datetime.utcnow().isoformat(),
        **(extra_context or {})
    }
    return log_data


@app.get("/test/validation")
async def test_validation(field: str = "default"):
    """Returns a validation error (logged at DEBUG level)."""
    if field == "bad":
        error = ValueError("Invalid field value")
        data = log_error(error, extra_context={"field": field})
        logger.debug(f"Validation error: {data}")
        raise HTTPException(status_code=400, detail=str(error))
    return {"field": field, "status": "valid"}


@app.get("/test/business")
async def test_business(account: str = "ACC-001"):
    """Returns a business logic error (logged at WARNING level)."""
    error = InsufficientFundsError(amount=100, available=30)
    data = log_error(error, extra_context={"account": account})
    logger.warning(f"Business error: {data}")
    raise error


@app.get("/test/system")
async def test_system():
    """Returns a system error (logged at ERROR level)."""
    try:
        raise RuntimeError("Database connection pool exhausted")
    except Exception as e:
        data = log_error(e, extra_context={"db_pool_size": 10, "active_connections": 10})
        logger.error(f"System error: {data}")
        raise HTTPException(status_code=500, detail="Internal system error")


@app.get("/test/security")
async def test_security(token: str = Header(default="")):
    """Returns a security error (logged at CRITICAL level)."""
    if not token or token == "invalid":
        error = AuthenticationError("Invalid authentication token")
        data = log_error(error, extra_context={"token_preview": token[:10] + "..." if token else "empty"})
        logger.critical(f"Security error: {data}")
        raise error
    return {"status": "authenticated", "token_valid": True}
