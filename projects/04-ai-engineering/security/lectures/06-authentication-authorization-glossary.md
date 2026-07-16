# Glossary 06: Authentication & Authorization Terms

## Quick Reference Table

| Term | Category | Importance | See Also |
|------|----------|------------|----------|
| Authentication | Process | Critical | Authorization, Identity |
| Authorization | Process | Critical | Access Control |
| API Key | Credential | High | Authentication |
| JWT (JSON Web Token) | Token | Critical | Access Token |
| OAuth 2.0 | Protocol | Critical | Authorization |
| RBAC | Model | Critical | Role-Based Access |
| ABAC | Model | High | Attribute-Based Access |
| Access Token | Token | Critical | JWT, Bearer Token |
| Refresh Token | Token | High | Token Rotation |
| Session Management | Process | High | Token Management |
| Multi-Factor Authentication | Technique | Critical | MFA, 2FA |
| Password Hashing | Technique | Critical | Bcrypt, PBKDF2 |
| Single Sign-On | Protocol | High | SSO, Federated Auth |
| Scope | Concept | High | Permissions |
| Principle of Least Privilege | Principle | Critical | Minimization |
| Token Expiration | Mechanism | High | Timeout, Refresh |

---

## Alphabetical Definitions

### Access Control

**Definition**: The process of granting or denying specific requests to use resources, including computing resources, physical resources, or information.

**Example**:
```python
class AccessControl:
    def __init__(self):
        self.policies = []

    def add_policy(self, policy: dict):
        self.policies.append(policy)

    def check_access(self, user: dict, resource: str, action: str) -> bool:
        """Check if user can perform action on resource."""
        for policy in self.policies:
            if (policy["user_role"] == user.get("role") and
                policy["resource"] == resource and
                policy["action"] == action):
                return policy.get("allowed", False)
        return False  # Default deny

# Usage
ac = AccessControl()
ac.add_policy({"user_role": "admin", "resource": "users", "action": "delete", "allowed": True})
print(ac.check_access({"role": "admin"}, "users", "delete"))  # True
```

**Related Terms**: Authorization, RBAC, ABAC

---

### Access Token

**Definition**: A credential issued to a client after successful authentication, used to access protected resources. Typically short-lived and scoped to specific permissions.

**Example**:
```python
class AccessToken:
    def __init__(self, token: str, expires_in: int, scope: list):
        self.token = token
        self.expires_in = expires_in
        self.scope = scope
        self.issued_at = time.time()

    def is_valid(self) -> bool:
        """Check if token is still valid."""
        elapsed = time.time() - self.issued_at
        return elapsed < self.expires_in

    def has_scope(self, required_scope: str) -> bool:
        """Check if token has required scope."""
        return required_scope in self.scope

# Usage
token = AccessToken("abc123", 3600, ["read", "write"])
print(f"Valid: {token.is_valid()}")
print(f"Has write: {token.has_scope('write')}")
```

**Related Terms**: JWT, Bearer Token, Token Expiration

---

### Attribute-Based Access Control (ABAC)

**Definition**: An authorization model that evaluates access decisions based on attributes of the subject, resource, action, and environment.

**Example**:
```python
class ABACPolicy:
    def __init__(self, name: str, conditions: dict):
        self.name = name
        self.conditions = conditions

    def evaluate(self, subject: dict, resource: dict,
                 action: str, environment: dict) -> bool:
        """Evaluate policy against request."""
        for key, condition in self.conditions.items():
            if key == "subject":
                if not condition(subject):
                    return False
            elif key == "resource":
                if not condition(resource):
                    return False
            elif key == "action":
                if not condition(action):
                    return False
            elif key == "environment":
                if not condition(environment):
                    return False
        return True

# Usage
policy = ABACPolicy(
    "engineer_access",
    {
        "subject": lambda s: s.get("department") == "engineering",
        "resource": lambda r: r.get("classification") != "top_secret",
        "action": lambda a: a in ["read", "write"],
    }
)

allowed = policy.evaluate(
    subject={"department": "engineering"},
    resource={"classification": "internal"},
    action="read",
    environment={}
)
print(f"Allowed: {allowed}")  # True
```

**Related Terms**: RBAC, Policy-Based Access Control

---

### API Key

**Definition**: A unique identifier used to authenticate a client making API requests. API keys are simpler than OAuth but less secure for user-facing applications.

**Example**:
```python
import secrets
import hashlib

class APIKeyManager:
    def __init__(self):
        self.keys = {}

    def generate_key(self, user_id: str, permissions: list) -> str:
        """Generate a new API key."""
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

        key_info = self.keys[key_hash]
        if datetime.utcnow() > key_info["expires_at"]:
            return {"valid": False, "error": "Key expired"}

        return {
            "valid": True,
            "user_id": key_info["user_id"],
            "permissions": key_info["permissions"],
        }

    def revoke_key(self, key: str) -> bool:
        """Revoke an API key."""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        if key_hash in self.keys:
            del self.keys[key_hash]
            return True
        return False
```

**Related Terms**: Authentication, Secret Key, Credential

---

### Attribute-Based Access Control (ABAC)

**Definition**: An authorization model that evaluates access decisions based on attributes of the subject, resource, action, and environment.

**Example**:
```python
class ABACSystem:
    def __init__(self):
        self.policies = []

    def add_policy(self, name: str, conditions: dict):
        self.policies.append({"name": name, "conditions": conditions})

    def evaluate(self, subject: dict, resource: dict,
                 action: str, context: dict) -> dict:
        """Evaluate access request."""
        for policy in self.policies:
            if self._matches(policy["conditions"], subject, resource, action, context):
                return {"allowed": True, "policy": policy["name"]}
        return {"allowed": False, "reason": "No matching policy"}

    def _matches(self, conditions, subject, resource, action, context):
        """Check if conditions match request."""
        for key, check in conditions.items():
            if key == "subject" and not check(subject):
                return False
            if key == "resource" and not check(resource):
                return False
            if key == "action" and not check(action):
                return False
            if key == "context" and not check(context):
                return False
        return True
```

**Related Terms**: RBAC, Policy Engine, Attribute Evaluation

---

### Bearer Token

**Definition**: A security token with the property that any party in possession of it can use it to access the associated resource, similar to carrying cash.

**Example**:
```python
# Bearer token in HTTP header
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIs..."
}

# Usage in requests
import requests

response = requests.get(
    "https://api.example.com/data",
    headers=headers
)
```

**Related Terms**: Access Token, JWT, Authorization Header

---

### Bcrypt

**Definition**: A password hashing function designed to be slow and computationally expensive, making it resistant to brute-force attacks.

**Example**:
```python
import bcrypt

class PasswordHasher:
    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode(), hashed.encode())

# Usage
hasher = PasswordHasher()
hashed = hasher.hash_password("secure_password_123")
print(f"Hash: {hashed}")
print(f"Valid: {hasher.verify_password('secure_password_123', hashed)}")
```

**Related Terms**: Password Hashing, Salt, PBKDF2

---

### Client ID

**Definition**: A public identifier for an application registered with an OAuth provider, used to identify the application making requests.

**Example**:
```python
# Client ID in OAuth flow
oauth_config = {
    "client_id": "abc123.apps.googleusercontent.com",
    "client_secret": "GOCSPX-xxxxx",  # Keep secret!
    "redirect_uri": "https://myapp.com/callback",
    "scope": "openid email profile",
}

# Authorization URL
auth_url = (
    f"https://accounts.google.com/o/oauth2/auth?"
    f"client_id={oauth_config['client_id']}"
    f"&redirect_uri={oauth_config['redirect_uri']}"
    f"&scope={oauth_config['scope']}"
    f"&response_type=code"
)
```

**Related Terms**: OAuth 2.0, Client Secret, Redirect URI

---

### Client Secret

**Definition**: A confidential value used to authenticate the client application to the OAuth provider. Must be kept secure and never exposed to users.

**Example**:
```python
# NEVER expose client secret in frontend code
# Store securely in environment variables or secret manager

import os

# Server-side only
client_secret = os.environ.get("OAUTH_CLIENT_SECRET")

# In token exchange
token_data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "client_id": client_id,
    "client_secret": client_secret,  # Sent to provider server-side only
}
```

**Related Terms**: OAuth 2.0, Client ID, Secret Management

---

### Multi-Factor Authentication (MFA)

**Definition**: A security mechanism that requires users to provide two or more verification factors to gain access to a resource.

**Example**:
```python
class MFAProvider:
    def __init__(self):
        self.totp_secrets = {}

    def generate_totp_secret(self, user_id: str) -> str:
        """Generate TOTP secret for user."""
        secret = pyotp.random_base32()
        self.totp_secrets[user_id] = secret
        return secret

    def verify_totp(self, user_id: str, code: str) -> bool:
        """Verify TOTP code."""
        if user_id not in self.totp_secrets:
            return False

        totp = pyotp.TOTP(self.totp_secrets[user_id])
        return totp.verify(code, valid_window=1)

    def get_mfa_factors(self, user_id: str) -> list:
        """Get available MFA factors for user."""
        factors = []
        if user_id in self.totp_secrets:
            factors.append("totp")
        factors.append("sms")  # Always available as fallback
        return factors
```

**Related Terms**: Two-Factor Authentication, TOTP, SMS Verification

---

### Principle of Least Privilege

**Definition**: The security concept that a user should have only the minimum levels of access—or permissions—needed to perform their job functions.

**Example**:
```python
# Role definitions with least privilege
roles = {
    "viewer": {
        "permissions": ["read"],
        "description": "Can only view data"
    },
    "editor": {
        "permissions": ["read", "write"],
        "description": "Can view and edit data"
    },
    "admin": {
        "permissions": ["read", "write", "delete", "manage_users"],
        "description": "Full system access"
    }
}

def assign_minimum_role(user_task: str) -> str:
    """Assign minimum role needed for task."""
    task_roles = {
        "view_reports": "viewer",
        "edit_content": "editor",
        "manage_system": "admin",
    }
    return task_roles.get(user_task, "viewer")  # Default to viewer
```

**Related Terms**: Access Control, RBAC, Security Principle

---

### Refresh Token

**Definition**: A long-lived token used to obtain new access tokens without requiring the user to re-authenticate. Should be stored securely.

**Example**:
```python
class TokenManager:
    def __init__(self):
        self.refresh_tokens = {}

    def create_refresh_token(self, user_id: str) -> str:
        """Create a refresh token."""
        token = secrets.token_urlsafe(64)
        self.refresh_tokens[token] = {
            "user_id": user_id,
            "expires_at": datetime.utcnow() + timedelta(days=30),
            "revoked": False,
        }
        return token

    def use_refresh_token(self, token: str) -> dict:
        """Use refresh token to get new access token."""
        if token not in self.refresh_tokens:
            return {"error": "Invalid refresh token"}

        token_info = self.refresh_tokens[token]

        if token_info["revoked"]:
            return {"error": "Refresh token revoked"}

        if datetime.utcnow() > token_info["expires_at"]:
            return {"error": "Refresh token expired"}

        # Generate new access token
        new_access_token = secrets.token_urlsafe(32)
        return {"access_token": new_access_token, "expires_in": 3600}

    def revoke_refresh_token(self, token: str):
        """Revoke a refresh token."""
        if token in self.refresh_tokens:
            self.refresh_tokens[token]["revoked"] = True
```

**Related Terms**: Access Token, Token Rotation, Session Management

---

### Role-Based Access Control (RBAC)

**Definition**: An authorization model where access is granted based on the roles assigned to users, rather than individual permissions.

**Example**:
```python
class RBACSystem:
    def __init__(self):
        self.roles = {}
        self.user_roles = {}

    def define_role(self, name: str, permissions: list):
        self.roles[name] = set(permissions)

    def assign_role(self, user_id: str, role: str):
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        self.user_roles[user_id].add(role)

    def check_permission(self, user_id: str, permission: str) -> bool:
        if user_id not in self.user_roles:
            return False

        for role in self.user_roles[user_id]:
            if role in self.roles and permission in self.roles[role]:
                return True
        return False

# Usage
rbac = RBACSystem()
rbac.define_role("viewer", ["read"])
rbac.define_role("editor", ["read", "write"])
rbac.define_role("admin", ["read", "write", "delete"])

rbac.assign_role("user1", "editor")
print(rbac.check_permission("user1", "write"))  # True
print(rbac.check_permission("user1", "delete"))  # False
```

**Related Terms**: ABAC, Role Hierarchy, Permission

---

### Scope

**Definition**: The specific permissions or access levels granted to a token, limiting what actions can be performed with that token.

**Example**:
```python
# OAuth scopes
available_scopes = {
    "read": "Read access to resources",
    "write": "Write access to resources",
    "delete": "Delete access to resources",
    "admin": "Full administrative access",
    "profile": "Access to user profile",
    "email": "Access to user email",
}

# Token with limited scope
token = {
    "access_token": "abc123",
    "scope": "read write",  # Can read and write, but not delete
    "expires_in": 3600,
}

# Scope validation
def has_scope(token_scopes: str, required_scope: str) -> bool:
    """Check if token has required scope."""
    return required_scope in token_scopes.split()

print(has_scope("read write", "read"))  # True
print(has_scope("read write", "delete"))  # False
```

**Related Terms**: Access Control, Permissions, OAuth

---

### Session Management

**Definition**: The process of securely creating, maintaining, and destroying user sessions after authentication.

**Example**:
```python
class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id: str) -> str:
        """Create a new session."""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=1),
            "ip_address": None,
            "user_agent": None,
        }
        return session_id

    def validate_session(self, session_id: str) -> dict:
        """Validate a session."""
        if session_id not in self.sessions:
            return {"valid": False, "error": "Session not found"}

        session = self.sessions[session_id]

        if datetime.utcnow() > session["expires_at"]:
            self.destroy_session(session_id)
            return {"valid": False, "error": "Session expired"}

        # Update last activity
        session["last_activity"] = datetime.utcnow()

        return {"valid": True, "user_id": session["user_id"]}

    def destroy_session(self, session_id: str):
        """Destroy a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_active_sessions(self, user_id: str) -> list:
        """Get all active sessions for a user."""
        active = []
        for session_id, session in self.sessions.items():
            if session["user_id"] == user_id:
                if datetime.utcnow() < session["expires_at"]:
                    active.append(session_id)
        return active
```

**Related Terms**: Token Management, Session Fixation, Session Hijacking

---

### Single Sign-On (SSO)

**Definition**: An authentication scheme that allows a user to log in with a single ID and password to access multiple independent systems.

**Example**:
```python
class SSOProvider:
    def __init__(self):
        self.service_providers = {}
        self.user_sessions = {}

    def register_service_provider(self, sp_id: str, metadata_url: str):
        """Register a service provider."""
        self.service_providers[sp_id] = {
            "metadata_url": metadata_url,
            "registered_at": datetime.utcnow(),
        }

    def initiate_sso(self, user_id: str, sp_id: str) -> str:
        """Initiate SSO login."""
        # Generate SAML assertion or OIDC token
        assertion = self._create_assertion(user_id, sp_id)

        # Create session
        session_token = secrets.token_urlsafe(32)
        self.user_sessions[session_token] = {
            "user_id": user_id,
            "sp_id": sp_id,
            "created_at": datetime.utcnow(),
        }

        return session_token

    def validate_sso_token(self, token: str, sp_id: str) -> dict:
        """Validate SSO token at service provider."""
        if token not in self.user_sessions:
            return {"valid": False}

        session = self.user_sessions[token]
        if session["sp_id"] != sp_id:
            return {"valid": False}

        return {"valid": True, "user_id": session["user_id"]}

    def _create_assertion(self, user_id: str, sp_id: str) -> str:
        """Create SAML assertion."""
        return f"saml_assertion_{user_id}_{sp_id}"
```

**Related Terms**: Federated Authentication, SAML, OIDC

---

### Token Expiration

**Definition**: The mechanism by which tokens become invalid after a specified time period, limiting the window of exposure if a token is compromised.

**Example**:
```python
class TokenWithExpiration:
    def __init__(self, token: str, expires_in_seconds: int):
        self.token = token
        self.issued_at = time.time()
        self.expires_at = self.issued_at + expires_in_seconds

    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    def time_until_expiry(self) -> int:
        """Seconds until token expires."""
        remaining = self.expires_at - time.time()
        return max(0, int(remaining))

# Usage
token = TokenWithExpiration("abc123", expires_in_seconds=3600)
print(f"Expired: {token.is_expired()}")
print(f"Expires in: {token.time_until_expiry()} seconds")
```

**Related Terms**: Access Token, Refresh Token, TTL

---

### Two-Factor Authentication (2FA)

**Definition**: An authentication method that requires two different verification factors, typically something you know (password) and something you have (phone).

**Example**:
```python
class TwoFactorAuth:
    def __init__(self):
        self.totp_secrets = {}

    def enable_2fa(self, user_id: str) -> dict:
        """Enable 2FA for a user."""
        secret = pyotp.random_base32()
        self.totp_secrets[user_id] = secret

        # Generate provisioning URI for QR code
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user_id,
            issuer_name="MyApp"
        )

        return {
            "secret": secret,
            "provisioning_uri": provisioning_uri,
        }

    def verify_2fa(self, user_id: str, code: str) -> bool:
        """Verify 2FA code."""
        if user_id not in self.totp_secrets:
            return False

        totp = pyotp.TOTP(self.totp_secrets[user_id])
        return totp.verify(code, valid_window=1)
```

**Related Terms**: MFA, TOTP, Authenticator App

---

*Part of the [AI Security Lecture Series](README.md). See also: [Lecture 06: Authentication & Authorization](06-authentication-authorization-lecture.md)*
