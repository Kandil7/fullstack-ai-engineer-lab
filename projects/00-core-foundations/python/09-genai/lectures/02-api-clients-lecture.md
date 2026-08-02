# GenAI — 02: API Clients

## Topic Overview

An API client is the code that calls an LLM provider reliably: authentication,
request/response handling, retries, timeouts, error mapping, and provider
abstraction. Production LLM applications are *network applications first* —
most of the engineering is not in the "AI" but in making the calls to a remote
service robust, observable, and interchangeable. This lecture covers both the
OpenAI and Anthropic SDKs, the local model path (OpenAI-compatible servers),
and the reliability patterns that make LLM calls safe in production.

The core abstraction is the **chat-completion interface**: you send a list of
messages (`system`, `user`, `assistant`) and receive a completion. Every major
provider (OpenAI, Anthropic, Google, local via vLLM/Ollama) speaks roughly this
shape, which is why abstraction layers like **LiteLLM** exist — one client,
many providers. The AI engineer's job is to make this boundary: reliable
(retries + timeouts), observable (log cost, latency, tokens), and swappable
(an interface, not a vendor lock-in).

Why this matters: LLM calls fail constantly in the wild — rate limits (429),
timeouts (network, long generations), provider outages, context-window
overflows (400). Production clients handle all of these with exponential
backoff, token-aware budgeting, and graceful degradation. This lecture is
where "calling the model" becomes "operating the model."

## Learning Objectives

By the end of this lecture, you will be able to:
1. Send chat completions with the OpenAI and Anthropic SDKs
2. Build a provider-agnostic `LLMClient` interface (swap providers without code change)
3. Implement retries with exponential backoff + jitter for 429/5xx
4. Handle the standard errors: rate limit, timeout, context overflow, auth
5. Log tokens, latency, and cost per call
6. Stream responses for low-latency UX
7. Call local models (vLLM/Ollama) through the OpenAI-compatible endpoint

## Prerequisites

| Need | Where |
|---|---|
| LLM fundamentals | `09-genai/lectures/01-llm-fundamentals-lecture.md` |
| Python requests/HTTP | `05-web-frameworks/fastapi/` |
| Error handling | `01-core-python/` |
| Phase 8 observability | `08-mlops/lectures/11-monitoring-and-drift-lecture.md` |

## 1. The Chat-Completion Shape

All providers share one message shape: a list of `{role, content}` messages.

```python
messages = [
    {"role": "system", "content": "You are a concise assistant."},
    {"role": "user", "content": "Explain RAG in one sentence."},
]
# every provider: send messages, get a completion
```

Output:
```
{"role": "assistant", "content": "RAG retrieves relevant documents and
 feeds them to the model as context so answers are grounded in facts."}
```

The **system message** sets behavior; **user** is the query; **assistant**
messages carry prior turns (conversation history). This shape is so universal
that abstraction is trivial — and usually worth it.

## 2. OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")   # or env OPENAI_API_KEY

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Answer briefly."},
        {"role": "user", "content": "What is a vector embedding?"},
    ],
    temperature=0.2,
    max_tokens=200,
)
print(resp.choices[0].message.content)
print("usage:", resp.usage)   # prompt + completion tokens
```

Output:
```
A vector embedding is a dense numerical representation of text that captures
semantic meaning, enabling similarity search.
usage: CompletionUsage(prompt_tokens=24, completion_tokens=18, total_tokens=42)
```

Key details: the API key from env (never hardcode), `usage` gives the token
count for cost logging, and the response object is structured (`choices[0]`).

## 3. Anthropic SDK

```python
from anthropic import Anthropic

client = Anthropic()   # ANTHROPIC_API_KEY from env

resp = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=200,
    system="Answer briefly.",
    messages=[{"role": "user", "content": "What is a vector embedding?"}],
)
print(resp.content[0].text)
print("usage:", resp.usage.input_tokens, resp.usage.output_tokens)
```

Output:
```
A vector embedding maps text into a high-dimensional space where similar
meanings are near each other.
usage: 24 18
```

Note the differences: `system` is a top-level parameter (not a message),
`max_tokens` is required, and token usage is split into input/output. The
shape similarity makes abstraction straightforward.

## 4. The Provider-Agnostic Interface

The pattern that prevents vendor lock-in: define your own client interface,
implement it per provider, and inject it everywhere. The app never imports
`openai` or `anthropic` directly — it depends on the interface.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ChatMessage:
    role: str      # system | user | assistant
    content: str

@dataclass
class LLMResponse:
    content: str
    prompt_tokens: int
    completion_tokens: int
    model: str

class LLMClient(ABC):
    @abstractmethod
    def complete(self, messages: list[ChatMessage], **kwargs) -> LLMResponse:
        """Send messages, return a completion."""

class OpenAIAdapter(LLMClient):
    def __init__(self, model: str = "gpt-4o-mini", api_key: str = ""):
        from openai import OpenAI
        self._client = OpenAI(api_key=api_key)
        self.model = model

    def complete(self, messages, **kwargs) -> LLMResponse:
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[m.__dict__ for m in messages], **kwargs)
        return LLMResponse(
            content=resp.choices[0].message.content,
            prompt_tokens=resp.usage.prompt_tokens,
            completion_tokens=resp.usage.completion_tokens,
            model=self.model)
```

Output:
```
One client interface → OpenAI or Anthropic or local behind it.
```

Swapping providers is then a one-line change at wiring time, and every
cross-cutting concern (retries, logging, caching — Lectures 17–18) attaches to
the interface once.

## 5. Reliability: Retries, Backoff, Timeouts

LLM calls fail. The standard playbook: exponential backoff with jitter on
429 (rate limit) and 5xx (server), immediate failure on 4xx client errors
(bad request, auth), and a generous timeout for long generations.

```python
import time, random

def complete_with_retries(client, messages, *, max_retries=4, base_delay=1.0,
                          timeout_s=60):
    """Retry 429/5xx with exponential backoff + jitter."""
    for attempt in range(max_retries):
        try:
            return client.complete(messages, timeout=timeout_s)
        except RateLimitError as e:      # 429
            if attempt == max_retries - 1:
                raise
        except ServerError as e:         # 5xx
            if attempt == max_retries - 1:
                raise
        except TimeoutError as e:        # network/timeout
            if attempt == max_retries - 1:
                raise
        delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
        time.sleep(delay)
    raise RuntimeError("unreachable")
```

Output:
```
attempt 1 → 429 → sleep 1.3s → attempt 2 → 200 ✓
```

**Jitter** (random 0–0.5s) prevents the "thundering herd" — all retrying
clients hammering the API in sync. Without jitter, retries make rate limits
worse.

## 6. Streaming: First-Token Latency

For chat UX, stream tokens as they arrive instead of waiting for the full
response. First-token latency drops from seconds to milliseconds of perceived
delay.

```python
def stream_chat(client, messages, on_token):
    """Stream a completion, calling on_token per token."""
    stream = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, stream=True)
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            on_token(delta)   # e.g. push to an SSE/WebSocket client
```

Output:
```
t1: "RAG"   t2: " retrieves"   t3: " relevant"   ...   (token by token)
```

Streaming also lets you stop early (user cancels) and estimate total tokens
as you go — a cost-control lever.

## 7. Local Models: vLLM / Ollama

Local or self-hosted models expose an OpenAI-compatible endpoint, so the
*exact same* OpenAI client works — just point it at your server with no API
key.

```python
from openai import OpenAI

local = OpenAI(base_url="http://localhost:8000/v1", api_key="none")
resp = local.chat.completions.create(
    model="mistral-7b-instruct",
    messages=[{"role": "user", "content": "Hi, in one word: are you ready?"}],
)
print(resp.choices[0].message.content)
```

Output:
```
Yes
```

This is the key to **provider portability**: local (privacy, cost control) and
hosted (capability) are one code path apart — the interface decision pays off
again (see Lecture 22 for the full local-model story).

## Every Use Case

- **Chat assistants**: streaming, history, multi-turn.
- **Document extraction**: structured output from documents (L3).
- **Classification pipelines**: intent/routing/toxicity at scale.
- **Batch offline jobs**: summarize/evaluate corpora with token-aware batching.
- **Agents**: tool-calling loop over the same interface (L13–15).
- **RAG systems**: the generation stage (L9).
- **Multi-provider platforms**: fallback chains (primary fails → secondary).
- **Internal copilots**: shared gateway with budgets and logging (L17–18).
- **Local/private deployments**: self-hosted via OpenAI-compatible endpoints (L22).

## Real-World Use Cases for AI Engineers

- **SaaS customer-support copilot**: the client layer retries 429s with
  backoff during peak hours, streams responses for UX, and logs
  tokens-per-call to the cost dashboard (L18). The team's p99 error rate for
  LLM calls dropped from 8% to 0.4% just by adding the retry/timeout layer —
  before any model work.
- **Legal document extraction (insurance)**: a batch pipeline calls the API
  for 10k documents; a `LLMClient` interface means the team A/B tests OpenAI
  vs a local vLLM model by changing one line — the local model wins on cost
  and data-residency rules.
- **Startup with a hard budget**: every call goes through a gateway with
  token logging and prompt caching; the client's `usage` numbers feed the
  cost dashboard that keeps the product margin-positive (L18).
- **Agent platform**: the tool-calling agent (L13) calls the LLM dozens of
  times per task; each call carries retries + timeouts, and the whole loop is
  cancelable mid-stream when a user aborts.
- **Fallback chains**: a fintech app calls a primary provider, and on 5xx
  fails over to a secondary provider via the same interface — five nines of
  availability for the LLM boundary.

## Common Mistakes to Avoid

### Mistake 1: Hardcoding API keys
Keys in code leak into git history. Use environment variables / secret managers.

### Mistake 2: No retries with jitter
A single 429 storm retried in sync makes rate limits worse. Backoff + jitter.

### Mistake 3: No timeout
A hung generation blocks the worker forever. Always set a timeout.

### Mistake 4: No token logging
Without `usage`, you cannot track cost or detect runaway prompts (L17–18).

### Mistake 5: Vendor lock-in at the import level
`import openai` scattered through the app makes provider swaps a rewrite.
Use an interface.

### Mistake 6: Retrying 4xx client errors
A 400 (bad request) will fail forever; retrying wastes calls. Retry only
429/5xx/timeouts.

### Mistake 7: Ignoring the context-overflow error
400 with "maximum context length" needs a *strategy* (truncate, summarize,
retrieve) — not a retry.

## Best Practices

1. Read API keys from env/secret manager, never code
2. Abstract the provider behind your own `LLMClient` interface
3. Retry 429/5xx/timeouts with exponential backoff + jitter
4. Set explicit timeouts on every call
5. Log `usage` (tokens) and latency per call — cost and monitoring depend on it
6. Use streaming for interactive UX
7. Handle context-overflow with truncation/retrieval, not retries
8. Fall back across providers via the interface for availability
9. Use OpenAI-compatible endpoints for local models — one code path
10. Test with mock clients (no network) in CI

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| One completion | 0.5–10s | O(tokens) | fewer tokens / cheaper model |
| Retry on 429 | backoff × attempts | O(1) | better rate budgeting upstream |
| Streaming | first-token ~0.1s | O(1) | — |
| Provider fallback | +1 call | O(1) | only on failure |

## AI Engineering Relevance

**Where this shows up:** the client layer is the single chokepoint for
reliability, cost, and portability — every improvement here multiplies across
every LLM feature in the product.

| Concept here | Used for |
|---|---|
| Chat-completion shape | one interface for all providers |
| Retries/backoff | production reliability |
| Token logging | cost + observability |
| Interface abstraction | provider portability |

**Scale note:** at 1M calls/day, a 0.5% error rate is 5,000 failed calls/day —
the client layer's retries and fallbacks are what turn that into ~50. The
client is the first and most impactful place to invest.

## Practice Exercises

### Exercise 1: Mock Client (Easy)
Build a `MockLLMClient` that returns canned responses with fixed token counts;
write a test asserting the `LLMClient` interface is satisfied (no network).

### Exercise 2: Retry Logic (Medium)
Implement `complete_with_retries` with a fake client that fails twice with
429 then succeeds; assert the call count is 3 and the backoff delays were
increasing.

### Exercise 3: Provider Swap (Medium)
Implement `OpenAIAdapter` and `LocalAdapter` (both via the interface) and
write a function that runs the same task on both — proving the app code never
changes when the provider changes.

### Exercise 4: Cost Logger (Hard)
Extend the interface with a `logged_complete` wrapper that records
`{model, prompt_tokens, completion_tokens, latency_ms}` to a list; write
`summarize_costs(records)` returning total tokens and estimated cost, and
assert a mock sequence's numbers.

## Summary

| Concept | Description |
|---|---|
| Chat-completion shape | the universal message interface |
| Provider abstraction | one interface, many providers |
| Reliability | retries, backoff, timeouts, fallbacks |
| Token logging | the basis of cost and monitoring |
| Streaming | low first-token latency |
| Local compatibility | OpenAI-compatible endpoints |

Calling an LLM is a network problem with an AI flavor: the professional
engineering is in retries, abstraction, observability, and graceful failure.
The client layer is where reliability, cost, and portability are won or lost —
before any model-specific logic runs.

## Quick Reference

| Task | Idiom |
|---|---|
| Call OpenAI | `client.chat.completions.create(model=..., messages=...)` |
| Call Anthropic | `client.messages.create(model=..., max_tokens=..., system=...)` |
| Abstract | your own `LLMClient.complete(messages)` |
| Retry | backoff + jitter on 429/5xx only |
| Stream | `stream=True`, iterate chunks |
| Local | `OpenAI(base_url="http://localhost:8000/v1")` |

## Next Steps

Next: **[03 Structured Output](03-structured-output-lecture.md)** — forcing
reliable, schema-valid JSON out of the model.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/api-reference/chat,
https://docs.anthropic.com/en/api/messages
