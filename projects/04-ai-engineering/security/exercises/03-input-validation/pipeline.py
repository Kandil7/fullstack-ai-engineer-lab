"""
03 Input Validation: Pipeline
"""

from ._types import *
from .command_injection import CommandInjectionValidator
from .constraints import ConstraintValidator, InputConstraints
from .path_traversal import PathTraversalValidator
from .sql_injection import SQLInjectionValidator
from .xss import XSSValidator


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
            "xss": XSSValidator(allowed_tags=config.get("allowed_html_tags", [])),
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
        self.validation_log.append(
            {
                "input_hash": hashlib.sha256(text.encode()).hexdigest()[:16],
                "valid": overall_valid,
                "max_threat": max_threat.name,
                "validators_run": list(results.keys()),
                "timestamp": time.time(),
            }
        )

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
        priority_order = [
            "constraint",
            "xss",
            "sql_injection",
            "command_injection",
            "path_traversal",
        ]
        for name in priority_order:
            if name in results and results[name].sanitized_output:
                return results[name].sanitized_output
        return ""


# =============================================================================
# Section 8: Demonstration & Testing
# =============================================================================
