"""
FastAPI Exercise 09 - Dependency Injection
===========================================

Topics covered:
- Using Depends() for dependency injection
- Dependency functions and classes
- Sub-dependencies (dependencies that depend on other dependencies)
- Overriding dependencies for testing
- Yield dependencies (for cleanup/teardown)

Requirements:
    pip install fastapi uvicorn

Run any exercise:
    uvicorn 09-dependency-injection:app1 --reload
    uvicorn 09-dependency-injection:app2 --reload
    uvicorn 09-dependency-injection:app3 --reload
"""

from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Exercise 1: Basic Dependency Injection
# =============================================================================

app1 = FastAPI(title="Exercise 9.1 - Basic Dependency Injection")


def get_current_user(user_id: Optional[str] = Header(default=None)):
    """Dependency that extracts and validates user from header."""
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing X-User-Id header")
    return {"user_id": user_id, "role": "user"}


@app1.get("/profile")
def get_profile(user: dict = Depends(get_current_user)):
    """Return user profile using dependency injection."""
    return {"profile": user}


@app1.get("/dashboard")
def get_dashboard(user: dict = Depends(get_current_user)):
    """Return dashboard welcome using dependency injection."""
    return {"dashboard": f"Welcome, user {user['user_id']}"}


# =============================================================================
# Exercise 2: Sub-Dependencies and Chained Dependencies
# =============================================================================

app2 = FastAPI(title="Exercise 9.2 - Sub-Dependencies")

TOKEN_DB = {
    "admin-token": {"user_id": "admin-001", "role": "admin"},
    "user-token": {"user_id": "user-123", "role": "user"},
}


def get_auth_token(authorization: Optional[str] = Header(default=None)):
    """Extract Bearer token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    return authorization.replace("Bearer ", "")


def validate_token(token: str = Depends(get_auth_token)):
    """Validate token and return user info."""
    if token not in TOKEN_DB:
        raise HTTPException(status_code=401, detail="Invalid token")
    return TOKEN_DB[token]


def require_admin(user: dict = Depends(validate_token)):
    """Ensure user has admin role."""
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@app2.get("/public")
def public_endpoint():
    """Public endpoint - no authentication required."""
    return {"message": "Public endpoint"}


@app2.get("/user-info")
def user_info(user: dict = Depends(validate_token)):
    """Protected endpoint - returns user info from token."""
    return user


@app2.get("/admin-panel")
def admin_panel(user: dict = Depends(require_admin)):
    """Admin-only endpoint - requires admin role."""
    return {"message": "Welcome to admin panel", "admin": user}


# =============================================================================
# Exercise 3: Yield Dependencies and Overriding
# =============================================================================

app3 = FastAPI(title="Exercise 9.3 - Yield Dependencies")


def get_database():
    """Yield database connection with cleanup."""
    db = {"type": "real", "connection_id": "db-001"}
    logger.info("Database connection opened")
    yield db
    logger.info("Database connection closed")


def get_db_session(db: dict = Depends(get_database)):
    """Yield database session with cleanup."""
    session = {"id": "session-001", "db": db}
    logger.info("Session started")
    yield session
    logger.info("Session closed")


@app3.get("/items")
def list_items(session: dict = Depends(get_db_session)):
    """List items using database session dependency."""
    return {"items": [], "session_id": session["id"]}


@app3.post("/items")
def create_item(session: dict = Depends(get_db_session), name: str = ""):
    """Create an item using database session dependency."""
    return {"created": True, "name": name}


# Test app with overridden dependency
test_app = FastAPI()
test_app.dependency_overrides[get_database] = lambda: {"type": "mock", "connection_id": "mock-db"}


@test_app.get("/items")
def test_list_items(session: dict = Depends(get_db_session)):
    """Test endpoint that uses mock database."""
    return {"items": [], "session_id": session["id"], "db_type": session["db"]["type"]}
