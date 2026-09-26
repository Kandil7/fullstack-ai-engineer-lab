"""
05 Data Privacy: Audit Logger
"""

from ._types import *


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
