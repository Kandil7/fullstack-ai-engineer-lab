"""
=============================================================================
AI Security Exercise 04: Output Filtering & Safety
=============================================================================

Topic: Output Filtering
-----------------------
Output filtering ensures AI-generated content is safe, accurate, and
appropriate before reaching users. This exercise covers PII detection,
toxicity filtering, hallucination detection, groundedness checking, and
output quality scoring.

Learning Objectives:
  1. Detect and mask PII in AI outputs
  2. Filter toxic and harmful content from responses
  3. Detect hallucinations and verify factual accuracy
  4. Score output quality and groundedness
  5. Build production-ready output filtering pipelines

Prerequisites:
  - Python 3.9+
  - re, json, hashlib, logging, dataclasses, enum, typing, math
  - Optional: openai (for LLM-based detection)

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
from collections import defaultdict


class FilterCategory(Enum):
    """Categories of output filtering."""

    PII = auto()
    TOXICITY = auto()
    HALLUCINATION = auto()
    GROUNDEDNESS = auto()
    QUALITY = auto()
    CITATION = auto()
    SAFETY = auto()


class SeverityLevel(Enum):
    """Severity levels for filter results."""

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class FilterResult:
    """Result of a single output filter check."""

    category: FilterCategory
    passed: bool
    severity: SeverityLevel
    confidence: float  # 0.0 - 1.0
    details: str
    flagged_items: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class OutputVerdict:
    """Final verdict combining all filter results."""

    content_id: str
    is_safe: bool
    overall_score: float  # 0.0 - 1.0 (1.0 = perfect)
    filter_results: list[FilterResult]
    requires_human_review: bool = False
    blocked_sections: list[str] = field(default_factory=list)
    explanation: str = ""


# =============================================================================
# Section 2: PII Detection & Masking
# =============================================================================
