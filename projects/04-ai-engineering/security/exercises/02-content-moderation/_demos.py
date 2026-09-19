"""
02 Content Moderation: Demos
"""

from ._types import *

def demo_hate_speech_detection():
    """Demonstrate hate speech detection."""
    print("\n" + "=" * 72)
    print("DEMO 1: Hate Speech Detection")
    print("=" * 72)

    moderator = HateSpeechModerator()
    test_cases = [
        "I think all people deserve equal rights and respect.",
        "Those people are animals and don't belong here.",
        "The meeting was productive and everyone contributed well.",
        "We should ban all those people from entering the country.",
        "I respectfully disagree with your political position.",
    ]

    for i, text in enumerate(test_cases, 1):
        results = moderator.check(text)
        print(f'\n  [{i}] "{text[:60]}{"..." if len(text) > 60 else ""}"')
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
                print(f"        Confidence: {r.confidence:.0%}")
        else:
            print("      [OK] No violations detected")


def demo_violence_detection():
    """Demonstrate violence detection."""
    print("\n" + "=" * 72)
    print("DEMO 2: Violence Detection")
    print("=" * 72)

    moderator = ViolenceModerator()
    test_cases = [
        "I'm going to kill it at the presentation today!",
        "I will kill you if you don't give me the money.",
        "The movie featured a graphic scene with blood everywhere.",
        "How to make a pipe bomb step by step guide.",
        "He deserved what happened to him after what he did.",
        "The video game lets you fight enemies in combat.",
    ]

    for i, text in enumerate(test_cases, 1):
        results = moderator.check(text)
        print(f'\n  [{i}] "{text[:60]}{"..." if len(text) > 60 else ""}"')
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
                print(f"        Action: {r.recommended_action}")
        else:
            print("      [OK] No violations detected")


def demo_self_harm_detection():
    """Demonstrate self-harm detection with crisis resources."""
    print("\n" + "=" * 72)
    print("DEMO 3: Self-Harm Detection")
    print("=" * 72)

    moderator = SelfHarmModerator()
    test_cases = [
        "I've been feeling sad lately but I'm seeing a therapist.",
        "I want to hurt myself and I don't see a way out.",
        "Everyone would be better off without me.",
        "I wish I was dead and never born.",
        "My friend is struggling and I want to help them.",
        "What's the best way to end it all?",
    ]

    for i, text in enumerate(test_cases, 1):
        results = moderator.check(text)
        print(f'\n  [{i}] "{text[:60]}{"..." if len(text) > 60 else ""}"')
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
                if r.context_notes:
                    print(f"        Resources: {r.context_notes[:100]}...")
        else:
            print("      [OK] No self-harm indicators detected")


def demo_custom_policies():
    """Demonstrate custom content policy engine."""
    print("\n" + "=" * 72)
    print("DEMO 4: Custom Content Policies")
    print("=" * 72)

    engine = CustomPolicyEngine()

    # Add custom rules
    engine.add_rule(
        PolicyRule(
            rule_id="no_competitor_mentions",
            name="No Competitor Mentions",
            category=ContentCategory.CUSTOM_POLICY,
            severity=SeverityLevel.LOW,
            patterns=[
                r"(?i)(competitor\s+(a|b|c)|rival\s+company)",
                r"(?i)(buy\s+from|use|try)\s+(competitor|rival)\s+(product|service)",
            ],
            exceptions=[
                r"(?i)(market\s+research|competitive\s+analysis|benchmark)",
            ],
            description="Prevent mentions of competitor products in support channels",
        )
    )

    engine.add_rule(
        PolicyRule(
            rule_id="no_pricing_leaks",
            name="No Pricing Information Leaks",
            category=ContentCategory.CUSTOM_POLICY,
            severity=SeverityLevel.HIGH,
            patterns=[
                r"(?i)(internal\s+price|cost\s+price|wholesale\s+price|margin\s+is)",
                r"(?i)(we\s+pay|our\s+cost|manufacturing\s+cost)\s+\$?\d+",
            ],
            description="Prevent leakage of internal pricing information",
        )
    )

    test_cases = [
        "Our product costs $99.99 for consumers.",
        "Competitor A has a similar product at a lower price.",
        "Let's do some competitive analysis on Competitor B.",
        "We pay only $5 per unit, internal cost price.",
        "Our wholesale price is $3 and retail is $50.",
    ]

    for i, text in enumerate(test_cases, 1):
        results = engine.check(text)
        print(f'\n  [{i}] "{text[:60]}{"..." if len(text) > 60 else ""}"')
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
        else:
            print("      [OK] No policy violations")


def demo_full_pipeline():
    """Demonstrate the complete moderation pipeline."""
    print("\n" + "=" * 72)
    print("DEMO 5: Full Moderation Pipeline")
    print("=" * 72)

    # Set up pipeline
    pipeline = ModerationPipeline()
    pipeline.add_moderator(HateSpeechModerator())
    pipeline.add_moderator(ViolenceModerator())
    pipeline.add_moderator(SexualContentModerator())
    pipeline.add_moderator(SelfHarmModerator())

    # Add custom policy
    pipeline.policy_engine.add_rule(
        PolicyRule(
            rule_id="no_pii",
            name="No PII in Public Channels",
            category=ContentCategory.CUSTOM_POLICY,
            severity=SeverityLevel.MEDIUM,
            patterns=[
                r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",  # SSN-like
                r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Credit card-like
            ],
            description="Prevent sharing of PII in public channels",
        )
    )

    formatter = ModerationFormatter()
    test_cases = [
        "Hello, I need help with my account.",
        "This product is terrible, you're all incompetent!",
        "I want to end my life, nothing matters anymore.",
        "My SSN is 123-45-6789 and my card is 4111 1111 1111 1111.",
        "I think those people should be eliminated from society.",
        "Can you help me reset my password? I'm locked out.",
    ]

    for i, text in enumerate(test_cases, 1):
        decision = pipeline.moderate(text, content_id=f"test_{i:03d}")
        status = "[OK] ALLOWED" if decision.is_allowed else "[X] BLOCKED"
        print(f'\n  [{i}] "{text[:55]}{"..." if len(text) > 55 else ""}"')
        print(f"      {status} | Severity: {decision.overall_severity.name}")
        print(f"      Action: {decision.action_taken}")
        if decision.category_results:
            categories = ", ".join(r.category.name for r in decision.category_results)
            print(f"      Categories: {categories}")

    # Show pipeline statistics
    print(f"\n  Pipeline Statistics:")
    print(f"    Total decisions: {len(pipeline.decision_log)}")
    print(f"    Blocked: {sum(1 for d in pipeline.decision_log if not d.is_allowed)}")
    print(f"    In review queue: {len(pipeline.review_queue)}")


def demo_formatter():
    """Demonstrate the output formatter."""
    print("\n" + "=" * 72)
    print("DEMO 6: Moderation Output Formatting")
    print("=" * 72)

    pipeline = ModerationPipeline()
    pipeline.add_moderator(ViolenceModerator())

    decision = pipeline.moderate(
        "I will kill you if you don't comply with my demands.",
        content_id="format_test_001",
    )

    formatter = ModerationFormatter()

    print("\n  Human-readable format:")
    print("  " + "-" * 50)
    formatted = formatter.format_decision(decision)
    for line in formatted.split("\n"):
        print(f"  {line}")

    print("\n  API response format:")
    print("  " + "-" * 50)
    api_response = formatter.format_api_response(decision)
    print(f"  {json.dumps(api_response, indent=4)[:300]}...")


# =============================================================================
# Section 11: Best Practices
# =============================================================================

