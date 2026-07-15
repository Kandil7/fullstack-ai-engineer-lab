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

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import re
import time
import uuid

# ============================================================
# Exercise 22.1: Basic CORS Setup
# ============================================================

app1 = FastAPI(title="Exercise 1 - Basic CORS")

# Configure CORS middleware
app1.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://myapp.example.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With", "X-Client-Id"],
    expose_headers=["X-Request-Id", "X-Response-Time"],
    max_age=3600,
)


@app1.get("/api/profile")
async def get_profile(request: Request):
    """Return user profile (cors-protected)."""
    origin = request.headers.get("origin", "unknown")
    return {
        "profile": {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com"
        },
        "request_origin": origin
    }


@app1.post("/api/data")
async def post_data(data: dict, request: Request):
    """Accept data submissions (cors-protected)."""
    return {"received": data, "origin": request.headers.get("origin")}


# ============================================================
# Exercise 22.2: Dynamic CORS Origins
# ============================================================

app2 = FastAPI(title="Exercise 2 - Dynamic CORS")

ALLOWED_ORIGINS_CONFIG = {
    "exact": [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://myapp.example.com",
    ],
    "wildcard": ["*.example.com"],
    "regex": [r"https://.*\.dev\.local:\d+"],
}


class DynamicCORS:
    """Dynamic CORS checker with wildcard and regex support."""

    def __init__(self, config: dict):
        self.config = config

    def is_origin_allowed(self, origin: str) -> bool:
        # Check exact matches
        if origin in self.config.get("exact", []):
            return True

        # Check wildcard subdomains
        for wildcard in self.config.get("wildcard", []):
            if wildcard.startswith("*."):
                domain_suffix = wildcard[1:]  # e.g., ".example.com"
                if origin.endswith(domain_suffix):
                    # Also check that it's a subdomain, not the bare domain
                    # e.g., *.example.com matches https://api.example.com but not https://example.com
                    import urllib.parse
                    parsed = urllib.parse.urlparse(origin)
                    hostname = parsed.hostname or ""
                    if hostname.endswith(domain_suffix[1:]):
                        return True

        # Check regex patterns
        for pattern in self.config.get("regex", []):
            if re.match(pattern, origin):
                return True

        # Log rejected origin
        print(f"[CORS] Rejected origin: {origin}")
        return False


dynamic_cors = DynamicCORS(ALLOWED_ORIGINS_CONFIG)


@app2.middleware("http")
async def dynamic_cors_middleware(request: Request, call_next):
    """Custom middleware that applies dynamic CORS checking."""
    origin = request.headers.get("origin")
    response = await call_next(request)

    if origin and dynamic_cors.is_origin_allowed(origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Max-Age"] = "3600"

    return response


@app2.get("/api/data")
async def get_data():
    return {"message": "Dynamic CORS protected data"}


# ============================================================
# Exercise 22.3: Per-Route CORS Configuration
# ============================================================

app3 = FastAPI(title="Exercise 3 - Per-Route CORS")


class PerRouteCORSMiddleware:
    """Custom middleware that applies CORS rules based on request path."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path = scope.get("path", "")
        headers = []

        if path.startswith("/public"):
            # Wide open - any origin
            headers = [
                (b"access-control-allow-origin", b"*"),
                (b"access-control-allow-methods", b"GET, POST"),
                (b"access-control-allow-headers", b"*"),
            ]
        elif path.startswith("/api"):
            # Restricted - specific origins (we'll set based on request)
            # This is set below by reading the request origin
            pass
        elif path.startswith("/admin"):
            # Locked down - no CORS headers
            pass

        # We need to wrap the send to add CORS headers
        # For simplicity, use a different approach with send wrapper
        original_send = send

        async def send_with_cors(message):
            if message["type"] == "http.response.start":
                existing_headers = dict(message.get("headers", []))
                new_headers = list(message.get("headers", []))

                if path.startswith("/public"):
                    new_headers = list(set(new_headers) - {
                        h for h in new_headers if h[0] == b"access-control-allow-origin"
                    })
                    new_headers.append((b"access-control-allow-origin", b"*"))
                    new_headers.append((b"access-control-allow-methods", b"GET, POST"))
                elif path.startswith("/api"):
                    # Check request origin
                    req_headers = dict(scope.get("headers", []))
                    origin = req_headers.get(b"origin", b"").decode()
                    allowed = ["http://localhost:3000", "https://myapp.example.com"]
                    if origin in allowed:
                        new_headers.append((b"access-control-allow-origin", origin.encode()))
                        new_headers.append((b"access-control-allow-credentials", b"true"))

                message = dict(message)
                message["headers"] = new_headers
            await original_send(message)

        return await self.app(scope, receive, send_with_cors)


app3.add_middleware(PerRouteCORSMiddleware)


@app3.get("/public/info")
async def public_info():
    return {"message": "Public information - accessible from any origin"}


@app3.get("/api/data")
async def api_data():
    return {"message": "Protected data - restricted origins"}


@app3.get("/admin/settings")
async def admin_settings():
    return {"settings": {"feature_x": True, "max_users": 100}}


# ============================================================
# Exercise 22.4: CORS with Custom Headers
# ============================================================

app4 = FastAPI(title="Exercise 4 - CORS with Custom Headers")

app4.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    expose_headers=[
        "X-Total-Count",
        "X-Request-Id",
        "X-Rate-Limit-Remaining",
        "X-API-Version",
        "X-Response-Time",
    ],
    allow_headers=["*"],
)


@app4.get("/api/items")
async def list_items():
    """Return items with custom headers exposed to JS."""
    items = [{"id": 1, "name": "Widget"}, {"id": 2, "name": "Gadget"}]
    return JSONResponse(
        content=items,
        headers={
            "X-Total-Count": str(len(items)),
            "X-Request-Id": str(uuid.uuid4()),
            "X-Rate-Limit-Remaining": "98",
            "X-API-Version": "v2.1",
            "X-Response-Time": "0.003s",
        }
    )


@app4.post("/api/items", status_code=201)
async def create_item(item: dict, request: Request):
    """Accept custom header X-Client-Id from clients."""
    client_id = request.headers.get("x-client-id", "unknown")
    return JSONResponse(
        content={"created": True, "item": item, "client": client_id},
        headers={"X-Request-Id": str(uuid.uuid4())}
    )


# ============================================================
# Exercise 22.5: CORS Security Hardening
# ============================================================

app5 = FastAPI(title="Exercise 5 - Secure CORS")

SECURE_ALLOWED_ORIGINS = [
    "https://myapp.example.com",
    "https://admin.myapp.example.com",
]

REJECTED_ORIGINS_LOG: List[str] = []


@app5.middleware("http")
async def secure_cors_middleware(request: Request, call_next):
    """Middleware implementing CORS security best practices."""
    origin = request.headers.get("origin", "").strip()

    response = await call_next(request)

    if not origin:
        # Server-to-server request, no CORS needed
        return response

    # Reject null origin (used by some attacks)
    if origin.lower() == "null":
        REJECTED_ORIGINS_LOG.append(f"Rejected null origin from {request.client.host}")
        raise HTTPException(status_code=403, detail="Origin not allowed")

    # Validate origin
    import urllib.parse
    try:
        parsed = urllib.parse.urlparse(origin)
        hostname = parsed.hostname or ""

        # Reject IP addresses
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname):
            REJECTED_ORIGINS_LOG.append(f"Rejected IP origin: {origin}")
            raise HTTPException(status_code=403, detail="Origin not allowed")

        # Reject missing scheme
        if not parsed.scheme:
            REJECTED_ORIGINS_LOG.append(f"Rejected scheme-less origin: {origin}")
            raise HTTPException(status_code=403, detail="Origin not allowed")

        # Check allowlist
        if origin not in SECURE_ALLOWED_ORIGINS:
            REJECTED_ORIGINS_LOG.append(f"Rejected unknown origin: {origin}")
            raise HTTPException(status_code=403, detail="Origin not allowed")

    except HTTPException:
        raise
    except Exception:
        REJECTED_ORIGINS_LOG.append(f"Rejected malformed origin: {origin}")
        raise HTTPException(status_code=403, detail="Origin not allowed")

    # Add CORS headers for allowed origins
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    response.headers["Access-Control-Max-Age"] = "3600"
    response.headers["Vary"] = "Origin"

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


@app5.get("/secure/data")
async def secure_data():
    """CORS-hardened endpoint with security headers."""
    return {"message": "This is securely served with strict CORS and security headers"}


@app5.get("/secure/rejected-log")
async def get_rejected_log():
    """View rejected origins for security monitoring."""
    return {"rejected_origins": REJECTED_ORIGINS_LOG[-50:]}
