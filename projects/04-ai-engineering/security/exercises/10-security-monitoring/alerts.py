"""
10 Security Monitoring: Alerts
"""

from ._types import *
from .incident_response import Incident


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
            a
            for a in self._alerts.values()
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
