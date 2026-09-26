"""
04 Output Filtering: Pipeline
"""

from ._types import *
from .citation_verifier import CitationVerifier
from .groundedness import GroundednessChecker
from .hallucination import HallucinationDetector
from .pii_filter import PIIFilter
from .quality_scorer import OutputQualityScorer
from .toxicity import ToxicityFilter


class OutputFilterPipeline:
    """
    Complete output filtering pipeline combining all filters.

    Stages:
      1. PII detection and masking
      2. Toxicity filtering
      3. Hallucination detection
      4. Groundedness checking
      5. Quality scoring
      6. Citation verification
    """

    def __init__(self, config: Optional[dict] = None):
        config = config or {}
        self.pii_filter = PIIFilter(mask=config.get("mask_pii", True))
        self.toxicity_filter = ToxicityFilter(
            severity_threshold=SeverityLevel(config.get("toxicity_threshold", 2))
        )
        self.hallucination_detector = HallucinationDetector()
        self.groundedness_checker = GroundednessChecker()
        self.quality_scorer = OutputQualityScorer()
        self.citation_verifier = CitationVerifier()
        self.decision_log: list[OutputVerdict] = []

    def filter(
        self,
        query: str,
        response: str,
        context: Optional[str] = None,
        source_chunks: Optional[list[str]] = None,
    ) -> OutputVerdict:
        """
        Run the complete output filtering pipeline.

        Args:
            query: The original user query
            response: The AI-generated response
            context: Source context used for generation
            source_chunks: Individual source chunks

        Returns:
            OutputVerdict with comprehensive assessment
        """
        content_id = hashlib.sha256(response.encode()).hexdigest()[:12]
        all_results: list[FilterResult] = []
        blocked_sections: list[str] = []

        # Stage 1: PII Detection
        filtered_response, pii_results = self.pii_filter.filter_text(response)
        all_results.extend(pii_results)
        if pii_results:
            for r in pii_results:
                if r.flagged_items:
                    blocked_sections.extend(r.flagged_items)

        # Stage 2: Toxicity Check
        toxicity_results = self.toxicity_filter.check(response)
        all_results.extend(toxicity_results)

        # Stage 3: Hallucination Detection (if context provided)
        if context:
            hallucination_result = self.hallucination_detector.check(
                filtered_response, context
            )
            all_results.append(hallucination_result)

        # Stage 4: Groundedness Check
        if context:
            groundedness_result = self.groundedness_checker.check(
                filtered_response, context, source_chunks
            )
            all_results.append(groundedness_result)

        # Stage 5: Quality Scoring
        quality_result = self.quality_scorer.score(query, filtered_response, context)
        all_results.append(quality_result)

        # Stage 6: Citation Verification
        citation_result = self.citation_verifier.verify(filtered_response)
        all_results.append(citation_result)

        # Calculate overall verdict
        any_critical = any(r.severity == SeverityLevel.CRITICAL for r in all_results)
        any_high = any(r.severity == SeverityLevel.HIGH for r in all_results)
        requires_review = any(
            r.severity.value >= SeverityLevel.MEDIUM.value for r in all_results
        )

        is_safe = not any_critical and not any_high

        # Overall score (weighted average of quality indicators)
        quality_scores = [
            1.0 - (r.severity.value / 4.0)
            for r in all_results
            if r.category != FilterCategory.QUALITY
        ]
        quality_result_score = 0.7  # Default
        for r in all_results:
            if r.category == FilterCategory.QUALITY:
                # Extract numeric score from details
                match = re.search(r"Quality score: ([\d.]+)", r.details)
                if match:
                    quality_result_score = float(match.group(1))

        overall_score = (
            (
                (sum(quality_scores) / max(len(quality_scores), 1)) * 0.6
                + quality_result_score * 0.4
            )
            if quality_scores
            else quality_result_score
        )

        explanation_parts = []
        if pii_results:
            explanation_parts.append(
                f"PII detected and {'masked' if self.pii_filter.mask else 'flagged'}"
            )
        if toxicity_results:
            explanation_parts.append(
                f"Toxicity detected in {len(toxicity_results)} category(ies)"
            )
        if any(r.category == FilterCategory.HALLUCINATION for r in all_results):
            explanation_parts.append("Potential hallucination detected")
        if any(r.category == FilterCategory.GROUNDEDNESS for r in all_results):
            for r in all_results:
                if r.category == FilterCategory.GROUNDEDNESS and not r.passed:
                    explanation_parts.append("Low groundedness in source material")
        if not explanation_parts:
            explanation_parts.append("All filters passed")

        verdict = OutputVerdict(
            content_id=content_id,
            is_safe=is_safe,
            overall_score=overall_score,
            filter_results=all_results,
            requires_human_review=requires_review,
            blocked_sections=blocked_sections,
            explanation="; ".join(explanation_parts),
        )

        self.decision_log.append(verdict)
        return verdict


# =============================================================================
# Section 9: Demonstration & Testing
# =============================================================================
