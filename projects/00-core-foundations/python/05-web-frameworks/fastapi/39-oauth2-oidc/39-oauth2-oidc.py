"""
FastAPI — 39: OAuth2 & OIDC
=============================
Topics: Authorization Code + PKCE; scopes vs claims; id_token vs access
        token; JWKS and key rotation; verifying provider tokens locally

Why this matters for AI/backend engineering:
    "Sign in with Google" and provider-hosted model APIs both run on
    OAuth2/OIDC. The security-sensitive details are the ones most
    tutorials skip: PKCE proves the app that started the flow is the
    one finishing it (a stolen code is useless without the verifier);
    scopes limit what the app may do; and JWKS is how your service
    verifies tokens it never signed — using the provider's public
    keys, honoring the kid, and surviving key rotation.

Run:      python 39-oauth2-oidc.py
Verify:   python 39-oauth2-oidc.py --verify
Reference: https://openid.net/connect/
"""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
import sys
import time
from typing import Optional

# ============================================================
# 1. PKCE — proving the app that finishes the flow started it
# ============================================================
# The app generates a random code_verifier, sends an S256 digest of it
# (code_challenge) with the authorize request, and presents the plain
# verifier at the token exchange. A hijacked authorization code is
# useless without the matching verifier.

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def generate_pkce_pair() -> tuple[str, str]:
    """Return (code_verifier, code_challenge). Verifier: 43-128 chars."""
    verifier = b64url(secrets.token_bytes(32))
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


def verify_pkce(verifier: str, challenge: str) -> bool:
    """Server-side: recompute S256 from the verifier and compare."""
    return secrets.compare_digest(
        b64url(hashlib.sha256(verifier.encode()).digest()), challenge
    )


print("=== 1. PKCE ===")
verifier, challenge = generate_pkce_pair()
print(f"verifier : {verifier[:20]}...")
print(f"challenge: {challenge[:20]}...")
print(f"verify with correct verifier : {verify_pkce(verifier, challenge)}")
print(f"verify with wrong verifier   : {verify_pkce(verifier + 'x', challenge)}")
print()

# ============================================================
# 2. Simulated Authorization Code + PKCE flow
# ============================================================
# authorize -> 302 with ?code= -> token exchange with code+verifier.
# The token endpoint must reject a code without the right verifier.

class Provider:
    """Tiny stand-in for an OAuth provider (in-memory)."""

    def __init__(self) -> None:
        self._codes: dict[str, dict] = {}   # code -> {challenge, client_id}

    def authorize(self, client_id: str, code_challenge: str, scope: str) -> str:
        code = b64url(secrets.token_bytes(16))
        self._codes[code] = {"challenge": code_challenge, "scope": scope}
        return code

    def exchange(self, code: str, verifier: str) -> dict:
        entry = self._codes.pop(code, None)
        if entry is None:
            raise ValueError("unknown or used code")
        if not verify_pkce(verifier, entry["challenge"]):
            raise ValueError("PKCE verification failed: code stolen or verifier wrong")
        return {"access_token": f"at-{code}", "scope": entry["scope"], "token_type": "Bearer"}


prov = Provider()
print("=== 2. Authorization Code + PKCE flow ===")
code = prov.authorize("my-app", challenge, "read:models")
print(f"redirect to app with code={code[:12]}...")
tok = prov.exchange(code, verifier)
print(f"token exchange OK: scope={tok['scope']}")
code2 = prov.authorize("my-app", challenge, "read:models")
try:
    prov.exchange(code2, verifier + "tampered")
except ValueError as e:
    print(f"stolen-code-without-verifier rejected: {e}")
print()

# ============================================================
# 3. Scopes vs claims, and id_token vs access_token
# ============================================================
# Scopes are AUTHORIZATION (what the app may do, coarse, provider-
# decided). Claims are IDENTITY (who the user is, in the id_token).
# The id_token proves authentication to the app; the access_token is
# the key to resource APIs. Never use the id_token as an API credential.

def id_token(sub: str, aud: str, email: str) -> dict:
    return {"iss": "https://provider.example", "sub": sub, "aud": aud,
            "email": email, "email_verified": True, "exp": int(time.time()) + 300}


def access_token(sub: str, scope: str) -> dict:
    return {"iss": "https://provider.example", "sub": sub,
            "scope": scope, "exp": int(time.time()) + 600}


print("=== 3. Scopes vs claims; id vs access token ===")
idt = id_token("user-1", "my-app", "ada@example.com")
acc = access_token("user-1", "read:models write:runs")
print(f"id_token claims  : aud={idt['aud']} sub={idt['sub']} email={idt['email']}")
print(f"access token scope: {acc['scope']}")
print()

# ============================================================
# 4. JWKS — verify tokens the provider signed, survive rotation
# ============================================================
# The provider publishes public keys at /.well-known/jwks.json. Your
# service reads the token's kid header, picks that key, and verifies.
# Keys rotate, so fetch JWKS (cache briefly), never hardcode.

def jwk_from_pem_placeholder(kid: str) -> dict:
    """Stand-in for a real RSA JWK. Real providers emit n/e for RSA keys."""
    return {"kty": "RSA", "kid": kid, "use": "sig",
            "n": "fake-n", "e": "AQAB"}


class JwksEndpoint:
    """Simulates the provider's published keyset with rotation."""

    def __init__(self) -> None:
        self._keys: dict[str, dict] = {}

    def add_key(self, kid: str, jwk: dict) -> None:
        self._keys[kid] = jwk

    def fetch(self) -> list[dict]:
        return list(self._keys.values())

    def rotate(self, old_kid: str, new_kid: str) -> None:
        del self._keys[old_kid]
        self._keys[new_kid] = {"kty": "RSA", "kid": new_kid, "use": "sig"}


jwks = JwksEndpoint()
jwks.add_key("key-1", jwk_from_pem_placeholder("key-1"))

def pick_key(keys: list[dict], kid: str) -> dict | None:
    return next((k for k in keys if k["kid"] == kid), None)


print("=== 4. JWKS and rotation ===")
token_kid = "key-1"
key = pick_key(jwks.fetch(), token_kid)
print(f"token kid={token_kid} -> JWKS key found: {key is not None}")
jwks.rotate("key-1", "key-2")
print(f"after rotation, old kid {token_kid} -> key found: "
      f"{pick_key(jwks.fetch(), token_kid) is not None}")
print("=> a cached stale key would fail verification after rotation; "
      "refresh JWKS on failure")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: implicit flow / tokens in URL fragments — history leaks
# CORRECT: Authorization Code + PKCE; tokens only in the token response
#
# MISTAKE: treating a valid signature as permission to do everything
# CORRECT: verify signature AND check the scope claim per route
#
# MISTAKE: sending the id_token as an API credential
# CORRECT: id_token -> app identity; access_token -> resource APIs
#
# MISTAKE: hardcoding the provider's public key
# CORRECT: fetch JWKS, honor kid, cache briefly, refresh on rotation failure

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. PKCE: challenge deterministic per verifier; wrong verifier fails
    v1, c1 = generate_pkce_pair()
    v2, c2 = generate_pkce_pair()
    assert verify_pkce(v1, c1), "correct verifier must pass"
    assert not verify_pkce(v1 + "x", c1), "tampered verifier must fail"
    assert not verify_pkce(v2, c1), "wrong verifier must fail"
    assert 43 <= len(v1) <= 128, "verifier must be 43-128 chars (RFC 7636)"

    # 2. Code exchange requires the correct verifier
    p = Provider()
    code = p.authorize("app", c1, "read")
    assert p.exchange(code, v1)["scope"] == "read", "happy path must work"
    code = p.authorize("app", c1, "read")
    try:
        p.exchange(code, "wrong-verifier")
        assert False, "exchange without verifier must fail"
    except ValueError:
        pass
    # Codes are single-use
    try:
        p.exchange(code, v1)
        assert False, "reuse of an exchanged code must fail"
    except ValueError:
        pass

    # 3. Scope is coarse authorization; claims are identity
    assert acc["scope"] == "read:models write:runs", "scope carries capabilities"
    assert idt["aud"] == "my-app", "id_token audience is the app"
    assert idt["email_verified"] is True, "OIDC claims include verification"

    # 4. JWKS lookup honors kid; rotation makes the old kid vanish
    j = JwksEndpoint()
    j.add_key("k1", jwk_from_pem_placeholder("k1"))
    assert pick_key(j.fetch(), "k1") is not None
    assert pick_key(j.fetch(), "ghost") is None, "unknown kid must not match"
    j.rotate("k1", "k2")
    assert pick_key(j.fetch(), "k1") is None, "rotated-away kid must be gone"
    assert pick_key(j.fetch(), "k2") is not None, "new kid must be present"

    print("[OK] 39-oauth2-oidc: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. PKCE: the verifier proves the app that finishes the flow")
        print("2. Scopes = authorization; claims = identity")
        print("3. JWKS + kid = verify provider tokens, survive rotation")
        _verify()          # always runs, so plain execution is also a test
