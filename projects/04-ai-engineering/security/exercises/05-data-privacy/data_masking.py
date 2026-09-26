"""
05 Data Privacy: Data Masking
"""

from ._types import *


class DataMasker:
    """
    Implements various data masking strategies for different use cases.
    """

    def __init__(self):
        self.mask_characters = {
            "full": "*",
            "partial": "#",
            "space": " ",
            "asterisk": "*",
        }

    def mask_field(
        self,
        value: str,
        pii_type: PIIType,
        strategy: str = "partial",
        preserve_format: bool = True,
    ) -> str:
        """
        Mask a field value using the specified strategy.

        Args:
            value: Original value
            pii_type: Type of PII
            strategy: Masking strategy (full, partial, format_preserving)
            preserve_format: Whether to preserve the original format

        Returns:
            Masked value
        """
        if strategy == "full":
            return self._full_mask(value)
        elif strategy == "partial":
            return self._partial_mask(value, pii_type, preserve_format)
        elif strategy == "redact":
            return "[REDACTED]"
        elif strategy == "tokenize":
            return self._tokenize(value)
        else:
            return self._partial_mask(value, pii_type, preserve_format)

    def _full_mask(self, value: str) -> str:
        """Replace all characters with mask character."""
        return "*" * len(value)

    def _partial_mask(
        self, value: str, pii_type: PIIType, preserve_format: bool
    ) -> str:
        """Show partial value with masking."""
        if pii_type == PIIType.EMAIL:
            parts = value.split("@")
            if len(parts) == 2:
                name = parts[0]
                domain = parts[1]
                masked_name = name[0] + "*" * max(len(name) - 1, 1)
                return f"{masked_name}@{domain}"
            return "****"
        elif pii_type == PIIType.PHONE:
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 4:
                if preserve_format:
                    return f"(***) ***-{digits[-4:]}"
                return f"***-***-{digits[-4:]}"
            return "***"
        elif pii_type == PIIType.SSN:
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 4:
                if preserve_format:
                    return f"***-**-{digits[-4:]}"
                return f"***-**-{digits[-4:]}"
            return "***"
        elif pii_type == PIIType.CREDIT_CARD:
            digits = re.sub(r"\D", "", value)
            if len(digits) >= 4:
                if preserve_format:
                    return f"****-****-****-{digits[-4:]}"
                return f"****-****-****-{digits[-4:]}"
            return "***"
        elif pii_type == PIIType.NAME:
            parts = value.split()
            if len(parts) >= 2:
                masked = [parts[0][0] + "***" for parts in [parts]]
                masked.extend([p[0] + "***" for p in parts[1:]])
                return " ".join(masked)
            return value[0] + "***" if len(value) > 0 else "***"
        elif pii_type == PIIType.DATE_OF_BIRTH:
            return "**/**/****"
        elif pii_type == PIIType.IP_ADDRESS:
            parts = value.split(".")
            if len(parts) == 4:
                return f"{parts[0]}.{parts[1]}.*.*"
            return "*.*.*.*"
        else:
            if len(value) <= 2:
                return "*"
            return value[0] + "*" * (len(value) - 2) + value[-1]

    def _tokenize(self, value: str) -> str:
        """Create a consistent token for a value."""
        token_hash = hashlib.sha256(value.encode()).hexdigest()[:12]
        return f"TOK_{token_hash.upper()}"

    def mask_dataset(
        self,
        records: list[dict[str, Any]],
        field_configs: dict[str, dict],
    ) -> list[dict[str, Any]]:
        """
        Mask an entire dataset according to field configurations.

        Args:
            records: List of record dictionaries
            field_configs: Configuration for each field
                Format: {"field_name": {"pii_type": PIIType, "strategy": "partial"}}

        Returns:
            List of masked records
        """
        masked_records = []
        for record in records:
            masked = dict(record)
            for field_name, config in field_configs.items():
                if field_name in masked and isinstance(masked[field_name], str):
                    pii_type = config.get("pii_type", PIIType.CUSTOM)
                    strategy = config.get("strategy", "partial")
                    masked[field_name] = self.mask_field(
                        masked[field_name], pii_type, strategy
                    )
            masked_records.append(masked)
        return masked_records


# =============================================================================
# Section 6: GDPR Compliance Patterns
# =============================================================================
