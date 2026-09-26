"""
04 Output Filtering: Quality Scorer
"""

from ._types import *


class OutputQualityScorer:
    """
    Scores the quality of AI-generated output based on multiple factors:
      1. Relevance to query
      2. Completeness
      3. Clarity
      4. Factual accuracy indicators
      5. Coherence
    """

    def score(
        self,
        query: str,
        response: str,
        context: Optional[str] = None,
    ) -> FilterResult:
        """Score the quality of an AI response."""
        scores = {}

        # Relevance score (keyword overlap with query)
        query_tokens = set(re.findall(r"\b\w{3,}\b", query.lower()))
        response_tokens = set(re.findall(r"\b\w{3,}\b", response.lower()))
        if query_tokens:
            relevance = len(query_tokens & response_tokens) / len(query_tokens)
        else:
            relevance = 0.0
        scores["relevance"] = min(relevance * 1.2, 1.0)

        # Completeness score (length and structure)
        word_count = len(response.split())
        if word_count < 10:
            completeness = 0.3
        elif word_count < 50:
            completeness = 0.6
        elif word_count < 200:
            completeness = 0.9
        else:
            completeness = 1.0
        scores["completeness"] = completeness

        # Clarity score (sentence structure, readability)
        sentences = re.split(r"[.!?]+", response)
        sentences = [s.strip() for s in sentences if s.strip()]
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(
            len(sentences), 1
        )
        # Ideal sentence length: 15-25 words
        if 10 <= avg_sentence_length <= 30:
            clarity = 0.9
        elif 5 <= avg_sentence_length <= 40:
            clarity = 0.7
        else:
            clarity = 0.4
        scores["clarity"] = clarity

        # Coherence score (discourse markers, logical flow)
        coherence_indicators = [
            r"(?i)(therefore|however|moreover|furthermore|additionally|consequently)",
            r"(?i)(first|second|third|finally|in\s+conclusion|to\s+summarize)",
            r"(?i)(for\s+example|such\s+as|specifically|in\s+particular)",
            r"(?i)(because|since|thus|as\s+a\s+result|this\s+means)",
        ]
        coherence_count = sum(
            1 for pat in coherence_indicators if re.search(pat, response)
        )
        coherence = min(0.5 + coherence_count * 0.15, 1.0)
        scores["coherence"] = coherence

        # Citation quality (if context provided)
        if context:
            context_tokens = set(re.findall(r"\b\w{3,}\b", context.lower()))
            citation_overlap = len(response_tokens & context_tokens) / max(
                len(response_tokens), 1
            )
            scores["citation_quality"] = min(citation_overlap * 1.5, 1.0)

        # Calculate overall score
        weights = {
            "relevance": 0.3,
            "completeness": 0.2,
            "clarity": 0.2,
            "coherence": 0.2,
            "citation_quality": 0.1,
        }
        overall = sum(scores.get(k, 0) * w for k, w in weights.items())
        overall = min(overall, 1.0)

        # Determine severity
        if overall >= 0.7:
            severity = SeverityLevel.NONE
            passed = True
        elif overall >= 0.5:
            severity = SeverityLevel.LOW
            passed = True
        else:
            severity = SeverityLevel.MEDIUM
            passed = False

        recommendations = []
        if scores.get("relevance", 0) < 0.5:
            recommendations.append("Response may not adequately address the query")
        if scores.get("completeness", 0) < 0.6:
            recommendations.append("Response may be too brief - consider expanding")
        if scores.get("clarity", 0) < 0.6:
            recommendations.append("Consider simplifying sentence structure")
        if scores.get("coherence", 0) < 0.6:
            recommendations.append("Add transition words to improve flow")

        return FilterResult(
            category=FilterCategory.QUALITY,
            passed=passed,
            severity=severity,
            confidence=0.7,
            details=f"Quality score: {overall:.2f} (relevance={scores.get('relevance', 0):.2f}, "
            f"completeness={scores.get('completeness', 0):.2f}, "
            f"clarity={scores.get('clarity', 0):.2f}, "
            f"coherence={scores.get('coherence', 0):.2f})",
            flagged_items=[f"{k}: {v:.2f}" for k, v in scores.items() if v < 0.5],
            recommendations=recommendations,
        )


# =============================================================================
# Section 7: Citation Verifier
# =============================================================================
