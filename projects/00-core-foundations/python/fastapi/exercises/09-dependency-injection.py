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


# =============================================================================
# Exercise 1: Basic Dependency Injection
# =============================================================================
# Create an app using dependency injection:
#
#   Create a dependency function get_current_user() that:
#       - Reads the X-User-Id header
#       - If missing: raise HTTPException(400, "Missing X-User-Id header")
#       - Return: {"user_id": user_id, "role": "user"}
#
#   Routes:
#   GET /profile
#       - Uses get_current_user dependency
#       - Returns: {"profile": <user dict>}
#
#   GET /dashboard
#       - Uses get_current_user dependency
#       - Returns: {"dashboard": "Welcome, user <id>"}
#
# Hints:
#   - Dependencies are functions that run before the route
#   - Use: def route(dep: dict = Depends(get_current_user))
#   - The return value of the dependency is injected into the route
#   - Use HTTPException for error responses
#   - from fastapi import HTTPException
#
# Expected behavior:
#   GET /profile with X-User-Id: 42
#       -> {"profile": {"user_id": "42", "role": "user"}}
#   GET /profile without header -> 400 error
#   GET /dashboard with header -> {"dashboard": "Welcome, user 42"}
#
# Test with:
#   curl http://localhost:8000/profile -H "X-User-Id: 42"
#   curl http://localhost:8000/profile  # should fail
# =============================================================================

app1 = FastAPI(title="Exercise 9.1 - Basic Dependency Injection")


def get_current_user(user_id: Optional[str] = Header(default=None)):
    """Dependency that extracts and validates user from header."""
    pass  # TODO: Validate header, raise HTTPException if missing, return user dict


@app1.get("/profile")
def get_profile(user: dict = Depends(get_current_user)):
    pass  # TODO: Return {"profile": user}


@app1.get("/dashboard")
def get_dashboard(user: dict = Depends(get_current_user)):
    pass  # TODO: Return {"dashboard": f"Welcome, user {user['user_id']}"}


# =============================================================================
# Exercise 2: Sub-Dependencies and Chained Dependencies
# =============================================================================
# Create an app with layered dependencies:
#
#   get_auth_token() -> reads Authorization header, returns token string
#   validate_token(token: str = Depends(get_auth_token)) -> validates token, returns user info
#   require_admin(user: dict = Depends(validate_token)) -> checks role is "admin"
#
#   Routes:
#   GET /user-info
#       - Uses validate_token
#       - Returns user info
#
#   GET /admin-panel
#       - Uses require_admin (which chains through validate_token -> get_auth_token)
#       - Returns {"message": "Welcome to admin panel", "admin": user}
#
#   GET /public
#       - No dependencies
#       - Returns {"message": "Public endpoint"}
#
# Hints:
#   - Dependencies can depend on other dependencies!
#   - get_auth_token returns str, validate_token takes str, returns dict
#   - require_admin takes dict, checks role, raises 403 if not admin
#   - Chain: route -> require_admin -> validate_token -> get_auth_token
#   - Valid tokens: "admin-token" -> admin, "user-token" -> user
#
# Expected behavior:
#   GET /public -> {"message": "Public endpoint"}
#   GET /user-info with Authorization: Bearer user-token
#       -> {"user_id": "user-123", "role": "user"}
#   GET /admin-panel with Authorization: Bearer admin-token
#       -> {"message": "Welcome to admin panel", ...}
#   GET /admin-panel with Authorization: Bearer user-token
#       -> 403 (not admin)
#
# Test with:
#   curl http://localhost:8000/public
#   curl http://localhost:8000/user-info -H "Authorization: Bearer user-token"
#   curl http://localhost:8000/admin-panel -H "Authorization: Bearer admin-token"
#   curl http://localhost:8000/admin-panel -H "Authorization: Bearer user-token"
# =============================================================================

app2 = FastAPI(title="Exercise 9.2 - Sub-Dependencies")

TOKEN_DB = {
    "admin-token": {"user_id": "admin-001", "role": "admin"},
    "user-token": {"user_id": "user-123", "role": "user"},
}


def get_auth_token(authorization: Optional[str] = Header(default=None)):
    """Extract Bearer token from Authorization header."""
    pass  # TODO: Parse "Bearer <token>", return token or raise 401


def validate_token(token: str = Depends(get_auth_token)):
    """Validate token and return user info."""
    pass  # TODO: Look up token in TOKEN_DB, return user dict or raise 401


def require_admin(user: dict = Depends(validate_token)):
    """Ensure user has admin role."""
    pass  # TODO: Check role == "admin", raise 403 if not


@app2.get("/public")
def public_endpoint():
    pass  # TODO: Return {"message": "Public endpoint"}


@app2.get("/user-info")
def user_info(user: dict = Depends(validate_token)):
    pass  # TODO: Return user dict


@app2.get("/admin-panel")
def admin_panel(user: dict = Depends(require_admin)):
    pass  # TODO: Return {"message": "Welcome to admin panel", "admin": user}


# =============================================================================
# Exercise 3: Yield Dependencies and Overriding
# =============================================================================
# Create an app demonstrating yield dependencies and dependency overriding:
#
#   get_database():
#       - yield a "database connection" (just a dict模拟)
#       - Log "Database connection opened"
#       - After route: log "Database connection closed"
#
#   get_db_session(db: dict = Depends(get_database)):
#       - yield a session object (a dict with db reference)
#       - Log "Session started"
#       - After route: log "Session closed"
#
#   Routes:
#   GET /items
#       - Uses get_db_session
#       - Returns {"items": [], "session_id": session["id"]}
#
#   POST /items
#       - Uses get_db_session
#       - Body: {"name": str}
#       - Returns {"created": true, "name": name}
#
#   Override for testing:
#   test_app = FastAPI()
#   # Override get_database to return mock
#   test_app.dependency_overrides[get_database] = lambda: {"type": "mock"}
#   # Copy routes from app3 to test_app
#
# Hints:
#   - Yield dependencies run code before AND after the route
#   - The code after yield runs after the response is sent
#   - Use: dependency_overrides[dep_func] = mock_func for testing
#   - This is useful for test isolation (no real DB needed)
#
# Expected behavior:
#   GET /items -> logs "opened", "Session started", "Session closed", "closed"
#   POST /items -> same logging pattern
#   Override test -> uses mock database
#
# Test with:
#   curl http://localhost:8000/items
#   curl -X POST http://localhost:8000/items \
#     -H "Content-Type: application/json" \
#     -d '{"name": "Widget"}'
# =============================================================================

app3 = FastAPI(title="Exercise 9.3 - Yield Dependencies")

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    pass  # TODO: Return {"items": [], "session_id": session["id"]}


@app3.post("/items")
def create_item(session: dict = Depends(get_db_session), name: str = ""):
    pass  # TODO: Return {"created": True, "name": name}


# =============================================================================
# TEST APP (for overriding dependencies)
# =============================================================================
# Create a test version of app3 that overrides get_database:
#
# test_app = FastAPI()
# test_app.dependency_overrides[get_database] = lambda: {"type": "mock", "connection_id": "mock-db"}
#
# @test_app.get("/items")
# def test_list_items(session: dict = Depends(get_db_session)):
#     return {"items": [], "session_id": session["id"], "db_type": session["db"]["type"]}
#
# This test app uses a mock database instead of the real one.
# =============================================================================

# TODO: Create test_app with overridden get_database dependency


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 09-dependency-injection:app1 --reload
#    - Test /profile with header -> should work
#    - Test /profile without header -> should return 400
#    - Verify dependency runs for both routes
#
# 2. Run: uvicorn 09-dependency-injection:app2 --reload
#    - Test /public (no deps)
#    - Test /user-info with user-token
#    - Test /admin-panel with admin-token
#    - Test /admin-panel with user-token -> should return 403
#    - Verify dependency chain: token -> user -> admin check
#
# 3. Run: uvicorn 09-dependency-injection:app3 --reload
#    - Test /items and /items POST
#    - Verify log messages show dependency lifecycle
#    - Create test_app and verify it uses mock database
#    - Test dependency overriding for test isolation
# =============================================================================
