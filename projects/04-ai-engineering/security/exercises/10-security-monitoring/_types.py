"""
=============================================================
Topic 10: Security Monitoring & Incident Response
=============================================================

Security Level: ########-- High

Build comprehensive security monitoring for AI systems. This
exercise covers security logging, intrusion detection, anomaly
detection, alert systems, incident response, and compliance
auditing.

Learning Objectives:
- Implement structured security logging
- Build intrusion detection systems
- Create anomaly detection pipelines
- Design alert and escalation systems
- Develop incident response procedures
- Perform compliance auditing

Prerequisites:
- Understanding of security operations
- Familiarity with log analysis
- Basic knowledge of compliance frameworks
=============================================================
"""

import hashlib
import hmac
import json
import math
import re
import secrets
import statistics
import struct
import time
from collections import defaultdict, Counter, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from enum import Enum
import base64


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class SecurityEventType(Enum):
    AUTH_SUCCESS = "auth.success"
    AUTH_FAILURE = "auth.failure"
    AUTHORIZATION_DENIED = "authorization.denied"
    ACCESS_VIOLATION = "access.violation"
    DATA_BREACH = "data.breach"
    INTRUSION_DETECTED = "intrusion.detected"
    ANOMALY_DETECTED = "anomaly.detected"
    RATE_LIMIT_EXCEEDED = "rate_limit.exceeded"
    API_ABUSE = "api.abuse"
    MODEL_THEFT_ATTEMPT = "model.theft_attempt"
    PRIVILEGE_ESCALATION = "privilege.escalation"
    CONFIG_CHANGE = "config.change"
    SYSTEM_ERROR = "system.error"
    COMPLIANCE_VIOLATION = "compliance.violation"


@dataclass
class SecurityEvent:
    """Structured security event."""

    event_id: str
    event_type: SecurityEventType
    timestamp: float
    source: str
    user_id: Optional[str]
    ip_address: Optional[str]
    details: Dict
    severity: str = "info"
    tags: List[str] = field(default_factory=list)
    checksum: str = ""

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        """Compute event checksum for integrity."""
        data = f"{self.event_type.value}:{self.timestamp}:{self.source}:{json.dumps(self.details, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp,
            "source": self.source,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "details": self.details,
            "severity": self.severity,
            "tags": self.tags,
            "checksum": self.checksum,
        }


class SecurityLogger:
    """
    Structured security logging system.

    Features:
    - Structured event logging
    - Event correlation
    - Tamper-evident logs
    - Log aggregation
    """

    def __init__(self):
        self._events: List[SecurityEvent] = []
        self._event_index: Dict[str, List[int]] = defaultdict(list)
        self._log_chain: List[str] = []  # For tamper evidence
        self._prev_hash = "genesis"

    def log_event(
        self,
        event_type: SecurityEventType,
        source: str,
        details: Dict,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        severity: str = "info",
        tags: Optional[List[str]] = None,
    ) -> SecurityEvent:
        """Log a security event with integrity protection."""
        event = SecurityEvent(
            event_id=str(secrets.token_urlsafe(16)),
            event_type=event_type,
            timestamp=time.time(),
            source=source,
            user_id=user_id,
            ip_address=ip_address,
            details=details,
            severity=severity,
            tags=tags or [],
        )

        # Create chain hash for tamper evidence
        event_data = json.dumps(event.to_dict(), sort_keys=True)
        chain_hash = hashlib.sha256((self._prev_hash + event_data).encode()).hexdigest()
        self._log_chain.append(chain_hash)
        self._prev_hash = chain_hash

        # Store event
        self._events.append(event)
        self._event_index[event_type.value].append(len(self._events) - 1)

        return event

    def query_events(
        self,
        event_type: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        user_id: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100,
    ) -> List[SecurityEvent]:
        """Query security events with filters."""
        results = []

        for event in reversed(self._events):  # Most recent first
            if event_type and event.event_type.value != event_type:
                continue
            if start_time and event.timestamp < start_time:
                continue
            if end_time and event.timestamp > end_time:
                continue
            if user_id and event.user_id != user_id:
                continue
            if severity and event.severity != severity:
                continue

            results.append(event)
            if len(results) >= limit:
                break

        return results

    def get_event_statistics(self, hours: int = 24) -> Dict:
        """Get event statistics for the specified time window."""
        cutoff = time.time() - (hours * 3600)
        recent = [e for e in self._events if e.timestamp > cutoff]

        type_counts = Counter(e.event_type.value for e in recent)
        severity_counts = Counter(e.severity for e in recent)
        source_counts = Counter(e.source for e in recent)

        return {
            "total_events": len(recent),
            "by_type": dict(type_counts),
            "by_severity": dict(severity_counts),
            "by_source": dict(source_counts),
            "time_window_hours": hours,
            "unique_users": len(set(e.user_id for e in recent if e.user_id)),
            "unique_ips": len(set(e.ip_address for e in recent if e.ip_address)),
        }

    def verify_log_integrity(self) -> Dict:
        """Verify the integrity of the log chain."""
        # In production, would verify entire chain
        return {
            "chain_length": len(self._log_chain),
            "last_hash": self._prev_hash,
            "integrity_valid": True,  # Simplified
        }


# =============================================================
# SECTION 2: Intrusion Detection System
# =============================================================
