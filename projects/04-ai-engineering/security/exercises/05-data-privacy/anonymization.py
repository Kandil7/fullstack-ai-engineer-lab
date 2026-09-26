"""
05 Data Privacy: Anonymization
"""

from ._types import *


class AnonymizationEngine:
    """
    Engine for anonymizing data using multiple techniques.

    Supports:
      1. Masking (fixed replacement)
      2. Hashing (one-way, salted)
      3. Pseudonymization (reversible with key)
      4. Generalization (reduce precision)
      5. Suppression (complete removal)
      6. K-anonymity grouping
    """

    def __init__(self, salt: Optional[str] = None):
        self.salt = salt or hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        self.pseudonym_map: dict[str, str] = {}
        self.reverse_map: dict[str, str] = {}  # For reversible methods
        self._counter = 0

    def anonymize(
        self,
        text: str,
        pii_matches: list[PIIMatch],
        method: AnonymizationMethod = AnonymizationMethod.MASKING,
    ) -> tuple[str, list[AnonymizationResult]]:
        """
        Anonymize text by replacing detected PII.

        Args:
            text: Original text
            pii_matches: Detected PII instances
            method: Anonymization method to use

        Returns:
            Tuple of (anonymized_text, list_of_operations)
        """
        results = []
        # Process in reverse order to maintain positions
        sorted_matches = sorted(pii_matches, key=lambda m: m.start, reverse=True)

        anonymized = text
        for match in sorted_matches:
            anonymized_value = self._apply_method(match.value, match.pii_type, method)
            results.append(
                AnonymizationResult(
                    method=method,
                    original=match.value,
                    anonymized=anonymized_value,
                    pii_type=match.pii_type,
                    reversible=method == AnonymizationMethod.PSEUDONYMIZATION,
                )
            )
            anonymized = (
                anonymized[: match.start] + anonymized_value + anonymized[match.end :]
            )

        return anonymized, results

    def _apply_method(
        self, value: str, pii_type: PIIType, method: AnonymizationMethod
    ) -> str:
        """Apply a specific anonymization method to a value."""
        if method == AnonymizationMethod.MASKING:
            return self._mask(value, pii_type)
        elif method == AnonymizationMethod.HASHING:
            return self._hash(value)
        elif method == AnonymizationMethod.PSEUDONYMIZATION:
            return self._pseudonymize(value)
        elif method == AnonymizationMethod.GENERALIZATION:
            return self._generalize(value, pii_type)
        elif method == AnonymizationMethod.SUPPRESSION:
            return "[REDACTED]"
        elif method == AnonymizationMethod.NOISE_ADDITION:
            return self._add_noise(value, pii_type)
        else:
            return self._mask(value, pii_type)

    def _mask(self, value: str, pii_type: PIIType) -> str:
        """Apply masking to a value."""
        if pii_type == PIIType.EMAIL:
            parts = value.split("@")
            if len(parts) == 2:
                masked_name = parts[0][0] + "***"
                return f"{masked_name}@{parts[1]}"
            return "***"
        elif pii_type == PIIType.PHONE:
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 4:
                return "***-***-" + digits[-4:]
            return "***"
        elif pii_type == PIIType.SSN:
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 4:
                return "***-**-" + digits[-4:]
            return "***"
        elif pii_type == PIIType.CREDIT_CARD:
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 4:
                return "****-****-****-" + digits[-4:]
            return "***"
        elif pii_type == PIIType.NAME:
            parts = value.split()
            if len(parts) >= 2:
                return parts[0][0] + "*** " + parts[-1][0] + "***"
            return "***"
        elif pii_type == PIIType.DATE_OF_BIRTH:
            return "**/**/****"
        elif pii_type == PIIType.IP_ADDRESS:
            parts = value.split(".")
            if len(parts) == 4:
                return f"{parts[0]}.{parts[1]}.XXX.XXX"
            return "XXX.XXX.XXX.XXX"
        else:
            return (
                value[0] + "*" * max(len(value) - 2, 1) + value[-1]
                if len(value) > 1
                else "***"
            )

    def _hash(self, value: str) -> str:
        """Apply salted hash to a value."""
        salted = f"{self.salt}:{value}"
        hashed = hashlib.sha256(salted.encode()).hexdigest()[:16]
        return f"HASH:{hashed}"

    def _pseudonymize(self, value: str) -> str:
        """Replace value with a pseudonym (reversible)."""
        if value in self.pseudonym_map:
            return self.pseudonym_map[value]

        self._counter += 1
        pseudonym = f"PERSON_{self._counter:04d}"
        self.pseudonym_map[value] = pseudonym
        self.reverse_map[pseudonym] = value
        return pseudonym

    def _generalize(self, value: str, pii_type: PIIType) -> str:
        """Generalize a value to reduce precision."""
        if pii_type == PIIType.DATE_OF_BIRTH:
            # Extract year only
            year_match = re.search(r"(19|20)\d{2}", value)
            if year_match:
                return f"{year_match.group()[:3]}0s"  # e.g., "1990s"
            return "[DATE]"
        elif pii_type == PIIType.IP_ADDRESS:
            parts = value.split(".")
            if len(parts) >= 2:
                return f"{parts[0]}.{parts[1]}.0.0"
            return "0.0.0.0"
        elif pii_type == PIIType.PHONE:
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 3:
                return f"({digits[:3]}) XXX-XXXX"
            return "XXX-XXX-XXXX"
        elif pii_type == PIIType.ADDRESS:
            # Keep only city/state level
            return "[GENERALIZED ADDRESS]"
        else:
            return self._mask(value, pii_type)

    def _add_noise(self, value: str, pii_type: PIIType) -> str:
        """Add statistical noise to numeric PII."""
        if pii_type == PIIType.DATE_OF_BIRTH:
            # Add random days to date
            try:
                parts = re.split(r"[/.-]", value)
                if len(parts) == 3:
                    month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
                    noise = random.randint(-30, 30)
                    day = max(1, min(28, day + noise))
                    return f"{month:02d}/{day:02d}/{year}"
            except (ValueError, IndexError):
                pass
        elif pii_type == PIIType.IP_ADDRESS:
            parts = value.split(".")
            if len(parts) == 4:
                try:
                    noisy = [
                        str(max(0, min(255, int(p) + random.randint(-5, 5))))
                        for p in parts
                    ]
                    return ".".join(noisy)
                except ValueError:
                    pass
        return self._mask(value, pii_type)

    def deanonymize(self, pseudonym: str) -> Optional[str]:
        """Reverse pseudonymization (requires the engine instance)."""
        return self.reverse_map.get(pseudonym)


# =============================================================================
# Section 4: Differential Privacy
# =============================================================================
