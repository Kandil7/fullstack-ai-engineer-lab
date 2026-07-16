# Lecture 07: API Security

## Topic Overview

APIs are the primary interface for AI services, making them a critical attack surface. This lecture covers rate limiting, input/output validation, encryption, OWASP API Security Top 10, API gateway patterns, and building secure AI APIs. Protecting AI APIs is essential for preventing abuse, data leakage, and service disruption.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement** rate limiting and throttling for AI APIs
2. **Apply** OWASP API Security Top 10 mitigations
3. **Design** secure API authentication and authorization
4. **Build** API input validation and output sanitization
5. **Implement** encryption for API communications
6. **Create** API monitoring and anomaly detection
7. **Design** API gateway patterns for AI services

---

## Key Concepts

### 1. Rate Limiting

```python
import time
from collections import defaultdict
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    burst_limit: int = 10
    window_seconds: int = 60

class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.buckets: Dict[str, Dict] = defaultdict(lambda: {
            "tokens": config.burst_limit,
            "last_refill": time.time(),
        })

    def is_allowed(self, client_id: str) -> Dict:
        """Check if request is allowed under rate limit."""
        bucket = self.buckets[client_id]
        now = time.time()

        # Refill tokens based on elapsed time
        elapsed = now - bucket["last_refill"]
        refill_rate = self.config.requests_per_minute / 60
        new_tokens = elapsed * refill_rate
        bucket["tokens"] = min(
            self.config.burst_limit,
            bucket["tokens"] + new_tokens
        )
        bucket["last_refill"] = now

        # Check if token available
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return {
                "allowed": True,
                "remaining": int(bucket["tokens"]),
                "limit": self.config.burst_limit,
                "reset_at": int(now + (self.config.burst_limit - bucket["tokens"]) / refill_rate),
            }
        else:
            return {
                "allowed": False,
                "remaining": 0,
                "limit": self.config.burst_limit,
                "retry_after": int((1 - bucket["tokens"]) / refill_rate),
            }

class SlidingWindowRateLimiter:
    """Sliding window rate limiter for more accurate limiting."""

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        window_start = now - self.window_seconds

        # Remove old requests
        self.requests[client_id] = [
            t for t in self.requests[client_id]
            if t > window_start
        ]

        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return True
        return False

    def get_usage(self, client_id: str) -> Dict:
        """Get current usage stats."""
        now = time.time()
        window_start = now - self.window_seconds
        current = sum(1 for t in self.requests[client_id] if t > window_start)

        return {
            "current": current,
            "limit": self.max_requests,
            "remaining": max(0, self.max_requests - current),
        }
```

### 2. OWASP API Security Top 10

```python
class OWASPSecurityChecklist:
    """OWASP API Security Top 10 checklist."""

    TOP_10 = {
        "API1": {
            "name": "Broken Object Level Authorization",
            "description": "Accessing objects without proper authorization checks",
            "mitigation": "Implement object-level authorization checks",
            "example_code": """
# BAD: No object-level authorization
@app.get("/api/users/{user_id}/data")
def get_user_data(user_id: str):
    return db.get_user_data(user_id)  # Any user can access any user's data

# GOOD: With object-level authorization
@app.get("/api/users/{user_id}/data")
@require_auth
def get_user_data(user_id: str, current_user: User):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, "Access denied")
    return db.get_user_data(user_id)
""",
        },
        "API2": {
            "name": "Broken Authentication",
            "description": "Weak or missing authentication mechanisms",
            "mitigation": "Implement strong authentication and session management",
        },
        "API3": {
            "name": "Broken Object Property Level Authorization",
            "description": "Exposing more object properties than intended",
            "mitigation": "Implement property-level access control",
            "example_code": """
# BAD: Returning all user properties
@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    user = db.get_user(user_id)
    return user  # Returns password_hash, internal_notes, etc.

# GOOD: Returning only allowed properties
@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    user = db.get_user(user_id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        # Excluded: password_hash, internal_notes, etc.
    }
""",
        },
        "API4": {
            "name": "Unrestricted Resource Consumption",
            "description": "Lack of rate limiting allowing abuse",
            "mitigation": "Implement rate limiting and resource quotas",
        },
        "API5": {
            "name": "Broken Function Level Authorization",
            "description": "Accessing admin functions without proper authorization",
            "mitigation": "Implement function-level authorization checks",
        },
        "API6": {
            "name": "Unrestricted Access to Sensitive Business Flows",
            "description": "Abusing business logic vulnerabilities",
            "mitigation": "Implement business flow rate limiting and monitoring",
        },
        "API7": {
            "name": "Server Side Request Forgery (SSRF)",
            "description": "Making requests to unintended internal services",
            "mitigation": "Validate and sanitize URLs, use allowlists",
        },
        "API8": {
            "name": "Security Misconfiguration",
            "description": "Default configurations, unnecessary features enabled",
            "mitigation": "Harden configurations, disable unnecessary features",
        },
        "API9": {
            "name": "Improper Inventory Management",
            "description": "Old or undocumented APIs still accessible",
            "mitigation": "Maintain API inventory, deprecate old versions",
        },
        "API10": {
            "name": "Unsafe Consumption of APIs",
            "description": "Trusting data from external APIs without validation",
            "mitigation": "Validate all data from external APIs",
        },
    }

    def run_security_audit(self, api_endpoints: list) -> list:
        """Run security audit against API endpoints."""
        findings = []

        for endpoint in api_endpoints:
            # Check for common vulnerabilities
            if not endpoint.get("rate_limited"):
                findings.append({
                    "api": "API4",
                    "endpoint": endpoint["path"],
                    "issue": "Missing rate limiting",
                })

            if not endpoint.get("auth_required"):
                findings.append({
                    "api": "API2",
                    "endpoint": endpoint["path"],
                    "issue": "Missing authentication",
                })

            if endpoint.get("returns_sensitive_data"):
                findings.append({
                    "api": "API3",
                    "endpoint": endpoint["path"],
                    "issue": "Exposes sensitive properties",
                })

        return findings
```

### 3. Secure API Design

```python
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
security = HTTPBearer()

class SecureAIRequest(BaseModel):
    """Secure AI request schema."""
    prompt: str = Field(..., min_length=1, max_length=4096)
    model: str = Field(default="gpt-4", pattern="^(gpt-3.5-turbo|gpt-4)$")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4096)

    class Config:
        extra = "forbid"  # Reject extra fields

class SecureAIResponse(BaseModel):
    """Secure AI response schema."""
    response: str
    model: str
    usage: dict
    safety_score: float

@app.post("/v1/chat/completions", response_model=SecureAIResponse)
async def chat_completion(
    request: SecureAIRequest,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Secure AI chat completion endpoint."""
    # Validate token
    token = credentials.credentials
    user = await validate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check rate limit
    if not rate_limiter.is_allowed(user.id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Check permissions
    if not user.has_permission("chat:completion"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Process request
    response = await process_ai_request(request, user)

    # Sanitize response
    sanitized_response = sanitize_output(response)

    return sanitized_response

@app.get("/v1/models")
async def list_models(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """List available models with proper authorization."""
    user = await validate_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401)

    # Return only models user has access to
    models = get_user_models(user.id)
    return {"models": models}

@app.delete("/v1/api-keys/{key_id}")
async def revoke_api_key(
    key_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Revoke API key with proper authorization."""
    user = await validate_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401)

    # Check if user owns the key
    if not user_owns_key(user.id, key_id):
        raise HTTPException(status_code=403)

    revoke_key(key_id)
    return {"status": "revoked"}
```

### 4. Input Validation for APIs

```python
from pydantic import BaseModel, Field, validator
import re

class AIRequestValidator:
    """Validate AI API requests."""

    # Dangerous patterns in prompts
    INJECTION_PATTERNS = [
        r'ignore\s+(all\s+)?previous',
        r'you\s+are\s+now\s+',
        r'\[SYSTEM\]',
        r'<\|im_start\|>',
    ]

    def validate_prompt(self, prompt: str) -> dict:
        """Validate prompt content."""
        issues = []

        # Length check
        if len(prompt) > 4096:
            issues.append("prompt_too_long")

        # Injection pattern check
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                issues.append("potential_injection")

        # Control character check
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', prompt):
            issues.append("control_characters")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def validate_model(self, model: str) -> bool:
        """Validate model name."""
        allowed_models = {"gpt-3.5-turbo", "gpt-4", "claude-3-opus", "llama-3"}
        return model in allowed_models

    def validate_temperature(self, temp: float) -> bool:
        """Validate temperature parameter."""
        return 0.0 <= temp <= 2.0

    def validate_max_tokens(self, tokens: int) -> bool:
        """Validate max tokens parameter."""
        return 1 <= tokens <= 4096
```

### 5. API Monitoring and Logging

```python
import logging
import time
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class APIRequestLog:
    """Log entry for API request."""
    timestamp: datetime
    method: str
    path: str
    user_id: Optional[str]
    ip_address: str
    status_code: int
    response_time: float
    request_size: int
    response_size: int

class APIMonitor:
    """Monitor API usage and detect anomalies."""

    def __init__(self):
        self.request_logs: list = []
        self.user_stats: Dict[str, Dict] = defaultdict(lambda: {
            "requests": 0,
            "errors": 0,
            "last_request": None,
        })

    def log_request(self, log: APIRequestLog):
        """Log an API request."""
        self.request_logs.append(log)

        # Update user stats
        if log.user_id:
            stats = self.user_stats[log.user_id]
            stats["requests"] += 1
            if log.status_code >= 400:
                stats["errors"] += 1
            stats["last_request"] = log.timestamp

    def detect_anomalies(self, time_window_minutes: int = 5) -> list:
        """Detect anomalous API usage patterns."""
        anomalies = []
        now = datetime.utcnow()
        window_start = now.timestamp() - (time_window_minutes * 60)

        # Get recent requests
        recent_logs = [
            log for log in self.request_logs
            if log.timestamp.timestamp() > window_start
        ]

        # Check for unusual patterns
        user_request_counts = defaultdict(int)
        for log in recent_logs:
            if log.user_id:
                user_request_counts[log.user_id] += 1

        # Detect high request rates
        for user_id, count in user_request_counts.items():
            if count > 100:  # More than 100 requests in window
                anomalies.append({
                    "type": "high_request_rate",
                    "user_id": user_id,
                    "request_count": count,
                    "time_window": time_window_minutes,
                })

        # Detect high error rates
        for user_id, stats in self.user_stats.items():
            if stats["requests"] > 10:
                error_rate = stats["errors"] / stats["requests"]
                if error_rate > 0.5:  # More than 50% errors
                    anomalies.append({
                        "type": "high_error_rate",
                        "user_id": user_id,
                        "error_rate": error_rate,
                    })

        return anomalies

    def get_usage_stats(self, time_window_hours: int = 24) -> Dict:
        """Get API usage statistics."""
        now = datetime.utcnow()
        window_start = now.timestamp() - (time_window_hours * 3600)

        recent_logs = [
            log for log in self.request_logs
            if log.timestamp.timestamp() > window_start
        ]

        return {
            "total_requests": len(recent_logs),
            "unique_users": len(set(log.user_id for log in recent_logs if log.user_id)),
            "avg_response_time": sum(log.response_time for log in recent_logs) / len(recent_logs) if recent_logs else 0,
            "error_rate": sum(1 for log in recent_logs if log.status_code >= 400) / len(recent_logs) if recent_logs else 0,
        }

# Usage
monitor = APIMonitor()

# Log a request
log = APIRequestLog(
    timestamp=datetime.utcnow(),
    method="POST",
    path="/v1/chat/completions",
    user_id="user123",
    ip_address="192.168.1.100",
    status_code=200,
    response_time=0.5,
    request_size=100,
    response_size=500,
)
monitor.log_request(log)

# Check for anomalies
anomalies = monitor.detect_anomalies()
print(f"Anomalies detected: {len(anomalies)}")
```

---

## Common Mistakes to Avoid

1. **No rate limiting** — APIs can be abused without rate limits
2. **Over-exposing data** — Return only necessary fields
3. **Missing authentication** — All endpoints must require auth
4. **No input validation** — Validate all inputs server-side
5. **Hardcoded credentials** — Never hardcode secrets
6. **No HTTPS** — Always use TLS for API communications
7. **Verbose error messages** — Don't expose internal details
8. **No monitoring** — You can't protect what you don't monitor

---

## Best Practices

1. **Use API gateways** — Centralize security controls
2. **Implement rate limiting** — Prevent abuse and DoS
3. **Validate all inputs** — Use schema validation
4. **Apply least privilege** — Tokens should have minimal permissions
5. **Log everything** — For security monitoring and forensics
6. **Use HTTPS everywhere** — Encrypt all communications
7. **Implement CORS properly** — Control cross-origin access
8. **Regular security audits** — Test against OWASP Top 10

---

## Practice Exercises

### Exercise 1: Rate Limiter (Easy)
Implement a token bucket rate limiter for an API endpoint.

### Exercise 2: Input Validation (Medium)
Build a comprehensive input validation system for an AI API.

### Exercise 3: API Security Audit (Medium)
Audit an existing API against OWASP API Security Top 10.

### Exercise 4: Secure API Gateway (Hard)
Design and implement a secure API gateway for AI services.

---

## Summary

API security is critical for protecting AI services. Key takeaways:

- **Rate limiting prevents abuse** — Implement per-user and global limits
- **Follow OWASP Top 10** — Address common API vulnerabilities
- **Validate everything** — Input and output validation is essential
- **Monitor continuously** — Detect and respond to anomalies
- **Use API gateways** — Centralize security controls
- **Encrypt communications** — Always use HTTPS

---

## References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [API Security Best Practices](https://cloud.google.com/apis/design)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
