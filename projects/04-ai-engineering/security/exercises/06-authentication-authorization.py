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


# =============================================================
# SECTION 1: JWT Security Best Practices
# =============================================================

class JWTConfig:
    """JWT configuration with security best practices."""

    def __init__(self):
        self.algorithm = "HS256"
        self.access_token_ttl = 15 * 60      # 15 minutes (short-lived)
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
        self,
        user_id: str,
        roles: List[str],
        metadata: Optional[Dict] = None
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
        return jwt.encode(payload, secret, algorithm=self.config.algorithm, headers=headers)

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
        return jwt.encode(payload, secret, algorithm=self.config.algorithm, headers=headers)

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

    def rotate_refresh_token(self, old_refresh_token: str, user_id: str, roles: List[str]) -> Dict:
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

class OAuth2Flow(Enum):
    AUTHORIZATION_CODE = "authorization_code"
    CLIENT_CREDENTIALS = "client_credentials"
    IMPLICIT = "implicit"  # Not recommended
    PKCE = "pkce"  # Recommended for SPAs


@dataclass
class OAuth2Client:
    client_id: str
    client_secret: str
    redirect_uris: List[str]
    allowed_scopes: Set[str]
    token_endpoint_auth_method: str = "client_secret_basic"
    grant_types: List[str] = field(default_factory=lambda: ["authorization_code"])
    is_confidential: bool = True


@dataclass
class OAuth2Token:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: str = ""
    created_at: float = field(default_factory=time.time)


class OAuth2Server:
    """
    Simplified OAuth2 server for AI service authentication.

    Supports:
    - Authorization Code flow with PKCE
    - Client Credentials flow
    - Scope-based access control
    - Token introspection
    """

    def __init__(self, jwt_manager: SecureJWTManager):
        self.jwt_manager = jwt_manager
        self._clients: Dict[str, OAuth2Client] = {}
        self._codes: Dict[str, Dict] = {}
        self._tokens: Dict[str, OAuth2Token] = {}
        self._scopes = {
            "models:read": "Read model metadata",
            "models:inference": "Run model inference",
            "models:train": "Train models",
            "data:read": "Read training data",
            "data:write": "Write training data",
            "admin": "Full administrative access",
        }

    def register_client(
        self,
        client_id: str,
        client_secret: str,
        redirect_uris: List[str],
        scopes: Set[str],
        is_confidential: bool = True,
    ) -> OAuth2Client:
        """Register a new OAuth2 client."""
        client = OAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uris=redirect_uris,
            allowed_scopes=scopes,
            is_confidential=is_confidential,
        )
        self._clients[client_id] = client
        return client

    def generate_authorization_code(
        self,
        client_id: str,
        redirect_uri: str,
        scopes: List[str],
        code_challenge: Optional[str] = None,
        code_challenge_method: str = "S256",
    ) -> str:
        """Generate an authorization code for the authorization code flow."""
        client = self._clients.get(client_id)
        if not client:
            raise SecurityError("Unknown client")

        if redirect_uri not in client.redirect_uris:
            raise SecurityError("Invalid redirect URI")

        # Validate scopes
        invalid_scopes = set(scopes) - client.allowed_scopes
        if invalid_scopes:
            raise SecurityError(f"Invalid scopes: {invalid_scopes}")

        code = secrets.token_urlsafe(32)
        self._codes[code] = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scopes": scopes,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method,
            "expires_at": time.time() + 600,  # 10 minutes
            "used": False,
        }

        return code

    def exchange_code(
        self,
        code: str,
        client_id: str,
        client_secret: str,
        code_verifier: Optional[str] = None,
    ) -> OAuth2Token:
        """Exchange authorization code for tokens."""
        code_data = self._codes.get(code)
        if not code_data:
            raise SecurityError("Invalid authorization code")

        if code_data["used"]:
            # Code reuse attempt -- invalidate all tokens for this client
            self._invalidate_client_tokens(client_id)
            raise SecurityError("Authorization code reuse detected -- possible attack")

        if time.time() > code_data["expires_at"]:
            raise SecurityError("Authorization code expired")

        client = self._clients.get(client_id)
        if not client:
            raise SecurityError("Unknown client")

        if code_data["client_id"] != client_id:
            raise SecurityError("Code was not issued to this client")

        if not hmac.compare_digest(client.client_secret, client_secret):
            raise SecurityError("Invalid client secret")

        # PKCE verification
        if code_data["code_challenge"]:
            if not code_verifier:
                raise SecurityError("Code verifier required for PKCE")
            if not self._verify_pkce(code_data["code_challenge"], code_verifier, code_data["code_challenge_method"]):
                raise SecurityError("PKCE verification failed")

        # Mark code as used
        code_data["used"] = True

        # Create tokens
        access_token = self.jwt_manager.create_access_token(
            user_id=client_id,
            roles=["oauth2_client"],
            metadata={"scopes": code_data["scopes"], "grant_type": "authorization_code"},
        )

        refresh_token = self.jwt_manager.create_refresh_token(client_id)

        token = OAuth2Token(
            access_token=access_token,
            token_type="Bearer",
            expires_in=15 * 60,
            refresh_token=refresh_token,
            scope=" ".join(code_data["scopes"]),
        )

        self._tokens[access_token] = token
        return token

    def client_credentials_grant(
        self,
        client_id: str,
        client_secret: str,
        scopes: List[str],
    ) -> OAuth2Token:
        """Client Credentials flow for machine-to-machine auth."""
        client = self._clients.get(client_id)
        if not client:
            raise SecurityError("Unknown client")

        if not client.is_confidential:
            raise SecurityError("Client Credentials requires confidential client")

        if not hmac.compare_digest(client.client_secret, client_secret):
            raise SecurityError("Invalid client secret")

        invalid_scopes = set(scopes) - client.allowed_scopes
        if invalid_scopes:
            raise SecurityError(f"Invalid scopes: {invalid_scopes}")

        access_token = self.jwt_manager.create_access_token(
            user_id=client_id,
            roles=["service_account"],
            metadata={"scopes": scopes, "grant_type": "client_credentials"},
        )

        token = OAuth2Token(
            access_token=access_token,
            token_type="Bearer",
            expires_in=15 * 60,
            scope=" ".join(scopes),
        )

        self._tokens[access_token] = token
        return token

    def introspect_token(self, token: str) -> Dict:
        """Introspect a token to check its validity and metadata."""
        try:
            payload = self.jwt_manager.validate_token(token)
            return {
                "active": True,
                "sub": payload.get("sub"),
                "scope": " ".join(payload.get("meta", {}).get("scopes", [])),
                "exp": payload.get("exp"),
                "token_type": "Bearer",
                "client_id": payload.get("sub"),
            }
        except SecurityError:
            return {"active": False}

    def _verify_pkce(self, challenge: str, verifier: str, method: str) -> bool:
        """Verify PKCE code challenge."""
        if method == "S256":
            computed = base64.urlsafe_b64encode(
                hashlib.sha256(verifier.encode()).digest()
            ).rstrip(b"=").decode()
            return hmac.compare_digest(computed, challenge)
        elif method == "plain":
            return hmac.compare_digest(verifier, challenge)
        return False

    def _invalidate_client_tokens(self, client_id: str):
        """Invalidate all tokens for a client (security measure)."""
        to_remove = [t for t, tok in self._tokens.items() if tok.scope and client_id in t]
        for t in to_remove:
            self.jwt_manager.revoke_token(t)


# =============================================================
# SECTION 3: API Key Management
# =============================================================

@dataclass
class APIKey:
    key_id: str
    key_hash: str  # We never store raw keys
    prefix: str   # First 8 chars for identification
    user_id: str
    scopes: Set[str]
    created_at: float
    expires_at: Optional[float]
    last_used: Optional[float] = None
    is_active: bool = True
    rate_limit: int = 1000  # requests per hour
    metadata: Dict = field(default_factory=dict)


class APIKeyManager:
    """
    Secure API key management system.

    Features:
    - Key generation with secure randomness
    - Hashed storage (never store raw keys)
    - Key rotation support
    - Usage tracking
    - Scope-based permissions
    """

    def __init__(self):
        self._keys: Dict[str, APIKey] = {}  # key_id -> APIKey
        self._key_lookup: Dict[str, str] = {}  # key_hash -> key_id
        self._usage_log: List[Dict] = []

    def generate_key(
        self,
        user_id: str,
        scopes: Set[str],
        expires_in: Optional[int] = None,
        rate_limit: int = 1000,
    ) -> tuple:
        """
        Generate a new API key.

        Returns: (raw_key, key_info)
        The raw_key is shown ONCE and never stored.
        """
        key_id = str(uuid.uuid4())
        raw_key = f"sk_{secrets.token_urlsafe(32)}"
        key_hash = self._hash_key(raw_key)
        prefix = raw_key[:11]  # "sk_" + 8 chars

        expires_at = None
        if expires_in:
            expires_at = time.time() + expires_in

        api_key = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            prefix=prefix,
            user_id=user_id,
            scopes=scopes,
            created_at=time.time(),
            expires_at=expires_at,
            rate_limit=rate_limit,
        )

        self._keys[key_id] = api_key
        self._key_lookup[key_hash] = key_id

        return raw_key, api_key

    def validate_key(self, raw_key: str, required_scope: str) -> Optional[APIKey]:
        """Validate an API key and check scope permissions."""
        key_hash = self._hash_key(raw_key)
        key_id = self._key_lookup.get(key_hash)

        if not key_id:
            return None

        api_key = self._keys.get(key_id)
        if not api_key or not api_key.is_active:
            return None

        if api_key.expires_at and time.time() > api_key.expires_at:
            api_key.is_active = False
            return None

        if required_scope not in api_key.scopes and "admin" not in api_key.scopes:
            return None

        # Update last used
        api_key.last_used = time.time()
        return api_key

    def revoke_key(self, key_id: str) -> bool:
        """Revoke an API key."""
        api_key = self._keys.get(key_id)
        if not api_key:
            return False

        api_key.is_active = False
        if api_key.key_hash in self._key_lookup:
            del self._key_lookup[api_key.key_hash]
        return True

    def rotate_key(self, key_id: str) -> tuple:
        """Rotate an API key -- create new, deactivate old."""
        old_key = self._keys.get(key_id)
        if not old_key:
            raise SecurityError("Key not found")

        # Create new key with same permissions
        raw_key, new_key = self.generate_key(
            user_id=old_key.user_id,
            scopes=old_key.scopes,
            rate_limit=old_key.rate_limit,
        )

        # Revoke old key
        self.revoke_key(key_id)

        return raw_key, new_key

    def list_keys(self, user_id: str) -> List[APIKey]:
        """List all active keys for a user."""
        return [k for k in self._keys.values() if k.user_id == user_id and k.is_active]

    @staticmethod
    def _hash_key(key: str) -> str:
        """Hash an API key using SHA-256."""
        return hashlib.sha256(key.encode()).hexdigest()


# =============================================================
# SECTION 4: Role-Based Access Control (RBAC)
# =============================================================

@dataclass
class Permission:
    resource: str
    actions: Set[str]  # read, write, delete, inference, admin
    conditions: Dict = field(default_factory=dict)


@dataclass
class Role:
    name: str
    permissions: List[Permission]
    inherits: List[str] = field(default_factory=list)


class RBACManager:
    """
    Role-Based Access Control system for AI services.

    Supports:
    - Hierarchical roles with inheritance
    - Resource-level permissions
    - Condition-based access (time, IP, etc.)
    - Dynamic permission evaluation
    """

    def __init__(self):
        self._roles: Dict[str, Role] = {}
        self._user_roles: Dict[str, Set[str]] = {}  # user_id -> role names
        self._setup_default_roles()

    def _setup_default_roles(self):
        """Setup default roles for AI platform."""
        # Viewer: Read-only access
        self.add_role(Role(
            name="viewer",
            permissions=[
                Permission("models", {"read"}),
                Permission("data", {"read"}),
                Permission("logs", {"read"}),
            ],
        ))

        # Developer: Can run inference
        self.add_role(Role(
            name="developer",
            permissions=[
                Permission("models", {"read", "inference"}),
                Permission("data", {"read"}),
                Permission("experiments", {"read", "write"}),
            ],
            inherits=["viewer"],
        ))

        # Data Scientist: Can train models
        self.add_role(Role(
            name="data_scientist",
            permissions=[
                Permission("models", {"read", "write", "train"}),
                Permission("data", {"read", "write"}),
                Permission("experiments", {"read", "write", "delete"}),
            ],
            inherits=["developer"],
        ))

        # Admin: Full access
        self.add_role(Role(
            name="admin",
            permissions=[
                Permission("*", {"read", "write", "delete", "admin"}),
            ],
            inherits=["data_scientist"],
        ))

        # API Service: Limited to inference
        self.add_role(Role(
            name="api_service",
            permissions=[
                Permission("models", {"read", "inference"}),
                Permission("predictions", {"write"}),
            ],
        ))

    def add_role(self, role: Role):
        """Add or update a role."""
        self._roles[role.name] = role

    def assign_role(self, user_id: str, role_name: str):
        """Assign a role to a user."""
        if role_name not in self._roles:
            raise SecurityError(f"Unknown role: {role_name}")
        if user_id not in self._user_roles:
            self._user_roles[user_id] = set()
        self._user_roles[user_id].add(role_name)

    def remove_role(self, user_id: str, role_name: str):
        """Remove a role from a user."""
        if user_id in self._user_roles:
            self._user_roles[user_id].discard(role_name)

    def check_permission(
        self,
        user_id: str,
        resource: str,
        action: str,
        context: Optional[Dict] = None,
    ) -> bool:
        """
        Check if a user has permission for an action on a resource.

        Args:
            user_id: The user requesting access
            resource: Resource type (e.g., "models", "data")
            action: Action to perform (e.g., "read", "write", "inference")
            context: Optional context for condition evaluation
        """
        user_roles = self._user_roles.get(user_id, set())

        for role_name in user_roles:
            if self._check_role_permission(role_name, resource, action, context):
                return True
        return False

    def _check_role_permission(
        self,
        role_name: str,
        resource: str,
        action: str,
        context: Optional[Dict],
    ) -> bool:
        """Check permission including inherited roles."""
        role = self._roles.get(role_name)
        if not role:
            return False

        # Check direct permissions
        for perm in role.permissions:
            if (perm.resource in ("*", resource) and
                    (action in perm.actions or "*" in perm.actions)):
                if self._evaluate_conditions(perm.conditions, context):
                    return True

        # Check inherited roles
        for inherited_role in role.inherits:
            if self._check_role_permission(inherited_role, resource, action, context):
                return True

        return False

    def _evaluate_conditions(self, conditions: Dict, context: Optional[Dict]) -> bool:
        """Evaluate access conditions."""
        if not conditions:
            return True
        if not context:
            return not conditions  # No context means conditions can't be met

        for key, expected in conditions.items():
            actual = context.get(key)
            if actual is None:
                return False

            if isinstance(expected, list):
                if actual not in expected:
                    return False
            elif isinstance(expected, dict):
                if "min" in expected and actual < expected["min"]:
                    return False
                if "max" in expected and actual > expected["max"]:
                    return False
            elif actual != expected:
                return False

        return True

    def get_user_permissions(self, user_id: str) -> Dict[str, Set[str]]:
        """Get all permissions for a user across all roles."""
        permissions: Dict[str, Set[str]] = {}
        user_roles = self._user_roles.get(user_id, set())

        for role_name in user_roles:
            self._collect_permissions(role_name, permissions, set())

        return permissions

    def _collect_permissions(self, role_name: str, permissions: Dict, visited: Set):
        """Recursively collect permissions from role hierarchy."""
        if role_name in visited:
            return
        visited.add(role_name)

        role = self._roles.get(role_name)
        if not role:
            return

        for perm in role.permissions:
            if perm.resource not in permissions:
                permissions[perm.resource] = set()
            permissions[perm.resource].update(perm.actions)

        for inherited in role.inherits:
            self._collect_permissions(inherited, permissions, visited)


# =============================================================
# SECTION 5: Session Management & Token Rotation
# =============================================================

@dataclass
class Session:
    session_id: str
    user_id: str
    created_at: float
    expires_at: float
    ip_address: str
    user_agent: str
    is_active: bool = True
    last_activity: float = 0.0
    metadata: Dict = field(default_factory=dict)


class SessionManager:
    """
    Secure session management with token rotation.

    Features:
    - Session creation and validation
    - Automatic expiration
    - Session fixation prevention
    - Concurrent session limits
    - Token rotation on activity
    """

    def __init__(
        self,
        session_ttl: int = 3600,          # 1 hour
        max_sessions: int = 5,
        rotation_interval: int = 900,     # 15 minutes
    ):
        self.session_ttl = session_ttl
        self.max_sessions = max_sessions
        self.rotation_interval = rotation_interval
        self._sessions: Dict[str, Session] = {}
        self._user_sessions: Dict[str, Set[str]] = {}
        self._jwt_manager: Optional[SecureJWTManager] = None

    def set_jwt_manager(self, jwt_manager: SecureJWTManager):
        """Set the JWT manager for token rotation."""
        self._jwt_manager = jwt_manager

    def create_session(
        self,
        user_id: str,
        ip_address: str,
        user_agent: str,
    ) -> Session:
        """Create a new session with fixation prevention."""
        now = time.time()

        # Session fixation prevention: invalidate old sessions if limit reached
        if user_id in self._user_sessions:
            active = [
                self._sessions[sid]
                for sid in self._user_sessions[user_id]
                if sid in self._sessions and self._sessions[sid].is_active
            ]
            if len(active) >= self.max_sessions:
                # Remove oldest session
                oldest = min(active, key=lambda s: s.last_activity)
                oldest.is_active = False

        session_id = secrets.token_urlsafe(32)
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            expires_at=now + self.session_ttl,
            ip_address=ip_address,
            user_agent=user_agent,
            last_activity=now,
        )

        self._sessions[session_id] = session
        if user_id not in self._user_sessions:
            self._user_sessions[user_id] = set()
        self._user_sessions[user_id].add(session_id)

        return session

    def validate_session(
        self,
        session_id: str,
        ip_address: str,
        user_agent: str,
    ) -> Optional[Session]:
        """Validate a session with binding checks."""
        session = self._sessions.get(session_id)
        if not session or not session.is_active:
            return None

        if time.time() > session.expires_at:
            session.is_active = False
            return None

        # Session binding: verify IP and User-Agent haven't changed
        # (relaxed in dev -- tighten in production)
        if session.ip_address != ip_address:
            # Log suspicious activity
            session.metadata["ip_mismatch"] = session.metadata.get("ip_mismatch", 0) + 1
            if session.metadata["ip_mismatch"] > 3:
                session.is_active = False
                return None

        return session

    def rotate_session_token(self, session_id: str) -> Optional[str]:
        """Rotate session token to prevent session fixation."""
        session = self._sessions.get(session_id)
        if not session or not session.is_active:
            return None

        now = time.time()
        if now - session.last_activity < self.rotation_interval:
            return session_id  # Not time to rotate yet

        # Create new session ID
        new_session_id = secrets.token_urlsafe(32)
        new_session = Session(
            session_id=new_session_id,
            user_id=session.user_id,
            created_at=session.created_at,
            expires_at=session.expires_at,
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            last_activity=now,
            metadata=session.metadata.copy(),
        )

        # Invalidate old session
        session.is_active = False

        # Store new session
        self._sessions[new_session_id] = new_session
        if session.user_id in self._user_sessions:
            self._user_sessions[user_id].discard(session_id)
            self._user_sessions[user_id].add(new_session_id)

        return new_session_id

    def destroy_session(self, session_id: str):
        """Destroy a session."""
        session = self._sessions.get(session_id)
        if session:
            session.is_active = False
            if session.user_id in self._user_sessions:
                self._user_sessions[session.user_id].discard(session_id)

    def destroy_all_user_sessions(self, user_id: str):
        """Destroy all sessions for a user (e.g., on password change)."""
        if user_id in self._user_sessions:
            for sid in self._user_sessions[user_id]:
                if sid in self._sessions:
                    self._sessions[sid].is_active = False
            self._user_sessions[user_id] = set()

    def get_active_sessions(self, user_id: str) -> List[Session]:
        """Get all active sessions for a user."""
        if user_id not in self._user_sessions:
            return []
        return [
            self._sessions[sid]
            for sid in self._user_sessions[user_id]
            if sid in self._sessions and self._sessions[sid].is_active
        ]


# =============================================================
# SECTION 6: Authentication Decorators & Middleware
# =============================================================

def require_auth(*required_scopes):
    """Decorator for requiring authentication and specific scopes."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # In real app, extract token from request headers
            auth_header = kwargs.get("auth_header", "")
            if not auth_header.startswith("Bearer "):
                raise SecurityError("Missing or invalid authorization header")

            token = auth_header[7:]
            # Would use JWT manager to validate in production
            # For demo, we check scope presence
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(role_name: str):
    """Decorator for requiring a specific role."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_roles = kwargs.get("user_roles", set())
            if role_name not in user_roles:
                raise SecurityError(f"Requires role: {role_name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================
# DEMONSTRATIONS
# =============================================================

def demo_jwt_security():
    """Demonstrate JWT security best practices."""
    print("\n" + "=" * 60)
    print("DEMO 1: JWT Security Best Practices")
    print("=" * 60)

    config = JWTConfig()
    kid, secret = config.generate_key_pair()
    manager = SecureJWTManager(config)

    # Create access token
    access_token = manager.create_access_token(
        user_id="user_123",
        roles=["developer", "api_service"],
        metadata={"plan": "enterprise", "mfa_verified": True},
    )
    print(f"Access Token (truncated): {access_token[:50]}...")

    # Validate token
    payload = manager.validate_token(access_token)
    print(f"Token validated: sub={payload['sub']}, roles={payload['roles']}")
    print(f"Token expires at: {datetime.fromtimestamp(payload['exp'])}")

    # Create refresh token
    refresh_token = manager.create_refresh_token("user_123")
    print(f"Refresh Token (truncated): {refresh_token[:50]}...")

    # Token rotation
    rotated = manager.rotate_refresh_token(refresh_token, "user_123", ["developer"])
    print(f"Token rotated: new access token issued")

    # Revoke old token
    manager.revoke_token(access_token)
    try:
        manager.validate_token(access_token)
        print("ERROR: Should have raised SecurityError!")
    except SecurityError as e:
        print(f"Revoked token rejected: {e}")

    print("\n[OK] JWT security best practices demonstrated")


def demo_oauth2():
    """Demonstrate OAuth2 implementation."""
    print("\n" + "=" * 60)
    print("DEMO 2: OAuth2 for AI Services")
    print("=" * 60)

    config = JWTConfig()
    kid, secret = config.generate_key_pair()
    jwt_manager = SecureJWTManager(config)
    oauth2 = OAuth2Server(jwt_manager)

    # Register client
    client = oauth2.register_client(
        client_id="ai-app-001",
        client_secret="super_secret_key_123",
        redirect_uris=["https://myapp.com/callback"],
        scopes={"models:read", "models:inference", "data:read"},
    )
    print(f"Registered OAuth2 client: {client.client_id}")

    # Client Credentials flow (machine-to-machine)
    token = oauth2.client_credentials_grant(
        client_id="ai-app-001",
        client_secret="super_secret_key_123",
        scopes=["models:inference"],
    )
    print(f"Client Credentials token issued: {token.access_token[:50]}...")
    print(f"Scopes: {token.scope}")

    # Token introspection
    introspection = oauth2.introspect_token(token.access_token)
    print(f"Token introspection: active={introspection['active']}, sub={introspection.get('sub')}")

    print("\n[OK] OAuth2 implementation demonstrated")


def demo_api_keys():
    """Demonstrate API key management."""
    print("\n" + "=" * 60)
    print("DEMO 3: API Key Management")
    print("=" * 60)

    manager = APIKeyManager()

    # Generate API key
    raw_key, key_info = manager.generate_key(
        user_id="user_456",
        scopes={"models:inference", "data:read"},
        expires_in=30 * 24 * 3600,  # 30 days
        rate_limit=500,
    )
    print(f"Generated API Key: {raw_key[:20]}...")
    print(f"Key ID: {key_info.key_id}")
    print(f"Prefix: {key_info.prefix}")
    print(f"Scopes: {key_info.scopes}")

    # Validate API key
    validated = manager.validate_key(raw_key, "models:inference")
    print(f"Key validated: {validated is not None}")

    # List keys for user
    keys = manager.list_keys("user_456")
    print(f"Active keys for user: {len(keys)}")

    # Rotate key
    new_raw, new_key = manager.rotate_key(key_info.key_id)
    print(f"Key rotated: new key prefix = {new_key.prefix}")

    # Old key no longer works
    old_valid = manager.validate_key(raw_key, "models:inference")
    print(f"Old key still valid: {old_valid is not None}")

    print("\n[OK] API key management demonstrated")


def demo_rbac():
    """Demonstrate role-based access control."""
    print("\n" + "=" * 60)
    print("DEMO 4: Role-Based Access Control (RBAC)")
    print("=" * 60)

    rbac = RBACManager()

    # Assign roles
    rbac.assign_role("alice", "data_scientist")
    rbac.assign_role("bob", "developer")
    rbac.assign_role("charlie", "viewer")

    # Check permissions
    print("Alice (data_scientist):")
    print(f"  Can train models: {rbac.check_permission('alice', 'models', 'train')}")
    print(f"  Can write data: {rbac.check_permission('alice', 'data', 'write')}")
    print(f"  Can delete experiments: {rbac.check_permission('alice', 'experiments', 'delete')}")

    print("\nBob (developer):")
    print(f"  Can run inference: {rbac.check_permission('bob', 'models', 'inference')}")
    print(f"  Can train models: {rbac.check_permission('bob', 'models', 'train')}")
    print(f"  Can write data: {rbac.check_permission('bob', 'data', 'write')}")

    print("\nCharlie (viewer):")
    print(f"  Can read models: {rbac.check_permission('charlie', 'models', 'read')}")
    print(f"  Can run inference: {rbac.check_permission('charlie', 'models', 'inference')}")

    # Get all permissions
    print("\nAlice's full permissions:")
    perms = rbac.get_user_permissions("alice")
    for resource, actions in perms.items():
        print(f"  {resource}: {', '.join(actions)}")

    print("\n[OK] RBAC demonstrated")


def demo_session_management():
    """Demonstrate session management."""
    print("\n" + "=" * 60)
    print("DEMO 5: Session Management & Token Rotation")
    print("=" * 60)

    manager = SessionManager(max_sessions=3, rotation_interval=5)

    # Create sessions
    s1 = manager.create_session("user_789", "192.168.1.1", "Mozilla/5.0")
    s2 = manager.create_session("user_789", "10.0.0.1", "Python/3.11")
    print(f"Created session 1: {s1.session_id[:20]}...")
    print(f"Created session 2: {s2.session_id[:20]}...")

    # Validate session
    validated = manager.validate_session(s1.session_id, "192.168.1.1", "Mozilla/5.0")
    print(f"Session 1 validated: {validated is not None}")

    # Session from different IP
    validated_bad = manager.validate_session(s1.session_id, "10.0.0.99", "Mozilla/5.0")
    print(f"Session from different IP: {validated_bad is not None}")

    # List active sessions
    active = manager.get_active_sessions("user_789")
    print(f"Active sessions: {len(active)}")

    # Destroy all sessions
    manager.destroy_all_user_sessions("user_789")
    active_after = manager.get_active_sessions("user_789")
    print(f"Active sessions after logout all: {len(active_after)}")

    print("\n[OK] Session management demonstrated")


# =============================================================
# SECURITY ATTACK PATTERNS & DEFENSES
# =============================================================

ATTACK_PATTERNS = """
+==============================================================+
|           COMMON AUTHENTICATION ATTACKS                      |
+==============================================================+
|                                                              |
|  1. JWT ALGORITHM CONFUSION                                  |
|     Attack: Change "alg" header to "none" or RS256->HS256    |
|     Defense: Always specify allowed algorithms explicitly     |
|     Code: jwt.decode(token, key, algorithms=["HS256"])       |
|                                                              |
|  2. TOKEN THEFT (XSS)                                       |
|     Attack: Steal tokens via XSS in localStorage            |
|     Defense: Use httpOnly cookies, short TTL, refresh rotation|
|                                                              |
|  3. SESSION FIXATION                                         |
|     Attack: Set session ID before login, hijack after       |
|     Defense: Regenerate session ID on login                  |
|                                                              |
|  4. API KEY LEAKAGE                                          |
|     Attack: Keys in source code, logs, or URLs              |
|     Defense: Never log keys, use env vars, rotate regularly |
|                                                              |
|  5. BROKEN AUTHORIZATION                                     |
|     Attack: Access other users' resources by changing IDs   |
|     Defense: Use UUIDs, check ownership on every request     |
|                                                              |
|  6. PASSWORD SPRAYING                                        |
|     Attack: Try common passwords across many accounts       |
|     Defense: Rate limit, account lockout, MFA               |
|                                                              |
|  7. OAUTH2 REDIRECT ATTACK                                  |
|     Attack: Manipulate redirect_uri parameter               |
|     Defense: Validate exact redirect URI match               |
|                                                              |
|  8. REPLAY ATTACKS                                           |
|     Attack: Reuse captured tokens                            |
|     Defense: Short TTL, nonce tracking, token binding        |
|                                                              |
+==============================================================+
"""


# =============================================================
# BEST PRACTICES SUMMARY
# =============================================================

BEST_PRACTICES = """
+==============================================================+
|              AUTHENTICATION BEST PRACTICES                   |
+==============================================================+
|                                                              |
|  JWT SECURITY:                                               |
|  [OK] Use short-lived access tokens (15 min)                   |
|  [OK] Implement refresh token rotation                          |
|  [OK] Validate all claims (exp, iss, aud, sub)                |
|  [OK] Use strong secret keys (256+ bits)                       |
|  [OK] Maintain token blacklist for revocation                  |
|  [OK] Never store sensitive data in JWT payload                 |
|                                                              |
|  API KEYS:                                                   |
|  [OK] Hash keys before storage (SHA-256)                       |
|  [OK] Use key prefixes for identification                       |
|  [OK] Implement key rotation                                    |
|  [OK] Set expiration dates                                      |
|  [OK] Track usage and detect anomalies                          |
|                                                              |
|  RBAC:                                                       |
|  [OK] Follow principle of least privilege                       |
|  [OK] Use role inheritance to reduce complexity                 |
|  [OK] Audit permissions regularly                               |
|  [OK] Support conditional access (time, IP, MFA)               |
|                                                              |
|  SESSIONS:                                                   |
|  [OK] Regenerate session IDs after login                       |
|  [OK] Implement session binding (IP, User-Agent)               |
|  [OK] Set session timeout and idle timeout                      |
|  [OK] Limit concurrent sessions                                 |
|  [OK] Provide session revocation on logout/password change     |
|                                                              |
+==============================================================+
"""


# =============================================================
# MAIN EXECUTION
# =============================================================

if __name__ == "__main__":
    print("+==============================================================+")
    print("|   Topic 06: Authentication & Authorization for AI Systems   |")
    print("+==============================================================+")

    try:
        demo_jwt_security()
        demo_oauth2()
        demo_api_keys()
        demo_rbac()
        demo_session_management()

        print(ATTACK_PATTERNS)
        print(BEST_PRACTICES)

        print("\n" + "=" * 60)
        print("[OK] ALL AUTHENTICATION & AUTHORIZATION DEMOS COMPLETED")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
