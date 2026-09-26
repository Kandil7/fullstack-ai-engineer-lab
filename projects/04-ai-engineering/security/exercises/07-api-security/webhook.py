"""
07 Api Security: Webhook
"""

from ._types import *


class WebhookVerifier:
    """
    Verify webhook authenticity using HMAC signatures.

    Supports:
    - HMAC-SHA256 signatures
    - Timestamp verification (replay protection)
    - Multiple signature algorithms
    """

    def __init__(self, secret: bytes, tolerance: int = 300):
        """
        Args:
            secret: Webhook signing secret
            tolerance: Max age of webhook in seconds (default 5 min)
        """
        self.secret = secret
        self.tolerance = tolerance
        self._processed_events: Set[str] = set()

    def generate_signature(
        self,
        payload: bytes,
        timestamp: Optional[int] = None,
        algorithm: str = "sha256",
    ) -> str:
        """Generate a webhook signature."""
        if timestamp is None:
            timestamp = int(time.time())

        # Create signed payload
        signed_payload = f"{timestamp}.{payload.decode('utf-8', errors='replace')}"
        signature = hmac.new(
            self.secret,
            signed_payload.encode(),
            getattr(hashlib, algorithm),
        ).hexdigest()

        return f"t={timestamp},{algorithm}={signature}"

    def verify_signature(
        self,
        payload: bytes,
        signature_header: str,
        algorithm: str = "sha256",
    ) -> Dict:
        """
        Verify a webhook signature.

        Args:
            payload: Raw request body
            signature_header: Value from signature header
            algorithm: Hash algorithm

        Returns:
            Dict with valid, error, timestamp
        """
        try:
            # Parse signature header
            parts = {}
            for part in signature_header.split(","):
                if "=" in part:
                    key, value = part.split("=", 1)
                    parts[key.strip()] = value.strip()

            timestamp = int(parts.get("t", 0))
            expected_sig = parts.get(algorithm, "")

            if not timestamp or not expected_sig:
                return {"valid": False, "error": "Invalid signature format"}

            # Check timestamp tolerance
            current_time = int(time.time())
            if abs(current_time - timestamp) > self.tolerance:
                return {
                    "valid": False,
                    "error": f"Webhook timestamp outside tolerance: {abs(current_time - timestamp)}s",
                }

            # Compute expected signature
            signed_payload = f"{timestamp}.{payload.decode('utf-8', errors='replace')}"
            computed_sig = hmac.new(
                self.secret,
                signed_payload.encode(),
                getattr(hashlib, algorithm),
            ).hexdigest()

            # Constant-time comparison
            if not hmac.compare_digest(computed_sig, expected_sig):
                return {"valid": False, "error": "Signature mismatch"}

            # Check for replay
            event_id = f"{timestamp}:{computed_sig[:16]}"
            if event_id in self._processed_events:
                return {"valid": False, "error": "Duplicate webhook (replay detected)"}

            self._processed_events.add(event_id)

            return {
                "valid": True,
                "timestamp": timestamp,
                "algorithm": algorithm,
            }

        except Exception as e:
            return {"valid": False, "error": f"Verification error: {e}"}


# =============================================================
# SECTION 7: Security Headers Middleware
# =============================================================
