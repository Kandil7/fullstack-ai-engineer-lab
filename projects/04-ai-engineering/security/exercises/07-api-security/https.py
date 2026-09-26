"""
07 Api Security: Https
"""

from ._types import *


class HTTPSEnforcer:
    """
    HTTPS enforcement with HSTS and redirect handling.
    """

    def __init__(
        self,
        max_age: int = 31536000,  # 1 year
        include_subdomains: bool = True,
        preload: bool = True,
    ):
        self.hsts_max_age = max_age
        self.include_subdomains = include_subdomains
        self.preload = preload
        self._trusted_proxies: Set[str] = set()

    def add_trusted_proxy(self, proxy_ip: str):
        """Add a trusted reverse proxy IP."""
        self._trusted_proxies.add(proxy_ip)

    def get_hsts_header(self) -> str:
        """Generate the HSTS header value."""
        directives = [f"max-age={self.hsts_max_age}"]
        if self.include_subdomains:
            directives.append("includeSubDomains")
        if self.preload:
            directives.append("preload")
        return "; ".join(directives)

    def check_request(self, request: Dict) -> Dict:
        """
        Check if request should be redirected to HTTPS.

        Args:
            request: Dict with scheme, host, path, headers, client_ip

        Returns:
            Dict with redirect_needed, redirect_url, headers
        """
        scheme = request.get("scheme", "http")
        host = request.get("host", "")
        path = request.get("path", "/")
        client_ip = request.get("client_ip", "")

        # If already HTTPS, just add HSTS header
        if scheme == "https":
            return {
                "redirect_needed": False,
                "headers": {
                    "Strict-Transport-Security": self.get_hsts_header(),
                },
            }

        # Check if request is from a trusted proxy
        if client_ip in self._trusted_proxies:
            # Behind proxy -- check X-Forwarded-Proto
            forwarded_proto = request.get("headers", {}).get(
                "X-Forwarded-Proto", "https"
            )
            if forwarded_proto == "https":
                return {
                    "redirect_needed": False,
                    "headers": {
                        "Strict-Transport-Security": self.get_hsts_header(),
                    },
                }

        # Build redirect URL
        redirect_url = f"https://{host}{path}"

        return {
            "redirect_needed": True,
            "redirect_url": redirect_url,
            "status_code": 301,
            "headers": {
                "Location": redirect_url,
                "Strict-Transport-Security": self.get_hsts_header(),
            },
        }


# =============================================================
# SECTION 4: Request Validation
# =============================================================
