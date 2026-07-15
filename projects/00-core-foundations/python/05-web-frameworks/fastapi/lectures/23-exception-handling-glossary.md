# Glossary: Exception Handling in FastAPI

## Quick Reference Table

| Term | Definition | Related Terms |
|------|------------|---------------|
| Exception | Error that occurs during program execution | Error, Handler |
| HTTPException | FastAPI exception for HTTP errors | Status Code, Detail |
| Exception Handler | Function that catches and handles exceptions | Decorator, Global |
| Custom Exception | Application-specific exception class | Inheritance, Error |
| Status Code | HTTP response code indicating result | 4xx, 5xx |
| Error Response | JSON response containing error information | JSON, Response |
| Validation Error | Error from invalid input data | Pydantic, Request |
| Global Handler | Handler that catches all exceptions | Middleware, App |
| Logging | Recording exceptions for debugging | Debug, Traceback |
| Raise | Keyword to trigger an exception | Exception, Error |
| Try/Except | Block for catching exceptions | Error Handling |
| Middleware | Component that processes requests/responses | Error Handler |
| Integrity Error | Database constraint violation | Database, SQL |
| 4xx Error | Client-side error (bad request) | Client Error |
| 5xx Error | Server-side error (internal) | Server Error |

---

## Detailed Definitions

### Exception

**Definition**: An error that occurs during program execution, disrupting normal flow.

**Code Example**:
```python
# Built-in exceptions
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Raising exceptions
def get_user(user_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise LookupError(f"User {user_id} not found")
    return user

# Exception hierarchy
"""
BaseException
├── Exception
│   ├── ValueError
│   ├── TypeError
│   ├── AttributeError
│   ├── LookupError
│   │   ├── IndexError
│   │   └── KeyError
│   └── RuntimeError
└── SystemExit
"""
```

**Related Terms**: Error, Raise, Handler

---

### HTTPException

**Definition**: FastAPI's exception class for returning HTTP error responses.

**Code Example**:
```python
from fastapi import HTTPException

# Basic HTTPException
raise HTTPException(status_code=404, detail="Item not found")

# With custom detail
raise HTTPException(
    status_code=400,
    detail={
        "error": "Invalid input",
        "fields": ["email", "password"]
    }
)

# With headers
raise HTTPException(
    status_code=401,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"}
)

# Common status codes
"""
200 - OK
201 - Created
204 - No Content
400 - Bad Request
401 - Unauthorized
403 - Forbidden
404 - Not Found
409 - Conflict
422 - Unprocessable Entity
429 - Too Many Requests
500 - Internal Server Error
503 - Service Unavailable
"""
```

**Related Terms**: Status Code, Detail, Headers

---

### Exception Handler

**Definition**: A function that catches exceptions and returns appropriate responses.

**Code Example**:
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Handler for specific exception
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

# Handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Handler for all exceptions
@app.exception_handler(Exception)
async def general_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

**Related Terms**: Decorator, Exception, Response

---

### Custom Exception

**Definition**: An application-specific exception class for domain-specific errors.

**Code Example**:
```python
# Custom exception classes
class AppException(Exception):
    """Base exception for application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(AppException):
    """Resource not found"""
    def __init__(self, resource: str, id: int):
        super().__init__(
            f"{resource} with id {id} not found",
            status_code=404
        )

class ValidationException(AppException):
    """Validation error"""
    def __init__(self, errors: list):
        super().__init__(
            "Validation failed",
            status_code=422
        )
        self.errors = errors

class ConflictException(AppException):
    """Resource conflict"""
    def __init__(self, message: str):
        super().__init__(message, status_code=409)

# Usage
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException("User", user_id)
    return user
```

**Related Terms**: Inheritance, Exception, Class

---

### Status Code

**Definition**: A three-digit number indicating the result of an HTTP request.

**Code Example**:
```python
from fastapi import HTTPException

# Success codes (2xx)
# 200 - OK
# 201 - Created
# 202 - Accepted
# 204 - No Content

# Client error codes (4xx)
# 400 - Bad Request
# 401 - Unauthorized
# 403 - Forbidden
# 404 - Not Found
# 409 - Conflict
# 422 - Unprocessable Entity
# 429 - Too Many Requests

# Server error codes (5xx)
# 500 - Internal Server Error
# 502 - Bad Gateway
# 503 - Service Unavailable

# Usage
@app.post("/users/")
async def create_user(user: UserCreate):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email required")
    
    if user_exists(user.email):
        raise HTTPException(status_code=409, detail="Email exists")
    
    # Create user...
    return {"status": "created"}  # Implicit 200
```

**Related Terms**: HTTP, Response, Error

---

### Error Response

**Definition**: A JSON response containing error information returned to the client.

**Code Example**:
```python
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

# Error response models
class ErrorDetail(BaseModel):
    field: Optional[str]
    message: str
    type: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorInfo

class ErrorInfo(BaseModel):
    code: int
    message: str
    details: Optional[List[ErrorDetail]] = None

# Example error responses
"""
400 Bad Request:
{
    "success": false,
    "error": {
        "code": 400,
        "message": "Invalid input"
    }
}

422 Validation Error:
{
    "success": false,
    "error": {
        "code": 422,
        "message": "Validation error",
        "details": [
            {
                "field": "email",
                "message": "field required",
                "type": "value_error.missing"
            }
        ]
    }
}

500 Server Error:
{
    "success": false,
    "error": {
        "code": 500,
        "message": "Internal server error"
    }
}
"""
```

**Related Terms**: JSON, Response, Error

---

### Validation Error

**Definition**: An error that occurs when input data doesn't match expected schema.

**Code Example**:
```python
from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

# FastAPI automatically returns 422 for validation errors
@app.post("/users/")
async def create_user(user: UserCreate):
    return user

# Custom validation error handling
@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": 422,
                "message": "Validation error",
                "details": errors
            }
        }
    )
```

**Related Terms**: Pydantic, Request, Schema

---

### Global Handler

**Definition**: An exception handler that catches exceptions across the entire application.

**Code Example**:
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

# Global handler for all exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal server error"
            }
        }
    )

# Global handler for specific exceptions
@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database error: {exc}")
    
    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error": {
                "code": 503,
                "message": "Database temporarily unavailable"
            }
        }
    )
```

**Related Terms**: Middleware, Exception, App

---

### Logging

**Definition**: Recording exceptions and errors for debugging and monitoring.

**Code Example**:
```python
import logging
from fastapi import Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log exceptions
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting item {item_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error")

# Log with context
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

**Related Terms**: Debug, Traceback, Error

---

### Raise

**Definition**: A keyword that triggers an exception.

**Code Example**:
```python
# Raising built-in exceptions
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Raising HTTPException
from fastapi import HTTPException

def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Raising custom exceptions
class InsufficientFunds(Exception):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient funds: {balance} < {amount}")

def withdraw(balance: float, amount: float):
    if amount > balance:
        raise InsufficientFunds(balance, amount)
    return balance - amount

# Re-raising exceptions
def process_payment():
    try:
        charge_card()
    except CardError as e:
        logger.error(f"Card error: {e}")
        raise  # Re-raise the same exception
```

**Related Terms**: Exception, Error, Throw

---

### Try/Except

**Definition**: A block that catches and handles exceptions.

**Code Example**:
```python
# Basic try/except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

# Try/except/else/finally
try:
    user = get_user(user_id)
except UserNotFound:
    return {"error": "User not found"}
else:
    # Runs if no exception
    return user
finally:
    # Always runs
    db.close()

# Multiple exceptions
try:
    process_data()
except ValidationError as e:
    return {"error": "Validation failed", "details": e.errors()}
except DatabaseError as e:
    return {"error": "Database error"}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"error": "Internal error"}

# Exception chaining
try:
    open("file.txt")
except FileNotFoundError as e:
    raise RuntimeError("Failed to load config") from e
```

**Related Terms**: Exception, Error, Handle

---

### Middleware

**Definition**: A component that processes requests and responses, often used for error handling.

**Code Example**:
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )

# Add middleware
app.add_middleware(ErrorHandlerMiddleware)

# Simpler middleware approach
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )
```

**Related Terms**: Handler, Request, Response

---

### Integrity Error

**Definition**: A database error that occurs when a constraint is violated.

**Code Example**:
```python
from sqlalchemy.exc import IntegrityError

@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        return db_user
    except IntegrityError as e:
        db.rollback()
        if "unique" in str(e.orig).lower():
            raise HTTPException(
                status_code=409,
                detail="User already exists"
            )
        elif "foreign key" in str(e.orig).lower():
            raise HTTPException(
                status_code=400,
                detail="Referenced resource not found"
            )
        raise HTTPException(
            status_code=400,
            detail="Database constraint violation"
        )
```

**Related Terms**: Database, Constraint, SQL

---

### 4xx Error

**Definition**: Client-side errors indicating the request is invalid.

**Code Example**:
```python
from fastapi import HTTPException

# 400 Bad Request
@app.get("/items/")
async def get_items(page: int = 1):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be positive")
    return []

# 401 Unauthorized
@app.get("/protected/")
async def protected(user = Depends(get_current_user)):
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {"data": "secret"}

# 403 Forbidden
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, user = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return {"deleted": True}

# 404 Not Found
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# 409 Conflict
@app.post("/users/")
async def create_user(user: UserCreate):
    if user_exists(user.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    return {"created": True}

# 422 Unprocessable Entity
# Automatically raised by FastAPI for validation errors
```

**Related Terms**: Client Error, Request, Validation

---

### 5xx Error

**Definition**: Server-side errors indicating something went wrong on the server.

**Code Example**:
```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

# 500 Internal Server Error
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        return item
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 502 Bad Gateway
@app.get("/external/")
async def get_external():
    try:
        response = await httpx.get("https://api.external.com/data")
        return response.json()
    except Exception as e:
        logger.error(f"External API error: {e}")
        raise HTTPException(status_code=502, detail="Bad gateway")

# 503 Service Unavailable
@app.get("/health/")
async def health_check():
    if not db_is_healthy():
        raise HTTPException(status_code=503, detail="Service unavailable")
    return {"status": "healthy"}
```

**Related Terms**: Server Error, Internal, Database

---

## Common Error Patterns

### Pattern: Result Wrapper
```python
class Result:
    def __init__(self, success: bool, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error
    
    @classmethod
    def ok(cls, data):
        return cls(success=True, data=data)
    
    @classmethod
    def fail(cls, error):
        return cls(success=False, error=error)

# Usage
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        return Result.fail("Item not found")
    return Result.ok(item)
```

### Pattern: Error Codes
```python
class ErrorCode:
    USER_NOT_FOUND = "USER_001"
    EMAIL_EXISTS = "USER_002"
    INVALID_PASSWORD = "USER_003"
    INSUFFICIENT_FUNDS = "PAYMENT_001"

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return JSONResponse(
            status_code=404,
            content={
                "error_code": ErrorCode.USER_NOT_FOUND,
                "message": "User not found"
            }
        )
    return user
```

---

## Summary

Understanding exception handling is crucial for building robust FastAPI applications. Key takeaways:

1. **HTTPException**: Standard for HTTP errors
2. **Custom Exceptions**: Domain-specific error handling
3. **Global Handlers**: Catch exceptions at app level
4. **Status Codes**: Correct codes for different errors
5. **Error Responses**: Consistent JSON format
6. **Logging**: Record errors for debugging
7. **Don't Expose Internals**: Hide server details

**Next**: Move to the API router lecture for endpoint organization.
