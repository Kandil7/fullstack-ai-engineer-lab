"""
GenAI - 17: LLM Observability
=============================
Topics: tracing a request through retrieval and generation; token/cost/
latency per call; prompt and response logging with PII care.

Why this matters for AI/backend engineering:
    A production LLM system you cannot see is a production incident you
    cannot diagnose. Per-request traces - tokens, cost, latency, the
    retrieved context, the prompt, the response - are the difference
    between "it's broken" and "here is exactly which retrieval chunk
    caused it".

Run:      python 17-llm-observability.py
Verify:   python 17-llm-observability.py --verify
Reference: https://docs.langfuse.com/
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# 1. The Span Model
# ============================================================
# A request = a trace with spans: retrieval, prompt-building, generation.
# Each span records duration, tokens, and cost.

@dataclass
class Span:
    name: str
    start_ns: int
    end_ns: int
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        return (self.end_ns - self.start_ns) / 1_000_000


@dataclass
class Trace:
    request_id: str
    spans: list[Span] = field(default_factory=list)
    total_cost: float = 0.0

    def add_span(self, span: Span) -> None:
        self.spans.append(span)

    def total_duration_ms(self) -> float:
        return sum(s.duration_ms for s in self.spans)

    def to_json(self) -> str:
        return json.dumps({
            "request_id": self.request_id,
            "spans": [{"name": s.name, "duration_ms": round(s.duration_ms, 2),
                       "meta": s.meta} for s in self.spans],
            "total_cost": self.total_cost,
            "total_duration_ms": round(self.total_duration_ms(), 2),
        }, indent=2)


# ============================================================
# 2. A Traced Request
# ============================================================

class TracedPipeline:
    def __init__(self, retrieve_fn: Callable[[str], list[str]],
                 generate_fn: Callable[[str], str],
                 price_per_1m_in: float = 3.0,
                 price_per_1m_out: float = 15.0) -> None:
        self.retrieve_fn = retrieve_fn
        self.generate_fn = generate_fn
        self.price_in, self.price_out = price_per_1m_in, price_per_1m_out
        self.traces: list[Trace] = []

    def estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4)

    def answer(self, query: str) -> tuple[str, Trace]:
        trace = Trace(request_id=f"req-{len(self.traces) + 1}")

        # span 1: retrieval
        t0 = time.perf_counter_ns()
        chunks = self.retrieve_fn(query)
        t1 = time.perf_counter_ns()
        trace.add_span(Span("retrieval", t0, t1, {"chunks": len(chunks)}))

        # span 2: generation
        t0 = time.perf_counter_ns()
        answer = self.generate_fn(query)
        t1 = time.perf_counter_ns()
        in_tokens = self.estimate_tokens(query)
        out_tokens = self.estimate_tokens(answer)
        cost = in_tokens / 1e6 * self.price_in + out_tokens / 1e6 * self.price_out
        trace.total_cost = cost
        trace.add_span(Span("generation", t0, t1,
                            {"in_tokens": in_tokens, "out_tokens": out_tokens,
                             "cost": round(cost, 6)}))

        self.traces.append(trace)
        return answer, trace


# Example 1: a traced call
def stub_retrieve(q: str) -> list[str]:
    time.sleep(0.002)
    return ["chunk about config", "chunk about deploy"]

def stub_generate(q: str) -> str:
    time.sleep(0.003)
    return "Set the API key in the environment file."

pipe = TracedPipeline(stub_retrieve, stub_generate)
answer, trace = pipe.answer("where is the key?")
print("Example 1: traced request")
print(trace.to_json())
assert len(trace.spans) == 2 and trace.total_cost > 0

# ============================================================
# 3. PII Care
# ============================================================
# Logs are a liability: prompts may contain customer data. Redact PII
# (emails, phone numbers, API keys) before logging.

PII_PATTERNS = [
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[EMAIL]"),
    (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),
    (r"sk-[A-Za-z0-9]{20,}", "[API_KEY]"),
]


def redact(text: str) -> str:
    import re
    for pattern, replacement in PII_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text


# Example 2: redaction
sensitive = "Contact jane@example.com or 555-123-4567. Key: sk-abcdefghijklmnopqrstuvwxyz"
redacted = redact(sensitive)
print("\nExample 2: PII redaction")
print(f"  {redacted}")
assert "[EMAIL]" in redacted and "[PHONE]" in redacted and "[API_KEY]" in redacted
assert "jane@" not in redacted

# ============================================================
# 4. Sampling
# ============================================================
# Logging every request is expensive. Log 100% of errors and failures,
# sample the success path (e.g. 10%).

def should_log(request_id: str, has_error: bool, sample_rate: float = 0.1) -> bool:
    if has_error:
        return True  # always log failures
    return int(request_id.split("-")[-1]) % 10 < int(sample_rate * 10)


# Example 3: sampling
print("\nExample 3: sampling")
for rid in ["req-1", "req-4", "req-9", "req-51"]:
    logged = should_log(rid, has_error=False, sample_rate=0.3)
    print(f"  {rid}: {'log' if logged else 'skip'}")
assert should_log("req-1", has_error=True), "errors always logged"
assert not should_log("req-51", has_error=False, sample_rate=0.1), "sampled out"
assert should_log("req-50", has_error=False, sample_rate=0.1), "ids ending 0 sampled in at 10%"
assert should_log("req-4", has_error=False, sample_rate=0.5), "ids ending <5 sampled in at 50%"

# ============================================================
# Production Pattern
# ============================================================
# The production logger: redact, then store the trace with a retention
# policy. Attach the trace id to every downstream error message.

def log_trace_safely(trace: Trace, prompt: str) -> dict:
    return {
        "request_id": trace.request_id,
        "duration_ms": trace.total_duration_ms(),
        "cost": trace.total_cost,
        "prompt_redacted": redact(prompt),
    }


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: logging raw prompts (PII breach by default)
# MISTAKE: no cost per request - the bill arrives without attribution
# MISTAKE: logging everything at 100% (storage bill) or nothing
# MISTAKE: no trace id linking logs to requests


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # trace math
    t0, t1 = time.perf_counter_ns(), time.perf_counter_ns() + 1_000_000
    s = Span("x", t0, t1)
    assert s.duration_ms >= 0.5, "span duration in ms"

    tr = Trace("r1")
    tr.add_span(s)
    tr.total_cost = 0.01
    j = tr.to_json()
    assert '"request_id": "r1"' in j and '"x"' in j, "trace serializes"

    # redaction
    assert redact("no pii here") == "no pii here"
    assert "[EMAIL]" in redact("mail me at a@b.com")

    # sampling
    assert should_log("req-0", False, 1.0), "100% sample logs"
    assert should_log("req-4", False, 0.5), "ids ending <5 sampled in at 50%"
    assert should_log("req-1", True, 0.0), "errors always logged even at 0%"

    # pipeline tracing
    p = TracedPipeline(lambda q: ["c"], lambda q: "a")
    ans, trace = p.answer("q")
    assert ans == "a" and trace.total_cost > 0, "traced end to end"

    safe = log_trace_safely(trace, "hi a@b.com")
    assert "[EMAIL]" in safe["prompt_redacted"], "safe logging redacts"
    print("[OK] 17-llm-observability: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Trace every request: retrieval + generation spans.")
        print("2. Record tokens, cost, latency per call.")
        print("3. Redact PII; log all errors, sample the happy path.")
        _verify()
