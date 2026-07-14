# Lecture 06: Authentication & Authorization

## Topic Overview

Authentication verifies who users are, while authorization determines what they can do. This lecture covers API key management, OAuth 2.0, JWT tokens, role-based access control (RBAC), attribute-based access control (ABAC), and building secure identity systems for AI applications. Proper auth is essential for protecting AI services from unauthorized access and abuse.

---

## Learning Objectives

By the end of this lecture, you will be able:

1. **Implement** secure API key generation and management
2. **Design** OAuth 2.0 flows for AI applications
3. **Create** and validate JWT tokens
4. **Build** RBAC and ABAC authorization systems
5. **Implement** multi-factor authentication
6. **Handle** session management securely
7. **Apply** least privilege principles to AI systems

---

## Key Concepts

### 1. Authentication Methods

```python
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Optional, Dict
from dataclasses import dataclass

class AuthenticationMethod:
    """Base class for authentication methods."""

    def authenticate(self, credentials: Dict) -> Dict:
        """Authenticate user with credentials."""
        raise NotImplementedError

class APIKeyAuth(AuthenticationMethod):
    """API Key based authentication."""

    def __init__(self):
        self.api_keys = {}

    def generate_api_key(self, user_id: str, permissions: list) -> str:
        """Generate a new API key."""
        key = f"sk-{secrets.token_hex(32)}"
        self.api_keys[key] = {
            "user_id": user_id,
            "permissions": permissions,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=90),
            "last_used": None,
        }
        return key

    def authenticate(self, api_key: str) -> Dict:
        """Authenticate using API key."""
        if api_key not in self.api_keys:
            return {"authenticated": False, "error": "Invalid API key"}

        key_info = self.api_keys[api_key]

        # Check expiration
        if datetime.utcnow() > key_info["expires_at"]:
            return {"authenticated": False, "error": "API key expired"}

        # Update last used
        key_info["last_used"] = datetime.utcnow()

        return {
            "authenticated": True,
            "user_id": key_info["user_id"],
            "permissions": key_info["permissions"],
        }

    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key."""
        if api_key in self.api_keys:
            del self.api_keys[api_key]
            return True
        return False

class PasswordAuth(AuthenticationMethod):
    """Password-based authentication with secure hashing."""

    def __init__(self):
        self.users = {}

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with hashed password."""
        if username in self.users:
            return False

        # Hash password with salt
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000  # Iterations
        )

        self.users[username] = {
            "password_hash": password_hash.hex(),
            "salt": salt,
            "created_at": datetime.utcnow(),
            "failed_attempts": 0,
            "locked_until": None,
        }
        return True

    def authenticate(self, username: str, password: str) -> Dict:
        """Authenticate with username and password."""
        if username not in self.users:
            # Don't reveal if username exists
            return {"authenticated": False, "error": "Invalid credentials"}

        user = self.users[username]

        # Check if account is locked
        if user["locked_until"] and datetime.utcnow() < user["locked_until"]:
            return {"authenticated": False, "error": "Account locked"}

        # Verify password
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            user["salt"].encode(),
            100000
        )

        if password_hash.hex() != user["password_hash"]:
            user["failed_attempts"] += 1
            if user["failed_attempts"] >= 5:
                user["locked_until"] = datetime.utcnow() + timedelta(minutes=15)
            return {"authenticated": False, "error": "Invalid credentials"}

        # Reset failed attempts on success
        user["failed_attempts"] = 0
        user["locked_until"] = None

        return {"authenticated": True, "user_id": username}
```

### 2. JWT Token Management

```python
import json
import base64
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, Optional

class JWTManager:
    """JSON Web Token management."""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def create_token(self, payload: Dict, expires_in: int = 3600) -> str:
        """Create a JWT token."""
        # Header
        header = {"alg": "HS256", "typ": "JWT"}

        # Add standard claims
        now = datetime.utcnow()
        payload.update({
            "iat": int(now.timestamp()),           # Issued at
            "exp": int((now + timedelta(seconds=expires_in)).timestamp()),  # Expiration
            "jti": secrets.token_hex(16),          # JWT ID
        })

        # Encode header and payload
        header_encoded = self._base64url_encode(json.dumps(header))
        payload_encoded = self._base64url_encode(json.dumps(payload))

        # Create signature
        message = f"{header_encoded}.{payload_encoded}"
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        return f"{header_encoded}.{payload_encoded}.{signature}"

    def validate_token(self, token: str) -> Dict:
        """Validate and decode a JWT token."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return {"valid": False, "error": "Invalid token format"}

            header_encoded, payload_encoded, signature = parts

            # Verify signature
            message = f"{header_encoded}.{payload_encoded}"
            expected_signature = hmac.new(
                self.secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()

            if signature != expected_signature:
                return {"valid": False, "error": "Invalid signature"}

            # Decode payload
            payload = json.loads(self._base64url_decode(payload_encoded))

            # Check expiration
            if "exp" in payload:
                if datetime.utcnow().timestamp() > payload["exp"]:
                    return {"valid": False, "error": "Token expired"}

            return {"valid": True, "payload": payload}

        except Exception as e:
            return {"valid": False, "error": str(e)}

    def refresh_token(self, token: str, expires_in: int = 3600) -> Optional[str]:
        """Refresh an existing token."""
        validation = self.validate_token(token)
        if not validation["valid"]:
            return None

        payload = validation["payload"]
        # Remove old timestamps
        payload.pop("iat", None)
        payload.pop("exp", None)
        payload.pop("jti", None)

        return self.create_token(payload, expires_in)

    def _base64url_encode(self, data: str) -> str:
        """Base64url encode a string."""
        encoded = base64.urlsafe_b64encode(data.encode()).decode()
        return encoded.rstrip("=")

    def _base64url_decode(self, data: str) -> str:
        """Base64url decode a string."""
        # Add padding
        padding = 4 - len(data) % 4
        if padding != 4:
            data += "=" * padding
        return base64.urlsafe_b64decode(data).decode()

# Usage
jwt_manager = JWTManager("your-secret-key-here")

# Create token
token = jwt_manager.create_token({
    "sub": "user123",
    "role": "admin",
    "permissions": ["read", "write"]
})
print(f"Token: {token[:50]}...")

# Validate token
result = jwt_manager.validate_token(token)
print(f"Valid: {result['valid']}")
print(f"Payload: {result.get('payload')}")
```

### 3. Role-Based Access Control (RBAC)

```python
from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass
class Role:
    """User role definition."""
    name: str
    permissions: Set[str]
    description: str

@dataclass
class User:
    """User with roles."""
    user_id: str
    roles: Set[str]

class RBACSystem:
    """Role-Based Access Control system."""

    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.role_hierarchy: Dict[str, Set[str]] = {}

    def define_role(self, name: str, permissions: Set[str],
                    description: str = ""):
        """Define a new role."""
        self.roles[name] = Role(
            name=name,
            permissions=permissions,
            description=description,
        )

    def set_role_hierarchy(self, parent_role: str, child_roles: Set[str]):
        """Set role hierarchy (parent inherits child permissions)."""
        self.role_hierarchy[parent_role] = child_roles

    def assign_role(self, user_id: str, role_name: str):
        """Assign a role to a user."""
        if user_id not in self.users:
            self.users[user_id] = User(user_id=user_id, roles=set())
        self.users[user_id].roles.add(role_name)

    def remove_role(self, user_id: str, role_name: str):
        """Remove a role from a user."""
        if user_id in self.users:
            self.users[user_id].roles.discard(role_name)

    def get_user_permissions(self, user_id: str) -> Set[str]:
        """Get all permissions for a user (including inherited)."""
        if user_id not in self.users:
            return set()

        permissions = set()
        for role_name in self.users[user_id].roles:
            # Add direct permissions
            if role_name in self.roles:
                permissions.update(self.roles[role_name].permissions)

            # Add inherited permissions
            if role_name in self.role_hierarchy:
                for child_role in self.role_hierarchy[role_name]:
                    if child_role in self.roles:
                        permissions.update(self.roles[child_role].permissions)

        return permissions

    def check_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has a specific permission."""
        user_permissions = self.get_user_permissions(user_id)
        return permission in user_permissions

    def require_permission(self, user_id: str, permission: str) -> Dict:
        """Require a permission or return error."""
        if self.check_permission(user_id, permission):
            return {"allowed": True}
        return {
            "allowed": False,
            "error": f"Missing permission: {permission}",
        }

# Setup RBAC
rbac = RBACSystem()

# Define roles
rbac.define_role("viewer", {"read"}, "Can view content")
rbac.define_role("editor", {"read", "write"}, "Can edit content")
rbac.define_role("admin", {"read", "write", "delete", "manage_users"}, "Full access")

# Set hierarchy: admin inherits editor, editor inherits viewer
rbac.set_role_hierarchy("editor", {"viewer"})
rbac.set_role_hierarchy("admin", {"editor"})

# Assign roles
rbac.assign_role("user1", "viewer")
rbac.assign_role("user2", "editor")
rbac.assign_role("user3", "admin")

# Check permissions
print(f"user1 can read: {rbac.check_permission('user1', 'read')}")      # True
print(f"user1 can write: {rbac.check_permission('user1', 'write')}")    # False
print(f"user2 can write: {rbac.check_permission('user2', 'write')}")    # True
print(f"user3 can delete: {rbac.check_permission('user3', 'delete')}")  # True
```

### 4. Attribute-Based Access Control (ABAC)

```python
from typing import Dict, List, Callable
from dataclasses import dataclass
from enum import Enum

class PolicyEffect(Enum):
    ALLOW = "allow"
    DENY = "deny"

@dataclass
class Policy:
    """ABAC policy definition."""
    name: str
    effect: PolicyEffect
    conditions: Dict[str, Callable]
    description: str = ""

class ABACSystem:
    """Attribute-Based Access Control system."""

    def __init__(self):
        self.policies: List[Policy] = []

    def add_policy(self, policy: Policy):
        """Add a policy."""
        self.policies.append(policy)

    def evaluate(self, subject: Dict, resource: Dict,
                 action: str, context: Dict) -> Dict:
        """Evaluate access request against policies."""
        applicable_policies = []

        for policy in self.policies:
            if self._matches_policy(policy, subject, resource, action, context):
                applicable_policies.append(policy)

        # Evaluate policies (deny takes precedence)
        for policy in applicable_policies:
            if policy.effect == PolicyEffect.DENY:
                return {
                    "allowed": False,
                    "reason": f"Denied by policy: {policy.name}",
                }

        for policy in applicable_policies:
            if policy.effect == PolicyEffect.ALLOW:
                return {
                    "allowed": True,
                    "reason": f"Allowed by policy: {policy.name}",
                }

        # Default deny
        return {"allowed": False, "reason": "No matching policy"}

    def _matches_policy(self, policy: Policy, subject: Dict,
                        resource: Dict, action: str,
                        context: Dict) -> bool:
        """Check if a policy matches the request."""
        for condition_key, condition_func in policy.conditions.items():
            if condition_key == "subject":
                if not condition_func(subject):
                    return False
            elif condition_key == "resource":
                if not condition_func(resource):
                    return False
            elif condition_key == "action":
                if not condition_func(action):
                    return False
            elif condition_key == "context":
                if not condition_func(context):
                    return False
        return True

# Usage
abac = ABACSystem()

# Define policies
abac.add_policy(Policy(
    name="allow_admin_full_access",
    effect=PolicyEffect.ALLOW,
    conditions={
        "subject": lambda s: s.get("role") == "admin",
        "action": lambda a: True,  # Any action
    },
    description="Admins can do anything"
))

abac.add_policy(Policy(
    name="deny_external_write",
    effect=PolicyEffect.DENY,
    conditions={
        "subject": lambda s: s.get("department") != "engineering",
        "resource": lambda r: r.get("type") == "production_data",
        "action": lambda a: a in ["write", "delete"],
    },
    description="Non-engineers cannot write to production data"
))

abac.add_policy(Policy(
    name="allow_business_hours",
    effect=PolicyEffect.ALLOW,
    conditions={
        "context": lambda c: 9 <= c.get("hour", 0) <= 17,
        "subject": lambda s: s.get("department") == "engineering",
    },
    description="Engineers can access during business hours"
))

# Test access
result = abac.evaluate(
    subject={"role": "admin", "department": "engineering"},
    resource={"type": "production_data"},
    action="write",
    context={"hour": 14}
)
print(f"Admin access: {result}")  # {'allowed': True, ...}
```

### 5. OAuth 2.0 Flow

```python
from typing import Dict, Optional
import secrets
import hashlib

class OAuth2Server:
    """Simplified OAuth 2.0 server implementation."""

    def __init__(self):
        self.clients = {}
        self.authorization_codes = {}
        self.access_tokens = {}

    def register_client(self, client_id: str, redirect_uri: str,
                        client_secret: str):
        """Register an OAuth client."""
        self.clients[client_id] = {
            "redirect_uri": redirect_uri,
            "client_secret": client_secret,
            "created_at": datetime.utcnow(),
        }

    def generate_authorization_code(self, client_id: str,
                                     user_id: str,
                                     scope: str) -> str:
        """Generate authorization code."""
        code = secrets.token_urlsafe(32)
        self.authorization_codes[code] = {
            "client_id": client_id,
            "user_id": user_id,
            "scope": scope,
            "expires_at": datetime.utcnow() + timedelta(minutes=10),
            "used": False,
        }
        return code

    def exchange_code_for_token(self, code: str, client_id: str,
                                 client_secret: str) -> Dict:
        """Exchange authorization code for access token."""
        # Validate code
        if code not in self.authorization_codes:
            return {"error": "invalid_grant"}

        code_info = self.authorization_codes[code]

        # Check expiration
        if datetime.utcnow() > code_info["expires_at"]:
            return {"error": "invalid_grant"}

        # Check if already used
        if code_info["used"]:
            return {"error": "invalid_grant"}

        # Validate client
        if client_id != code_info["client_id"]:
            return {"error": "invalid_grant"}

        if client_id not in self.clients:
            return {"error": "invalid_client"}

        if self.clients[client_id]["client_secret"] != client_secret:
            return {"error": "invalid_client"}

        # Mark code as used
        code_info["used"] = True

        # Generate tokens
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)

        self.access_tokens[access_token] = {
            "user_id": code_info["user_id"],
            "scope": code_info["scope"],
            "expires_at": datetime.utcnow() + timedelta(hours=1),
        }

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": code_info["scope"],
        }

    def validate_access_token(self, token: str) -> Dict:
        """Validate an access token."""
        if token not in self.access_tokens:
            return {"valid": False, "error": "Invalid token"}

        token_info = self.access_tokens[token]

        if datetime.utcnow() > token_info["expires_at"]:
            return {"valid": False, "error": "Token expired"}

        return {
            "valid": True,
            "user_id": token_info["user_id"],
            "scope": token_info["scope"],
        }
```

---

## Common Mistakes to Avoid

1. **Hardcoding secrets** — Never hardcode API keys, passwords, or tokens
2. **Weak password hashing** — Use bcrypt, scrypt, or PBKDF2 with high iterations
3. **No token expiration** — Always set expiration times for tokens
4. **Over-privileged access** — Apply principle of least privilege
5. **Missing rate limiting** — Prevent brute force attacks
6. **Not validating tokens** — Always validate tokens on every request
7. **Storing secrets in code** — Use environment variables or secret managers
8. **No audit logging** — Log all authentication events

---

## Best Practices

1. **Use industry standards** — OAuth 2.0, OpenID Connect, JWT
2. **Implement MFA** — Add multi-factor authentication
3. **Apply least privilege** — Users get minimum necessary permissions
4. **Secure token storage** — Never store tokens in localStorage
5. **Rotate secrets** — Regularly rotate API keys and tokens
6. **Monitor auth events** — Log and alert on suspicious activity
7. **Handle failures gracefully** — Don't reveal whether username exists
8. **Implement account lockout** — After failed attempts

---

## Practice Exercises

### Exercise 1: API Key System (Easy)
Build an API key generation and validation system.

### Exercise 2: JWT Implementation (Medium)
Create a complete JWT authentication system.

### Exercise 3: RBAC System (Medium)
Implement a role-based access control system with inheritance.

### Exercise 4: OAuth 2.0 Flow (Hard)
Build a complete OAuth 2.0 authorization server.

---

## Summary

Authentication and authorization are foundational to AI security. Key takeaways:

- **Verify identity first** — Authentication must precede authorization
- **Use strong credentials** — API keys, JWT tokens, secure passwords
- **Apply least privilege** — Users get minimum necessary access
- **Implement RBAC or ABAC** — Structured authorization models
- **Secure token lifecycle** — Generate, validate, refresh, revoke properly
- **Monitor all auth events** — Detect and respond to suspicious activity

---

## References

- [OAuth 2.0 Specification](https://oauth.net/2/)
- [JWT RFC 7519](https://tools.ietf.org/html/rfc7519)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
