# Lecture 10: Security Monitoring & Incident Response

## Topic Overview

Security monitoring involves continuously observing AI systems for threats, anomalies, and security events. This lecture covers logging, alerting, anomaly detection, incident response procedures, forensics, and building a security operations center (SOC) for AI. Effective monitoring is essential for detecting and responding to security incidents before they cause significant damage.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Design** comprehensive logging systems for AI applications
2. **Implement** real-time alerting for security events
3. **Build** anomaly detection systems for AI behavior
4. **Create** incident response procedures
5. **Perform** security forensics and root cause analysis
6. **Build** security dashboards for monitoring
7. **Apply** threat detection techniques for AI systems

---

## Key Concepts

### 1. Security Logging

```python
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class LogLevel(Enum):
    """Security log levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class SecurityEvent:
    """Security event log entry."""
    timestamp: datetime
    event_type: str
    severity: LogLevel
    source: str
    user_id: Optional[str]
    ip_address: Optional[str]
    details: Dict[str, Any]
    event_id: str

class SecurityLogger:
    """Comprehensive security logging system."""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(f"security.{service_name}")
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(f"security_{service_name}.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)

    def log_event(self, event: SecurityEvent):
        """Log a security event."""
        log_entry = {
            "event_id": event.event_id,
            "timestamp": event.timestamp.isoformat(),
            "event_type": event.event_type,
            "severity": event.severity.value,
            "source": event.source,
            "user_id": event.user_id,
            "ip_address": event.ip_address,
            "details": event.details,
            "service": self.service_name,
        }

        # Log based on severity
        if event.severity == LogLevel.CRITICAL:
            self.logger.critical(json.dumps(log_entry))
        elif event.severity == LogLevel.ERROR:
            self.logger.error(json.dumps(log_entry))
        elif event.severity == LogLevel.WARNING:
            self.logger.warning(json.dumps(log_entry))
        else:
            self.logger.info(json.dumps(log_entry))

    def log_authentication(self, user_id: str, success: bool,
                          ip_address: str, method: str):
        """Log authentication attempt."""
        event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type="authentication",
            severity=LogLevel.INFO if success else LogLevel.WARNING,
            source="auth_service",
            user_id=user_id,
            ip_address=ip_address,
            details={
                "success": success,
                "method": method,
            },
            event_id=f"auth_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        )
        self.log_event(event)

    def log_authorization(self, user_id: str, resource: str,
                         action: str, allowed: bool):
        """Log authorization decision."""
        event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type="authorization",
            severity=LogLevel.INFO if allowed else LogLevel.WARNING,
            source="authz_service",
            user_id=user_id,
            ip_address=None,
            details={
                "resource": resource,
                "action": action,
                "allowed": allowed,
            },
            event_id=f"authz_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        )
        self.log_event(event)

    def log_data_access(self, user_id: str, data_type: str,
                       access_type: str, record_count: int):
        """Log data access."""
        event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type="data_access",
            severity=LogLevel.INFO,
            source="data_service",
            user_id=user_id,
            ip_address=None,
            details={
                "data_type": data_type,
                "access_type": access_type,
                "record_count": record_count,
            },
            event_id=f"data_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        )
        self.log_event(event)

    def log_security_violation(self, violation_type: str,
                               details: Dict[str, Any],
                               ip_address: str = None):
        """Log a security violation."""
        event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type="security_violation",
            severity=LogLevel.CRITICAL,
            source="security_monitor",
            user_id=details.get("user_id"),
            ip_address=ip_address,
            details={
                "violation_type": violation_type,
                **details,
            },
            event_id=f"violation_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        )
        self.log_event(event)

# Usage
logger = SecurityLogger("ai-api")
logger.log_authentication("user123", True, "192.168.1.100", "password")
logger.log_data_access("user123", "training_data", "read", 1000)
logger.log_security_violation("prompt_injection", {
    "user_id": "user456",
    "input_preview": "Ignore all previous...",
}, "10.0.0.50")
```

### 2. Anomaly Detection

```python
import numpy as np
from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta

class AnomalyDetector:
    """Detect anomalous behavior in AI systems."""

    def __init__(self):
        self.baselines: Dict[str, Dict] = {}
        self.alerts: List[Dict] = []

    def establish_baseline(self, metric_name: str, values: List[float]):
        """Establish baseline for a metric."""
        self.baselines[metric_name] = {
            "mean": np.mean(values),
            "std": np.std(values),
            "min": np.min(values),
            "max": np.max(values),
            "p95": np.percentile(values, 95),
            "p99": np.percentile(values, 99),
        }

    def detect_anomaly(self, metric_name: str, value: float) -> Dict:
        """Detect if a value is anomalous."""
        if metric_name not in self.baselines:
            return {"anomaly": False, "reason": "no_baseline"}

        baseline = self.baselines[metric_name]
        z_score = abs(value - baseline["mean"]) / (baseline["std"] + 1e-8)

        is_anomaly = z_score > 3  # 3 standard deviations

        if is_anomaly:
            self.alerts.append({
                "timestamp": datetime.utcnow().isoformat(),
                "metric": metric_name,
                "value": value,
                "z_score": z_score,
                "baseline_mean": baseline["mean"],
                "baseline_std": baseline["std"],
            })

        return {
            "anomaly": is_anomaly,
            "z_score": z_score,
            "threshold": 3.0,
        }

class RequestAnomalyDetector:
    """Detect anomalous API request patterns."""

    def __init__(self):
        self.user_patterns: Dict[str, Dict] = defaultdict(lambda: {
            "request_times": [],
            "endpoints": defaultdict(int),
            "error_count": 0,
            "total_count": 0,
        })

    def record_request(self, user_id: str, endpoint: str,
                      status_code: int):
        """Record a user request."""
        pattern = self.user_patterns[user_id]
        pattern["request_times"].append(datetime.utcnow())
        pattern["endpoints"][endpoint] += 1
        pattern["total_count"] += 1
        if status_code >= 400:
            pattern["error_count"] += 1

    def detect_brute_force(self, user_id: str,
                           time_window_minutes: int = 5) -> Dict:
        """Detect brute force attack attempts."""
        pattern = self.user_patterns[user_id]
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=time_window_minutes)

        recent_errors = 0
        for time in pattern["request_times"]:
            if time > window_start:
                recent_errors += 1

        is_brute_force = recent_errors > 10

        return {
            "detected": is_brute_force,
            "recent_requests": recent_errors,
            "threshold": 10,
        }

    def detect_scraping(self, user_id: str,
                        time_window_minutes: int = 1) -> Dict:
        """Detect scraping behavior."""
        pattern = self.user_patterns[user_id]
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=time_window_minutes)

        recent_requests = sum(1 for t in pattern["request_times"]
                            if t > window_start)

        # High request rate to many different endpoints
        unique_endpoints = len(pattern["endpoints"])
        is_scraping = recent_requests > 50 and unique_endpoints > 20

        return {
            "detected": is_scraping,
            "recent_requests": recent_requests,
            "unique_endpoints": unique_endpoints,
        }

    def detect_model_extraction(self, user_id: str) -> Dict:
        """Detect model extraction attempts."""
        pattern = self.user_patterns[user_id]

        # Check for systematic querying
        if pattern["total_count"] > 10000:
            return {
                "detected": True,
                "reason": "high_query_volume",
                "total_queries": pattern["total_count"],
            }

        return {"detected": False}
```

### 3. Real-Time Alerting

```python
from typing import Callable, List, Dict
from datetime import datetime
from enum import Enum

class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertManager:
    """Manage security alerts."""

    def __init__(self):
        self.alert_rules: List[Dict] = []
        self.alert_history: List[Dict] = []
        self.notification_channels: List[Callable] = []

    def add_rule(self, name: str, condition: Callable,
                 severity: AlertSeverity, message_template: str):
        """Add an alert rule."""
        self.alert_rules.append({
            "name": name,
            "condition": condition,
            "severity": severity,
            "message_template": message_template,
        })

    def add_notification_channel(self, channel: Callable):
        """Add a notification channel (email, slack, etc.)."""
        self.notification_channels.append(channel)

    def evaluate_rules(self, metrics: Dict) -> List[Dict]:
        """Evaluate all alert rules against current metrics."""
        triggered_alerts = []

        for rule in self.alert_rules:
            if rule["condition"](metrics):
                alert = {
                    "rule": rule["name"],
                    "severity": rule["severity"].value,
                    "message": rule["message_template"].format(**metrics),
                    "timestamp": datetime.utcnow().isoformat(),
                    "metrics": metrics,
                }
                triggered_alerts.append(alert)
                self.alert_history.append(alert)

                # Send notifications
                for channel in self.notification_channels:
                    try:
                        channel(alert)
                    except Exception as e:
                        print(f"Notification failed: {e}")

        return triggered_alerts

    def get_alert_summary(self, hours: int = 24) -> Dict:
        """Get summary of alerts in time window."""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        recent_alerts = [
            a for a in self.alert_history
            if datetime.fromisoformat(a["timestamp"]) > cutoff
        ]

        severity_counts = defaultdict(int)
        for alert in recent_alerts:
            severity_counts[alert["severity"]] += 1

        return {
            "total_alerts": len(recent_alerts),
            "by_severity": dict(severity_counts),
            "time_window_hours": hours,
        }

# Usage
alert_manager = AlertManager()

# Add rules
alert_manager.add_rule(
    name="high_error_rate",
    condition=lambda m: m.get("error_rate", 0) > 0.1,
    severity=AlertSeverity.WARNING,
    message_template="High error rate: {error_rate:.2%}"
)

alert_manager.add_rule(
    name="critical_security_violation",
    condition=lambda m: m.get("security_violations", 0) > 0,
    severity=AlertSeverity.CRITICAL,
    message_template="Security violation detected: {violation_type}"
)

# Add notification channels
def log_alert(alert: Dict):
    print(f"ALERT [{alert['severity']}]: {alert['message']}")

alert_manager.add_notification_channel(log_alert)

# Evaluate
metrics = {"error_rate": 0.15, "security_violations": 1}
alerts = alert_manager.evaluate_rules(metrics)
```

### 4. Incident Response

```python
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

class IncidentStatus(Enum):
    """Incident status."""
    DETECTED = "detected"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    ERADICATED = "eradicated"
    RECOVERED = "recovered"
    CLOSED = "closed"

class SecurityIncident:
    """Security incident management."""

    def __init__(self, incident_id: str, title: str, severity: str):
        self.incident_id = incident_id
        self.title = title
        self.severity = severity
        self.status = IncidentStatus.DETECTED
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.timeline: List[Dict] = []
        self.evidence: List[Dict] = []
        self.actions_taken: List[Dict] = []

    def update_status(self, new_status: IncidentStatus, note: str = ""):
        """Update incident status."""
        self.status = new_status
        self.updated_at = datetime.utcnow()
        self.timeline.append({
            "timestamp": self.updated_at.isoformat(),
            "event": "status_change",
            "new_status": new_status.value,
            "note": note,
        })

    def add_evidence(self, evidence_type: str, description: str,
                    data: Dict):
        """Add evidence to incident."""
        self.evidence.append({
            "type": evidence_type,
            "description": description,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def add_action(self, action: str, owner: str, result: str = ""):
        """Record an action taken."""
        self.actions_taken.append({
            "action": action,
            "owner": owner,
            "result": result,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def get_summary(self) -> Dict:
        """Get incident summary."""
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "severity": self.severity,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "timeline_entries": len(self.timeline),
            "evidence_count": len(self.evidence),
            "actions_count": len(self.actions_taken),
            "duration_hours": (datetime.utcnow() - self.created_at).total_seconds() / 3600,
        }

class IncidentResponsePlan:
    """Incident response procedures."""

    def __init__(self):
        self.procedures = {
            "detection": self._detection_procedure,
            "analysis": self._analysis_procedure,
            "containment": self._containment_procedure,
            "eradication": self._eradication_procedure,
            "recovery": self._recovery_procedure,
            "post_mortem": self._post_mortem_procedure,
        }

    def execute_procedure(self, phase: str, incident: SecurityIncident) -> Dict:
        """Execute an incident response procedure."""
        if phase in self.procedures:
            return self.procedures[phase](incident)
        return {"error": f"Unknown phase: {phase}"}

    def _detection_procedure(self, incident: SecurityIncident) -> Dict:
        """Detection phase procedures."""
        return {
            "phase": "detection",
            "steps": [
                "Verify the alert is not a false positive",
                "Identify affected systems and data",
                "Assess initial severity",
                "Notify security team",
            ],
            "owner": "Security Operations",
            "sl_hours": 1,
        }

    def _analysis_procedure(self, incident: SecurityIncident) -> Dict:
        """Analysis phase procedures."""
        return {
            "phase": "analysis",
            "steps": [
                "Collect and preserve evidence",
                "Analyze logs and indicators",
                "Determine root cause",
                "Assess scope and impact",
                "Document findings",
            ],
            "owner": "Incident Response Team",
            "sl_hours": 4,
        }

    def _containment_procedure(self, incident: SecurityIncident) -> Dict:
        """Containment phase procedures."""
        return {
            "phase": "containment",
            "steps": [
                "Isolate affected systems",
                "Block malicious IPs/accounts",
                "Preserve evidence for forensics",
                "Implement temporary fixes",
            ],
            "owner": "Incident Response Team",
            "sl_hours": 2,
        }

    def _eradication_procedure(self, incident: SecurityIncident) -> Dict:
        """Eradication phase procedures."""
        return {
            "phase": "eradication",
            "steps": [
                "Remove malware/backdoors",
                "Patch vulnerabilities",
                "Reset compromised credentials",
                "Verify system integrity",
            ],
            "owner": "Engineering Team",
            "sl_hours": 24,
        }

    def _recovery_procedure(self, incident: SecurityIncident) -> Dict:
        """Recovery phase procedures."""
        return {
            "phase": "recovery",
            "steps": [
                "Restore systems from clean backups",
                "Verify system functionality",
                "Monitor for recurrence",
                "Gradually restore service",
            ],
            "owner": "Engineering Team",
            "sl_hours": 24,
        }

    def _post_mortem_procedure(self, incident: SecurityIncident) -> Dict:
        """Post-mortem phase procedures."""
        return {
            "phase": "post_mortem",
            "steps": [
                "Conduct blameless post-mortem",
                "Document lessons learned",
                "Implement preventive measures",
                "Update incident response plan",
            ],
            "owner": "Security Team",
            "sl_hours": 168,  # 1 week
        }

# Usage
incident = SecurityIncident(
    incident_id="INC-2024-001",
    title="Prompt Injection Attack Detected",
    severity="high"
)

incident.update_status(IncidentStatus.INVESTIGATING, "Starting investigation")
incident.add_evidence("log", "Suspicious API logs", {"user": "attacker123"})
incident.add_action("blocked_user", "Security Analyst", "User account blocked")
```

### 5. Security Dashboard

```python
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class SecurityDashboard:
    """Security monitoring dashboard."""

    def __init__(self):
        self.metrics = defaultdict(list)
        self.incidents: List[Dict] = []

    def record_metric(self, metric_name: str, value: float,
                     timestamp: datetime = None):
        """Record a security metric."""
        self.metrics[metric_name].append({
            "value": value,
            "timestamp": timestamp or datetime.utcnow(),
        })

    def get_dashboard_data(self, hours: int = 24) -> Dict:
        """Get dashboard data for time window."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        dashboard = {
            "summary": self._get_summary(cutoff),
            "metrics": self._get_metrics_summary(cutoff),
            "recent_incidents": self._get_recent_incidents(cutoff),
            "alerts": self._get_recent_alerts(cutoff),
            "trends": self._get_trends(cutoff),
        }

        return dashboard

    def _get_summary(self, cutoff: datetime) -> Dict:
        """Get summary statistics."""
        return {
            "total_requests": len(self.metrics.get("requests", [])),
            "total_errors": len(self.metrics.get("errors", [])),
            "total_incidents": len([
                i for i in self.incidents
                if i["timestamp"] > cutoff
            ]),
            "active_incidents": len([
                i for i in self.incidents
                if i["status"] != "closed"
            ]),
        }

    def _get_metrics_summary(self, cutoff: datetime) -> Dict:
        """Get metrics summary."""
        summary = {}
        for metric_name, values in self.metrics.items():
            recent = [v for v in values if v["timestamp"] > cutoff]
            if recent:
                summary[metric_name] = {
                    "count": len(recent),
                    "avg": sum(v["value"] for v in recent) / len(recent),
                    "min": min(v["value"] for v in recent),
                    "max": max(v["value"] for v in recent),
                }
        return summary

    def _get_recent_incidents(self, cutoff: datetime) -> List[Dict]:
        """Get recent incidents."""
        return [
            i for i in self.incidents
            if i["timestamp"] > cutoff
        ][:10]

    def _get_recent_alerts(self, cutoff: datetime) -> List[Dict]:
        """Get recent alerts."""
        # Would fetch from alert manager
        return []

    def _get_trends(self, cutoff: datetime) -> Dict:
        """Get metric trends."""
        trends = {}
        for metric_name in ["requests", "errors", "security_violations"]:
            if metric_name in self.metrics:
                values = self.metrics[metric_name]
                recent = [v["value"] for v in values if v["timestamp"] > cutoff]
                if len(recent) >= 2:
                    trends[metric_name] = {
                        "trend": "increasing" if recent[-1] > recent[0] else "decreasing",
                        "change": recent[-1] - recent[0],
                    }
        return trends
```

### 6. Threat Intelligence

```python
class ThreatIntelligence:
    """Threat intelligence for AI systems."""

    def __init__(self):
        self.indicators = {
            "malicious_ips": set(),
            "malicious_patterns": [],
            "known_attacks": [],
        }

    def add_indicator(self, indicator_type: str, value: str):
        """Add a threat indicator."""
        if indicator_type in self.indicators:
            if isinstance(self.indicators[indicator_type], set):
                self.indicators[indicator_type].add(value)
            else:
                self.indicators[indicator_type].append(value)

    def check_indicator(self, indicator_type: str, value: str) -> bool:
        """Check if an indicator is known malicious."""
        if indicator_type in self.indicators:
            if isinstance(self.indicators[indicator_type], set):
                return value in self.indicators[indicator_type]
            else:
                return any(value in item for item in self.indicators[indicator_type])
        return False

    def analyze_threat_landscape(self) -> Dict:
        """Analyze current threat landscape for AI systems."""
        return {
            "top_threats": [
                "Prompt injection attacks",
                "Model extraction attempts",
                "Data poisoning",
                "API abuse",
            ],
            "emerging_threats": [
                "Multi-modal injection attacks",
                "Adversarial ML attacks",
                "Supply chain attacks on AI models",
            ],
            "recommended_defenses": [
                "Implement input validation",
                "Enable rate limiting",
                "Monitor for anomalies",
                "Regular security audits",
            ],
        }

    def correlate_events(self, events: List[Dict]) -> List[Dict]:
        """Correlate security events to identify patterns."""
        correlations = []

        # Group events by source IP
        by_ip = defaultdict(list)
        for event in events:
            if "ip_address" in event:
                by_ip[event["ip_address"]].append(event)

        # Find suspicious patterns
        for ip, ip_events in by_ip.items():
            if len(ip_events) > 10:
                correlations.append({
                    "type": "high_activity_ip",
                    "ip": ip,
                    "event_count": len(ip_events),
                    "time_span": (
                        ip_events[-1]["timestamp"] - ip_events[0]["timestamp"]
                    ).total_seconds(),
                })

        return correlations
```

---

## Common Mistakes to Avoid

1. **No logging** — You can't investigate what you don't log
2. **Logging too much** — Can overwhelm storage and analysis
3. **Not monitoring logs** — Logs are useless without monitoring
4. **No alerting** — Manual monitoring doesn't scale
5. **Ignoring alerts** — Alert fatigue leads to missed incidents
6. **No incident response plan** — Chaos during actual incidents
7. **Not practicing** — Regular drills are essential
8. **No post-mortem** — Learning from incidents is crucial

---

## Best Practices

1. **Log everything relevant** — Authentication, authorization, data access
2. **Centralize logs** — Use SIEM or log aggregation
3. **Set up alerts** — For critical security events
4. **Document procedures** — Have written incident response plans
5. **Practice regularly** — Conduct security drills
6. **Learn from incidents** — Perform blameless post-mortems
7. **Update defenses** — Based on new threats and lessons learned
8. **Report to stakeholders** — Regular security reporting

---

## Practice Exercises

### Exercise 1: Security Logger (Easy)
Implement a security logging system for an AI API.

### Exercise 2: Anomaly Detector (Medium)
Build an anomaly detection system for API request patterns.

### Exercise 3: Alert System (Medium)
Create a real-time alerting system with multiple notification channels.

### Exercise 4: Incident Response (Hard)
Develop a complete incident response workflow with automation.

---

## Summary

Security monitoring is essential for detecting and responding to threats. Key takeaways:

- **Comprehensive logging** provides visibility into system activity
- **Anomaly detection** identifies suspicious behavior
- **Real-time alerting** enables rapid response
- **Incident response procedures** ensure organized handling
- **Forensics and analysis** help understand root causes
- **Continuous improvement** strengthens defenses over time

---

## References

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [SANS Incident Response](https://www.sans.org/white-papers/incident-response/)
