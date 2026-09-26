"""
02 Content Moderation: Violence
"""

from ._types import *
from .base_moderator import ContentModerator


class ViolenceModerator(ContentModerator):
    """
    Detects violent content including threats, glorification of violence,
    and graphic descriptions.
    """

    category = ContentCategory.VIOLENCE

    def __init__(self):
        self.pattern_groups = {
            "direct_threats": [
                r"(?i)(i'?ll|i\s+will|going\s+to|gonna)\s+(kill|murder|assault|beat|hurt|destroy)\s+(you|them|him|her|everyone)",
                r"(?i)(death|die|killed?|murdered?)\s+(threat|warning|promise|to\s+you)",
                r"(?i)(you|they|he|she)\s+(will|shall|must)\s+(die|perish|suffer|burn)",
            ],
            "graphic_violence": [
                r"(?i)(cut|slash|stab|shoot|blow\s+up)\s+(them|him|her|someone|a\s+person|people)\s+(up|apart|to\s+pieces|with)",
                r"(?i)(blood|gore|guts?|entrails?|organs?)\s+(splatter|spray|everywhere|pooling)",
                r"(?i)(torture|maim|dismember|decapitate|disembowel)\s+(them|him|her|someone|people)",
            ],
            "weapons_and_plans": [
                r"(?i)(how\s+to\s+(make|build|create|obtain))\s+(a\s+)?(bomb|explosive|weapon|gun|rifle|pipe\s+bomb)",
                r"(?i)(school|movie\s+theater|mall|concert)\s+(shooting|bombing|attack)\s+(plan|method|how)",
            ],
            "glorification": [
                r"(?i)(glorif|praise|celebrate|hero|heroic)\s+(violence|killing|murder|massacre|shooting)",
                r"(?i)(he|she|they)\s+(deserved|had\s+it\s+coming|asked\s+for\s+it)\s+(to\s+be|getting)\s+(killed|hurt|beaten)",
            ],
        }

        self.severity_map = {
            "direct_threats": SeverityLevel.CRITICAL,
            "graphic_violence": SeverityLevel.HIGH,
            "weapons_and_plans": SeverityLevel.CRITICAL,
            "glorification": SeverityLevel.MEDIUM,
        }

    def check(self, text: str) -> list[ModerationResult]:
        results = []
        for group_name, patterns in self.pattern_groups.items():
            flagged_terms = []
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    flagged_terms.extend(matches[:3])

            if flagged_terms:
                severity = self.severity_map.get(group_name, SeverityLevel.MEDIUM)
                results.append(
                    ModerationResult(
                        category=self.category,
                        severity=severity,
                        confidence=min(len(flagged_terms) * 0.25 + 0.45, 0.95),
                        details=f"Violence detected: {group_name}",
                        flagged_terms=flagged_terms[:5],
                        recommended_action="block"
                        if severity.value >= SeverityLevel.HIGH.value
                        else "flag",
                    )
                )
        return results


# =============================================================================
# Section 5: Sexual Content Detection
# =============================================================================
