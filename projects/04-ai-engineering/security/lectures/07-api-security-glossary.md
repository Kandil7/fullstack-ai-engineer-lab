# Glossary 07: API Security Terms

## Quick Reference Table

| Term | Category | Importance | See Also |
|------|----------|------------|----------|
| Rate Limiting | Technique | Critical | Throttling, Token Bucket |
| OWASP Top 10 | Standard | Critical | API Security |
| API Gateway | Architecture | High | Security Controls |
| Input Validation | Technique | Critical | Schema Validation |
| HTTPS/TLS | Protocol | Critical | Encryption |
| CORS | Mechanism | High | Cross-Origin |
| API Key | Credential | High | Authentication |
| OAuth 2.0 | Protocol | Critical | Authorization |
| JWT | Token | Critical | Access Token |
| SSRF | Attack | Critical | Server-Side Forgery |
| BOLA | Attack | Critical | Broken Authorization |
| Rate Limit | Mechanism | Critical | Throttling |
| API Throttling | Technique | High | Rate Limiting |
| Request Validation | Technique | Critical | Input Validation |
| Response Filtering | Technique | High | Output Filtering |
| API Monitoring | Process | High | Observability |

---

## Alphabetical Definitions

### API Gateway

**Definition**: A server that acts as a single entry point for API calls, routing requests to appropriate services and providing centralized security controls.

**Example**:
```python
class APIGateway:
    def __init__(self):
        self.routes = {}
        self.middleware = []

    def add_route(self, path: str, service: str, methods: list):
        """Add a route to the gateway."""
        self.routes[path] = {"service": service, "methods": methods}

    def add_middleware(self, middleware):
        """Add middleware for security checks."""
        self.middleware.append(middleware)

    def handle_request(self, request: dict) -> dict:
        """Handle incoming request through gateway."""
        # Apply middleware
        for mw in self.middleware:
            result = mw(request)
            if not result.get("allowed", True):
                return {"status": 403, "error": result.get("reason")}

        # Route to service
        path = request["path"]
        if path not in self.routes:
            return {"status": 404, "error": "Not found"}

        route = self.routes[path]
        if request["method"] not in route["methods"]:
            return {"status": 405, "error": "Method not allowed"}

        return {"status": 200, "service": route["service"]}

# Usage
gateway = APIGateway()
gateway.add_middleware(lambda r: {"allowed": r.get("auth")})
gateway.add_route("/api/v1/chat", "ai-service", ["POST"])
```

**Related Terms**: Microservices, Load Balancer, Reverse Proxy

---

### API Key

**Definition**: A unique identifier used to authenticate a client making API requests. Simpler than OAuth but less secure for user-facing applications.

**Example**:
```python
import secrets
import hashlib

class APIKeyManager:
    def __init__(self):
        self.keys = {}

    def create_key(self, user_id: str, permissions: list) -> str:
        """Create a new API key."""
        key = f"sk_{secrets.token_hex(32)}"
        key_hash = hashlib.sha256(key.encode()).hexdigest()

        self.keys[key_hash] = {
            "user_id": user_id,
            "permissions": permissions,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=90),
        }
        return key

    def validate_key(self, key: str) -> dict:
        """Validate an API key."""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        if key_hash not in self.keys:
            return {"valid": False, "error": "Invalid key"}
        return {"valid": True, **self.keys[key_hash]}

# Usage
manager = APIKeyManager()
api_key = manager.create_key("user123", ["read", "write"])
```

**Related Terms**: Authentication, Secret Key, Credential

---

### API Rate Limit

**Definition**: The maximum number of API requests a client can make within a specified time period.

**Example**:
```python
class RateLimit:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []

    def is_allowed(self) -> dict:
        """Check if request is within rate limit."""
        now = time.time()
        window_start = now - self.window_seconds

        # Remove old requests
        self.requests = [t for t in self.requests if t > window_start]

        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return {
                "allowed": True,
                "remaining": self.max_requests - len(self.requests),
                "limit": self.max_requests,
            }
        return {
            "allowed": False,
            "remaining": 0,
            "retry_after": self.window_seconds,
        }

# Usage
rate_limit = RateLimit(max_requests=100, window_seconds=60)
result = rate_limit.is_allowed()
print(f"Allowed: {result['allowed']}, Remaining: {result['remaining']}")
```

**Related Terms**: Rate Limiting, Throttling, Quota

---

### API Security

**Definition**: The practices and mechanisms used to protect APIs from attacks, unauthorized access, and abuse.

**Example**:
```python
# API Security Checklist
security_checklist = {
    "authentication": {
        "require_auth": True,
        "use_oauth": True,
        "api_key_rotation": True,
    },
    "authorization": {
        "rbac": True,
        "object_level_auth": True,
        "least_privilege": True,
    },
    "input_validation": {
        "schema_validation": True,
        "max_length": True,
        "injection_protection": True,
    },
    "rate_limiting": {
        "per_user_limit": True,
        "global_limit": True,
        "burst_protection": True,
    },
    "encryption": {
        "https_only": True,
        "encrypt_sensitive_data": True,
    },
    "monitoring": {
        "request_logging": True,
        "anomaly_detection": True,
        "alerting": True,
    },
}
```

**Related Terms**: OWASP Top 10, API Gateway, Security Controls

---

### BOLA (Broken Object Level Authorization)

**Definition**: An API vulnerability where an attacker can access objects (data) belonging to other users by manipulating object IDs in API requests.

**Example**:
```python
# VULNERABLE: No object-level authorization
@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    # Any user can access any order by guessing order IDs
    return db.get_order(order_id)

# SECURE: With object-level authorization
@app.get("/api/orders/{order_id}")
@require_auth
def get_order(order_id: str, current_user: User):
    order = db.get_order(order_id)
    if order.user_id != current_user.id:
        raise HTTPException(403, "Access denied")
    return order
```

**Related Terms**: IDOR, Authorization, Access Control

---

### CORS (Cross-Origin Resource Sharing)

**Definition**: A security mechanism that restricts web pages from making requests to a different domain than the one that served the page.

**Example**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],  # Only allow specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow specific methods
    allow_headers=["Authorization", "Content-Type"],
)

# BAD: Allow all origins (insecure)
# allow_origins=["*"]
```

**Related Terms**: Cross-Origin, Preflight Request, Same-Origin Policy

---

### HTTP Security Headers

**Definition**: HTTP headers that provide additional security controls for web applications and APIs.

**Example**:
```python
# Security headers to include in API responses
security_headers = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Content-Security-Policy": "default-src 'self'",
    "Cache-Control": "no-store, no-cache, must-revalidate",
    "Pragma": "no-cache",
}

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    for header, value in security_headers.items():
        response.headers[header] = value
    return response
```

**Related Terms**: HTTPS, Content Security Policy, HSTS

---

### OWASP API Security Top 10

**Definition**: A standard awareness document listing the top 10 most critical API security risks.

**Example**:
```python
owasp_api_top_10 = {
    "API1": "Broken Object Level Authorization (BOLA)",
    "API2": "Broken Authentication",
    "API3": "Broken Object Property Level Authorization",
    "API4": "Unrestricted Resource Consumption",
    "API5": "Broken Function Level Authorization",
    "API6": "Unrestricted Access to Sensitive Business Flows",
    "API7": "Server Side Request Forgery (SSRF)",
    "API8": "Security Misconfiguration",
    "API9": "Improper Inventory Management",
    "API10": "Unsafe Consumption of APIs",
}
```

**Related Terms**: API Security, Vulnerability Assessment, Security Audit

---

### Rate Limiting

**Definition**: Controlling the number of requests a client can make to an API within a specified time period to prevent abuse.

**Example**:
```python
from collections import defaultdict
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = defaultdict(lambda: {"tokens": capacity, "last_refill": time.time()})

    def allow_request(self, client_id: str) -> bool:
        """Check if request should be allowed."""
        bucket = self.buckets[client_id]
        now = time.time()

        # Refill tokens
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(
            self.capacity,
            bucket["tokens"] + elapsed * self.refill_rate
        )
        bucket["last_refill"] = now

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        return False

# Usage
limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10)
print(limiter.allow_request("user123"))  # True
```

**Related Terms**: Token Bucket, Sliding Window, Throttling

---

### Request Validation

**Definition**: The process of checking API requests for correctness, completeness, and security before processing.

**Example**:
```python
from pydantic import BaseModel, Field, validator
import re

class APIRequest(BaseModel):
    """Validated API request."""
    prompt: str = Field(..., min_length=1, max_length=4096)
    model: str = Field(default="gpt-4", pattern="^(gpt-3.5-turbo|gpt-4)$")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    @validator('prompt')
    def validate_prompt(cls, v):
        # Check for injection patterns
        if re.search(r'ignore\s+(all\s+)?previous', v, re.IGNORECASE):
            raise ValueError('Potential prompt injection detected')
        return v

    class Config:
        extra = "forbid"  # Reject extra fields
```

**Related Terms**: Input Validation, Schema Validation, Pydantic

---

### Response Filtering

**Definition**: The process of removing or masking sensitive data from API responses before sending to clients.

**Example**:
```python
class ResponseFilter:
    SENSITIVE_FIELDS = ["password", "ssn", "api_key", "secret"]

    def filter_response(self, data: dict) -> dict:
        """Remove sensitive fields from response."""
        filtered = {}
        for key, value in data.items():
            if key.lower() in [f.lower() for f in self.SENSITIVE_FIELDS]:
                filtered[key] = "[REDACTED]"
            elif isinstance(value, dict):
                filtered[key] = self.filter_response(value)
            else:
                filtered[key] = value
        return filtered

# Usage
filter = ResponseFilter()
response = {"user": "john", "password": "secret123", "email": "john@example.com"}
filtered = filter.filter_response(response)
# {'user': 'john', 'password': '[REDACTED]', 'email': 'john@example.com'}
```

**Related Terms**: Output Filtering, Data Minimization, PII Protection

---

### SSRF (Server-Side Request Forgery)

**Definition**: An attack where an attacker can make the server perform requests to unintended internal or external resources.

**Example**:
```python
# VULNERABLE: No URL validation
@app.post("/api/fetch")
def fetch_url(url: str):
    response = requests.get(url)  # Attacker can access internal services!
    return response.text

# SECURE: URL validation
import ipaddress
from urllib.parse import urlparse

ALLOWED_HOSTS = ["api.example.com", "cdn.example.com"]
BLOCKED_RANGES = ["127.0.0.0/8", "10.0.0.0/8", "192.168.0.0/16"]

def is_safe_url(url: str) -> bool:
    """Validate URL is safe to fetch."""
    try:
        parsed = urlparse(url)

        # Only allow HTTP/HTTPS
        if parsed.scheme not in ["http", "https"]:
            return False

        # Check against blocked IP ranges
        import socket
        ip = socket.gethostbyname(parsed.hostname)
        for blocked in BLOCKED_RANGES:
            if ipaddress.ip_address(ip) in ipaddress.ip_network(blocked):
                return False

        return True
    except Exception:
        return False

@app.post("/api/fetch")
def fetch_url(url: str):
    if not is_safe_url(url):
        raise HTTPException(400, "URL not allowed")
    response = requests.get(url, timeout=5)
    return response.text
```

**Related Terms**: Internal Network, URL Validation, Request Forgery

---

### Throttling

**Definition**: A technique to limit the rate at which requests are processed, often used to prevent abuse and ensure fair usage.

**Example**:
```python
class Throttler:
    def __init__(self, requests_per_second: float):
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = {}

    def should_throttle(self, client_id: str) -> dict:
        """Check if client should be throttled."""
        now = time.time()
        last_time = self.last_request_time.get(client_id, 0)

        if now - last_time < self.min_interval:
            wait_time = self.min_interval - (now - last_time)
            return {"throttled": True, "wait_seconds": wait_time}

        self.last_request_time[client_id] = now
        return {"throttled": False}

# Usage
throttler = Throttler(requests_per_second=10)
result = throttler.should_throttle("user123")
print(f"Throttled: {result['throttled']}")
```

**Related Terms**: Rate Limiting, Token Bucket, QoS

---

### Token Bucket

**Definition**: A rate limiting algorithm where tokens are added to a bucket at a fixed rate and requests consume tokens.

**Example**:
```python
import time

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens."""
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now

# Usage
bucket = TokenBucket(capacity=100, refill_rate=10)
print(bucket.consume())  # True
print(bucket.tokens)  # 99
```

**Related Terms**: Rate Limiting, Sliding Window, Leaky Bucket

---

*Part of the [AI Security Lecture Series](README.md). See also: [Lecture 07: API Security](07-api-security-lecture.md)*
