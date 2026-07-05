# Lecture 23: Exception Handling in FastAPI

## Overview

Exception handling is crucial for building robust applications that gracefully handle errors and provide meaningful feedback to users. This lecture covers FastAPI's exception handling mechanisms, custom exception classes, global error handlers, and best practices for error management.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Handle exceptions in FastAPI endpoints
2. Create custom exception classes
3. Implement global exception handlers
4. Use HTTPException for API errors
5. Handle validation errors properly
6. Log exceptions for debugging
7. Return consistent error responses
8. Implement error handling middleware

---

## Key Concepts

### 1. Exception Handling in FastAPI

FastAPI provides several ways to handle exceptions:

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Method 1: Try/except in endpoint
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        item = get_item_from_db(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error")

# Method 2: Exception handler decorator
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

# Method 3: Custom exception class
class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Item {exc.item_id} not found"}
    )
```

### 2. HTTPException

The standard way to raise HTTP errors in FastAPI:

```python
from fastapi import HTTPException

# Basic HTTPException
raise HTTPException(status_code=404, detail="Not found")

# With headers
raise HTTPException(
    status_code=401,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"}
)

# With custom detail
raise HTTPException(
    status_code=422,
    detail={
        "error": "Validation failed",
        "fields": ["email", "password"]
    }
)
```

---

## Code Examples

### Example 1: Custom Exception Classes

```python
# exceptions.py
from fastapi import HTTPException
from typing import Any, Optional

class AppException(HTTPException):
    """Base application exception"""
    def __init__(
        self,
        status_code: int,
        detail: Any,
        headers: Optional[dict] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(AppException):
    """Resource not found"""
    def __init__(self, resource: str, resource_id: Any):
        detail = f"{resource} with id {resource_id} not found"
        super().__init__(status_code=404, detail=detail)

class BadRequestException(AppException):
    """Invalid request"""
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class UnauthorizedException(AppException):
    """Authentication required"""
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=401,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(AppException):
    """Permission denied"""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(status_code=403, detail=detail)

class ConflictException(AppException):
    """Resource conflict"""
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)

class RateLimitException(AppException):
    """Rate limit exceeded"""
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(retry_after)}
        )

class ValidationException(AppException):
    """Validation error"""
    def __init__(self, errors: list):
        super().__init__(
            status_code=422,
            detail={"errors": errors}
        )

# Domain-specific exceptions
class UserNotFoundException(NotFoundException):
    def __init__(self, user_id: int):
        super().__init__("User", user_id)

class EmailAlreadyExistsException(ConflictException):
    def __init__(self, email: str):
        super().__init__(f"Email {email} already exists")

class InsufficientFundsException(BadRequestException):
    def __init__(self, balance: float, amount: float):
        super().__init__(
            f"Insufficient funds: balance {balance}, requested {amount}"
        )
```

### Example 2: Global Exception Handlers

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global exception handler for custom exceptions
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException: {exc.detail}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )

# Handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation error: {errors}")
    
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

# Handler for HTTP exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )

# Handler for unexpected exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
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
```

### Example 3: Endpoint with Exception Handling

```python
# routes/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if email exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise EmailAlreadyExistsException(user.email)
        
        # Create user
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {"success": True, "data": db_user}
        
    except AppException:
        raise  # Re-raise our exceptions
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise UserNotFoundException(user_id)
    
    return {"success": True, "data": user}

@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise UserNotFoundException(user_id)
    
    # Update fields
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        if "email" in str(e):
            raise EmailAlreadyExistsException(user_update.email)
        raise
    
    return {"success": True, "data": user}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise UserNotFoundException(user_id)
    
    db.delete(user)
    db.commit()
    
    return {"success": True, "message": f"User {user_id} deleted"}
```

### Example 4: Error Response Models

```python
# schemas/errors.py
from pydantic import BaseModel
from typing import List, Optional, Any

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    type: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorInfo

class ErrorInfo(BaseModel):
    code: int
    message: str
    details: Optional[List[ErrorDetail]] = None

class ValidationErrorResponse(BaseModel):
    success: bool = False
    error: ErrorInfo

# Usage in endpoints
@router.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    # On success
    return {"success": True, "data": item}
    
# On error (automatic with exceptions)
# {
#     "success": false,
#     "error": {
#         "code": 422,
#         "message": "Validation error",
#         "details": [
#             {
#                 "field": "name",
#                 "message": "Field required",
#                 "type": "missing"
#             }
#         ]
#     }
# }
```

### Example 5: Exception Handling Middleware

```python
# middleware/error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
import logging

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
            
        except Exception as e:
            # Log the full traceback
            logger.error(
                f"Unhandled exception: {str(e)}\n"
                f"Traceback: {traceback.format_exc()}"
            )
            
            # Return JSON error response
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "code": 500,
                        "message": "Internal server error",
                        "request_id": request.state.request_id
                    }
                }
            )

# Add to app
app.add_middleware(ErrorHandlerMiddleware)

# Request ID middleware (for tracking)
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    import uuid
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response
```

### Example 6: Database Exception Handling

```python
# database/exceptions.py
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    ProgrammingError
)
from fastapi import HTTPException

def handle_database_error(e: Exception):
    """Convert database exceptions to HTTP exceptions"""
    
    if isinstance(e, IntegrityError):
        # Handle constraint violations
        if "unique" in str(e.orig).lower():
            raise HTTPException(
                status_code=409,
                detail="Resource already exists"
            )
        elif "foreign key" in str(e.orig).lower():
            raise HTTPException(
                status_code=400,
                detail="Referenced resource not found"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Data integrity error"
            )
    
    elif isinstance(e, OperationalError):
        # Handle connection/query errors
        logger.error(f"Database operational error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable"
        )
    
    elif isinstance(e, ProgrammingError):
        # Handle SQL errors
        logger.error(f"SQL error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    
    else:
        # Unknown database error
        logger.error(f"Unknown database error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# Usage in CRUD operations
def create_item(db: Session, item: ItemCreate):
    try:
        db_item = Item(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        handle_database_error(e)
```

---

## Common Mistakes to Avoid

### 1. Exposing Internal Errors

```python
# BAD: Exposing database details
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        # Exposes internal error details!
        raise HTTPException(status_code=500, detail=str(e))

# GOOD: Generic error message
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 2. Catching Too Broadly

```python
# BAD: Catching everything
@app.post("/users/")
async def create_user(user: UserCreate):
    try:
        # ... create user
        return user
    except Exception:  # Too broad!
        raise HTTPException(status_code=500)

# GOOD: Catch specific exceptions
@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        return db_user
    except IntegrityError as e:
        db.rollback()
        if "email" in str(e):
            raise HTTPException(status_code=409, detail="Email already exists")
        raise HTTPException(status_code=400, detail="Database constraint error")
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 3. Not Logging Exceptions

```python
# BAD: No logging
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        item = get_item(item_id)
        return item
    except Exception:
        raise HTTPException(status_code=500)

# GOOD: Log exceptions
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        item = get_item(item_id)
        return item
    except Exception as e:
        logger.error(f"Error getting item {item_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Best Practices

1. **Use Custom Exceptions**: Create meaningful exception classes
2. **Global Handlers**: Handle exceptions at the application level
3. **Consistent Responses**: Return standardized error formats
4. **Log Exceptions**: Always log for debugging
5. **Don't Expose Internals**: Hide database/server details from users
6. **Handle Database Errors**: Convert to appropriate HTTP errors
7. **Use Status Codes Correctly**: 4xx for client errors, 5xx for server errors
8. **Provide Helpful Messages**: Help users understand what went wrong
9. **Test Exception Paths**: Include error scenarios in tests
10. **Document Error Responses**: API docs should show error formats

---

## Error Response Format

```json
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
```

---

## Practice Exercises

### Exercise 1: Custom Exceptions
Create custom exceptions for an e-commerce API:
- ProductNotFoundException
- InsufficientStockException
- OrderAlreadyPaidException

### Exercise 2: Global Handlers
Implement global exception handlers for:
- Validation errors
- Database errors
- Authentication errors
- Rate limiting

### Exercise 3: Error Logging
Set up comprehensive error logging:
- Log all exceptions
- Include request context
- Stack traces for debugging
- Error aggregation

---

## Summary

- Use custom exceptions for meaningful errors
- Implement global exception handlers
- Return consistent error responses
- Log exceptions for debugging
- Don't expose internal details
- Handle database errors properly
- Test error scenarios

**Next Lecture**: We'll explore API routers for organizing endpoints.
