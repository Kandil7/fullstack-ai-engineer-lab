"""
=============================================================================
AI Security Exercise 05: Data Privacy & Protection
=============================================================================

Topic: Data Privacy
-------------------
Data privacy is critical for AI systems that handle personal information.
This exercise covers PII detection, data anonymization, differential
privacy, data masking, and GDPR compliance patterns.

Learning Objectives:
  1. Detect PII across multiple data types (names, emails, phones, SSNs)
  2. Implement data anonymization techniques
  3. Understand differential privacy basics
  4. Design data masking strategies
  5. Build GDPR-compliant data handling patterns

Prerequisites:
  - Python 3.9+
  - re, hashlib, json, logging, dataclasses, enum, typing, math, random
  - Optional: faker (pip install faker) for test data generation

WARNING: This code is for EDUCATIONAL purposes.
=============================================================================
"""

import re
import hashlib
import json
import logging
import time
import math
import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Any
from collections import defaultdict


class PIIType(Enum):
    """Types of personally identifiable information."""

    NAME = auto()
    EMAIL = auto()
    PHONE = auto()
    SSN = auto()
    CREDIT_CARD = auto()
    IP_ADDRESS = auto()
    DATE_OF_BIRTH = auto()
    ADDRESS = auto()
    MEDICAL_RECORD = auto()
    BIOMETRIC = auto()
    PASSPORT = auto()
    DRIVER_LICENSE = auto()
    FINANCIAL_ACCOUNT = auto()
    CUSTOM = auto()


class AnonymizationMethod(Enum):
    """Methods for anonymizing data."""

    MASKING = auto()  # Replace with fixed characters
    HASHING = auto()  # One-way hash
    PSEUDONYMIZATION = auto()  # Replace with pseudonym
    GENERALIZATION = auto()  # Reduce precision
    SUPPRESSION = auto()  # Remove entirely
    NOISE_ADDITION = auto()  # Add statistical noise
    K_ANONYMITY = auto()  # Group into k-sized equivalence classes
    L_DIVERSITY = auto()  # Ensure l distinct values per class
    T_CLOSURENESS = auto()  # Limit distribution skew


class PrivacyLevel(Enum):
    """Privacy protection levels."""

    PUBLIC = 0  # No protection needed
    INTERNAL = 1  # Basic masking
    CONFIDENTIAL = 2  # Strong anonymization
    RESTRICTED = 3  # Full suppression + audit
    TOP_SECRET = 4  # Maximum protection


@dataclass
class PIIMatch:
    """A detected PII instance in text."""

    pii_type: PIIType
    value: str
    start: int
    end: int
    confidence: float
    context: str = ""


@dataclass
class AnonymizationResult:
    """Result of an anonymization operation."""

    method: AnonymizationMethod
    original: str
    anonymized: str
    pii_type: PIIType
    reversible: bool = False
    key: Optional[str] = None  # For reversible methods


@dataclass
class PrivacyAuditEntry:
    """Audit log entry for privacy operations."""

    timestamp: float
    operation: str
    pii_types: list[str]
    data_hash: str
    user_id: Optional[str] = None
    details: str = ""


# =============================================================================
# Section 2: PII Detection Engine
# =============================================================================


