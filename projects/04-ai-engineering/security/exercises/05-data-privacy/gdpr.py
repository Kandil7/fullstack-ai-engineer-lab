"""
05 Data Privacy: Gdpr
"""

from ._types import *


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

        self.processing_log.append(
            PrivacyAuditEntry(
                timestamp=time.time(),
                operation="consent_recorded",
                pii_types=[],
                data_hash=hashlib.sha256(user_id.encode()).hexdigest()[:16],
                user_id=user_id,
                details=f"Consent {'given' if consent_given else 'denied'} for: {', '.join(purposes)}",
            )
        )

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
        self.processing_log.append(
            PrivacyAuditEntry(
                timestamp=time.time(),
                operation="right_to_erasure",
                pii_types=erased_fields,
                data_hash=hashlib.sha256(user_id.encode()).hexdigest()[:16],
                user_id=user_id,
                details=f"Erased {len(erased_fields)} field(s): {', '.join(erased_fields[:5])}",
            )
        )

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
                r for r in self.consent_records.values() if r["user_id"] == user_id
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

        self.processing_log.append(
            PrivacyAuditEntry(
                timestamp=time.time(),
                operation="data_export",
                pii_types=[],
                data_hash=hashlib.sha256(user_id.encode()).hexdigest()[:16],
                user_id=user_id,
                details=f"Exported {len(user_data)} field(s)",
            )
        )

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
