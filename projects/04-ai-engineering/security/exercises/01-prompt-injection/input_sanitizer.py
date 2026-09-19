"""
01 Prompt Injection: Input Sanitizer
"""

from ._types import *

class InputSanitizer:
    """
    Sanitizes user input to prevent prompt injection attacks.

    Uses multiple layers of defense:
      1. Pattern matching against known attacks
      2. Character encoding normalization
      3. Structural analysis
      4. Content length limits
    """

    def __init__(self, max_input_length: int = 4096):
        self.max_input_length = max_input_length
        self.blocked_patterns = self._build_blocklist()
        self.suspicious_pattern_cache: dict[str, float] = {}
        self.alert_threshold = 3  # Alert after N suspicious signals

    def _build_blocklist(self) -> list[re.Pattern]:
        """Build compiled regex patterns for known attacks."""
        patterns = []
        for sig in ATTACK_SIGNATURES:
            for pat_str in sig.patterns:
                try:
                    patterns.append(re.compile(pat_str))
                except re.error as e:
                    logger.warning(f"Invalid regex pattern: {pat_str} -> {e}")
        return patterns

    def sanitize(self, user_input: str) -> tuple[str, list[str]]:
        """
        Sanitize user input and return cleaned version + warnings.

        Args:
            user_input: Raw user input string

        Returns:
            Tuple of (sanitized_input, list_of_warnings)
        """
        warnings = []
        cleaned = user_input

        # Layer 1: Length check
        if len(user_input) > self.max_input_length:
            cleaned = user_input[: self.max_input_length]
            warnings.append(
                f"Input truncated from {len(user_input)} to {self.max_input_length} chars"
            )

        # Layer 2: Unicode normalization (defeat homoglyph attacks)
        cleaned = self._normalize_unicode(cleaned)
        if cleaned != user_input[: self.max_input_length]:
            warnings.append("Unicode normalization applied")

        # Layer 3: Pattern-based detection
        detected = self._detect_patterns(cleaned)
        warnings.extend(detected)

        # Layer 4: Structural analysis
        structural_warnings = self._analyze_structure(cleaned)
        warnings.extend(structural_warnings)

        # Layer 5: Encoding detection
        encoding_warnings = self._detect_encoding_tricks(cleaned)
        warnings.extend(encoding_warnings)

        return cleaned, warnings

    def _normalize_unicode(self, text: str) -> str:
        """Normalize unicode characters to prevent homoglyph attacks."""
        import unicodedata

        # NFKC normalization: compatibility decomposition + canonical composition
        normalized = unicodedata.normalize("NFKC", text)

        # Replace common homoglyphs
        homoglyph_map = {
            "\u0440": "p",  # Cyrillic р -> Latin p
            "\u043e": "o",  # Cyrillic о -> Latin o
            "\u0430": "a",  # Cyrillic а -> Latin a
            "\u0435": "e",  # Cyrillic е -> Latin e
            "\u0441": "c",  # Cyrillic с -> Latin c
            "\u200b": "",  # Zero-width space
            "\u200c": "",  # Zero-width non-joiner
            "\u200d": "",  # Zero-width joiner
            "\ufeff": "",  # Zero-width no-break space
        }
        for char, replacement in homoglyph_map.items():
            normalized = normalized.replace(char, replacement)

        return normalized

    def _detect_patterns(self, text: str) -> list[str]:
        """Detect known attack patterns in input."""
        warnings = []
        for pattern in self.blocked_patterns:
            if pattern.search(text):
                sig_name = next(
                    (
                        s.name
                        for s in ATTACK_SIGNATURES
                        if any(p == pattern.pattern for p in s.patterns)
                    ),
                    "unknown",
                )
                warnings.append(f"Detected attack pattern: {sig_name}")
                logger.warning(f"Attack pattern detected: {sig_name} in input")
        return warnings

    def _analyze_structure(self, text: str) -> list[str]:
        """Analyze structural anomalies in input."""
        warnings = []

        # Check for prompt-like structures
        prompt_markers = ["```", "<<<", ">>>", "[[", "]]", "<<", ">>"]
        for marker in prompt_markers:
            if text.count(marker) > 2:
                warnings.append(f"Suspicious structural pattern: repeated '{marker}'")

        # Check for role impersonation markers
        role_patterns = [
            (r"(?i)^(system|assistant|user)\s*:", "Potential role prefix detected"),
            (
                r"(?i)^###\s*(system|instruction)",
                "Potential instruction header detected",
            ),
        ]
        for pat, msg in role_patterns:
            if re.search(pat, text, re.MULTILINE):
                warnings.append(msg)

        # Check for excessive newline injection (separation attacks)
        newline_count = text.count("\n")
        if newline_count > 20:
            warnings.append(
                f"Excessive newlines ({newline_count}) - possible separation attack"
            )

        return warnings

    def _detect_encoding_tricks(self, text: str) -> list[str]:
        """Detect encoding-based evasion attempts."""
        warnings = []

        # High ratio of special characters may indicate encoding tricks
        special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
        ratio = special_chars / max(len(text), 1)
        if ratio > 0.5 and len(text) > 20:
            warnings.append(
                f"High special character ratio ({ratio:.0%}) - possible encoding evasion"
            )

        # Check for base64-like patterns
        b64_pattern = re.compile(r"^[A-Za-z0-9+/]{20,}={0,2}$", re.MULTILINE)
        lines = text.strip().split("\n")
        b64_lines = sum(1 for line in lines if b64_pattern.match(line.strip()))
        if b64_lines > 0 and b64_lines == len(lines):
            warnings.append("Possible base64-encoded payload detected")

        # Check for binary patterns
        binary_pattern = re.compile(r"^[01]{8}(\s+[01]{8})+\s*$", re.MULTILINE)
        if binary_pattern.search(text):
            warnings.append("Possible binary-encoded payload detected")

        return warnings

    def get_risk_score(self, warnings: list[str]) -> float:
        """Calculate a risk score (0.0 - 1.0) based on detected warnings."""
        critical_count = sum(1 for w in warnings if "attack pattern" in w.lower())
        medium_count = sum(
            1 for w in warnings if "suspicious" in w.lower() or "possible" in w.lower()
        )
        low_count = sum(
            1 for w in warnings if w not in ["attack pattern", "suspicious", "possible"]
        )

        score = min(
            1.0, (critical_count * 0.4) + (medium_count * 0.2) + (low_count * 0.05)
        )
        return score


# =============================================================================
# Section 3: System Prompt Hardening
# =============================================================================


