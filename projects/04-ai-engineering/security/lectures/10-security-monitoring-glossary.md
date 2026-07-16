# Glossary 10: Security Monitoring Terms

## Quick Reference Table

| Term | Category | Importance | See Also |
|------|----------|------------|----------|
| Security Monitoring | Process | Critical | SIEM, Log Analysis |
| Anomaly Detection | Technique | Critical | Behavioral Analysis |
| Incident Response | Process | Critical | IR Plan, Forensics |
| SIEM | Tool | High | Security Information Management |
| Alert Fatigue | Problem | High | Alert Management |
| Threat Intelligence | Intelligence | High | IoC, TTPs |
| Log Aggregation | Technique | High | Centralized Logging |
| Forensics | Process | High | Digital Forensics |
| Post-Mortem | Process | High | Root Cause Analysis |
| Playbook | Document | High | Runbook, Procedures |
| Indicator of Compromise | Intelligence | Critical | IoC |
| MITRE ATT&CK | Framework | High | Threat Framework |
| SOC | Organization | High | Security Operations |
| Dashboard | Tool | High | Visualization |
| Root Cause Analysis | Process | High | RCA, Post-Mortem |
| Tabletop Exercise | Process | Medium | Drill, Simulation |

---

## Alphabetical Definitions

### Alert Fatigue

**Definition**: A condition where security personnel become overwhelmed by the volume of alerts, leading to missed or ignored critical alerts.

**Example**:
```python
class AlertFatigueMonitor:
    """Monitor and prevent alert fatigue."""

    def __init__(self):
        self.alert_history = []
        self.false_positive_rate = 0.0

    def track_alert(self, alert: dict, outcome: str):
        """Track alert and its outcome."""
        self.alert_history.append({
            "alert": alert,
            "outcome": outcome,  # "true_positive", "false_positive"
            "timestamp": datetime.utcnow(),
        })
        self._update_metrics()

    def _update_metrics(self):
        """Update fatigue metrics."""
        if self.alert_history:
            false_positives = sum(
                1 for a in self.alert_history
                if a["outcome"] == "false_positive"
            )
            self.false_positive_rate = false_positives / len(self.alert_history)

    def get_fatigue_score(self) -> dict:
        """Calculate alert fatigue score."""
        # Factors contributing to fatigue
        factors = {
            "false_positive_rate": self.false_positive_rate,
            "alert_volume": min(len(self.alert_history) / 100, 1.0),
            "duplicate_rate": self._calculate_duplicate_rate(),
        }

        # Weighted fatigue score (0-1, higher = more fatigued)
        fatigue_score = (
            factors["false_positive_rate"] * 0.5 +
            factors["alert_volume"] * 0.3 +
            factors["duplicate_rate"] * 0.2
        )

        return {
            "fatigue_score": fatigue_score,
            "factors": factors,
            "recommendation": self._get_recommendation(fatigue_score),
        }

    def _calculate_duplicate_rate(self) -> float:
        """Calculate rate of duplicate alerts."""
        # Simplified duplicate detection
        return 0.2  # Placeholder

    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on fatigue score."""
        if score > 0.8:
            return "Critical: Review and tune alert rules immediately"
        elif score > 0.6:
            return "High: Reduce false positives and alert volume"
        elif score > 0.4:
            return "Medium: Consider alert consolidation"
        return "Low: Current alert levels are manageable"
```

**Related Terms**: Alert Management, False Positive, SOC

---

### Anomaly Detection

**Definition**: The process of identifying patterns in data that do not conform to expected behavior, often indicating security threats or system issues.

**Example**:
```python
class AnomalyDetector:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.baseline = None

    def establish_baseline(self, data: list):
        """Establish baseline from normal behavior."""
        import numpy as np
        self.baseline = {
            "mean": np.mean(data),
            "std": np.std(data),
            "min": np.min(data),
            "max": np.max(data),
        }

    def detect(self, value: float, threshold: float = 3.0) -> dict:
        """Detect if value is anomalous."""
        if self.baseline is None:
            return {"anomaly": False, "reason": "no_baseline"}

        z_score = abs(value - self.baseline["mean"]) / (self.baseline["std"] + 1e-8)

        return {
            "anomaly": z_score > threshold,
            "z_score": z_score,
            "threshold": threshold,
        }

# Usage
detector = AnomalyDetector()
detector.establish_baseline([10, 12, 11, 13, 12, 11, 10, 12])
result = detector.detect(50)  # Anomalous value
print(f"Anomaly detected: {result['anomaly']}")
```

**Related Terms**: Behavioral Analysis, Statistical Detection, ML-based Detection

---

### Dashboard

**Definition**: A visual display of key security metrics and indicators, providing real-time visibility into system security status.

**Example**:
```python
class SecurityDashboard:
    def __init__(self):
        self.widgets = []

    def add_widget(self, widget_type: str, title: str, data_source: str):
        """Add a widget to the dashboard."""
        self.widgets.append({
            "type": widget_type,
            "title": title,
            "data_source": data_source,
        })

    def generate_dashboard(self) -> dict:
        """Generate dashboard configuration."""
        return {
            "layout": "grid",
            "refresh_interval": 60,
            "widgets": self.widgets,
            "alerts_panel": True,
            "metrics_panel": True,
        }

# Usage
dashboard = SecurityDashboard()
dashboard.add_widget("line_chart", "API Requests", "metrics.requests")
dashboard.add_widget("bar_chart", "Error Rates", "metrics.errors")
dashboard.add_widget("pie_chart", "Alert Severity", "alerts.severity_distribution")
dashboard.add_widget("table", "Recent Incidents", "incidents.recent")
```

**Related Terms**: Visualization, Metrics, Monitoring

---

### Digital Forensics

**Definition**: The process of collecting, preserving, and analyzing digital evidence to investigate security incidents.

**Example**:
```python
class DigitalForensics:
    """Digital forensics procedures."""

    def __init__(self):
        self.evidence_chain = []

    def collect_evidence(self, evidence_type: str, source: str,
                         data: dict, collector: str) -> str:
        """Collect and log evidence."""
        import hashlib
        import json

        evidence_id = f"EVD-{len(self.evidence_chain) + 1}"

        # Create hash of evidence for integrity
        evidence_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()

        self.evidence_chain.append({
            "id": evidence_id,
            "type": evidence_type,
            "source": source,
            "data": data,
            "hash": evidence_hash,
            "collector": collector,
            "timestamp": datetime.utcnow().isoformat(),
            "chain_of_custody": [
                {
                    "action": "collected",
                    "by": collector,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
        })

        return evidence_id

    def verify_evidence_integrity(self, evidence_id: str) -> dict:
        """Verify evidence hasn't been tampered with."""
        import hashlib
        import json

        for evidence in self.evidence_chain:
            if evidence["id"] == evidence_id:
                current_hash = hashlib.sha256(
                    json.dumps(evidence["data"], sort_keys=True).encode()
                ).hexdigest()

                return {
                    "verified": current_hash == evidence["hash"],
                    "original_hash": evidence["hash"],
                    "current_hash": current_hash,
                }

        return {"verified": False, "reason": "evidence_not_found"}

    def transfer_custody(self, evidence_id: str, from_person: str,
                         to_person: str, reason: str):
        """Transfer evidence custody."""
        for evidence in self.evidence_chain:
            if evidence["id"] == evidence_id:
                evidence["chain_of_custody"].append({
                    "action": "transferred",
                    "from": from_person,
                    "to": to_person,
                    "reason": reason,
                    "timestamp": datetime.utcnow().isoformat(),
                })
                return True
        return False
```

**Related Terms**: Chain of Custody, Evidence, Investigation

---

### Indicator of Compromise (IoC)

**Definition**: Technical artifacts or clues that indicate a system has been compromised or a security incident has occurred.

**Example**:
```python
class IoCManager:
    """Manage Indicators of Compromise."""

    def __init__(self):
        self.iocs = {
            "ip_addresses": set(),
            "domains": set(),
            "file_hashes": set(),
            "url_patterns": [],
            "email_addresses": set(),
        }

    def add_ioc(self, ioc_type: str, value: str, confidence: float,
                source: str, description: str = ""):
        """Add an indicator of compromise."""
        if ioc_type in self.iocs:
            if isinstance(self.iocs[ioc_type], set):
                self.iocs[ioc_type].add(value)
            else:
                self.iocs[ioc_type].append(value)

    def check_ioc(self, ioc_type: str, value: str) -> dict:
        """Check if a value matches known IoCs."""
        if ioc_type in self.iocs:
            if isinstance(self.iocs[ioc_type], set):
                return {
                    "matched": value in self.iocs[ioc_type],
                    "type": ioc_type,
                }
            else:
                # Pattern matching for URL patterns
                import re
                for pattern in self.iocs[ioc_type]:
                    if re.search(pattern, value):
                        return {"matched": True, "type": ioc_type, "pattern": pattern}
        return {"matched": False, "type": ioc_type}

    def get_ioc_summary(self) -> dict:
        """Get summary of all IoCs."""
        return {
            "ip_addresses": len(self.iocs["ip_addresses"]),
            "domains": len(self.iocs["domains"]),
            "file_hashes": len(self.iocs["file_hashes"]),
            "url_patterns": len(self.iocs["url_patterns"]),
            "email_addresses": len(self.iocs["email_addresses"]),
            "total": sum(
                len(v) if isinstance(v, set) else len(v)
                for v in self.iocs.values()
            ),
        }

# Usage
ioc_manager = IoCManager()
ioc_manager.add_ioc("ip_addresses", "192.168.1.100", 0.9, "threat_intel", "Known C2 server")
ioc_manager.add_ioc("domains", "malware.example.com", 0.85, "threat_intel")
result = ioc_manager.check_ioc("ip_addresses", "192.168.1.100")
print(f"IoC matched: {result['matched']}")
```

**Related Terms**: Threat Intelligence, TTPs, Threat Hunting

---

### Incident Response

**Definition**: The organized approach to addressing and managing security incidents, including detection, containment, eradication, and recovery.

**Example**:
```python
class IncidentResponsePlan:
    def __init__(self):
        self.phases = {
            "preparation": {
                "description": "Prepare for incidents before they occur",
                "activities": [
                    "Develop IR plan",
                    "Train team",
                    "Set up tools",
                ],
            },
            "detection_analysis": {
                "description": "Identify and analyze incidents",
                "activities": [
                    "Monitor alerts",
                    "Validate incidents",
                    "Assess scope",
                ],
            },
            "containment": {
                "description": "Limit incident damage",
                "activities": [
                    "Isolate systems",
                    "Preserve evidence",
                    "Block threats",
                ],
            },
            "eradication": {
                "description": "Remove threat from environment",
                "activities": [
                    "Remove malware",
                    "Patch vulnerabilities",
                    "Reset credentials",
                ],
            },
            "recovery": {
                "description": "Restore systems to normal",
                "activities": [
                    "Restore from backups",
                    "Verify functionality",
                    "Monitor for recurrence",
                ],
            },
            "post_mortem": {
                "description": "Learn from the incident",
                "activities": [
                    "Conduct review",
                    "Document lessons",
                    "Update procedures",
                ],
            },
        }

    def get_phase_activities(self, phase: str) -> list:
        """Get activities for a phase."""
        return self.phases.get(phase, {}).get("activities", [])

    def generate_checklist(self) -> dict:
        """Generate incident response checklist."""
        checklist = {}
        for phase, details in self.phases.items():
            checklist[phase] = {
                "description": details["description"],
                "tasks": [
                    {"activity": a, "completed": False}
                    for a in details["activities"]
                ],
            }
        return checklist
```

**Related Terms**: IR Plan, NIST, SANS

---

### Log Aggregation

**Definition**: The process of collecting and centralizing logs from multiple sources for analysis and monitoring.

**Example**:
```python
class LogAggregator:
    """Aggregate logs from multiple sources."""

    def __init__(self):
        self.sources = {}
        self.aggregated_logs = []

    def add_source(self, name: str, source_type: str, config: dict):
        """Add a log source."""
        self.sources[name] = {
            "type": source_type,
            "config": config,
            "status": "active",
        }

    def ingest_log(self, source: str, log_entry: dict):
        """Ingest a log entry from a source."""
        log_entry["_source"] = source
        log_entry["_ingested_at"] = datetime.utcnow().isoformat()
        self.aggregated_logs.append(log_entry)

    def query_logs(self, time_range: dict = None,
                   source: str = None,
                   level: str = None) -> list:
        """Query aggregated logs."""
        results = self.aggregated_logs

        if source:
            results = [l for l in results if l.get("_source") == source]

        if level:
            results = [l for l in results if l.get("level") == level]

        return results

    def get_statistics(self) -> dict:
        """Get log ingestion statistics."""
        source_counts = {}
        for log in self.aggregated_logs:
            source = log.get("_source", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1

        return {
            "total_logs": len(self.aggregated_logs),
            "by_source": source_counts,
            "sources": len(self.sources),
        }
```

**Related Terms**: SIEM, Centralized Logging, Log Management

---

### MITRE ATT&CK

**Definition**: A globally accessible knowledge base of adversary tactics and techniques based on real-world observations.

**Example**:
```python
# MITRE ATT&CK tactics relevant to AI systems
mitre_ai_tactics = {
    "initial_access": {
        "techniques": [
            "T1190 - Exploit Public-Facing Application",
            "T1133 - External Remote Services",
        ],
        "ai_specific": [
            "Prompt injection to gain initial access",
            "Exploiting AI API vulnerabilities",
        ],
    },
    "execution": {
        "techniques": [
            "T1059 - Command and Scripting Interpreter",
        ],
        "ai_specific": [
            "Code execution via AI-generated code",
            "Exploiting AI plugin vulnerabilities",
        ],
    },
    "persistence": {
        "techniques": [
            "T1078 - Valid Accounts",
        ],
        "ai_specific": [
            "Backdoor in AI model",
            "Persistent prompt injection",
        ],
    },
    "exfiltration": {
        "techniques": [
            "T1041 - Exfiltration Over C2 Channel",
        ],
        "ai_specific": [
            "Model extraction via API",
            "Data exfiltration through AI outputs",
        ],
    },
}

def map_attack_to_mitre(attack_type: str) -> dict:
    """Map AI attack to MITRE ATT&CK framework."""
    for tactic, details in mitre_ai_tactics.items():
        if attack_type.lower() in [t.lower() for t in details.get("ai_specific", [])]:
            return {
                "tactic": tactic,
                "techniques": details["techniques"],
            }
    return {"tactic": "unknown", "techniques": []}
```

**Related Terms**: Threat Framework, Tactics, Techniques

---

### Post-Mortem

**Definition**: A blameless review conducted after an incident to understand what happened, why, and how to prevent recurrence.

**Example**:
```python
class PostMortem:
    """Incident post-mortem documentation."""

    def __init__(self, incident_id: str, title: str):
        self.incident_id = incident_id
        self.title = title
        self.sections = {
            "summary": "",
            "timeline": [],
            "root_cause": "",
            "impact": {},
            "what_went_well": [],
            "what_went_wrong": [],
            "action_items": [],
            "lessons_learned": [],
        }

    def add_timeline_entry(self, timestamp: str, event: str,
                          actor: str = "system"):
        """Add entry to incident timeline."""
        self.sections["timeline"].append({
            "timestamp": timestamp,
            "event": event,
            "actor": actor,
        })

    def add_action_item(self, action: str, owner: str,
                       due_date: str, priority: str):
        """Add a follow-up action item."""
        self.sections["action_items"].append({
            "action": action,
            "owner": owner,
            "due_date": due_date,
            "priority": priority,
            "status": "open",
        })

    def generate_report(self) -> dict:
        """Generate post-mortem report."""
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "sections": self.sections,
            "generated_at": datetime.utcnow().isoformat(),
        }

# Usage
post_mortem = PostMortem("INC-001", "API Security Incident")
post_mortem.add_timeline_entry("2024-01-01T10:00:00Z", "Incident detected")
post_mortem.add_timeline_entry("2024-01-01T10:30:00Z", "Investigation started")
post_mortem.add_action_item(
    "Implement rate limiting",
    "Engineering Team",
    "2024-01-15",
    "high"
)
report = post_mortem.generate_report()
```

**Related Terms**: Root Cause Analysis, Lessons Learned, Action Items

---

### Root Cause Analysis (RCA)

**Definition**: The process of identifying the fundamental reason for an incident or problem.

**Example**:
```python
class RootCauseAnalysis:
    """Root cause analysis methodology."""

    def __init__(self):
        self.findings = []
        self.root_causes = []

    def add_finding(self, category: str, description: str,
                   evidence: list):
        """Add a finding from the investigation."""
        self.findings.append({
            "category": category,
            "description": description,
            "evidence": evidence,
        })

    def identify_root_causes(self) -> list:
        """Identify root causes from findings."""
        # Group findings by category
        categories = {}
        for finding in self.findings:
            cat = finding["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(finding)

        # Analyze each category
        for cat, findings in categories.items():
            if len(findings) >= 2:  # Multiple related findings
                self.root_causes.append({
                    "category": cat,
                    "description": f"Systemic issue in {cat}",
                    "findings_count": len(findings),
                })

        return self.root_causes

    def generate_5_whys(self, problem: str) -> list:
        """Generate 5 Whys analysis."""
        # Simplified - in practice would be interactive
        return [
            {"why": 1, "question": f"Why did {problem} happen?", "answer": "Investigation needed"},
            {"why": 2, "question": "Why did that happen?", "answer": "Investigation needed"},
            {"why": 3, "question": "Why did that happen?", "answer": "Investigation needed"},
            {"why": 4, "question": "Why did that happen?", "answer": "Investigation needed"},
            {"why": 5, "question": "Why did that happen?", "answer": "Root cause identified"},
        ]
```

**Related Terms**: 5 Whys, Fishbone Diagram, Problem Analysis

---

### SIEM (Security Information and Event Management)

**Definition**: A system that aggregates and analyzes log data from across an organization's infrastructure to detect security threats.

**Example**:
```python
class SIEMSystem:
    """Simplified SIEM system."""

    def __init__(self):
        self.log_sources = []
        self.correlation_rules = []
        self.alerts = []

    def add_log_source(self, name: str, source_type: str):
        """Add a log source."""
        self.log_sources.append({
            "name": name,
            "type": source_type,
            "status": "active",
        })

    def add_correlation_rule(self, name: str, conditions: dict,
                            alert_severity: str):
        """Add a correlation rule."""
        self.correlation_rules.append({
            "name": name,
            "conditions": conditions,
            "severity": alert_severity,
        })

    def ingest_logs(self, logs: list):
        """Ingest and correlate logs."""
        for log in logs:
            # Check against correlation rules
            for rule in self.correlation_rules:
                if self._match_rule(log, rule):
                    self.alerts.append({
                        "rule": rule["name"],
                        "severity": rule["severity"],
                        "log": log,
                        "timestamp": datetime.utcnow(),
                    })

    def _match_rule(self, log: dict, rule: dict) -> bool:
        """Check if log matches correlation rule."""
        # Simplified rule matching
        return False

    def get_alerts(self, severity: str = None) -> list:
        """Get alerts, optionally filtered by severity."""
        if severity:
            return [a for a in self.alerts if a["severity"] == severity]
        return self.alerts
```

**Related Terms**: Log Management, Correlation, Alerting

---

### Threat Hunting

**Definition**: The proactive process of searching for threats in an environment, rather than waiting for alerts.

**Example**:
```python
class ThreatHunter:
    """Proactive threat hunting."""

    def __init__(self):
        self.hypotheses = []
        self.findings = []

    def create_hypothesis(self, hypothesis: str, data_sources: list,
                         search_queries: list):
        """Create a threat hunting hypothesis."""
        self.hypotheses.append({
            "hypothesis": hypothesis,
            "data_sources": data_sources,
            "queries": search_queries,
            "status": "active",
            "created_at": datetime.utcnow(),
        })

    def execute_hunt(self, hypothesis_index: int) -> dict:
        """Execute a threat hunt."""
        if hypothesis_index >= len(self.hypotheses):
            return {"error": "Invalid hypothesis"}

        hypothesis = self.hypotheses[hypothesis_index]

        # Execute queries (simplified)
        results = []
        for query in hypothesis["queries"]:
            # Would execute actual queries against log data
            results.append({"query": query, "matches": 0})

        hunt_result = {
            "hypothesis": hypothesis["hypothesis"],
            "results": results,
            "findings": [],
            "completed_at": datetime.utcnow(),
        }

        self.findings.append(hunt_result)
        return hunt_result

    def get_hunt_statistics(self) -> dict:
        """Get threat hunting statistics."""
        return {
            "total_hypotheses": len(self.hypotheses),
            "active_hunts": sum(1 for h in self.hypotheses if h["status"] == "active"),
            "completed_hunts": len(self.findings),
            "findings_count": sum(len(f["findings"]) for f in self.findings),
        }
```

**Related Terms**: Proactive Security, Hypothesis-Driven, Threat Intelligence

---

*Part of the [AI Security Lecture Series](README.md). See also: [Lecture 10: Security Monitoring](10-security-monitoring-lecture.md)*
