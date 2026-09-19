"""
02 Content Moderation: Best Practices
"""

from ._types import *

BEST_PRACTICES = {
    "Architecture": [
        "Use multiple independent moderators for different content types",
        "Implement a pipeline pattern where each stage filters specific content",
        "Support both rule-based and ML-based detection",
        "Design for graceful degradation - if one moderator fails, others continue",
    ],
    "Severity & Escalation": [
        "Define clear severity levels with documented thresholds",
        "Implement automatic escalation for high-severity content",
        "Maintain a human-in-the-loop review queue for edge cases",
        "Track false positive rates to tune thresholds",
    ],
    "Custom Policies": [
        "Make policies configurable without code changes",
        "Support exceptions and context-aware rules",
        "Version control policy definitions",
        "A/B test policy changes before full rollout",
    ],
    "User Experience": [
        "Provide clear, non-judgmental explanations for content removal",
        "Offer appeal mechanisms for false positives",
        "Include crisis resources for self-harm content",
        "Respect context - educational/medical discussions may use strong language",
    ],
}


def print_best_practices():
    """Print the best practices reference."""
    print("\n" + "=" * 72)
    print("CONTENT MODERATION BEST PRACTICES")
    print("=" * 72)

    for category, practices in BEST_PRACTICES.items():
        print(f"\n  {category}:")
        for i, practice in enumerate(practices, 1):
            print(f"    {i}. {practice}")


# =============================================================================
# Main Entry Point
# =============================================================================

