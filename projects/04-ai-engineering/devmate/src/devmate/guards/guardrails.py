"""
Input and output guardrails for security and safety.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from devmate.config import settings
from devmate.obs.tracing import tracer


class GuardrailAction(str, Enum):
    """Action to take when guardrail triggers."""
    BLOCK = "block"
    WARN = "warn"
    REDACT = "redact"
    LOG = "log"


class GuardrailCategory(str, Enum):
    """Categories of guardrail checks."""
    PROMPT_INJECTION = "prompt_injection"
    PII = "pii"
    TOXICITY = "toxicity"
    CODE_EXECUTION = "code_execution"
    SYSTEM_PROMPT_EXTRACTION = "system_prompt_extraction"
    JAILBREAK = "jailbreak"
    EXCESSIVE_LENGTH = "excessive_length"


@dataclass
class GuardrailResult:
    """Result of a guardrail check."""
    triggered: bool
    category: GuardrailCategory
    action: GuardrailAction
    message: str
    details: Dict[str, Any] = None
    sanitized_content: Optional[str] = None


class BaseGuardrail:
    """Base class for guardrails."""
    
    def __init__(self, action: GuardrailAction = GuardrailAction.BLOCK):
        self.action = action
        self.enabled = True
    
    @abstractmethod
    async def check(self, content: str, context: Dict[str, Any] = None) -> GuardrailResult:
        pass


class PromptInjectionGuardrail(BaseGuardrail):
    """Detect prompt injection attempts."""
    
    # Common injection patterns
    INJECTION_PATTERNS = [
        r"ignore\s+(previous|above|all)\s+instructions",
        r"disregard\s+(previous|above|all)\s+instructions",
        r"forget\s+(everything|all\s+context|previous)",
        r"you\s+are\s+now\s+(a|an)\s+\w+",
        r"act\s+as\s+(a|an)\s+\w+",
        r"pretend\s+to\s+be\s+(a|an)\s+\w+",
        r"system\s*:\s*",
        r"assistant\s*:\s*",
        r"human\s*:\s*",
        r"<\|.*?\|>",
        r"\[INST\].*?\[/INST\]",
        r"<<SYS>>.*?<</SYS>>",
        r"###\s*Instruction",
        r"override\s+system",
        r"bypass\s+(safety|security|filter)",
        r"jailbreak",
        r"DAN\s+mode",
        r"developer\s+mode",
    ]
    
    def __init__(self, action: GuardrailAction = GuardrailAction.BLOCK):
        super().__init__(action)
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]
    
    async def check(self, content: str, context: Dict[str, Any] = None) -> GuardrailResult:
        if not self.enabled or not settings.injection_detection_enabled:
            return GuardrailResult(False, GuardrailCategory.PROMPT_INJECTION, GuardrailAction.LOG, "Disabled")
        
        async with tracer.trace("guardrail.prompt_injection"):
            for pattern in self.compiled_patterns:
                match = pattern.search(content)
                if match:
                    return GuardrailResult(
                        triggered=True,
                        category=GuardrailCategory.PROMPT_INJECTION,
                        action=self.action,
                        message=f"Prompt injection detected: {match.group()[:50]}",
                        details={"pattern": match.group(), "position": match.start()},
                    )
            
            return GuardrailResult(False, GuardrailCategory.PROMPT_INJECTION, GuardrailAction.LOG, "Clean")


class PIIGuardrail(BaseGuardrail):
    """Detect and redact PII (Personally Identifiable Information)."""
    
    PII_PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone_us": r"\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "api_key": r"\b(?:sk-|pk-|api_)[A-Za-z0-9]{20,}\b",
        "aws_key": r"\bAKIA[0-9A-Z]{16}\b",
        "github_token": r"\bgh[ps]_[A-Za-z0-9]{36}\b",
    }
    
    def __init__(self, action: GuardrailAction = GuardrailAction.REDACT):
        super().__init__(action)
        self.compiled_patterns = {
            name: re.compile(pattern) for name, pattern in self.PII_PATTERNS.items()
        }
    
    async def check(self, content: str, context: Dict[str, Any] = None) -> GuardrailResult:
        if not self.enabled or not settings.pii_detection_enabled:
            return GuardrailResult(False, GuardrailCategory.PII, GuardrailAction.LOG, "Disabled")
        
        async with tracer.trace("guardrail.pii"):
            findings = []
            sanitized = content
            
            for pii_type, pattern in self.compiled_patterns.items():
                matches = list(pattern.finditer(content))
                if matches:
                    findings.append({
                        "type": pii_type,
                        "count": len(matches),
                        "positions": [m.start() for m in matches],
                    })
                    
                    if self.action == GuardrailAction.REDACT:
                        sanitized = pattern.sub(f"[REDACTED_{pii_type.upper()}]", sanitized)
            
            if findings:
                return GuardrailResult(
                    triggered=True,
                    category=GuardrailCategory.PII,
                    action=self.action,
                    message=f"PII detected: {', '.join(f['type'] for f in findings)}",
                    details={"findings": findings},
                    sanitized_content=sanitized if self.action == GuardrailAction.REDACT else None,
                )
            
            return GuardrailResult(False, GuardrailCategory.PII, GuardrailAction.LOG, "Clean")


class LengthGuardrail(BaseGuardrail):
    """Check for excessive input length."""
    
    def __init__(self, max_length: int = None, action: GuardrailAction = GuardrailAction.BLOCK):
        super().__init__(action)
        self.max_length = max_length or settings.max_prompt_length
    
    async def check(self, content: str, context: Dict[str, Any] = None) -> GuardrailResult:
        if not self.enabled:
            return GuardrailResult(False, GuardrailCategory.EXCESSIVE_LENGTH, GuardrailAction.LOG, "Disabled")
        
        if len(content) > self.max_length:
            return GuardrailResult(
                triggered=True,
                category=GuardrailCategory.EXCESSIVE_LENGTH,
                action=self.action,
                message=f"Input exceeds maximum length: {len(content)} > {self.max_length}",
                details={"length": len(content), "max_length": self.max_length},
                sanitized_content=content[:self.max_length] if self.action == GuardrailAction.REDACT else None,
            )
        
        return GuardrailResult(False, GuardrailCategory.EXCESSIVE_LENGTH, GuardrailAction.LOG, "OK")


class SystemPromptExtractionGuardrail(BaseGuardrail):
    """Detect attempts to extract system prompt."""
    
    EXTRACTION_PATTERNS = [
        r"what\s+(is|was)\s+(your|the)\s+(system|initial)\s+prompt",
        r"show\s+me\s+(your|the)\s+(system|initial)\s+prompt",
        r"repeat\s+(your|the)\s+(system|initial)\s+prompt",
        r"print\s+(your|the)\s+(system|initial)\s+prompt",
        r"output\s+(your|the)\s+(system|initial)\s+prompt",
        r"reveal\s+(your|the)\s+(system|initial)\s+prompt",
        r"what\s+were\s+you\s+told\s+to\s+do",
        r"what\s+are\s+your\s+instructions",
        r"tell\s+me\s+your\s+instructions",
    ]
    
    def __init__(self, action: GuardrailAction = GuardrailAction.BLOCK):
        super().__init__(action)
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.EXTRACTION_PATTERNS]
    
    async def check(self, content: str, context: Dict[str, Any] = None) -> GuardrailResult:
        if not self.enabled:
            return GuardrailResult(False, GuardrailCategory.SYSTEM_PROMPT_EXTRACTION, GuardrailAction.LOG, "Disabled")
        
        async with tracer.trace("guardrail.system_prompt_extraction"):
            for pattern in self.compiled_patterns:
                match = pattern.search(content)
                if match:
                    return GuardrailResult(
                        triggered=True,
                        category=GuardrailCategory.SYSTEM_PROMPT_EXTRACTION,
                        action=self.action,
                        message="System prompt extraction attempt detected",
                        details={"pattern": match.group()},
                    )
            
            return GuardrailResult(False, GuardrailCategory.SYSTEM_PROMPT_EXTRACTION, GuardrailAction.LOG, "Clean")


class CodeExecutionGuardrail(BaseGuardrail):
    """Detect code execution attempts in user input."""
    
    EXECUTION_PATTERNS = [
        r"```\s*(python|py|javascript|js|bash|sh|sql)\s*\n.*?(?:exec|eval|subprocess|os\.system|shell)",
        r"(?:exec|eval|compile)\s*\(",
        r"__import__\s*\(",
        r"subprocess\.(run|call|Popen)",
        r"os\.system\s*\(",
        r"shell\s*=\s*True",
        r"pickle\.loads?",
        r"marshal\.loads?",
    ]
    
    def __init__(self, action: GuardrailAction = GuardrailAction.WARN):
        super().__init__(action)
        self.compiled_patterns = [re.compile(p, re.IGNORECASE | re.DOTALL) for p in self.EXECUTION_PATTERNS]
    
    async def check(self, content: str, context: Dict[str, Any] = None) -> GuardrailResult:
        if not self.enabled:
            return GuardrailResult(False, GuardrailCategory.CODE_EXECUTION, GuardrailAction.LOG, "Disabled")
        
        async with tracer.trace("guardrail.code_execution"):
            for pattern in self.compiled_patterns:
                match = pattern.search(content)
                if match:
                    return GuardrailResult(
                        triggered=True,
                        category=GuardrailCategory.CODE_EXECUTION,
                        action=self.action,
                        message="Potential code execution attempt detected",
                        details={"pattern": match.group()[:100]},
                    )
            
            return GuardrailResult(False, GuardrailCategory.CODE_EXECUTION, GuardrailAction.LOG, "Clean")


class GuardrailManager:
    """Manages and runs all guardrails."""
    
    def __init__(self):
        self.input_guardrails: List[BaseGuardrail] = []
        self.output_guardrails: List[BaseGuardrail] = []
        self._setup_default_guardrails()
    
    def _setup_default_guardrails(self):
        """Setup default guardrails."""
        # Input guardrails
        self.input_guardrails = [
            LengthGuardrail(),
            PromptInjectionGuardrail(),
            PIIGuardrail(GuardrailAction.REDACT),
            SystemPromptExtractionGuardrail(),
            CodeExecutionGuardrail(GuardrailAction.WARN),
        ]
        
        # Output guardrails (for LLM responses)
        self.output_guardrails = [
            PIIGuardrail(GuardrailAction.REDACT),
        ]
    
    async def check_input(self, content: str, context: Dict[str, Any] = None) -> List[GuardrailResult]:
        """Run all input guardrails."""
        results = []
        
        for guardrail in self.input_guardrails:
            if guardrail.enabled:
                result = await guardrail.check(content, context)
                results.append(result)
                
                if result.triggered and result.action == GuardrailAction.BLOCK:
                    # Stop on first blocking guardrail
                    break
        
        return results
    
    async def check_output(self, content: str, context: Dict[str, Any] = None) -> Tuple[str, List[GuardrailResult]]:
        """Run all output guardrails, return sanitized content and results."""
        results = []
        sanitized = content
        
        for guardrail in self.output_guardrails:
            if guardrail.enabled:
                result = await guardrail.check(sanitized, context)
                results.append(result)
                
                if result.sanitized_content:
                    sanitized = result.sanitized_content
        
        return sanitized, results
    
    def enable(self, category: GuardrailCategory):
        """Enable a guardrail category."""
        for g in self.input_guardrails + self.output_guardrails:
            if g.category == category:
                g.enabled = True
    
    def disable(self, category: GuardrailCategory):
        """Disable a guardrail category."""
        for g in self.input_guardrails + self.output_guardrails:
            if g.category == category:
                g.enabled = False
    
    def set_action(self, category: GuardrailCategory, action: GuardrailAction):
        """Set action for a guardrail category."""
        for g in self.input_guardrails + self.output_guardrails:
            if g.category == category:
                g.action = action


# Global guardrail manager
input_guardrails = GuardrailManager()
output_guardrails = GuardrailManager()  # Uses same instance for output