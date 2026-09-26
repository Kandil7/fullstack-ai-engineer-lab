"""
04 Output Filtering: Toxicity
"""

from ._types import *


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
                results.append(
                    FilterResult(
                        category=FilterCategory.TOXICITY,
                        passed=severity.value < self.severity_threshold.value,
                        severity=severity,
                        confidence=min(0.5 + len(matches) * 0.15, 0.95),
                        details=f"Toxic content detected: {category}",
                        flagged_items=[str(m)[:50] for m in matches[:5]],
                        recommendations=[
                            f"Consider rephrasing to remove {category}"
                            if severity.value < SeverityLevel.HIGH.value
                            else f"Block content containing {category}"
                        ],
                    )
                )

        return results


# =============================================================================
# Section 4: Hallucination Detection
# =============================================================================
