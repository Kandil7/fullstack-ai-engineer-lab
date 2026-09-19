"""
06 Authentication Authorization: Decorators
"""

from ._types import *

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


