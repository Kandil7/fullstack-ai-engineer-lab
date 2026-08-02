"""
GenAI - 25: Case Study - High-Volume Structured Extraction
===========================================================
Topics: production structured extraction with validation, retry, cost
controls, and fallback - the full loop from topic 03 at volume.

Why this matters for AI/backend engineering:
    Extraction at volume is where cost discipline meets reliability:
    thousands of docs, each needing validated structured output, each
    costing tokens. The production loop - validate, retry, fallback,
    track cost - is the whole job.

Run:      python 25-case-study-extraction.py
Verify:   python 25-case-study-extraction.py --verify
Reference: https://docs.pydantic.dev/latest/
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# Components (compact forms of topic 03 + 18)
# ============================================================

@dataclass
class Schema:
    fields: dict[str, str]

    def validate(self, data: dict) -> list[str]:
        errors = []
        for name, kind in self.fields.items():
            if name not in data:
                errors.append(f"missing: {name}")
                continue
            v = data[name]
            if kind == "str" and not isinstance(v, str):
                errors.append(f"{name} must be str")
            elif kind == "float" and not isinstance(v, (int, float)):
                errors.append(f"{name} must be number")
            elif kind == "int" and not (isinstance(v, int) and not isinstance(v, bool)):
                errors.append(f"{name} must be int")
        return errors


def parse_llm_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
    return json.loads(cleaned)


# ============================================================
# The Extraction Service
# ============================================================

@dataclass
class ExtractionService:
    schema: Schema
    max_retries: int = 3
    price_per_1m: float = 3.0
    calls: int = 0
    failures: int = 0
    fallback_used: int = 0
    failed_docs: list[str] = field(default_factory=list)

    def _llm_extract(self, text: str) -> str:
        """Simulate an LLM: return correct JSON, but occasionally bad."""
        self.calls += 1
        if self.calls % 4 == 0:
            return '{"invoice_id": "broken", "amount": "NaN"}'
        return '{"invoice_id": "INV-001", "amount": 250.0}'

    def extract(self, text: str) -> dict:
        for _ in range(self.max_retries):
            raw = self._llm_extract(text)
            try:
                data = parse_llm_json(raw)
            except json.JSONDecodeError:
                continue
            if not self.schema.validate(data):
                return data
        self.failures += 1
        return {}

    def extract_many(self, docs: list[str],
                     fallback: Callable[[str], dict] | None = None) -> list[dict]:
        """Batch extraction with a regex fallback for hard failures."""
        results = []
        for doc in docs:
            data = self.extract(doc)
            if not data and fallback is not None:
                self.fallback_used += 1
                data = fallback(doc)
            if not data:
                self.failed_docs.append(doc[:40])
            results.append(data)
        return results

    def estimated_cost(self, docs: int, tokens_per_doc: int) -> float:
        return self.calls * tokens_per_doc / 1_000_000 * self.price_per_1m


# ============================================================
# Worked example: invoice extraction at volume
# ============================================================
invoice_schema = Schema({"invoice_id": "str", "amount": "float"})
service = ExtractionService(invoice_schema, max_retries=2, price_per_1m=3.0)

docs = [f"Invoice #{i}: total 100.0" for i in range(10)]


def regex_fallback(doc: str) -> dict:
    import re
    m = re.search(r"Invoice #(\d+).*?(\d+\.\d+)", doc)
    if m:
        return {"invoice_id": f"INV-{m.group(1)}", "amount": float(m.group(2))}
    return {}


results = service.extract_many(docs, fallback=regex_fallback)
print("=== Case study: extraction service ===")
ok_count = sum(1 for r in results if r)
print(f"  extracted ok: {ok_count}/{len(docs)}")
print(f"  fallbacks used: {service.fallback_used}")
print(f"  total failures: {service.failures}")
print(f"  failed docs: {service.failed_docs}")
print(f"  estimated cost: ${service.estimated_cost(len(docs), 200):.4f}")
assert ok_count == len(docs), "fallback rescues every doc"

# ============================================================
# Production Pattern
# ============================================================
# The production loop: validate -> retry -> fallback -> alert on
# failures. Failures are surfaced, not silently swallowed.

def production_extraction(docs: list[str], service: ExtractionService,
                          fallback: Callable[[str], dict],
                          alert: Callable[[list[str]], None]) -> list[dict]:
    results = service.extract_many(docs, fallback=fallback)
    if service.failed_docs:
        alert(service.failed_docs)
    return results


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: no retry - one bad response poisons the batch
# MISTAKE: no fallback - a whole batch fails over formatting drift
# MISTAKE: no cost tracking - extraction at volume surprises the bill
# MISTAKE: swallowing failures - bad extractions ship silently


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    s = Schema({"id": "str", "n": "int"})
    assert not s.validate({"id": "a", "n": 1})
    assert s.validate({"id": "a", "n": "x"}), "wrong type flagged"
    assert s.validate({"id": "a"}), "missing flagged"

    assert parse_llm_json('{"a": 1}') == {"a": 1}
    assert parse_llm_json('```json\n{"a": 2}\n```') == {"a": 2}

    svc = ExtractionService(Schema({"invoice_id": "str", "amount": "float"}),
                            max_retries=2)
    r = svc.extract("doc")
    assert r["invoice_id"] == "INV-001", "happy path extracts"

    # fallback rescues when LLM fails repeatedly
    always_bad = ExtractionService(Schema({"x": "str"}), max_retries=1)
    out = always_bad.extract_many(["d1", "d2"], fallback=lambda d: {"x": "fb"})
    assert out == [{"x": "fb"}, {"x": "fb"}], "fallback fills"

    assert svc.estimated_cost(10, 1000) == svc.calls * 1000 / 1e6 * svc.price_per_1m

    alerts = []
    production_extraction(["d1"], always_bad, lambda d: {}, alerts.append)
    assert alerts, "failures are surfaced"
    print("[OK] 25-case-study-extraction: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Validate -> retry -> fallback: the reliability loop.")
        print("2. Track cost per batch - extraction scales linearly.")
        print("3. Surface failures; never ship silently-bad extractions.")
        _verify()
