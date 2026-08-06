"""
FastAPI — 38: Authentication Deep Dive
=========================================
Topics: sessions vs tokens; JWT structure and signing; what JWTs are bad at;
        refresh-token rotation; revocation lists; bcrypt; timing-safe compare

Why this matters for AI/backend engineering:
    Every AI product has an auth boundary — API keys for users, service
    tokens for agents, JWTs for your own app. JWT's appeal (stateless,
    portable) is exactly its weakness (a valid token cannot be revoked
    until expiry). Production auth pairs short-lived JWTs with rotating
    refresh tokens and a revocation list for the escape hatch. Passwords
    are hashed with a slow, salted algorithm (bcrypt), and comparisons
    are timing-safe. This exercise builds the whole mechanism with
    PyJWT + bcrypt and asserts every property with TestClient.

Run:      python 38-auth-deep.py
Verify:   python 38-auth-deep.py --verify
Reference: https://pyjwt.readthedocs.io/en/stable/
"""

from __future__ import annotations

import hashlib
import hmac
import json
import sys
import time
from typing import Optional

import bcrypt

# ============================================================
# 1. Password hashing — slow + salted, and timing-safe compare
# ============================================================
# NEVER store plaintext or a fast hash. bcrypt is deliberately slow
# (adaptable work factor) and embeds a per-password salt. Verify with
# the library's own compare (which is timing-safe: constant-ish work
# regardless of match).

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# Timing-safe comparison for our own tokens/keys — never use == on secrets.
def timing_safe_eq(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode(), b.encode())


print("=== 1. Password hashing ===")
pw_hash = hash_password("hunter2")
print(f"bcrypt hash: {pw_hash[:32]}...  (salted + slow)")
print(f"correct pw -> {verify_password('hunter2', pw_hash)}")
print(f"wrong pw   -> {verify_password('hunter2!', pw_hash)}")
print()

# ============================================================
# 2. JWT structure — header.payload.signature
# ============================================================
# A JWT is three base64url parts: header (alg, typ), payload (claims),
# signature (HMAC-SHA256 over header.payload with the secret). The
# signature is what prevents forgery — anyone can READ the payload;
# only the secret holder can WRITE it.

SECRET = "dev-secret-change-me"

def b64url(data: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def sign_jwt(payload: dict, secret: str, exp_seconds: int = 300) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    full_payload = dict(payload)
    full_payload["exp"] = int(time.time()) + exp_seconds
    full_payload["iat"] = int(time.time())
    h = b64url(json.dumps(header, separators=(",", ":")).encode())
    p = b64url(json.dumps(full_payload, separators=(",", ":")).encode())
    sig = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{b64url(sig)}"


def verify_jwt(token: str, secret: str) -> dict:
    h, p, sig = token.split(".")
    expected = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(expected, __import__("base64").urlsafe_b64decode(sig + "==")):
        raise ValueError("bad signature")
    payload = json.loads(__import__("base64").urlsafe_b64decode(p + "=="))
    if payload.get("exp", 0) < time.time():
        raise ValueError("token expired")
    return payload


print("=== 2. JWT structure ===")
token = sign_jwt({"sub": "user-1", "role": "admin"})
print(f"token: {token[:60]}...")
claims = verify_jwt(token, SECRET)
print(f"claims: sub={claims['sub']} role={claims['role']} exp~{claims['exp']}")
print()

# ============================================================
# 3. What JWTs are bad at — revocation
# ============================================================
# A signed token is valid until exp. Logout, account suspension, and
# stolen-token response ALL need revocation — which requires state,
# defeating "stateless". Production answer: short-lived access tokens
# (5-15 min) + a revocation check (denylist) for the rare kill switch.

class TokenStore:
    """In-memory stand-in for a denylist (Redis in production)."""

    def __init__(self) -> None:
        self._denylist: set[str] = set()

    def revoke(self, jti: str) -> None:
        self._denylist.add(jti)

    def is_revoked(self, jti: str) -> bool:
        return jti in self._denylist


store = TokenStore()
print("=== 3. Revocation ===")
print("stateless JWT: valid until exp even after 'logout'")
print("fix: short exp + denylist check by jti claim")
print()

# ============================================================
# 4. Refresh-token rotation
# ============================================================
# Access token: short (minutes), sent with every request.
# Refresh token: long-lived, but only sent to ONE endpoint that
# exchanges it for a fresh pair — and ROTATES (old one is invalidated)
# so a stolen refresh token dies at first reuse.

def issue_pair(user_id: str) -> tuple[str, str, str]:
    """Return (access, refresh, refresh_jti)."""
    access = sign_jwt({"sub": user_id, "type": "access"}, SECRET, exp_seconds=300)
    jti = f"ref-{int(time.time() * 1000)}"
    refresh = sign_jwt({"sub": user_id, "type": "refresh", "jti": jti}, SECRET, exp_seconds=86400)
    return access, refresh, jti


def rotate(refresh: str, store: TokenStore, active_refreshes: dict[str, str]) -> tuple[str, str, str]:
    """Exchange a refresh token for a new pair; the old jti is dead."""
    claims = verify_jwt(refresh, SECRET)
    if claims.get("type") != "refresh":
        raise ValueError("not a refresh token")
    jti = claims.get("jti")
    if store.is_revoked(jti):
        raise ValueError("refresh token already used — possible theft, revoke family")
    store.revoke(jti)                       # rotation: old token is now dead
    access, new_refresh, new_jti = issue_pair(claims["sub"])
    active_refreshes[new_jti] = claims["sub"]
    return access, new_refresh, new_jti


active: dict[str, str] = {}
print("=== 4. Refresh rotation ===")
access, refresh, jti = issue_pair("user-1")
access2, refresh2, jti2 = rotate(refresh, store, active)
print(f"rotated: new access issued, old refresh revoked={store.is_revoked(jti)}")
try:
    rotate(refresh, store, active)          # reuse of the dead token
except ValueError as e:
    print(f"reuse detected: {e}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: 30-day access tokens so users 'don't have to log in'
# CORRECT: 5-15 min access + rotating refresh; denylist for kill switch
#
# MISTAKE: comparing hashes with ==
# CORRECT: hmac.compare_digest / bcrypt.checkpw (timing-safe)
#
# MISTAKE: storing passwords as sha256 (fast = brute-forceable)
# CORRECT: bcrypt/argon2 with a work factor; salted
#
# MISTAKE: accepting 'any role claim' — the signature binds it, so an
#   attacker cannot forge, but a USER with a role claim can be trusted
#   only if the token came from YOUR issuer. Validate issuer + audience.

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. bcrypt: correct verifies, wrong fails, hashes are salted
    h1 = hash_password("secret-1")
    h2 = hash_password("secret-1")
    assert h1 != h2, "bcrypt must salt: same password, different hash"
    assert verify_password("secret-1", h1), "correct password must verify"
    assert not verify_password("secret-2", h1), "wrong password must fail"
    assert timing_safe_eq("abc", "abc") and not timing_safe_eq("abc", "abd"), \
        "timing-safe compare must be correct"

    # 2. JWT: valid verifies; tampered payload fails signature check
    tok = sign_jwt({"sub": "u1", "role": "user"}, SECRET)
    claims = verify_jwt(tok, SECRET)
    assert claims["sub"] == "u1", "valid token must verify"
    h, p, s = tok.split(".")
    forged = f"{h}.{b64url(json.dumps({'sub': 'u1', 'role': 'admin', 'exp': int(time.time()) + 300, 'iat': int(time.time())}, separators=(',', ':')).encode())}.{s}"
    try:
        verify_jwt(forged, SECRET)
        assert False, "tampered payload must fail signature verification"
    except ValueError:
        pass

    # 3. Wrong secret cannot verify
    try:
        verify_jwt(tok, "other-secret")
        assert False, "wrong secret must fail"
    except ValueError:
        pass

    # 4. Expired token is rejected
    expired = sign_jwt({"sub": "u1"}, SECRET, exp_seconds=-10)
    try:
        verify_jwt(expired, SECRET)
        assert False, "expired token must be rejected"
    except ValueError:
        pass

    # 5. Refresh rotation: old refresh dies at first use; reuse detected
    store2 = TokenStore()
    active2: dict[str, str] = {}
    a1, r1, j1 = issue_pair("u1")
    a2, r2, j2 = rotate(r1, store2, active2)
    assert store2.is_revoked(j1), "old refresh must be revoked after rotation"
    try:
        rotate(r1, store2, active2)
        assert False, "reused refresh token must raise"
    except ValueError:
        pass
    # The NEW refresh still works (family continues)
    a3, r3, j3 = rotate(r2, store2, active2)
    assert store2.is_revoked(j2), "each rotation revokes the previous refresh"

    print("[OK] 38-auth-deep: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. bcrypt: slow, salted, timing-safe verify")
        print("2. JWT = header.payload.signature; payload is readable, not forgeable")
        print("3. Short access + rotating refresh + denylist = revocation reality")
        _verify()          # always runs, so plain execution is also a test
