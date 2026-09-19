"""
04 Output Filtering: Pii Filter
"""

from ._types import *

class PIIFilter:
    """
    Detects and masks Personally Identifiable Information (PII) in
    AI-generated outputs.
    """

    PII_PATTERNS = {
        "email": {
            "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "mask_fn": lambda m: m[:2] + "***@" + m.split("@")[1],
            "severity": SeverityLevel.MEDIUM,
        },
        "phone_us": {
            "pattern": r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",
            "mask_fn": lambda m: "***-***-" + m[-4:],
            "severity": SeverityLevel.MEDIUM,
        },
        "ssn": {
            "pattern": r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b",
            "mask_fn": lambda m: "***-**-" + m[-4:],
            "severity": SeverityLevel.HIGH,
        },
        "credit_card": {
            "pattern": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b",
            "mask_fn": lambda m: "****-****-****-" + m[-4:],
            "severity": SeverityLevel.HIGH,
        },
        "ip_address": {
            "pattern": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            "mask_fn": lambda m: m[: m.rfind(".")] + ".XXX",
            "severity": SeverityLevel.LOW,
        },
        "date_of_birth": {
            "pattern": r"\b(?:0[1-9]|1[0-2])[/.-](?:0[1-9]|[12]\d|3[01])[/.-](?:19|20)\d{2}\b",
            "mask_fn": lambda m: "**/**/****",
            "severity": SeverityLevel.HIGH,
        },
        "address_us": {
            "pattern": r"\d{1,5}\s+(?:[A-Z][a-zA-Z]*\s+){1,3}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln)\b",
            "mask_fn": lambda m: "[ADDRESS REDACTED]",
            "severity": SeverityLevel.MEDIUM,
        },
        "name_pattern": {
            "pattern": r"(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+",
            "mask_fn": lambda m: m.split(".")[0] + ". [NAME REDACTED]",
            "severity": SeverityLevel.MEDIUM,
        },
    }

    def __init__(self, mask: bool = True, custom_patterns: Optional[dict] = None):
        self.mask = mask
        self.custom_patterns = custom_patterns or {}
        self.all_patterns = {**self.PII_PATTERNS, **self.custom_patterns}
        self.compiled = {
            name: re.compile(info["pattern"])
            for name, info in self.all_patterns.items()
        }

    def detect(self, text: str) -> list[FilterResult]:
        """Detect PII in text."""
        results = []
        for pii_type, pattern_info in self.all_patterns.items():
            compiled = self.compiled[pii_type]
            matches = compiled.findall(text)

            if matches:
                masked_items = []
                for match in matches:
                    if self.mask and "mask_fn" in pattern_info:
                        masked_items.append(pattern_info["mask_fn"](match))
                    else:
                        masked_items.append(match)

                results.append(
                    FilterResult(
                        category=FilterCategory.PII,
                        passed=False,
                        severity=pattern_info["severity"],
                        confidence=0.9,
                        details=f"Detected {len(matches)} {pii_type} instance(s)",
                        flagged_items=masked_items[:5],
                        recommendations=[
                            f"Mask or redact {pii_type} data before display"
                        ],
                    )
                )

        return results

    def filter_text(self, text: str) -> tuple[str, list[FilterResult]]:
        """Detect and mask PII in text, returning filtered text and results."""
        results = self.detect(text)
        filtered = text

        if self.mask:
            for pii_type, pattern_info in self.all_patterns.items():
                compiled = self.compiled[pii_type]
                matches = compiled.findall(filtered)
                for match in matches:
                    if "mask_fn" in pattern_info:
                        masked = pattern_info["mask_fn"](match)
                        filtered = filtered.replace(match, masked, 1)

        return filtered, results


# =============================================================================
# Section 3: Toxicity Detection
# =============================================================================


