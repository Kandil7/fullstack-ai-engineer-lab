"""
05 Data Privacy: Demos
"""

from ._types import *

def demo_pii_detection():
    """Demonstrate PII detection."""
    print("\n" + "=" * 72)
    print("DEMO 1: PII Detection")
    print("=" * 72)

    detector = PIIDetector()

    test_texts = [
        "Contact John Doe at john.doe@example.com or call (555) 123-4567.",
        "Patient MRN: ABC123456, SSN: 123-45-6789, DOB: 01/15/1990.",
        "Card number: 4111111111111111, server IP: 192.168.1.100.",
        "Visit 123 Main Street, Springfield, IL 62701 for more info.",
        "This sentence has no personal information in it at all.",
    ]

    for i, text in enumerate(test_texts, 1):
        matches = detector.detect(text)
        print(f'\n  [{i}] "{text[:60]}{"..." if len(text) > 60 else ""}"')
        if matches:
            for m in matches:
                print(
                    f'      {m.pii_type.name}: "{m.value}" (conf: {m.confidence:.0%})'
                )
        else:
            print("      [OK] No PII detected")


def demo_anonymization():
    """Demonstrate anonymization techniques."""
    print("\n" + "=" * 72)
    print("DEMO 2: Data Anonymization")
    print("=" * 72)

    detector = PIIDetector()
    engine = AnonymizationEngine()

    text = "Email John at john@acme.com, SSN 123-45-6789, born 03/15/1985."
    matches = detector.detect(text)

    methods = [
        ("Masking", AnonymizationMethod.MASKING),
        ("Hashing", AnonymizationMethod.HASHING),
        ("Pseudonymization", AnonymizationMethod.PSEUDONYMIZATION),
        ("Generalization", AnonymizationMethod.GENERALIZATION),
        ("Suppression", AnonymizationMethod.SUPPRESSION),
    ]

    print(f'\n  Original: "{text}"')
    for method_name, method in methods:
        anonymized, ops = engine.anonymize(text, matches, method)
        print(f"\n  {method_name}:")
        print(f'    "{anonymized}"')
        if ops:
            for op in ops[:3]:
                print(f'    - {op.pii_type.name}: "{op.original}" -> "{op.anonymized}"')


def demo_differential_privacy():
    """Demonstrate differential privacy mechanisms."""
    print("\n" + "=" * 72)
    print("DEMO 3: Differential Privacy")
    print("=" * 72)

    dp = DifferentialPrivacy(epsilon=1.0)

    # Laplace mechanism
    true_value = 100.0
    print(f"\n  Laplace Mechanism (true value: {true_value}):")
    noisy_values = [dp.laplace_mechanism(true_value) for _ in range(5)]
    print(f"    Noisy values: {[f'{v:.2f}' for v in noisy_values]}")
    avg_error = sum(abs(v - true_value) for v in noisy_values) / len(noisy_values)
    print(f"    Average error: {avg_error:.2f}")

    # Gaussian mechanism
    print(f"\n  Gaussian Mechanism (true value: {true_value}):")
    gaussian_values = [dp.gaussian_mechanism(true_value) for _ in range(5)]
    print(f"    Noisy values: {[f'{v:.2f}' for v in gaussian_values]}")

    # Randomized response
    print(f"\n  Randomized Response (epsilon={dp.epsilon}):")
    true_answers = [True, True, False, True, False, True, True, True, False, True]
    reported = [dp.randomized_response(a) for a in true_answers]
    print(f"    True answers:    {true_answers}")
    print(f"    Reported answers: {reported}")
    true_rate = sum(true_answers) / len(true_answers)
    reported_rate = sum(reported) / len(reported)
    print(f"    True rate: {true_rate:.0%} | Reported rate: {reported_rate:.0%}")

    # Privacy report
    print(f"\n  Privacy Report:")
    report = dp.get_privacy_report()
    for key, value in report.items():
        print(f"    {key}: {value}")


def demo_data_masking():
    """Demonstrate data masking strategies."""
    print("\n" + "=" * 72)
    print("DEMO 4: Data Masking Strategies")
    print("=" * 72)

    masker = DataMasker()

    # Individual field masking
    test_cases = [
        ("john.doe@example.com", PIIType.EMAIL, "Partial mask"),
        ("(555) 123-4567", PIIType.PHONE, "Partial mask"),
        ("123-45-6789", PIIType.SSN, "Partial mask"),
        ("4111111111111111", PIIType.CREDIT_CARD, "Partial mask"),
        ("John Smith", PIIType.NAME, "Partial mask"),
        ("192.168.1.100", PIIType.IP_ADDRESS, "Partial mask"),
    ]

    for value, pii_type, description in test_cases:
        masked = masker.mask_field(value, pii_type, "partial")
        print(f'  {description:20s} | {pii_type.name:15s} | "{value}" -> "{masked}"')

    # Dataset masking
    print(f"\n  Dataset Masking:")
    dataset = [
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "phone": "555-0101",
            "age": 30,
        },
        {"name": "Bob Smith", "email": "bob@acme.com", "phone": "555-0202", "age": 25},
        {
            "name": "Carol White",
            "email": "carol@test.org",
            "phone": "555-0303",
            "age": 35,
        },
    ]

    field_configs = {
        "name": {"pii_type": PIIType.NAME, "strategy": "partial"},
        "email": {"pii_type": PIIType.EMAIL, "strategy": "partial"},
        "phone": {"pii_type": PIIType.PHONE, "strategy": "partial"},
    }

    masked_dataset = masker.mask_dataset(dataset, field_configs)
    for original, masked in zip(dataset, masked_dataset):
        print(f"  Original: {original}")
        print(f"  Masked:   {masked}")
        print()


def demo_gdpr_compliance():
    """Demonstrate GDPR compliance patterns."""
    print("\n" + "=" * 72)
    print("DEMO 5: GDPR Compliance")
    print("=" * 72)

    gdpr = GDPRCompliance()

    # Record consent
    print("\n  Consent Management:")
    gdpr.record_consent("user_001", ["marketing", "analytics"], True)
    gdpr.record_consent("user_002", ["marketing"], False)

    # Check consent
    print(
        f"  User 001 marketing consent: {gdpr.check_consent('user_001', 'marketing')}"
    )
    print(
        f"  User 002 marketing consent: {gdpr.check_consent('user_002', 'marketing')}"
    )
    print(
        f"  User 002 analytics consent: {gdpr.check_consent('user_002', 'analytics')}"
    )

    # Data minimization check
    print(f"\n  Data Minimization Check (purpose: newsletter):")
    fields = ["name", "email", "phone", "ssn", "credit_card", "address"]
    minimization = gdpr.data_minimization_check(fields, "newsletter")
    for field, necessary in minimization.items():
        status = "NECESSARY" if necessary else "UNNECESSARY"
        print(f"    {field}: {status}")

    # Right to erasure
    print(f"\n  Right to Erasure:")
    data_store = {
        "user_001": {
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "555-0101",
        },
        "user_002": {"name": "Bob", "email": "bob@example.com", "phone": "555-0202"},
    }
    erasure_result = gdpr.right_to_erasure("user_001", data_store)
    print(f"    Erased: {erasure_result['fields_erased']}")
    print(f"    Remaining users: {list(data_store.keys())}")

    # Processing report
    report = gdpr.get_processing_report()
    print(f"\n  Processing Report:")
    for key, value in report.items():
        if key != "recent_operations":
            print(f"    {key}: {value}")


def demo_privacy_preserving_collection():
    """Demonstrate privacy-preserving data collection."""
    print("\n" + "=" * 72)
    print("DEMO 6: Privacy-Preserving Collection")
    print("=" * 72)

    gdpr = GDPRCompliance()
    collector = PrivacyPreservingCollector(retention_days=30)

    # Record consent
    gdpr.record_consent("user_a", ["analytics", "newsletter"], True)
    gdpr.record_consent("user_b", ["analytics"], True)

    # Collect data
    print("\n  Data Collection:")
    result1 = collector.collect(
        "user_a",
        {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "page_views": 42,
        },
        "analytics",
        gdpr,
    )
    print(
        f"  User A: {result1['status']} | PII handled: {result1.get('pii_handled', [])}"
    )

    result2 = collector.collect(
        "user_b",
        {
            "name": "Bob Jones",
            "email": "bob@test.com",
            "page_views": 15,
        },
        "newsletter",
        gdpr,
    )
    print(f"  User B: {result2['status']} | Reason: {result2.get('reason', 'N/A')}")

    # Aggregate stats (without exposing individual data)
    print(f"\n  Privacy-Preserving Aggregation:")
    total_views = collector.aggregate_stats("page_views", "sum")
    avg_views = collector.aggregate_stats("page_views", "avg")
    count = collector.aggregate_stats("page_views", "count")
    print(f"    Total page views: {total_views}")
    print(f"    Average page views: {avg_views}")
    print(f"    User count: {count}")

    # Data portability
    print(f"\n  Data Portability Export:")
    export = gdpr.export_user_data("user_a", collector.data_store)
    print(f"    Fields exported: {list(export.get('personal_data', {}).keys())}")
    print(
        f"    Processing history entries: {len(export.get('processing_history', []))}"
    )


def demo_audit_logging():
    """Demonstrate privacy audit logging."""
    print("\n" + "=" * 72)
    print("DEMO 7: Privacy Audit Logging")
    print("=" * 72)

    logger_instance = PrivacyAuditLogger()

    # Simulate various operations
    operations = [
        PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_collection",
            pii_types=["EMAIL", "NAME"],
            data_hash="abc123",
            user_id="user_001",
            details="Collected email and name for newsletter",
        ),
        PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_anonymization",
            pii_types=["SSN", "CREDIT_CARD"],
            data_hash="def456",
            user_id="user_002",
            details="Anonymized SSN and credit card for analytics",
        ),
        PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_export",
            pii_types=[],
            data_hash="ghi789",
            user_id="user_001",
            details="GDPR data portability export",
        ),
        PrivacyAuditEntry(
            timestamp=time.time(),
            operation="data_deletion",
            pii_types=["EMAIL", "PHONE", "ADDRESS"],
            data_hash="jkl012",
            user_id="user_003",
            details="Right to erasure executed",
        ),
    ]

    for entry in operations:
        logger_instance.log(entry)

    # Query audit log
    print("\n  Audit Log Entries:")
    all_entries = logger_instance.query()
    for entry in all_entries:
        print(
            f"    [{entry.operation}] User: {entry.user_id or 'N/A'} | Types: {entry.pii_types}"
        )

    # Query by operation
    deletion_entries = logger_instance.query(operation="data_deletion")
    print(f"\n  Deletion operations: {len(deletion_entries)}")

    # Summary
    summary = logger_instance.get_summary()
    print(f"\n  Audit Summary:")
    for key, value in summary.items():
        print(f"    {key}: {value}")


# =============================================================================
# Section 10: Best Practices
# =============================================================================

