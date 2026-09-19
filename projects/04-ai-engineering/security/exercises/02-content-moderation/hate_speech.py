"""
02 Content Moderation: Hate Speech
"""

from ._types import *
from .base_moderator import ContentModerator

class HateSpeechModerator(ContentModerator):
    """
    Detects hate speech targeting individuals or groups based on
    race, ethnicity, religion, gender, sexual orientation, disability, etc.
    """

    category = ContentCategory.HATE_SPEECH

    def __init__(self):
        # Pattern groups for different types of hate speech
        self.pattern_groups = {
            "dehumanization": [
                r"(?i)(are|they're|those\s+people)\s+(animals?|vermin|trash|garbage|scum|cockroaches?|rats?|subhuman|parasites?)",
                r"(?i)(treat|view|see)\s+(them|those|these)\s+(people|folks)?\s+as\s+(less\s+than|not\s+human|animals?)",
            ],
            "slurs_and_epithets": [
                r"(?i)\b(n[i1]gg[ae3]r|f[ae]g[g]?[o0]t|k[i1]ke|sp[i1]c|ch[i1]nk|j[ae]p|t[o0]w[el]{2})\b",
                r"(?i)\b(r[3]t[ae]rd|cr[i1]p|gimp|retard(?:ed)?)\b",
            ],
            "calls_for_exclusion": [
                r"(?i)(ban|deport|remove|exterminate|eliminate|get\s+rid\s+of)\s+(all\s+)?(the\s+)?(those|them|these|every)\s+(people|ones?|folks?)\s+(who|that|because)",
                r"(?i)(they|those\s+people)\s+(don'?t|do\s+not)\s+(belong|deserve|merit)\s+(to\s+be|here|rights?)",
            ],
            "supremacy": [
                r"(?i)(white|black|arab|jewish|muslim|christian)\s+(supremacy|master\s+race|is\s+superior)",
                r"(?i)(our|their)\s+(race|ethnicity|religion)\s+(is\s+)?(better|superior|more\s+evolved|purer)",
            ],
        }

        # Severity mapping
        self.severity_map = {
            "dehumanization": SeverityLevel.HIGH,
            "slurs_and_epithets": SeverityLevel.CRITICAL,
            "calls_for_exclusion": SeverityLevel.HIGH,
            "supremacy": SeverityLevel.HIGH,
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
                        confidence=min(len(flagged_terms) * 0.3 + 0.4, 0.95),
                        details=f"Hate speech detected: {group_name}",
                        flagged_terms=flagged_terms[:5],
                        recommended_action="block"
                        if severity.value >= SeverityLevel.HIGH.value
                        else "flag",
                    )
                )
        return results


# =============================================================================
# Section 4: Violence Detection
# =============================================================================


