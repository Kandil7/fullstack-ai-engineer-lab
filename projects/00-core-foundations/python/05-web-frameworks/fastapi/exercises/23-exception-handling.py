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
from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum

app = FastAPI(title="Exception Handling Exercises")

# ============================================================
# Exercise 23.1: Custom Exception Classes
# ============================================================
"""
Problem:
    Create a hierarchy of custom exceptions for a banking application.

Exception hierarchy:
    BankingError (base)
        InsufficientFundsError(amount, available, required)
        AccountNotFoundError(account_id)
        AccountFrozenError(account_id, reason)
        TransactionLimitError(limit, attempted)
        AuthenticationError(message)
        AuthorizationError(action, role)

Requirements:
    1. Each exception stores relevant context data
    2. Each exception has a unique error code
    3. Each exception has a user-friendly message
    4. Exceptions include HTTP status codes

Exception skeleton:
    class BankingError(Exception):
        status_code: int = 500
        error_code: str = "BANKING_ERROR"
        message: str = "An unexpected banking error occurred"

        def __init__(self, message: str = None, **context):
            self.message = message or self.__class__.message
            self.context = context
            super().__init__(self.message)

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
                amount=amount, available=available
            )

Hints:
    - Inherit from Exception for custom exceptions
    - Override __init__ to store context data
    - Use class-level attributes for defaults
    - Include __str__ for readable error messages
    - Consider using dataclasses for exception data

Test cases:
    # Insufficient funds
    raise InsufficientFundsError(amount=100, available=50)
    -> message: "Need $50.00 more"
    -> status_code: 400
    -> error_code: "INSUFFICIENT_FUNDS"

    # Account not found
    raise AccountNotFoundError(account_id="ACC-123")
    -> message: "Account ACC-123 not found"
    -> status_code: 404

    # Account frozen
    raise AccountFrozenError(account_id="ACC-456", reason="Suspicious activity")
    -> message: "Account ACC-456 is frozen: Suspicious activity"
    -> status_code: 403
"""

# TODO: Define your exception classes below


# ============================================================
# Exercise 23.2: Exception Handler Registration
# ============================================================
"""
Problem:
    Register global exception handlers for your custom exceptions.

Requirements:
    1. Register handlers for each custom exception
    2. Return consistent JSON error responses
    3. Include error codes for client-side handling
    4. Log errors with appropriate severity
    5. Handle unexpected exceptions gracefully

Error response format:
    {
        "error": {
            "code": "INSUFFICIENT_FUNDS",
            "message": "Need $50.00 more",
            "details": {
                "amount": 100,
                "available": 50,
                "required": 50
            },
            "status": 400,
            "timestamp": "2024-01-15T10:30:00Z",
            "request_id": "req-abc-123"
        }
    }

Handler registration:
    @app.exception_handler(BankingError)
    async def banking_error_handler(request: Request, exc: BankingError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.context,
                    "status": exc.status_code,
                }
            }
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        # Log the full error for debugging
        # Return a generic message to the client
        pass

Hints:
    - Use @app.exception_handler(ExceptionClass) decorator
    - Return JSONResponse with appropriate status_code
    - Use datetime.utcnow().isoformat() for timestamps
    - For generic errors, log exc details but don't expose internals
    - Consider adding request ID middleware for tracing

Test cases:
    # Custom exception returns formatted error
    GET /bank/withdraw
    -> 400 {
        "error": {
            "code": "INSUFFICIENT_FUNDS",
            "message": "Need $50.00 more",
            "details": {"amount": 100, "available": 50},
            "status": 400
        }
    }

    # Generic exception returns safe error
    GET /bank/crash
    -> 500 {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
            "status": 500
        }
    }
"""

# TODO: Register your exception handlers below


# ============================================================
# Exercise 23.3: Validation Error Formatting
# ============================================================
"""
Problem:
    Customize Pydantic validation error responses.

Default Pydantic errors look like:
    {"detail": [{"loc": ["body", "field"], "msg": "...", "type": "..."}]}

Create a better format:
    {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "status": 422,
            "fields": {
                "email": "Invalid email format",
                "age": "Must be between 0 and 150",
                "name": "Field required"
            }
        }
    }

Requirements:
    1. Catch RequestValidationError (from fastapi.exceptions)
    2. Convert field errors to user-friendly messages
    3. Group errors by field name
    4. Handle both body and query param errors
    5. Handle missing fields gracefully

Request model for testing:
    class UserRegistration(BaseModel):
        username: str          # min 3 chars, alphanumeric
        email: str             # valid email format
        age: int               # 0-150
        password: str          # min 8 chars
        bio: Optional[str] = None  # max 500 chars

Handler:
    from fastapi.exceptions import RequestValidationError

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        errors = {}
        for error in exc.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            # Simplify field name (remove "body." prefix)
            field = field.replace("body.", "")
            errors[field] = message
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "fields": errors,
                    "status": 422
                }
            }
        )

Hints:
    - from fastapi.exceptions import RequestValidationError
    - exc.errors() returns list of error dicts
    - Each error has: loc, msg, type, ctx (optional)
    - loc is a tuple like ("body", "field") or ("query", "param")
    - Use error["type"] to create contextual messages

Test cases:
    # Missing required fields
    POST /users/register {}
    -> 422 {
        "error": {
            "code": "VALIDATION_ERROR",
            "fields": {
                "username": "Field required",
                "email": "Field required",
                "age": "Field required",
                "password": "Field required"
            }
        }
    }

    # Invalid field values
    POST /users/register {"username": "ab", "email": "bad", "age": -5, "password": "short"}
    -> 422 {
        "error": {
            "fields": {
                "username": "String should have at least 3 characters",
                "email": "Invalid email format",
                "age": "Must be between 0 and 150",
                "password": "String should have at least 8 characters"
            }
        }
    }
"""

# TODO: Register validation error handler below
# TODO: Create the UserRegistration model


# ============================================================
# Exercise 23.4: Error Recovery Patterns
# ============================================================
"""
Problem:
    Implement error recovery patterns for common failure scenarios.

Patterns to implement:

    1. Retry with fallback:
       - Try operation up to N times
       - On failure, try fallback operation
       - Return best available result

    2. Circuit breaker:
       - Track failure counts per service
       - Open circuit after N failures
       - Reset after timeout
       - Return degraded response when open

    3. Graceful degradation:
       - Try best quality response
       - Fall back to cached response
       - Fall back to default response
       - Never fail completely

Endpoints:
    GET /resilient/data         - Uses retry pattern
    GET /resilient/circuit      - Uses circuit breaker
    GET /resilient/degraded     - Uses graceful degradation

Circuit breaker skeleton:
    class CircuitBreaker:
        def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
            self.failure_count = 0
            self.failure_threshold = failure_threshold
            self.reset_timeout = reset_timeout
            self.last_failure_time = None
            self.state = "closed"  # closed, open, half-open

        async def call(self, func, *args, **kwargs):
            if self.state == "open":
                if time.time() - self.last_failure_time > self.reset_timeout:
                    self.state = "half-open"
                else:
                    raise HTTPException(503, "Service temporarily unavailable")
            try:
                result = await func(*args, **kwargs)
                if self.state == "half-open":
                    self.state = "closed"
                    self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
                raise

Hints:
    - Use asyncio.sleep() for retry delays
    - Use time.time() for circuit breaker timing
    - Cache responses with TTL (time-to-live)
    - Log state transitions for debugging
    - Consider using tenacity library for production retry logic

Test cases:
    # Retry succeeds after transient failure
    GET /resilient/data
    -> 200 {"data": "...", "retries": 2}

    # Circuit breaker opens after failures
    (trigger 5 failures)
    GET /resilient/circuit
    -> 503 {"detail": "Service temporarily unavailable", "circuit_state": "open"}

    # Graceful degradation returns cached data
    GET /resilient/degraded
    (with service down)
    -> 200 {"data": "cached", "quality": "degraded", "source": "cache"}
"""

# TODO: Write resilience patterns below


# ============================================================
# Exercise 23.5: Structured Error Logging
# ============================================================
"""
Problem:
    Implement structured error logging with context.

Requirements:
    1. Create a structured logger for API errors
    2. Include request context (path, method, client IP)
    3. Include user context (authenticated user ID)
    4. Include error context (stack trace, custom data)
    5. Different log levels for different error types

Logger skeleton:
    import logging
    import traceback

    logger = logging.getLogger("api.errors")

    def log_error(
        error: Exception,
        request: Request,
        user_id: str = None,
        extra_context: dict = None
    ):
        log_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "path": request.url.path,
            "method": request.method,
            "client_ip": request.client.host,
            "user_id": user_id,
            "traceback": traceback.format_exc(),
            **(extra_context or {})
        }
        logger.error("API Error", extra={"data": log_data})

Log levels:
    - DEBUG: Validation errors (expected)
    - WARNING: Business logic errors (insufficient funds)
    - ERROR: Unexpected errors (system failures)
    - CRITICAL: Security errors (authentication bypass attempts)

Endpoints:
    GET /test/validation  - Returns validation error (DEBUG level)
    GET /test/business    - Returns business error (WARNING level)
    GET /test/system      - Returns system error (ERROR level)
    GET /test/security    - Returns security error (CRITICAL level)

Hints:
    - Use Python's logging module
    - Use extra={} to attach custom data to log records
    - Use json.dumps() for structured log output
    - Consider using structlog library for production
    - Log correlation IDs for request tracing

Test cases:
    # Validation error logged at DEBUG
    GET /test/validation?field=bad
    -> 400 (response)
    Log: DEBUG validation error, field=bad

    # Security error logged at CRITICAL
    GET /test/security?token=invalid
    -> 401 (response)
    Log: CRITICAL security error, token=invalid
"""

# TODO: Write structured logging code below
