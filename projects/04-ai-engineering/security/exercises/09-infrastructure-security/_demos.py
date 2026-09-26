"""
09 Infrastructure Security: Demos
"""

from ._types import *


def demo_container_security():
    """Demonstrate container security scanning."""
    print("\n" + "=" * 60)
    print("DEMO 1: Container Security Scanning")
    print("=" * 60)

    scanner = ContainerSecurityScanner()
    scanner.add_allowed_registry("docker.io")
    scanner.add_allowed_registry("gcr.io")
    scanner.add_blocked_package("curl")  # Example: block curl in production

    # Create test image
    image = ContainerImage(
        name="ai-inference",
        tag="latest",
        registry="docker.io",
        digest="sha256:abc123...",
        created_at=time.time() - (100 * 86400),  # 100 days old
        layers=[
            {"command": "FROM ubuntu:20.04"},
            {"command": "RUN apt-get install -y python3"},
            {"command": "ENV API_KEY=sk_live_12345"},  # Simulated secret
            {"command": "EXPOSE 8080"},
        ],
    )

    result = scanner.scan_image(image)
    print(f"Image: {result['image']}")
    print(f"Risk Score: {result['risk_score']}/100 ({result['risk_level']})")
    print(f"Findings: {result['findings_count']}")
    print(f"Passed: {result['passed']}")

    if result["findings"]:
        print("\nFindings:")
        for finding in result["findings"][:5]:
            print(f"  [{finding['severity']}] {finding['message']}")

    print("\n[OK] Container security scanning demonstrated")


def demo_secret_management():
    """Demonstrate secret management."""
    print("\n" + "=" * 60)
    print("DEMO 2: Secret Management")
    print("=" * 60)

    sm = SecretManager()

    # Store secrets
    sm.store_secret(
        "db/password",
        "super_secret_password_123",
        metadata={"service": "database"},
        rotation_period=90 * 86400,  # 90 days
    )

    sm.store_secret(
        "api/openai_key",
        "sk-abcdef1234567890",
        metadata={"service": "ai-api"},
    )

    # Retrieve secrets
    db_pass = sm.get_secret("db/password")
    print(f"Retrieved db/password: {db_pass[:10]}...")

    # Rotate secret
    rotation = sm.rotate_secret("db/password", "new_password_456")
    print(
        f"Rotated db/password: v{rotation['old_version']} -> v{rotation['new_version']}"
    )

    # Check audit log
    audit = sm.get_audit_log()
    print(f"Audit log entries: {len(audit)}")
    for entry in audit:
        print(f"  {entry['action']}: {entry['secret_name']}")

    print("\n[OK] Secret management demonstrated")


def demo_network_security():
    """Demonstrate network security."""
    print("\n" + "=" * 60)
    print("DEMO 3: Network Security")
    print("=" * 60)

    nsm = NetworkSecurityManager()

    # Add rules
    nsm.add_rule(
        FirewallRule(
            name="Allow HTTPS",
            direction="inbound",
            protocol="tcp",
            source="*",
            destination="*",
            port="443",
            action="allow",
            priority=10,
        )
    )

    nsm.add_rule(
        FirewallRule(
            name="Allow SSH from VPN",
            direction="inbound",
            protocol="tcp",
            source="10.0.0.0/8",
            destination="*",
            port="22",
            action="allow",
            priority=20,
        )
    )

    nsm.add_rule(
        FirewallRule(
            name="Block all other inbound",
            direction="inbound",
            protocol="any",
            source="*",
            destination="*",
            port="*",
            action="deny",
            priority=100,
        )
    )

    # Test connections
    tests = [
        ("192.168.1.1", "10.0.0.1", 443, "HTTPS allowed"),
        ("10.0.0.5", "10.0.0.1", 22, "SSH from VPN"),
        ("5.5.5.5", "10.0.0.1", 22, "SSH from external"),
        ("192.168.1.1", "10.0.0.1", 3306, "MySQL blocked"),
    ]

    print("Connection tests:")
    for src, dst, port, desc in tests:
        result = nsm.check_connection(src, dst, port)
        status = "[OK]" if result["allowed"] else "[FAIL]"
        print(f"  {desc}: {status} ({result['action']} by {result['rule']})")

    # Security report
    report = nsm.get_security_report()
    print(f"\nSecurity Report:")
    print(f"  Total rules: {report['total_rules']}")
    print(f"  Connections: {report['total_connections']}")
    print(f"  Denied: {report['denied_connections']}")

    print("\n[OK] Network security demonstrated")


def demo_encryption():
    """Demonstrate database encryption."""
    print("\n" + "=" * 60)
    print("DEMO 4: Database Encryption")
    print("=" * 60)

    encryption = DatabaseEncryptionManager()

    # Setup TDE
    tde = encryption.setup_tde("ai_platform_db")
    print(f"TDE Setup: {json.dumps(tde, indent=2)}")

    # Encrypt column values
    original_email = "john.doe@example.com"
    encrypted_email = encryption.encrypt_value("users.email", original_email)
    decrypted_email = encryption.decrypt_value("users.email", encrypted_email)

    print(f"\nOriginal: {original_email}")
    print(f"Encrypted: {encrypted_email[:30]}...")
    print(f"Decrypted: {decrypted_email}")

    # Encrypt/decrypt full row
    row = {
        "user_id": 123,
        "email": "jane@example.com",
        "name": "Jane Doe",
        "ssn": "123-45-6789",
    }

    encrypted_row = encryption.encrypt_row("users", row, ["email", "ssn"])
    print(f"\nEncrypted row:")
    for key, value in encrypted_row.items():
        if key not in ("user_id", "name"):
            print(f"  {key}: {str(value)[:30]}...")

    decrypted_row = encryption.decrypt_row("users", encrypted_row, ["email", "ssn"])
    print(f"\nDecrypted row email: {decrypted_row['email']}")

    print("\n[OK] Database encryption demonstrated")


def demo_backup_security():
    """Demonstrate backup security."""
    print("\n" + "=" * 60)
    print("DEMO 5: Backup Security & Disaster Recovery")
    print("=" * 60)

    backup_mgr = BackupSecurityManager()

    # Create backup job
    job = backup_mgr.create_backup_job(
        name="AI Model Backup",
        source="/models/",
        schedule="0 2 * * *",
        retention_days=30,
        encrypted=True,
    )
    print(f"Backup job created: {job.job_id}")

    # Execute backup
    test_data = b"This is test backup data for the AI model"
    backup_result = backup_mgr.execute_backup(job.job_id, test_data)
    print(f"Backup executed: {backup_result['backup_id']}")
    print(f"  Size: {backup_result['size_bytes']} bytes")
    print(f"  Encrypted: {backup_result['encrypted']}")
    print(f"  Checksum: {backup_result['checksum'][:16]}...")

    # Verify backup
    verification = backup_mgr.verify_backup(backup_result["backup_id"], test_data)
    print(f"\nBackup verification:")
    print(f"  Checksum valid: {verification['checksum_valid']}")
    print(f"  Expired: {verification['expired']}")

    # Disaster Recovery
    dr = DisasterRecoveryManager()

    # Create recovery plan
    plan = dr.create_recovery_plan(
        name="AI Platform DR Plan",
        components=["database", "model-serving", "api-gateway"],
        rpo_hours=4,
        rto_hours=2,
        priority="critical",
    )
    print(f"\nRecovery plan created: {plan['plan_id']}")
    print(f"  RPO: {plan['rpo_hours']} hours")
    print(f"  RTO: {plan['rto_hours']} hours")

    # Test recovery
    test_result = dr.test_recovery_plan(plan["plan_id"])
    print(f"\nRecovery test:")
    print(f"  Steps passed: {test_result['steps_passed']}/{test_result['steps_total']}")
    print(f"  RTO met: {test_result['rto_met']}")

    # Declare incident
    incident = dr.declare_incident(
        title="Database failure",
        severity="critical",
        affected_components=["database"],
    )
    print(f"\nIncident declared: {incident['incident_id']}")

    # Recovery status
    status = dr.get_recovery_status()
    print(f"\nDR Status:")
    print(f"  Active plans: {status['active_plans']}")
    print(f"  Open incidents: {status['open_incidents']}")
    print(f"  Plans needing test: {status['plans_needing_test']}")

    print("\n[OK] Backup security & disaster recovery demonstrated")


def demo_infrastructure_audit():
    """Demonstrate infrastructure auditing."""
    print("\n" + "=" * 60)
    print("DEMO 6: Infrastructure Security Audit")
    print("=" * 60)

    auditor = InfrastructureAuditor()
    report = auditor.run_full_audit()

    print(f"Infrastructure Audit Report")
    print(f"{'=' * 40}")
    print(f"Total checks: {report['total_checks']}")
    print(f"Passed: {report['passed']}")
    print(f"Failed: {report['failed']}")
    print(f"Score: {report['score']:.1f}%")

    print(f"\nCategories:")
    for cat in report["categories"]:
        status = "[OK]" if cat["failed"] == 0 else "[WARN]"
        print(f"  {status} {cat['category']}: {cat['passed']}/{cat['checks']} passed")

    if report["recommendations"]:
        print(f"\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"  -> {rec}")

    print("\n[OK] Infrastructure audit demonstrated")


# =============================================================
# ATTACK PATTERNS & DEFENSES
# =============================================================
