"""
10 Security Monitoring: Intrusion Detection
"""

from ._types import *


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
        self.add_rule(
            {
                "name": "brute_force_detection",
                "description": "Detect brute force login attempts",
                "condition": lambda events: self._check_brute_force(events),
                "severity": "high",
                "action": "block_ip",
            }
        )

        self.add_rule(
            {
                "name": "port_scan_detection",
                "description": "Detect port scanning activity",
                "condition": lambda events: self._check_port_scan(events),
                "severity": "medium",
                "action": "alert",
            }
        )

        self.add_rule(
            {
                "name": "data_exfiltration",
                "description": "Detect potential data exfiltration",
                "condition": lambda events: self._check_exfiltration(events),
                "severity": "critical",
                "action": "block_and_alert",
            }
        )

        self.add_rule(
            {
                "name": "api_abuse",
                "description": "Detect API abuse patterns",
                "condition": lambda events: self._check_api_abuse(events),
                "severity": "high",
                "action": "rate_limit",
            }
        )

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
            e
            for e in events
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
            e
            for e in events
            if e.get("event_type") == "data.download"
            and e.get("details", {}).get("size_bytes", 0) > 10 * 1024 * 1024  # 10MB
        ]
        return len(large_downloads) >= 3

    def _check_api_abuse(self, events: List[Dict]) -> bool:
        """Check for API abuse pattern."""
        api_calls = [
            e
            for e in events
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
