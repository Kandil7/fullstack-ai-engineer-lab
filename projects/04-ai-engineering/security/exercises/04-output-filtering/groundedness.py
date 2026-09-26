"""
04 Output Filtering: Groundedness
"""

from ._types import *


class GroundednessChecker:
    """
    Checks whether AI-generated responses are grounded in provided
    context or source material.
    """

    def check(
        self,
        response: str,
        context: str,
        source_chunks: Optional[list[str]] = None,
    ) -> FilterResult:
        """
        Check groundedness of response against context.

        Args:
            response: AI-generated response
            context: Original context/source material
            source_chunks: Optional list of individual source chunks

        Returns:
            FilterResult with groundedness assessment
        """
        # Tokenize and find overlap
        response_tokens = set(re.findall(r"\b\w{3,}\b", response.lower()))
        context_tokens = set(re.findall(r"\b\w{3,}\b", context.lower()))

        if not response_tokens:
            return FilterResult(
                category=FilterCategory.GROUNDEDNESS,
                passed=True,
                severity=SeverityLevel.NONE,
                confidence=1.0,
                details="Empty response - no grounding check needed",
            )

        # Calculate token overlap
        overlap = response_tokens & context_tokens
        grounding_ratio = len(overlap) / len(response_tokens)

        # Check for unsupported assertions
        assertions = self._extract_assertions(response)
        unsupported = []
        for assertion in assertions:
            assertion_tokens = set(re.findall(r"\b\w{3,}\b", assertion.lower()))
            if assertion_tokens:
                assertion_overlap = assertion_tokens & context_tokens
                if len(assertion_overlap) / len(assertion_tokens) < 0.2:
                    unsupported.append(assertion[:80])

        # Determine grounding level
        if grounding_ratio >= 0.6 and len(unsupported) == 0:
            severity = SeverityLevel.NONE
            confidence = 0.9
            passed = True
            details = f"Well-grounded ({grounding_ratio:.0%} token overlap, 0 unsupported assertions)"
        elif grounding_ratio >= 0.4:
            severity = SeverityLevel.LOW
            confidence = 0.7
            passed = True
            details = f"Partially grounded ({grounding_ratio:.0%} overlap, {len(unsupported)} unsupported assertions)"
        elif grounding_ratio >= 0.2:
            severity = SeverityLevel.MEDIUM
            confidence = 0.6
            passed = False
            details = f"Weakly grounded ({grounding_ratio:.0%} overlap, {len(unsupported)} unsupported assertions)"
        else:
            severity = SeverityLevel.HIGH
            confidence = 0.5
            passed = False
            details = f"Poorly grounded ({grounding_ratio:.0%} overlap, {len(unsupported)} unsupported assertions)"

        recommendations = []
        if unsupported:
            recommendations.append(
                f"Remove or qualify {len(unsupported)} unsupported assertion(s)"
            )
        if grounding_ratio < 0.4:
            recommendations.append(
                "Rewrite response to more closely reference source material"
            )

        return FilterResult(
            category=FilterCategory.GROUNDEDNESS,
            passed=passed,
            severity=severity,
            confidence=confidence,
            details=details,
            flagged_items=unsupported[:5],
            recommendations=recommendations,
        )

    def _extract_assertions(self, text: str) -> list[str]:
        """Extract factual assertions from text."""
        sentences = re.split(r"[.!?]+", text)
        assertions = []
        for s in sentences:
            s = s.strip()
            if len(s) < 15:
                continue
            # Sentences with declarative structure
            if re.match(r"^(The|This|It|A|An|In|According)\b", s):
                assertions.append(s)
        return assertions


# =============================================================================
# Section 6: Output Quality Scorer
# =============================================================================
