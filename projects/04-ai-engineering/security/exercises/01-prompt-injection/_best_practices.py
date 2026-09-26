"""
01 Prompt Injection: Best Practices
"""

from ._types import *

BEST_PRACTICES = {
    "Input Defense": [
        "Always sanitize user input before processing",
        "Use boundary markers to separate system and user content",
        "Implement input length limits to prevent overflow attacks",
        "Normalize Unicode to defeat homoglyph attacks",
        "Log all suspicious inputs for audit trails",
    ],
    "System Prompt Hardening": [
        "Include explicit refusal instructions for injection attempts",
        "Use role anchoring to prevent role manipulation",
        "Add instruction hierarchy to establish priority order",
        "Include input boundary markers in system prompt",
        "Avoid revealing system prompt contents under any circumstances",
    ],
    "Detection & Monitoring": [
        "Implement multiple detection layers (signature + heuristic)",
        "Track suspicious patterns across conversation turns",
        "Set escalation thresholds for repeated suspicious activity",
        "Use entropy analysis to detect structured payloads",
        "Monitor instruction-to-data ratio in user inputs",
    ],
    "Architecture": [
        "Never trust user input - treat it as untrusted data",
        "Apply principle of least privilege to LLM capabilities",
        "Implement rate limiting on API endpoints",
        "Use output validation before returning responses",
        "Separate sensitive operations from conversational flow",
    ],
}


def print_best_practices():
    """Print the best practices reference."""
    print("\n" + "=" * 72)
    print("BEST PRACTICES REFERENCE")
    print("=" * 72)

    for category, practices in BEST_PRACTICES.items():
        print(f"\n  {category}:")
        for i, practice in enumerate(practices, 1):
            print(f"    {i}. {practice}")


# =============================================================================
# Main Entry Point
# =============================================================================
