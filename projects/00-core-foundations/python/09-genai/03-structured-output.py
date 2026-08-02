"""
GenAI - 03: Structured Output
=============================
Topics: JSON mode, tool/function calling as structured extraction, Pydantic
schema validation, retry-on-invalid loops, when to use a grammar.

Why this matters for AI/backend engineering:
    Free text is not a system contract. To wire an LLM into your
    backend you must get *typed, validated* data out of it. Schema
    validation + retry-on-invalid is the difference between a demo
    and a reliable pipeline.

Run:      python 03-structured-output.py
Verify:   python 03-structured-output.py --verify
Reference: https://docs.pydantic.dev/latest/
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# 1. A Pydantic-style Schema
# ============================================================
# Declare the contract the LLM must fill. Validation is not optional:
# an LLM can emit valid JSON that is still wrong (missing fields, wrong
# types, out-of-range values).

@dataclass
class ExtractionSchema:
    name: str
    fields: dict[str, str]  # field -> type ("str", "int", "float", "bool")

    def validate(self, data: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        for fname, ftype in self.fields.items():
            if fname not in data:
                errors.append(f"missing field: {fname}")
                continue
            value = data[fname]
            if ftype == "int":
                if not isinstance(value, int) or isinstance(value, bool):
                    errors.append(f"{fname} must be int, got {type(value).__name__}")
            elif ftype == "float":
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    errors.append(f"{fname} must be float, got {type(value).__name__}")
            elif ftype == "str":
                if not isinstance(value, str):
                    errors.append(f"{fname} must be str, got {type(value).__name__}")
            elif ftype == "bool":
                if not isinstance(value, bool):
                    errors.append(f"{fname} must be bool, got {type(value).__name__}")
        return errors


# Example 1: schema validation
invoice = ExtractionSchema("invoice", {"id": "str", "amount": "float", "paid": "bool"})
good = {"id": "INV-1", "amount": 99.5, "paid": True}
bad = {"id": "INV-1", "amount": "ninety-nine", "paid": "yes"}
print("Example 1: schema validation")
print(f"  good: {invoice.validate(good)}")
print(f"  bad:  {invoice.validate(bad)}")
assert not invoice.validate(good)
assert len(invoice.validate(bad)) >= 2

# ============================================================
# 2. Parsing the LLM Output
# ============================================================
# The LLM returns text; we must parse JSON (tolerating markdown fences
# and stray prose) and validate it against the schema.

def parse_llm_json(text: str) -> dict[str, Any]:
    """Extract the first JSON object from an LLM response."""
    # strip markdown code fences
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
    return json.loads(cleaned)


# Example 2: parsing tolerant of markdown
raw = '```json\n{"id": "INV-2", "amount": 12.0, "paid": false}\n```'
parsed = parse_llm_json(raw)
print("\nExample 2: parse LLM JSON")
print(f"  parsed: {parsed}")
assert parsed["id"] == "INV-2"

# ============================================================
# 3. Retry-on-Invalid
# ============================================================
# The reliable pattern: ask -> parse -> validate -> retry with the
# error message fed back as a correction -> give up after N attempts.

@dataclass
class LLMExtractor:
    schema: ExtractionSchema
    max_retries: int = 3
    calls: int = 0

    def _ask(self, prompt: str) -> str:
        """Mock LLM: returns a fixable JSON blob. First call is broken."""
        self.calls += 1
        if self.calls == 1:
            return '{"id": "INV-3", "amount": "oops", "paid": true}'
        return '{"id": "INV-3", "amount": 45.0, "paid": true}'

    def extract(self, prompt: str) -> dict[str, Any]:
        for _ in range(self.max_retries):
            text = self._ask(prompt)
            try:
                data = parse_llm_json(text)
            except json.JSONDecodeError:
                continue
            errors = self.schema.validate(data)
            if not errors:
                return data
        raise ValueError(f"LLM failed to produce valid output after "
                         f"{self.max_retries} attempts")


# Example 3: self-correcting extraction
extractor = LLMExtractor(invoice)
result = extractor.extract("Extract the invoice")
print("\nExample 3: retry-on-invalid")
print(f"  final: {result}  (after {extractor.calls} calls)")
assert result["amount"] == 45.0 and extractor.calls == 2

# ============================================================
# 4. Tool/Function Calling Shape
# ============================================================
# Instead of asking for JSON in prose, declare a *tool* the model can
# call. The API enforces the argument structure.

def tool_schema(name: str, description: str, parameters: dict) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters,
        },
    }


# Example 4: a search tool schema
search_tool = tool_schema(
    "search_docs",
    "Search internal documentation by query and return top results",
    {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "limit": {"type": "integer", "minimum": 1, "maximum": 20},
        },
        "required": ["query"],
    },
)
print("\nExample 4: tool schema")
print(f"  tool: {search_tool['function']['name']}")
assert search_tool["function"]["parameters"]["required"] == ["query"]

# ============================================================
# Production Pattern
# ============================================================
# Gate structured extraction behind a bounded retry loop with an
# escalation: fall back to a deterministic regex parser before giving up.

def robust_extract(text: str, schema: ExtractionSchema,
                   llm: LLMExtractor, regex_fallback: Callable[[str], dict] | None
                   ) -> dict[str, Any]:
    try:
        return llm.extract(text)
    except ValueError:
        if regex_fallback is not None:
            return regex_fallback(text)
        raise


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: json.loads on raw LLM output (markdown fences, prose)
# MISTAKE: trusting the schema-less "valid JSON" - type errors slip in
# MISTAKE: no retry loop - one bad response breaks the whole pipeline
# MISTAKE: infinite retries - bound the loop and escalate


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    s = ExtractionSchema("t", {"a": "int", "b": "str"})
    assert not s.validate({"a": 1, "b": "x"}), "valid passes"
    assert s.validate({"a": "1", "b": "x"}), "wrong type flagged"
    assert s.validate({"a": 1}), "missing field flagged"
    assert s.validate({"a": True, "b": "x"}), "bool is not int"

    assert parse_llm_json('{"a": 1}') == {"a": 1}
    assert parse_llm_json('```json\n{"a": 2}\n```') == {"a": 2}

    # extractor exhausts retries -> raise
    always_bad = LLMExtractor(s, max_retries=2)
    always_bad._ask = lambda p: '{"a": "nope", "b": 1}'  # type: ignore[assignment]
    try:
        always_bad.extract("x")
        raised = False
    except ValueError:
        raised = True
    assert raised, "exhaustion raises"

    ts = tool_schema("f", "desc", {"type": "object", "properties": {}})
    assert ts["type"] == "function" and ts["function"]["name"] == "f"

    fallback_called = {"n": 0}
    def fb(text: str) -> dict:
        fallback_called["n"] += 1
        return {"a": 0, "b": "fallback"}
    ex = LLMExtractor(s, max_retries=1)
    ex._ask = lambda p: "not json at all"  # type: ignore[assignment]
    out = robust_extract("x", s, ex, fb)
    assert out == {"a": 0, "b": "fallback"} and fallback_called["n"] == 1
    print("[OK] 03-structured-output: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Declare a schema; validate every LLM output.")
        print("2. Parse tolerantly (fences/prose), retry on invalid.")
        print("3. Bound retries and escalate to a fallback parser.")
        _verify()
