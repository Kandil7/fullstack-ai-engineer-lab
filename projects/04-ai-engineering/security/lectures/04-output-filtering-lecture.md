# Lecture 04: Output Filtering

## Topic Overview

Output filtering is the process of examining, sanitizing, and controlling what AI systems produce before it reaches users or downstream systems. This lecture covers PII redaction, content filtering, safe completion techniques, output validation, and building robust output filtering pipelines. Output filtering is essential for preventing data leakage, ensuring compliance, and maintaining user safety.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement** PII detection and redaction in AI outputs
2. **Build** content filtering systems for different output types
3. **Design** output validation pipelines
4. **Handle** sensitive data in AI responses safely
5. **Create** safe completion mechanisms
6. **Evaluate** output filtering effectiveness
7. **Apply** output filtering for regulatory compliance

---

## Key Concepts

### 1. Output Filtering Layers

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import re

class FilterLayer(Enum):
    """Different layers of output filtering."""
    PII_REDACTION = "pii_redaction"
    CONTENT_FILTER = "content_filter"
    POLICY_CHECK = "policy_check"
    FORMAT_VALIDATION = "format_validation"
    SECURITY_SCAN = "security_scan"

@dataclass
class FilterResult:
    """Result of output filtering."""
    original: str
    filtered: str
    layer: FilterLayer
    modifications: List[Dict[str, Any]]
    blocked: bool
    reason: Optional[str] = None

class OutputFilterPipeline:
    """Multi-layer output filtering pipeline."""

    def __init__(self):
        self.filters = []

    def add_filter(self, layer: FilterLayer, filter_func):
        """Add a filter layer."""
        self.filters.append((layer, filter_func))

    def filter(self, text: str, context: Optional[Dict] = None) -> str:
        """Apply all filters to the output."""
        current_text = text
        all_modifications = []

        for layer, filter_func in self.filters:
            result = filter_func(current_text, context)
            current_text = result.filtered
            all_modifications.extend(result.modifications)

            if result.blocked:
                return "[Content blocked by security filter]"

        return current_text
```

### 2. PII Detection and Redaction

```python
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class PIIEntity:
    """A detected PII entity."""
    text: str
    pii_type: str
    start: int
    end: int
    confidence: float

class PIIDetector:
    """Detect personally identifiable information in text."""

    def __init__(self):
        self.patterns = {
            "email": {
                "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "confidence": 0.95,
            },
            "phone_us": {
                "pattern": r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
                "confidence": 0.90,
            },
            "ssn": {
                "pattern": r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b',
                "confidence": 0.85,
            },
            "credit_card": {
                "pattern": r'\b(?:\d{4}[-.\s]?){3}\d{4}\b',
                "confidence": 0.80,
            },
            "ip_address": {
                "pattern": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                "confidence": 0.75,
            },
            "date_of_birth": {
                "pattern": r'\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d{2}\b',
                "confidence": 0.70,
            },
            "address_us": {
                "pattern": r'\d{1,5}\s\w+(?:\s\w+)*\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln)\b',
                "confidence": 0.65,
            },
            "name_pattern": {
                "pattern": r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',
                "confidence": 0.40,  # Lower confidence - many false positives
            },
        }

    def detect(self, text: str) -> List[PIIEntity]:
        """Detect all PII entities in text."""
        entities = []

        for pii_type, config in self.patterns.items():
            for match in re.finditer(config["pattern"], text):
                entities.append(PIIEntity(
                    text=match.group(),
                    pii_type=pii_type,
                    start=match.start(),
                    end=match.end(),
                    confidence=config["confidence"],
                ))

        # Sort by position and remove overlaps
        entities.sort(key=lambda x: x.start)
        entities = self._remove_overlaps(entities)

        return entities

    def _remove_overlaps(self, entities: List[PIIEntity]) -> List[PIIEntity]:
        """Remove overlapping entities, keeping higher confidence ones."""
        if not entities:
            return entities

        filtered = [entities[0]]
        for entity in entities[1:]:
            if entity.start >= filtered[-1].end:
                filtered.append(entity)
            elif entity.confidence > filtered[-1].confidence:
                filtered[-1] = entity

        return filtered

class PIIRedactor:
    """Redact detected PII from text."""

    def __init__(self, detector: PIIDetector):
        self.detector = detector

    def redact(self, text: str, replacement: str = "[REDACTED]") -> str:
        """Redact all PII from text."""
        entities = self.detector.detect(text)

        # Replace from end to start to preserve positions
        for entity in reversed(entities):
            text = text[:entity.start] + replacement + text[entity.end:]

        return text

    def redact_with_log(self, text: str) -> Dict[str, Any]:
        """Redact PII and return detailed log."""
        entities = self.detector.detect(text)
        redacted = text

        modifications = []
        for entity in reversed(entities):
            replacement = f"[{entity.pii_type.upper()}]"
            redacted = redacted[:entity.start] + replacement + redacted[entity.end:]
            modifications.append({
                "type": entity.pii_type,
                "original": entity.text,
                "replacement": replacement,
                "position": entity.start,
            })

        return {
            "redacted_text": redacted,
            "entities_found": len(entities),
            "modifications": modifications,
        }
```

### 3. Content Filtering

```python
class ContentFilter:
    """Filter AI outputs based on content policies."""

    def __init__(self):
        self.filters = {
            "harmful_content": {
                "patterns": [
                    r'(how\s+to\s+(make|build|create)\s+(bomb|explosive|weapon))',
                    r'(step\s+by\s+step\s+(attack|hack|exploit))',
                ],
                "action": "block",
            },
            "personal_opinions": {
                "patterns": [
                    r'(i\s+(think|believe|feel)\s+that\s+(you|we|they)\s+should)',
                    r'(in\s+my\s+opinion)',
                ],
                "action": "rewrite",
            },
            "speculative_claims": {
                "patterns": [
                    r'(definitely|certainly|absolutely)\s+(is|are|will)',
                    r'(proven\s+to\s+be)',
                ],
                "action": "soften",
            },
        }

    def filter(self, text: str) -> Dict[str, Any]:
        """Apply content filters to output."""
        results = []

        for filter_name, config in self.filters.items():
            for pattern in config["patterns"]:
                if re.search(pattern, text, re.IGNORECASE):
                    results.append({
                        "filter": filter_name,
                        "pattern": pattern,
                        "action": config["action"],
                    })

        return {
            "filtered": len(results) > 0,
            "filters_applied": results,
        }

    def apply_filter(self, text: str, filter_result: Dict) -> str:
        """Apply the determined filter action."""
        if not filter_result["filtered"]:
            return text

        for filter_applied in filter_result["filters_applied"]:
            if filter_applied["action"] == "block":
                return "[This content has been filtered]"
            elif filter_applied["action"] == "rewrite":
                # Would use LLM to rewrite in neutral tone
                return self._rewrite_neutral(text)
            elif filter_applied["action"] == "soften":
                text = self._soften_claims(text)

        return text

    def _rewrite_neutral(self, text: str) -> str:
        """Rewrite text in neutral tone."""
        # Simplified - would use LLM in practice
        text = re.sub(r'i\s+think', 'the general consensus is', text, flags=re.IGNORECASE)
        text = re.sub(r'i\s+believe', 'research suggests', text, flags=re.IGNORECASE)
        return text

    def _soften_claims(self, text: str) -> str:
        """Soften absolute claims."""
        replacements = {
            r'\bdefinitely\b': 'likely',
            r'\bcertainly\b': 'probably',
            r'\babsolutely\b': 'generally',
            r'\bproven\b': 'suggested',
        }
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text
```

### 4. Output Validation

```python
class OutputValidator:
    """Validate AI output before delivering to users."""

    def __init__(self):
        self.validators = [
            self.validate_length,
            self.validate_encoding,
            self.validate_format,
            self.validate_safety,
            self.validate_consistency,
        ]

    def validate(self, text: str, context: Dict) -> Dict[str, Any]:
        """Validate output through all validators."""
        results = []

        for validator in self.validators:
            result = validator(text, context)
            results.append(result)

        return {
            "valid": all(r["valid"] for r in results),
            "results": results,
        }

    def validate_length(self, text: str, context: Dict) -> Dict:
        """Validate output length."""
        max_length = context.get("max_output_length", 4096)

        return {
            "validator": "length",
            "valid": len(text) <= max_length,
            "length": len(text),
            "max_length": max_length,
        }

    def validate_encoding(self, text: str, context: Dict) -> Dict:
        """Validate output encoding."""
        issues = []

        # Check for control characters
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', text):
            issues.append("control_characters")

        # Check for null bytes
        if '\x00' in text:
            issues.append("null_bytes")

        return {
            "validator": "encoding",
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def validate_format(self, text: str, context: Dict) -> Dict:
        """Validate output format."""
        expected_format = context.get("expected_format", "text")
        issues = []

        if expected_format == "json":
            try:
                import json
                json.loads(text)
            except json.JSONDecodeError:
                issues.append("invalid_json")

        elif expected_format == "email":
            if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', text):
                issues.append("invalid_email_format")

        return {
            "validator": "format",
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def validate_safety(self, text: str, context: Dict) -> Dict:
        """Validate output safety."""
        issues = []

        # Check for potential prompt injection in output
        injection_patterns = [
            r'ignore\s+(all\s+)?previous',
            r'you\s+are\s+now\s+',
            r'\[SYSTEM\]',
        ]

        for pattern in injection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append("potential_injection")

        return {
            "validator": "safety",
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def validate_consistency(self, text: str, context: Dict) -> Dict:
        """Validate output consistency with context."""
        # Check if output is consistent with expected response type
        return {
            "validator": "consistency",
            "valid": True,  # Simplified
            "issues": [],
        }
```

### 5. Safe Completion

```python
class SafeCompletion:
    """Ensure AI completions are safe and appropriate."""

    def __init__(self):
        self.blocked_topics = [
            "how to make weapons",
            "personal attacks",
            "illegal activities",
        ]

    def safe_complete(self, prompt: str, completion: str) -> Dict[str, Any]:
        """Ensure completion is safe."""
        issues = []

        # Check if completion strays into dangerous topics
        for topic in self.blocked_topics:
            if topic.lower() in completion.lower():
                issues.append(f"dangerous_topic:{topic}")

        # Check if completion contains PII
        pii_detector = PIIDetector()
        pii_entities = pii_detector.detect(completion)
        if pii_entities:
            issues.append(f"pii_detected:{len(pii_entities)}_entities")

        # Check if completion is off-topic
        if self._is_off_topic(prompt, completion):
            issues.append("off_topic")

        return {
            "safe": len(issues) == 0,
            "issues": issues,
            "filtered_completion": self._filter_if_needed(completion, issues),
        }

    def _is_off_topic(self, prompt: str, completion: str) -> bool:
        """Check if completion is off-topic."""
        # Simplified - would use semantic similarity in practice
        prompt_words = set(prompt.lower().split())
        completion_words = set(completion.lower().split())
        overlap = len(prompt_words & completion_words)
        return overlap < len(prompt_words) * 0.2

    def _filter_if_needed(self, completion: str, issues: List[str]) -> str:
        """Filter completion if issues found."""
        if not issues:
            return completion

        # Apply filters based on issues
        for issue in issues:
            if "dangerous_topic" in issue:
                return "I apologize, but I cannot provide information on that topic."
            elif "pii_detected" in issue:
                # Redact PII
                redactor = PIIRedactor(PIIDetector())
                completion = redactor.redact(completion)

        return completion
```

### 6. Complete Output Filtering Pipeline

```python
class OutputFilterPipeline:
    """Complete output filtering pipeline."""

    def __init__(self):
        self.pii_detector = PIIDetector()
        self.pii_redactor = PIIRedactor(self.pii_detector)
        self.content_filter = ContentFilter()
        self.output_validator = OutputValidator()
        self.safe_completion = SafeCompletion()

    def process(self, output: str, context: Dict) -> Dict[str, Any]:
        """Process AI output through complete filtering pipeline."""
        result = {
            "original": output,
            "steps": [],
        }

        current_text = output

        # Step 1: PII Redaction
        pii_result = self.pii_redactor.redact_with_log(current_text)
        current_text = pii_result["redacted_text"]
        result["steps"].append({
            "step": "pii_redaction",
            "entities_found": pii_result["entities_found"],
        })

        # Step 2: Content Filtering
        filter_result = self.content_filter.filter(current_text)
        if filter_result["filtered"]:
            current_text = self.content_filter.apply_filter(
                current_text, filter_result
            )
        result["steps"].append({
            "step": "content_filter",
            "filtered": filter_result["filtered"],
        })

        # Step 3: Output Validation
        validation_result = self.output_validator.validate(current_text, context)
        if not validation_result["valid"]:
            current_text = "[Output filtered due to validation failure]"
        result["steps"].append({
            "step": "validation",
            "valid": validation_result["valid"],
        })

        # Step 4: Safe Completion Check
        completion_result = self.safe_completion.safe_complete(
            context.get("prompt", ""), current_text
        )
        if not completion_result["safe"]:
            current_text = completion_result["filtered_completion"]
        result["steps"].append({
            "step": "safe_completion",
            "safe": completion_result["safe"],
        })

        result["filtered"] = current_text
        result["modified"] = current_text != output

        return result
```

---

## Common Mistakes to Avoid

1. **Trusting AI output** — Always validate and filter before delivering to users
2. **Only filtering input** — Attackers can manipulate AI to output harmful content
3. **Ignoring PII in outputs** — AI may inadvertently expose personal information
4. **Over-filtering** — Too aggressive filtering degrades user experience
5. **Not logging filtered content** — You need to know what's being filtered
6. **Ignoring edge cases** — Test with diverse inputs and contexts
7. **Static filters only** — Content threats evolve; filters must evolve too
8. **No fallback behavior** — Always have safe defaults when filtering fails

---

## Best Practices

1. **Filter before delivery** — Never send unfiltered output to users
2. **Layer your filters** — Combine PII, content, and safety filters
3. **Log all filtering** — Track what's filtered for improvement
4. **Test with adversarial outputs** — Include edge cases in testing
5. **Provide clear feedback** — Tell users when content is filtered
6. **Maintain filter updates** — Keep filters current with new threats
7. **Balance safety with usability** — Don't over-filter legitimate content
8. **Have fallback responses** — Always have safe defaults

---

## Practice Exercises

### Exercise 1: PII Detector (Easy)
Build a PII detector that identifies emails, phone numbers, and SSNs in text.

### Exercise 2: Content Filter (Medium)
Create a content filter that handles different types of policy violations.

### Exercise 3: Output Validation Pipeline (Medium)
Build a complete output validation pipeline with multiple stages.

### Exercise 4: End-to-End Filtering (Hard)
Create a complete output filtering system with logging, metrics, and testing.

---

## Summary

Output filtering is essential for safe AI deployments. Key takeaways:

- **Always filter outputs** — Never trust raw AI output
- **PII redaction protects users** — Detect and redact personal information
- **Content filtering ensures compliance** — Apply policies to outputs
- **Validation catches errors** — Verify output format and safety
- **Safe completion prevents harm** — Ensure outputs are appropriate
- **Log everything** — Track filtering for improvement and compliance

---

## References

- [OpenAI Output Filtering](https://platform.openai.com/docs/guides/moderation)
- [Google Cloud DLP](https://cloud.google.com/dlp)
- [AWS Comprehend PII Detection](https://aws.amazon.com/comprehend/features/)
