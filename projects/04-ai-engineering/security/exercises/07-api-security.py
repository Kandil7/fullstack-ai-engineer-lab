"""
=============================================================
Topic 07: API Security for AI Services
=============================================================

Security Level: ########-- High

Secure your AI APIs against common web vulnerabilities and abuse.
This exercise covers rate limiting, CORS configuration, HTTPS
enforcement, request validation, response sanitization, and
webhook verification.

Learning Objectives:
- Implement rate limiting with sliding window algorithms
- Configure CORS for AI service deployments
- Enforce HTTPS with HSTS
- Validate and sanitize all API inputs
- Protect against data leakage in responses
- Verify webhook authenticity

Prerequisites:
- Understanding of HTTP protocol
- Basic web application security concepts
- Familiarity with REST API design
=============================================================
"""

import hashlib
import hmac
import json
import re
import time
import secrets
import ipaddress
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse
from functools import wraps
import base64
import struct
import math


# =============================================================
# SECTION 1: Rate Limiting
# =============================================================

class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter for API protection.

    Uses a sliding window algorithm that combines the benefits of
    fixed windows (simple) and sliding logs (accurate) without
    the memory overhead of storing individual timestamps.
    """

    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        burst_limit: int = 10,
        burst_window: int = 1,  # seconds
    ):
        self.rpm = requests_per_minute
        self.rph = requests_per_hour
        self.burst_limit = burst_limit
        self.burst_window = burst_window
        self._windows: Dict[str, Dict] = defaultdict(lambda: {
            "minute": deque(),
            "hour": deque(),
            "burst": deque(),
        })

    def is_allowed(self, client_id: str, cost: int = 1) -> Dict:
        """
        Check if a request is allowed under rate limits.

        Args:
            client_id: Unique identifier for the client (IP, API key, etc.)
            cost: Cost of the request (default 1)

        Returns:
            Dict with allowed, remaining, retry_after, limits
        """
        now = time.time()
        window = self._windows[client_id]

        # Clean old entries
        self._cleanup(window["minute"], now - 60)
        self._cleanup(window["hour"], now - 3600)
        self._cleanup(window["burst"], now - self.burst_window)

        # Count current requests
        minute_count = sum(window["minute"])
        hour_count = sum(window["hour"])
        burst_count = sum(window["burst"])

        # Check limits
        if burst_count + cost > self.burst_limit:
            retry_after = self.burst_window - (now - window["burst"][0]) if window["burst"] else 0
            return {
                "allowed": False,
                "remaining": 0,
                "retry_after": max(0.1, retry_after),
                "limits": {"rpm": self.rpm, "rph": self.rph, "burst": self.burst_limit},
                "current": {"minute": minute_count, "hour": hour_count, "burst": burst_count},
                "reason": "burst_limit",
            }

        if minute_count + cost > self.rpm:
            retry_after = 60 - (now - window["minute"][0]) if window["minute"] else 60
            return {
                "allowed": False,
                "remaining": 0,
                "retry_after": max(1, retry_after),
                "limits": {"rpm": self.rpm, "rph": self.rph, "burst": self.burst_limit},
                "current": {"minute": minute_count, "hour": hour_count, "burst": burst_count},
                "reason": "minute_limit",
            }

        if hour_count + cost > self.rph:
            retry_after = 3600 - (now - window["hour"][0]) if window["hour"] else 3600
            return {
                "allowed": False,
                "remaining": 0,
                "retry_after": max(1, retry_after),
                "limits": {"rpm": self.rpm, "rph": self.rph, "burst": self.burst_limit},
                "current": {"minute": minute_count, "hour": hour_count, "burst": burst_count},
                "reason": "hour_limit",
            }

        # Record the request
        window["minute"].append(cost)
        window["hour"].append(cost)
        window["burst"].append(cost)

        return {
            "allowed": True,
            "remaining": {
                "minute": max(0, self.rpm - minute_count - cost),
                "hour": max(0, self.rph - hour_count - cost),
            },
            "retry_after": 0,
            "limits": {"rpm": self.rpm, "rph": self.rph, "burst": self.burst_limit},
            "current": {
                "minute": minute_count + cost,
                "hour": hour_count + cost,
                "burst": burst_count + cost,
            },
        }

    def _cleanup(self, window: deque, cutoff: float):
        """Remove entries older than cutoff from the window."""
        while window and window[0] < cutoff:
            # For our implementation, entries are costs, not timestamps
            # In a real implementation, we'd store (timestamp, cost) tuples
            window.popleft()


class TokenBucketRateLimiter:
    """
    Token bucket rate limiter -- allows bursts while maintaining
    average rate.
    """

    def __init__(
        self,
        capacity: int = 100,      # Max tokens
        refill_rate: float = 10,   # Tokens per second
    ):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._buckets: Dict[str, Dict] = {}

    def is_allowed(self, client_id: str, tokens: int = 1) -> Dict:
        """Check if request is allowed."""
        now = time.time()

        if client_id not in self._buckets:
            self._buckets[client_id] = {
                "tokens": self.capacity,
                "last_refill": now,
            }

        bucket = self._buckets[client_id]

        # Refill tokens
        elapsed = now - bucket["last_refill"]
        refill = elapsed * self.refill_rate
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + refill)
        bucket["last_refill"] = now

        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            return {
                "allowed": True,
                "remaining": int(bucket["tokens"]),
                "retry_after": 0,
            }
        else:
            wait_time = (tokens - bucket["tokens"]) / self.refill_rate
            return {
                "allowed": False,
                "remaining": 0,
                "retry_after": wait_time,
            }


class AdaptiveRateLimiter:
    """
    Adaptive rate limiter that adjusts limits based on client behavior.

    Clients with good behavior get higher limits; suspicious clients
    get stricter limits.
    """

    def __init__(self):
        self._client_scores: Dict[str, float] = defaultdict(lambda: 1.0)
        self._base_limits = {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "inference_per_minute": 20,
        }
        self._violations: Dict[str, List[float]] = defaultdict(list)

    def evaluate_request(self, client_id: str, request_type: str = "api") -> Dict:
        """Evaluate a request with adaptive limits."""
        score = self._client_scores[client_id]

        # Clean old violations
        now = time.time()
        self._violations[client_id] = [
            v for v in self._violations[client_id] if now - v < 3600
        ]

        # Calculate dynamic limits based on score
        multiplier = min(2.0, max(0.1, score))
        limits = {
            k: int(v * multiplier)
            for k, v in self._base_limits.items()
        }

        return {
            "client_id": client_id,
            "score": score,
            "multiplier": multiplier,
            "limits": limits,
            "violations_last_hour": len(self._violations[client_id]),
        }

    def record_violation(self, client_id: str):
        """Record a rate limit violation."""
        self._violations[client_id].append(time.time())
        # Decrease score
        violations = len(self._violations[client_id])
        self._client_scores[client_id] = max(0.1, 1.0 - (violations * 0.1))

    def record_good_behavior(self, client_id: str):
        """Reward good behavior."""
        current = self._client_scores[client_id]
        self._client_scores[client_id] = min(2.0, current + 0.01)


# =============================================================
# SECTION 2: CORS Configuration
# =============================================================

class CORSPolicy:
    """
    Configurable CORS policy for AI service APIs.

    Security-first approach with explicit allowlists.
    """

    def __init__(self):
        self._allowed_origins: Set[str] = set()
        self._allowed_methods: Set[str] = {"GET", "POST", "OPTIONS"}
        self._allowed_headers: Set[str] = {
            "Authorization",
            "Content-Type",
            "X-Request-ID",
            "X-API-Key",
        }
        self._exposed_headers: Set[str] = {
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-Request-ID",
        }
        self._allow_credentials: bool = False
        self._max_age: int = 86400  # 24 hours
        self._allow_subdomains: bool = False

    def allow_origin(self, origin: str, allow_subdomains: bool = False):
        """Add an allowed origin."""
        # Validate origin format
        parsed = urlparse(origin)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid origin scheme: {parsed.scheme}")
        if not parsed.hostname:
            raise ValueError(f"Invalid origin: {origin}")

        self._allowed_origins.add(origin)
        self._allow_subdomains = allow_subdomains

    def allow_origin_pattern(self, pattern: str):
        """Add an allowed origin pattern (regex)."""
        # Store patterns for matching
        if not hasattr(self, "_origin_patterns"):
            self._origin_patterns = []
        self._origin_patterns.append(re.compile(pattern))

    def set_allowed_methods(self, methods: List[str]):
        """Set allowed HTTP methods."""
        valid_methods = {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}
        self._allowed_methods = set(m.upper() for m in methods) & valid_methods

    def set_allowed_headers(self, headers: List[str]):
        """Set allowed request headers."""
        self._allowed_headers = set(h.lower() for h in headers)

    def check_origin(self, origin: Optional[str], request_method: str = "GET") -> Dict:
        """
        Check if an origin is allowed and return CORS headers.

        Returns:
            Dict with allowed, headers, and error if not allowed
        """
        if not origin:
            # No origin header (same-origin or non-browser request)
            return {"allowed": True, "headers": {}, "note": "no_origin"}

        # Normalize origin
        origin = origin.strip().rstrip("/")

        # Check exact match
        if origin in self._allowed_origins:
            return self._build_cors_response(origin)

        # Check subdomains
        if self._allow_subdomains:
            parsed = urlparse(origin)
            for allowed in self._allowed_origins:
                allowed_parsed = urlparse(allowed)
                if (parsed.hostname and allowed_parsed.hostname and
                        parsed.hostname.endswith("." + allowed_parsed.hostname)):
                    return self._build_cors_response(origin)

        # Check patterns
        if hasattr(self, "_origin_patterns"):
            for pattern in self._origin_patterns:
                if pattern.match(origin):
                    return self._build_cors_response(origin)

        # Origin not allowed
        return {
            "allowed": False,
            "headers": {},
            "error": f"Origin not allowed: {origin}",
        }

    def _build_cors_response(self, origin: str) -> Dict:
        """Build CORS response headers."""
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": ", ".join(sorted(self._allowed_methods)),
            "Access-Control-Allow-Headers": ", ".join(sorted(self._allowed_headers)),
            "Access-Control-Expose-Headers": ", ".join(sorted(self._exposed_headers)),
            "Access-Control-Max-Age": str(self._max_age),
        }

        if self._allow_credentials:
            headers["Access-Control-Allow-Credentials"] = "true"

        return {"allowed": True, "headers": headers}


# =============================================================
# SECTION 3: HTTPS Enforcement
# =============================================================

class HTTPSEnforcer:
    """
    HTTPS enforcement with HSTS and redirect handling.
    """

    def __init__(
        self,
        max_age: int = 31536000,  # 1 year
        include_subdomains: bool = True,
        preload: bool = True,
    ):
        self.hsts_max_age = max_age
        self.include_subdomains = include_subdomains
        self.preload = preload
        self._trusted_proxies: Set[str] = set()

    def add_trusted_proxy(self, proxy_ip: str):
        """Add a trusted reverse proxy IP."""
        self._trusted_proxies.add(proxy_ip)

    def get_hsts_header(self) -> str:
        """Generate the HSTS header value."""
        directives = [f"max-age={self.hsts_max_age}"]
        if self.include_subdomains:
            directives.append("includeSubDomains")
        if self.preload:
            directives.append("preload")
        return "; ".join(directives)

    def check_request(self, request: Dict) -> Dict:
        """
        Check if request should be redirected to HTTPS.

        Args:
            request: Dict with scheme, host, path, headers, client_ip

        Returns:
            Dict with redirect_needed, redirect_url, headers
        """
        scheme = request.get("scheme", "http")
        host = request.get("host", "")
        path = request.get("path", "/")
        client_ip = request.get("client_ip", "")

        # If already HTTPS, just add HSTS header
        if scheme == "https":
            return {
                "redirect_needed": False,
                "headers": {
                    "Strict-Transport-Security": self.get_hsts_header(),
                },
            }

        # Check if request is from a trusted proxy
        if client_ip in self._trusted_proxies:
            # Behind proxy -- check X-Forwarded-Proto
            forwarded_proto = request.get("headers", {}).get("X-Forwarded-Proto", "https")
            if forwarded_proto == "https":
                return {
                    "redirect_needed": False,
                    "headers": {
                        "Strict-Transport-Security": self.get_hsts_header(),
                    },
                }

        # Build redirect URL
        redirect_url = f"https://{host}{path}"

        return {
            "redirect_needed": True,
            "redirect_url": redirect_url,
            "status_code": 301,
            "headers": {
                "Location": redirect_url,
                "Strict-Transport-Security": self.get_hsts_header(),
            },
        }


# =============================================================
# SECTION 4: Request Validation
# =============================================================

class RequestValidator:
    """
    Comprehensive request validation for API security.

    Features:
    - JSON schema validation
    - Input sanitization
    - SQL injection prevention
    - XSS prevention
    - Path traversal prevention
    """

    def __init__(self):
        self._max_body_size = 10 * 1024 * 1024  # 10MB
        self._max_url_length = 2048
        self._blocked_patterns = [
            # SQL injection patterns
            re.compile(r"(?i)(union\s+select|insert\s+into|drop\s+table|delete\s+from)"),
            re.compile(r"(?i)(--\s|;\s*drop|;\s*delete|;\s*update)"),
            # XSS patterns
            re.compile(r"<script[^>]*>", re.IGNORECASE),
            re.compile(r"javascript:", re.IGNORECASE),
            re.compile(r"on\w+\s*=", re.IGNORECASE),
            # Path traversal
            re.compile(r"\.\./"),
            re.compile(r"\.\.\\"),
            # Command injection
            re.compile(r"[;&|`$]"),
        ]

    def validate_request(self, request: Dict) -> Dict:
        """
        Validate a complete request.

        Args:
            request: Dict with method, path, headers, body, query_params

        Returns:
            Dict with valid, errors, sanitized_request
        """
        errors = []
        sanitized = request.copy()

        # Validate method
        if request.get("method") not in ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"):
            errors.append("Invalid HTTP method")

        # Validate URL length
        url = request.get("path", "")
        if len(url) > self._max_url_length:
            errors.append(f"URL too long: {len(url)} > {self._max_url_length}")

        # Validate body size
        body = request.get("body", "")
        if isinstance(body, str) and len(body) > self._max_body_size:
            errors.append(f"Body too large: {len(body)} > {self._max_body_size}")

        # Check for blocked patterns
        check_strings = [url, str(body)]
        for header_val in request.get("headers", {}).values():
            check_strings.append(str(header_val))

        for check_str in check_strings:
            for pattern in self._blocked_patterns:
                if pattern.search(check_str):
                    errors.append(f"Blocked pattern detected: {pattern.pattern}")
                    break

        # Validate query parameters
        query_params = request.get("query_params", {})
        for key, value in query_params.items():
            if isinstance(value, str):
                for pattern in self._blocked_patterns:
                    if pattern.search(value):
                        errors.append(f"Blocked pattern in query param '{key}'")
                        break

        # Sanitize inputs
        sanitized["path"] = self._sanitize_string(url)
        if isinstance(sanitized.get("body"), str):
            sanitized["body"] = self._sanitize_string(sanitized["body"])

        # Validate JSON content type for POST/PUT/PATCH
        method = request.get("method", "")
        content_type = request.get("headers", {}).get("content-type", "")
        if method in ("POST", "PUT", "PATCH"):
            if "application/json" not in content_type and "multipart/form-data" not in content_type:
                errors.append(f"Invalid content type for {method}: {content_type}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "sanitized_request": sanitized,
        }

    def _sanitize_string(self, value: str) -> str:
        """Sanitize a string input."""
        # Remove null bytes
        value = value.replace("\x00", "")
        # Encode HTML entities
        value = value.replace("&", "&amp;")
        value = value.replace("<", "&lt;")
        value = value.replace(">", "&gt;")
        value = value.replace('"', "&quot;")
        value = value.replace("'", "&#x27;")
        return value

    def validate_json_body(self, body: Any, schema: Dict) -> Dict:
        """
        Validate JSON body against a simple schema.

        Schema format:
        {
            "field_name": {"type": "string", "required": True, "max_length": 100},
            "field_name2": {"type": "integer", "required": False, "min": 0, "max": 100},
        }
        """
        errors = []

        if not isinstance(body, dict):
            return {"valid": False, "errors": ["Body must be a JSON object"]}

        for field_name, rules in schema.items():
            value = body.get(field_name)

            # Check required
            if rules.get("required", False) and value is None:
                errors.append(f"Missing required field: {field_name}")
                continue

            if value is None:
                continue

            # Check type
            expected_type = rules.get("type")
            if expected_type == "string" and not isinstance(value, str):
                errors.append(f"Field '{field_name}' must be a string")
            elif expected_type == "integer" and not isinstance(value, int):
                errors.append(f"Field '{field_name}' must be an integer")
            elif expected_type == "number" and not isinstance(value, (int, float)):
                errors.append(f"Field '{field_name}' must be a number")
            elif expected_type == "boolean" and not isinstance(value, bool):
                errors.append(f"Field '{field_name}' must be a boolean")
            elif expected_type == "array" and not isinstance(value, list):
                errors.append(f"Field '{field_name}' must be an array")

            # String constraints
            if isinstance(value, str):
                if "max_length" in rules and len(value) > rules["max_length"]:
                    errors.append(f"Field '{field_name}' exceeds max length: {len(value)} > {rules['max_length']}")
                if "pattern" in rules and not re.match(rules["pattern"], value):
                    errors.append(f"Field '{field_name}' doesn't match pattern: {rules['pattern']}")
                if "enum" in rules and value not in rules["enum"]:
                    errors.append(f"Field '{field_name}' must be one of: {rules['enum']}")

            # Number constraints
            if isinstance(value, (int, float)):
                if "min" in rules and value < rules["min"]:
                    errors.append(f"Field '{field_name}' is below minimum: {value} < {rules['min']}")
                if "max" in rules and value > rules["max"]:
                    errors.append(f"Field '{field_name}' exceeds maximum: {value} > {rules['max']}")

            # Array constraints
            if isinstance(value, list):
                if "max_items" in rules and len(value) > rules["max_items"]:
                    errors.append(f"Field '{field_name}' exceeds max items: {len(value)} > {rules['max_items']}")
                if "item_type" in rules:
                    for i, item in enumerate(value):
                        if rules["item_type"] == "string" and not isinstance(item, str):
                            errors.append(f"Field '{field_name}[{i}]' must be a string")

        return {"valid": len(errors) == 0, "errors": errors}


# =============================================================
# SECTION 5: Response Sanitization
# =============================================================

class ResponseSanitizer:
    """
    Protect against data leakage in API responses.

    Features:
    - Remove sensitive fields
    - Mask PII data
    - Prevent internal error details leakage
    - Safe error messages
    """

    SENSITIVE_FIELDS = {
        "password", "password_hash", "secret", "api_key", "api_secret",
        "access_token", "refresh_token", "private_key", "credit_card",
        "ssn", "social_security", "bank_account", "routing_number",
    }

    PII_FIELDS = {
        "email", "phone", "address", "ssn", "credit_card",
        "date_of_birth", "full_name",
    }

    INTERNAL_ERROR_MESSAGES = {
        "database error",
        "connection refused",
        "permission denied",
        "file not found",
        "null pointer",
        "stack trace",
        "traceback",
    }

    def __init__(self):
        self._masking_rules: Dict[str, Callable] = {}

    def sanitize_response(self, data: Any, context: str = "api") -> Any:
        """Sanitize response data based on context."""
        if isinstance(data, dict):
            return self._sanitize_dict(data, context)
        elif isinstance(data, list):
            return [self.sanitize_response(item, context) for item in data]
        elif isinstance(data, str):
            return self._sanitize_string_response(data)
        return data

    def _sanitize_dict(self, data: Dict, context: str) -> Dict:
        """Sanitize dictionary response."""
        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()

            # Remove sensitive fields
            if key_lower in self.SENSITIVE_FIELDS:
                continue

            # Mask PII fields
            if key_lower in self.PII_FIELDS and isinstance(value, str):
                sanitized[key] = self._mask_pii(key_lower, value)
            elif isinstance(value, (dict, list)):
                sanitized[key] = self.sanitize_response(value, context)
            else:
                sanitized[key] = value

        return sanitized

    def _sanitize_string_response(self, value: str) -> str:
        """Sanitize string response to prevent XSS."""
        # Remove HTML tags
        value = re.sub(r"<[^>]+>", "", value)
        # Remove javascript: protocol
        value = re.sub(r"javascript:", "", value, flags=re.IGNORECASE)
        return value

    def _mask_pii(self, field_type: str, value: str) -> str:
        """Mask PII data."""
        if field_type == "email":
            if "@" in value:
                local, domain = value.split("@", 1)
                masked_local = local[0] + "***" + local[-1] if len(local) > 1 else "***"
                return f"{masked_local}@{domain}"
            return "***@***"

        elif field_type == "phone":
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 10:
                return f"({digits[:3]}) ***-**{digits[-2:]}"
            return "***"

        elif field_type == "credit_card":
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 16:
                return f"****-****-****-{digits[-4:]}"
            return "****"

        elif field_type == "ssn":
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 4:
                return f"***-**-{digits[-4:]}"
            return "***"

        return "***"

    def sanitize_error(self, error: Exception, include_details: bool = False) -> Dict:
        """
        Create a safe error response that doesn't leak internals.
        """
        error_msg = str(error).lower()

        # Check for internal error patterns
        is_internal = any(pattern in error_msg for pattern in self.INTERNAL_ERROR_MESSAGES)

        if is_internal or not include_details:
            return {
                "error": "An internal error occurred",
                "error_code": "INTERNAL_ERROR",
                "request_id": str(secrets.token_urlsafe(16)),
            }

        return {
            "error": str(error)[:200],  # Limit error message length
            "error_code": "VALIDATION_ERROR",
        }

    def add_masking_rule(self, field_name: str, mask_func: Callable):
        """Add custom masking rule for a field."""
        self._masking_rules[field_name.lower()] = mask_func


# =============================================================
# SECTION 6: Webhook Verification
# =============================================================

class WebhookVerifier:
    """
    Verify webhook authenticity using HMAC signatures.

    Supports:
    - HMAC-SHA256 signatures
    - Timestamp verification (replay protection)
    - Multiple signature algorithms
    """

    def __init__(self, secret: bytes, tolerance: int = 300):
        """
        Args:
            secret: Webhook signing secret
            tolerance: Max age of webhook in seconds (default 5 min)
        """
        self.secret = secret
        self.tolerance = tolerance
        self._processed_events: Set[str] = set()

    def generate_signature(
        self,
        payload: bytes,
        timestamp: Optional[int] = None,
        algorithm: str = "sha256",
    ) -> str:
        """Generate a webhook signature."""
        if timestamp is None:
            timestamp = int(time.time())

        # Create signed payload
        signed_payload = f"{timestamp}.{payload.decode('utf-8', errors='replace')}"
        signature = hmac.new(
            self.secret,
            signed_payload.encode(),
            getattr(hashlib, algorithm),
        ).hexdigest()

        return f"t={timestamp},{algorithm}={signature}"

    def verify_signature(
        self,
        payload: bytes,
        signature_header: str,
        algorithm: str = "sha256",
    ) -> Dict:
        """
        Verify a webhook signature.

        Args:
            payload: Raw request body
            signature_header: Value from signature header
            algorithm: Hash algorithm

        Returns:
            Dict with valid, error, timestamp
        """
        try:
            # Parse signature header
            parts = {}
            for part in signature_header.split(","):
                if "=" in part:
                    key, value = part.split("=", 1)
                    parts[key.strip()] = value.strip()

            timestamp = int(parts.get("t", 0))
            expected_sig = parts.get(algorithm, "")

            if not timestamp or not expected_sig:
                return {"valid": False, "error": "Invalid signature format"}

            # Check timestamp tolerance
            current_time = int(time.time())
            if abs(current_time - timestamp) > self.tolerance:
                return {
                    "valid": False,
                    "error": f"Webhook timestamp outside tolerance: {abs(current_time - timestamp)}s",
                }

            # Compute expected signature
            signed_payload = f"{timestamp}.{payload.decode('utf-8', errors='replace')}"
            computed_sig = hmac.new(
                self.secret,
                signed_payload.encode(),
                getattr(hashlib, algorithm),
            ).hexdigest()

            # Constant-time comparison
            if not hmac.compare_digest(computed_sig, expected_sig):
                return {"valid": False, "error": "Signature mismatch"}

            # Check for replay
            event_id = f"{timestamp}:{computed_sig[:16]}"
            if event_id in self._processed_events:
                return {"valid": False, "error": "Duplicate webhook (replay detected)"}

            self._processed_events.add(event_id)

            return {
                "valid": True,
                "timestamp": timestamp,
                "algorithm": algorithm,
            }

        except Exception as e:
            return {"valid": False, "error": f"Verification error: {e}"}


# =============================================================
# SECTION 7: Security Headers Middleware
# =============================================================

class SecurityHeaders:
    """
    Security headers for API responses.

    Implements OWASP recommended security headers.
    """

    def __init__(self):
        self._custom_headers: Dict[str, str] = {}

    def get_security_headers(self, request: Dict) -> Dict[str, str]:
        """Get all security headers for a response."""
        headers = {
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            # Clickjacking protection
            "X-Frame-Options": "DENY",
            # XSS protection (legacy browsers)
            "X-XSS-Protection": "1; mode=block",
            # Content Security Policy
            "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # Permissions policy
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            # Cache control for sensitive endpoints
            "Cache-Control": "no-store, no-cache, must-revalidate, private",
            "Pragma": "no-cache",
            # Prevent information leakage
            "Server": "AI-Platform",
            "X-Powered-By": "",  # Remove framework info
        }

        # Add custom headers
        headers.update(self._custom_headers)

        return headers

    def add_custom_header(self, name: str, value: str):
        """Add a custom security header."""
        self._custom_headers[name] = value


# =============================================================
# SECTION 8: Request Signing
# =============================================================

class RequestSigner:
    """
    Sign API requests for mutual TLS alternative.

    Uses HMAC-SHA256 to sign request components.
    """

    def __init__(self, api_secret: bytes):
        self.api_secret = api_secret

    def sign_request(
        self,
        method: str,
        path: str,
        body: bytes,
        timestamp: Optional[int] = None,
    ) -> Dict[str, str]:
        """Generate request signature and headers."""
        if timestamp is None:
            timestamp = int(time.time())

        # Create string to sign
        string_to_sign = f"{method}\n{path}\n{timestamp}\n{body.decode('utf-8', errors='replace')}"
        signature = hmac.new(
            self.api_secret,
            string_to_sign.encode(),
            hashlib.sha256,
        ).hexdigest()

        return {
            "X-Signature": signature,
            "X-Timestamp": str(timestamp),
            "X-API-Version": "2024-01-01",
        }

    def verify_request(
        self,
        method: str,
        path: str,
        body: bytes,
        headers: Dict[str, str],
        tolerance: int = 300,
    ) -> Dict:
        """Verify a request signature."""
        signature = headers.get("X-Signature", "")
        timestamp = int(headers.get("X-Timestamp", "0"))

        if not signature or not timestamp:
            return {"valid": False, "error": "Missing signature headers"}

        # Check timestamp
        if abs(time.time() - timestamp) > tolerance:
            return {"valid": False, "error": "Request timestamp expired"}

        # Compute expected signature
        string_to_sign = f"{method}\n{path}\n{timestamp}\n{body.decode('utf-8', errors='replace')}"
        expected = hmac.new(
            self.api_secret,
            string_to_sign.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            return {"valid": False, "error": "Invalid signature"}

        return {"valid": True, "timestamp": timestamp}


# =============================================================
# DEMONSTRATIONS
# =============================================================

def demo_rate_limiting():
    """Demonstrate rate limiting."""
    print("\n" + "=" * 60)
    print("DEMO 1: Rate Limiting")
    print("=" * 60)

    # Sliding window rate limiter
    limiter = SlidingWindowRateLimiter(
        requests_per_minute=5,
        requests_per_hour=100,
        burst_limit=3,
        burst_window=1,
    )

    print("Testing sliding window limiter (5 RPM, 3 burst):")
    for i in range(7):
        result = limiter.is_allowed("client_1")
        status = "[OK]" if result["allowed"] else "[FAIL]"
        print(f"  Request {i+1}: {status} remaining_minute={result['remaining'].get('minute', 'N/A')}")

    # Token bucket
    print("\nToken bucket limiter (capacity=5, refill=2/s):")
    bucket = TokenBucketRateLimiter(capacity=5, refill_rate=2)
    for i in range(8):
        result = bucket.is_allowed("client_2")
        status = "[OK]" if result["allowed"] else "[FAIL]"
        remaining = result["remaining"] if result["allowed"] else 0
        print(f"  Request {i+1}: {status} tokens_remaining={remaining}")

    print("\n[OK] Rate limiting demonstrated")


def demo_cors():
    """Demonstrate CORS configuration."""
    print("\n" + "=" * 60)
    print("DEMO 2: CORS Configuration")
    print("=" * 60)

    cors = CORSPolicy()
    cors.allow_origin("https://app.ai-platform.com")
    cors.allow_origin("https://admin.ai-platform.com")
    cors.set_allowed_methods(["GET", "POST", "PUT", "DELETE"])
    cors.set_allowed_headers(["Authorization", "Content-Type", "X-API-Key"])

    # Test allowed origin
    result = cors.check_origin("https://app.ai-platform.com")
    print(f"Origin https://app.ai-platform.com: {'[OK]' if result['allowed'] else '[FAIL]'}")

    # Test disallowed origin
    result = cors.check_origin("https://evil-site.com")
    print(f"Origin https://evil-site.com: {'[OK]' if result['allowed'] else '[FAIL]'}")

    # Test no origin (server-to-server)
    result = cors.check_origin(None)
    print(f"No origin (server-to-server): {'[OK]' if result['allowed'] else '[FAIL]'}")

    if "headers" in result and result["headers"]:
        print(f"CORS Headers: {json.dumps(result['headers'], indent=2)}")

    print("\n[OK] CORS configuration demonstrated")


def demo_request_validation():
    """Demonstrate request validation."""
    print("\n" + "=" * 60)
    print("DEMO 3: Request Validation")
    print("=" * 60)

    validator = RequestValidator()

    # Test normal request
    result = validator.validate_request({
        "method": "POST",
        "path": "/api/v1/models",
        "headers": {"Content-Type": "application/json"},
        "body": '{"name": "my-model"}',
    })
    print(f"Normal request: {'[OK] Valid' if result['valid'] else '[FAIL] Invalid'}")
    if result["errors"]:
        print(f"  Errors: {result['errors']}")

    # Test SQL injection
    result = validator.validate_request({
        "method": "GET",
        "path": "/api/v1/models?id=1' OR '1'='1",
        "headers": {},
    })
    print(f"SQL injection attempt: {'[OK] Valid' if result['valid'] else '[FAIL] Blocked'}")

    # Test XSS
    result = validator.validate_request({
        "method": "POST",
        "path": "/api/v1/chat",
        "headers": {"Content-Type": "application/json"},
        "body": '<script>alert("xss")</script>',
    })
    print(f"XSS attempt: {'[OK] Valid' if result['valid'] else '[FAIL] Blocked'}")

    # Test path traversal
    result = validator.validate_request({
        "method": "GET",
        "path": "/api/v1/files?path=../../etc/passwd",
        "headers": {},
    })
    print(f"Path traversal attempt: {'[OK] Valid' if result['valid'] else '[FAIL] Blocked'}")

    # JSON schema validation
    print("\nJSON Body Validation:")
    schema = {
        "model_name": {"type": "string", "required": True, "max_length": 100, "pattern": r"^[a-zA-Z0-9_-]+$"},
        "temperature": {"type": "number", "required": False, "min": 0.0, "max": 2.0},
        "max_tokens": {"type": "integer", "required": False, "min": 1, "max": 4096},
    }

    valid_body = {"model_name": "gpt-4", "temperature": 0.7, "max_tokens": 1000}
    result = validator.validate_json_body(valid_body, schema)
    print(f"Valid body: {'[OK]' if result['valid'] else '[FAIL]'} {result['errors']}")

    invalid_body = {"model_name": "gpt/4", "temperature": 5.0}
    result = validator.validate_json_body(invalid_body, schema)
    print(f"Invalid body: {'[OK]' if result['valid'] else '[FAIL]'} {result['errors']}")

    print("\n[OK] Request validation demonstrated")


def demo_response_sanitization():
    """Demonstrate response sanitization."""
    print("\n" + "=" * 60)
    print("DEMO 4: Response Sanitization")
    print("=" * 60)

    sanitizer = ResponseSanitizer()

    # Test data masking
    sensitive_data = {
        "user_id": "12345",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-123-4567",
        "credit_card": "4111-1111-1111-1234",
        "password": "super_secret_123",
        "api_key": "sk_live_abcdef123456",
        "model_output": "The answer is 42",
    }

    sanitized = sanitizer.sanitize_response(sensitive_data)
    print("Original vs Sanitized:")
    for key in sensitive_data:
        original = sensitive_data[key]
        masked = sanitized.get(key, "REMOVED")
        print(f"  {key}: {original} -> {masked}")

    # Test error sanitization
    print("\nError Sanitization:")
    db_error = Exception("Connection refused to database at 10.0.0.5:5432")
    safe_error = sanitizer.sanitize_error(db_error, include_details=False)
    print(f"  DB error (safe): {json.dumps(safe_error, indent=4)}")

    validation_error = Exception("Invalid email format")
    safe_error = sanitizer.sanitize_error(validation_error, include_details=True)
    print(f"  Validation error: {json.dumps(safe_error, indent=4)}")

    print("\n[OK] Response sanitization demonstrated")


def demo_webhook_verification():
    """Demonstrate webhook verification."""
    print("\n" + "=" * 60)
    print("DEMO 5: Webhook Verification")
    print("=" * 60)

    secret = secrets.token_bytes(32)
    verifier = WebhookVerifier(secret, tolerance=300)

    # Generate signature
    payload = json.dumps({"event": "model.updated", "model_id": "12345"}).encode()
    timestamp = int(time.time())
    signature = verifier.generate_signature(payload, timestamp)
    print(f"Generated signature: {signature[:50]}...")

    # Verify valid signature
    result = verifier.verify_signature(payload, signature)
    print(f"Valid webhook: {'[OK]' if result['valid'] else '[FAIL]'}")

    # Verify tampered payload
    tampered_payload = payload + b"tampered"
    result = verifier.verify_signature(tampered_payload, signature)
    print(f"Tampered payload: {'[OK]' if result['valid'] else '[FAIL]'} {result.get('error', '')}")

    # Verify replayed webhook
    result = verifier.verify_signature(payload, signature)
    print(f"Replayed webhook: {'[OK]' if result['valid'] else '[FAIL]'} {result.get('error', '')}")

    # Request signing
    print("\nRequest Signing:")
    signer = RequestSigner(secret)
    signed_headers = signer.sign_request("POST", "/api/v1/inference", payload)
    print(f"Signed headers: {json.dumps(signed_headers, indent=2)}")

    # Verify signed request
    result = signer.verify_request("POST", "/api/v1/inference", payload, signed_headers)
    print(f"Valid signed request: {'[OK]' if result['valid'] else '[FAIL]'}")

    print("\n[OK] Webhook verification demonstrated")


# =============================================================
# ATTACK PATTERNS & DEFENSES
# =============================================================

ATTACK_PATTERNS = """
+==============================================================+
|              COMMON API SECURITY ATTACKS                     |
+==============================================================+
|                                                              |
|  1. RATE LIMIT BYPASS                                        |
|     Attack: Rotate IPs, use distributed requests            |
|     Defense: Sliding window + per-API-key + global limits   |
|                                                              |
|  2. CORS MISCONFIGURATION                                   |
|     Attack: Access-Control-Allow-Origin: *                   |
|     Defense: Explicit origin allowlist, no wildcards         |
|                                                              |
|  3. HTTP REQUEST SMUGGLING                                   |
|     Attack: Exploit parser differentials between proxies     |
|     Defense: Normalize requests, consistent parsing          |
|                                                              |
|  4. SERVER-SIDE REQUEST FORGERY (SSRF)                       |
|     Attack: Make server fetch internal resources             |
|     Defense: URL validation, network segmentation            |
|                                                              |
|  5. API ABUSE / DATA SCRAPING                                |
|     Attack: Automated bulk data extraction                   |
|     Defense: Rate limits, CAPTCHA, usage monitoring          |
|                                                              |
|  6. PAYLOAD SIZE ATTACK                                      |
|     Attack: Send extremely large requests                    |
|     Defense: Request size limits, streaming validation       |
|                                                              |
|  7. HEADER INJECTION                                         |
|     Attack: Inject malicious headers                         |
|     Defense: Header validation, sanitization                 |
|                                                              |
|  8. ENDPOINT ENUMERATION                                     |
|     Attack: Probe for hidden endpoints                       |
|     Defense: Consistent error responses, rate limit probes   |
|                                                              |
+==============================================================+
"""

BEST_PRACTICES = """
+==============================================================+
|               API SECURITY BEST PRACTICES                    |
+==============================================================+
|                                                              |
|  RATE LIMITING:                                              |
|  [OK] Use sliding window or token bucket algorithms             |
|  [OK] Apply limits at multiple levels (global, user, endpoint) |
|  [OK] Return 429 status with Retry-After header                |
|  [OK] Use adaptive limits for known clients                     |
|                                                              |
|  CORS:                                                       |
|  [OK] Use explicit origin allowlists                            |
|  [OK] Never use Access-Control-Allow-Origin: *                  |
|  [OK] Limit exposed headers                                     |
|  [OK] Use credentials only with specific origins                |
|                                                              |
|  REQUEST VALIDATION:                                         |
|  [OK] Validate ALL input (query, body, headers)                |
|  [OK] Use schema validation for structured data                 |
|  [OK] Implement content-type checking                           |
|  [OK] Block known attack patterns                               |
|                                                              |
|  RESPONSE SECURITY:                                          |
|  [OK] Remove sensitive fields from responses                    |
|  [OK] Mask PII data                                             |
|  [OK] Use safe error messages (no stack traces)                |
|  [OK] Set appropriate cache headers                             |
|                                                              |
+==============================================================+
"""


# =============================================================
# MAIN EXECUTION
# =============================================================

if __name__ == "__main__":
    print("+==============================================================+")
    print("|       Topic 07: API Security for AI Services                |")
    print("+==============================================================+")

    try:
        demo_rate_limiting()
        demo_cors()
        demo_request_validation()
        demo_response_sanitization()
        demo_webhook_verification()

        print(ATTACK_PATTERNS)
        print(BEST_PRACTICES)

        print("\n" + "=" * 60)
        print("[OK] ALL API SECURITY DEMOS COMPLETED")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
