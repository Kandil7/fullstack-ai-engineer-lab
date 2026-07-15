"""
09 - Dependency Injection
===========================
Dependency Injection (DI) is a pattern where FastAPI "injects" dependencies
into your path operation functions. Common uses: database sessions,
authentication, shared logic, and configuration.

Run: uvicorn 09-dependency-injection:app --reload
"""

from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="Dependency Injection in FastAPI")


# ----- Simple dependency function -----
def get_common_query():
    """Common query parameters extracted as a dependency."""
    return {"skip": 0, "limit": 10, "sort": "name"}


@app.get("/items/")
def list_items(common: dict = Depends(get_common_query)):
    """
    FastAPI calls get_common_query() and passes the result to 'common'.
    This keeps shared logic DRY across multiple endpoints.
    """
    return {"filters": common, "items": ["item1", "item2"]}


# ----- Dependency with parameters -----
def get_pagination(skip: int = 0, limit: int = 10):
    """Reusable pagination dependency."""
    return {"skip": skip, "limit": limit}


@app.get("/products/")
def list_products(pagination: dict = Depends(get_pagination)):
    """Products endpoint reusing pagination dependency."""
    return {"pagination": pagination, "products": []}


@app.get("/categories/")
def list_categories(pagination: dict = Depends(get_pagination)):
    """Categories endpoint also reusing pagination dependency."""
    return {"pagination": pagination, "categories": []}


# ----- Authentication dependency -----
def verify_token(authorization: str = Header(...)) -> str:
    """
    Dependency that checks for an Authorization header.
    Returns the token if valid, raises 401 if not.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    if token != "valid-token-123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token


@app.get("/protected/")
def protected_endpoint(token: str = Depends(verify_token)):
    """Endpoint that requires authentication."""
    return {"message": "Access granted", "token": token[:10] + "..."}


# ----- Chained dependencies -----
def get_db_session():
    """Simulated database session dependency."""
    session = {"connected": True, "created_at": datetime.now().isoformat()}
    try:
        yield session  # Use yield for cleanup dependencies
    finally:
        session["connected"] = False  # Cleanup


def get_current_user(db: dict = Depends(get_db_session)):
    """Depends on get_db_session — chained dependency."""
    if not db["connected"]:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"user_id": 1, "username": "alice", "db_session": db}


@app.get("/my-profile/")
def get_profile(user: dict = Depends(get_current_user)):
    """Chained: get_db_session → get_current_user → get_profile."""
    return {"user": user["username"], "db_connected": user["db_session"]["connected"]}


# ----- Class-based dependency -----
class QueryParams:
    """
    Class-based dependency.
    FastAPI instantiates it once per request.
    """
    def __init__(self, q: str = "", page: int = 1, per_page: int = 20):
        self.q = q
        self.page = max(1, page)
        self.per_page = min(max(1, per_page), 100)
        self.offset = (self.page - 1) * self.per_page


@app.get("/search/")
def search(params: QueryParams = Depends()):
    """Class-based dependency for complex parameter handling."""
    return {
        "query": params.q,
        "page": params.page,
        "per_page": params.per_page,
        "offset": params.offset,
    }


# ----- Dependency with yield (lifecycle) -----
def get_cache():
    """Simulated cache with lifecycle management."""
    cache = {}
    print("Cache initialized")
    try:
        yield cache  # Cache is available during request
    finally:
        cache.clear()
        print("Cache cleared")


@app.get("/cached-data/")
def get_cached_data(cache: dict = Depends(get_cache)):
    """Demonstrates yield-based dependency with cleanup."""
    if "data" not in cache:
        cache["data"] = {"computed": True, "timestamp": datetime.now().isoformat()}
    return {"cached": True, "data": cache["data"]}


# ----- Override dependencies for testing -----
def fake_get_db():
    """Fake dependency for testing — no real DB needed."""
    return {"connected": True, "test": True}


# You can override dependencies at the app or router level
# app.dependency_overrides[get_db_session] = fake_get_db


# ----- Multiple dependencies on one endpoint -----
def verify_api_key(x_api_key: str = Header(...)):
    """API key verification dependency."""
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key


@app.get("/admin/stats/")
def admin_stats(
    token: str = Depends(verify_token),
    api_key: str = Depends(verify_api_key),
    db: dict = Depends(get_db_session),
):
    """Multiple dependencies: auth + API key + DB session."""
    return {
        "authorized": True,
        "api_key_valid": True,
        "db_connected": db["connected"],
        "stats": {"users": 42, "orders": 1337},
    }


"""
Testing with curl:
    curl http://127.0.0.1:8000/items/
    curl "http://127.0.0.1:8000/products/?skip=5&limit=5"
    curl -H "Authorization: Bearer valid-token-123" http://127.0.0.1:8000/protected/
    curl http://127.0.0.1:8000/my-profile/
    curl "http://127.0.0.1:8000/search?q=fastapi&page=2&per_page=10"
    curl http://127.0.0.1:8000/cached-data/
    curl -H "Authorization: Bearer valid-token-123" -H "X-Api-Key: my-secret-key" http://127.0.0.1:8000/admin/stats/
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
