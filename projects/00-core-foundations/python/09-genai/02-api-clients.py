"""
GenAI - 02: API Clients
=======================
Topics: OpenAI/Anthropic SDKs, messages format, system prompts, streaming,
retries on 429/503 with backoff, timeouts, token counting before sending.
Uses a mock client so it runs offline; the pattern transfers to the SDKs.

Why this matters for AI/backend engineering:
    Production LLM code is mostly plumbing: correct request shapes,
    exponential backoff, timeouts, and graceful degradation. Getting
    these wrong is how a spike in traffic becomes an outage and a
    billing shock.

Run:      python 02-api-clients.py
Verify:   python 02-api-clients.py --verify
Reference: https://platform.openai.com/docs/api-reference/chat
"""

from __future__ import annotations

import random
import sys
import time
from dataclasses import dataclass
from typing import Any, Callable


# ============================================================
# 1. The Messages Format
# ============================================================
# The universal shape: a list of {role, content} dicts. system sets
# behavior, user is the request, assistant is prior turns.

def build_messages(system: str, user: str,
                   history: list[dict] | None = None) -> list[dict]:
    msgs = [{"role": "system", "content": system}]
    if history:
        msgs.extend(history)
    msgs.append({"role": "user", "content": user})
    return msgs


# Example 1: request shape
msgs = build_messages(
    system="You are a terse code reviewer.",
    user="Review this: x = 1",
    history=[{"role": "assistant", "content": "acknowledged"}],
)
print("Example 1: messages format")
for m in msgs:
    print(f"  {m['role']}: {m['content'][:40]}")
assert msgs[0]["role"] == "system" and msgs[-1]["role"] == "user"

# ============================================================
# 2. A Mock LLM Client
# ============================================================
# Simulates the OpenAI client surface: create() + streaming. A tiny
# deterministic "model" so tests never hit the network.

@dataclass
class MockResponse:
    content: str

    def __str__(self) -> str:
        return self.content


class MockClient:
    def __init__(self, replies: list[str] | None = None) -> None:
        self.replies = replies or [
            "Understood. Here is the analysis you asked for.",
        ]
        self.calls = 0

    def create(self, model: str, messages: list[dict],
               temperature: float = 0.7, **kwargs: Any) -> MockResponse:
        self.calls += 1
        user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        reply = self.replies[min(len(self.replies) - 1, max(0, len(user) % len(self.replies)))]
        return MockResponse(reply)


# Example 2: a call through the mock
client = MockClient()
resp = client.create("mock-model", build_messages("be brief", "summarize python"))
print("\nExample 2: chat completion")
print(f"  response: {resp.content}")

# ============================================================
# 3. Retries with Exponential Backoff
# ============================================================
# 429 (rate limit) and 503 (overloaded) are transient - retry with
# backoff and jitter. 4xx like 400 are permanent - fail fast.

@dataclass
class RetryPolicy:
    max_retries: int = 3
    base_delay_s: float = 0.05
    max_delay_s: float = 2.0

    def retry_delay(self, attempt: int) -> float:
        delay = min(self.base_delay_s * (2 ** attempt), self.max_delay_s)
        # jitter within [0.5x, 1.0x] so backoff never exceeds the cap
        return delay * (0.5 + random.random() * 0.5)


def call_with_retries(fn: Callable[[], Any], policy: RetryPolicy,
                      transient_statuses: set[int]) -> Any:
    """Call fn, retrying on transient failures with backoff."""
    attempt = 0
    while True:
        try:
            return fn()
        except RateLimitError as e:
            attempt += 1
            if e.status not in transient_statuses or attempt > policy.max_retries:
                raise
            time.sleep(policy.retry_delay(attempt - 1))


class RateLimitError(Exception):
    def __init__(self, status: int, message: str = "") -> None:
        super().__init__(message)
        self.status = status


# Example 3: transient failure is retried; permanent is not
attempts = {"n": 0}

def flaky_call() -> str:
    attempts["n"] += 1
    if attempts["n"] < 3:
        raise RateLimitError(429, "rate limited")
    return "ok"

policy = RetryPolicy(max_retries=4, base_delay_s=0.01)
result = call_with_retries(flaky_call, policy, transient_statuses={429, 503})
print("\nExample 3: retries with backoff")
print(f"  result={result} after {attempts['n']} attempts")
assert result == "ok" and attempts["n"] == 3

# ============================================================
# 4. Timeouts
# ============================================================
# A request without a timeout can hang forever, tying up a worker
# and its memory. Set a connect + read timeout and treat timeout as
# a retryable (or fallback) event.

def call_with_timeout(fn: Callable[[], Any], timeout_s: float) -> Any:
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(fn)
        try:
            return future.result(timeout=timeout_s)
        except concurrent.futures.TimeoutError:
            future.cancel()
            raise TimeoutError(f"call exceeded {timeout_s}s")


def slow_call() -> str:
    time.sleep(0.5)
    return "slow but done"


# Example 4: timeout enforcement
try:
    call_with_timeout(slow_call, timeout_s=0.1)
    timed_out = False
except TimeoutError:
    timed_out = True
print("\nExample 4: timeouts")
print(f"  slow call with 0.1s timeout -> timed out: {timed_out}")
assert timed_out

# ============================================================
# Production Pattern
# ============================================================
# The production call path: build messages -> count tokens -> call
# with retries and timeout -> inspect the result -> return or raise.

def robust_completion(client: MockClient, system: str, user: str,
                      retries: RetryPolicy, timeout_s: float,
                      transient_statuses: set[int]) -> str:
    messages = build_messages(system, user)

    def do_call() -> str:
        return call_with_timeout(
            lambda: client.create("gpt-4o-mini", messages), timeout_s
        ).content

    return call_with_retries(do_call, retries, transient_statuses)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: no timeout - a hung upstream takes down your endpoint
# MISTAKE: retrying 400s forever (permanent errors never recover)
# MISTAKE: no jitter - synchronized retries thundering-herd the API
# MISTAKE: forgetting the system prompt in the messages


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    m = build_messages("s", "u")
    assert m == [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]

    c = MockClient(["hello"])
    r = c.create("m", build_messages("", "hi"))
    assert r.content == "hello" and c.calls == 1

    # retry policy: transient retried
    n = {"calls": 0}
    def flaky() -> str:
        n["calls"] += 1
        if n["calls"] < 3:
            raise RateLimitError(503)
        return "done"
    out = call_with_retries(flaky, RetryPolicy(max_retries=5, base_delay_s=0.0),
                            transient_statuses={503})
    assert out == "done" and n["calls"] == 3, "transient retried"

    # permanent error fails fast
    n2 = {"calls": 0}
    def perm() -> str:
        n2["calls"] += 1
        raise RateLimitError(400)
    try:
        call_with_retries(perm, RetryPolicy(max_retries=5, base_delay_s=0.0),
                          transient_statuses={429, 503})
        raised = False
    except RateLimitError:
        raised = True
    assert raised and n2["calls"] == 1, "permanent fails fast"

    assert RetryPolicy(base_delay_s=0.1).retry_delay(0) <= 0.1, "backoff bounded"

    text = robust_completion(MockClient(["final"]), "s", "q",
                             RetryPolicy(max_retries=1, base_delay_s=0.0), 5.0, {503})
    assert text == "final", "robust completion works"
    print("[OK] 02-api-clients: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Messages = [{role, content}, ...] with a system prompt.")
        print("2. Retry 429/503 with exponential backoff + jitter.")
        print("3. Always set timeouts; fail fast on permanent errors.")
        _verify()
