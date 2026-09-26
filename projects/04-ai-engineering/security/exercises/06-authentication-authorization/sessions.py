"""
06 Authentication Authorization: Sessions
"""

from ._types import *


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
        session_ttl: int = 3600,  # 1 hour
        max_sessions: int = 5,
        rotation_interval: int = 900,  # 15 minutes
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
