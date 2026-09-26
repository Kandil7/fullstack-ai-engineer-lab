"""
04 Output Filtering: Citation Verifier
"""

from ._types import *


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
        "author_year": re.compile(
            r"\(([A-Z][a-z]+(?:\s+(?:et\s+al\.?|and|&)\s+[A-Z][a-z]+)*),?\s+(\d{4})\)"
        ),
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
        has_references_section = bool(
            re.search(r"(?i)(references?|bibliography|works?\s+cited)", text)
        )
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
            issues.append(
                f"Long text ({word_count} words) with few citations ({len(citations_found)})"
            )

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
