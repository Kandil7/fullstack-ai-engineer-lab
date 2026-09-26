"""
06 Authentication Authorization: Rbac
"""

from ._types import *
from .sessions import Session


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
        self.add_role(
            Role(
                name="viewer",
                permissions=[
                    Permission("models", {"read"}),
                    Permission("data", {"read"}),
                    Permission("logs", {"read"}),
                ],
            )
        )

        # Developer: Can run inference
        self.add_role(
            Role(
                name="developer",
                permissions=[
                    Permission("models", {"read", "inference"}),
                    Permission("data", {"read"}),
                    Permission("experiments", {"read", "write"}),
                ],
                inherits=["viewer"],
            )
        )

        # Data Scientist: Can train models
        self.add_role(
            Role(
                name="data_scientist",
                permissions=[
                    Permission("models", {"read", "write", "train"}),
                    Permission("data", {"read", "write"}),
                    Permission("experiments", {"read", "write", "delete"}),
                ],
                inherits=["developer"],
            )
        )

        # Admin: Full access
        self.add_role(
            Role(
                name="admin",
                permissions=[
                    Permission("*", {"read", "write", "delete", "admin"}),
                ],
                inherits=["data_scientist"],
            )
        )

        # API Service: Limited to inference
        self.add_role(
            Role(
                name="api_service",
                permissions=[
                    Permission("models", {"read", "inference"}),
                    Permission("predictions", {"write"}),
                ],
            )
        )

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
            if perm.resource in ("*", resource) and (
                action in perm.actions or "*" in perm.actions
            ):
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
