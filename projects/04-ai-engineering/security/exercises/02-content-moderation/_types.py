"""
=============================================================================
AI Security Exercise 02: Content Moderation Systems
=============================================================================

Topic: Content Moderation
-------------------------
Content moderation is essential for AI systems that interact with users.
This exercise covers detecting and filtering harmful content including
hate speech, violence, sexual content, self-harm, and custom policy
violations.

Learning Objectives:
  1. Build multi-category content classifiers
  2. Implement custom content policies
  3. Create moderation pipelines with severity levels
  4. Design human-in-the-loop review systems

Prerequisites:
  - Python 3.9+
  - re, json, hashlib, logging, dataclasses, enum, typing, abc
  - Optional: openai (for LLM-based moderation)

WARNING: This code is for EDUCATIONAL purposes.
=============================================================================
"""

import re
import json
import hashlib
import logging
import time
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Callable
from abc import ABC, abstractmethod
from collections import defaultdict


class ContentCategory(Enum):
    """Categories of content that may need moderation."""

    SAFE = auto()
    HATE_SPEECH = auto()
    VIOLENCE = auto()
    SEXUAL_CONTENT = auto()
    SELF_HARM = auto()
    HARASSMENT = auto()
    SPAM = auto()
    MISINFORMATION = auto()
    CUSTOM_POLICY = auto()


class SeverityLevel(Enum):
    """Severity levels for content violations."""

    NONE = 0
    LOW = 1  # Mildly inappropriate, may be acceptable in context
    MEDIUM = 2  # Clearly inappropriate, should be flagged
    HIGH = 3  # Severely inappropriate, should be blocked
    CRITICAL = 4  # Illegal or extremely harmful, block + report


@dataclass
class ModerationResult:
    """Result of a content moderation check."""

    category: ContentCategory
    severity: SeverityLevel
    confidence: float  # 0.0 - 1.0
    details: str
    flagged_terms: list[str] = field(default_factory=list)
    context_notes: str = ""
    recommended_action: str = "allow"
    timestamp: float = field(default_factory=time.time)

    @property
    def should_block(self) -> bool:
        return self.severity.value >= SeverityLevel.HIGH.value

    @property
    def should_flag(self) -> bool:
        return self.severity.value >= SeverityLevel.MEDIUM.value


@dataclass
class ModerationDecision:
    """Final moderation decision combining multiple category checks."""

    content_id: str
    is_allowed: bool
    overall_severity: SeverityLevel
    category_results: list[ModerationResult]
    requires_human_review: bool = False
    explanation: str = ""
    action_taken: str = ""


# =============================================================================
# Section 2: Base Moderator (Abstract)
# =============================================================================
