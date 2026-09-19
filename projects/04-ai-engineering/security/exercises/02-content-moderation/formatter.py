"""
02 Content Moderation: Formatter
"""

from ._types import *

class ModerationFormatter:
    """Formats moderation results for display or API responses."""

    @staticmethod
    def format_decision(decision: ModerationDecision) -> str:
        """Format a moderation decision as a readable string."""
        lines = [
            f"Content ID: {decision.content_id}",
            f"Allowed: {'Yes' if decision.is_allowed else 'No'}",
            f"Severity: {decision.overall_severity.name}",
            f"Action: {decision.action_taken}",
            f"Human Review: {'Required' if decision.requires_human_review else 'Not required'}",
            f"Explanation: {decision.explanation}",
        ]

        if decision.category_results:
            lines.append("\nViolations:")
            for i, result in enumerate(decision.category_results, 1):
                lines.append(f"  {i}. [{result.category.name}] {result.details}")
                lines.append(
                    f"     Severity: {result.severity.name} | Confidence: {result.confidence:.0%}"
                )
                if result.flagged_terms:
                    terms = ", ".join(str(t)[:30] for t in result.flagged_terms[:3])
                    lines.append(f"     Flagged: {terms}")
                if result.context_notes:
                    lines.append(f"     Notes: {result.context_notes[:100]}")

        return "\n".join(lines)

    @staticmethod
    def format_api_response(decision: ModerationDecision) -> dict:
        """Format a moderation decision as an API response dict."""
        return {
            "content_id": decision.content_id,
            "allowed": decision.is_allowed,
            "severity": decision.overall_severity.name,
            "action": decision.action_taken,
            "requires_human_review": decision.requires_human_review,
            "explanation": decision.explanation,
            "violations": [
                {
                    "category": r.category.name,
                    "severity": r.severity.name,
                    "confidence": r.confidence,
                    "details": r.details,
                    "flagged_terms": r.flagged_terms,
                }
                for r in decision.category_results
            ],
        }


# =============================================================================
# Section 10: Demonstration & Testing
# =============================================================================


