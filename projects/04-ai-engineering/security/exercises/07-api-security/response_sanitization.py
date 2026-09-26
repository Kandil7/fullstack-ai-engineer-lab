"""
07 Api Security: Response Sanitization
"""

from ._types import *


class ResponseSanitizer:
    """
    Protect against data leakage in API responses.

    Features:
    - Remove sensitive fields
    - Mask PII data
    - Prevent internal error details leakage
    - Safe error messages
    """

    SENSITIVE_FIELDS = {
        "password",
        "password_hash",
        "secret",
        "api_key",
        "api_secret",
        "access_token",
        "refresh_token",
        "private_key",
        "credit_card",
        "ssn",
        "social_security",
        "bank_account",
        "routing_number",
    }

    PII_FIELDS = {
        "email",
        "phone",
        "address",
        "ssn",
        "credit_card",
        "date_of_birth",
        "full_name",
    }

    INTERNAL_ERROR_MESSAGES = {
        "database error",
        "connection refused",
        "permission denied",
        "file not found",
        "null pointer",
        "stack trace",
        "traceback",
    }

    def __init__(self):
        self._masking_rules: Dict[str, Callable] = {}

    def sanitize_response(self, data: Any, context: str = "api") -> Any:
        """Sanitize response data based on context."""
        if isinstance(data, dict):
            return self._sanitize_dict(data, context)
        elif isinstance(data, list):
            return [self.sanitize_response(item, context) for item in data]
        elif isinstance(data, str):
            return self._sanitize_string_response(data)
        return data

    def _sanitize_dict(self, data: Dict, context: str) -> Dict:
        """Sanitize dictionary response."""
        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()

            # Remove sensitive fields
            if key_lower in self.SENSITIVE_FIELDS:
                continue

            # Mask PII fields
            if key_lower in self.PII_FIELDS and isinstance(value, str):
                sanitized[key] = self._mask_pii(key_lower, value)
            elif isinstance(value, (dict, list)):
                sanitized[key] = self.sanitize_response(value, context)
            else:
                sanitized[key] = value

        return sanitized

    def _sanitize_string_response(self, value: str) -> str:
        """Sanitize string response to prevent XSS."""
        # Remove HTML tags
        value = re.sub(r"<[^>]+>", "", value)
        # Remove javascript: protocol
        value = re.sub(r"javascript:", "", value, flags=re.IGNORECASE)
        return value

    def _mask_pii(self, field_type: str, value: str) -> str:
        """Mask PII data."""
        if field_type == "email":
            if "@" in value:
                local, domain = value.split("@", 1)
                masked_local = local[0] + "***" + local[-1] if len(local) > 1 else "***"
                return f"{masked_local}@{domain}"
            return "***@***"

        elif field_type == "phone":
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 10:
                return f"({digits[:3]}) ***-**{digits[-2:]}"
            return "***"

        elif field_type == "credit_card":
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 16:
                return f"****-****-****-{digits[-4:]}"
            return "****"

        elif field_type == "ssn":
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 4:
                return f"***-**-{digits[-4:]}"
            return "***"

        return "***"

    def sanitize_error(self, error: Exception, include_details: bool = False) -> Dict:
        """
        Create a safe error response that doesn't leak internals.
        """
        error_msg = str(error).lower()

        # Check for internal error patterns
        is_internal = any(
            pattern in error_msg for pattern in self.INTERNAL_ERROR_MESSAGES
        )

        if is_internal or not include_details:
            return {
                "error": "An internal error occurred",
                "error_code": "INTERNAL_ERROR",
                "request_id": str(secrets.token_urlsafe(16)),
            }

        return {
            "error": str(error)[:200],  # Limit error message length
            "error_code": "VALIDATION_ERROR",
        }

    def add_masking_rule(self, field_name: str, mask_func: Callable):
        """Add custom masking rule for a field."""
        self._masking_rules[field_name.lower()] = mask_func


# =============================================================
# SECTION 6: Webhook Verification
# =============================================================
