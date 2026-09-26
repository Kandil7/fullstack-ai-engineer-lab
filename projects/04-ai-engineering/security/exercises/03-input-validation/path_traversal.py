"""
03 Input Validation: Path Traversal
"""

from ._types import *


class PathTraversalValidator:
    """
    Detects and prevents path traversal attacks in file paths.

    Protects against:
      1. Directory traversal (../)
      2. Absolute path injection
      3. Symlink attacks
      4. Null byte injection
    """

    def __init__(self, allowed_base_dirs: Optional[list[str]] = None):
        self.allowed_base_dirs = [
            Path(d).resolve() for d in (allowed_base_dirs or ["/tmp/uploads"])
        ]

    def validate(self, file_path: str, operation: str = "read") -> ValidationResult:
        """Validate a file path for traversal attacks."""
        threats = []
        details = {}

        # Check for null bytes
        if "\x00" in file_path:
            threats.append("null_byte_injection")
            details["null_byte"] = True

        # Check for directory traversal
        if ".." in file_path:
            threats.append("directory_traversal")
            details["parent_reference"] = file_path.count("..")

        # Check for absolute path injection
        if Path(file_path).is_absolute():
            threats.append("absolute_path")
            details["absolute_path"] = file_path

        # Check for URL-encoded traversal
        decoded = unquote(file_path)
        if decoded != file_path and (".." in decoded or "/" in decoded):
            threats.append("encoded_traversal")
            details["decoded_path"] = decoded

        # Normalize and check against allowed directories
        try:
            resolved = Path(file_path).resolve()
            # Check if the resolved path is within any allowed directory
            is_within_allowed = any(
                str(resolved).startswith(str(allowed))
                for allowed in self.allowed_base_dirs
            )
            if not is_within_allowed and self.allowed_base_dirs:
                threats.append("outside_allowed_directory")
                details["resolved_path"] = str(resolved)
        except (ValueError, OSError) as e:
            threats.append("invalid_path")
            details["error"] = str(e)

        # Calculate threat level
        if not threats:
            threat_level = ThreatLevel.SAFE
        elif "null_byte_injection" in threats:
            threat_level = ThreatLevel.CRITICAL
        elif "directory_traversal" in threats or "encoded_traversal" in threats:
            threat_level = ThreatLevel.MALICIOUS
        else:
            threat_level = ThreatLevel.SUSPICIOUS

        sanitized = self._sanitize(file_path)
        is_valid = threat_level.value <= ThreatLevel.SUSPICIOUS.value

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="PathTraversal",
            message=f"Path traversal {'detected' if threats else 'not detected'}",
            original_input=file_path,
            sanitized_output=sanitized,
            details={"threats": threats, **details},
        )

    def _sanitize(self, file_path: str) -> str:
        """Sanitize a file path."""
        # Remove null bytes
        sanitized = file_path.replace("\x00", "")
        # Decode URL encoding
        sanitized = unquote(sanitized)
        # Resolve to absolute path
        try:
            resolved = Path(sanitized).resolve()
            # Check if within allowed directories
            for allowed in self.allowed_base_dirs:
                try:
                    resolved.relative_to(allowed)
                    return str(resolved)
                except ValueError:
                    continue
        except (ValueError, OSError):
            pass
        # Fallback: strip traversal sequences
        sanitized = re.sub(r"\.\.[\\/]", "", sanitized)
        sanitized = sanitized.lstrip("/\\")
        return sanitized


# =============================================================================
# Section 6: Input Length & Encoding Validation
# =============================================================================
