"""
06 Authentication Authorization: Demos
"""

from ._types import *

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
    print(
        f"Token introspection: active={introspection['active']}, sub={introspection.get('sub')}"
    )

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
    print(
        f"  Can delete experiments: {rbac.check_permission('alice', 'experiments', 'delete')}"
    )

    print("\nBob (developer):")
    print(f"  Can run inference: {rbac.check_permission('bob', 'models', 'inference')}")
    print(f"  Can train models: {rbac.check_permission('bob', 'models', 'train')}")
    print(f"  Can write data: {rbac.check_permission('bob', 'data', 'write')}")

    print("\nCharlie (viewer):")
    print(f"  Can read models: {rbac.check_permission('charlie', 'models', 'read')}")
    print(
        f"  Can run inference: {rbac.check_permission('charlie', 'models', 'inference')}"
    )

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

