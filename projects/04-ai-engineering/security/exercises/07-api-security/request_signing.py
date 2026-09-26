"""
07 Api Security: Request Signing
"""

from ._types import *


class RequestSigner:
    """
    Sign API requests for mutual TLS alternative.

    Uses HMAC-SHA256 to sign request components.
    """

    def __init__(self, api_secret: bytes):
        self.api_secret = api_secret

    def sign_request(
        self,
        method: str,
        path: str,
        body: bytes,
        timestamp: Optional[int] = None,
    ) -> Dict[str, str]:
        """Generate request signature and headers."""
        if timestamp is None:
            timestamp = int(time.time())

        # Create string to sign
        string_to_sign = (
            f"{method}\n{path}\n{timestamp}\n{body.decode('utf-8', errors='replace')}"
        )
        signature = hmac.new(
            self.api_secret,
            string_to_sign.encode(),
            hashlib.sha256,
        ).hexdigest()

        return {
            "X-Signature": signature,
            "X-Timestamp": str(timestamp),
            "X-API-Version": "2024-01-01",
        }

    def verify_request(
        self,
        method: str,
        path: str,
        body: bytes,
        headers: Dict[str, str],
        tolerance: int = 300,
    ) -> Dict:
        """Verify a request signature."""
        signature = headers.get("X-Signature", "")
        timestamp = int(headers.get("X-Timestamp", "0"))

        if not signature or not timestamp:
            return {"valid": False, "error": "Missing signature headers"}

        # Check timestamp
        if abs(time.time() - timestamp) > tolerance:
            return {"valid": False, "error": "Request timestamp expired"}

        # Compute expected signature
        string_to_sign = (
            f"{method}\n{path}\n{timestamp}\n{body.decode('utf-8', errors='replace')}"
        )
        expected = hmac.new(
            self.api_secret,
            string_to_sign.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            return {"valid": False, "error": "Invalid signature"}

        return {"valid": True, "timestamp": timestamp}


# =============================================================
# DEMONSTRATIONS
# =============================================================
