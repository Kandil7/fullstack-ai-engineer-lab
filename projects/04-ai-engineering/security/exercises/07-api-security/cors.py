"""
07 Api Security: Cors
"""

from ._types import *

class CORSPolicy:
    """
    Configurable CORS policy for AI service APIs.

    Security-first approach with explicit allowlists.
    """

    def __init__(self):
        self._allowed_origins: Set[str] = set()
        self._allowed_methods: Set[str] = {"GET", "POST", "OPTIONS"}
        self._allowed_headers: Set[str] = {
            "Authorization",
            "Content-Type",
            "X-Request-ID",
            "X-API-Key",
        }
        self._exposed_headers: Set[str] = {
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-Request-ID",
        }
        self._allow_credentials: bool = False
        self._max_age: int = 86400  # 24 hours
        self._allow_subdomains: bool = False

    def allow_origin(self, origin: str, allow_subdomains: bool = False):
        """Add an allowed origin."""
        # Validate origin format
        parsed = urlparse(origin)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid origin scheme: {parsed.scheme}")
        if not parsed.hostname:
            raise ValueError(f"Invalid origin: {origin}")

        self._allowed_origins.add(origin)
        self._allow_subdomains = allow_subdomains

    def allow_origin_pattern(self, pattern: str):
        """Add an allowed origin pattern (regex)."""
        # Store patterns for matching
        if not hasattr(self, "_origin_patterns"):
            self._origin_patterns = []
        self._origin_patterns.append(re.compile(pattern))

    def set_allowed_methods(self, methods: List[str]):
        """Set allowed HTTP methods."""
        valid_methods = {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}
        self._allowed_methods = set(m.upper() for m in methods) & valid_methods

    def set_allowed_headers(self, headers: List[str]):
        """Set allowed request headers."""
        self._allowed_headers = set(h.lower() for h in headers)

    def check_origin(self, origin: Optional[str], request_method: str = "GET") -> Dict:
        """
        Check if an origin is allowed and return CORS headers.

        Returns:
            Dict with allowed, headers, and error if not allowed
        """
        if not origin:
            # No origin header (same-origin or non-browser request)
            return {"allowed": True, "headers": {}, "note": "no_origin"}

        # Normalize origin
        origin = origin.strip().rstrip("/")

        # Check exact match
        if origin in self._allowed_origins:
            return self._build_cors_response(origin)

        # Check subdomains
        if self._allow_subdomains:
            parsed = urlparse(origin)
            for allowed in self._allowed_origins:
                allowed_parsed = urlparse(allowed)
                if (
                    parsed.hostname
                    and allowed_parsed.hostname
                    and parsed.hostname.endswith("." + allowed_parsed.hostname)
                ):
                    return self._build_cors_response(origin)

        # Check patterns
        if hasattr(self, "_origin_patterns"):
            for pattern in self._origin_patterns:
                if pattern.match(origin):
                    return self._build_cors_response(origin)

        # Origin not allowed
        return {
            "allowed": False,
            "headers": {},
            "error": f"Origin not allowed: {origin}",
        }

    def _build_cors_response(self, origin: str) -> Dict:
        """Build CORS response headers."""
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": ", ".join(sorted(self._allowed_methods)),
            "Access-Control-Allow-Headers": ", ".join(sorted(self._allowed_headers)),
            "Access-Control-Expose-Headers": ", ".join(sorted(self._exposed_headers)),
            "Access-Control-Max-Age": str(self._max_age),
        }

        if self._allow_credentials:
            headers["Access-Control-Allow-Credentials"] = "true"

        return {"allowed": True, "headers": headers}


# =============================================================
# SECTION 3: HTTPS Enforcement
# =============================================================


