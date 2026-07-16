"""
Practice Problems — Module 09: AI Safety (NO SOLUTIONS)
========================================================
Solve these yourself! No hints, no solutions.

Run: python 09-ai-safety-practice.py
Select a problem number to see the description.

Categories:
  EASY (20 XP):   Problems 1-5
  MEDIUM (50 XP): Problems 6-10
  HARD (100 XP):  Problems 11-15

Prerequisites:
    pip install openai regex python-dotenv
"""

import re
import time
import hashlib
from dataclasses import dataclass, field
from typing import Any
from collections import defaultdict


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: PII Redactor
# Write a function that redacts personally identifiable information from text:
# - Emails: replace with [EMAIL]
# - Phone numbers: replace with [PHONE]
# - SSN (XXX-XX-XXXX): replace with [SSN]
# - Credit card numbers (16 digits): replace with [CARD]
# Return the redacted text.
def problem_01():
    pass  # Write your code here


# Problem 2: Input Length Validator
# Write a function that validates input length:
# - min_length: minimum characters (default 1)
# - max_length: maximum characters (default 10000)
# - Returns {"valid": bool, "error": str or None, "char_count": int}
# - Should also check for empty/whitespace-only input
def problem_02():
    pass  # Write your code here


# Problem 3: Content Category Classifier
# Write a function that classifies text into safety categories:
# - SAFE: normal content
# - HATE_SPEECH: hate or discrimination
# - VIOLENCE: threats or violent content
# - PII: contains personal information
# - ILLEGAL: references illegal activities
# Use simple keyword matching. Return the category and confidence.
def problem_03():
    pass  # Write your code here


# Problem 4: Output Sanitizer
# Write a function that sanitizes LLM output:
# - Removes HTML tags
# - Removes script injection attempts (eval, exec, import)
# - Removes excessive special characters
# - Truncates to max_length
# - Returns the sanitized text
def problem_04():
    pass  # Write your code here


# Problem 5: Audit Logger
# Write an AuditLogger class that:
# - Logs every LLM interaction with: timestamp, user_id, prompt_hash,
#   response_hash, category, flagged
# - Stores logs in memory (list of dicts)
# - Has search(user_id, start_time, end_time)
# - Has export(path) to write logs to JSON
class AuditLogger:
    def __init__(self):
        pass  # Write your code here

    def log(self, user_id: str, prompt: str, response: str,
            category: str, flagged: bool):
        pass  # Write your code here

    def search(self, user_id: str = None, start_time: float = None,
               end_time: float = None) -> list[dict]:
        pass  # Write your code here

    def export(self, path: str):
        pass  # Write your code here


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 6: Prompt Injection Detector
# Write a function that detects prompt injection attempts:
# - Instruction override: "ignore previous instructions", "forget everything"
# - Role manipulation: "you are now X", "act as X", "pretend to be X"
# - Delimiter attacks: "---", "===", "system:", "SYSTEM:"
# - Encoding attacks: base64 patterns, ROT13
# - Returns {"safe": bool, "risk_level": str, "findings": list[str]}
def problem_06():
    pass  # Write your code here


# Problem 7: Jailbreak Pattern Matcher
# Write a function that detects jailbreak patterns:
# - DAN (Do Anything Now) prompts
# - "Hypothetical" scenario attacks
# - "Developer mode" or "debug mode" requests
# - Token smuggling (splitting harmful words)
# - Role-play jailbreaks ("you are now in a movie where...")
# - Returns matches with confidence scores
def problem_07():
    pass  # Write your code here


# Problem 8: Token Budget Enforcer
# Write a TokenBudgetEnforcer class that:
# - Tracks token usage per user per time window
# - Has configurable limits (e.g., 1000 tokens per minute)
# - Returns remaining budget and reset time
# - Blocks requests when budget exceeded
# - Supports different limits for different user tiers
class TokenBudgetEnforcer:
    def __init__(self):
        pass  # Write your code here

    def check_budget(self, user_id: str, tier: str = "free") -> dict:
        pass  # Write your code here

    def record_usage(self, user_id: str, tokens: int):
        pass  # Write your code here

    def get_usage(self, user_id: str) -> dict:
        pass  # Write your code here


# Problem 9: Role Boundary Enforcer
# Write a function that enforces role boundaries:
# - System prompt should never be revealed
# - Agent should not perform out-of-scope actions
# - Checks if a response accidentally includes system prompt fragments
# - Validates that responses stay in the configured role
# - Returns {"compliant": bool, "violations": list[str]}
def problem_09():
    pass  # Write your code here


# Problem 10: Output Format Validator
# Write a function that validates LLM output against an expected format:
# - JSON: valid JSON with required fields
# - Email: valid email format
# - URL: valid URL
# - Number: valid number within range
# - Custom regex pattern
# Returns {"valid": bool, "error": str, "parsed": Any}
def problem_10():
    pass  # Write your code here


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 11: Multi-Layer Content Filter
# Write a ContentFilter class with multiple filter layers:
# - Layer 1: Keyword blacklist (fast, catches obvious cases)
# - Layer 2: Regex patterns (catches structured attacks)
# - Layer 3: Semantic similarity (embed and compare to known bad examples)
# - Layer 4: LLM classifier (slow but accurate, only for borderline cases)
# - Returns combined risk score and which layer flagged
class ContentFilter:
    def __init__(self):
        pass  # Write your code here

    def filter(self, text: str) -> dict:
        pass  # Write your code here

    def add_to_blacklist(self, pattern: str):
        pass  # Write your code here

    def get_stats(self) -> dict:
        pass  # Write your code here


# Problem 12: Abuse Pattern Detector
# Write an AbuseDetector class that:
# - Tracks user behavior over time
# - Detects: rapid-fire requests, prompt stuffing, token exhaustion attacks
# - Detects: adversarial inputs (special characters, unicode tricks)
# - Computes a risk score per user
# - Auto-blocks users exceeding risk threshold
# - Returns risk reports
class AbuseDetector:
    def __init__(self, risk_threshold: float = 0.8):
        pass  # Write your code here

    def analyze_request(self, user_id: str, prompt: str) -> dict:
        pass  # Write your code here

    def get_risk_score(self, user_id: str) -> float:
        pass  # Write your code here

    def block_user(self, user_id: str, reason: str):
        pass  # Write your code here


# Problem 13: Guardrails Pipeline
# Write a GuardrailsPipeline class that:
# - Pre-process: input validation, injection detection, PII redaction
# - During generation: token budget, content filtering
# - Post-process: output validation, format checking, hallucination detection
# - Each step can block, modify, or pass the content
# - Returns a full audit trail of what happened at each step
class GuardrailsPipeline:
    def __init__(self):
        pass  # Write your code here

    def add_guard(self, name: str, stage: str, fn: Callable):
        pass  # Write your code here

    def process(self, user_id: str, prompt: str, generate_fn: Callable) -> dict:
        pass  # Write your code here

    def get_audit_trail(self, request_id: str) -> list[dict]:
        pass  # Write your code here


# Problem 14: Incident Response Logger
# Write an IncidentLogger class that:
# - Logs safety incidents with severity (low/medium/high/critical)
# - Captures: timestamp, user_id, incident_type, evidence, action_taken
# - Auto-escalates: 3 medium incidents → 1 high
# - 5 high incidents → alert (returns alert dict)
# - Generates incident reports
# - Exports to JSON for compliance
class IncidentLogger:
    def __init__(self):
        pass  # Write your code here

    def log_incident(self, user_id: str, incident_type: str,
                     evidence: dict, action_taken: str, severity: str = "low"):
        pass  # Write your code here

    def get_user_history(self, user_id: str) -> list[dict]:
        pass  # Write your code here

    def check_escalation(self, user_id: str) -> dict | None:
        pass  # Write your code here

    def generate_report(self, incident_id: str) -> dict:
        pass  # Write your code here

    def export_compliance(self, path: str):
        pass  # Write your code here


# Problem 15: Complete Safety System
# Build a SafetySystem class that combines everything:
# - Input guard: injection detection, PII redaction, length validation
# - Content filter: multi-layer filtering
# - Token budget: per-user rate limiting
# - Output guard: format validation, hallucination check
# - Audit logging: full interaction history
# - Incident tracking: auto-escalation and reporting
# - Abuse detection: behavioral analysis
# - Returns a comprehensive safety report for each request
class SafetySystem:
    def __init__(self):
        pass  # Write your code here

    def process_request(self, user_id: str, prompt: str,
                        generate_fn: Callable) -> dict:
        pass  # Write your code here

    def get_safety_report(self, request_id: str) -> dict:
        pass  # Write your code here

    def get_user_risk_profile(self, user_id: str) -> dict:
        pass  # Write your code here

    def export_compliance_report(self, path: str, date_range: tuple = None):
        pass  # Write your code here


# ============================================================
# MAIN — Run to see problem descriptions
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Module 09: AI Safety — Practice Problems")
    print("=" * 60)
    print()

    problems = {
        1: ("PII Redactor", "Easy", 20),
        2: ("Input Length Validator", "Easy", 20),
        3: ("Content Category Classifier", "Easy", 20),
        4: ("Output Sanitizer", "Easy", 20),
        5: ("Audit Logger", "Easy", 20),
        6: ("Prompt Injection Detector", "Medium", 50),
        7: ("Jailbreak Pattern Matcher", "Medium", 50),
        8: ("Token Budget Enforcer", "Medium", 50),
        9: ("Role Boundary Enforcer", "Medium", 50),
        10: ("Output Format Validator", "Medium", 50),
        11: ("Multi-Layer Content Filter", "Hard", 100),
        12: ("Abuse Pattern Detector", "Hard", 100),
        13: ("Guardrails Pipeline", "Hard", 100),
        14: ("Incident Response Logger", "Hard", 100),
        15: ("Complete Safety System", "Hard", 100),
    }

    total_xp = sum(p[2] for p in problems.values())
    print(f"Total Problems: {len(problems)}")
    print(f"Total XP: {total_xp}")
    print()

    for num, (name, diff, xp) in problems.items():
        print(f"  [{num:2d}] {name:<40} {diff:<8} +{xp} XP")

    print()
    print("Select a problem number to see its full description.")
    print("Solve each function by replacing 'pass' with your implementation.")
    print("No solutions are provided — figure it out yourself!")
    print("=" * 60)
