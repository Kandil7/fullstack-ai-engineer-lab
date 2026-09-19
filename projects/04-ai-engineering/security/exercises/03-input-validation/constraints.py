"""
03 Input Validation: Constraints
"""

from ._types import *

@dataclass
class InputConstraints:
    """Configuration for input validation constraints."""

    max_length: int = 10000
    min_length: int = 1
    allowed_encodings: list[str] = field(default_factory=lambda: ["utf-8"])
    max_line_count: int = 1000
    max_word_count: int = 5000
    allow_null_bytes: bool = False
    allow_control_chars: bool = False
    required_pattern: Optional[str] = None


class ConstraintValidator:
    """
    Validates inputs against configurable constraints including
    length limits, encoding validation, and pattern matching.
    """

    def __init__(self, constraints: Optional[InputConstraints] = None):
        self.constraints = constraints or InputConstraints()

    def validate(self, text: str) -> ValidationResult:
        """Validate input against all configured constraints."""
        violations = []
        details = {}

        # Length check
        if len(text) > self.constraints.max_length:
            violations.append(
                f"Exceeds max length ({len(text)} > {self.constraints.max_length})"
            )
            details["length"] = len(text)

        if len(text) < self.constraints.min_length:
            violations.append(
                f"Below min length ({len(text)} < {self.constraints.min_length})"
            )
            details["length"] = len(text)

        # Null byte check
        if not self.constraints.allow_null_bytes and "\x00" in text:
            violations.append("Contains null bytes")
            details["null_bytes"] = text.count("\x00")

        # Control character check
        if not self.constraints.allow_control_chars:
            control_chars = [c for c in text if ord(c) < 32 and c not in "\n\r\t"]
            if control_chars:
                violations.append(f"Contains {len(control_chars)} control characters")
                details["control_chars"] = len(control_chars)

        # Line count check
        line_count = text.count("\n") + 1
        if line_count > self.constraints.max_line_count:
            violations.append(
                f"Too many lines ({line_count} > {self.constraints.max_line_count})"
            )
            details["line_count"] = line_count

        # Word count check
        words = text.split()
        if len(words) > self.constraints.max_word_count:
            violations.append(
                f"Too many words ({len(words)} > {self.constraints.max_word_count})"
            )
            details["word_count"] = len(words)

        # Encoding validation
        try:
            text.encode("utf-8")
        except UnicodeEncodeError:
            violations.append("Invalid UTF-8 encoding")
            details["encoding_error"] = True

        # Pattern validation
        if self.constraints.required_pattern:
            if not re.match(self.constraints.required_pattern, text):
                violations.append(
                    f"Does not match required pattern: {self.constraints.required_pattern}"
                )

        # Calculate threat level
        if not violations:
            threat_level = ThreatLevel.SAFE
        elif any("null" in v.lower() for v in violations):
            threat_level = ThreatLevel.CRITICAL
        elif any("length" in v.lower() or "line" in v.lower() for v in violations):
            threat_level = ThreatLevel.SUSPICIOUS
        else:
            threat_level = ThreatLevel.MALICIOUS

        sanitized = self._sanitize(text)
        is_valid = len(violations) == 0

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="Constraint",
            message=f"{len(violations)} constraint violation(s) found",
            original_input=text,
            sanitized_output=sanitized,
            details={"violations": violations, **details},
        )

    def _sanitize(self, text: str) -> str:
        """Sanitize input to meet constraints."""
        sanitized = text
        # Remove null bytes
        if not self.constraints.allow_null_bytes:
            sanitized = sanitized.replace("\x00", "")
        # Truncate to max length
        sanitized = sanitized[: self.constraints.max_length]
        # Limit lines
        lines = sanitized.split("\n")[: self.constraints.max_line_count]
        sanitized = "\n".join(lines)
        return sanitized


# =============================================================================
# Section 7: Validation Pipeline
# =============================================================================


