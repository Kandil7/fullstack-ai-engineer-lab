"""
07 Api Security: Request Validation
"""

from ._types import *

class RequestValidator:
    """
    Comprehensive request validation for API security.

    Features:
    - JSON schema validation
    - Input sanitization
    - SQL injection prevention
    - XSS prevention
    - Path traversal prevention
    """

    def __init__(self):
        self._max_body_size = 10 * 1024 * 1024  # 10MB
        self._max_url_length = 2048
        self._blocked_patterns = [
            # SQL injection patterns
            re.compile(
                r"(?i)(union\s+select|insert\s+into|drop\s+table|delete\s+from)"
            ),
            re.compile(r"(?i)(--\s|;\s*drop|;\s*delete|;\s*update)"),
            # XSS patterns
            re.compile(r"<script[^>]*>", re.IGNORECASE),
            re.compile(r"javascript:", re.IGNORECASE),
            re.compile(r"on\w+\s*=", re.IGNORECASE),
            # Path traversal
            re.compile(r"\.\./"),
            re.compile(r"\.\.\\"),
            # Command injection
            re.compile(r"[;&|`$]"),
        ]

    def validate_request(self, request: Dict) -> Dict:
        """
        Validate a complete request.

        Args:
            request: Dict with method, path, headers, body, query_params

        Returns:
            Dict with valid, errors, sanitized_request
        """
        errors = []
        sanitized = request.copy()

        # Validate method
        if request.get("method") not in (
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
            "HEAD",
        ):
            errors.append("Invalid HTTP method")

        # Validate URL length
        url = request.get("path", "")
        if len(url) > self._max_url_length:
            errors.append(f"URL too long: {len(url)} > {self._max_url_length}")

        # Validate body size
        body = request.get("body", "")
        if isinstance(body, str) and len(body) > self._max_body_size:
            errors.append(f"Body too large: {len(body)} > {self._max_body_size}")

        # Check for blocked patterns
        check_strings = [url, str(body)]
        for header_val in request.get("headers", {}).values():
            check_strings.append(str(header_val))

        for check_str in check_strings:
            for pattern in self._blocked_patterns:
                if pattern.search(check_str):
                    errors.append(f"Blocked pattern detected: {pattern.pattern}")
                    break

        # Validate query parameters
        query_params = request.get("query_params", {})
        for key, value in query_params.items():
            if isinstance(value, str):
                for pattern in self._blocked_patterns:
                    if pattern.search(value):
                        errors.append(f"Blocked pattern in query param '{key}'")
                        break

        # Sanitize inputs
        sanitized["path"] = self._sanitize_string(url)
        if isinstance(sanitized.get("body"), str):
            sanitized["body"] = self._sanitize_string(sanitized["body"])

        # Validate JSON content type for POST/PUT/PATCH
        method = request.get("method", "")
        content_type = request.get("headers", {}).get("content-type", "")
        if method in ("POST", "PUT", "PATCH"):
            if (
                "application/json" not in content_type
                and "multipart/form-data" not in content_type
            ):
                errors.append(f"Invalid content type for {method}: {content_type}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "sanitized_request": sanitized,
        }

    def _sanitize_string(self, value: str) -> str:
        """Sanitize a string input."""
        # Remove null bytes
        value = value.replace("\x00", "")
        # Encode HTML entities
        value = value.replace("&", "&amp;")
        value = value.replace("<", "&lt;")
        value = value.replace(">", "&gt;")
        value = value.replace('"', "&quot;")
        value = value.replace("'", "&#x27;")
        return value

    def validate_json_body(self, body: Any, schema: Dict) -> Dict:
        """
        Validate JSON body against a simple schema.

        Schema format:
        {
            "field_name": {"type": "string", "required": True, "max_length": 100},
            "field_name2": {"type": "integer", "required": False, "min": 0, "max": 100},
        }
        """
        errors = []

        if not isinstance(body, dict):
            return {"valid": False, "errors": ["Body must be a JSON object"]}

        for field_name, rules in schema.items():
            value = body.get(field_name)

            # Check required
            if rules.get("required", False) and value is None:
                errors.append(f"Missing required field: {field_name}")
                continue

            if value is None:
                continue

            # Check type
            expected_type = rules.get("type")
            if expected_type == "string" and not isinstance(value, str):
                errors.append(f"Field '{field_name}' must be a string")
            elif expected_type == "integer" and not isinstance(value, int):
                errors.append(f"Field '{field_name}' must be an integer")
            elif expected_type == "number" and not isinstance(value, (int, float)):
                errors.append(f"Field '{field_name}' must be a number")
            elif expected_type == "boolean" and not isinstance(value, bool):
                errors.append(f"Field '{field_name}' must be a boolean")
            elif expected_type == "array" and not isinstance(value, list):
                errors.append(f"Field '{field_name}' must be an array")

            # String constraints
            if isinstance(value, str):
                if "max_length" in rules and len(value) > rules["max_length"]:
                    errors.append(
                        f"Field '{field_name}' exceeds max length: {len(value)} > {rules['max_length']}"
                    )
                if "pattern" in rules and not re.match(rules["pattern"], value):
                    errors.append(
                        f"Field '{field_name}' doesn't match pattern: {rules['pattern']}"
                    )
                if "enum" in rules and value not in rules["enum"]:
                    errors.append(
                        f"Field '{field_name}' must be one of: {rules['enum']}"
                    )

            # Number constraints
            if isinstance(value, (int, float)):
                if "min" in rules and value < rules["min"]:
                    errors.append(
                        f"Field '{field_name}' is below minimum: {value} < {rules['min']}"
                    )
                if "max" in rules and value > rules["max"]:
                    errors.append(
                        f"Field '{field_name}' exceeds maximum: {value} > {rules['max']}"
                    )

            # Array constraints
            if isinstance(value, list):
                if "max_items" in rules and len(value) > rules["max_items"]:
                    errors.append(
                        f"Field '{field_name}' exceeds max items: {len(value)} > {rules['max_items']}"
                    )
                if "item_type" in rules:
                    for i, item in enumerate(value):
                        if rules["item_type"] == "string" and not isinstance(item, str):
                            errors.append(f"Field '{field_name}[{i}]' must be a string")

        return {"valid": len(errors) == 0, "errors": errors}


# =============================================================
# SECTION 5: Response Sanitization
# =============================================================


