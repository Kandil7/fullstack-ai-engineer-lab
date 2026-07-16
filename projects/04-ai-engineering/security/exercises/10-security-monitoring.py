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


# =============================================================
# SECTION 1: Security Logging
# =============================================================

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
        chain_hash = hashlib.sha256(
            (self._prev_hash + event_data).encode()
        ).hexdigest()
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

class IntrusionDetectionSystem:
    """
    Rule-based intrusion detection for AI systems.

    Detects:
    - Brute force attacks
    - Port scanning
    - Data exfiltration
    - Unauthorized access attempts
    - Anomalous API usage
    """

    def __init__(self):
        self._rules: List[Dict] = []
        self._alerts: List[Dict] = []
        self._blocked_ips: Set[str] = set()
        self._ip_activity: Dict[str, List[Dict]] = defaultdict(list)
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Setup default detection rules."""
        self.add_rule({
            "name": "brute_force_detection",
            "description": "Detect brute force login attempts",
            "condition": lambda events: self._check_brute_force(events),
            "severity": "high",
            "action": "block_ip",
        })

        self.add_rule({
            "name": "port_scan_detection",
            "description": "Detect port scanning activity",
            "condition": lambda events: self._check_port_scan(events),
            "severity": "medium",
            "action": "alert",
        })

        self.add_rule({
            "name": "data_exfiltration",
            "description": "Detect potential data exfiltration",
            "condition": lambda events: self._check_exfiltration(events),
            "severity": "critical",
            "action": "block_and_alert",
        })

        self.add_rule({
            "name": "api_abuse",
            "description": "Detect API abuse patterns",
            "condition": lambda events: self._check_api_abuse(events),
            "severity": "high",
            "action": "rate_limit",
        })

    def add_rule(self, rule: Dict):
        """Add a detection rule."""
        self._rules.append(rule)

    def analyze_event(self, event: Dict) -> List[Dict]:
        """
        Analyze an event against all detection rules.

        Returns list of triggered alerts.
        """
        ip = event.get("ip_address")
        if ip:
            self._ip_activity[ip].append(event)
            # Keep bounded
            if len(self._ip_activity[ip]) > 1000:
                self._ip_activity[ip] = self._ip_activity[ip][-500:]

        triggered_alerts = []

        for rule in self._rules:
            try:
                # Get recent events for this IP
                recent_events = self._ip_activity.get(ip, [])[-100:]

                if rule["condition"](recent_events):
                    alert = {
                        "alert_id": str(secrets.token_urlsafe(16)),
                        "rule": rule["name"],
                        "description": rule["description"],
                        "severity": rule["severity"],
                        "action": rule["action"],
                        "timestamp": time.time(),
                        "triggering_event": event,
                        "ip_address": ip,
                    }
                    triggered_alerts.append(alert)
                    self._alerts.append(alert)

                    # Execute action
                    if rule["action"] == "block_ip" and ip:
                        self._blocked_ips.add(ip)
            except Exception as e:
                continue

        return triggered_alerts

    def _check_brute_force(self, events: List[Dict]) -> bool:
        """Check for brute force login pattern."""
        auth_failures = [
            e for e in events
            if e.get("event_type") == "auth.failure"
            and time.time() - e.get("timestamp", 0) < 300  # Last 5 minutes
        ]
        return len(auth_failures) >= 5

    def _check_port_scan(self, events: List[Dict]) -> bool:
        """Check for port scanning pattern."""
        unique_ports = set()
        for e in events:
            if e.get("event_type") == "connection":
                port = e.get("details", {}).get("port")
                if port:
                    unique_ports.add(port)
        return len(unique_ports) > 10

    def _check_exfiltration(self, events: List[Dict]) -> bool:
        """Check for data exfiltration pattern."""
        large_downloads = [
            e for e in events
            if e.get("event_type") == "data.download"
            and e.get("details", {}).get("size_bytes", 0) > 10 * 1024 * 1024  # 10MB
        ]
        return len(large_downloads) >= 3

    def _check_api_abuse(self, events: List[Dict]) -> bool:
        """Check for API abuse pattern."""
        api_calls = [
            e for e in events
            if e.get("event_type") == "api.call"
            and time.time() - e.get("timestamp", 0) < 60  # Last minute
        ]
        return len(api_calls) > 100

    def get_blocked_ips(self) -> Set[str]:
        """Get list of blocked IPs."""
        return self._blocked_ips.copy()

    def get_alerts(self, severity: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get alerts, optionally filtered by severity."""
        alerts = self._alerts
        if severity:
            alerts = [a for a in alerts if a["severity"] == severity]
        return alerts[-limit:]


# =============================================================
# SECTION 3: Anomaly Detection
# =============================================================

class AnomalyDetector:
    """
    Statistical anomaly detection for security monitoring.

    Techniques:
    - Z-score based detection
    - Moving average detection
    - Isolation Forest (simplified)
    - Time series analysis
    """

    def __init__(self, sensitivity: float = 2.0):
        """
        Args:
            sensitivity: Number of standard deviations for anomaly threshold
        """
        self.sensitivity = sensitivity
        self._baselines: Dict[str, Dict] = {}
        self._time_series: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self._anomalies: List[Dict] = []

    def update_baseline(self, metric_name: str, value: float):
        """Update baseline statistics for a metric."""
        if metric_name not in self._baselines:
            self._baselines[metric_name] = {
                "values": deque(maxlen=10000),
                "mean": 0,
                "std": 1,
                "count": 0,
            }

        baseline = self._baselines[metric_name]
        baseline["values"].append(value)
        baseline["count"] += 1

        # Update running statistics
        values = list(baseline["values"])
        baseline["mean"] = statistics.mean(values)
        baseline["std"] = statistics.stdev(values) if len(values) > 1 else 1

    def detect_anomaly(self, metric_name: str, value: float) -> Dict:
        """Check if a value is anomalous."""
        if metric_name not in self._baselines:
            return {"is_anomaly": False, "reason": "No baseline established"}

        baseline = self._baselines[metric_name]

        if baseline["count"] < 30:
            return {"is_anomaly": False, "reason": "Insufficient baseline data"}

        # Z-score
        z_score = (value - baseline["mean"]) / max(baseline["std"], 1e-10)
        is_anomaly = abs(z_score) > self.sensitivity

        # Moving average check
        values = list(baseline["values"])
        if len(values) >= 10:
            recent_mean = statistics.mean(values[-10:])
            recent_std = statistics.stdev(values[-10:]) if len(values) > 10 else 1
            recent_z = (value - recent_mean) / max(recent_std, 1e-10)
        else:
            recent_z = z_score

        result = {
            "is_anomaly": is_anomaly,
            "metric": metric_name,
            "value": value,
            "baseline_mean": round(baseline["mean"], 4),
            "baseline_std": round(baseline["std"], 4),
            "z_score": round(z_score, 4),
            "recent_z_score": round(recent_z, 4),
            "sensitivity": self.sensitivity,
        }

        if is_anomaly:
            self._anomalies.append({
                **result,
                "timestamp": time.time(),
            })

        return result

    def detect_time_series_anomaly(self, series_name: str, value: float) -> Dict:
        """Detect anomalies in time series data."""
        self._time_series[series_name].append((time.time(), value))
        series = list(self._time_series[series_name])

        if len(series) < 20:
            return {"is_anomaly": False, "reason": "Insufficient data points"}

        # Extract values
        values = [v for _, v in series[-100:]]

        # Compute seasonal component (simplified)
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 1

        # Check for sudden changes
        if len(values) >= 10:
            recent = values[-5:]
            historical = values[:-5]
            recent_mean = statistics.mean(recent)
            historical_mean = statistics.mean(historical)

            change_ratio = abs(recent_mean - historical_mean) / max(abs(historical_mean), 1e-10)

            if change_ratio > 0.5:  # 50% change
                return {
                    "is_anomaly": True,
                    "type": "sudden_change",
                    "change_ratio": round(change_ratio, 4),
                    "recent_mean": round(recent_mean, 4),
                    "historical_mean": round(historical_mean, 4),
                }

        # Z-score check
        z_score = (value - mean) / max(std, 1e-10)
        if abs(z_score) > self.sensitivity:
            return {
                "is_anomaly": True,
                "type": "statistical_outlier",
                "z_score": round(z_score, 4),
            }

        return {"is_anomaly": False}

    def get_anomalies(self, hours: int = 24) -> List[Dict]:
        """Get detected anomalies."""
        cutoff = time.time() - (hours * 3600)
        return [a for a in self._anomalies if a.get("timestamp", 0) > cutoff]

    def get_baseline_summary(self) -> Dict:
        """Get summary of all baselines."""
        return {
            metric: {
                "mean": round(b["mean"], 4),
                "std": round(b["std"], 4),
                "count": b["count"],
            }
            for metric, b in self._baselines.items()
        }


# =============================================================
# SECTION 4: Alert System
# =============================================================

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


@dataclass
class Alert:
    """Security alert."""
    alert_id: str
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    created_at: float
    source: str
    affected_assets: List[str]
    assigned_to: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    escalated: bool = False


class AlertManager:
    """
    Alert management system with escalation and notification.

    Features:
    - Alert creation and tracking
    - Escalation policies
    - Notification routing
    - Alert correlation
    - Deduplication
    """

    def __init__(self):
        self._alerts: Dict[str, Alert] = {}
        self._escalation_policies: Dict[str, Dict] = {}
        self._notification_channels: List[Dict] = []
        self._alert_rules: List[Dict] = []
        self._dedup_window: Dict[str, float] = {}

    def create_alert(
        self,
        title: str,
        description: str,
        severity: AlertSeverity,
        source: str,
        affected_assets: List[str],
        metadata: Optional[Dict] = None,
    ) -> Alert:
        """Create a new security alert."""
        # Deduplication check
        dedup_key = f"{title}:{source}"
        if dedup_key in self._dedup_window:
            if time.time() - self._dedup_window[dedup_key] < 300:  # 5 min window
                return None  # Duplicate

        self._dedup_window[dedup_key] = time.time()

        alert = Alert(
            alert_id=str(secrets.token_urlsafe(16)),
            title=title,
            description=description,
            severity=severity,
            status=AlertStatus.OPEN,
            created_at=time.time(),
            source=source,
            affected_assets=affected_assets,
            metadata=metadata or {},
        )

        self._alerts[alert.alert_id] = alert

        # Check escalation
        self._check_escalation(alert)

        # Send notifications
        self._send_notifications(alert)

        return alert

    def update_alert(
        self,
        alert_id: str,
        status: Optional[AlertStatus] = None,
        assigned_to: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> Optional[Alert]:
        """Update an alert."""
        alert = self._alerts.get(alert_id)
        if not alert:
            return None

        if status:
            alert.status = status
        if assigned_to:
            alert.assigned_to = assigned_to
        if metadata:
            alert.metadata.update(metadata)

        return alert

    def add_escalation_policy(self, name: str, policy: Dict):
        """Add an escalation policy."""
        self._escalation_policies[name] = policy

    def add_notification_channel(self, channel: Dict):
        """Add a notification channel."""
        self._notification_channels.append(channel)

    def _check_escalation(self, alert: Alert):
        """Check if alert needs escalation."""
        # Auto-escalate critical alerts
        if alert.severity == AlertSeverity.CRITICAL:
            alert.escalated = True

        # Check time-based escalation
        open_alerts = [
            a for a in self._alerts.values()
            if a.status == AlertStatus.OPEN
            and a.severity in (AlertSeverity.HIGH, AlertSeverity.CRITICAL)
        ]

        for a in open_alerts:
            age_minutes = (time.time() - a.created_at) / 60
            if age_minutes > 30 and not a.escalated:
                a.escalated = True

    def _send_notifications(self, alert: Alert):
        """Send notifications for an alert."""
        # In production, would send to Slack, PagerDuty, email, etc.
        pass

    def get_open_alerts(self, severity: Optional[AlertSeverity] = None) -> List[Alert]:
        """Get all open alerts."""
        alerts = [a for a in self._alerts.values() if a.status == AlertStatus.OPEN]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return sorted(alerts, key=lambda a: a.created_at, reverse=True)

    def get_alert_statistics(self, hours: int = 24) -> Dict:
        """Get alert statistics."""
        cutoff = time.time() - (hours * 3600)
        recent = [a for a in self._alerts.values() if a.created_at > cutoff]

        return {
            "total_alerts": len(recent),
            "by_severity": dict(Counter(a.severity.value for a in recent)),
            "by_status": dict(Counter(a.status.value for a in recent)),
            "escalated": sum(1 for a in recent if a.escalated),
            "mean_time_to_acknowledge": self._calculate_mtta(recent),
        }

    def _calculate_mtta(self, alerts: List[Alert]) -> Optional[float]:
        """Calculate mean time to acknowledge."""
        ack_times = []
        for alert in alerts:
            if alert.status != AlertStatus.OPEN:
                # Would track actual ack time in production
                ack_times.append(300)  # Placeholder: 5 minutes
        return statistics.mean(ack_times) if ack_times else None


# =============================================================
# SECTION 5: Incident Response
# =============================================================

class IncidentPhase(Enum):
    PREPARATION = "preparation"
    DETECTION = "detection"
    CONTAINMENT = "containment"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    LESSONS_LEARNED = "lessons_learned"


@dataclass
class Incident:
    """Security incident."""
    incident_id: str
    title: str
    description: str
    severity: str
    phase: IncidentPhase
    created_at: float
    status: str
    affected_systems: List[str]
    timeline: List[Dict] = field(default_factory=list)
    assigned_team: Optional[str] = None
    resolution: Optional[str] = None


class IncidentResponseManager:
    """
    Incident response management system.

    Features:
    - Incident lifecycle management
    - Playbook execution
    - Timeline tracking
    - Communication management
    - Post-incident review
    """

    def __init__(self):
        self._incidents: Dict[str, Incident] = {}
        self._playbooks: Dict[str, Dict] = {}
        self._communication_log: List[Dict] = []
        self._setup_default_playbooks()

    def _setup_default_playbooks(self):
        """Setup default incident response playbooks."""
        self._playbooks["data_breach"] = {
            "name": "Data Breach Response",
            "phases": [
                {"phase": "detection", "steps": [
                    "Verify the breach",
                    "Identify affected data",
                    "Assess scope and impact",
                ]},
                {"phase": "containment", "steps": [
                    "Isolate affected systems",
                    "Preserve evidence",
                    "Block attacker access",
                ]},
                {"phase": "eradication", "steps": [
                    "Remove attacker presence",
                    "Patch vulnerabilities",
                    "Reset compromised credentials",
                ]},
                {"phase": "recovery", "steps": [
                    "Restore from clean backups",
                    "Verify system integrity",
                    "Monitor for reinfection",
                ]},
                {"phase": "lessons_learned", "steps": [
                    "Document findings",
                    "Update procedures",
                    "Conduct post-mortem",
                ]},
            ],
        }

        self._playbooks["model_theft"] = {
            "name": "Model Theft Response",
            "phases": [
                {"phase": "detection", "steps": [
                    "Verify unauthorized model access",
                    "Identify exfiltration method",
                    "Assess model sensitivity",
                ]},
                {"phase": "containment", "steps": [
                    "Revoke compromised credentials",
                    "Block extraction endpoints",
                    "Enable enhanced logging",
                ]},
                {"phase": "eradication", "steps": [
                    "Rotate all API keys",
                    "Update access controls",
                    "Patch extraction vectors",
                ]},
                {"phase": "recovery", "steps": [
                    "Redeploy with new credentials",
                    "Verify model integrity",
                    "Implement additional protections",
                ]},
            ],
        }

    def declare_incident(
        self,
        title: str,
        description: str,
        severity: str,
        affected_systems: List[str],
        playbook: Optional[str] = None,
    ) -> Incident:
        """Declare a new incident."""
        incident = Incident(
            incident_id=str(secrets.token_urlsafe(8)),
            title=title,
            description=description,
            severity=severity,
            phase=IncidentPhase.DETECTION,
            created_at=time.time(),
            status="open",
            affected_systems=affected_systems,
            timeline=[
                {"time": time.time(), "event": "Incident declared", "phase": "detection"},
            ],
        )

        self._incidents[incident.incident_id] = incident
        return incident

    def update_incident(
        self,
        incident_id: str,
        phase: Optional[IncidentPhase] = None,
        status: Optional[str] = None,
        resolution: Optional[str] = None,
        event: Optional[str] = None,
    ) -> Optional[Incident]:
        """Update an incident."""
        incident = self._incidents.get(incident_id)
        if not incident:
            return None

        if phase:
            incident.phase = phase
            incident.timeline.append({
                "time": time.time(),
                "event": f"Phase transition to {phase.value}",
                "phase": phase.value,
            })

        if status:
            incident.status = status

        if resolution:
            incident.resolution = resolution
            incident.timeline.append({
                "time": time.time(),
                "event": f"Resolution: {resolution}",
            })

        if event:
            incident.timeline.append({
                "time": time.time(),
                "event": event,
            })

        return incident

    def get_playbook(self, playbook_name: str) -> Optional[Dict]:
        """Get an incident response playbook."""
        return self._playbooks.get(playbook_name)

    def get_incident_timeline(self, incident_id: str) -> List[Dict]:
        """Get incident timeline."""
        incident = self._incidents.get(incident_id)
        if not incident:
            return []
        return incident.timeline

    def get_open_incidents(self) -> List[Incident]:
        """Get all open incidents."""
        return [
            i for i in self._incidents.values()
            if i.status == "open"
        ]

    def generate_incident_report(self, incident_id: str) -> Optional[Dict]:
        """Generate an incident report."""
        incident = self._incidents.get(incident_id)
        if not incident:
            return None

        duration = time.time() - incident.created_at

        return {
            "incident_id": incident.incident_id,
            "title": incident.title,
            "description": incident.description,
            "severity": incident.severity,
            "status": incident.status,
            "phase": incident.phase.value,
            "affected_systems": incident.affected_systems,
            "duration_hours": round(duration / 3600, 2),
            "timeline": incident.timeline,
            "resolution": incident.resolution,
        }


# =============================================================
# SECTION 6: Compliance Auditing
# =============================================================

class ComplianceFramework(Enum):
    SOC2 = "soc2"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    ISO27001 = "iso27001"
    PCI_DSS = "pci_dss"


@dataclass
class ComplianceControl:
    """A compliance control."""
    control_id: str
    framework: ComplianceFramework
    title: str
    description: str
    category: str
    required: bool = True


@dataclass
class ComplianceAssessment:
    """Assessment result for a control."""
    control_id: str
    status: str  # compliant, non_compliant, partial, not_applicable
    evidence: List[str]
    findings: List[str]
    assessed_at: float
    assessed_by: str


class ComplianceAuditor:
    """
    Compliance auditing system.

    Features:
    - Control library management
    - Assessment tracking
    - Evidence collection
    - Gap analysis
    - Reporting
    """

    def __init__(self):
        self._controls: Dict[str, ComplianceControl] = {}
        self._assessments: Dict[str, List[ComplianceAssessment]] = defaultdict(list)
        self._setup_ai_security_controls()

    def _setup_ai_security_controls(self):
        """Setup AI security compliance controls."""
        ai_controls = [
            ComplianceControl(
                control_id="AI-001",
                framework=ComplianceFramework.SOC2,
                title="Model Access Control",
                description="Implement role-based access control for AI model access",
                category="access_control",
            ),
            ComplianceControl(
                control_id="AI-002",
                framework=ComplianceFramework.SOC2,
                title="Training Data Protection",
                description="Encrypt and protect training data at rest and in transit",
                category="data_protection",
            ),
            ComplianceControl(
                control_id="AI-003",
                framework=ComplianceFramework.SOC2,
                title="Model Audit Logging",
                description="Log all model access and inference requests",
                category="monitoring",
            ),
            ComplianceControl(
                control_id="AI-004",
                framework=ComplianceFramework.GDPR,
                title="Right to Explanation",
                description="Provide explanations for AI decisions affecting individuals",
                category="transparency",
            ),
            ComplianceControl(
                control_id="AI-005",
                framework=ComplianceFramework.GDPR,
                title="Data Minimization",
                description="Collect only necessary data for AI model training",
                category="data_protection",
            ),
            ComplianceControl(
                control_id="AI-006",
                framework=ComplianceFramework.SOC2,
                title="Incident Response",
                description="Maintain incident response plan for AI security events",
                category="incident_response",
            ),
            ComplianceControl(
                control_id="AI-007",
                framework=ComplianceFramework.ISO27001,
                title="Risk Assessment",
                description="Conduct regular risk assessments for AI systems",
                category="risk_management",
            ),
            ComplianceControl(
                control_id="AI-008",
                framework=ComplianceFramework.SOC2,
                title="Vendor Management",
                description="Assess security of AI service providers",
                category="third_party",
            ),
        ]

        for control in ai_controls:
            self._controls[control.control_id] = control

    def add_control(self, control: ComplianceControl):
        """Add a compliance control."""
        self._controls[control.control_id] = control

    def assess_control(
        self,
        control_id: str,
        status: str,
        evidence: List[str],
        findings: List[str],
        assessed_by: str,
    ) -> ComplianceAssessment:
        """Assess a compliance control."""
        assessment = ComplianceAssessment(
            control_id=control_id,
            status=status,
            evidence=evidence,
            findings=findings,
            assessed_at=time.time(),
            assessed_by=assessed_by,
        )

        self._assessments[control_id].append(assessment)
        return assessment

    def get_compliance_status(
        self,
        framework: Optional[ComplianceFramework] = None,
    ) -> Dict:
        """Get compliance status for a framework."""
        controls = self._controls.values()
        if framework:
            controls = [c for c in controls if c.framework == framework]

        results = {
            "total_controls": 0,
            "compliant": 0,
            "non_compliant": 0,
            "partial": 0,
            "not_assessed": 0,
            "compliance_score": 0,
            "control_details": [],
        }

        for control in controls:
            results["total_controls"] += 1
            assessments = self._assessments.get(control.control_id, [])

            if not assessments:
                results["not_assessed"] += 1
                status = "not_assessed"
            else:
                latest = assessments[-1]
                status = latest.status
                if status == "compliant":
                    results["compliant"] += 1
                elif status == "non_compliant":
                    results["non_compliant"] += 1
                elif status == "partial":
                    results["partial"] += 1

            results["control_details"].append({
                "control_id": control.control_id,
                "title": control.title,
                "framework": control.framework.value,
                "status": status,
            })

        # Calculate compliance score
        assessed = results["total_controls"] - results["not_assessed"]
        if assessed > 0:
            results["compliance_score"] = (
                (results["compliant"] / assessed) * 100
            )

        return results

    def generate_gap_analysis(self, framework: ComplianceFramework) -> Dict:
        """Generate gap analysis for a framework."""
        controls = [c for c in self._controls.values() if c.framework == framework]
        gaps = []

        for control in controls:
            assessments = self._assessments.get(control.control_id, [])
            if not assessments:
                gaps.append({
                    "control_id": control.control_id,
                    "title": control.title,
                    "gap_type": "not_assessed",
                    "recommendation": f"Conduct assessment for {control.title}",
                })
            elif assessments[-1].status == "non_compliant":
                gaps.append({
                    "control_id": control.control_id,
                    "title": control.title,
                    "gap_type": "non_compliant",
                    "findings": assessments[-1].findings,
                    "recommendation": f"Remediate: {control.title}",
                })

        return {
            "framework": framework.value,
            "total_controls": len(controls),
            "gaps_found": len(gaps),
            "gaps": gaps,
            "compliance_score": (
                (len(controls) - len(gaps)) / len(controls) * 100
            ) if controls else 0,
        }


# =============================================================
# DEMONSTRATIONS
# =============================================================

def demo_security_logging():
    """Demonstrate security logging."""
    print("\n" + "=" * 60)
    print("DEMO 1: Security Logging")
    print("=" * 60)

    logger = SecurityLogger()

    # Log various events
    logger.log_event(
        SecurityEventType.AUTH_SUCCESS,
        "api-gateway",
        {"method": "jwt", "session_id": "abc123"},
        user_id="user_001",
        ip_address="192.168.1.100",
    )

    logger.log_event(
        SecurityEventType.AUTH_FAILURE,
        "api-gateway",
        {"method": "password", "reason": "invalid_credentials"},
        user_id="user_002",
        ip_address="10.0.0.50",
        severity="warning",
    )

    logger.log_event(
        SecurityEventType.RATE_LIMIT_EXCEEDED,
        "ai-inference",
        {"endpoint": "/v1/completions", "limit": 100, "actual": 150},
        user_id="user_003",
        ip_address="172.16.0.10",
        severity="warning",
        tags=["api-abuse"],
    )

    logger.log_event(
        SecurityEventType.INTRUSION_DETECTED,
        "ids",
        {"attack_type": "brute_force", "attempts": 25},
        ip_address="5.5.5.5",
        severity="critical",
    )

    # Query events
    print("Recent security events:")
    events = logger.query_events(limit=5)
    for event in events:
        print(f"  [{event.severity.upper()}] {event.event_type.value}: {event.details}")

    # Statistics
    stats = logger.get_event_statistics(hours=1)
    print(f"\nStatistics:")
    print(f"  Total events: {stats['total_events']}")
    print(f"  By type: {stats['by_type']}")
    print(f"  By severity: {stats['by_severity']}")

    # Verify integrity
    integrity = logger.verify_log_integrity()
    print(f"\nLog integrity: chain length = {integrity['chain_length']}")

    print("\n[OK] Security logging demonstrated")


def demo_intrusion_detection():
    """Demonstrate intrusion detection."""
    print("\n" + "=" * 60)
    print("DEMO 2: Intrusion Detection System")
    print("=" * 60)

    ids = IntrusionDetectionSystem()

    # Simulate brute force attack
    print("Simulating brute force attack...")
    for i in range(7):
        event = {
            "event_type": "auth.failure",
            "ip_address": "attacker_ip_1",
            "timestamp": time.time(),
            "details": {"attempt": i + 1},
        }
        alerts = ids.analyze_event(event)
        if alerts:
            print(f"  Alert triggered: {alerts[0]['rule']} ({alerts[0]['severity']})")

    # Simulate normal traffic
    print("\nNormal traffic...")
    for i in range(3):
        event = {
            "event_type": "auth.success",
            "ip_address": "192.168.1.10",
            "timestamp": time.time(),
            "details": {"user": "legitimate_user"},
        }
        alerts = ids.analyze_event(event)
        print(f"  Event {i+1}: {len(alerts)} alerts")

    # Check blocked IPs
    blocked = ids.get_blocked_ips()
    print(f"\nBlocked IPs: {blocked}")

    # Get all alerts
    all_alerts = ids.get_alerts()
    print(f"Total alerts: {len(all_alerts)}")

    print("\n[OK] Intrusion detection demonstrated")


def demo_anomaly_detection():
    """Demonstrate anomaly detection."""
    print("\n" + "=" * 60)
    print("DEMO 3: Anomaly Detection")
    print("=" * 60)

    detector = AnomalyDetector(sensitivity=2.5)

    # Build baseline with normal data
    print("Building baseline with normal data...")
    for _ in range(100):
        value = 50 + random.gauss(0, 5)  # Normal: mean=50, std=5
        detector.update_baseline("api_latency", value)

    # Test with normal value
    normal_value = 52
    result = detector.detect_anomaly("api_latency", normal_value)
    print(f"\nNormal value ({normal_value}):")
    print(f"  Anomaly: {result['is_anomaly']}")
    print(f"  Z-score: {result['z_score']}")

    # Test with anomalous value
    anomalous_value = 200
    result = detector.detect_anomaly("api_latency", anomalous_value)
    print(f"\nAnomalous value ({anomalous_value}):")
    print(f"  Anomaly: {result['is_anomaly']}")
    print(f"  Z-score: {result['z_score']}")

    # Time series anomaly
    print("\nTime series anomaly detection:")
    for i in range(30):
        value = 100 + random.gauss(0, 10)
        detector.update_baseline("requests_per_second", value)
        detector.detect_anomaly("requests_per_second", value)

    # Sudden spike
    spike_result = detector.detect_time_series_anomaly("requests_per_second", 500)
    print(f"  Spike detected: {spike_result['is_anomaly']}")
    if spike_result['is_anomaly']:
        print(f"  Type: {spike_result.get('type')}")
        print(f"  Change ratio: {spike_result.get('change_ratio', spike_result.get('z_score'))}")

    # Baseline summary
    summary = detector.get_baseline_summary()
    print(f"\nBaseline summary:")
    for metric, stats in summary.items():
        print(f"  {metric}: mean={stats['mean']}, std={stats['std']}, samples={stats['count']}")

    print("\n[OK] Anomaly detection demonstrated")


def demo_alert_management():
    """Demonstrate alert management."""
    print("\n" + "=" * 60)
    print("DEMO 4: Alert Management System")
    print("=" * 60)

    manager = AlertManager()

    # Create alerts
    alert1 = manager.create_alert(
        title="Brute Force Attack Detected",
        description="Multiple failed login attempts from IP 5.5.5.5",
        severity=AlertSeverity.HIGH,
        source="ids",
        affected_assets=["api-gateway"],
        metadata={"ip": "5.5.5.5", "attempts": 25},
    )
    print(f"Alert created: {alert1.alert_id}")
    print(f"  Title: {alert1.title}")
    print(f"  Severity: {alert1.severity.value}")

    alert2 = manager.create_alert(
        title="Data Exfiltration Attempt",
        description="Large data transfer detected from model server",
        severity=AlertSeverity.CRITICAL,
        source="dlp",
        affected_assets=["model-server", "storage"],
    )
    print(f"\nAlert created: {alert2.alert_id}")
    print(f"  Escalated: {alert2.escalated}")

    # Update alert
    manager.update_alert(
        alert1.alert_id,
        status=AlertStatus.INVESTIGATING,
        assigned_to="security-team",
    )

    # Get statistics
    stats = manager.get_alert_statistics(hours=1)
    print(f"\nAlert Statistics:")
    print(f"  Total: {stats['total_alerts']}")
    print(f"  By severity: {stats['by_severity']}")
    print(f"  By status: {stats['by_status']}")

    # Open alerts
    open_alerts = manager.get_open_alerts()
    print(f"\nOpen alerts: {len(open_alerts)}")

    print("\n[OK] Alert management demonstrated")


def demo_incident_response():
    """Demonstrate incident response."""
    print("\n" + "=" * 60)
    print("DEMO 5: Incident Response Management")
    print("=" * 60)

    irm = IncidentResponseManager()

    # Declare incident
    incident = irm.declare_incident(
        title="Training Data Breach",
        description="Unauthorized access to training data storage detected",
        severity="critical",
        affected_systems=["data-lake", "training-pipeline"],
        playbook="data_breach",
    )
    print(f"Incident declared: {incident.incident_id}")
    print(f"  Title: {incident.title}")
    print(f"  Phase: {incident.phase.value}")

    # Update through phases
    irm.update_incident(
        incident.incident_id,
        phase=IncidentPhase.CONTAINMENT,
        event="Isolated affected systems",
    )

    irm.update_incident(
        incident.incident_id,
        event="Preserved forensic evidence",
    )

    irm.update_incident(
        incident.incident_id,
        phase=IncidentPhase.ERADICATION,
        event="Removed attacker access",
    )

    irm.update_incident(
        incident.incident_id,
        phase=IncidentPhase.RECOVERY,
        event="Restored from clean backup",
    )

    # Get playbook
    playbook = irm.get_playbook("data_breach")
    print(f"\nPlaybook: {playbook['name']}")
    print(f"  Phases: {len(playbook['phases'])}")

    # Get timeline
    timeline = irm.get_incident_timeline(incident.incident_id)
    print(f"\nIncident Timeline:")
    for entry in timeline:
        phase = entry.get('phase', 'update')
        print(f"  [{phase}] {entry['event']}")

    # Generate report
    report = irm.generate_incident_report(incident.incident_id)
    print(f"\nIncident Report:")
    print(f"  Duration: {report['duration_hours']} hours")
    print(f"  Status: {report['status']}")
    print(f"  Timeline events: {len(report['timeline'])}")

    print("\n[OK] Incident response demonstrated")


def demo_compliance_auditing():
    """Demonstrate compliance auditing."""
    print("\n" + "=" * 60)
    print("DEMO 6: Compliance Auditing")
    print("=" * 60)

    auditor = ComplianceAuditor()

    # Assess controls
    auditor.assess_control(
        "AI-001",
        "compliant",
        ["RBAC implemented", "Access logs available"],
        [],
        "security-auditor",
    )

    auditor.assess_control(
        "AI-002",
        "compliant",
        ["AES-256 encryption at rest", "TLS 1.3 in transit"],
        [],
        "security-auditor",
    )

    auditor.assess_control(
        "AI-003",
        "partial",
        ["Basic logging in place"],
        ["Missing inference request logging"],
        "security-auditor",
    )

    auditor.assess_control(
        "AI-004",
        "non_compliant",
        [],
        ["No explanation mechanism for AI decisions"],
        "security-auditor",
    )

    # Get compliance status
    soc2_status = auditor.get_compliance_status(ComplianceFramework.SOC2)
    print("SOC 2 Compliance Status:")
    print(f"  Total controls: {soc2_status['total_controls']}")
    print(f"  Compliant: {soc2_status['compliant']}")
    print(f"  Non-compliant: {soc2_status['non_compliant']}")
    print(f"  Partial: {soc2_status['partial']}")
    print(f"  Score: {soc2_status['compliance_score']:.1f}%")

    # Gap analysis
    print("\nGDPR Gap Analysis:")
    gaps = auditor.generate_gap_analysis(ComplianceFramework.GDPR)
    print(f"  Total controls: {gaps['total_controls']}")
    print(f"  Gaps found: {gaps['gaps_found']}")
    print(f"  Compliance score: {gaps['compliance_score']:.1f}%")

    for gap in gaps["gaps"]:
        print(f"  - {gap['control_id']}: {gap['title']} ({gap['gap_type']})")

    print("\n[OK] Compliance auditing demonstrated")


# =============================================================
# ATTACK PATTERNS & DEFENSES
# =============================================================

ATTACK_PATTERNS = """
+==============================================================+
|            SECURITY MONITORING CHALLENGES                    |
+==============================================================+
|                                                              |
|  1. LOG MANIPULATION                                         |
|     Attack: Delete or modify security logs                   |
|     Defense: Tamper-evident logs, remote storage, chaining   |
|                                                              |
|  2. ALERT FATIGUE                                            |
|     Attack: Overwhelm with false positives                   |
|     Defense: Tuning, correlation, deduplication              |
|                                                              |
|  3. EVASION TECHNIQUES                                       |
|     Attack: Slow attacks to avoid detection                  |
|     Defense: Long-term behavioral analysis, correlation      |
|                                                              |
|  4. INSIDER THREATS                                          |
|     Attack: Malicious actions by trusted users               |
|     Defense: UEBA, least privilege, monitoring               |
|                                                              |
|  5. LATERAL MOVEMENT                                         |
|     Attack: Move through network undetected                  |
|     Defense: Network segmentation, east-west monitoring      |
|                                                              |
+==============================================================+
"""


# =============================================================
# MAIN EXECUTION
# =============================================================

if __name__ == "__main__":
    print("+==============================================================+")
    print("|   Topic 10: Security Monitoring & Incident Response         |")
    print("+==============================================================+")

    import random

    try:
        demo_security_logging()
        demo_intrusion_detection()
        demo_anomaly_detection()
        demo_alert_management()
        demo_incident_response()
        demo_compliance_auditing()

        print(ATTACK_PATTERNS)

        print("\n" + "=" * 60)
        print("[OK] ALL SECURITY MONITORING DEMOS COMPLETED")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
