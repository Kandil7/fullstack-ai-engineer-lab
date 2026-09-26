"""
=============================================================
Topic 06: Authentication & Authorization for AI Systems
=============================================================

Security Level: ########-- High

Master the authentication and authorization mechanisms that protect
AI systems from unauthorized access and misuse. This exercise covers
JWT security, OAuth2 flows, API key management, RBAC, session handling,
and token rotation strategies.

Learning Objectives:
- Implement secure JWT creation and validation
- Set up OAuth2 flows for AI service access
- Design API key management systems
- Build role-based access control for AI resources
- Implement secure session management
- Create token rotation and revocation mechanisms

Prerequisites:
- Understanding of HTTP authentication headers
- Basic cryptography concepts (hashing, signing)
- Familiarity with REST API patterns
=============================================================
"""

import jwt
import hashlib
import secrets
import time
import json
import hmac
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Callable
from enum import Enum
from functools import wraps
import base64
import uuid
import re


class JWTConfig:
    """JWT configuration with security best practices."""

    def __init__(self):
        self.algorithm = "HS256"
        self.access_token_ttl = 15 * 60  # 15 minutes (short-lived)
        self.refresh_token_ttl = 7 * 24 * 3600  # 7 days
        self.issuer = "ai-platform"
        self.audience = "ai-api"
        self._revoked_tokens: Set[str] = set()
        self._key_rotation_keys: Dict[str, bytes] = {}

    def generate_key_pair(self, key_id: Optional[str] = None) -> tuple:
        """Generate a new signing key pair."""
        kid = key_id or str(uuid.uuid4())
        secret = secrets.token_bytes(64)
        self._key_rotation_keys[kid] = secret
        return kid, secret


class SecureJWTManager:
    """
    Production-grade JWT manager with security best practices.

    Features:
    - Short-lived access tokens
    - Refresh token rotation
    - Token revocation
    - Key rotation support
    - Claim validation
    """

    def __init__(self, config: JWTConfig):
        self.config = config
        self._token_blacklist: Set[str] = set()

    def create_access_token(
        self, user_id: str, roles: List[str], metadata: Optional[Dict] = None
    ) -> str:
        """Create a secure access token."""
        now = time.time()
        jti = str(uuid.uuid4())  # Unique token ID for revocation

        payload = {
            # Registered claims
            "sub": user_id,
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "exp": now + self.config.access_token_ttl,
            "nbf": now,
            "iat": now,
            "jti": jti,
            # Custom claims
            "roles": roles,
            "token_type": "access",
        }

        if metadata:
            payload["meta"] = metadata

        # Find current signing key
        kid = list(self.config._key_rotation_keys.keys())[-1]
        secret = self.config._key_rotation_keys[kid]

        headers = {"kid": kid, "alg": self.config.algorithm}
        return jwt.encode(
            payload, secret, algorithm=self.config.algorithm, headers=headers
        )

    def create_refresh_token(self, user_id: str) -> str:
        """Create a secure refresh token with rotation support."""
        now = time.time()

        payload = {
            "sub": user_id,
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "exp": now + self.config.refresh_token_ttl,
            "iat": now,
            "jti": str(uuid.uuid4()),
            "token_type": "refresh",
            "rotated": False,
        }

        kid = list(self.config._key_rotation_keys.keys())[-1]
        secret = self.config._key_rotation_keys[kid]
        headers = {"kid": kid, "alg": self.config.algorithm}
        return jwt.encode(
            payload, secret, algorithm=self.config.algorithm, headers=headers
        )

    def validate_token(self, token: str) -> Dict:
        """Validate and decode a JWT token with full security checks."""
        # Check blacklist first
        try:
            unverified = jwt.decode(token, options={"verify_signature": False})
            if unverified.get("jti") in self._token_blacklist:
                raise SecurityError("Token has been revoked")
        except jwt.InvalidTokenError:
            pass

        # Decode with full verification
        kid = jwt.get_unverified_header(token).get("kid")
        if not kid or kid not in self.config._key_rotation_keys:
            raise SecurityError("Unknown signing key")

        secret = self.config._key_rotation_keys[kid]
        try:
            payload = jwt.decode(
                token,
                secret,
                algorithms=[self.config.algorithm],
                issuer=self.config.issuer,
                audience=self.config.audience,
                options={
                    "require": ["exp", "iss", "sub", "jti"],
                    "verify_exp": True,
                    "verify_iss": True,
                    "verify_aud": True,
                },
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise SecurityError("Token has expired")
        except jwt.InvalidAudienceError:
            raise SecurityError("Invalid audience")
        except jwt.InvalidIssuerError:
            raise SecurityError("Invalid issuer")
        except jwt.InvalidTokenError as e:
            raise SecurityError(f"Invalid token: {e}")

    def revoke_token(self, token: str):
        """Revoke a token by adding its JTI to the blacklist."""
        try:
            payload = jwt.decode(
                token,
                options={"verify_signature": False},
                algorithms=[self.config.algorithm],
            )
            self._token_blacklist.add(payload.get("jti", ""))
        except jwt.InvalidTokenError:
            pass

    def rotate_refresh_token(
        self, old_refresh_token: str, user_id: str, roles: List[str]
    ) -> Dict:
        """
        Rotate refresh token and issue new access token.
        Security: Old refresh token is invalidated.
        """
        payload = self.validate_token(old_refresh_token)

        if payload.get("token_type") != "refresh":
            raise SecurityError("Not a refresh token")

        # Revoke old refresh token
        self.revoke_token(old_refresh_token)

        # Issue new token pair
        new_access = self.create_access_token(user_id, roles)
        new_refresh = self.create_refresh_token(user_id)

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "token_type": "Bearer",
            "expires_in": self.config.access_token_ttl,
        }


class SecurityError(Exception):
    """Custom security error."""

    pass


# =============================================================
# SECTION 2: OAuth2 Implementation for AI Services
# =============================================================
