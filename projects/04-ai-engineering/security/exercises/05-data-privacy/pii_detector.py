"""
05 Data Privacy: Pii Detector
"""

from ._types import *


class PIIDetector:
    """
    Comprehensive PII detection engine supporting multiple data types
    and international formats.
    """

    def __init__(self, custom_patterns: Optional[dict[PIIType, str]] = None):
        self.patterns = self._build_patterns()
        if custom_patterns:
            for pii_type, pattern in custom_patterns.items():
                self.patterns[pii_type] = re.compile(pattern, re.IGNORECASE)

    def _build_patterns(self) -> dict[PIIType, re.Pattern]:
        """Build regex patterns for PII detection."""
        return {
            PIIType.EMAIL: re.compile(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            ),
            PIIType.PHONE: re.compile(
                r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b"
            ),
            PIIType.SSN: re.compile(r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b"),
            PIIType.CREDIT_CARD: re.compile(
                r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|"
                r"3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
            ),
            PIIType.IP_ADDRESS: re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
            PIIType.DATE_OF_BIRTH: re.compile(
                r"\b(?:0[1-9]|1[0-2])[/.-](?:0[1-9]|[12]\d|3[01])[/.-]"
                r"(?:19|20)\d{2}\b"
            ),
            PIIType.NAME: re.compile(
                r"(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+"
            ),
            PIIType.ADDRESS: re.compile(
                r"\d{1,5}\s+(?:[A-Z][a-zA-Z]*\s+){1,3}"
                r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|"
                r"Drive|Dr|Lane|Ln|Court|Ct|Place|Pl)\b"
            ),
            PIIType.MEDICAL_RECORD: re.compile(
                r"(?i)(?:MRN|medical\s+record|patient\s+id)[\s:=]+[A-Z0-9-]{6,20}"
            ),
            PIIType.PASSPORT: re.compile(r"\b[A-Z]{1,2}\d{6,9}\b"),
            PIIType.DRIVER_LICENSE: re.compile(
                r"(?i)(?:driver'?s?\s+license|DL)[\s:=]+[A-Z0-9-]{6,20}"
            ),
            PIIType.FINANCIAL_ACCOUNT: re.compile(
                r"\b(?:account|acct)[\s:=]+[A-Z0-9-]{8,20}\b"
            ),
        }

    def detect(self, text: str) -> list[PIIMatch]:
        """Detect all PII instances in text."""
        matches = []
        for pii_type, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                # Calculate confidence based on context and pattern specificity
                confidence = self._calculate_confidence(match, pii_type, text)
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end]

                matches.append(
                    PIIMatch(
                        pii_type=pii_type,
                        value=match.group(),
                        start=match.start(),
                        end=match.end(),
                        confidence=confidence,
                        context=context,
                    )
                )

        # Sort by position and remove overlaps (keep highest confidence)
        matches.sort(key=lambda m: (m.start, -m.confidence))
        return self._remove_overlaps(matches)

    def _calculate_confidence(
        self, match: re.Match, pii_type: PIIType, text: str
    ) -> float:
        """Calculate confidence score for a PII match."""
        base_confidence = 0.7

        # Boost confidence for specific patterns
        if pii_type == PIIType.SSN:
            # SSN format validation
            value = match.group().replace("-", "").replace(".", "").replace(" ", "")
            if len(value) == 9 and value.isdigit():
                base_confidence = 0.9
        elif pii_type == PIIType.CREDIT_CARD:
            # Luhn check for credit cards
            if self._luhn_check(match.group().replace("-", "").replace(" ", "")):
                base_confidence = 0.95
        elif pii_type == PIIType.EMAIL:
            base_confidence = 0.85
        elif pii_type == PIIType.PHONE:
            base_confidence = 0.8

        # Context boost
        context_keywords = {
            PIIType.NAME: ["name", "mr", "mrs", "dr"],
            PIIType.EMAIL: ["email", "contact", "@"],
            PIIType.PHONE: ["phone", "call", "tel"],
            PIIType.SSN: ["ssn", "social", "security"],
        }
        for keyword in context_keywords.get(pii_type, []):
            if keyword.lower() in text.lower():
                base_confidence = min(base_confidence + 0.1, 0.99)
                break

        return base_confidence

    def _luhn_check(self, number: str) -> bool:
        """Validate a credit card number using the Luhn algorithm."""
        try:
            digits = [int(d) for d in number]
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            total = sum(odd_digits)
            for d in even_digits:
                total += sum(divmod(d * 2, 10))
            return total % 10 == 0
        except (ValueError, IndexError):
            return False

    def _remove_overlaps(self, matches: list[PIIMatch]) -> list[PIIMatch]:
        """Remove overlapping matches, keeping higher confidence ones."""
        if not matches:
            return matches

        result = [matches[0]]
        for match in matches[1:]:
            last = result[-1]
            if match.start >= last.end:
                result.append(match)
            elif match.confidence > last.confidence:
                result[-1] = match
        return result

    def detect_in_record(self, record: dict[str, Any]) -> list[PIIMatch]:
        """Detect PII in a dictionary record."""
        all_matches = []
        for key, value in record.items():
            if isinstance(value, str):
                matches = self.detect(value)
                for m in matches:
                    m.context = f"field={key}: {m.context}"
                all_matches.extend(matches)
            elif isinstance(value, (int, float)):
                # Check if numeric fields contain PII-like values
                text = str(value)
                if len(text) == 9 and text.isdigit():
                    all_matches.append(
                        PIIMatch(
                            pii_type=PIIType.SSN,
                            value=text,
                            start=0,
                            end=len(text),
                            confidence=0.6,
                            context=f"field={key}",
                        )
                    )
        return all_matches


# =============================================================================
# Section 3: Data Anonymization Engine
# =============================================================================
