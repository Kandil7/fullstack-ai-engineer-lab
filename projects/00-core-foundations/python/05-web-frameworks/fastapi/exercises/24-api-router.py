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

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# ============================================================
# Exercise 24.1: Basic Router Setup
# ============================================================
"""
Problem:
    Create a modular API with separate routers for different domains.

Application structure:
    main_app/
        __init__.py
        main.py          # FastAPI app instance
        routers/
            users.py     # User management router
            products.py  # Product management router
            orders.py    # Order management router

For this exercise, create all routers in a single file.

Router definitions:
    users_router = APIRouter(
        prefix="/users",
        tags=["users"],
        responses={404: {"description": "Not found"}}
    )

    products_router = APIRouter(
        prefix="/products",
        tags=["products"],
        responses={404: {"description": "Not found"}}
    )

    orders_router = APIRouter(
        prefix="/orders",
        tags=["orders"],
        responses={404: {"description": "Not found"}}
    )

Endpoints per router:
    users_router:
        GET    /users          - List users
        POST   /users          - Create user
        GET    /users/{id}     - Get user
        DELETE /users/{id}     - Delete user

    products_router:
        GET    /products       - List products
        POST   /products       - Create product
        GET    /products/{id}  - Get product
        PUT    /products/{id}  - Update product

    orders_router:
        GET    /orders         - List orders
        POST   /orders         - Create order
        GET    /orders/{id}    - Get order
        POST   /orders/{id}/cancel - Cancel order

Main app:
    app = FastAPI(title="Modular API")
    app.include_router(users_router)
    app.include_router(products_router)
    app.include_router(orders_router)

Hints:
    - APIRouter groups related endpoints
    - prefix="/users" prepends /users to all routes in router
    - tags=["users"] groups endpoints in Swagger UI
    - include_router() adds the router to the main app
    - Routers can have their own dependencies

Test cases:
    # User endpoints
    GET /users -> 200 [list of users]
    POST /users -> 201 created user

    # Product endpoints
    GET /products -> 200 [list of products]
    POST /products -> 201 created product

    # Order endpoints
    GET /orders -> 200 [list of orders]
    POST /orders -> 201 created order

    # Swagger UI shows grouped endpoints
    GET /docs -> Shows "users", "products", "orders" tags
"""

# TODO: Create your routers below


# ============================================================
# Exercise 24.2: Router Dependencies
# ============================================================
"""
Problem:
    Add dependencies to routers for authentication and authorization.

Requirements:
    1. Create a shared get_current_user() dependency
    2. Add role-based access control (RBAC) dependency
    3. Apply dependencies at router level
    4. Override dependencies for specific endpoints

Dependency chain:
    get_current_user() -> get_db() -> user session

    # Public endpoint (no auth required)
    @products_router.get("/public")
    async def public_products():
        pass

    # Authenticated endpoint
    @users_router.get("/me")
    async def get_profile(user = Depends(get_current_user)):
        return user

    # Admin-only endpoint
    @users_router.get("/admin/all")
    async def admin_list_users(
        user = Depends(require_role("admin"))
    ):
        pass

RBAC dependency:
    def require_role(role: str):
        async def check_role(user = Depends(get_current_user)):
            if user.role != role:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role '{role}' required"
                )
            return user
        return check_role

Router with default dependency:
    admin_router = APIRouter(
        prefix="/admin",
        dependencies=[Depends(get_current_user)]
    )
    # All endpoints in admin_router require authentication

Hints:
    - Dependencies can be added to APIRouter constructor
    - Use Depends() with a factory function for parameterized deps
    - Router dependencies run before endpoint dependencies
    - Use dependencies=[Depends(...)] in APIRouter()
    - Endpoint-level deps override router-level deps

Test cases:
    # Public endpoint (no auth)
    GET /products/public
    -> 200 [products] (no auth needed)

    # Authenticated endpoint
    GET /users/me
    Headers: Authorization: Bearer valid-token
    -> 200 {"id": 1, "username": "alice"}

    # Admin endpoint (non-admin)
    GET /admin/users
    Headers: Authorization: Bearer user-token
    -> 403 {"detail": "Role 'admin' required"}

    # Admin endpoint (admin)
    GET /admin/users
    Headers: Authorization: Bearer admin-token
    -> 200 [all users]
"""

# TODO: Write router dependencies below


# ============================================================
# Exercise 24.3: Nested Routers (Sub-Applications)
# ============================================================
"""
Problem:
    Create nested router structure for a complex API.

Structure:
    /api/v1/users       - User management
    /api/v1/users/{id}/addresses  - User addresses (nested)
    /api/v1/products    - Product management
    /api/v1/products/{id}/reviews  - Product reviews (nested)
    /api/v2/users       - V2 user API (different format)

Architecture:
    v1_router = APIRouter(prefix="/api/v1", tags=["v1"])
    v2_router = APIRouter(prefix="/api/v2", tags=["v2"])

    v1_users = APIRouter(prefix="/users", tags=["users"])
    v1_user_addresses = APIRouter(prefix="/{user_id}/addresses", tags=["addresses"])

    v1_products = APIRouter(prefix="/products", tags=["products"])
    v1_product_reviews = APIRouter(prefix="/{product_id}/reviews", tags=["reviews"])

    # Nest routers
    v1_users.include_router(v1_user_addresses)
    v1_products.include_router(v1_product_reviews)
    v1_router.include_router(v1_users)
    v1_router.include_router(v1_products)
    v2_router.include_router(v2_users)

    app.include_router(v1_router)
    app.include_router(v2_router)

Endpoints:
    V1:
        GET    /api/v1/users                        - List users
        GET    /api/v1/users/{user_id}               - Get user
        GET    /api/v1/users/{user_id}/addresses      - List user addresses
        POST   /api/v1/users/{user_id}/addresses      - Add address
        GET    /api/v1/products                       - List products
        GET    /api/v1/products/{product_id}/reviews   - List product reviews
        POST   /api/v1/products/{product_id}/reviews   - Add review

    V2 (different response format):
        GET    /api/v2/users                          - List users (v2 format)

Hints:
    - Nest routers with parent_router.include_router(child_router)
    - Path parameters in nested routers inherit from parent
    - Use API tags to organize in Swagger UI
    - V2 can reuse V1 logic with different response models
    - Consider using versioning middleware instead of prefixes

Test cases:
    # Nested route - get user addresses
    GET /api/v1/users/1/addresses
    -> 200 [{"id": 1, "street": "...", "city": "..."}]

    # Nested route - add address
    POST /api/v1/users/1/addresses
    {"street": "123 Main St", "city": "Springfield"}
    -> 201 {"id": 1, "street": "123 Main St", "city": "Springfield"}

    # V2 format
    GET /api/v2/users
    -> 200 {"data": [...], "meta": {"total": 5}}
"""

# TODO: Write nested routers below


# ============================================================
# Exercise 24.4: Router-Level Middleware
# ============================================================
"""
Problem:
    Apply middleware to specific router groups.

Requirements:
    1. Add request timing middleware to /api routes only
    2. Add logging middleware to /admin routes only
    3. Add rate limiting to /public routes only
    4. Each router group has its own middleware stack

Middleware per router:
    # Admin router - adds audit logging
    admin_router = APIRouter(prefix="/admin")

    @admin_router.middleware("http")
    async def admin_audit_log(request: Request, call_next):
        response = await call_next(request)
        print(f"[ADMIN] {request.method} {request.url.path} -> {response.status_code}")
        return response

    # Public router - adds rate limiting
    public_router = APIRouter(prefix="/public")

    @public_router.middleware("http")
    async def public_rate_limit(request: Request, call_next):
        # Simple in-memory rate limiting
        # Allow 100 requests per minute
        pass

    # API router - adds timing
    api_router = APIRouter(prefix="/api")

    @api_router.middleware("http")
    async def add_timing_header(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        return response

Endpoints:
    GET /admin/settings        - Has audit logging
    GET /public/info           - Has rate limiting
    GET /api/data              - Has timing header

Hints:
    - Use @router.middleware("http") decorator
    - Middleware runs for ALL routes in that router
    - Middleware order: outermost runs first
    - Use request.state to pass data between middleware
    - starlette.middleware.base.BaseMiddleware for class-based

Test cases:
    # Admin endpoint has audit log
    GET /admin/settings
    -> 200 (console shows: [ADMIN] GET /admin/settings -> 200)

    # Public endpoint has rate limiting
    GET /public/info
    -> 200 (with rate limit headers)

    # API endpoint has timing
    GET /api/data
    -> 200
    Headers: X-Response-Time: 0.003s
"""

# TODO: Write router-level middleware below


# ============================================================
# Exercise 24.5: API Versioning Strategy
# ============================================================
"""
Problem:
    Implement API versioning with backward compatibility.

Versioning approach:
    1. URL-based: /api/v1/, /api/v2/
    2. Header-based: Accept: application/vnd.myapp.v2+json
    3. Query parameter: /api/data?version=2

Requirements:
    1. Support URL-based versioning (primary)
    2. Support header-based versioning (fallback)
    3. V2 adds pagination to list endpoints
    4. V2 adds HATEOAS links
    5. V1 still works (no breaking changes)

V1 response:
    [{"id": 1, "name": "Widget"}]

V2 response:
    {
        "data": [{"id": 1, "name": "Widget", "_links": {...}}],
        "meta": {"total": 1, "page": 1, "per_page": 20},
        "_links": {"self": "/api/v2/items", "next": null}
    }

Version detection:
    def get_api_version(request: Request) -> str:
        # 1. Check URL path for /v1/ or /v2/
        path = request.url.path
        if "/v1/" in path:
            return "v1"
        if "/v2/" in path:
            return "v2"

        # 2. Check Accept header
        accept = request.headers.get("accept", "")
        if "vnd.myapp.v2" in accept:
            return "v2"

        # 3. Default to v1
        return "v1"

Hints:
    - Create version-specific response models
    - Use dependency injection for version detection
    - Keep business logic in shared services
    - Format responses differently per version
    - Consider using OpenAPI for version documentation

Test cases:
    # V1 (default)
    GET /api/items
    -> 200 [{"id": 1, "name": "Widget"}]

    # V2 (URL-based)
    GET /api/v2/items
    -> 200 {"data": [...], "meta": {...}, "_links": {...}}

    # V2 (header-based)
    GET /api/items
    Accept: application/vnd.myapp.v2+json
    -> 200 {"data": [...], "meta": {...}}

    # V1 still works
    GET /api/v1/items
    -> 200 [{"id": 1, "name": "Widget"}]
"""

# TODO: Write API versioning code below
