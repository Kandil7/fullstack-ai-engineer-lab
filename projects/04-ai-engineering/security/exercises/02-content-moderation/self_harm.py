"""
02 Content Moderation: Self Harm
"""

from ._types import *
from .base_moderator import ContentModerator


class SelfHarmModerator(ContentModerator):
    """
    Detects self-harm content and provides appropriate responses
    including crisis resources.
    """

    category = ContentCategory.SELF_HARM

    CRISIS_RESOURCES = {
        "US": "988 Suicide & Crisis Lifeline: Call or text 988",
        "UK": "Samaritans: 116 123",
        "International": "https://findahelpline.com/",
    }

    def __init__(self):
        self.pattern_groups = {
            "direct_self_harm": [
                r"(?i)(i\s+(want|need|plan|am\s+going|might))\s+to\s+(hurt|kill|end|cut|slice|burn)\s+(myself|me)",
                r"(?i)(cutting|cutting\s+myself|self[-\s]harm|self[-\s]injury)",
                r"(?i)(suicide|suicidal|end\s+(my\s+)?life|kill\s+myself)",
                r"(?i)(overdose|take\s+(too\s+many|all)\s+(pills|medication))\s+(to\s+)?(die|end|kill)",
            ],
            "method_discussion": [
                r"(?i)(best|easiest|most\s+painful|effective)\s+(way|method)\s+to\s+(kill|die|end\s+it)",
                r"(?i)(how\s+to\s+(kill|die|end|commit\s+suicide))\s+(myself|yourself|someone)",
                r"(?i)(razor|blade|knife|pills|rope|bridge)\s+(for|to|in)\s+(self[-\s]harm|suicide|killing)",
            ],
            "ideation": [
                r"(?i)(no\s+(reason|point|purpose)\s+to\s+(live|be\s+alive|continue))",
                r"(?i)(everyone\s+(would\s+be\s+better|be\s+ happier)\s+(off\s+)?without\s+me)",
                r"(?i)(i\s+(wish|hope|want)\s+(i\s+)?(was|were)\s+(dead|gone|never\s+born))",
                r"(?i)(nothing\s+matters|what'?s\s+the\s+point|no\s+way\s+out)",
            ],
        }

        self.severity_map = {
            "direct_self_harm": SeverityLevel.CRITICAL,
            "method_discussion": SeverityLevel.HIGH,
            "ideation": SeverityLevel.HIGH,
        }

    def check(self, text: str) -> list[ModerationResult]:
        results = []
        for group_name, patterns in self.pattern_groups.items():
            flagged_terms = []
            for pattern in patterns:
                matches = re.findall(pattern, text)
                flagged_terms.extend(matches[:3])

            if flagged_terms:
                severity = self.severity_map.get(group_name, SeverityLevel.MEDIUM)
                crisis_info = "\n".join(
                    f"  {k}: {v}" for k, v in self.CRISIS_RESOURCES.items()
                )
                results.append(
                    ModerationResult(
                        category=self.category,
                        severity=severity,
                        confidence=min(len(flagged_terms) * 0.25 + 0.5, 0.95),
                        details=f"Self-harm content detected: {group_name}",
                        flagged_terms=flagged_terms[:5],
                        context_notes=f"Crisis resources:\n{crisis_info}",
                        recommended_action="block_with_support",
                    )
                )
        return results


# =============================================================================
# Section 7: Custom Content Policy Engine
# =============================================================================
