"""
03 Input Validation: Sql Injection
"""

from ._types import *

class SQLInjectionValidator:
    """
    Detects and prevents SQL injection attacks in user inputs.

    Strategies:
      1. Pattern-based detection of SQL syntax
      2. Parameterized query enforcement
      3. Input encoding for safe database insertion
    """

    # SQL injection patterns organized by technique
    INJECTION_PATTERNS = {
        "classic_union": [
            r"(?i)(UNION\s+(ALL\s+)?SELECT)",
            r"(?i)(SELECT\s+.*\s+FROM\s+.*\s+WHERE)",
            r"(?i)(INSERT\s+INTO\s+.*\s+VALUES)",
            r"(?i)(DELETE\s+FROM\s+.*\s+WHERE)",
            r"(?i)(UPDATE\s+.*\s+SET\s+.*\s+WHERE)",
            r"(?i)(DROP\s+(TABLE|DATABASE|COLUMN))",
        ],
        "blind_injection": [
            r"(?i)(AND\s+\d+\s*=\s*\d+)",
            r"(?i)(OR\s+\d+\s*=\s*\d+)",
            r"(?i)(AND\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?)",
            r"(?i)(OR\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?)",
            r"(?i)(AND\s+SUBSTRING)",
            r"(?i)(AND\s+ASCII)",
            r"(?i)(AND\s+LENGTH)",
        ],
        "time_based": [
            r"(?i)(WAITFOR\s+DELAY)",
            r"(?i)(SLEEP\s*\(\s*\d+\s*\))",
            r"(?i)(BENCHMARK\s*\()",
            r"(?i)(PG_SLEEP\s*\()",
            r"(?i)(LOAD_FILE\s*\()",
        ],
        "stacked_queries": [
            r";\s*(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)",
            r";\s*--",
            r";\s*/\*",
        ],
        "comment_abuse": [
            r"--\s*$",
            r"/\*.*\*/",
            r"#\s*$",
        ],
        "encoding_tricks": [
            r"(?i)(0x[0-9a-fA-F]{4,})",  # Hex-encoded strings
            r"(?i)(CHAR\s*\(\s*\d+)",  # CHAR() encoding
            r"(?i)(CONCAT\s*\()",  # String concatenation
            r"(?i)(EXEC\s*\(|EXECUTE\s*\()",  # Dynamic execution
        ],
    }

    # SQL keywords that are suspicious in user input
    DANGEROUS_KEYWORDS = [
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "CREATE",
        "ALTER",
        "EXEC",
        "EXECUTE",
        "UNION",
        "WHERE",
        "FROM",
        "TABLE",
        "DATABASE",
        "GRANT",
        "REVOKE",
        "TRUNCATE",
        "MERGE",
        "DECLARE",
        "CURSOR",
    ]

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.compiled_patterns: dict[str, list[re.Pattern]] = {}
        for category, patterns in self.INJECTION_PATTERNS.items():
            self.compiled_patterns[category] = [re.compile(pat) for pat in patterns]

    def validate(self, user_input: str) -> ValidationResult:
        """Validate input for SQL injection attempts."""
        threats = []
        details = {}

        # Pattern matching
        for category, patterns in self.compiled_patterns.items():
            matches = []
            for pattern in patterns:
                found = pattern.findall(user_input)
                if found:
                    matches.extend(found[:3])
            if matches:
                threats.append(category)
                details[category] = matches[:5]

        # Keyword density analysis
        words = re.findall(r"\b\w+\b", user_input.upper())
        keyword_count = sum(1 for w in words if w in self.DANGEROUS_KEYWORDS)
        keyword_ratio = keyword_count / max(len(words), 1)

        if keyword_ratio > 0.3:
            threats.append("high_keyword_density")
            details["keyword_ratio"] = f"{keyword_ratio:.2%}"

        # Semicolon + keyword combo
        if ";" in user_input:
            for kw in self.DANGEROUS_KEYWORDS:
                if kw.lower() in user_input.lower().split(";")[1:]:
                    threats.append("stacked_query嫌疑")
                    break

        # Calculate threat level
        if not threats:
            threat_level = ThreatLevel.SAFE
        elif len(threats) == 1 and "comment_abuse" in threats:
            threat_level = ThreatLevel.SUSPICIOUS
        elif "classic_union" in threats or "stacked_queries" in threats:
            threat_level = ThreatLevel.CRITICAL
        elif "blind_injection" in threats or "time_based" in threats:
            threat_level = ThreatLevel.MALICIOUS
        else:
            threat_level = ThreatLevel.SUSPICIOUS

        # Sanitize output
        sanitized = self._sanitize(user_input) if self.strict_mode else user_input

        is_valid = threat_level.value <= ThreatLevel.SUSPICIOUS.value

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="SQLInjection",
            message=f"SQL injection {'detected' if threats else 'not detected'}",
            original_input=user_input,
            sanitized_output=sanitized,
            details={"threats": threats, **details},
        )

    def _sanitize(self, input_str: str) -> str:
        """Sanitize input for safe SQL parameterization."""
        # Escape single quotes (basic defense - prefer parameterized queries)
        sanitized = input_str.replace("'", "''")
        # Remove null bytes
        sanitized = sanitized.replace("\x00", "")
        # Encode dangerous characters
        sanitized = sanitized.replace(";", "\\;")
        return sanitized

    @staticmethod
    def create_parameterized_query(
        template: str, params: dict[str, Any]
    ) -> tuple[str, list[Any]]:
        """
        Create a parameterized query to prevent SQL injection.

        Args:
            template: SQL template with :param placeholders
            params: Dictionary of parameter values

        Returns:
            Tuple of (safe_query, param_values)
        """
        import re as _re

        param_names = _re.findall(r":(\w+)", template)
        safe_template = _re.sub(r":(\w+)", "?", template)
        param_values = [params[name] for name in param_names]
        return safe_template, param_values


# =============================================================================
# Section 3: XSS Prevention
# =============================================================================


