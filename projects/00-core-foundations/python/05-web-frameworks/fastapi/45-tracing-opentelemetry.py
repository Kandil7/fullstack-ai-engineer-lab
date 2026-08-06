"""
FastAPI — 45: Tracing with OpenTelemetry
==========================================
Topics: spans and context propagation; auto vs manual instrumentation;
        sampling; tracing across services; tracing an async RAG pipeline

Why this matters for AI/backend engineering:
    Metrics say HOW the service is doing; traces say WHERE the time went.
    A distributed trace is a tree of spans — one root span per request,
    child spans per call — connected by propagated context (trace_id,
    span_id). For an async RAG pipeline the trace answers the question
    metrics cannot: "is the 2.4s spent in retrieval, embedding, or the
    LLM call?" OpenTelemetry is the standard: vendor-neutral, auto-
    instrumentation for libraries + manual spans for your code.

Run:      python 45-tracing-opentelemetry.py
Verify:   python 45-tracing-opentelemetry.py --verify
Reference: https://opentelemetry.io/docs/
"""

from __future__ import annotations

import sys
import time
from typing import Optional

from opentelemetry import trace, context as otel_context
from opentelemetry.sdk.trace import TracerProvider, ReadableSpan
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter

# ============================================================
# 0. In-memory exporter so we can inspect spans without a backend
# ============================================================
class InMemoryExporter(SpanExporter):
    """Collect finished spans into a list (no collector needed)."""

    def __init__(self) -> None:
        self.spans: list[ReadableSpan] = []

    def export(self, spans):
        self.spans.extend(spans)
        return 0

    def shutdown(self) -> None:
        pass


exporter = InMemoryExporter()
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)
TRACER = trace.get_tracer("rag-service")


def reset() -> None:
    exporter.spans.clear()


# ============================================================
# 1. Spans: the unit of tracing
# ============================================================
# A span is a named, timed unit of work with attributes. Parent-child
# spans form a tree: the root is the request; children are the calls
# it made. The trace_id is shared across the whole tree.

def single_span() -> None:
    with TRACER.start_as_current_span("http.request", kind=trace.SpanKind.SERVER) as span:
        span.set_attribute("http.path", "/generate")
        span.set_attribute("http.status_code", 200)
        time.sleep(0.01)   # simulated work
        with TRACER.start_as_current_span("inference.call") as child:
            child.set_attribute("model", "gpt-4o-mini")
            time.sleep(0.005)


print("=== 1. Spans ===")
reset()
single_span()
root = exporter.spans[0]
child = exporter.spans[1]
print(f"root span : {root.name} ({root.duration_s*1000:.1f}ms)")
print(f"child span: {child.name} model={child.attributes.get('model')}")
print(f"shared trace_id: {root.context.trace_id == child.context.trace_id}")
print(f"parent link     : {child.parent.span_id == root.context.span_id}")
print()

# ============================================================
# 2. Tracing an async RAG pipeline end to end
# ============================================================
# The trace tree reveals WHERE latency goes. Without it you only know
# the total; with it you know retrieval vs embed vs LLM vs rerank.

def rag_query(query: str) -> float:
    """Simulated RAG pipeline; each stage is a child span."""
    with TRACER.start_as_current_span("rag.query", kind=trace.SpanKind.SERVER) as root_span:
        root_span.set_attribute("query_len", len(query))
        with TRACER.start_as_current_span("retrieval") as s1:
            s1.set_attribute("top_k", 5)
            time.sleep(0.02)
        with TRACER.start_as_current_span("embedding") as s2:
            s2.set_attribute("model", "bge-large")
            time.sleep(0.01)
        with TRACER.start_as_current_span("llm.generate") as s3:
            s3.set_attribute("model", "gpt-4o-mini")
            s3.set_attribute("tokens_in", 512)
            time.sleep(0.05)
        return root_span.duration_s


print("=== 2. RAG pipeline trace ===")
reset()
total = rag_query("what is RAG?")
rows = [(s.name, round(s.duration_s * 1000, 1)) for s in exporter.spans]
print(f"total {total*1000:.1f}ms split into:")
for name, ms in rows:
    print(f"  {name:<16} {ms:>6.1f}ms")
print()

# ============================================================
# 3. Context propagation across service boundaries
# ============================================================
# Context is carried explicitly across process boundaries (HTTP
# headers: traceparent). Here we simulate it with a dict 'wire'.

def propagate_across_boundary() -> tuple[str, str]:
    """Pass the tracing context over a simulated wire, then continue."""
    reset()
    with TRACER.start_as_current_span("gateway.request") as gw:
        # serialize the current context to a fake header
        ctx = otel_context.get_current()
        carrier: dict[str, str] = {}
        from opentelemetry.propagators.tracecontext import TraceContextTextMapPropagator
        TraceContextTextMapPropagator().inject(carrier, context=ctx)
        # downstream service extracts and creates a child span
        extracted = TraceContextTextMapPropagator().extract(carrier)
        token = otel_context.attach(extracted)
        try:
            with TRACER.start_as_current_span("inference.service") as inf:
                inf.set_attribute("node", "worker-3")
        finally:
            otel_context.detach(token)
    return (str(gw.context.trace_id), str(inf.context.trace_id))


print("=== 3. Context propagation ===")
gw_tid, inf_tid = propagate_across_boundary()
print(f"same trace across 'services': {gw_tid == inf_tid}")
print()

# ============================================================
# 4. Sampling — bounding trace volume
# ============================================================
# Traces are expensive to store. Head sampling decides BEFORE the
# request (fixed % / rate); tail sampling decides AFTER (keep the
# slow/failing ones). Parent-based sampling keeps trees consistent.

def head_sample(rate: float, trace_id: int) -> bool:
    """Deterministic head sampling: hash the trace_id vs the rate."""
    return (trace_id % 1000) < rate * 1000


print("=== 4. Sampling ===")
kept = sum(1 for i in range(1000) if head_sample(0.1, i))
print(f"10% head sampling kept {kept}/1000 traces")
print()

# ============================================================
# 5. Manual vs auto instrumentation
# ============================================================
# Auto: library instrumentation (httpx, sqlalchemy, fastapi) creates
# spans for you. Manual: your business code's spans (the RAG stages
# above). Production uses both — auto for the framework, manual for
# the domain.

AUTO = ["fastapi", "httpx", "sqlalchemy", "redis", "openai"]
MANUAL = ["retrieval", "embedding", "llm.generate", "rerank"]

print("=== 5. Auto vs manual ===")
print(f"auto-instrumented: {AUTO}")
print(f"manual (domain)  : {MANUAL}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: tracing only the entry — the child spans are the diagnosis
# CORRECT: span every boundary call (retrieval, embed, LLM, rerank)
#
# MISTAKE: forgetting propagation — child service starts a NEW trace
# CORRECT: extract traceparent at every boundary; continue the tree
#
# MISTAKE: 100% sampling of expensive traces at high rps
# CORRECT: head sampling by trace_id; tail sampling for slow/failing
#
# MISTAKE: no attributes — a span without model/endpoint is anonymous
# CORRECT: set the attributes that make a span queryable
#
# MISTAKE: manual-only (framework spans missing) or auto-only (no domain)
# CORRECT: both layers

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Span tree: child shares trace_id and links to parent
    reset()
    single_span()
    assert len(exporter.spans) == 2, "root + child spans"
    root, child = exporter.spans[0], exporter.spans[1]
    assert root.context.trace_id == child.context.trace_id, "same trace"
    assert child.parent.span_id == root.context.span_id, "parent linkage"
    assert root.attributes.get("http.path") == "/generate", "attributes ride along"

    # 2. RAG pipeline: 4 spans, sum of children <= root
    reset()
    rag_query("hello")
    names = sorted(s.name for s in exporter.spans)
    assert set(names) == {"llm.generate", "rag.query", "retrieval", "embedding"}, names
    children_total = sum(s.duration_s for s in exporter.spans if s.name != "rag.query")
    root_span = next(s for s in exporter.spans if s.name == "rag.query")
    assert children_total <= root_span.duration_s + 1e-9, "children fit inside root"

    # 3. Propagation: same trace_id across the simulated boundary
    gw, inf = propagate_across_boundary()
    assert gw == inf, "propagated context must continue the trace"

    # 4. Sampling rate respected
    kept = sum(1 for i in range(2000) if head_sample(0.1, i))
    assert 0.05 * 2000 < kept < 0.15 * 2000, f"10% sampling got {kept}/2000"

    print("[OK] 45-tracing-opentelemetry: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Spans = named timed work; trees = the request story")
        print("2. RAG trace: retrieval/embed/LLM each visible")
        print("3. traceparent propagation continues the trace across services")
        print("4. Head sampling bounds volume; auto+manual cover both layers")
        _verify()          # always runs, so plain execution is also a test
