"""
=============================================================================
AI Security Exercise 05: Data Privacy & Protection
=============================================================================

Topic: Data Privacy
-------------------
Data privacy is critical for AI systems that handle personal information.
This exercise covers PII detection, data anonymization, differential
privacy, data masking, and GDPR compliance patterns.

Learning Objectives:
  1. Detect PII across multiple data types (names, emails, phones, SSNs)
  2. Implement data anonymization techniques
  3. Understand differential privacy basics
  4. Design data masking strategies
  5. Build GDPR-compliant data handling patterns

Prerequisites:
  - Python 3.9+
  - re, hashlib, json, logging, dataclasses, enum, typing, math, random
  - Optional: faker (pip install faker) for test data generation

WARNING: This code is for EDUCATIONAL purposes.
=============================================================================
"""

import re
import hashlib
import json
import logging
import time
import math
import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Any
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("data_privacy")


# =============================================================================
# Section 1: Core Types
# =============================================================================

class PIIType(Enum):
    """Types of personally identifiable information."""
    NAME = auto()
    EMAIL = auto()
    PHONE = auto()
    SSN = auto()
    CREDIT_CARD = auto()
    IP_ADDRESS = auto()
    DATE_OF_BIRTH = auto()
    ADDRESS = auto()
    MEDICAL_RECORD = auto()
    BIOMETRIC = auto()
    PASSPORT = auto()
    DRIVER_LICENSE = auto()
    FINANCIAL_ACCOUNT = auto()
    CUSTOM = auto()


class AnonymizationMethod(Enum):
    """Methods for anonymizing data."""
    MASKING = auto()         # Replace with fixed characters
    HASHING = auto()         # One-way hash
    PSEUDONYMIZATION = auto() # Replace with pseudonym
    GENERALIZATION = auto()  # Reduce precision
    SUPPRESSION = auto()     # Remove entirely
    NOISE_ADDITION = auto()  # Add statistical noise
    K_ANONYMITY = auto()     # Group into k-sized equivalence classes
    L_DIVERSITY = auto()     # Ensure l distinct values per class
    T_CLOSURENESS = auto()   # Limit distribution skew


class PrivacyLevel(Enum):
    """Privacy protection levels."""
    PUBLIC = 0        # No protection needed
    INTERNAL = 1      # Basic masking
    CONFIDENTIAL = 2  # Strong anonymization
    RESTRICTED = 3    # Full suppression + audit
    TOP_SECRET = 4    # Maximum protection


@dataclass
class PIIMatch:
    """A detected PII instance in text."""
    pii_type: PIIType
    value: str
    start: int
    end: int
    confidence: float
    context: str = ""


@dataclass
class AnonymizationResult:
    """Result of an anonymization operation."""
    method: AnonymizationMethod
    original: str
    anonymized: str
    pii_type: PIIType
    reversible: bool = False
    key: Optional[str] = None  # For reversible methods


@dataclass
class PrivacyAuditEntry:
    """Audit log entry for privacy operations."""
    timestamp: float
    operation: str
    pii_types: list[str]
    data_hash: str
    user_id: Optional[str] = None
    details: str = ""


# =============================================================================
# Section 2: PII Detection Engine
# =============================================================================

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
            PIIType.SSN: re.compile(
                r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b"
            ),
            PIIType.CREDIT_CARD: re.compile(
                r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|"
                r"3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
            ),
            PIIType.IP_ADDRESS: re.compile(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
            ),
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
            PIIType.PASSPORT: re.compile(
                r"\b[A-Z]{1,2}\d{6,9}\b"
            ),
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

                matches.append(PIIMatch(
                    pii_type=pii_type,
                    value=match.group(),
                    start=match.start(),
                    end=match.end(),
                    confidence=confidence,
                    context=context,
                ))

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
                    all_matches.append(PIIMatch(
                        pii_type=PIIType.SSN,
                        value=text,
                        start=0,
                        end=len(text),
                        confidence=0.6,
                        context=f"field={key}",
                    ))
        return all_matches


# =============================================================================
# Section 3: Data Anonymization Engine
# =============================================================================

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
            results.append(AnonymizationResult(
                method=method,
                original=match.value,
                anonymized=anonymized_value,
                pii_type=match.pii_type,
                reversible=method == AnonymizationMethod.PSEUDONYMIZATION,
            ))
            anonymized = anonymized[:match.start] + anonymized_value + anonymized[match.end:]

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
            return value[0] + "*" * max(len(value) - 2, 1) + value[-1] if len(value) > 1 else "***"

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
                    noisy = [str(max(0, min(255, int(p) + random.randint(-5, 5)))) for p in parts]
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

class DifferentialPrivacy:
    """
    Implements basic differential privacy mechanisms for data protection.

    Differential privacy provides mathematical guarantees that individual
    records cannot be distinguished from aggregate statistics.
    """

    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        """
        Args:
            epsilon: Privacy budget (lower = more private, typical: 0.1-10)
            delta: Probability of privacy guarantee failure
        """
        self.epsilon = epsilon
        self.delta = delta
        self.privacy_budget_used = 0.0

    def laplace_mechanism(self, value: float, sensitivity: float = 1.0) -> float:
        """
        Add Laplace noise to a numeric value.

        Args:
            value: True value to protect
            sensitivity: Maximum change one individual can cause

        Returns:
            Noisy value
        """
        if self.privacy_budget_used >= self.epsilon:
            logger.warning("Privacy budget exhausted!")
            return value

        scale = sensitivity / self.epsilon
        noise = random.random()  # Uniform [0, 1]
        # Convert to Laplace distribution
        if noise < 0.5:
            noisy_value = value - scale * math.log(1 - 2 * noise)
        else:
            noisy_value = value + scale * math.log(2 * noise - 1)

        self.privacy_budget_used += self.epsilon / 100  # Approximate budget tracking
        return noisy_value

    def gaussian_mechanism(self, value: float, sensitivity: float = 1.0) -> float:
        """
        Add Gaussian noise for (epsilon, delta)-differential privacy.

        Args:
            value: True value to protect
            sensitivity: L2 sensitivity

        Returns:
            Noisy value
        """
        if self.privacy_budget_used >= self.epsilon:
            return value

        sigma = (sensitivity * math.sqrt(2 * math.log(1.25 / self.delta))) / self.epsilon
        noise = random.gauss(0, sigma)

        self.privacy_budget_used += self.epsilon / 100
        return value + noise

    def exponential_mechanism(
        self,
        candidates: list[Any],
        scores: list[float],
        sensitivity: float = 1.0,
    ) -> Any:
        """
        Select an item from candidates using the exponential mechanism.

        Args:
            candidates: List of possible outputs
            scores: Utility scores for each candidate (higher = more useful)
            sensitivity: Maximum change in score from one individual

        Returns:
            Selected candidate
        """
        if len(candidates) != len(scores):
            raise ValueError("candidates and scores must have same length")

        # Calculate selection probabilities
        max_score = max(scores)
        probabilities = []
        for score in scores:
            prob = math.exp((self.epsilon * score) / (2 * sensitivity))
            probabilities.append(prob)

        # Normalize
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        # Weighted random selection
        rand = random.random()
        cumulative = 0.0
        for i, prob in enumerate(probabilities):
            cumulative += prob
            if rand <= cumulative:
                return candidates[i]

        return candidates[-1]

    def randomized_response(self, true_answer: bool) -> bool:
        """
        Implement randomized response for boolean questions.

        Each respondent answers truthfully with probability p = e^epsilon / (1 + e^epsilon),
        and randomly otherwise. This provides plausible deniability.
        """
        p = math.exp(self.epsilon) / (1 + math.exp(self.epsilon))
        if random.random() < p:
            return true_answer
        else:
            return random.random() < 0.5

    def get_privacy_report(self) -> dict:
        """Get a report on privacy budget usage."""
        return {
            "epsilon": self.epsilon,
            "delta": self.delta,
            "budget_used": round(self.privacy_budget_used, 4),
            "budget_remaining": round(self.epsilon - self.privacy_budget_used, 4),
            "utilization": f"{(self.privacy_budget_used / self.epsilon * 100):.1f}%",
        }


# =============================================================================
# Section 5: Data Masking Strategies
# =============================================================================

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

class GDPRCompliance:
    """
    Implements GDPR compliance patterns for data handling.

    Covers:
      1. Consent tracking
      2. Right to erasure (forgetting)
      3. Data portability
      4. Processing records
      5. Data minimization
    """

    def __init__(self):
        self.consent_records: dict[str, dict] = {}
        self.processing_log: list[PrivacyAuditEntry] = []
        self.data_inventory: dict[str, dict] = {}

    def record_consent(
        self,
        user_id: str,
        purposes: list[str],
        consent_given: bool,
        method: str = "explicit",
    ) -> dict:
        """Record user consent for data processing."""
        consent_record = {
            "user_id": user_id,
            "purposes": purposes,
            "consent_given": consent_given,
            "method": method,
            "timestamp": time.time(),
            "version": "1.0",
        }
        self.consent_records[user_id] = consent_record

        self.processing_log.append(PrivacyAuditEntry(
            timestamp=time.time(),
            operation="consent_recorded",
            pii_types=[],
            data_hash=hashlib.sha256(user_id.encode()).hexdigest()[:16],
            user_id=user_id,
            details=f"Consent {'given' if consent_given else 'denied'} for: {', '.join(purposes)}",
        ))

        logger.info(f"Consent recorded for user {user_id[:8]}...: {consent_given}")
        return consent_record

    def check_consent(self, user_id: str, purpose: str) -> bool:
        """Check if a user has given consent for a specific purpose."""
        record = self.consent_records.get(user_id)
        if not record:
            return False
        return record["consent_given"] and purpose in record["purposes"]

    def right_to_erasure(self, user_id: str, data_store: dict[str, dict]) -> dict:
        """
        Implement the right to erasure (right to be forgotten).

        Removes all personal data for the specified user.
        """
        erased_fields = []
        if user_id in data_store:
            user_data = data_store[user_id]
            erased_fields = list(user_data.keys())
            del data_store[user_id]

        # Log the erasure
        self.processing_log.append(PrivacyAuditEntry(
            timestamp=time.time(),
            operation="right_to_erasure",
            pii_types=erased_fields,
            data_hash=hashlib.sha256(user_id.encode()).hexdigest()[:16],
            user_id=user_id,
            details=f"Erased {len(erased_fields)} field(s): {', '.join(erased_fields[:5])}",
        ))

        logger.info(f"Right to erasure executed for user {user_id[:8]}...")
        return {
            "user_id": user_id,
            "fields_erased": erased_fields,
            "timestamp": time.time(),
            "status": "completed",
        }

    def export_user_data(self, user_id: str, data_store: dict[str, dict]) -> dict:
        """
        Implement data portability (GDPR Article 20).

        Export all user data in a machine-readable format.
        """
        user_data = data_store.get(user_id, {})

        export = {
            "export_metadata": {
                "user_id": user_id,
                "exported_at": time.time(),
                "format": "JSON",
                "version": "1.0",
            },
            "personal_data": user_data,
            "consent_history": [
                r for r in self.consent_records.values()
                if r["user_id"] == user_id
            ],
            "processing_history": [
                {
                    "operation": entry.operation,
                    "timestamp": entry.timestamp,
                    "details": entry.details,
                }
                for entry in self.processing_log
                if entry.user_id == user_id
            ],
        }

        self.processing_log.append(PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_export",
            pii_types=[],
            data_hash=hashlib.sha256(user_id.encode()).hexdigest()[:16],
            user_id=user_id,
            details=f"Exported {len(user_data)} field(s)",
        ))

        return export

    def data_minimization_check(
        self, fields: list[str], purpose: str
    ) -> dict[str, bool]:
        """
        Check if collected fields are necessary for the stated purpose.

        Returns a dict indicating which fields are necessary vs unnecessary.
        """
        # Define necessary fields per purpose
        purpose_requirements = {
            "account_creation": {"name", "email", "password_hash"},
            "newsletter": {"email", "name"},
            "payment": {"name", "email", "credit_card", "address"},
            "analytics": {"ip_address", "browser_type"},
            "customer_support": {"name", "email", "issue_description"},
        }

        required = purpose_requirements.get(purpose, set())
        return {field: field in required for field in fields}

    def get_processing_report(self) -> dict:
        """Generate a GDPR compliance report."""
        operations = defaultdict(int)
        for entry in self.processing_log:
            operations[entry.operation] += 1

        return {
            "total_processing_operations": len(self.processing_log),
            "consent_records": len(self.consent_records),
            "consents_given": sum(
                1 for r in self.consent_records.values() if r["consent_given"]
            ),
            "operations_breakdown": dict(operations),
            "recent_operations": [
                {
                    "operation": entry.operation,
                    "timestamp": entry.timestamp,
                    "details": entry.details,
                }
                for entry in self.processing_log[-5:]
            ],
        }


# =============================================================================
# Section 7: Privacy-Preserving Data Collection
# =============================================================================

class PrivacyPreservingCollector:
    """
    Collects and processes data while preserving user privacy.

    Implements:
      1. Data collection with consent
      2. Automatic PII detection and handling
      3. Privacy-aware aggregation
      4. Retention policy enforcement
    """

    def __init__(
        self,
        retention_days: int = 365,
        auto_anonymize: bool = True,
    ):
        self.retention_days = retention_days
        self.auto_anonymize = auto_anonymize
        self.pii_detector = PIIDetector()
        self.anonymizer = AnonymizationEngine()
        self.data_store: dict[str, dict] = {}
        self.collection_log: list[dict] = []

    def collect(
        self,
        user_id: str,
        data: dict[str, Any],
        purpose: str,
        gdpr: GDPRCompliance,
    ) -> dict:
        """
        Collect data with privacy protections.

        Args:
            user_id: User identifier
            data: Data to collect
            purpose: Purpose of collection
            gdpr: GDPR compliance manager

        Returns:
            Collection result with privacy info
        """
        # Check consent
        if not gdpr.check_consent(user_id, purpose):
            return {
                "status": "rejected",
                "reason": "No consent for specified purpose",
                "purpose": purpose,
            }

        # Detect PII in collected data
        pii_matches = self.pii_detector.detect_in_record(data)

        # Anonymize if configured
        processed_data = dict(data)
        pii_handled = []
        if self.auto_anonymize and pii_matches:
            for key, value in processed_data.items():
                if isinstance(value, str):
                    matches = [m for m in pii_matches if f"field={key}" in m.context]
                    if matches:
                        anonymized, ops = self.anonymizer.anonymize(
                            value, matches, AnonymizationMethod.PSEUDONYMIZATION
                        )
                        processed_data[key] = anonymized
                        pii_handled.extend([op.pii_type.name for op in ops])

        # Store with metadata
        self.data_store[user_id] = {
            **processed_data,
            "_collected_at": time.time(),
            "_purpose": purpose,
            "_retention_until": time.time() + (self.retention_days * 86400),
        }

        # Log collection
        self.collection_log.append({
            "user_id": hashlib.sha256(user_id.encode()).hexdigest()[:8],
            "purpose": purpose,
            "pii_detected": len(pii_matches),
            "pii_handled": pii_handled,
            "timestamp": time.time(),
        })

        return {
            "status": "collected",
            "purpose": purpose,
            "pii_detected": len(pii_matches),
            "pii_handled": pii_handled,
            "retention_days": self.retention_days,
        }

    def enforce_retention(self) -> int:
        """Remove data that has exceeded retention period."""
        now = time.time()
        expired_keys = [
            key for key, data in self.data_store.items()
            if data.get("_retention_until", 0) < now
        ]

        for key in expired_keys:
            del self.data_store[key]

        if expired_keys:
            logger.info(f"Purged {len(expired_keys)} expired records")

        return len(expired_keys)

    def aggregate_stats(
        self, field: str, operation: str = "count"
    ) -> Optional[float]:
        """
        Aggregate data without exposing individual records.

        Args:
            field: Field to aggregate
            operation: Aggregation operation (count, sum, avg, min, max)

        Returns:
            Aggregated value or None
        """
        values = []
        for data in self.data_store.values():
            if field in data and not field.startswith("_"):
                try:
                    values.append(float(data[field]))
                except (ValueError, TypeError):
                    pass

        if not values:
            return None

        if operation == "count":
            return float(len(values))
        elif operation == "sum":
            return sum(values)
        elif operation == "avg":
            return sum(values) / len(values)
        elif operation == "min":
            return min(values)
        elif operation == "max":
            return max(values)
        return None


# =============================================================================
# Section 8: Privacy Audit Logger
# =============================================================================

class PrivacyAuditLogger:
    """
    Comprehensive audit logging for privacy operations.
    """

    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file
        self.entries: list[PrivacyAuditEntry] = []

    def log(self, entry: PrivacyAuditEntry) -> None:
        """Log a privacy audit entry."""
        self.entries.append(entry)
        logger.info(
            f"Privacy Audit: {entry.operation} | "
            f"Types: {entry.pii_types} | "
            f"User: {entry.user_id or 'N/A'}"
        )

    def query(
        self,
        operation: Optional[str] = None,
        user_id: Optional[str] = None,
        time_range: Optional[tuple[float, float]] = None,
    ) -> list[PrivacyAuditEntry]:
        """Query audit log entries."""
        results = self.entries

        if operation:
            results = [e for e in results if e.operation == operation]
        if user_id:
            results = [e for e in results if e.user_id == user_id]
        if time_range:
            start, end = time_range
            results = [e for e in results if start <= e.timestamp <= end]

        return results

    def get_summary(self) -> dict:
        """Get a summary of all audit log entries."""
        operations = defaultdict(int)
        pii_types_count = defaultdict(int)

        for entry in self.entries:
            operations[entry.operation] += 1
            for pii_type in entry.pii_types:
                pii_types_count[pii_type] += 1

        return {
            "total_entries": len(self.entries),
            "operations": dict(operations),
            "pii_types_affected": dict(pii_types_count),
            "unique_users": len(set(e.user_id for e in self.entries if e.user_id)),
        }


# =============================================================================
# Section 9: Demonstration & Testing
# =============================================================================

def demo_pii_detection():
    """Demonstrate PII detection."""
    print("\n" + "=" * 72)
    print("DEMO 1: PII Detection")
    print("=" * 72)

    detector = PIIDetector()

    test_texts = [
        "Contact John Doe at john.doe@example.com or call (555) 123-4567.",
        "Patient MRN: ABC123456, SSN: 123-45-6789, DOB: 01/15/1990.",
        "Card number: 4111111111111111, server IP: 192.168.1.100.",
        "Visit 123 Main Street, Springfield, IL 62701 for more info.",
        "This sentence has no personal information in it at all.",
    ]

    for i, text in enumerate(test_texts, 1):
        matches = detector.detect(text)
        print(f"\n  [{i}] \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        if matches:
            for m in matches:
                print(f"      {m.pii_type.name}: \"{m.value}\" (conf: {m.confidence:.0%})")
        else:
            print("      [OK] No PII detected")


def demo_anonymization():
    """Demonstrate anonymization techniques."""
    print("\n" + "=" * 72)
    print("DEMO 2: Data Anonymization")
    print("=" * 72)

    detector = PIIDetector()
    engine = AnonymizationEngine()

    text = "Email John at john@acme.com, SSN 123-45-6789, born 03/15/1985."
    matches = detector.detect(text)

    methods = [
        ("Masking", AnonymizationMethod.MASKING),
        ("Hashing", AnonymizationMethod.HASHING),
        ("Pseudonymization", AnonymizationMethod.PSEUDONYMIZATION),
        ("Generalization", AnonymizationMethod.GENERALIZATION),
        ("Suppression", AnonymizationMethod.SUPPRESSION),
    ]

    print(f"\n  Original: \"{text}\"")
    for method_name, method in methods:
        anonymized, ops = engine.anonymize(text, matches, method)
        print(f"\n  {method_name}:")
        print(f"    \"{anonymized}\"")
        if ops:
            for op in ops[:3]:
                print(f"    - {op.pii_type.name}: \"{op.original}\" -> \"{op.anonymized}\"")


def demo_differential_privacy():
    """Demonstrate differential privacy mechanisms."""
    print("\n" + "=" * 72)
    print("DEMO 3: Differential Privacy")
    print("=" * 72)

    dp = DifferentialPrivacy(epsilon=1.0)

    # Laplace mechanism
    true_value = 100.0
    print(f"\n  Laplace Mechanism (true value: {true_value}):")
    noisy_values = [dp.laplace_mechanism(true_value) for _ in range(5)]
    print(f"    Noisy values: {[f'{v:.2f}' for v in noisy_values]}")
    avg_error = sum(abs(v - true_value) for v in noisy_values) / len(noisy_values)
    print(f"    Average error: {avg_error:.2f}")

    # Gaussian mechanism
    print(f"\n  Gaussian Mechanism (true value: {true_value}):")
    gaussian_values = [dp.gaussian_mechanism(true_value) for _ in range(5)]
    print(f"    Noisy values: {[f'{v:.2f}' for v in gaussian_values]}")

    # Randomized response
    print(f"\n  Randomized Response (epsilon={dp.epsilon}):")
    true_answers = [True, True, False, True, False, True, True, True, False, True]
    reported = [dp.randomized_response(a) for a in true_answers]
    print(f"    True answers:    {true_answers}")
    print(f"    Reported answers: {reported}")
    true_rate = sum(true_answers) / len(true_answers)
    reported_rate = sum(reported) / len(reported)
    print(f"    True rate: {true_rate:.0%} | Reported rate: {reported_rate:.0%}")

    # Privacy report
    print(f"\n  Privacy Report:")
    report = dp.get_privacy_report()
    for key, value in report.items():
        print(f"    {key}: {value}")


def demo_data_masking():
    """Demonstrate data masking strategies."""
    print("\n" + "=" * 72)
    print("DEMO 4: Data Masking Strategies")
    print("=" * 72)

    masker = DataMasker()

    # Individual field masking
    test_cases = [
        ("john.doe@example.com", PIIType.EMAIL, "Partial mask"),
        ("(555) 123-4567", PIIType.PHONE, "Partial mask"),
        ("123-45-6789", PIIType.SSN, "Partial mask"),
        ("4111111111111111", PIIType.CREDIT_CARD, "Partial mask"),
        ("John Smith", PIIType.NAME, "Partial mask"),
        ("192.168.1.100", PIIType.IP_ADDRESS, "Partial mask"),
    ]

    for value, pii_type, description in test_cases:
        masked = masker.mask_field(value, pii_type, "partial")
        print(f"  {description:20s} | {pii_type.name:15s} | \"{value}\" -> \"{masked}\"")

    # Dataset masking
    print(f"\n  Dataset Masking:")
    dataset = [
        {"name": "Alice Johnson", "email": "alice@example.com", "phone": "555-0101", "age": 30},
        {"name": "Bob Smith", "email": "bob@acme.com", "phone": "555-0202", "age": 25},
        {"name": "Carol White", "email": "carol@test.org", "phone": "555-0303", "age": 35},
    ]

    field_configs = {
        "name": {"pii_type": PIIType.NAME, "strategy": "partial"},
        "email": {"pii_type": PIIType.EMAIL, "strategy": "partial"},
        "phone": {"pii_type": PIIType.PHONE, "strategy": "partial"},
    }

    masked_dataset = masker.mask_dataset(dataset, field_configs)
    for original, masked in zip(dataset, masked_dataset):
        print(f"  Original: {original}")
        print(f"  Masked:   {masked}")
        print()


def demo_gdpr_compliance():
    """Demonstrate GDPR compliance patterns."""
    print("\n" + "=" * 72)
    print("DEMO 5: GDPR Compliance")
    print("=" * 72)

    gdpr = GDPRCompliance()

    # Record consent
    print("\n  Consent Management:")
    gdpr.record_consent("user_001", ["marketing", "analytics"], True)
    gdpr.record_consent("user_002", ["marketing"], False)

    # Check consent
    print(f"  User 001 marketing consent: {gdpr.check_consent('user_001', 'marketing')}")
    print(f"  User 002 marketing consent: {gdpr.check_consent('user_002', 'marketing')}")
    print(f"  User 002 analytics consent: {gdpr.check_consent('user_002', 'analytics')}")

    # Data minimization check
    print(f"\n  Data Minimization Check (purpose: newsletter):")
    fields = ["name", "email", "phone", "ssn", "credit_card", "address"]
    minimization = gdpr.data_minimization_check(fields, "newsletter")
    for field, necessary in minimization.items():
        status = "NECESSARY" if necessary else "UNNECESSARY"
        print(f"    {field}: {status}")

    # Right to erasure
    print(f"\n  Right to Erasure:")
    data_store = {
        "user_001": {"name": "Alice", "email": "alice@example.com", "phone": "555-0101"},
        "user_002": {"name": "Bob", "email": "bob@example.com", "phone": "555-0202"},
    }
    erasure_result = gdpr.right_to_erasure("user_001", data_store)
    print(f"    Erased: {erasure_result['fields_erased']}")
    print(f"    Remaining users: {list(data_store.keys())}")

    # Processing report
    report = gdpr.get_processing_report()
    print(f"\n  Processing Report:")
    for key, value in report.items():
        if key != "recent_operations":
            print(f"    {key}: {value}")


def demo_privacy_preserving_collection():
    """Demonstrate privacy-preserving data collection."""
    print("\n" + "=" * 72)
    print("DEMO 6: Privacy-Preserving Collection")
    print("=" * 72)

    gdpr = GDPRCompliance()
    collector = PrivacyPreservingCollector(retention_days=30)

    # Record consent
    gdpr.record_consent("user_a", ["analytics", "newsletter"], True)
    gdpr.record_consent("user_b", ["analytics"], True)

    # Collect data
    print("\n  Data Collection:")
    result1 = collector.collect("user_a", {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "page_views": 42,
    }, "analytics", gdpr)
    print(f"  User A: {result1['status']} | PII handled: {result1.get('pii_handled', [])}")

    result2 = collector.collect("user_b", {
        "name": "Bob Jones",
        "email": "bob@test.com",
        "page_views": 15,
    }, "newsletter", gdpr)
    print(f"  User B: {result2['status']} | Reason: {result2.get('reason', 'N/A')}")

    # Aggregate stats (without exposing individual data)
    print(f"\n  Privacy-Preserving Aggregation:")
    total_views = collector.aggregate_stats("page_views", "sum")
    avg_views = collector.aggregate_stats("page_views", "avg")
    count = collector.aggregate_stats("page_views", "count")
    print(f"    Total page views: {total_views}")
    print(f"    Average page views: {avg_views}")
    print(f"    User count: {count}")

    # Data portability
    print(f"\n  Data Portability Export:")
    export = gdpr.export_user_data("user_a", collector.data_store)
    print(f"    Fields exported: {list(export.get('personal_data', {}).keys())}")
    print(f"    Processing history entries: {len(export.get('processing_history', []))}")


def demo_audit_logging():
    """Demonstrate privacy audit logging."""
    print("\n" + "=" * 72)
    print("DEMO 7: Privacy Audit Logging")
    print("=" * 72)

    logger_instance = PrivacyAuditLogger()

    # Simulate various operations
    operations = [
        PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_collection",
            pii_types=["EMAIL", "NAME"],
            data_hash="abc123",
            user_id="user_001",
            details="Collected email and name for newsletter",
        ),
        PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_anonymization",
            pii_types=["SSN", "CREDIT_CARD"],
            data_hash="def456",
            user_id="user_002",
            details="Anonymized SSN and credit card for analytics",
        ),
        PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_export",
            pii_types=[],
            data_hash="ghi789",
            user_id="user_001",
            details="GDPR data portability export",
        ),
        PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_deletion",
            pii_types=["EMAIL", "PHONE", "ADDRESS"],
            data_hash="jkl012",
            user_id="user_003",
            details="Right to erasure executed",
        ),
    ]

    for entry in operations:
        logger_instance.log(entry)

    # Query audit log
    print("\n  Audit Log Entries:")
    all_entries = logger_instance.query()
    for entry in all_entries:
        print(f"    [{entry.operation}] User: {entry.user_id or 'N/A'} | Types: {entry.pii_types}")

    # Query by operation
    deletion_entries = logger_instance.query(operation="data_deletion")
    print(f"\n  Deletion operations: {len(deletion_entries)}")

    # Summary
    summary = logger_instance.get_summary()
    print(f"\n  Audit Summary:")
    for key, value in summary.items():
        print(f"    {key}: {value}")


# =============================================================================
# Section 10: Best Practices
# =============================================================================

BEST_PRACTICES = {
    "Data Collection": [
        "Collect only data that is strictly necessary (data minimization)",
        "Obtain explicit consent before collecting personal data",
        "Clearly communicate the purpose of data collection",
        "Provide easy mechanisms for users to withdraw consent",
        "Log all data collection operations for audit purposes",
    ],
    "Data Storage": [
        "Encrypt personal data at rest and in transit",
        "Implement access controls based on role and need-to-know",
        "Set retention policies and automatically purge expired data",
        "Use pseudonymization where possible to reduce risk",
        "Maintain separate storage for PII and non-PII data",
    ],
    "Data Processing": [
        "Process data only for stated purposes (purpose limitation)",
        "Apply differential privacy for aggregate statistics",
        "Use anonymization techniques for non-essential processing",
        "Implement privacy-preserving machine learning techniques",
        "Audit all data processing operations",
    ],
    "Data Sharing": [
        "Never share raw personal data without explicit consent",
        "Use anonymization before sharing data with third parties",
        "Implement data processing agreements with partners",
        "Provide data portability in machine-readable formats",
        "Track all data sharing operations for compliance",
    ],
    "Compliance": [
        "Implement right to erasure (forgetting) mechanisms",
        "Maintain records of processing activities (GDPR Article 30)",
        "Conduct data protection impact assessments for high-risk processing",
        "Appoint a data protection officer if required",
        "Regularly audit privacy practices and update policies",
    ],
}


def print_best_practices():
    """Print the best practices reference."""
    print("\n" + "=" * 72)
    print("DATA PRIVACY BEST PRACTICES")
    print("=" * 72)

    for category, practices in BEST_PRACTICES.items():
        print(f"\n  {category}:")
        for i, practice in enumerate(practices, 1):
            print(f"    {i}. {practice}")


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    print("AI Security Exercise 05: Data Privacy & Protection")
    print("=" * 72)

    demo_pii_detection()
    demo_anonymization()
    demo_differential_privacy()
    demo_data_masking()
    demo_gdpr_compliance()
    demo_privacy_preserving_collection()
    demo_audit_logging()
    print_best_practices()

    print("\n" + "=" * 72)
    print("Exercise complete. Review the code for implementation details.")
    print("=" * 72)
