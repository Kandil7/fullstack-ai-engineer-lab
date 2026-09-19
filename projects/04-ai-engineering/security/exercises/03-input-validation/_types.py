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
        return (
            not self.is_valid and self.threat_level.value >= ThreatLevel.MALICIOUS.value
        )

    @property
    def should_log(self) -> bool:
        return self.threat_level.value >= ThreatLevel.SUSPICIOUS.value


# =============================================================================
# Section 2: SQL Injection Prevention
# =============================================================================


