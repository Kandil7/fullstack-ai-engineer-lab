"""
03 Input Validation: Xss
"""

from ._types import *


class XSSValidator:
    """
    Detects and prevents Cross-Site Scripting (XSS) attacks.

    Covers:
      1. Script tag injection
      2. Event handler injection
      3. JavaScript URI schemes
      4. DOM-based XSS patterns
    """

    XSS_PATTERNS = {
        "script_tags": [
            r"<\s*script[^>]*>",
            r"</\s*script\s*>",
            r"<\s*script\b",
            r"javascript\s*:",
        ],
        "event_handlers": [
            r"(?i)\bon\w+\s*=\s*['\"].*?['\"]",  # onclick=, onerror=, etc.
            r"(?i)\bon\w+\s*=\s*\w+",  # onclick=functionName
        ],
        "javascript_uri": [
            r"(?i)javascript\s*:",
            r"(?i)vbscript\s*:",
            r"(?i)data\s*:\s*text/html",
            r"(?i)livescript\s*:",
        ],
        "dom_manipulation": [
            r"(?i)(eval|expression)\s*\(",
            r"(?i)document\.(write|writeln|cookie|location)",
            r"(?i)window\.(location|open|eval)",
            r"(?i)(innerHTML|outerHTML)\s*=",
            r"(?i)element\.(setAttribute|setAttributeNode)",
        ],
        "encoding_bypass": [
            r"(?i)&#\d+;",  # HTML entity encoding
            r"(?i)&#[xX][0-9a-f]+;",  # Hex entity encoding
            r"(?i)%3[Cc]script",  # URL encoded <
            r"(?i)%3[Ee]",  # URL encoded >
            r"(?i)\\u[0-9a-fA-F]{4}",  # Unicode escape
        ],
        "css_injection": [
            r"(?i)expression\s*\(",
            r"(?i)url\s*\(\s*['\"]?\s*javascript:",
            r"(?i)-moz-binding\s*:",
            r"(?i)behavior\s*:\s*url",
        ],
    }

    # Tags that should never appear in user content
    FORBIDDEN_TAGS = [
        "script",
        "iframe",
        "object",
        "embed",
        "applet",
        "form",
        "input",
        "button",
        "link",
        "meta",
        "base",
    ]

    def __init__(self, allowed_tags: Optional[list[str]] = None):
        self.allowed_tags = set(
            allowed_tags or ["b", "i", "u", "em", "strong", "p", "br"]
        )
        self.compiled_patterns: dict[str, list[re.Pattern]] = {}
        for category, patterns in self.XSS_PATTERNS.items():
            self.compiled_patterns[category] = [re.compile(pat) for pat in patterns]

    def validate(self, user_input: str) -> ValidationResult:
        """Validate input for XSS attacks."""
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

        # Forbidden tag detection
        tag_pattern = re.compile(r"<\s*(\w+)", re.IGNORECASE)
        found_tags = tag_pattern.findall(user_input)
        forbidden_found = [t for t in found_tags if t.lower() in self.FORBIDDEN_TAGS]
        if forbidden_found:
            threats.append("forbidden_tags")
            details["forbidden_tags"] = list(set(forbidden_found))

        # Calculate threat level
        if not threats:
            threat_level = ThreatLevel.SAFE
        elif "script_tags" in threats or "javascript_uri" in threats:
            threat_level = ThreatLevel.CRITICAL
        elif "event_handlers" in threats or "dom_manipulation" in threats:
            threat_level = ThreatLevel.MALICIOUS
        else:
            threat_level = ThreatLevel.SUSPICIOUS

        sanitized = self._sanitize(user_input)
        is_valid = threat_level.value <= ThreatLevel.SUSPICIOUS.value

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="XSS",
            message=f"XSS {'detected' if threats else 'not detected'}",
            original_input=user_input,
            sanitized_output=sanitized,
            details={"threats": threats, **details},
        )

    def _sanitize(self, input_str: str) -> str:
        """Sanitize HTML input to prevent XSS."""
        # HTML-escape all content
        sanitized = html.escape(input_str)

        # Re-allow only safe tags
        for tag in self.allowed_tags:
            # Restore allowed opening tags
            escaped_open = html.escape(f"<{tag}")
            original_open = f"<{tag}"
            sanitized = sanitized.replace(escaped_open, original_open)

            # Restore allowed closing tags
            escaped_close = html.escape(f"</{tag}>")
            original_close = f"</{tag}>"
            sanitized = sanitized.replace(escaped_close, original_close)

        return sanitized


# =============================================================================
# Section 4: Command Injection Prevention
# =============================================================================
