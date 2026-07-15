"""
Exercise 22: CORS Configuration in FastAPI

Master Cross-Origin Resource Sharing configuration.
Topics: CORS middleware, origins, headers, credentials, preflight.

Prerequisites:
- HTTP basics (methods, headers)
- Browser security model basics
- FastAPI middleware concepts

Estimated time: 30-45 minutes
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="CORS Exercises")

# ============================================================
# Exercise 22.1: Basic CORS Setup
# ============================================================
"""
Problem:
    Configure CORS for a web application with multiple frontend origins.

Requirements:
    1. Allow requests from these origins:
       - http://localhost:3000 (development React app)
       - http://localhost:5173 (Vite dev server)
       - https://myapp.example.com (production)
    2. Allow all HTTP methods (GET, POST, PUT, DELETE, PATCH, OPTIONS)
    3. Allow common headers (Authorization, Content-Type, X-Requested-With)
    4. Allow credentials (cookies, auth headers)
    5. Set max age for preflight caching to 3600 seconds

CORS middleware setup:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[...],
        allow_credentials=True,
        allow_methods=[...],
        allow_headers=[...],
        max_age=3600,
    )

Endpoints to protect:
    GET  /api/profile    - Returns user profile (requires auth)
    POST /api/data       - Accepts data submissions

Hints:
    - CORSMiddleware must be added before other middleware
    - allow_origins=["*"] allows ALL origins (not recommended for production)
    - allow_credentials=True requires explicit origins (not "*")
    - max_age controls how long browsers cache preflight responses
    - Use expose_headers to make custom headers available to JS

Test cases:
    # Preflight request
    OPTIONS /api/profile
    Origin: http://localhost:3000
    Access-Control-Request-Method: GET
    Access-Control-Request-Headers: Authorization
    -> 200 with Access-Control-Allow-* headers

    # Actual request
    GET /api/profile
    Origin: http://localhost:3000
    Authorization: Bearer token123
    -> 200 with data + Access-Control-Allow-Origin header

    # Blocked origin
    GET /api/profile
    Origin: https://evil-site.com
    -> 200 (no CORS headers, browser blocks response)

    # Cross-origin with credentials
    GET /api/profile
    Origin: http://localhost:3000
    -> 200 + Access-Control-Allow-Credentials: true
"""

# TODO: Configure CORS middleware below
# TODO: Create the protected endpoints


# ============================================================
# Exercise 22.2: Dynamic CORS Origins
# ============================================================
"""
Problem:
    Build a CORS system that dynamically checks allowed origins.

Requirements:
    1. Store allowed origins in a database/config (use a dict for this exercise)
    2. Check incoming Origin header against allowed list
    3. Support wildcard subdomains (*.example.com)
    4. Support regex patterns for complex matching
    5. Log rejected origins for security monitoring

Origin configuration:
    ALLOWED_ORIGINS = {
        "exact": ["http://localhost:3000", "https://myapp.example.com"],
        "wildcard": ["*.example.com"],           # matches any subdomain
        "regex": [r"https://.*\.dev\.local:\d+"], # dev servers with any port
    }

Dynamic CORS class:
    class DynamicCORS:
        def __init__(self, config: dict):
            self.config = config

        def is_origin_allowed(self, origin: str) -> bool:
            # Check exact matches
            # Check wildcard subdomains
            # Check regex patterns
            # Log if rejected
            pass

Hints:
    - Wildcard: origin.endswith(".example.com") or origin == "https://example.com"
    - Regex: import re; re.match(pattern, origin)
    - Parse origin header: "https://myapp.example.com" -> scheme + domain
    - Log with: print(f"[CORS] Rejected origin: {origin}")

Test cases:
    # Exact match
    is_origin_allowed("http://localhost:3000") -> True

    # Wildcard subdomain
    is_origin_allowed("https://api.example.com") -> True
    is_origin_allowed("https://admin.example.com") -> True

    # Regex match
    is_origin_allowed("https://app.dev.local:5173") -> True

    # No match
    is_origin_allowed("https://evil.com") -> False

    # Rejected origin logged
    is_origin_allowed("https://evil.com")
    # Output: [CORS] Rejected origin: https://evil.com
"""

# TODO: Write dynamic CORS code below


# ============================================================
# Exercise 22.3: Per-Route CORS Configuration
# ============================================================
"""
Problem:
    Apply different CORS policies to different route groups.

Route groups:
    /public/*  - Wide open (any origin, no credentials)
    /api/*     - Restricted (specific origins, with credentials)
    /admin/*   - Locked down (same-origin only, no CORS)

Implementation approach:
    1. Create a custom middleware that checks the request path
    2. Apply appropriate CORS headers based on path prefix
    3. Handle preflight requests for each group

Custom middleware pattern:
    class PerRouteCORS:
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            if scope["type"] == "http":
                path = scope["path"]
                headers = self.get_cors_headers(path)
                # Add headers to response
            return await self.app(scope, receive, send)

Endpoints:
    GET /public/info          - Public information (any origin)
    GET /api/data             - Protected data (specific origins)
    GET /admin/settings       - Admin only (same-origin)

Hints:
    - path.startswith("/public") for public routes
    - path.startswith("/admin") for admin routes
    - Use Starlette middleware pattern: __call__(self, scope, receive, send)
    - scope["path"] gives you the request path
    - scope["headers"] contains request headers as list of tuples

Test cases:
    # Public endpoint - any origin allowed
    GET /public/info
    Origin: https://any-site.com
    -> 200 with Access-Control-Allow-Origin: *

    # API endpoint - restricted origins
    GET /api/data
    Origin: https://myapp.example.com
    -> 200 with proper CORS headers

    # API endpoint - wrong origin
    GET /api/data
    Origin: https://evil.com
    -> 200 (no CORS headers, browser blocks)

    # Admin endpoint - no CORS
    GET /admin/settings
    Origin: http://localhost:3000
    -> 200 (no Access-Control-Allow-Origin header)
"""

# TODO: Write per-route CORS code below


# ============================================================
# Exercise 22.4: CORS with Custom Headers
# ============================================================
"""
Problem:
    Configure CORS to expose custom response headers to the browser.

Requirements:
    1. API returns custom headers:
       - X-Total-Count: total number of items
       - X-Request-Id: unique request identifier
       - X-Rate-Limit-Remaining: rate limit info
       - X-API-Version: API version
    2. Configure CORS to expose these headers
    3. Allow clients to read all custom headers
    4. Support preflight for custom request headers

CORS configuration:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        expose_headers=[
            "X-Total-Count",
            "X-Request-Id",
            "X-Rate-Limit-Remaining",
            "X-API-Version",
        ],
        allow_headers=["*"],
    )

Endpoints:
    GET /api/items - Returns items with custom headers
    POST /api/items - Accepts X-Client-Id custom header

Hints:
    - Use Response(headers={...}) to add custom headers
    - Or use from starlette.responses import JSONResponse
    - expose_headers tells browsers which headers JS can access
    - allow_headers must include any headers the client sends
    - Without expose_headers, JS can only read "simple" headers

Test cases:
    # Get items with custom headers
    GET /api/items
    Origin: http://localhost:3000
    -> 200
    Headers:
        X-Total-Count: 42
        X-Request-Id: abc-123
        X-Rate-Limit-Remaining: 98
        X-API-Version: v2.1
        Access-Control-Expose-Headers: X-Total-Count, X-Request-Id, ...

    # JS can read exposed headers
    # const count = response.headers.get('X-Total-Count'); // works!

    # Send custom header
    POST /api/items
    Origin: http://localhost:3000
    X-Client-Id: frontend-app
    -> 201 Created
"""

# TODO: Write custom headers CORS code below


# ============================================================
# Exercise 22.5: CORS Security Hardening
# ============================================================
"""
Problem:
    Implement CORS security best practices.

Security requirements:
    1. Never use allow_origins=["*"] with allow_credentials=True
    2. Validate Origin header strictly against allowlist
    3. Reject requests with suspicious origins
    4. Add security headers alongside CORS
    5. Log all CORS rejections

Security middleware:
    class SecureCORS:
        def __init__(self, app, allowed_origins: list[str]):
            self.app = app
            self.allowed_origins = set(allowed_origins)

        async def __call__(self, scope, receive, send):
            # Check origin
            # Reject if not in allowlist
            # Add security headers
            # Log rejections
            pass

Security headers to add:
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    X-XSS-Protection: 1; mode=block
    Strict-Transport-Security: max-age=31536000; includeSubDomains

Suspicious origin patterns to block:
    - Null origin (used by some attacks)
    - Localhost from non-dev environments
    - IP addresses (should use domains)
    - Missing scheme (http/https)

Hints:
    - Check if Origin header exists (some requests don't have it)
    - "null" origin is used by sandboxed iframes (usually suspicious)
    - Use urllib.parse to parse origin URLs
    - Always prefer explicit allowlist over pattern matching
    - In production, use environment variables for allowed origins

Test cases:
    # Valid origin
    GET /secure/data
    Origin: https://myapp.example.com
    -> 200 with all security headers

    # Blocked suspicious origin
    GET /secure/data
    Origin: null
    -> 403 {"detail": "Origin not allowed"}

    # Missing origin (server-to-server, OK)
    GET /secure/data
    (no Origin header)
    -> 200 (no CORS headers needed, not a browser request)

    # Blocked IP address origin
    GET /secure/data
    Origin: http://192.168.1.100:3000
    -> 403 {"detail": "Origin not allowed"}
"""

# TODO: Write CORS security code below
