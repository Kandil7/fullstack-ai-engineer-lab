"""
=============================================================================
AI Security Exercise 02: Content Moderation Systems
=============================================================================

Topic: Content Moderation
-------------------------
Content moderation is essential for AI systems that interact with users.
This exercise covers detecting and filtering harmful content including
hate speech, violence, sexual content, self-harm, and custom policy
violations.

Learning Objectives:
  1. Build multi-category content classifiers
  2. Implement custom content policies
  3. Create moderation pipelines with severity levels
  4. Design human-in-the-loop review systems

Prerequisites:
  - Python 3.9+
  - re, json, hashlib, logging, dataclasses, enum, typing, abc
  - Optional: openai (for LLM-based moderation)

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
from abc import ABC, abstractmethod
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("content_moderation")


# =============================================================================
# Section 1: Content Categories & Severity
# =============================================================================

class ContentCategory(Enum):
    """Categories of content that may need moderation."""
    SAFE = auto()
    HATE_SPEECH = auto()
    VIOLENCE = auto()
    SEXUAL_CONTENT = auto()
    SELF_HARM = auto()
    HARASSMENT = auto()
    SPAM = auto()
    MISINFORMATION = auto()
    CUSTOM_POLICY = auto()


class SeverityLevel(Enum):
    """Severity levels for content violations."""
    NONE = 0
    LOW = 1       # Mildly inappropriate, may be acceptable in context
    MEDIUM = 2    # Clearly inappropriate, should be flagged
    HIGH = 3      # Severely inappropriate, should be blocked
    CRITICAL = 4  # Illegal or extremely harmful, block + report


@dataclass
class ModerationResult:
    """Result of a content moderation check."""
    category: ContentCategory
    severity: SeverityLevel
    confidence: float  # 0.0 - 1.0
    details: str
    flagged_terms: list[str] = field(default_factory=list)
    context_notes: str = ""
    recommended_action: str = "allow"
    timestamp: float = field(default_factory=time.time)

    @property
    def should_block(self) -> bool:
        return self.severity.value >= SeverityLevel.HIGH.value

    @property
    def should_flag(self) -> bool:
        return self.severity.value >= SeverityLevel.MEDIUM.value


@dataclass
class ModerationDecision:
    """Final moderation decision combining multiple category checks."""
    content_id: str
    is_allowed: bool
    overall_severity: SeverityLevel
    category_results: list[ModerationResult]
    requires_human_review: bool = False
    explanation: str = ""
    action_taken: str = ""


# =============================================================================
# Section 2: Base Moderator (Abstract)
# =============================================================================

class ContentModerator(ABC):
    """Abstract base class for content moderators."""

    @abstractmethod
    def check(self, text: str) -> list[ModerationResult]:
        """Check text and return list of moderation results."""
        pass

    @property
    @abstractmethod
    def category(self) -> ContentCategory:
        """The content category this moderator handles."""
        pass


# =============================================================================
# Section 3: Hate Speech Detection
# =============================================================================

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
                results.append(ModerationResult(
                    category=self.category,
                    severity=severity,
                    confidence=min(len(flagged_terms) * 0.3 + 0.4, 0.95),
                    details=f"Hate speech detected: {group_name}",
                    flagged_terms=flagged_terms[:5],
                    recommended_action="block" if severity.value >= SeverityLevel.HIGH.value else "flag",
                ))
        return results


# =============================================================================
# Section 4: Violence Detection
# =============================================================================

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
                results.append(ModerationResult(
                    category=self.category,
                    severity=severity,
                    confidence=min(len(flagged_terms) * 0.25 + 0.45, 0.95),
                    details=f"Violence detected: {group_name}",
                    flagged_terms=flagged_terms[:5],
                    recommended_action="block" if severity.value >= SeverityLevel.HIGH.value else "flag",
                ))
        return results


# =============================================================================
# Section 5: Sexual Content Detection
# =============================================================================

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
            results.append(ModerationResult(
                category=self.category,
                severity=SeverityLevel.CRITICAL,
                confidence=0.95,
                details="Exploitation of minors detected",
                flagged_terms=minor_matches[:3],
                recommended_action="block",
            ))
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

            results.append(ModerationResult(
                category=self.category,
                severity=severity,
                confidence=confidence,
                details=f"Sexual content detected{' (educational context)' if is_educational else ''}",
                flagged_terms=explicit_matches[:3],
                context_notes="Educational context detected" if is_educational else "",
                recommended_action="flag" if is_educational else "block",
            ))

        return results


# =============================================================================
# Section 6: Self-Harm Detection
# =============================================================================

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
                results.append(ModerationResult(
                    category=self.category,
                    severity=severity,
                    confidence=min(len(flagged_terms) * 0.25 + 0.5, 0.95),
                    details=f"Self-harm content detected: {group_name}",
                    flagged_terms=flagged_terms[:5],
                    context_notes=f"Crisis resources:\n{crisis_info}",
                    recommended_action="block_with_support",
                ))
        return results


# =============================================================================
# Section 7: Custom Content Policy Engine
# =============================================================================

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
                    results.append(ModerationResult(
                        category=rule.category,
                        severity=rule.severity,
                        confidence=min(len(flagged_terms) * 0.2 + 0.5, 0.9),
                        details=f"Custom policy violation: {rule.name}",
                        flagged_terms=flagged_terms[:5],
                        recommended_action="block" if rule.severity.value >= SeverityLevel.HIGH.value else "flag",
                    ))

        return results


# =============================================================================
# Section 8: Moderation Pipeline
# =============================================================================

class ModerationPipeline:
    """
    Complete content moderation pipeline combining multiple moderators
    with configurable policies and human-in-the-loop review.
    """

    def __init__(self, policy_engine: Optional[CustomPolicyEngine] = None):
        self.moderators: list[ContentModerator] = []
        self.policy_engine = policy_engine or CustomPolicyEngine()
        self.review_queue: list[ModerationDecision] = []
        self.decision_log: list[ModerationDecision] = []
        self.human_review_threshold = SeverityLevel.MEDIUM

    def add_moderator(self, moderator: ContentModerator) -> None:
        """Register a content moderator with the pipeline."""
        self.moderators.append(moderator)
        logger.info(f"Added moderator: {moderator.__class__.__name__}")

    def moderate(self, text: str, content_id: Optional[str] = None) -> ModerationDecision:
        """
        Run the full moderation pipeline on the given text.

        Args:
            text: The content to moderate
            content_id: Optional identifier for the content

        Returns:
            ModerationDecision with the final verdict
        """
        if not content_id:
            content_id = hashlib.sha256(text.encode()).hexdigest()[:12]

        all_results: list[ModerationResult] = []

        # Run all registered moderators
        for moderator in self.moderators:
            try:
                results = moderator.check(text)
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Moderator {moderator.__class__.__name__} failed: {e}")

        # Run custom policy engine
        policy_results = self.policy_engine.check(text)
        all_results.extend(policy_results)

        # Determine overall decision
        if not all_results:
            decision = ModerationDecision(
                content_id=content_id,
                is_allowed=True,
                overall_severity=SeverityLevel.NONE,
                category_results=[],
                explanation="No content policy violations detected",
                action_taken="allow",
            )
        else:
            max_severity = max((r.severity for r in all_results), key=lambda s: s.value)
            any_blocked = any(r.should_block for r in all_results)
            any_flagged = any(r.should_flag for r in all_results)
            requires_review = any(
                r.severity.value >= self.human_review_threshold.value
                for r in all_results
            )

            categories = ", ".join(r.category.name for r in all_results)
            explanation = (
                f"Detected {len(all_results)} violation(s) across categories: {categories}. "
                f"Max severity: {max_severity.name}"
            )

            if any_blocked:
                action = "block"
            elif any_flagged:
                action = "flag_for_review"
            else:
                action = "allow_with_monitoring"

            decision = ModerationDecision(
                content_id=content_id,
                is_allowed=not any_blocked,
                overall_severity=max_severity,
                category_results=all_results,
                requires_human_review=requires_review,
                explanation=explanation,
                action_taken=action,
            )

        # Log decision
        self.decision_log.append(decision)
        if decision.requires_human_review:
            self.review_queue.append(decision)
            logger.info(f"Content {content_id} queued for human review")

        return decision


# =============================================================================
# Section 9: Output Formatter
# =============================================================================

class ModerationFormatter:
    """Formats moderation results for display or API responses."""

    @staticmethod
    def format_decision(decision: ModerationDecision) -> str:
        """Format a moderation decision as a readable string."""
        lines = [
            f"Content ID: {decision.content_id}",
            f"Allowed: {'Yes' if decision.is_allowed else 'No'}",
            f"Severity: {decision.overall_severity.name}",
            f"Action: {decision.action_taken}",
            f"Human Review: {'Required' if decision.requires_human_review else 'Not required'}",
            f"Explanation: {decision.explanation}",
        ]

        if decision.category_results:
            lines.append("\nViolations:")
            for i, result in enumerate(decision.category_results, 1):
                lines.append(f"  {i}. [{result.category.name}] {result.details}")
                lines.append(f"     Severity: {result.severity.name} | Confidence: {result.confidence:.0%}")
                if result.flagged_terms:
                    terms = ", ".join(str(t)[:30] for t in result.flagged_terms[:3])
                    lines.append(f"     Flagged: {terms}")
                if result.context_notes:
                    lines.append(f"     Notes: {result.context_notes[:100]}")

        return "\n".join(lines)

    @staticmethod
    def format_api_response(decision: ModerationDecision) -> dict:
        """Format a moderation decision as an API response dict."""
        return {
            "content_id": decision.content_id,
            "allowed": decision.is_allowed,
            "severity": decision.overall_severity.name,
            "action": decision.action_taken,
            "requires_human_review": decision.requires_human_review,
            "explanation": decision.explanation,
            "violations": [
                {
                    "category": r.category.name,
                    "severity": r.severity.name,
                    "confidence": r.confidence,
                    "details": r.details,
                    "flagged_terms": r.flagged_terms,
                }
                for r in decision.category_results
            ],
        }


# =============================================================================
# Section 10: Demonstration & Testing
# =============================================================================

def demo_hate_speech_detection():
    """Demonstrate hate speech detection."""
    print("\n" + "=" * 72)
    print("DEMO 1: Hate Speech Detection")
    print("=" * 72)

    moderator = HateSpeechModerator()
    test_cases = [
        "I think all people deserve equal rights and respect.",
        "Those people are animals and don't belong here.",
        "The meeting was productive and everyone contributed well.",
        "We should ban all those people from entering the country.",
        "I respectfully disagree with your political position.",
    ]

    for i, text in enumerate(test_cases, 1):
        results = moderator.check(text)
        print(f"\n  [{i}] \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
                print(f"        Confidence: {r.confidence:.0%}")
        else:
            print("      [OK] No violations detected")


def demo_violence_detection():
    """Demonstrate violence detection."""
    print("\n" + "=" * 72)
    print("DEMO 2: Violence Detection")
    print("=" * 72)

    moderator = ViolenceModerator()
    test_cases = [
        "I'm going to kill it at the presentation today!",
        "I will kill you if you don't give me the money.",
        "The movie featured a graphic scene with blood everywhere.",
        "How to make a pipe bomb step by step guide.",
        "He deserved what happened to him after what he did.",
        "The video game lets you fight enemies in combat.",
    ]

    for i, text in enumerate(test_cases, 1):
        results = moderator.check(text)
        print(f"\n  [{i}] \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
                print(f"        Action: {r.recommended_action}")
        else:
            print("      [OK] No violations detected")


def demo_self_harm_detection():
    """Demonstrate self-harm detection with crisis resources."""
    print("\n" + "=" * 72)
    print("DEMO 3: Self-Harm Detection")
    print("=" * 72)

    moderator = SelfHarmModerator()
    test_cases = [
        "I've been feeling sad lately but I'm seeing a therapist.",
        "I want to hurt myself and I don't see a way out.",
        "Everyone would be better off without me.",
        "I wish I was dead and never born.",
        "My friend is struggling and I want to help them.",
        "What's the best way to end it all?",
    ]

    for i, text in enumerate(test_cases, 1):
        results = moderator.check(text)
        print(f"\n  [{i}] \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
                if r.context_notes:
                    print(f"        Resources: {r.context_notes[:100]}...")
        else:
            print("      [OK] No self-harm indicators detected")


def demo_custom_policies():
    """Demonstrate custom content policy engine."""
    print("\n" + "=" * 72)
    print("DEMO 4: Custom Content Policies")
    print("=" * 72)

    engine = CustomPolicyEngine()

    # Add custom rules
    engine.add_rule(PolicyRule(
        rule_id="no_competitor_mentions",
        name="No Competitor Mentions",
        category=ContentCategory.CUSTOM_POLICY,
        severity=SeverityLevel.LOW,
        patterns=[
            r"(?i)(competitor\s+(a|b|c)|rival\s+company)",
            r"(?i)(buy\s+from|use|try)\s+(competitor|rival)\s+(product|service)",
        ],
        exceptions=[
            r"(?i)(market\s+research|competitive\s+analysis|benchmark)",
        ],
        description="Prevent mentions of competitor products in support channels",
    ))

    engine.add_rule(PolicyRule(
        rule_id="no_pricing_leaks",
        name="No Pricing Information Leaks",
        category=ContentCategory.CUSTOM_POLICY,
        severity=SeverityLevel.HIGH,
        patterns=[
            r"(?i)(internal\s+price|cost\s+price|wholesale\s+price|margin\s+is)",
            r"(?i)(we\s+pay|our\s+cost|manufacturing\s+cost)\s+\$?\d+",
        ],
        description="Prevent leakage of internal pricing information",
    ))

    test_cases = [
        "Our product costs $99.99 for consumers.",
        "Competitor A has a similar product at a lower price.",
        "Let's do some competitive analysis on Competitor B.",
        "We pay only $5 per unit, internal cost price.",
        "Our wholesale price is $3 and retail is $50.",
    ]

    for i, text in enumerate(test_cases, 1):
        results = engine.check(text)
        print(f"\n  [{i}] \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        if results:
            for r in results:
                print(f"      [!] {r.severity.name}: {r.details}")
        else:
            print("      [OK] No policy violations")


def demo_full_pipeline():
    """Demonstrate the complete moderation pipeline."""
    print("\n" + "=" * 72)
    print("DEMO 5: Full Moderation Pipeline")
    print("=" * 72)

    # Set up pipeline
    pipeline = ModerationPipeline()
    pipeline.add_moderator(HateSpeechModerator())
    pipeline.add_moderator(ViolenceModerator())
    pipeline.add_moderator(SexualContentModerator())
    pipeline.add_moderator(SelfHarmModerator())

    # Add custom policy
    pipeline.policy_engine.add_rule(PolicyRule(
        rule_id="no_pii",
        name="No PII in Public Channels",
        category=ContentCategory.CUSTOM_POLICY,
        severity=SeverityLevel.MEDIUM,
        patterns=[
            r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",  # SSN-like
            r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Credit card-like
        ],
        description="Prevent sharing of PII in public channels",
    ))

    formatter = ModerationFormatter()
    test_cases = [
        "Hello, I need help with my account.",
        "This product is terrible, you're all incompetent!",
        "I want to end my life, nothing matters anymore.",
        "My SSN is 123-45-6789 and my card is 4111 1111 1111 1111.",
        "I think those people should be eliminated from society.",
        "Can you help me reset my password? I'm locked out.",
    ]

    for i, text in enumerate(test_cases, 1):
        decision = pipeline.moderate(text, content_id=f"test_{i:03d}")
        status = "[OK] ALLOWED" if decision.is_allowed else "[X] BLOCKED"
        print(f"\n  [{i}] \"{text[:55]}{'...' if len(text) > 55 else ''}\"")
        print(f"      {status} | Severity: {decision.overall_severity.name}")
        print(f"      Action: {decision.action_taken}")
        if decision.category_results:
            categories = ", ".join(r.category.name for r in decision.category_results)
            print(f"      Categories: {categories}")

    # Show pipeline statistics
    print(f"\n  Pipeline Statistics:")
    print(f"    Total decisions: {len(pipeline.decision_log)}")
    print(f"    Blocked: {sum(1 for d in pipeline.decision_log if not d.is_allowed)}")
    print(f"    In review queue: {len(pipeline.review_queue)}")


def demo_formatter():
    """Demonstrate the output formatter."""
    print("\n" + "=" * 72)
    print("DEMO 6: Moderation Output Formatting")
    print("=" * 72)

    pipeline = ModerationPipeline()
    pipeline.add_moderator(ViolenceModerator())

    decision = pipeline.moderate(
        "I will kill you if you don't comply with my demands.",
        content_id="format_test_001",
    )

    formatter = ModerationFormatter()

    print("\n  Human-readable format:")
    print("  " + "-" * 50)
    formatted = formatter.format_decision(decision)
    for line in formatted.split("\n"):
        print(f"  {line}")

    print("\n  API response format:")
    print("  " + "-" * 50)
    api_response = formatter.format_api_response(decision)
    print(f"  {json.dumps(api_response, indent=4)[:300]}...")


# =============================================================================
# Section 11: Best Practices
# =============================================================================

BEST_PRACTICES = {
    "Architecture": [
        "Use multiple independent moderators for different content types",
        "Implement a pipeline pattern where each stage filters specific content",
        "Support both rule-based and ML-based detection",
        "Design for graceful degradation - if one moderator fails, others continue",
    ],
    "Severity & Escalation": [
        "Define clear severity levels with documented thresholds",
        "Implement automatic escalation for high-severity content",
        "Maintain a human-in-the-loop review queue for edge cases",
        "Track false positive rates to tune thresholds",
    ],
    "Custom Policies": [
        "Make policies configurable without code changes",
        "Support exceptions and context-aware rules",
        "Version control policy definitions",
        "A/B test policy changes before full rollout",
    ],
    "User Experience": [
        "Provide clear, non-judgmental explanations for content removal",
        "Offer appeal mechanisms for false positives",
        "Include crisis resources for self-harm content",
        "Respect context - educational/medical discussions may use strong language",
    ],
}


def print_best_practices():
    """Print the best practices reference."""
    print("\n" + "=" * 72)
    print("CONTENT MODERATION BEST PRACTICES")
    print("=" * 72)

    for category, practices in BEST_PRACTICES.items():
        print(f"\n  {category}:")
        for i, practice in enumerate(practices, 1):
            print(f"    {i}. {practice}")


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    print("AI Security Exercise 02: Content Moderation Systems")
    print("=" * 72)

    demo_hate_speech_detection()
    demo_violence_detection()
    demo_self_harm_detection()
    demo_custom_policies()
    demo_full_pipeline()
    demo_formatter()
    print_best_practices()

    print("\n" + "=" * 72)
    print("Exercise complete. Review the code for implementation details.")
    print("=" * 72)
