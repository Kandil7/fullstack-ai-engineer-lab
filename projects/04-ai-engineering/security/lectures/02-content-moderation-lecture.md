# Lecture 02: Content Moderation

## Topic Overview

Content moderation in AI systems involves detecting, filtering, and managing harmful, inappropriate, or policy-violating content in both inputs and outputs. This lecture covers toxicity detection, NSFW filtering, hate speech detection, policy enforcement frameworks, and building robust moderation pipelines. Content moderation is essential for maintaining user safety, legal compliance, and platform integrity.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand** the taxonomy of harmful content categories
2. **Implement** multi-layer content moderation systems
3. **Configure** toxicity detection using multiple approaches
4. **Build** custom content policies for specific use cases
5. **Evaluate** moderation system effectiveness (precision/recall tradeoffs)
6. **Handle** edge cases like context-dependent content and cultural differences
7. **Design** human-in-the-loop moderation workflows

---

## Key Concepts

### 1. Content Taxonomy

Understanding the categories of content that need moderation:

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class ContentCategory(Enum):
    """Categories of harmful content."""
    HATE_SPEECH = "hate_speech"
    HARASSMENT = "harassment"
    VIOLENCE = "violence"
    SEXUAL_CONTENT = "sexual_content"
    SELF_HARM = "self_harm"
    MISINFORMATION = "misinformation"
    SPAM = "spam"
    PII_EXPOSURE = "pii_exposure"
    ILLEGAL_ACTIVITY = "illegal_activity"
    COPYRIGHT_VIOLATION = "copyright_violation"

class SeverityLevel(Enum):
    """Severity of content violation."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ModerationResult:
    """Result of content moderation analysis."""
    category: ContentCategory
    severity: SeverityLevel
    confidence: float
    flagged: bool
    explanation: Optional[str] = None

@dataclass
class ModerationPolicy:
    """Content moderation policy configuration."""
    name: str
    categories: List[ContentCategory]
    threshold: float  # Confidence threshold for flagging
    action: str  # "block", "warn", "log", "human_review"

# Example policy configuration
default_policy = ModerationPolicy(
    name="default_safety",
    categories=list(ContentCategory),
    threshold=0.7,
    action="block",
)

strict_policy = ModerationPolicy(
    name="strict_safety",
    categories=list(ContentCategory),
    threshold=0.5,  # Lower threshold = more aggressive filtering
    action="block",
)

permissive_policy = ModerationPolicy(
    name="permissive",
    categories=[ContentCategory.ILLEGAL_ACTIVITY, ContentCategory.SELF_HARM],
    threshold=0.9,  # Higher threshold = less filtering
    action="warn",
)
```

### 2. Toxicity Detection Methods

#### Method 1: Rule-Based Detection

```python
import re
from typing import Dict, List

class RuleBasedModerator:
    """Simple rule-based content moderation."""

    def __init__(self):
        # Define patterns for different content categories
        self.patterns = {
            ContentCategory.HATE_SPEECH: [
                r'\b(hate|kill|exterminate)\s+(all\s+)?(jews|muslims|christians|blacks|whites|asians|gays|lesbians)',
                r'\b(heil|sieg)\s+',
                # Add more patterns as needed (use responsibly)
            ],
            ContentCategory.HARASSMENT: [
                r'\b(you\s+(are|should)\s+(die|kill\s+yourself|suffer))',
                r'\b(stupid|idiot|moron)\s+(person|human|you)',
            ],
            ContentCategory.SELF_HARM: [
                r'\b(kill\s+myself|end\s+my\s+life|suicide\s+(method|ways|how))',
                r'\b(cutting\s+myself|self[-\s]harm\s+(method|how))',
            ],
            ContentCategory.ILLEGAL_ACTIVITY: [
                r'\b(how\s+to\s+(make|build|create)\s+(bomb|explosive|drug))',
                r'\b(buy\s+(drugs|weapons|stolen))',
            ],
        }

    def check(self, text: str) -> List[ModerationResult]:
        """Check text against all rules."""
        results = []

        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    results.append(ModerationResult(
                        category=category,
                        severity=SeverityLevel.HIGH,
                        confidence=0.9,
                        flagged=True,
                        explanation=f"Matched pattern: {pattern[:50]}...",
                    ))
                    break  # One match per category is enough

        return results
```

#### Method 2: ML-Based Detection

```python
# Using a pre-trained toxicity classifier
from transformers import pipeline

class MLBasedModerator:
    """Machine learning based content moderation."""

    def __init__(self):
        # Load pre-trained toxicity classifier
        self.classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            top_k=None  # Return all scores
        )

        # Thresholds for different categories
        self.thresholds = {
            "toxic": 0.7,
            "severe_toxic": 0.5,
            "obscene": 0.7,
            "threat": 0.6,
            "insult": 0.7,
            "identity_hate": 0.6,
        }

    def check(self, text: str) -> List[ModerationResult]:
        """Check text using ML classifier."""
        results = []

        # Get predictions
        predictions = self.classifier(text)

        if predictions and isinstance(predictions[0], list):
            predictions = predictions[0]

        for pred in predictions:
            label = pred["label"].lower()
            score = pred["score"]

            # Map label to our category
            category = self._map_label_to_category(label)
            threshold = self.thresholds.get(label, 0.7)

            if score >= threshold:
                results.append(ModerationResult(
                    category=category,
                    severity=self._score_to_severity(score),
                    confidence=score,
                    flagged=True,
                    explanation=f"ML model detected '{label}' with confidence {score:.2f}",
                ))

        return results

    def _map_label_to_category(self, label: str) -> ContentCategory:
        """Map model label to our content category."""
        mapping = {
            "toxic": ContentCategory.HARASSMENT,
            "severe_toxic": ContentCategory.HARASSMENT,
            "obscene": ContentCategory.HATE_SPEECH,
            "threat": ContentCategory.VIOLENCE,
            "insult": ContentCategory.HARASSMENT,
            "identity_hate": ContentCategory.HATE_SPEECH,
        }
        return mapping.get(label, ContentCategory.HARASSMENT)

    def _score_to_severity(self, score: float) -> SeverityLevel:
        """Convert confidence score to severity level."""
        if score >= 0.9:
            return SeverityLevel.CRITICAL
        elif score >= 0.7:
            return SeverityLevel.HIGH
        elif score >= 0.5:
            return SeverityLevel.MEDIUM
        else:
            return SeverityLevel.LOW
```

#### Method 3: LLM-Based Moderation

```python
import openai
import json

class LLMModerator:
    """Use an LLM for nuanced content moderation."""

    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def check(self, text: str) -> List[ModerationResult]:
        """Use GPT to analyze content for policy violations."""

        prompt = f"""Analyze the following text for content policy violations.

Text to analyze:
\"\"\"
{text}
\"\"\"

Evaluate for these categories:
1. Hate speech or discrimination
2. Harassment or bullying
3. Violence or graphic content
4. Sexual or explicit content
5. Self-harm or suicide
6. Misinformation or deception
7. Spam or manipulation
8. Personal information exposure
9. Illegal activity promotion
10. Copyright infringement

For each category that has a violation, provide:
- category: category name
- severity: none/low/medium/high/critical
- confidence: 0.0 to 1.0
- explanation: brief explanation

Return as JSON array. If no violations found, return empty array [].
Only return the JSON, no other text."""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,  # Deterministic for moderation
        )

        try:
            violations = json.loads(response.choices[0].message.content)
            return [self._parse_violation(v) for v in violations]
        except (json.JSONDecodeError, KeyError):
            return []

    def _parse_violation(self, violation: dict) -> ModerationResult:
        """Parse a violation dict into ModerationResult."""
        category_map = {
            "hate speech": ContentCategory.HATE_SPEECH,
            "harassment": ContentCategory.HARASSMENT,
            "violence": ContentCategory.VIOLENCE,
            "sexual": ContentCategory.SEXUAL_CONTENT,
            "self-harm": ContentCategory.SELF_HARM,
            "misinformation": ContentCategory.MISINFORMATION,
            "spam": ContentCategory.SPAM,
            "personal information": ContentCategory.PII_EXPOSURE,
            "illegal": ContentCategory.ILLEGAL_ACTIVITY,
            "copyright": ContentCategory.COPYRIGHT_VIOLATION,
        }

        severity_map = {
            "none": SeverityLevel.NONE,
            "low": SeverityLevel.LOW,
            "medium": SeverityLevel.MEDIUM,
            "high": SeverityLevel.HIGH,
            "critical": SeverityLevel.CRITICAL,
        }

        return ModerationResult(
            category=category_map.get(
                violation.get("category", "").lower(),
                ContentCategory.HARASSMENT
            ),
            severity=severity_map.get(
                violation.get("severity", "low").lower(),
                SeverityLevel.LOW
            ),
            confidence=float(violation.get("confidence", 0.5)),
            flagged=True,
            explanation=violation.get("explanation"),
        )
```

### 3. Multi-Layer Moderation Pipeline

```python
from dataclasses import dataclass
from typing import List, Optional, Callable
import logging

logger = logging.getLogger(__name__)

@dataclass
class ModerationConfig:
    """Configuration for the moderation pipeline."""
    enable_rule_based: bool = True
    enable_ml_based: bool = True
    enable_llm_based: bool = False  # More expensive, use selectively
    threshold: float = 0.7
    action_on_flag: str = "block"  # "block", "warn", "log", "human_review"
    max_text_length: int = 10000
    log_all_results: bool = True

class ModerationPipeline:
    """Multi-layer content moderation pipeline."""

    def __init__(self, config: ModerationConfig):
        self.config = config
        self.moderators = []

        if config.enable_rule_based:
            self.moderators.append(("rule_based", RuleBasedModerator()))
        if config.enable_ml_based:
            self.moderators.append(("ml_based", MLBasedModerator()))
        if config.enable_llm_based:
            self.moderators.append(("llm_based", LLMModerator(api_key="...")))

    def moderate(self, text: str, context: Optional[dict] = None) -> dict:
        """
        Run content through the moderation pipeline.

        Args:
            text: Content to moderate
            context: Additional context (user_id, conversation_id, etc.)

        Returns:
            dict with results, action, and metadata
        """
        # Input validation
        if not text or not text.strip():
            return {"action": "allow", "results": [], "reason": "empty_input"}

        if len(text) > self.config.max_text_length:
            return {"action": "block", "results": [], "reason": "input_too_long"}

        all_results = []
        pipeline_log = []

        # Run through each moderator layer
        for name, moderator in self.moderators:
            try:
                results = moderator.check(text)
                pipeline_log.append({
                    "layer": name,
                    "results_count": len(results),
                    "flagged": any(r.flagged for r in results),
                })
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Moderation layer {name} failed: {e}")
                pipeline_log.append({
                    "layer": name,
                    "error": str(e),
                })

        # Determine final action
        action = self._determine_action(all_results)

        # Log if configured
        if self.config.log_all_results:
            self._log_moderation(text, all_results, action, context)

        return {
            "action": action,
            "results": all_results,
            "pipeline_log": pipeline_log,
            "flagged_categories": list(set(r.category.value for r in all_results if r.flagged)),
            "max_severity": max((r.severity.value for r in all_results), default=0),
        }

    def _determine_action(self, results: List[ModerationResult]) -> str:
        """Determine the action based on moderation results."""
        flagged = [r for r in results if r.flagged]

        if not flagged:
            return "allow"

        # Check for critical severity
        if any(r.severity == SeverityLevel.CRITICAL for r in flagged):
            return "block"

        # Check for high severity
        if any(r.severity == SeverityLevel.HIGH for r in flagged):
            return self.config.action_on_flag

        # Check confidence threshold
        max_confidence = max(r.confidence for r in flagged)
        if max_confidence >= self.config.threshold:
            return self.config.action_on_flag

        return "allow"

    def _log_moderation(self, text: str, results: List[ModerationResult],
                        action: str, context: Optional[dict]):
        """Log moderation results for audit."""
        logger.info(f"Moderation: action={action}, "
                    f"results={len(results)}, "
                    f"context={context}")
```

### 4. Context-Aware Moderation

```python
class ContextAwareModerator:
    """Moderate content with awareness of conversation context."""

    def __init__(self):
        self.conversation_history = {}

    def moderate_with_context(self, text: str, user_id: str,
                              conversation_id: str) -> dict:
        """Moderate considering conversation context."""

        # Get conversation history
        history = self.conversation_history.get(conversation_id, [])

        # Analyze context
        context_analysis = self._analyze_context(text, history)

        # Adjust moderation based on context
        adjusted_result = self._apply_context_adjustments(
            text, context_analysis
        )

        # Store in history
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = []
        self.conversation_history[conversation_id].append({
            "text": text,
            "user_id": user_id,
            "moderation_result": adjusted_result,
        })

        return adjusted_result

    def _analyze_context(self, text: str, history: list) -> dict:
        """Analyze the context of the conversation."""

        analysis = {
            "is_escalating": False,
            "topic_drift": False,
            "repeated_violations": False,
            "sensitive_topic": False,
        }

        # Check for escalation patterns
        if len(history) >= 3:
            recent_texts = [h["text"] for h in history[-3:]]
            # Simple escalation detection
            violation_count = sum(
                1 for h in history[-3:]
                if h.get("moderation_result", {}).get("action") != "allow"
            )
            if violation_count >= 2:
                analysis["repeated_violations"] = True

        # Check for sensitive topics
        sensitive_keywords = ["suicide", "self-harm", "abuse", "violence"]
        if any(keyword in text.lower() for keyword in sensitive_keywords):
            analysis["sensitive_topic"] = True

        return analysis

    def _apply_context_adjustments(self, text: str, context: dict) -> dict:
        """Apply moderation adjustments based on context."""

        base_result = self._base_moderation(text)

        if context["repeated_violations"]:
            # Stricter moderation for repeat offenders
            base_result["threshold_adjusted"] = True
            base_result["note"] = "Adjusted for repeated violations"

        if context["sensitive_topic"]:
            # Special handling for sensitive topics
            base_result["sensitive_topic"] = True
            base_result["note"] = "Sensitive topic detected - review recommended"

        return base_result

    def _base_moderation(self, text: str) -> dict:
        """Perform base moderation."""
        # Simplified - would use the full pipeline
        return {"action": "allow", "results": []}
```

### 5. Human-in-the-Loop Moderation

```python
from datetime import datetime
from typing import Optional
import uuid

class HumanInTheLoopModerator:
    """Moderation system with human review queue."""

    def __init__(self):
        self.review_queue = []
        self.review_decisions = {}

    def submit_for_review(self, content: str, automated_result: dict,
                          context: Optional[dict] = None) -> str:
        """Submit content for human review."""

        review_id = str(uuid.uuid4())

        review_item = {
            "id": review_id,
            "content": content,
            "automated_result": automated_result,
            "context": context or {},
            "submitted_at": datetime.utcnow().isoformat(),
            "status": "pending",
            "reviewer": None,
            "decision": None,
            "notes": None,
        }

        self.review_queue.append(review_item)
        return review_id

    def get_pending_reviews(self, limit: int = 10) -> list:
        """Get pending items for human review."""
        return [
            item for item in self.review_queue
            if item["status"] == "pending"
        ][:limit]

    def submit_decision(self, review_id: str, reviewer: str,
                        decision: str, notes: Optional[str] = None):
        """Submit a human review decision."""

        for item in self.review_queue:
            if item["id"] == review_id:
                item["status"] = "reviewed"
                item["reviewer"] = reviewer
                item["decision"] = decision  # "allow", "block", "escalate"
                item["notes"] = notes
                item["reviewed_at"] = datetime.utcnow().isoformat()

                # Store decision for learning
                self.review_decisions[review_id] = {
                    "content_hash": hash(item["content"]),
                    "automated_result": item["automated_result"],
                    "human_decision": decision,
                }
                break

    def get_review_statistics(self) -> dict:
        """Get statistics about human reviews."""
        reviewed = [i for i in self.review_queue if i["status"] == "reviewed"]
        pending = [i for i in self.review_queue if i["status"] == "pending"]

        decisions = {}
        for item in reviewed:
            d = item["decision"]
            decisions[d] = decisions.get(d, 0) + 1

        return {
            "total_reviewed": len(reviewed),
            "total_pending": len(pending),
            "decision_distribution": decisions,
            "average_review_time": self._calculate_avg_review_time(reviewed),
        }

    def _calculate_avg_review_time(self, reviewed_items: list) -> float:
        """Calculate average time to review."""
        if not reviewed_items:
            return 0.0

        times = []
        for item in reviewed_items:
            submitted = datetime.fromisoformat(item["submitted_at"])
            reviewed = datetime.fromisoformat(item["reviewed_at"])
            times.append((reviewed - submitted).total_seconds())

        return sum(times) / len(times) if times else 0.0
```

### 6. Evaluation Metrics

```python
class ModerationEvaluator:
    """Evaluate moderation system performance."""

    def __init__(self):
        self.predictions = []
        self.ground_truth = []

    def add_evaluation(self, text: str, predicted: bool, actual: bool):
        """Add an evaluation sample."""
        self.predictions.append(predicted)
        self.ground_truth.append(actual)

    def calculate_metrics(self) -> dict:
        """Calculate precision, recall, F1, and other metrics."""
        tp = sum(1 for p, a in zip(self.predictions, self.ground_truth)
                 if p and a)
        fp = sum(1 for p, a in zip(self.predictions, self.ground_truth)
                 if p and not a)
        fn = sum(1 for p, a in zip(self.predictions, self.ground_truth)
                 if not p and a)
        tn = sum(1 for p, a in zip(self.predictions, self.ground_truth)
                 if not p and not a)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) \
            if (precision + recall) > 0 else 0

        accuracy = (tp + tn) / len(self.predictions) \
            if self.predictions else 0

        return {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "accuracy": accuracy,
            "total_samples": len(self.predictions),
        }

    def analyze_errors(self) -> dict:
        """Analyze types of errors."""
        false_positives = []
        false_negatives = []

        for i, (pred, actual) in enumerate(
            zip(self.predictions, self.ground_truth)
        ):
            if pred and not actual:
                false_positives.append(i)
            elif not pred and actual:
                false_negatives.append(i)

        return {
            "false_positive_count": len(false_positives),
            "false_negative_count": len(false_negatives),
            "false_positive_rate": len(false_positives) / len(self.predictions)
                if self.predictions else 0,
            "false_negative_rate": len(false_negatives) / len(self.predictions)
                if self.predictions else 0,
        }
```

---

## Common Mistakes to Avoid

1. **Over-reliance on keyword filtering** — Misses context, generates false positives
2. **Ignoring cultural context** — Content may be offensive in one culture but acceptable in another
3. **No human review queue** — Automated systems need human oversight for edge cases
4. **Single-language moderation** — Attackers may use other languages to bypass filters
5. **Not evaluating regularly** — Content moderation models degrade over time
6. **Ignoring false positives** — Over-moderation frustrates legitimate users
7. **No appeal mechanism** — Users should be able to contest moderation decisions
8. **Static policies** — Content threats evolve; policies must evolve too

---

## Best Practices

1. **Multi-layer approach**: Combine rule-based, ML, and LLM-based moderation
2. **Context-aware moderation**: Consider conversation history and user patterns
3. **Human-in-the-loop**: Maintain review queues for edge cases
4. **Regular evaluation**: Continuously measure precision, recall, and F1
5. **Appeal mechanism**: Allow users to contest moderation decisions
6. **Transparent policies**: Clearly communicate content policies to users
7. **Cultural sensitivity**: Consider regional and cultural differences
8. **Audit logging**: Log all moderation decisions for compliance and improvement

---

## Practice Exercises

### Exercise 1: Build a Basic Moderator (Easy)
Create a rule-based moderator that detects at least 5 categories of harmful content.

### Exercise 2: ML Integration (Medium)
Integrate a pre-trained toxicity classifier and calibrate thresholds for your use case.

### Exercise 3: Human Review Queue (Medium)
Build a human-in-the-loop moderation system with review queue and statistics.

### Exercise 4: Evaluation Pipeline (Hard)
Create a comprehensive evaluation pipeline that measures moderation accuracy across different content types and edge cases.

---

## Summary

Content moderation is essential for safe AI systems. Key takeaways:

- **Multi-layer moderation** combines rule-based, ML, and LLM approaches
- **Context matters** — the same content may be acceptable in different contexts
- **Human oversight** is essential for edge cases and policy evolution
- **Evaluation is ongoing** — regularly measure and improve moderation accuracy
- **Balance safety with usability** — avoid over-moderation that frustrates legitimate users

---

## References

- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [Google Jigsaw Perspective API](https://perspectiveapi.com/)
- [Anthropic Content Policy](https://www.anthropic.com/policies)
