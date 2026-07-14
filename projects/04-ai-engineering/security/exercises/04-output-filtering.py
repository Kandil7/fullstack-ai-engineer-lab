"""
=============================================================================
AI Security Exercise 04: Output Filtering & Safety
=============================================================================

Topic: Output Filtering
-----------------------
Output filtering ensures AI-generated content is safe, accurate, and
appropriate before reaching users. This exercise covers PII detection,
toxicity filtering, hallucination detection, groundedness checking, and
output quality scoring.

Learning Objectives:
  1. Detect and mask PII in AI outputs
  2. Filter toxic and harmful content from responses
  3. Detect hallucinations and verify factual accuracy
  4. Score output quality and groundedness
  5. Build production-ready output filtering pipelines

Prerequisites:
  - Python 3.9+
  - re, json, hashlib, logging, dataclasses, enum, typing, math
  - Optional: openai (for LLM-based detection)

WARNING: This code is for EDUCATIONAL purposes.
=============================================================================
"""

import re
import json
import hashlib
import logging
import time
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Callable
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("output_filtering")


# =============================================================================
# Section 1: Core Types
# =============================================================================

class FilterCategory(Enum):
    """Categories of output filtering."""
    PII = auto()
    TOXICITY = auto()
    HALLUCINATION = auto()
    GROUNDEDNESS = auto()
    QUALITY = auto()
    CITATION = auto()
    SAFETY = auto()


class SeverityLevel(Enum):
    """Severity levels for filter results."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class FilterResult:
    """Result of a single output filter check."""
    category: FilterCategory
    passed: bool
    severity: SeverityLevel
    confidence: float  # 0.0 - 1.0
    details: str
    flagged_items: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class OutputVerdict:
    """Final verdict combining all filter results."""
    content_id: str
    is_safe: bool
    overall_score: float  # 0.0 - 1.0 (1.0 = perfect)
    filter_results: list[FilterResult]
    requires_human_review: bool = False
    blocked_sections: list[str] = field(default_factory=list)
    explanation: str = ""


# =============================================================================
# Section 2: PII Detection & Masking
# =============================================================================

class PIIFilter:
    """
    Detects and masks Personally Identifiable Information (PII) in
    AI-generated outputs.
    """

    PII_PATTERNS = {
        "email": {
            "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "mask_fn": lambda m: m[:2] + "***@" + m.split("@")[1],
            "severity": SeverityLevel.MEDIUM,
        },
        "phone_us": {
            "pattern": r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",
            "mask_fn": lambda m: "***-***-" + m[-4:],
            "severity": SeverityLevel.MEDIUM,
        },
        "ssn": {
            "pattern": r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b",
            "mask_fn": lambda m: "***-**-" + m[-4:],
            "severity": SeverityLevel.HIGH,
        },
        "credit_card": {
            "pattern": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b",
            "mask_fn": lambda m: "****-****-****-" + m[-4:],
            "severity": SeverityLevel.HIGH,
        },
        "ip_address": {
            "pattern": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            "mask_fn": lambda m: m[:m.rfind(".")] + ".XXX",
            "severity": SeverityLevel.LOW,
        },
        "date_of_birth": {
            "pattern": r"\b(?:0[1-9]|1[0-2])[/.-](?:0[1-9]|[12]\d|3[01])[/.-](?:19|20)\d{2}\b",
            "mask_fn": lambda m: "**/**/****",
            "severity": SeverityLevel.HIGH,
        },
        "address_us": {
            "pattern": r"\d{1,5}\s+(?:[A-Z][a-zA-Z]*\s+){1,3}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln)\b",
            "mask_fn": lambda m: "[ADDRESS REDACTED]",
            "severity": SeverityLevel.MEDIUM,
        },
        "name_pattern": {
            "pattern": r"(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+",
            "mask_fn": lambda m: m.split(".")[0] + ". [NAME REDACTED]",
            "severity": SeverityLevel.MEDIUM,
        },
    }

    def __init__(self, mask: bool = True, custom_patterns: Optional[dict] = None):
        self.mask = mask
        self.custom_patterns = custom_patterns or {}
        self.all_patterns = {**self.PII_PATTERNS, **self.custom_patterns}
        self.compiled = {
            name: re.compile(info["pattern"])
            for name, info in self.all_patterns.items()
        }

    def detect(self, text: str) -> list[FilterResult]:
        """Detect PII in text."""
        results = []
        for pii_type, pattern_info in self.all_patterns.items():
            compiled = self.compiled[pii_type]
            matches = compiled.findall(text)

            if matches:
                masked_items = []
                for match in matches:
                    if self.mask and "mask_fn" in pattern_info:
                        masked_items.append(pattern_info["mask_fn"](match))
                    else:
                        masked_items.append(match)

                results.append(FilterResult(
                    category=FilterCategory.PII,
                    passed=False,
                    severity=pattern_info["severity"],
                    confidence=0.9,
                    details=f"Detected {len(matches)} {pii_type} instance(s)",
                    flagged_items=masked_items[:5],
                    recommendations=[f"Mask or redact {pii_type} data before display"],
                ))

        return results

    def filter_text(self, text: str) -> tuple[str, list[FilterResult]]:
        """Detect and mask PII in text, returning filtered text and results."""
        results = self.detect(text)
        filtered = text

        if self.mask:
            for pii_type, pattern_info in self.all_patterns.items():
                compiled = self.compiled[pii_type]
                matches = compiled.findall(filtered)
                for match in matches:
                    if "mask_fn" in pattern_info:
                        masked = pattern_info["mask_fn"](match)
                        filtered = filtered.replace(match, masked, 1)

        return filtered, results


# =============================================================================
# Section 3: Toxicity Detection
# =============================================================================

class ToxicityFilter:
    """
    Detects toxic content including profanity, insults, threats,
    and negative sentiment.
    """

    TOXICITY_PATTERNS = {
        "profanity": [
            r"(?i)\b(damn|hell|crap|ass|asshole|bitch|bastard|shit|fuck|fucking|fucked|fucker|dick|piss)\b",
        ],
        "insults": [
            r"(?i)(you(?:'re|\s+are)\s+)(stupid|idiot|moron|loser|worthless|pathetic|dumb|trash|garbage|scum|useless|incompetent)",
            r"(?i)(shut\s+up|go\s+away|nobody\s+(cares|asked|likes?\s+you))",
            r"(?i)(you\s+(should|need\s+to|must)\s+)(die|kill\s+yourself|disappear|leave|quit)",
        ],
        "threats": [
            r"(?i)(i'?ll\s+(kill|murder|destroy|hurt|beat|find)\s+(you|them|him|her))",
            r"(?i)(you(?:'re|\s+are)\s+(dead|finished|done|going\s+to\s+pay))",
            r"(?i)(watch\s+your\s+back|you(?:'ll|\s+will)\s+regret)",
        ],
        "discrimination": [
            r"(?i)(all|those)\s+(people|folks|ones)\s+(are|should|need\s+to)\s+(go|leave|die|suffer)",
            r"(?i)(don'?t\s+(let|allow|want)\s+)(them|those|these)\s+(in|here|around)",
        ],
    }

    def __init__(self, severity_threshold: SeverityLevel = SeverityLevel.MEDIUM):
        self.severity_threshold = severity_threshold
        self.severity_map = {
            "profanity": SeverityLevel.LOW,
            "insults": SeverityLevel.MEDIUM,
            "threats": SeverityLevel.HIGH,
            "discrimination": SeverityLevel.HIGH,
        }
        self.compiled = {
            cat: [re.compile(p) for p in patterns]
            for cat, patterns in self.TOXICITY_PATTERNS.items()
        }

    def check(self, text: str) -> list[FilterResult]:
        """Check text for toxic content."""
        results = []

        for category, patterns in self.compiled.items():
            matches = []
            for pattern in patterns:
                found = pattern.findall(text)
                matches.extend(found[:5])

            if matches:
                severity = self.severity_map.get(category, SeverityLevel.MEDIUM)
                results.append(FilterResult(
                    category=FilterCategory.TOXICITY,
                    passed=severity.value < self.severity_threshold.value,
                    severity=severity,
                    confidence=min(0.5 + len(matches) * 0.15, 0.95),
                    details=f"Toxic content detected: {category}",
                    flagged_items=[str(m)[:50] for m in matches[:5]],
                    recommendations=[
                        f"Consider rephrasing to remove {category}" if severity.value < SeverityLevel.HIGH.value
                        else f"Block content containing {category}"
                    ],
                ))

        return results


# =============================================================================
# Section 4: Hallucination Detection
# =============================================================================

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
        severity = SeverityLevel.NONE if score >= 0.8 else (SeverityLevel.LOW if score >= 0.5 else SeverityLevel.MEDIUM)

        return FilterResult(
            category=FilterCategory.HALLUCINATION,
            passed=passed,
            severity=severity,
            confidence=score,
            details=f"Hallucination score: {score:.2f} ({supported_count}/{len(claims)} claims supported)",
            flagged_items=unsupported_claims[:5],
            recommendations=["Verify claims against source material"] if not passed else [],
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
            r"\d+%",   # Percentages
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
            recommendations.append(f"Remove or qualify {len(unsupported)} unsupported assertion(s)")
        if grounding_ratio < 0.4:
            recommendations.append("Rewrite response to more closely reference source material")

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
        avg_sentence_length = (
            sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
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
            citation_overlap = len(response_tokens & context_tokens) / max(len(response_tokens), 1)
            scores["citation_quality"] = min(citation_overlap * 1.5, 1.0)

        # Calculate overall score
        weights = {
            "relevance": 0.3,
            "completeness": 0.2,
            "clarity": 0.2,
            "coherence": 0.2,
            "citation_quality": 0.1,
        }
        overall = sum(
            scores.get(k, 0) * w for k, w in weights.items()
        )
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
            details=f"Quality score: {overall:.2f} (relevance={scores.get('relevance',0):.2f}, "
                    f"completeness={scores.get('completeness',0):.2f}, "
                    f"clarity={scores.get('clarity',0):.2f}, "
                    f"coherence={scores.get('coherence',0):.2f})",
            flagged_items=[f"{k}: {v:.2f}" for k, v in scores.items() if v < 0.5],
            recommendations=recommendations,
        )


# =============================================================================
# Section 7: Citation Verifier
# =============================================================================

class CitationVerifier:
    """
    Verifies citations and references in AI-generated content.

    Checks:
      1. Citation format validity
      2. Reference existence
      3. Citation-context alignment
    """

    CITATION_PATTERNS = {
        "bracket_number": re.compile(r"\[(\d+(?:,\s*\d+)*)\]"),
        "author_year": re.compile(r"\(([A-Z][a-z]+(?:\s+(?:et\s+al\.?|and|&)\s+[A-Z][a-z]+)*),?\s+(\d{4})\)"),
        "footnote": re.compile(r"\^(\d+)"),
        "url": re.compile(r"https?://[^\s<>\")]+"),
        "doi": re.compile(r"(?:doi:|DOI:)\s*(10\.\d{4,}/[^\s]+)"),
    }

    def verify(
        self,
        text: str,
        known_references: Optional[list[str]] = None,
    ) -> FilterResult:
        """Verify citations in the text."""
        citations_found = []
        issues = []

        for cite_type, pattern in self.CITATION_PATTERNS.items():
            matches = pattern.findall(text)
            for match in matches:
                cite_str = match if isinstance(match, str) else str(match)
                citations_found.append({"type": cite_type, "ref": cite_str})

        # Check for references without citations and vice versa
        has_references_section = bool(re.search(r"(?i)(references?|bibliography|works?\s+cited)", text))
        has_citations_in_text = len(citations_found) > 0

        if has_references_section and not has_citations_in_text:
            issues.append("References section exists but no inline citations found")
        if has_citations_in_text and not has_references_section:
            issues.append("Inline citations found but no references section")

        # Validate URLs
        urls = self.CITATION_PATTERNS["url"].findall(text)
        for url in urls:
            if not url.startswith("http"):
                issues.append(f"Invalid URL format: {url[:50]}")

        # Check citation count vs text length
        word_count = len(text.split())
        if word_count > 200 and len(citations_found) < 2:
            issues.append(f"Long text ({word_count} words) with few citations ({len(citations_found)})")

        severity = SeverityLevel.NONE if not issues else SeverityLevel.LOW
        if len(issues) > 2:
            severity = SeverityLevel.MEDIUM

        return FilterResult(
            category=FilterCategory.CITATION,
            passed=len(issues) == 0,
            severity=severity,
            confidence=0.8,
            details=f"Found {len(citations_found)} citation(s), {len(issues)} issue(s)",
            flagged_items=[str(c) for c in citations_found[:5]],
            recommendations=issues[:5] if issues else [],
        )


# =============================================================================
# Section 8: Output Filtering Pipeline
# =============================================================================

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
        requires_review = any(r.severity.value >= SeverityLevel.MEDIUM.value for r in all_results)

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
            (sum(quality_scores) / max(len(quality_scores), 1)) * 0.6 +
            quality_result_score * 0.4
        ) if quality_scores else quality_result_score

        explanation_parts = []
        if pii_results:
            explanation_parts.append(f"PII detected and {'masked' if self.pii_filter.mask else 'flagged'}")
        if toxicity_results:
            explanation_parts.append(f"Toxicity detected in {len(toxicity_results)} category(ies)")
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
        print(f"\n  [{i}] Original: \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        print(f"      Filtered: \"{filtered[:60]}{'...' if len(filtered) > 60 else ''}\"")
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
        print(f"\n  [{i}] \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
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
        ("Python supports multiple paradigms and was created by Guido van Rossum.",
         "Mixed: supported + unsupported"),
    ]

    for response, description in test_responses:
        result = detector.check(response, source)
        status = "PASS" if result.passed else "FAIL"
        print(f"\n  [{status}] {description}")
        print(f"  Response: \"{response}\"")
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
        ("The Eiffel Tower is in Paris, France and was built for the 1889 Worlds Fair.",
         "Well-grounded response"),
        ("The Eiffel Tower was built in 1889. The Great Wall of China is very long.",
         "Partially grounded with irrelevant info"),
        ("The Eiffel Tower was built by Leonardo da Vinci in 1503 for the French Revolution.",
         "Poorly grounded with false claims"),
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
        ("Exercise improves cardiovascular health, strengthens muscles, "
         "boosts mental health, and helps maintain a healthy weight. "
         "Regular physical activity reduces the risk of chronic diseases "
         "such as diabetes and heart disease.",
         "High-quality response"),
        ("It is good.",
         "Low-quality: too brief"),
        ("The weather is nice today. I like pizza. Exercise exists.",
         "Low-quality: off-topic"),
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
            "Response with PII"
        ),
        (
            "What is Acme Corp?",
            "Acme Corp is a terrible company with awful employees.",
            context,
            "Toxic response"
        ),
        (
            "Acme Corp details",
            "Acme Corp was founded in 2010. It has 500 employees and $50 million in revenue.",
            context,
            "Grounded response"
        ),
    ]

    for query, response, ctx, description in test_cases:
        verdict = pipeline.filter(query, response, ctx)
        status = "[OK] SAFE" if verdict.is_safe else "[X] UNSAFE"
        print(f"\n  [{status}] {description}")
        print(f"  Query: \"{query}\"")
        print(f"  Score: {verdict.overall_score:.2f}")
        print(f"  Explanation: {verdict.explanation}")
        if verdict.requires_human_review:
            print(f"  [!] Requires human review")

    # Show pipeline statistics
    print(f"\n  Pipeline Statistics:")
    print(f"    Total decisions: {len(pipeline.decision_log)}")
    print(f"    Safe: {sum(1 for v in pipeline.decision_log if v.is_safe)}")
    print(f"    Requiring review: {sum(1 for v in pipeline.decision_log if v.requires_human_review)}")


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

if __name__ == "__main__":
    print("AI Security Exercise 04: Output Filtering & Safety")
    print("=" * 72)

    demo_pii_detection()
    demo_toxicity_detection()
    demo_hallucination_detection()
    demo_groundedness_checking()
    demo_quality_scoring()
    demo_output_pipeline()
    print_best_practices()

    print("\n" + "=" * 72)
    print("Exercise complete. Review the code for implementation details.")
    print("=" * 72)
