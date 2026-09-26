"""
02 Content Moderation: Sexual Content
"""

from ._types import *
from .base_moderator import ContentModerator


class SexualContentModerator(ContentModerator):
    """
    Detects explicit sexual content, with context awareness for
    educational/medical discussions.
    """

    category = ContentCategory.SEXUAL_CONTENT

    def __init__(self):
        self.explicit_patterns = [
            r"(?i)(pornograph|sex\s+video|nude\s+(photo|image|picture)|explicit\s+(sex|nude))",
            r"(?i)(have\s+sex\s+with|fuck(?:ing|ed)?|suck(?:ing)?|blowjob|handjob)",
            r"(?i)(genital|vagina|penis|clitoris|anus)\s+(pic(?:ture)?|video|image|photo|shot)",
        ]

        self.minor_exploitation_patterns = [
            r"(?i)(child|minor|underage|teen|young)\s+(porn|sex|nude|exploit|abuse)",
            r"(?i)(loli|lolita|pedo|pedophil|cp\b)",
            r"(?i)(age\s*(play|gap))\s*(sex|relationship|attraction)",
        ]

        # Context patterns that may indicate educational/medical discussion
        self.educational_context = [
            r"(?i)(medical|clinical|anatomical|educational|academic|scientific|textbook)",
            r"(?i)(doctor|nurse|professor|researcher|student)\s+(explained|said|discussed|noted)",
            r"(?i)(health|biology|anatomy|physiology|reproductive)",
        ]

    def check(self, text: str) -> list[ModerationResult]:
        results = []

        # Check for minor exploitation - always CRITICAL
        minor_matches = []
        for pattern in self.minor_exploitation_patterns:
            matches = re.findall(pattern, text)
            minor_matches.extend(matches)

        if minor_matches:
            results.append(
                ModerationResult(
                    category=self.category,
                    severity=SeverityLevel.CRITICAL,
                    confidence=0.95,
                    details="Exploitation of minors detected",
                    flagged_terms=minor_matches[:3],
                    recommended_action="block",
                )
            )
            return results  # Immediate return for highest severity

        # Check for explicit content
        explicit_matches = []
        for pattern in self.explicit_patterns:
            matches = re.findall(pattern, text)
            explicit_matches.extend(matches)

        if explicit_matches:
            # Check for educational context
            is_educational = any(
                re.search(pat, text) for pat in self.educational_context
            )

            severity = SeverityLevel.MEDIUM if is_educational else SeverityLevel.HIGH
            confidence = 0.5 if is_educational else 0.85

            results.append(
                ModerationResult(
                    category=self.category,
                    severity=severity,
                    confidence=confidence,
                    details=f"Sexual content detected{' (educational context)' if is_educational else ''}",
                    flagged_terms=explicit_matches[:3],
                    context_notes="Educational context detected"
                    if is_educational
                    else "",
                    recommended_action="flag" if is_educational else "block",
                )
            )

        return results


# =============================================================================
# Section 6: Self-Harm Detection
# =============================================================================
