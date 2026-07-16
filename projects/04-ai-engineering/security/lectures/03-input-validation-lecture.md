# Lecture 03: Input Validation

## Topic Overview

Input validation is the first line of defense against malicious or malformed data entering your AI system. This lecture covers validation strategies, sanitization techniques, schema validation, adversarial input detection, and building robust input handling pipelines. Proper input validation prevents injection attacks, data corruption, and unexpected system behavior.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement** comprehensive input validation for AI systems
2. **Design** input schemas using Pydantic or similar frameworks
3. **Build** sanitization pipelines for different data types
4. **Detect** adversarial inputs designed to manipulate AI behavior
5. **Handle** edge cases like Unicode attacks and encoding tricks
6. **Apply** the principle of least trust to all inputs
7. **Create** input validation testing suites

---

## Key Concepts

### 1. Validation Layers

```python
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List, Callable
import re

class ValidationLayer(Enum):
    """Different layers of input validation."""
    SYNTACTIC = "syntactic"      # Basic format checking
    SEMANTIC = "semantic"        # Meaning and context checking
    SECURITY = "security"        # Security-focused validation
    BUSINESS = "business"        # Business rule validation

@dataclass
class ValidationResult:
    """Result of input validation."""
    valid: bool
    layer: ValidationLayer
    errors: List[str]
    sanitized_value: Any = None
    risk_score: float = 0.0

class InputValidator:
    """Multi-layer input validation system."""

    def __init__(self):
        self.layers = []
        self.custom_validators = {}

    def add_layer(self, layer: ValidationLayer, validator: Callable):
        """Add a validation layer."""
        self.layers.append((layer, validator))

    def validate(self, value: Any, context: Optional[dict] = None) -> List[ValidationResult]:
        """Validate input through all layers."""
        results = []

        for layer, validator in self.layers:
            try:
                result = validator(value, context)
                results.append(result)
                if not result.valid:
                    break  # Stop on first failure
            except Exception as e:
                results.append(ValidationResult(
                    valid=False,
                    layer=layer,
                    errors=[f"Validator error: {str(e)}"],
                ))
                break

        return results
```

### 2. Type Validation

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class ChatMessage(BaseModel):
    """Schema for chat messages."""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1, max_length=10000)
    timestamp: Optional[datetime] = None

    @validator('content')
    def validate_content(cls, v):
        """Validate message content."""
        # Check for null bytes
        if '\x00' in v:
            raise ValueError("Content contains null bytes")

        # Check for excessive whitespace
        if len(v.strip()) == 0:
            raise ValueError("Content is empty after trimming")

        return v

class AIRequest(BaseModel):
    """Schema for AI service requests."""
    prompt: str = Field(..., min_length=1, max_length=4096)
    model: str = Field(default="gpt-4", pattern="^(gpt-3.5-turbo|gpt-4|claude-3)$")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4096)
    system_prompt: Optional[str] = Field(None, max_length=2000)
    user_id: str = Field(..., min_length=1, max_length=100)

    @validator('prompt')
    def validate_prompt(cls, v):
        """Validate prompt content."""
        # Remove control characters
        v = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', v)

        # Check for injection patterns
        injection_patterns = [
            r'ignore\s+(all\s+)?previous',
            r'you\s+are\s+now\s+',
            r'\[SYSTEM\]',
            r'<\|im_start\|>',
        ]
        for pattern in injection_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Potential prompt injection detected")

        return v

    @validator('system_prompt')
    def validate_system_prompt(cls, v):
        """Validate system prompt if provided."""
        if v is None:
            return v

        # System prompts shouldn't contain user-controlled content
        if '{' in v and '}' in v:
            raise ValueError("System prompt contains template variables")

        return v
```

### 3. String Sanitization

```python
import re
import html
import unicodedata
from typing import Optional

class StringSanitizer:
    """Comprehensive string sanitization."""

    # Characters that are dangerous in various contexts
    CONTROL_CHARS = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]')

    # SQL injection patterns
    SQL_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)",
        r"(--|#|/\*|\*/)",
        r"('|\")\s*(OR|AND)\s*('|\")\s*=\s*('|\")",
    ]

    # XSS patterns
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe',
    ]

    def sanitize_for_ai(self, text: str) -> str:
        """Sanitize text for AI processing."""
        # Normalize unicode
        text = unicodedata.normalize('NFKC', text)

        # Remove control characters
        text = self.CONTROL_CHARS.sub('', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Escape HTML entities
        text = html.escape(text)

        return text

    def sanitize_for_database(self, text: str) -> str:
        """Sanitize text for database storage."""
        # Basic SQL injection prevention
        text = text.replace("'", "''")
        text = text.replace(";", "")
        text = text.replace("--", "")
        return text

    def sanitize_for_display(self, text: str) -> str:
        """Sanitize text for HTML display."""
        text = html.escape(text)
        text = self.CONTROL_CHARS.sub('', text)
        return text

    def detect_encoding_tricks(self, text: str) -> dict:
        """Detect various encoding tricks."""
        tricks = {
            "has_null_bytes": '\x00' in text,
            "has_rtl_override": '\u202e' in text or '\u202d' in text,
            "has_zero_width_chars": bool(re.search(r'[\u200b-\u200f\u2028-\u202f\u2060-\u2064\ufeff]', text)),
            "has_homoglyphs": self._detect_homoglyphs(text),
            "has_excessive_combining": bool(re.search(r'[\u0300-\u036f]{3,}', text)),
        }
        return tricks

    def _detect_homoglyphs(self, text: str) -> bool:
        """Detect visually similar but different characters."""
        homoglyphs = {
            'a': ['а', 'ɑ', 'α'],  # Cyrillic, Latin, Greek
            'e': ['е', 'ε'],
            'o': ['о', 'ο'],
            'p': ['р', 'ρ'],
        }
        for char in text:
            for group in homoglyphs.values():
                if char in group:
                    return True
        return False
```

### 4. Adversarial Input Detection

```python
class AdversarialInputDetector:
    """Detect inputs designed to manipulate AI behavior."""

    def __init__(self):
        self.patterns = {
            "prompt_injection": [
                r'ignore\s+(all\s+)?previous',
                r'you\s+are\s+now\s+',
                r'new\s+instructions?\s*:',
                r'\[SYSTEM\]',
                r'<\|im_start\|>',
                r'###\s*System',
            ],
            "encoding_bypass": [
                r'decode\s+(this\s+)?base64',
                r'apply\s+rot13',
                r'convert\s+from\s+hex',
            ],
            "context_manipulation": [
                r'let\'?s\s+(play|pretend)',
                r'hypothetically\s+(speaking|if)',
                r'for\s+(educational|research)\s+purposes',
            ],
            "token_overflow": [
                r'.{5000,}',  # Very long input
                r'(.)\1{100,}',  # Repeated characters
            ],
        }

    def analyze(self, text: str) -> dict:
        """Analyze input for adversarial patterns."""
        findings = []

        for attack_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    findings.append({
                        "type": attack_type,
                        "pattern": pattern,
                        "severity": self._get_severity(attack_type),
                    })

        return {
            "is_adversarial": len(findings) > 0,
            "findings": findings,
            "risk_score": self._calculate_risk(findings),
        }

    def _get_severity(self, attack_type: str) -> str:
        """Get severity level for attack type."""
        severity_map = {
            "prompt_injection": "high",
            "encoding_bypass": "medium",
            "context_manipulation": "medium",
            "token_overflow": "low",
        }
        return severity_map.get(attack_type, "low")

    def _calculate_risk(self, findings: list) -> float:
        """Calculate overall risk score."""
        if not findings:
            return 0.0

        severity_scores = {"critical": 1.0, "high": 0.8, "medium": 0.5, "low": 0.2}
        scores = [severity_scores.get(f["severity"], 0.2) for f in findings]
        return min(sum(scores) / len(scores), 1.0)
```

### 5. Complete Validation Pipeline

```python
from dataclasses import dataclass
from typing import Any, Callable, List, Optional
import logging
import time

logger = logging.getLogger(__name__)

@dataclass
class ValidationConfig:
    """Configuration for the validation pipeline."""
    max_input_length: int = 10000
    enable_adversarial_detection: bool = True
    enable_sanitization: bool = True
    block_on_adversarial: bool = True
    log_all_inputs: bool = False

class InputValidationPipeline:
    """Complete input validation pipeline."""

    def __init__(self, config: ValidationConfig):
        self.config = config
        self.sanitizer = StringSanitizer()
        self.adversarial_detector = AdversarialInputDetector()
        self.custom_validators: List[Callable] = []

    def add_validator(self, validator: Callable):
        """Add a custom validator."""
        self.custom_validators.append(validator)

    def validate_and_sanitize(self, text: str, context: Optional[dict] = None) -> dict:
        """
        Validate and sanitize input through the complete pipeline.

        Args:
            text: Input text to validate
            context: Additional context (user_id, request_type, etc.)

        Returns:
            dict with sanitized_text, valid, errors, risk_score
        """
        start_time = time.time()
        errors = []
        risk_score = 0.0

        # Log if configured
        if self.config.log_all_inputs:
            logger.info(f"Input validation: length={len(text)}, context={context}")

        # Step 1: Basic length check
        if len(text) > self.config.max_input_length:
            return {
                "valid": False,
                "sanitized_text": "",
                "errors": [f"Input exceeds maximum length ({len(text)} > {self.config.max_input_length})"],
                "risk_score": 1.0,
                "processing_time": time.time() - start_time,
            }

        # Step 2: Sanitization
        if self.config.enable_sanitization:
            text = self.sanitizer.sanitize_for_ai(text)

        # Step 3: Adversarial detection
        if self.config.enable_adversarial_detection:
            adversarial_result = self.adversarial_detector.analyze(text)
            if adversarial_result["is_adversarial"]:
                risk_score = adversarial_result["risk_score"]
                if self.config.block_on_adversarial and risk_score > 0.5:
                    return {
                        "valid": False,
                        "sanitized_text": text,
                        "errors": [f"Adversarial input detected: {adversarial_result['findings']}"],
                        "risk_score": risk_score,
                        "processing_time": time.time() - start_time,
                    }

        # Step 4: Custom validators
        for validator in self.custom_validators:
            try:
                result = validator(text, context)
                if not result.get("valid", True):
                    errors.extend(result.get("errors", []))
                    risk_score = max(risk_score, result.get("risk_score", 0))
            except Exception as e:
                errors.append(f"Custom validator error: {str(e)}")

        # Step 5: Final validation
        valid = len(errors) == 0

        return {
            "valid": valid,
            "sanitized_text": text,
            "errors": errors,
            "risk_score": risk_score,
            "processing_time": time.time() - start_time,
        }

    def validate_structured(self, data: dict, schema: dict) -> dict:
        """Validate structured data against a schema."""
        errors = []

        for field, rules in schema.items():
            value = data.get(field)

            # Required check
            if rules.get("required", False) and value is None:
                errors.append(f"Field '{field}' is required")
                continue

            if value is None:
                continue

            # Type check
            expected_type = rules.get("type")
            if expected_type and not isinstance(value, expected_type):
                errors.append(f"Field '{field}' must be {expected_type.__name__}")
                continue

            # Length check
            if isinstance(value, str):
                min_len = rules.get("min_length", 0)
                max_len = rules.get("max_length", float('inf'))
                if len(value) < min_len or len(value) > max_len:
                    errors.append(f"Field '{field}' length must be between {min_len} and {max_len}")

            # Pattern check
            pattern = rules.get("pattern")
            if pattern and isinstance(value, str):
                if not re.search(pattern, value):
                    errors.append(f"Field '{field}' doesn't match required pattern")

            # Range check
            if isinstance(value, (int, float)):
                min_val = rules.get("min")
                max_val = rules.get("max")
                if min_val is not None and value < min_val:
                    errors.append(f"Field '{field}' must be >= {min_val}")
                if max_val is not None and value > max_val:
                    errors.append(f"Field '{field}' must be <= {max_val}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }
```

### 6. Unicode and Encoding Attacks

```python
class UnicodeValidator:
    """Handle Unicode-related security concerns."""

    # Dangerous Unicode categories
    DANGEROUS_CATEGORIES = {
        'Cf',  # Format characters (includes zero-width spaces)
        'Cc',  # Control characters
        'Cn',  # Unassigned characters
    }

    # Homoglyph mapping (visually similar characters)
    HOMOGLYPHS = {
        'a': 'а',  # Cyrillic а
        'e': 'е',  # Cyrillic е
        'o': 'о',  # Cyrillic о
        'p': 'р',  # Cyrillic р
        'c': 'с',  # Cyrillic с
        'x': 'х',  # Cyrillic х
    }

    def validate_unicode(self, text: str) -> dict:
        """Validate text for Unicode issues."""
        issues = []

        for i, char in enumerate(text):
            category = unicodedata.category(char)

            # Check for dangerous categories
            if category in self.DANGEROUS_CATEGORIES:
                issues.append({
                    "position": i,
                    "char": repr(char),
                    "category": category,
                    "issue": "dangerous_category",
                })

            # Check for RTL override
            if char in ('\u202e', '\u202d', '\u202a', '\u202b', '\u202c'):
                issues.append({
                    "position": i,
                    "char": repr(char),
                    "issue": "direction_override",
                })

        # Check for mixed scripts (potential homoglyph attack)
        scripts = set()
        for char in text:
            if char.isalpha():
                script = unicodedata.script(char) if hasattr(unicodedata, 'script') else 'Unknown'
                scripts.add(script)

        if len(scripts) > 2:
            issues.append({
                "issue": "mixed_scripts",
                "scripts": list(scripts),
            })

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "char_count": len(text),
            "unique_scripts": len(scripts) if 'scripts' in dir() else 0,
        }

    def normalize_unicode(self, text: str) -> str:
        """Normalize Unicode text to prevent attacks."""
        # NFKC normalization: compatibility decomposition + canonical composition
        # This converts fullwidth characters to ASCII equivalents
        # and normalizes combining characters
        return unicodedata.normalize('NFKC', text)

    def detect_confusables(self, text: str) -> list:
        """Detect confusable characters."""
        confusables = []
        for i, char in enumerate(text):
            for ascii_char, confusable in self.HOMOGLYPHS.items():
                if char == confusable:
                    confusables.append({
                        "position": i,
                        "confusable": char,
                        "looks_like": ascii_char,
                    })
        return confusables
```

---

## Common Mistakes to Avoid

1. **Trusting client-side validation only** — Always validate on the server
2. **Using blacklists instead of whitelists** — Whitelists are more secure
3. **Ignoring edge cases** — Test with Unicode, long strings, empty input
4. **Not normalizing input** — Different encodings can bypass filters
5. **Skipping validation for "internal" APIs** — Internal services can be compromised too
6. **Using regular expressions without anchoring** — Unanchored regex can be bypassed
7. **Not logging validation failures** — You need to know about attack attempts
8. **Assuming "clean" data** — All input should be treated as potentially malicious

---

## Best Practices

1. **Validate early, validate often** — Check input at every boundary
2. **Use whitelist validation** — Define what's allowed, reject everything else
3. **Normalize before validation** — Convert to a standard form first
4. **Layer your defenses** — Combine multiple validation approaches
5. **Keep validators updated** — New attack techniques emerge constantly
6. **Test with adversarial examples** — Include edge cases and attacks in tests
7. **Log all validation failures** — For security monitoring and improvement
8. **Fail securely** — When validation fails, deny access by default

---

## Practice Exercises

### Exercise 1: Type Validation (Easy)
Create Pydantic models for an AI chat application with proper validation.

### Exercise 2: Sanitization Pipeline (Medium)
Build a sanitization pipeline that handles Unicode, HTML, and SQL injection.

### Exercise 3: Adversarial Detection (Medium)
Implement an adversarial input detector that catches at least 10 different attack patterns.

### Exercise 4: Complete Pipeline (Hard)
Build a complete input validation pipeline with logging, metrics, and testing.

---

## Summary

Input validation is the foundation of AI security. Key takeaways:

- **Validate all input** — Never trust data from external sources
- **Use multiple layers** — Combine type, format, and content validation
- **Sanitize before processing** — Remove or escape dangerous content
- **Detect adversarial inputs** — Look for injection and manipulation attempts
- **Handle Unicode carefully** — Encoding tricks can bypass simple filters
- **Test thoroughly** — Include edge cases and attack patterns in tests
- **Log and monitor** — Track validation failures for security insights

---

## References

- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Unicode Security Guide](https://unicode.org/security/)
