"""
03 Input Validation: Command Injection
"""

from ._types import *


class CommandInjectionValidator:
    """
    Detects and prevents command injection attacks.

    Particularly important for AI systems with tool-use capabilities
    that execute shell commands or system operations.
    """

    COMMAND_INJECTION_PATTERNS = {
        "shell_metacharacters": [
            r"[;&|`$]",  # Shell metacharacters
            r"\$\(",  # Command substitution
            r"\$\{",  # Variable expansion
            r">[>&]",  # Redirect/duplicate
            r"\\n|\\r",  # Newline injection
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
            r"(?i)\\\\[^\\]+\\",  # UNC path
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
            self.compiled_patterns[category] = [re.compile(pat) for pat in patterns]

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
