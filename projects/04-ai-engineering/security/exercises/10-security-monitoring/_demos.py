"""
10 Security Monitoring: Demos
"""

from ._types import *

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
        print(f"  Event {i + 1}: {len(alerts)} alerts")

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
    if spike_result["is_anomaly"]:
        print(f"  Type: {spike_result.get('type')}")
        print(
            f"  Change ratio: {spike_result.get('change_ratio', spike_result.get('z_score'))}"
        )

    # Baseline summary
    summary = detector.get_baseline_summary()
    print(f"\nBaseline summary:")
    for metric, stats in summary.items():
        print(
            f"  {metric}: mean={stats['mean']}, std={stats['std']}, samples={stats['count']}"
        )

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
        phase = entry.get("phase", "update")
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

