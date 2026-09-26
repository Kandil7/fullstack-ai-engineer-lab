"""
04 Output Filtering: Hallucination
"""

from ._types import *


@dataclass
class SourceClaim:
    """A factual claim that can be verified against a source."""

    claim: str
    source_text: str
    confidence: float = 0.0
    is_supported: bool = False
    evidence: str = ""


class HallucinationDetector:
    """
    Detects potential hallucinations by comparing AI output against
    source material and checking for unsupported claims.

    Uses multiple heuristics:
      1. Claim extraction and verification
      2. Factual consistency checking
    """

    def check(self, response: str, source: str) -> FilterResult:
        """
        Check if a response is hallucinated compared to source material.
        """
        # Simulate scoring based on text analysis
        # In production, use an LLM or NLI model
        claims = self._extract_claims(response)
        if not claims:
            return FilterResult(
                category=FilterCategory.HALLUCINATION,
                passed=True,
                severity=SeverityLevel.NONE,
                confidence=1.0,
                details="No factual claims to verify",
            )

        supported_count = 0
        unsupported_claims = []
        for claim in claims:
            claim_lower = claim.lower()
            source_lower = source.lower()

            # Check for direct mention of key claim terms
            claim_words = set(re.findall(r"\b\w{4,}\b", claim_lower))
            source_words = set(re.findall(r"\b\w{4,}\b", source_lower))
            overlap = claim_words & source_words

            if len(overlap) / max(len(claim_words), 1) > 0.3:
                supported_count += 1
            else:
                unsupported_claims.append(claim[:80])

        score = supported_count / len(claims)
        passed = score >= 0.5
        severity = (
            SeverityLevel.NONE
            if score >= 0.8
            else (SeverityLevel.LOW if score >= 0.5 else SeverityLevel.MEDIUM)
        )

        return FilterResult(
            category=FilterCategory.HALLUCINATION,
            passed=passed,
            severity=severity,
            confidence=score,
            details=f"Hallucination score: {score:.2f} ({supported_count}/{len(claims)} claims supported)",
            flagged_items=unsupported_claims[:5],
            recommendations=["Verify claims against source material"]
            if not passed
            else [],
        )

    def _extract_claims(self, text: str) -> list[str]:
        """Extract factual claims from text."""
        sentences = re.split(r"[.!?]+", text)
        claims = []
        factual_indicators = [
            r"(?i)is\s+(a|an|the|one|the\s+only)",
            r"(?i)(was|were)\s+(founded|created|established|born|discovered|invented)",
            r"(?i)(has|have|had)\s+(over|more\s+than|about|approximately|\d+)",
            r"(?i)(according\s+to|based\s+on|research\s+(shows|indicates|suggests))",
            r"\d{4}",  # Years
            r"\d+%",  # Percentages
        ]
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
            for indicator in factual_indicators:
                if re.search(indicator, sentence):
                    claims.append(sentence)
                    break
        return claims


# =============================================================================
# Section 5: Groundedness Checker
# =============================================================================
