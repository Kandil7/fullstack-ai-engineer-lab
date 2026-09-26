"""
02 Content Moderation: Pipeline
"""

from ._types import *
from .base_moderator import ContentModerator
from .policy_engine import CustomPolicyEngine


class ModerationPipeline:
    """
    Complete content moderation pipeline combining multiple moderators
    with configurable policies and human-in-the-loop review.
    """

    def __init__(self, policy_engine: Optional[CustomPolicyEngine] = None):
        self.moderators: list[ContentModerator] = []
        self.policy_engine = policy_engine or CustomPolicyEngine()
        self.review_queue: list[ModerationDecision] = []
        self.decision_log: list[ModerationDecision] = []
        self.human_review_threshold = SeverityLevel.MEDIUM

    def add_moderator(self, moderator: ContentModerator) -> None:
        """Register a content moderator with the pipeline."""
        self.moderators.append(moderator)
        logger.info(f"Added moderator: {moderator.__class__.__name__}")

    def moderate(
        self, text: str, content_id: Optional[str] = None
    ) -> ModerationDecision:
        """
        Run the full moderation pipeline on the given text.

        Args:
            text: The content to moderate
            content_id: Optional identifier for the content

        Returns:
            ModerationDecision with the final verdict
        """
        if not content_id:
            content_id = hashlib.sha256(text.encode()).hexdigest()[:12]

        all_results: list[ModerationResult] = []

        # Run all registered moderators
        for moderator in self.moderators:
            try:
                results = moderator.check(text)
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Moderator {moderator.__class__.__name__} failed: {e}")

        # Run custom policy engine
        policy_results = self.policy_engine.check(text)
        all_results.extend(policy_results)

        # Determine overall decision
        if not all_results:
            decision = ModerationDecision(
                content_id=content_id,
                is_allowed=True,
                overall_severity=SeverityLevel.NONE,
                category_results=[],
                explanation="No content policy violations detected",
                action_taken="allow",
            )
        else:
            max_severity = max((r.severity for r in all_results), key=lambda s: s.value)
            any_blocked = any(r.should_block for r in all_results)
            any_flagged = any(r.should_flag for r in all_results)
            requires_review = any(
                r.severity.value >= self.human_review_threshold.value
                for r in all_results
            )

            categories = ", ".join(r.category.name for r in all_results)
            explanation = (
                f"Detected {len(all_results)} violation(s) across categories: {categories}. "
                f"Max severity: {max_severity.name}"
            )

            if any_blocked:
                action = "block"
            elif any_flagged:
                action = "flag_for_review"
            else:
                action = "allow_with_monitoring"

            decision = ModerationDecision(
                content_id=content_id,
                is_allowed=not any_blocked,
                overall_severity=max_severity,
                category_results=all_results,
                requires_human_review=requires_review,
                explanation=explanation,
                action_taken=action,
            )

        # Log decision
        self.decision_log.append(decision)
        if decision.requires_human_review:
            self.review_queue.append(decision)
            logger.info(f"Content {content_id} queued for human review")

        return decision


# =============================================================================
# Section 9: Output Formatter
# =============================================================================
