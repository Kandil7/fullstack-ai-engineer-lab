# Glossary 02: Content Moderation Terms

## Quick Reference Table

| Term | Category | Importance | See Also |
|------|----------|------------|----------|
| Content Moderation | Process | Critical | Content Policy |
| Toxicity Detection | Technique | Critical | Hate Speech, Harassment |
| NSFW Filtering | Technique | High | Sexual Content |
| Hate Speech | Content Type | Critical | Discrimination, Bias |
| Harassment | Content Type | Critical | Bullying, Cyberbullying |
| Content Policy | Governance | Critical | Community Guidelines |
| False Positive | Metric | High | Precision, Over-moderation |
| False Negative | Metric | High | Recall, Under-moderation |
| Human-in-the-Loop | Process | High | Review Queue |
| Moderation Pipeline | Architecture | Critical | Multi-layer |
| Context Awareness | Technique | High | Conversation History |
| Appeal Mechanism | Process | Medium | Due Process |
| Bias Detection | Process | Critical | Fairness |
| Cultural Sensitivity | Principle | High | Localization |
| Over-moderation | Problem | High | False Positive |
| Under-moderation | Problem | High | False Negative |

---

## Alphabetical Definitions

### Appeal Mechanism

**Definition**: A process that allows users to contest moderation decisions they believe were made in error. Essential for fairness and user trust.

**Example**:
```python
class AppealSystem:
    def __init__(self):
        self.appeals = []

    def submit_appeal(self, moderation_id: str, user_id: str,
                      reason: str) -> str:
        """User submits an appeal against a moderation decision."""
        appeal_id = f"appeal_{len(self.appeals) + 1}"
        self.appeals.append({
            "id": appeal_id,
            "moderation_id": moderation_id,
            "user_id": user_id,
            "reason": reason,
            "status": "pending",
            "submitted_at": datetime.utcnow(),
        })
        return appeal_id

    def review_appeal(self, appeal_id: str, reviewer: str,
                      decision: str, notes: str):
        """Human reviewer decides on the appeal."""
        for appeal in self.appeals:
            if appeal["id"] == appeal_id:
                appeal["status"] = decision  # "upheld", "overturned"
                appeal["reviewer"] = reviewer
                appeal["notes"] = notes
                appeal["reviewed_at"] = datetime.utcnow()
                return
```

**Related Terms**: Human-in-the-Loop, Due Process, User Trust

---

### Bias Detection

**Definition**: The process of identifying systematic unfairness in content moderation systems, such as disproportionately flagging content from certain demographic groups.

**Example**:
```python
class BiasDetector:
    def analyze_demographic_bias(self, moderation_results: list,
                                  demographic_data: dict) -> dict:
        """Analyze if moderation decisions show demographic bias."""
        # Group results by demographic
        group_stats = {}
        for result in moderation_results:
            user_id = result["user_id"]
            demo = demographic_data.get(user_id, "unknown")
            if demo not in group_stats:
                group_stats[demo] = {"flagged": 0, "total": 0}
            group_stats[demo]["total"] += 1
            if result["flagged"]:
                group_stats[demo]["flagged"] += 1

        # Calculate flag rates per group
        flag_rates = {}
        for group, stats in group_stats.items():
            flag_rates[group] = (
                stats["flagged"] / stats["total"]
                if stats["total"] > 0 else 0
            )

        # Identify disparities
        max_rate = max(flag_rates.values()) if flag_rates else 0
        min_rate = min(flag_rates.values()) if flag_rates else 0
        disparity_ratio = max_rate / min_rate if min_rate > 0 else float('inf')

        return {
            "flag_rates_by_group": flag_rates,
            "disparity_ratio": disparity_ratio,
            "potential_bias": disparity_ratio > 2.0,  # Threshold
        }
```

**Related Terms**: Fairness, Discrimination, Over-moderation

---

### Community Guidelines

**Definition**: Published rules that define what content is allowed on a platform. Clear guidelines help users understand expectations and provide a basis for moderation decisions.

**Example**:
```python
community_guidelines = {
    "prohibited": [
        "Hate speech targeting protected groups",
        "Harassment or bullying of individuals",
        "Graphic violence or gore",
        "Non-consensual sexual content",
        "Promotion of self-harm or suicide",
        "Misinformation about public health",
        "Spam or deceptive practices",
    ],
    "restricted": [
        "Profanity (requires age-gating)",
        "Political content (may be limited in certain contexts)",
        "Violent content (requires content warnings)",
    ],
    "allowed": [
        "Constructive criticism",
        "Educational content about sensitive topics",
        "News reporting",
        "Artistic expression",
    ],
}
```

**Related Terms**: Content Policy, Moderation Rules, Transparency

---

### Context Awareness

**Definition**: The ability of a moderation system to consider the context in which content appears, including conversation history, user intent, and situational factors.

**Example**:
```python
class ContextAwareModerator:
    def moderate_with_context(self, text: str, conversation_history: list):
        """Consider context when moderating."""
        # Check for educational/medical context
        medical_context = any(
            "doctor" in msg.lower() or "medical" in msg.lower()
            for msg in conversation_history[-3:]
        )

        # Check for news reporting context
        news_context = any(
            "article" in msg.lower() or "news" in msg.lower()
            for msg in conversation_history[-3:]
        )

        # Adjust moderation based on context
        if medical_context and "symptom" in text.lower():
            return {"action": "allow", "context_note": "medical_context"}
        elif news_context and "violence" in text.lower():
            return {"action": "allow", "context_note": "news_context"}

        # Default moderation
        return self.default_moderation(text)
```

**Related Terms**: Conversation History, Situational Context, Nuance

---

### Content Policy

**Definition**: Internal rules and guidelines that define what content an AI system will and won't generate, process, or facilitate.

**Example**:
```python
class ContentPolicy:
    def __init__(self):
        self.rules = {
            "generate_harmful_content": {
                "action": "block",
                "categories": ["violence", "illegal_activity", "self_harm"],
                "message": "I can't help with that request.",
            },
            "reveal_sensitive_info": {
                "action": "block",
                "categories": ["pii", "credentials", "system_info"],
                "message": "I can't share that information.",
            },
            "external_content": {
                "action": "moderate",
                "categories": ["hate_speech", "harassment", "misinformation"],
                "message": "This content may violate our policies.",
            },
        }

    def evaluate_request(self, request_type: str, content: str) -> dict:
        """Evaluate a request against content policy."""
        rule = self.rules.get(request_type, {"action": "allow"})
        return {
            "action": rule["action"],
            "message": rule.get("message", ""),
            "categories": rule.get("categories", []),
        }
```

**Related Terms**: Community Guidelines, Moderation Rules, Acceptable Use

---

### Content Warning

**Definition**: A label or notification applied to content that may be disturbing or sensitive, allowing users to make informed choices about viewing it.

**Example**:
```python
class ContentWarningSystem:
    WARNING_TYPES = {
        "violence": "⚠️ This content contains descriptions of violence.",
        "medical": "🏥 This content contains medical information.",
        "spoiler": "🎬 This content contains spoilers.",
        "nsfw": "🔞 This content may not be suitable for all audiences.",
        "trigger": "⚠️ This content may be triggering for some users.",
    }

    def add_warning(self, content: str, warning_type: str) -> dict:
        """Add a content warning to content."""
        warning = self.WARNING_TYPES.get(warning_type, "")
        return {
            "content": content,
            "warning": warning,
            "warning_type": warning_type,
            "user_choice": "show",  # User can choose to hide
        }
```

**Related Terms**: NSFW Filtering, Sensitive Content, User Choice

---

### Discrimination

**Definition**: Unfair or prejudicial treatment of content based on protected characteristics such as race, gender, religion, or sexual orientation. Moderation systems must avoid discriminating while still catching harmful content.

**Example**:
```python
# Example of biased moderation (BAD)
biased_keywords = ["gay", "lesbian", "transgender"]  # Flagging identity terms
# This would unfairly flag content from LGBTQ+ users

# Example of fair moderation (GOOD)
fair_keywords = ["hate", "kill", "exterminate"] + ["gay", "lesbian", "transgender"]
# Only flag when identity terms appear with hate/violence keywords
# e.g., "kill gay people" vs "I'm gay and proud"
```

**Related Terms**: Bias Detection, Fairness, Protected Groups

---

### Fairness

**Definition**: The principle that content moderation should treat all users and content equally regardless of demographic characteristics, political views, or other protected attributes.

**Example**:
```python
class FairnessEvaluator:
    def evaluate_fairness(self, moderation_results: list) -> dict:
        """Evaluate fairness across different groups."""
        # Measure false positive rates across demographic groups
        # Measure false negative rates across demographic groups
        # Ensure disparities are within acceptable bounds

        metrics = {
            "equal_opportunity": self._equal_opportunity(moderation_results),
            "demographic_parity": self._demographic_parity(moderation_results),
            "calibration": self._calibration(moderation_results),
        }
        return metrics

    def _equal_opportunity(self, results: list) -> float:
        """Equal opportunity: same true positive rate across groups."""
        # Implementation would compare TPR across groups
        pass
```

**Related Terms**: Bias Detection, Discrimination, Equity

---

### False Negative

**Definition**: When a moderation system fails to detect harmful content that should have been flagged. False negatives allow harmful content to pass through.

**Example**:
```python
# False negative example
harmful_content = "I know a way to hurt people that won't get flagged"
# Moderation system returns: {"flagged": False}
# But the content is actually harmful
# This is a false negative

# Impact analysis
false_negatives = {
    "user_harm": "Harmful content reaches users",
    "legal_liability": "Platform may be liable",
    "trust_damage": "Users lose trust in safety",
}
```

**Related Terms**: Recall, Under-moderation, Missed Detection

---

### False Positive

**Definition**: When a moderation system incorrectly flags benign content as harmful. False positives frustrate legitimate users and can lead to censorship concerns.

**Example**:
```python
# False positive example
benign_content = "I'm learning about cybersecurity and ethical hacking"
# Moderation system returns: {"flagged": True, "reason": "hacking content"}
# But the content is actually educational and benign
# This is a false positive

# Impact analysis
false_positives = {
    "user_frustration": "Legitimate users get blocked",
    "over_moderation": "System is too aggressive",
    "chilling_effect": "Users self-censor to avoid flags",
}
```

**Related Terms**: Precision, Over-moderation, Censorship

---

### F1 Score

**Definition**: The harmonic mean of precision and recall, providing a single metric that balances both false positives and false negatives. Used to evaluate overall moderation system performance.

**Example**:
```python
def calculate_f1(true_positives: int, false_positives: int,
                  false_negatives: int) -> float:
    """Calculate F1 score."""
    precision = true_positives / (true_positives + false_positives) \
        if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) \
        if (true_positives + false_negatives) > 0 else 0

    f1 = 2 * (precision * recall) / (precision + recall) \
        if (precision + recall) > 0 else 0
    return f1

# Example
tp, fp, fn = 85, 10, 5
f1 = calculate_f1(tp, fp, fn)
print(f"F1 Score: {f1:.2f}")  # F1 Score: 0.92
```

**Related Terms**: Precision, Recall, Accuracy

---

### Human-in-the-Loop

**Definition**: A moderation approach where automated systems handle obvious cases but uncertain or edge cases are escalated to human reviewers for final decisions.

**Example**:
```python
class HumanInTheLoop:
    def __init__(self):
        self.auto_allow_threshold = 0.3   # Below this = auto allow
        self.auto_block_threshold = 0.9   # Above this = auto block
        self.review_threshold = 0.3       # Between = human review

    def moderate(self, content: str, confidence: float) -> dict:
        """Route content based on confidence."""
        if confidence < self.auto_allow_threshold:
            return {"action": "allow", "reason": "low_risk"}
        elif confidence > self.auto_block_threshold:
            return {"action": "block", "reason": "high_risk"}
        else:
            # Route to human review
            review_id = self.queue_for_review(content, confidence)
            return {
                "action": "pending_review",
                "review_id": review_id,
                "reason": "uncertain_risk",
            }
```

**Related Terms**: Review Queue, Automated Moderation, Escalation

---

### Human Review Queue

**Definition**: A prioritized list of content items waiting for human reviewer decisions, typically ordered by risk level and user impact.

**Example**:
```python
class ReviewQueue:
    def __init__(self):
        self.queue = []

    def add_item(self, content: str, confidence: float,
                 user_id: str, priority: str = "normal"):
        """Add item to review queue."""
        self.queue.append({
            "content": content,
            "confidence": confidence,
            "user_id": user_id,
            "priority": priority,
            "added_at": datetime.utcnow(),
            "status": "pending",
        })
        # Sort by priority and confidence
        self.queue.sort(key=lambda x: (
            {"high": 0, "normal": 1, "low": 2}[x["priority"]],
            -x["confidence"]
        ))

    def get_next(self) -> dict:
        """Get next item for review."""
        for item in self.queue:
            if item["status"] == "pending":
                item["status"] = "in_review"
                return item
        return None
```

**Related Terms**: Human-in-the-Loop, Escalation, Prioritization

---

### Moderation Pipeline

**Definition**: The complete system architecture for processing content through multiple moderation stages, from initial detection through final action.

**Example**:
```python
class ModerationPipeline:
    def __init__(self):
        self.stages = [
            ("preprocessing", self.preprocess),
            ("rule_based", self.rule_check),
            ("ml_classification", self.ml_classify),
            ("context_analysis", self.context_check),
            ("decision", self.make_decision),
            ("action", self.execute_action),
            ("logging", self.log_result),
        ]

    def process(self, content: str, context: dict) -> dict:
        """Process content through all pipeline stages."""
        data = {"content": content, "context": context, "flags": []}

        for stage_name, stage_func in self.stages:
            try:
                data = stage_func(data)
            except Exception as e:
                data["errors"] = data.get("errors", [])
                data["errors"].append({"stage": stage_name, "error": str(e)})

        return data
```

**Related Terms**: Multi-layer Moderation, Pipeline Architecture, Processing Stages

---

### Moderation Rules

**Definition**: Specific criteria used to determine whether content violates policies. Rules can be keyword-based, pattern-based, or ML-based.

**Example**:
```python
moderation_rules = {
    "hate_speech": {
        "type": "pattern",
        "patterns": [
            r"(kill|exterminate|remove)\s+(all\s+)?(jews|muslims|christians)",
            r"(heil|sieg)\s+",
        ],
        "severity": "high",
        "action": "block",
    },
    "harassment": {
        "type": "ml",
        "model": "toxicity-classifier",
        "threshold": 0.8,
        "severity": "high",
        "action": "block",
    },
    "spam": {
        "type": "keyword",
        "keywords": ["buy now", "click here", "free money"],
        "threshold": 3,  # Number of keyword matches
        "severity": "medium",
        "action": "flag",
    },
}
```

**Related Terms**: Content Policy, Detection Rules, Moderation Criteria

---

### NSFW Filtering

**Definition**: The process of detecting and filtering Not Safe For Work content, including sexually explicit material, graphic violence, or other content inappropriate for professional settings.

**Example**:
```python
class NSFWFilter:
    def __init__(self):
        self.categories = {
            "sexual_explicit": {"threshold": 0.9, "action": "block"},
            "sexual_suggestive": {"threshold": 0.7, "action": "warn"},
            "graphic_violence": {"threshold": 0.85, "action": "block"},
            "gore": {"threshold": 0.8, "action": "block"},
        }

    def check_image(self, image_path: str) -> dict:
        """Check image for NSFW content."""
        # Would use a vision model or NSFW classifier
        # Placeholder implementation
        return {"nsfw": False, "categories": []}

    def check_text(self, text: str) -> dict:
        """Check text for NSFW descriptions."""
        # Would use a text classifier
        # Placeholder implementation
        return {"nsfw": False, "categories": []}
```

**Related Terms**: Content Warning, Sensitive Content, Age-Gating

---

### Over-moderation

**Definition**: When a moderation system is too aggressive, blocking or flagging content that is actually acceptable. Can frustrate legitimate users and create censorship concerns.

**Example**:
```python
# Examples of over-moderation
over_moderation_examples = [
    {
        "content": "I'm a doctor discussing medical procedures",
        "flagged": True,
        "reason": "Contains medical terms (overly sensitive)",
        "impact": "Medical professional cannot share expertise",
    },
    {
        "content": "Historical account of WWII atrocities",
        "flagged": True,
        "reason": "Contains violence keywords (lacks context)",
        "impact": "Educational content blocked",
    },
    {
        "content": "I love my gay friends",
        "flagged": True,
        "reason": "Contains identity term (biased keywords)",
        "impact": "Supportive content blocked",
    },
]

# Solutions
solutions = [
    "Use context-aware moderation",
    "Implement human review for edge cases",
    "Calibrate thresholds carefully",
    "Regular bias auditing",
    "Provide appeal mechanisms",
]
```

**Related Terms**: False Positive, Precision, Censorship

---

### Precision

**Definition**: The ratio of correctly flagged harmful content to all flagged content. High precision means fewer false positives (benign content incorrectly flagged).

**Example**:
```python
def calculate_precision(true_positives: int, false_positives: int) -> float:
    """Calculate precision."""
    return true_positives / (true_positives + false_positives) \
        if (true_positives + false_positives) > 0 else 0

# Example
# 100 items flagged as harmful
# 90 actually harmful (true positives)
# 10 actually benign (false positives)
precision = calculate_precision(90, 10)
print(f"Precision: {precision:.2f}")  # Precision: 0.90
# 90% of flagged items were actually harmful
```

**Related Terms**: False Positive, Accuracy, Quality Metrics

---

### Recall

**Definition**: The ratio of correctly flagged harmful content to all actual harmful content. High recall means fewer false negatives (harmful content that slips through).

**Example**:
```python
def calculate_recall(true_positives: int, false_negatives: int) -> float:
    """Calculate recall."""
    return true_positives / (true_positives + false_negatives) \
        if (true_positives + false_negatives) > 0 else 0

# Example
# 100 harmful items in the dataset
# 90 correctly flagged (true positives)
# 10 missed (false negatives)
recall = calculate_recall(90, 10)
print(f"Recall: {recall:.2f}")  # Recall: 0.90
# 90% of harmful items were caught
```

**Related Terms**: False Negative, Sensitivity, Coverage

---

### Sensitive Content

**Definition**: Content that may be disturbing, triggering, or inappropriate for certain audiences, even if not strictly violating policies.

**Example**:
```python
sensitive_content_categories = {
    "medical": {
        "description": "Graphic medical procedures or conditions",
        "action": "content_warning",
        "age_restrict": True,
    },
    "violence": {
        "description": "Descriptions of violence or conflict",
        "action": "content_warning",
        "context_dependent": True,
    },
    "mental_health": {
        "description": "Discussion of self-harm, eating disorders",
        "action": "content_warning",
        "provide_resources": True,  # Add mental health resources
    },
}
```

**Related Terms**: Content Warning, NSFW Filtering, Trigger Warning

---

### Spam Detection

**Definition**: The process of identifying and filtering unsolicited, repetitive, or deceptive content designed to manipulate or annoy users.

**Example**:
```python
class SpamDetector:
    def __init__(self):
        self.spam_indicators = {
            "repeated_chars": r'(.)\1{4,}',  # More than 4 repeated chars
            "excessive_links": r'https?://\S+.*https?://\S+.*https?://\S+',
            "all_caps": r'^[A-Z\s!?]{20,}$',
            "common_spam": r'\b(buy now|click here|free money|act now)\b',
        }

    def is_spam(self, text: str) -> dict:
        """Check if text is spam."""
        import re
        matches = []
        for name, pattern in self.spam_indicators.items():
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(name)

        return {
            "is_spam": len(matches) >= 2,  # Multiple indicators
            "indicators": matches,
            "confidence": len(matches) / len(self.spam_indicators),
        }
```

**Related Terms**: Deceptive Content, Unsolicited Content, Manipulation

---

### Toxicity

**Definition**: A measure of how likely content is to be rude, disrespectful, or unreasonable enough to cause someone to leave a discussion. Toxicity detection is a core component of content moderation.

**Example**:
```python
# Toxicity scoring
toxicity_levels = {
    0.0: "No toxicity detected",
    0.3: "Mildly toxic - may cause discomfort",
    0.5: "Moderately toxic - likely to upset readers",
    0.7: "Highly toxic - will upset most readers",
    0.9: "Extremely toxic - clear violation",
}

# Categories of toxicity
toxicity_categories = {
    "toxic": "Rude, disrespectful, or unreasonable",
    "severe_toxic": "Very hateful or aggressive",
    "obscene": "Vulgar or profane language",
    "threat": "Statements of intent to harm",
    "insult": "Insulting or belittling language",
    "identity_hate": "Hate based on identity",
}
```

**Related Terms**: Hate Speech, Harassment, Abuse

---

### Trigger Warning

**Definition**: A notice placed before content that may cause emotional distress to some readers, particularly those with PTSD, anxiety, or other conditions.

**Example**:
```python
class TriggerWarningSystem:
    TRIGGER_CATEGORIES = {
        "abuse": "Content contains descriptions of abuse",
        "self_harm": "Content discusses self-harm",
        "eating_disorders": "Content discusses eating disorders",
        "violence": "Content contains descriptions of violence",
        "sexual_assault": "Content discusses sexual assault",
    }

    def analyze_triggers(self, text: str) -> list:
        """Analyze text for potential triggers."""
        triggers = []
        for category, description in self.TRIGGER_CATEGORIES.items():
            if self._contains_trigger(text, category):
                triggers.append({
                    "category": category,
                    "description": description,
                })
        return triggers

    def _contains_trigger(self, text: str, category: str) -> bool:
        """Check if text contains trigger for category."""
        # Would use ML model in practice
        # Simplified keyword check
        keywords = {
            "self_harm": ["cut", "harm", "hurt myself"],
            "violence": ["attack", "assault", "hurt"],
        }
        text_lower = text.lower()
        return any(kw in text_lower for kw in keywords.get(category, []))
```

**Related Terms**: Content Warning, Sensitive Content, Mental Health

---

### Under-moderation

**Definition**: When a moderation system is too lenient, allowing harmful content to pass through undetected. Can expose users to harm and create legal liability.

**Example**:
```python
# Examples of under-moderation
under_moderation_examples = [
    {
        "content": "Coded hate speech using dog whistles",
        "flagged": False,
        "reason": "System doesn't recognize coded language",
        "impact": "Hate speech reaches users",
    },
    {
        "content": "Subtle harassment using sarcasm",
        "flagged": False,
        "reason": "Sarcasm not detected",
        "impact": "Harassment goes unaddressed",
    },
    {
        "content": "Misinformation in a foreign language",
        "flagged": False,
        "reason": "System only supports English",
        "impact": "Misinformation spreads",
    },
]

# Solutions
solutions = [
    "Train on diverse, adversarial examples",
    "Implement multi-language support",
    "Use LLM-based nuanced detection",
    "Regular red-team testing",
    "User reporting mechanisms",
]
```

**Related Terms**: False Negative, Recall, Missed Detection

---

### User Trust

**Definition**: The confidence users have that a platform will handle their content and data fairly, safely, and transparently. Trust is built through consistent, fair moderation and clear communication.

**Example**:
```python
# Trust-building practices
trust_practices = {
    "transparency": {
        "description": "Clearly communicate moderation policies",
        "implementation": "Publish community guidelines, explain decisions",
    },
    "consistency": {
        "description": "Apply rules equally to all users",
        "implementation": "Regular audits, bias detection",
    },
    "appeals": {
        "description": "Allow users to contest decisions",
        "implementation": "Appeal process with human review",
    },
    "accountability": {
        "description": "Take responsibility for mistakes",
        "implementation": "Public transparency reports",
    },
    "communication": {
        "description": "Explain why content was moderated",
        "implementation": "Detailed moderation messages",
    },
}
```

**Related Terms**: Transparency, Fairness, Accountability

---

*Part of the [AI Security Lecture Series](README.md). See also: [Lecture 02: Content Moderation](02-content-moderation-lecture.md)*
