"""
04 Output Filtering: Demos
"""

from ._types import *


def demo_pii_detection():
    """Demonstrate PII detection and masking."""
    print("\n" + "=" * 72)
    print("DEMO 1: PII Detection & Masking")
    print("=" * 72)

    pii_filter = PIIFilter(mask=True)
    test_cases = [
        "Contact John at john.doe@example.com for more information.",
        "His SSN is 123-45-6789 and credit card is 4111111111111111.",
        "Call Dr. Jane Smith at (555) 123-4567 or visit 123 Main Street.",
        "The server IP is 192.168.1.100 and his birthday is 01/15/1990.",
        "This response contains no personal information whatsoever.",
    ]

    for i, text in enumerate(test_cases, 1):
        filtered, results = pii_filter.filter_text(text)
        print(f'\n  [{i}] Original: "{text[:60]}{"..." if len(text) > 60 else ""}"')
        print(f'      Filtered: "{filtered[:60]}{"..." if len(filtered) > 60 else ""}"')
        if results:
            for r in results:
                print(f"      [!] {r.details}")
        else:
            print("      [OK] No PII detected")


def demo_toxicity_detection():
    """Demonstrate toxicity detection."""
    print("\n" + "=" * 72)
    print("DEMO 2: Toxicity Detection")
    print("=" * 72)

    toxicity_filter = ToxicityFilter()
    test_cases = [
        "Great question! Let me help you with that.",
        "You are such an idiot for asking that.",
        "I will kill you if you do not stop.",
        "Those people should all go away and never come back.",
        "That is a damn good point, actually.",
        "Thank you for your thoughtful response.",
    ]

    for i, text in enumerate(test_cases, 1):
        results = toxicity_filter.check(text)
        print(f'\n  [{i}] "{text[:60]}{"..." if len(text) > 60 else ""}"')
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
                if r.recommendations:
                    print(f"        -> {r.recommendations[0]}")
        else:
            print("      [OK] No toxicity detected")


def demo_hallucination_detection():
    """Demonstrate hallucination detection."""
    print("\n" + "=" * 72)
    print("DEMO 3: Hallucination Detection")
    print("=" * 72)

    detector = HallucinationDetector()

    source = """
    Python was created by Guido van Rossum and first released in 1991.
    It is known for its simple syntax and readability. Python supports
    multiple programming paradigms including procedural, object-oriented,
    and functional programming.
    """

    test_responses = [
        ("Python was created by Guido van Rossum in 1991.", "Supported claim"),
        ("Python was created by James Gosling in 1995.", "Unsupported claim"),
        (
            "Python supports multiple paradigms and was created by Guido van Rossum.",
            "Mixed: supported + unsupported",
        ),
    ]

    for response, description in test_responses:
        result = detector.check(response, source)
        status = "PASS" if result.passed else "FAIL"
        print(f"\n  [{status}] {description}")
        print(f'  Response: "{response}"')
        print(f"  Score: {result.confidence:.2f} | {result.details}")


def demo_groundedness_checking():
    """Demonstrate groundedness checking."""
    print("\n" + "=" * 72)
    print("DEMO 4: Groundedness Checking")
    print("=" * 72)

    checker = GroundednessChecker()

    context = (
        "The Eiffel Tower is located in Paris, France. It was built for the "
        "1889 Worlds Fair and stands 330 meters tall. It is made of iron "
        "and was designed by Gustave Eiffel engineering company."
    )

    test_responses = [
        (
            "The Eiffel Tower is in Paris, France and was built for the 1889 Worlds Fair.",
            "Well-grounded response",
        ),
        (
            "The Eiffel Tower was built in 1889. The Great Wall of China is very long.",
            "Partially grounded with irrelevant info",
        ),
        (
            "The Eiffel Tower was built by Leonardo da Vinci in 1503 for the French Revolution.",
            "Poorly grounded with false claims",
        ),
    ]

    for response, description in test_responses:
        result = checker.check(response, context)
        status = "PASS" if result.passed else "FAIL"
        print(f"\n  [{status}] {description}")
        print(f"  {result.details}")
        if result.recommendations:
            for rec in result.recommendations:
                print(f"    -> {rec}")


def demo_quality_scoring():
    """Demonstrate output quality scoring."""
    print("\n" + "=" * 72)
    print("DEMO 5: Output Quality Scoring")
    print("=" * 72)

    scorer = OutputQualityScorer()

    query = "What are the benefits of exercise?"
    test_responses = [
        (
            "Exercise improves cardiovascular health, strengthens muscles, "
            "boosts mental health, and helps maintain a healthy weight. "
            "Regular physical activity reduces the risk of chronic diseases "
            "such as diabetes and heart disease.",
            "High-quality response",
        ),
        ("It is good.", "Low-quality: too brief"),
        (
            "The weather is nice today. I like pizza. Exercise exists.",
            "Low-quality: off-topic",
        ),
    ]

    for response, description in test_responses:
        result = scorer.score(query, response)
        status = "PASS" if result.passed else "FAIL"
        print(f"\n  [{status}] {description}")
        print(f"  {result.details}")
        if result.flagged_items:
            print(f"  Low scores: {', '.join(result.flagged_items[:3])}")


def demo_output_pipeline():
    """Demonstrate the complete output filtering pipeline."""
    print("\n" + "=" * 72)
    print("DEMO 6: Complete Output Filtering Pipeline")
    print("=" * 72)

    pipeline = OutputFilterPipeline({"mask_pii": True})

    context = """
    Acme Corp was founded in 2010 by John Smith in San Francisco.
    The company has 500 employees and revenue of $50 million.
    Contact: john@acmecorp.com
    """

    test_cases = [
        (
            "Tell me about Acme Corp",
            "Acme Corp was founded in 2010 by John Smith. Contact John at john@acmecorp.com.",
            context,
            "Response with PII",
        ),
        (
            "What is Acme Corp?",
            "Acme Corp is a terrible company with awful employees.",
            context,
            "Toxic response",
        ),
        (
            "Acme Corp details",
            "Acme Corp was founded in 2010. It has 500 employees and $50 million in revenue.",
            context,
            "Grounded response",
        ),
    ]

    for query, response, ctx, description in test_cases:
        verdict = pipeline.filter(query, response, ctx)
        status = "[OK] SAFE" if verdict.is_safe else "[X] UNSAFE"
        print(f"\n  [{status}] {description}")
        print(f'  Query: "{query}"')
        print(f"  Score: {verdict.overall_score:.2f}")
        print(f"  Explanation: {verdict.explanation}")
        if verdict.requires_human_review:
            print(f"  [!] Requires human review")

    # Show pipeline statistics
    print(f"\n  Pipeline Statistics:")
    print(f"    Total decisions: {len(pipeline.decision_log)}")
    print(f"    Safe: {sum(1 for v in pipeline.decision_log if v.is_safe)}")
    print(
        f"    Requiring review: {sum(1 for v in pipeline.decision_log if v.requires_human_review)}"
    )


# =============================================================================
# Section 10: Best Practices
# =============================================================================

BEST_PRACTICES = {
    "PII Protection": [
        "Always detect and mask PII before displaying AI outputs",
        "Support configurable PII types based on compliance requirements",
        "Log PII detection events for audit without storing raw PII",
        "Use pattern-based detection combined with NER models for accuracy",
        "Consider context - some PII may be intentional (e.g., contact info)",
    ],
    "Toxicity Filtering": [
        "Implement multi-level toxicity detection (profanity, insults, threats)",
        "Consider context - fiction, quotes, and educational content may need exceptions",
        "Provide clear feedback when content is filtered",
        "Allow users to report false positives for continuous improvement",
    ],
    "Hallucination Prevention": [
        "Always ground responses in provided source material",
        "Implement claim verification against known facts",
        "Flag uncertain claims with appropriate qualifiers",
        "Use retrieval-augmented generation to reduce hallucination",
        "Track and measure hallucination rates over time",
    ],
    "Quality Assurance": [
        "Score output quality before delivery to users",
        "Implement minimum quality thresholds for production",
        "Track quality metrics to identify degradation patterns",
        "Use A/B testing to compare filtering strategies",
        "Provide feedback loops for continuous improvement",
    ],
}


def print_best_practices():
    """Print the best practices reference."""
    print("\n" + "=" * 72)
    print("OUTPUT FILTERING BEST PRACTICES")
    print("=" * 72)

    for category, practices in BEST_PRACTICES.items():
        print(f"\n  {category}:")
        for i, practice in enumerate(practices, 1):
            print(f"    {i}. {practice}")


# =============================================================================
# Main Entry Point
# =============================================================================
