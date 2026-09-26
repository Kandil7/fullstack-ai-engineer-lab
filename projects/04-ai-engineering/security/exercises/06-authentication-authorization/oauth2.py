"""
06 Authentication Authorization: Oauth2
"""

from ._types import *


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
            if not self._verify_pkce(
                code_data["code_challenge"],
                code_verifier,
                code_data["code_challenge_method"],
            ):
                raise SecurityError("PKCE verification failed")

        # Mark code as used
        code_data["used"] = True

        # Create tokens
        access_token = self.jwt_manager.create_access_token(
            user_id=client_id,
            roles=["oauth2_client"],
            metadata={
                "scopes": code_data["scopes"],
                "grant_type": "authorization_code",
            },
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
            computed = (
                base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
                .rstrip(b"=")
                .decode()
            )
            return hmac.compare_digest(computed, challenge)
        elif method == "plain":
            return hmac.compare_digest(verifier, challenge)
        return False

    def _invalidate_client_tokens(self, client_id: str):
        """Invalidate all tokens for a client (security measure)."""
        to_remove = [
            t for t, tok in self._tokens.items() if tok.scope and client_id in t
        ]
        for t in to_remove:
            self.jwt_manager.revoke_token(t)


# =============================================================
# SECTION 3: API Key Management
# =============================================================
