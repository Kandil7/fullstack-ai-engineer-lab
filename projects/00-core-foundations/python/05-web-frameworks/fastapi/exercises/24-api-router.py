"""
Exercise 24: APIRouter and Application Structure

Master modular routing and application organization.
Topics: APIRouter, sub-applications, route grouping, middleware per router.

Prerequisites:
- FastAPI basics (exercise 01-04)
- Dependency injection (exercise 15)
- Pydantic models (exercise 03)

Estimated time: 45-60 minutes
"""

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Header, Request
from pydantic import BaseModel
from typing import List
import time
import uuid
import asyncio


# ============================================================
# Exercise 24.1: Basic Router Setup
# ============================================================

app = FastAPI(title="Modular API")

# In-memory databases
users_db: dict = {}
products_db: dict = {}
orders_db: dict = {}

# --- Users Router ---

users_router = APIRouter(prefix="/users", tags=["users"],
                         responses={404: {"description": "Not found"}})


@users_router.get("/")
async def list_users():
    return list(users_db.values())


@users_router.post("/", status_code=201)
async def create_user(user_data: dict):
    user_id = str(len(users_db) + 1)
    users_db[user_id] = {"id": user_id, **user_data}
    return users_db[user_id]


@users_router.get("/{user_id}")
async def get_user(user_id: str):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.delete("/{user_id}")
async def delete_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted"}


# --- Products Router ---

products_router = APIRouter(prefix="/products", tags=["products"],
                            responses={404: {"description": "Not found"}})


@products_router.get("/")
async def list_products():
    return list(products_db.values())


@products_router.post("/", status_code=201)
async def create_product(product: dict):
    product_id = str(len(products_db) + 1)
    products_db[product_id] = {"id": product_id, **product}
    return products_db[product_id]


@products_router.get("/{product_id}")
async def get_product(product_id: str):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.put("/{product_id}")
async def update_product(product_id: str, product: dict):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db[product_id].update(product)
    return products_db[product_id]


# --- Orders Router ---

orders_router = APIRouter(prefix="/orders", tags=["orders"],
                          responses={404: {"description": "Not found"}})


@orders_router.get("/")
async def list_orders():
    return list(orders_db.values())


@orders_router.post("/", status_code=201)
async def create_order(order: dict):
    order_id = str(len(orders_db) + 1)
    orders_db[order_id] = {"id": order_id, "status": "pending", **order}
    return orders_db[order_id]


@orders_router.get("/{order_id}")
async def get_order(order_id: str):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@orders_router.post("/{order_id}/cancel")
async def cancel_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    orders_db[order_id]["status"] = "cancelled"
    return orders_db[order_id]


# Include routers in main app
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)


# ============================================================
# Exercise 24.2: Router Dependencies
# ============================================================

app2 = FastAPI(title="Router Dependencies")

MOCK_USERS = {
    1: {"id": 1, "username": "alice", "role": "admin"},
    2: {"id": 2, "username": "bob", "role": "user"},
    3: {"id": 3, "username": "charlie", "role": "user"},
}

TOKENS = {
    "admin-token": 1,
    "user-token": 2,
    "alice-token": 1,
}


async def get_current_user(authorization: str = Header(default="")):
    """Dependency that extracts and validates the current user from token."""
    token = authorization.replace("Bearer ", "").strip()
    user_id = TOKENS.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    user = MOCK_USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_role(role: str):
    """Factory function creating role-checking dependencies."""
    async def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{role}' required, but user has role '{user['role']}'"
            )
        return user
    return role_checker


# Public router - no auth needed
public_router = APIRouter(prefix="/products", tags=["public"])


@public_router.get("/public")
async def public_products():
    """Public endpoint - no authentication required."""
    return [{"id": 1, "name": "Public Product", "price": 9.99}]


# Users router - auth required
users_router2 = APIRouter(prefix="/users", tags=["users"],
                          dependencies=[Depends(get_current_user)])


@users_router2.get("/me")
async def get_profile(user: dict = Depends(get_current_user)):
    """Get current user's profile."""
    return user


# Admin router - admin role required
admin_router = APIRouter(prefix="/admin", tags=["admin"],
                         dependencies=[Depends(require_role("admin"))])


@admin_router.get("/users")
async def admin_list_users(user: dict = Depends(get_current_user)):
    """Admin-only: list all users."""
    return list(MOCK_USERS.values())


@admin_router.get("/stats")
async def admin_stats():
    """Admin-only: system statistics."""
    return {"total_users": len(MOCK_USERS), "active_sessions": 15}


app2.include_router(public_router)
app2.include_router(users_router2)
app2.include_router(admin_router)


# ============================================================
# Exercise 24.3: Nested Routers (Sub-Applications)
# ============================================================

app3 = FastAPI(title="Nested Routers")

# V1 routers
v1_router = APIRouter(prefix="/api/v1", tags=["v1"])
v2_router = APIRouter(prefix="/api/v2", tags=["v2"])

v1_users = APIRouter(prefix="/users", tags=["users"])
v1_user_addresses = APIRouter(prefix="/{user_id}/addresses", tags=["addresses"])
v1_products = APIRouter(prefix="/products", tags=["products"])
v1_product_reviews = APIRouter(prefix="/{product_id}/reviews", tags=["reviews"])

v2_users = APIRouter(prefix="/users", tags=["users"])

# Sample data
addresses_db: dict = {}
reviews_db: dict = {}

# V1 user address endpoints
@v1_user_addresses.get("/")
async def list_addresses(user_id: int):
    user_addrs = [a for a in addresses_db.values() if a["user_id"] == user_id]
    return user_addrs


@v1_user_addresses.post("/", status_code=201)
async def create_address(user_id: int, address: dict):
    addr_id = str(len(addresses_db) + 1)
    addresses_db[addr_id] = {"id": addr_id, "user_id": user_id, **address}
    return addresses_db[addr_id]


# V1 users
@v1_users.get("/")
async def list_v1_users():
    return [{"id": 1, "name": "Alice", "email": "alice@example.com"}]


@v1_users.get("/{user_id}")
async def get_v1_user(user_id: int):
    return {"id": user_id, "name": "User", "version": "v1"}


# V1 product review endpoints
@v1_product_reviews.get("/")
async def list_reviews(product_id: int):
    product_revs = [r for r in reviews_db.values() if r["product_id"] == product_id]
    return product_revs


@v1_product_reviews.post("/", status_code=201)
async def create_review(product_id: int, review: dict):
    rev_id = str(len(reviews_db) + 1)
    reviews_db[rev_id] = {"id": rev_id, "product_id": product_id, **review}
    return reviews_db[rev_id]


# V1 products
@v1_products.get("/")
async def list_v1_products():
    return [{"id": 1, "name": "Widget", "price": 9.99}]


# V2 users (different format with pagination)
@v2_users.get("/")
async def list_v2_users(page: int = 1, per_page: int = 10):
    return {
        "data": [
            {"id": 1, "username": "alice", "profile_url": "/api/v2/users/1"},
            {"id": 2, "username": "bob", "profile_url": "/api/v2/users/2"},
        ],
        "meta": {"total": 2, "page": page, "per_page": per_page},
        "_links": {"self": f"/api/v2/users?page={page}&per_page={per_page}", "next": None}
    }


# Nest routers
v1_users.include_router(v1_user_addresses)
v1_products.include_router(v1_product_reviews)
v1_router.include_router(v1_users)
v1_router.include_router(v1_products)
v2_router.include_router(v2_users)

app3.include_router(v1_router)
app3.include_router(v2_router)


# ============================================================
# Exercise 24.4: Router-Level Middleware
# ============================================================

app4 = FastAPI(title="Router-Level Middleware")

# Admin router with audit logging middleware
admin_router4 = APIRouter(prefix="/admin", tags=["admin"])


@admin_router4.middleware("http")
async def admin_audit_log(request: Request, call_next):
    """Log all admin requests."""
    response = await call_next(request)
    print(f"[ADMIN AUDIT] {request.method} {request.url.path} -> {response.status_code}")
    return response


@admin_router4.get("/settings")
async def admin_settings():
    return {"settings": {"feature_x": True, "debug_mode": False}}


# Public router with rate limiting middleware
public_router4 = APIRouter(prefix="/public", tags=["public"])
rate_limit_store: dict = {}


@public_router4.middleware("http")
async def public_rate_limit(request: Request, call_next):
    """Simple in-memory rate limiting for public endpoints."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    # Clean old entries
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store.get(client_ip, [])
        if now - t < 60
    ]

    # Check rate limit (10 requests/minute)
    if len(rate_limit_store.get(client_ip, [])) >= 10:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again in 60 seconds."}
        )

    rate_limit_store.setdefault(client_ip, []).append(now)
    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(10 - len(rate_limit_store[client_ip]))
    return response


@public_router4.get("/info")
async def public_info():
    return {"message": "Public information endpoint"}


# API router with timing middleware
api_router4 = APIRouter(prefix="/api", tags=["api"])


@api_router4.middleware("http")
async def add_timing_header(request: Request, call_next):
    """Add X-Response-Time header to all API responses."""
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Response-Time"] = f"{duration:.3f}s"
    return response


@api_router4.get("/data")
async def api_data():
    await asyncio.sleep(0.05)  # Simulate work
    return {"data": "API response with timing header"}


app4.include_router(admin_router4)
app4.include_router(public_router4)
app4.include_router(api_router4)


# ============================================================
# Exercise 24.5: API Versioning Strategy
# ============================================================

app5 = FastAPI(title="API Versioning")

# Shared data
shared_items = [
    {"id": 1, "name": "Widget", "price": 9.99},
    {"id": 2, "name": "Gadget", "price": 19.99},
    {"id": 3, "name": "Doohickey", "price": 4.99},
]


def get_api_version(request: Request) -> str:
    """Detect API version from URL path or Accept header."""
    path = request.url.path
    if "/v1/" in path:
        return "v1"
    if "/v2/" in path:
        return "v2"

    # Check Accept header
    accept = request.headers.get("accept", "")
    if "vnd.myapp.v2" in accept:
        return "v2"

    return "v1"


v1_router5 = APIRouter(prefix="/api/v1", tags=["v1"])
v2_router5 = APIRouter(prefix="/api/v2", tags=["v2"])


@v1_router5.get("/items")
async def v1_list_items():
    """V1: Simple array of items."""
    return shared_items


@v2_router5.get("/items")
async def v2_list_items(page: int = 1, per_page: int = 10):
    """V2: Paginated response with HATEOAS links."""
    total = len(shared_items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = shared_items[start:end]

    items_with_links = []
    for item in page_items:
        items_with_links.append({
            **item,
            "_links": {
                "self": f"/api/v2/items/{item['id']}",
                "update": {"method": "PUT", "href": f"/api/v2/items/{item['id']}"},
                "delete": {"method": "DELETE", "href": f"/api/v2/items/{item['id']}"},
            }
        })

    total_pages = (total + per_page - 1) // per_page
    next_page = f"/api/v2/items?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "data": items_with_links,
        "meta": {"total": total, "page": page, "per_page": per_page, "total_pages": total_pages},
        "_links": {
            "self": f"/api/v2/items?page={page}&per_page={per_page}",
            "next": next_page,
            "first": "/api/v2/items?page=1&per_page=10",
        }
    }


@v2_router5.get("/items/{item_id}")
async def v2_get_item(item_id: int):
    """V2: Get single item with HATEOAS links."""
    item = next((i for i in shared_items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        **item,
        "_links": {
            "self": f"/api/v2/items/{item_id}",
            "collection": "/api/v2/items",
        }
    }


app5.include_router(v1_router5)
app5.include_router(v2_router5)


# Fallback: version-aware endpoint via Accept header
@app5.get("/api/items")
async def versioned_items(request: Request):
    """Return items based on Accept header version detection."""
    version = get_api_version(request)
    if version == "v2":
        return await v2_list_items()
    return shared_items
