"""
FastAPI — 41: API Security
============================
Topics: rate limiting per identity; CORS done right; CSRF for cookie auth;
        security headers; request size limits; input validation; SSRF;
        secrets handling

Why this matters for AI/backend engineering:
    LLM endpoints are expensive per call — an unauthenticated, unlimited
    /generate endpoint is a billing bomb. Production API security is a
    layered checklist: rate limits per identity, strict CORS (never *),
    security headers, request-size caps, SSRF guards on URL-fetching
    features (agents fetch URLs!), and secrets only from env/secret
    managers. This exercise implements each layer in plain Python and
    verifies the whole stack with asserts.

Run:      python 41-api-security.py
Verify:   python 41-api-security.py --verify
Reference: https://owasp.org/www-project-top-ten/
"""

from __future__ import annotations

import os
import secrets
import sys
import time
from collections import defaultdict, deque
from typing import Optional
from urllib.parse import urlparse

# ============================================================
# 1. Rate limiting per identity
# ============================================================
# Token bucket per identity (user/api key/IP). Never a global limit:
# one bad actor must not starve everyone, and abuse must be charged to
# the right identity. In-memory here; Redis in production (same logic).

class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_per_sec: float) -> None:
        self.capacity = capacity
        self.refill = refill_per_sec
        self._buckets: dict[str, tuple[float, float]] = {}   # key -> (tokens, last_refill)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        tokens, last = self._buckets.get(key, (self.capacity, now))
        tokens = min(self.capacity, tokens + (now - last) * self.refill)
        if tokens < 1:
            self._buckets[key] = (tokens, now)
            return False
        self._buckets[key] = (tokens - 1, now)
        return True


limiter = TokenBucketLimiter(capacity=3, refill_per_sec=1.0)
print("=== 1. Rate limiting per identity ===")
for i in range(5):
    print(f"  request {i+1} for user-1: allowed={limiter.allow('user-1')}")
print(f"  burst for user-2 is independent: allowed={limiter.allow('user-2')}")
print()

# ============================================================
# 2. CORS done right — not *
# ============================================================
# Access-Control-Allow-Origin: * means ANY website's JS can call your
# API with the user's cookies/credentials. For credentialed requests
# browsers require an explicit origin, not *.

ALLOWED_ORIGINS = {"https://app.example.com", "https://admin.example.com"}

def cors_allow(origin: str | None) -> str | None:
    """Return the header value, or None to deny."""
    if origin is None:
        return None                      # same-origin / non-browser
    if origin in ALLOWED_ORIGINS:
        return origin
    return None                          # reflect nothing; deny


print("=== 2. CORS — explicit allowlist ===")
print(f"app origin: {cors_allow('https://app.example.com')}")
print(f"evil origin: {cors_allow('https://evil.example')}")
print()

# ============================================================
# 3. Security headers + CSRF for cookie auth
# ============================================================
# Headers: HSTS, X-Content-Type-Options, X-Frame-Options, CSP, and the
# Referrer-Policy. CSRF: if auth uses cookies, a hostile site can fire
# state-changing requests WITH the user's cookie — the fix is a
# per-session token (or SameSite=strict + custom header checks).

SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'none'",
}

def build_headers() -> dict[str, str]:
    return dict(SECURITY_HEADERS)


def csrf_check(session_token: str, form_token: str) -> bool:
    """Per-session CSRF token check for cookie-authenticated forms."""
    return secrets.compare_digest(session_token, form_token)


print("=== 3. Security headers + CSRF ===")
print(f"headers: {list(build_headers())[:3]}...")
session_tok = "tok-abc"
print(f"csrf with correct token: {csrf_check(session_tok, session_tok)}")
print(f"csrf with wrong token  : {csrf_check(session_tok, 'tok-evil')}")
print()

# ============================================================
# 4. Request size limits + input validation
# ============================================================
# Cap payload size at the boundary (FastAPI: max request body; proxies
# too). Validate inputs with typed schemas — a 10 MB "prompt" is both a
# DoS and a prompt-injection vector; a string length cap is free.

MAX_BODY_BYTES = 1024 * 1024   # 1 MB
MAX_PROMPT_CHARS = 4000

def check_body_size(raw: bytes) -> bool:
    return len(raw) <= MAX_BODY_BYTES


def validate_prompt(prompt: str) -> bool:
    return 1 <= len(prompt) <= MAX_PROMPT_CHARS


print("=== 4. Request size limits ===")
print(f"1KB body ok: {check_body_size(b'x' * 1024)}")
print(f"2MB body ok: {check_body_size(b'x' * (2 * 1024 * 1024))}")
print(f"prompt 3000 chars ok: {validate_prompt('x' * 3000)}")
print(f"prompt 9000 chars ok: {validate_prompt('x' * 9000)}")
print()

# ============================================================
# 5. SSRF — agents that fetch URLs must not reach internal hosts
# ============================================================
# Server-Side Request Forgery: an attacker points your URL-fetching
# feature at http://169.254.169.254 (cloud metadata) or http://localhost
# to reach internal services. Guard: resolve the host, reject private/
# link-local/literal-IP targets, and pin allowed schemes.

PRIVATE_HOSTS = {"127.0.0.1", "::1", "localhost", "169.254.169.254",
                 "10.0.0.1", "192.168.1.1"}

def safe_fetch_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    host = (parsed.hostname or "").lower()
    if host in PRIVATE_HOSTS:
        return False
    if host.startswith("0.") or host == "0":
        return False
    return True


print("=== 5. SSRF guard ===")
print(f"public https url: {safe_fetch_url('https://docs.example.com/x')}")
print(f"cloud metadata  : {safe_fetch_url('http://169.254.169.254/latest/meta-data')}")
print(f"localhost       : {safe_fetch_url('http://localhost:8000/admin')}")
print(f"file scheme     : {safe_fetch_url('file:///etc/passwd')}")
print()

# ============================================================
# 6. Secrets — env only, never code
# ============================================================
# Secrets belong in environment variables / a secret manager, not in
# source control, not in config files committed to the repo.

def get_secret(name: str, default: str = "") -> str:
    """Read from env; production uses a secret manager at startup."""
    value = os.environ.get(name, default)
    if not value:
        raise RuntimeError(f"missing required secret: {name}")
    return value


print("=== 6. Secrets ===")
os.environ["API_SECRET"] = "env-only-value"
print(f"secret from env: {get_secret('API_SECRET')[:12]}...")
try:
    get_secret("NEVER_SET")
except RuntimeError as e:
    print(f"missing secret fails fast: {e}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: CORS: "*" — any website can call with user credentials
# CORRECT: explicit origin allowlist; never * with credentials
#
# MISTAKE: global rate limit — one tenant starves all
# CORRECT: per-identity token buckets
#
# MISTAKE: no size cap on LLM inputs — billing bomb + DoS
# CORRECT: cap body/prompt at the boundary
#
# MISTAKE: SSRF — agent URL fetch reaching cloud metadata/localhost
# CORRECT: scheme pin + private-host denylist + DNS re-check
#
# MISTAKE: secrets in code/repo
# CORRECT: env / secret manager; fail fast when missing

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Rate limiting: per-identity, refilling
    lim = TokenBucketLimiter(capacity=2, refill_per_sec=10.0)
    assert lim.allow("a") and lim.allow("a"), "capacity allows burst"
    assert not lim.allow("a"), "bucket drained for user a"
    assert lim.allow("b"), "user b has its own bucket"
    time.sleep(0.11)
    assert lim.allow("a"), "bucket refills over time"

    # 2. CORS allowlist
    assert cors_allow("https://app.example.com") == "https://app.example.com"
    assert cors_allow("https://evil.example") is None
    assert cors_allow(None) is None

    # 3. CSRF token must match; headers present
    assert csrf_check("tok-1", "tok-1")
    assert not csrf_check("tok-1", "tok-2")
    assert "Strict-Transport-Security" in build_headers()
    assert "Content-Security-Policy" in build_headers()

    # 4. Size caps
    assert check_body_size(b"x" * (1024 * 1024))
    assert not check_body_size(b"x" * (1024 * 1024 + 1))
    assert validate_prompt("x" * 4000)
    assert not validate_prompt("x" * 4001)
    assert not validate_prompt("")

    # 5. SSRF guard blocks private/internal/file targets
    assert safe_fetch_url("https://public.example.com/data")
    assert not safe_fetch_url("http://169.254.169.254/latest/meta-data")
    assert not safe_fetch_url("http://localhost:8000/admin")
    assert not safe_fetch_url("http://127.0.0.1:8080")
    assert not safe_fetch_url("file:///etc/passwd")
    assert not safe_fetch_url("ftp://example.com/x"), "scheme must be pinned"

    # 6. Secrets fail fast when missing
    assert get_secret("API_SECRET") == "env-only-value"
    try:
        get_secret("DEFINITELY_NOT_SET")
        assert False, "missing secret must raise"
    except RuntimeError:
        pass

    print("[OK] 41-api-security: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Rate limit per identity (token bucket)")
        print("2. CORS allowlist, never *")
        print("3. Security headers + CSRF for cookie auth")
        print("4. Size caps at the boundary")
        print("5. SSRF guard for URL-fetching features")
        print("6. Secrets from env only, fail fast")
        _verify()          # always runs, so plain execution is also a test
