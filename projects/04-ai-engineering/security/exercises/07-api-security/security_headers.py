"""
07 Api Security: Security Headers
"""

from ._types import *

class SecurityHeaders:
    """
    Security headers for API responses.

    Implements OWASP recommended security headers.
    """

    def __init__(self):
        self._custom_headers: Dict[str, str] = {}

    def get_security_headers(self, request: Dict) -> Dict[str, str]:
        """Get all security headers for a response."""
        headers = {
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            # Clickjacking protection
            "X-Frame-Options": "DENY",
            # XSS protection (legacy browsers)
            "X-XSS-Protection": "1; mode=block",
            # Content Security Policy
            "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # Permissions policy
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            # Cache control for sensitive endpoints
            "Cache-Control": "no-store, no-cache, must-revalidate, private",
            "Pragma": "no-cache",
            # Prevent information leakage
            "Server": "AI-Platform",
            "X-Powered-By": "",  # Remove framework info
        }

        # Add custom headers
        headers.update(self._custom_headers)

        return headers

    def add_custom_header(self, name: str, value: str):
        """Add a custom security header."""
        self._custom_headers[name] = value


# =============================================================
# SECTION 8: Request Signing
# =============================================================


