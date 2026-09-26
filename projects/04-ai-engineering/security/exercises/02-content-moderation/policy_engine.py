"""
02 Content Moderation: Policy Engine
"""

from ._types import *


@dataclass
class PolicyRule:
    """A custom content policy rule."""

    rule_id: str
    name: str
    category: ContentCategory
    severity: SeverityLevel
    patterns: list[str]
    exceptions: list[str] = field(default_factory=list)
    description: str = ""
    enabled: bool = True


class CustomPolicyEngine:
    """
    Engine for defining and enforcing custom content policies.
    Supports rule creation, exception handling, and policy composition.
    """

    def __init__(self):
        self.rules: list[PolicyRule] = []
        self.compiled_rules: dict[str, list[re.Pattern]] = {}
        self.compiled_exceptions: dict[str, list[re.Pattern]] = {}

    def add_rule(self, rule: PolicyRule) -> None:
        """Add a policy rule and compile its patterns."""
        self.rules.append(rule)
        self.compiled_rules[rule.rule_id] = [
            re.compile(pat, re.IGNORECASE) for pat in rule.patterns
        ]
        self.compiled_exceptions[rule.rule_id] = [
            re.compile(pat, re.IGNORECASE) for pat in rule.exceptions
        ]
        logger.info(f"Added policy rule: {rule.name} ({rule.rule_id})")

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a policy rule by ID."""
        for i, rule in enumerate(self.rules):
            if rule.rule_id == rule_id:
                self.rules.pop(i)
                self.compiled_rules.pop(rule_id, None)
                self.compiled_exceptions.pop(rule_id, None)
                return True
        return False

    def check(self, text: str) -> list[ModerationResult]:
        """Check text against all active policy rules."""
        results = []
        for rule in self.rules:
            if not rule.enabled:
                continue

            matched = False
            flagged_terms = []
            for pattern in self.compiled_rules.get(rule.rule_id, []):
                matches = pattern.findall(text)
                if matches:
                    flagged_terms.extend(matches[:5])
                    matched = True

            if matched:
                # Check exceptions
                exception_hit = False
                for exc_pattern in self.compiled_exceptions.get(rule.rule_id, []):
                    if exc_pattern.search(text):
                        exception_hit = True
                        break

                if not exception_hit:
                    results.append(
                        ModerationResult(
                            category=rule.category,
                            severity=rule.severity,
                            confidence=min(len(flagged_terms) * 0.2 + 0.5, 0.9),
                            details=f"Custom policy violation: {rule.name}",
                            flagged_terms=flagged_terms[:5],
                            recommended_action="block"
                            if rule.severity.value >= SeverityLevel.HIGH.value
                            else "flag",
                        )
                    )

        return results


# =============================================================================
# Section 8: Moderation Pipeline
# =============================================================================
