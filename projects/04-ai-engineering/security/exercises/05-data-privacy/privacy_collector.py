"""
05 Data Privacy: Privacy Collector
"""

from ._types import *
from .anonymization import AnonymizationEngine
from .gdpr import GDPRCompliance
from .pii_detector import PIIDetector


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
        self.collection_log.append(
            {
                "user_id": hashlib.sha256(user_id.encode()).hexdigest()[:8],
                "purpose": purpose,
                "pii_detected": len(pii_matches),
                "pii_handled": pii_handled,
                "timestamp": time.time(),
            }
        )

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
            key
            for key, data in self.data_store.items()
            if data.get("_retention_until", 0) < now
        ]

        for key in expired_keys:
            del self.data_store[key]

        if expired_keys:
            logger.info(f"Purged {len(expired_keys)} expired records")

        return len(expired_keys)

    def aggregate_stats(self, field: str, operation: str = "count") -> Optional[float]:
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
