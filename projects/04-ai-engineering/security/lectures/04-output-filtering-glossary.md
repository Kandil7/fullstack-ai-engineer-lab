# Glossary 04: Output Filtering Terms

## Quick Reference Table

| Term | Category | Importance | See Also |
|------|----------|------------|----------|
| Output Filtering | Process | Critical | Content Moderation |
| PII Detection | Technique | Critical | Privacy, Redaction |
| PII Redaction | Technique | Critical | Data Protection |
| Content Filtering | Technique | High | Content Moderation |
| Safe Completion | Technique | High | Output Validation |
| Output Validation | Process | Critical | Data Integrity |
| Sensitive Data | Concept | Critical | PII, Confidential |
| Data Leakage | Risk | Critical | PII Exposure |
| Filter Pipeline | Architecture | High | Multi-layer |
| Content Policy | Governance | High | Moderation Rules |
| False Positive | Metric | High | Over-filtering |
| False Negative | Metric | High | Under-filtering |
| Redaction | Technique | High | Anonymization |
| Anonymization | Technique | High | Privacy |
| Masking | Technique | High | Data Protection |
| Sanitization | Technique | High | Cleaning |

---

## Alphabetical Definitions

### Anonymization

**Definition**: The process of removing or obfuscating personally identifiable information from data so that individuals cannot be identified.

**Example**:
```python
import re
import hashlib

class Anonymizer:
    def __init__(self):
        self.salt = "your-secret-salt"

    def anonymize_email(self, email: str) -> str:
        """Replace email with anonymized hash."""
        hash_obj = hashlib.sha256((email + self.salt).encode())
        return f"user_{hash_obj.hexdigest()[:8]}@example.com"

    def anonymize_name(self, name: str) -> str:
        """Replace name with generic placeholder."""
        return f"User_{hashlib.md5(name.encode()).hexdigest()[:6]}"

    def anonymize_ip(self, ip: str) -> str:
        """Anonymize IP address by zeroing last octet."""
        parts = ip.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
        return "[ANONYMIZED_IP]"

# Usage
anonymizer = Anonymizer()
print(anonymizer.anonymize_email("john@example.com"))
# user_a1b2c3d4@example.com
print(anonymizer.anonymize_name("John Doe"))
# User_x7y8z9
```

**Related Terms**: PII Redaction, Data Protection, Privacy

---

### Content Filter

**Definition**: A system that analyzes content against defined policies and blocks or modifies content that violates those policies.

**Example**:
```python
class ContentFilter:
    def __init__(self):
        self.policies = {
            "harmful": {
                "keywords": ["bomb", "weapon", "attack"],
                "action": "block",
                "message": "Content blocked: harmful material detected",
            },
            "spam": {
                "keywords": ["buy now", "click here", "free money"],
                "action": "flag",
                "message": "Content flagged: potential spam",
            },
            "pii": {
                "patterns": [r'\d{3}-\d{2}-\d{4}'],  # SSN pattern
                "action": "redact",
                "message": "PII detected and redacted",
            },
        }

    def filter(self, text: str) -> dict:
        """Apply content filters."""
        for policy_name, policy in self.policies.items():
            for keyword in policy.get("keywords", []):
                if keyword.lower() in text.lower():
                    return {
                        "filtered": True,
                        "policy": policy_name,
                        "action": policy["action"],
                        "message": policy["message"],
                    }
        return {"filtered": False}
```

**Related Terms**: Content Moderation, Policy Enforcement, Filtering

---

### Content Policy

**Definition**: Rules that define what content is allowed, restricted, or blocked in AI outputs.

**Example**:
```python
content_policies = {
    "generate_harmful_content": {
        "description": "AI should not generate content promoting harm",
        "categories": ["violence", "self-harm", "illegal_activity"],
        "action": "block",
        "response": "I can't help with that request.",
    },
    "reveal_pii": {
        "description": "AI should not output personal information",
        "categories": ["email", "phone", "ssn", "address"],
        "action": "redact",
        "response": "[REDACTED]",
    },
    "express_opinions": {
        "description": "AI should not express personal opinions",
        "categories": ["political", "religious", "controversial"],
        "action": "rewrite",
        "response": "neutral_rewrite",
    },
}
```

**Related Terms**: Moderation Rules, Content Guidelines, Acceptable Use

---

### Data Leakage

**Definition**: The unintended exposure of sensitive data through AI outputs. Data leakage can occur when AI systems reveal confidential information, PII, or proprietary data.

**Example**:
```python
# Common data leakage scenarios
leakage_scenarios = {
    "training_data": {
        "description": "AI memorizes and reproduces training data",
        "example": "Model outputs exact training examples",
        "defense": "Differential privacy, data deduplication",
    },
    "pii_exposure": {
        "description": "AI outputs personal information",
        "example": "Chatbot reveals user's email address",
        "defense": "PII detection and redaction",
    },
    "system_prompt": {
        "description": "AI reveals its system instructions",
        "example": "User asks for system prompt, AI complies",
        "defense": "Prompt hardening, output monitoring",
    },
    "internal_data": {
        "description": "AI reveals internal company information",
        "example": "AI outputs confidential business data",
        "defense": "Access controls, output filtering",
    },
}

def detect_data_leakage(output: str, context: dict) -> list:
    """Detect potential data leakage in AI output."""
    issues = []

    # Check for PII patterns
    pii_patterns = [
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "email"),
        (r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b', "ssn"),
        (r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b', "phone"),
    ]

    for pattern, pii_type in pii_patterns:
        if re.search(pattern, output):
            issues.append(f"potential_{pii_type}_leakage")

    return issues
```

**Related Terms**: PII Exposure, Data Protection, Information Security

---

### False Negative (Output)

**Definition**: When output filtering fails to detect and block harmful or policy-violating content.

**Example**:
```python
# Example of false negative
harmful_output = "Here's how to create a dangerous substance..."
# Filter result: {"blocked": False}
# But the content should have been blocked
# This is a false negative

# Impact analysis
false_negative_impacts = {
    "user_harm": "Harmful content reaches users",
    "legal_liability": "Platform may be liable",
    "reputation_damage": "Trust in the system decreases",
    "compliance_violation": "Regulatory requirements not met",
}
```

**Related Terms**: Under-filtering, Missed Detection, Recall

---

### False Positive (Output)

**Definition**: When output filtering incorrectly blocks or modifies legitimate, safe content.

**Example**:
```python
# Example of false positive
legitimate_output = "The chemical compound H2O is water"
# Filter result: {"blocked": True, "reason": "chemical_content"}
# But the content is actually educational and safe
# This is a false positive

# Impact analysis
false_positive_impacts = {
    "user_frustration": "Legitimate users get blocked",
    "degraded_experience": "System is over-aggressive",
    "chilling_effect": "Users avoid legitimate topics",
    "reduced_utility": "System becomes less useful",
}
```

**Related Terms**: Over-filtering, Censorship, Precision

---

### Masking

**Definition**: The process of replacing sensitive data with placeholder characters (like asterisks) while preserving some information for identification purposes.

**Example**:
```python
class DataMasker:
    def mask_email(self, email: str) -> str:
        """Mask email address."""
        parts = email.split('@')
        if len(parts) == 2:
            username = parts[0]
            domain = parts[1]
            if len(username) > 2:
                masked = username[0] + '*' * (len(username) - 2) + username[-1]
            else:
                masked = '*' * len(username)
            return f"{masked}@{domain}"
        return "***@***"

    def mask_phone(self, phone: str) -> str:
        """Mask phone number."""
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 10:
            return f"({digits[-10:-7]}) ***-{digits[-4:]}"
        return "***-***-****"

    def mask_credit_card(self, card: str) -> str:
        """Mask credit card number."""
        digits = re.sub(r'\D', '', card)
        if len(digits) >= 16:
            return f"****-****-****-{digits[-4:]}"
        return "****-****-****-****"

# Usage
masker = DataMasker()
print(masker.mask_email("john.doe@example.com"))  # j***e@example.com
print(masker.mask_phone("+1-555-123-4567"))      # (555) ***-4567
print(masker.mask_credit_card("4111-1111-1111-1111"))  # ****-****-****-1111
```

**Related Terms**: PII Redaction, Data Protection, Privacy

---

### Output Validation

**Definition**: The process of checking AI outputs against defined criteria for format, content, safety, and consistency before delivering to users.

**Example**:
```python
class OutputValidator:
    def validate(self, output: str, expected_format: str) -> dict:
        """Validate AI output."""
        issues = []

        # Length validation
        if len(output) > 4096:
            issues.append("output_too_long")

        # Format validation
        if expected_format == "json":
            try:
                json.loads(output)
            except json.JSONDecodeError:
                issues.append("invalid_json_format")

        # Safety validation
        safety_patterns = [
            r'ignore\s+(all\s+)?previous',
            r'you\s+are\s+now\s+',
        ]
        for pattern in safety_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                issues.append("potential_safety_issue")

        # Encoding validation
        if '\x00' in output:
            issues.append("null_bytes_detected")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }

# Usage
validator = OutputValidator()
result = validator.validate("Hello, world!", "text")
print(result)  # {'valid': True, 'issues': []}
```

**Related Terms**: Output Filtering, Quality Assurance, Safety Validation

---

### Output Filtering

**Definition**: The comprehensive process of examining, sanitizing, and controlling AI outputs before they reach users or downstream systems.

**Example**:
```python
class OutputFilterPipeline:
    def __init__(self):
        self.filters = [
            self.filter_pii,
            self.filter_harmful_content,
            self.filter_system_info,
            self.validate_format,
        ]

    def filter(self, output: str, context: dict) -> dict:
        """Apply all output filters."""
        current_output = output
        results = []

        for filter_func in self.filters:
            result = filter_func(current_output, context)
            if result.get("blocked"):
                return {
                    "filtered_output": "[Content filtered]",
                    "blocked": True,
                    "reason": result.get("reason"),
                }
            if result.get("modified"):
                current_output = result.get("output", current_output)
            results.append(result)

        return {
            "filtered_output": current_output,
            "blocked": False,
            "filters_applied": results,
        }

    def filter_pii(self, output: str, context: dict) -> dict:
        """Filter PII from output."""
        # Implementation here
        return {"blocked": False, "modified": False}

    def filter_harmful_content(self, output: str, context: dict) -> dict:
        """Filter harmful content."""
        # Implementation here
        return {"blocked": False, "modified": False}

    def filter_system_info(self, output: str, context: dict) -> dict:
        """Filter system information."""
        # Implementation here
        return {"blocked": False, "modified": False}

    def validate_format(self, output: str, context: dict) -> dict:
        """Validate output format."""
        # Implementation here
        return {"blocked": False, "modified": False}
```

**Related Terms**: Content Filtering, PII Redaction, Output Validation

---

### PII Detection

**Definition**: The process of identifying personally identifiable information in text, such as names, emails, phone numbers, addresses, and financial data.

**Example**:
```python
import re

class PIIDetector:
    def __init__(self):
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
            "ssn": r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b',
            "credit_card": r'\b(?:\d{4}[-.\s]?){3}\d{4}\b',
        }

    def detect(self, text: str) -> list:
        """Detect PII in text."""
        findings = []
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                findings.append({
                    "type": pii_type,
                    "count": len(matches),
                    "samples": matches[:3],
                })
        return findings

# Usage
detector = PIIDetector()
text = "Contact john@example.com or call 555-123-4567"
results = detector.detect(text)
# [{'type': 'email', 'count': 1, 'samples': ['john@example.com']},
#  {'type': 'phone', 'count': 1, 'samples': ['555-123-4567']}]
```

**Related Terms**: PII Redaction, Data Privacy, Personal Information

---

### PII Redaction

**Definition**: The process of detecting and removing or replacing personally identifiable information in text to protect user privacy.

**Example**:
```python
class PIIRedactor:
    def __init__(self):
        self.detector = PIIDetector()

    def redact(self, text: str, replacement: str = "[REDACTED]") -> str:
        """Redact all PII from text."""
        # Simple regex-based redaction
        # Email
        text = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            replacement, text
        )
        # Phone
        text = re.sub(
            r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
            replacement, text
        )
        # SSN
        text = re.sub(
            r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b',
            replacement, text
        )
        return text

# Usage
redactor = PIIRedactor()
text = "Send the report to john@example.com or call 555-123-4567"
redacted = redactor.redact(text)
# "Send the report to [REDACTED] or call [REDACTED]"
```

**Related Terms**: PII Detection, Anonymization, Data Protection

---

### PII (Personally Identifiable Information)

**Definition**: Any data that could potentially identify a specific individual, including names, emails, phone numbers, addresses, social security numbers, and financial information.

**Example**:
```python
# Categories of PII
pii_categories = {
    "direct_identifiers": {
        "examples": ["name", "email", "phone", "SSN", "passport number"],
        "risk": "critical",
    },
    "indirect_identifiers": {
        "examples": ["IP address", "device ID", "browsing history"],
        "risk": "high",
    },
    "sensitive_pii": {
        "examples": ["health records", "financial data", "biometrics"],
        "risk": "critical",
    },
    "quasi_identifiers": {
        "examples": ["age", "zip code", "gender", "occupation"],
        "risk": "medium",
    },
}

# PII detection patterns
pii_patterns = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    "ssn": r'\b\d{3}[-.]?\d{2}[-.]?\d{4}\b',
    "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
}
```

**Related Terms**: Personal Data, Privacy, Data Protection

---

### Privacy

**Definition**: The right of individuals to control how their personal information is collected, used, and shared. In AI systems, privacy involves protecting user data from unauthorized access and unintended exposure.

**Example**:
```python
# Privacy principles for AI systems
privacy_principles = {
    "data_minimization": {
        "description": "Collect only necessary data",
        "implementation": "Limit input fields, don't store raw prompts",
    },
    "purpose_limitation": {
        "description": "Use data only for stated purpose",
        "implementation": "Don't use customer data for training without consent",
    },
    "storage_limitation": {
        "description": "Don't keep data longer than needed",
        "implementation": "Auto-delete logs after retention period",
    },
    "accuracy": {
        "description": "Keep data accurate and up-to-date",
        "implementation": "Allow users to correct their data",
    },
    "integrity_confidentiality": {
        "description": "Protect data from unauthorized access",
        "implementation": "Encryption, access controls, auditing",
    },
}
```

**Related Terms**: Data Protection, GDPR, Consent

---

### Redaction

**Definition**: The process of obscuring or removing sensitive information from documents or text to prevent unauthorized access.

**Example**:
```python
class TextRedactor:
    def __init__(self):
        self.redaction_rules = [
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),
            (r'\b\d{3}[-.]?\d{2}[-.]?\d{4}\b', '[SSN]'),
            (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]'),
        ]

    def redact(self, text: str) -> str:
        """Apply redaction rules to text."""
        for pattern, replacement in self.redaction_rules:
            text = re.sub(pattern, replacement, text)
        return text

# Usage
redactor = TextRedactor()
text = "Email john@example.com from IP 192.168.1.1, SSN 123-45-6789"
redacted = redactor.redact(text)
# "Email [EMAIL] from IP [IP], SSN [SSN]"
```

**Related Terms**: PII Redaction, Data Masking, Censorship

---

### Sanitization

**Definition**: The process of cleaning input or output data by removing, encoding, or replacing potentially dangerous content.

**Example**:
```python
import html

class OutputSanitizer:
    def sanitize_for_display(self, text: str) -> str:
        """Sanitize output for HTML display."""
        # Escape HTML entities
        text = html.escape(text)

        # Remove script tags
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)

        # Remove event handlers
        text = re.sub(r'\bon\w+\s*=', '', text)

        return text

    def sanitize_for_api(self, text: str) -> str:
        """Sanitize output for API response."""
        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

# Usage
sanitizer = OutputSanitizer()
text = "<script>alert('XSS')</script>Hello <b>World</b>"
print(sanitizer.sanitize_for_display(text))
# "Hello &lt;b&gt;World&lt;/b&gt;"
```

**Related Terms**: Filtering, Cleaning, XSS Prevention

---

### Sensitive Data

**Definition**: Data that requires special protection due to its confidential nature, including PII, financial information, health records, and trade secrets.

**Example**:
```python
# Categories of sensitive data
sensitive_data_categories = {
    "pii": {
        "description": "Personally Identifiable Information",
        "examples": ["name", "email", "phone", "address", "SSN"],
        "regulation": "GDPR, CCPA, HIPAA",
    },
    "financial": {
        "description": "Financial and payment information",
        "examples": ["credit card", "bank account", "salary"],
        "regulation": "PCI DSS, SOX",
    },
    "health": {
        "description": "Health and medical information",
        "examples": ["medical records", "diagnoses", "prescriptions"],
        "regulation": "HIPAA, HITECH",
    },
    "authentication": {
        "description": "Credentials and security data",
        "examples": ["passwords", "API keys", "tokens"],
        "regulation": "SOC 2, ISO 27001",
    },
}

def classify_sensitivity(data_type: str) -> str:
    """Classify data sensitivity level."""
    for category, info in sensitive_data_categories.items():
        if data_type in info["examples"]:
            return category
    return "unknown"
```

**Related Terms**: PII, Confidential Data, Protected Information

---

### Under-filtering

**Definition**: When output filtering is insufficient, allowing harmful or policy-violating content to pass through to users.

**Example**:
```python
# Examples of under-filtering
under_filtering_examples = [
    {
        "content": "Subtle hate speech using coded language",
        "filtered": False,
        "reason": "Filter doesn't recognize coded language",
        "impact": "Harmful content reaches users",
    },
    {
        "content": "PII in unusual format",
        "filtered": False,
        "reason": "PII pattern not recognized",
        "impact": "Personal data exposed",
    },
    {
        "content": "Misinformation in foreign language",
        "filtered": False,
        "reason": "Filter only supports English",
        "impact": "False information spreads",
    },
]

# Solutions
solutions = [
    "Use multiple detection methods (regex + ML)",
    "Regularly update filter patterns",
    "Implement multi-language support",
    "Add human review for edge cases",
    "Monitor filter effectiveness metrics",
]
```

**Related Terms**: False Negative, Missed Detection, Recall

---

### Over-filtering

**Definition**: When output filtering is too aggressive, blocking or modifying legitimate, safe content unnecessarily.

**Example**:
```python
# Examples of over-filtering
over_filtering_examples = [
    {
        "content": "Educational content about chemistry",
        "filtered": True,
        "reason": "Contains chemical terms",
        "impact": "Educational content blocked",
    },
    {
        "content": "News report about current events",
        "filtered": True,
        "reason": "Contains sensitive keywords",
        "impact": "Legitimate news blocked",
    },
    {
        "content": "Medical information for patients",
        "filtered": True,
        "reason": "Contains health terms",
        "impact": "Useful health info blocked",
    },
]

# Solutions
solutions = [
    "Use context-aware filtering",
    "Implement human review for edge cases",
    "Calibrate thresholds carefully",
    "Provide user override options",
    "Regular false positive analysis",
]
```

**Related Terms**: False Positive, Censorship, Precision

---

*Part of the [AI Security Lecture Series](README.md). See also: [Lecture 04: Output Filtering](04-output-filtering-lecture.md)*
