"""
06 Authentication Authorization: Api Keys
"""

from ._types import *
from .rbac import Role

@dataclass
class APIKey:
    key_id: str
    key_hash: str  # We never store raw keys
    prefix: str  # First 8 chars for identification
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


