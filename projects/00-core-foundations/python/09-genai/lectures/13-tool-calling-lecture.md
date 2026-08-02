# GenAI — 13: Tool Calling

## Topic Overview

Tool calling (function calling) is the mechanism that lets an LLM request an
action it cannot perform itself — query a database, call an API, run code,
look up a document — by emitting a **structured function call** instead of
plain text. The model does not *execute* anything; it *declares* what it wants
(`tool: get_weather, args: {"city": "Cairo"}`), and your code executes it and
feeds the result back. This is the bridge from "chatbot that talks" to "agent
that acts" (L14), and the foundation of every tool-using system in production.

The loop (each iteration is one LLM call):

```
user request → model → tool call {name, args}
   → your code validates + executes the tool
   → tool result returned to the model
   → model produces the final answer (or another tool call)
```

Why this matters: tool calling is where LLMs become *useful* in systems —
grounding answers in live data (search, databases), taking actions (booking,
ordering), and composing workflows. The engineering discipline is in
**validation**: the model's args are generated text; they are parsed,
schema-checked (L3), and validated *before any tool executes*. A malformed
amount must never reach a payment API.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the tool-calling loop (model requests → you execute → feed back)
2. Define tools with schemas (name, description, JSON-schema args)
3. Parse and validate the model's tool calls before execution (L3 discipline)
4. Execute tools safely: allowlists, timeouts, error mapping
5. Feed tool results back correctly (the message contract)
6. Handle the failure modes: malformed args, missing tools, tool errors
7. Choose native tool-calling (OpenAI/Anthropic) vs prompt-based calling (local models)

## Prerequisites

| Need | Where |
|---|---|
| Structured output | `09-genai/lectures/03-structured-output-lecture.md` |
| API clients | `09-genai/lectures/02-api-clients-lecture.md` |
| Pydantic | `05-web-frameworks/fastapi/` |
| Python function basics | `01-core-python/` |

## 1. Defining a Tool

A tool is a function + a schema the model can read: **name**, **description**
(what it does, when to use it), and **parameters** (JSON schema). The
description is the prompt for tool selection — the model chooses tools by
their descriptions, so descriptions must be precise.

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city. Use when the user asks about weather.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": "Search internal documentation. Use for product questions.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]
```

Output:
```
Two tools registered: get_weather, search_docs (with argument schemas).
```

**Less is more:** too many tools with vague descriptions → the model picks
wrong. Every tool earns its place by being *discoverable and unambiguous*.

## 2. The Tool-Calling Loop

```python
def run_with_tools(user_input: str, llm_client, tools: list, registry: dict) -> str:
    messages = [{"role": "user", "content": user_input}]
    for _ in range(MAX_STEPS):                      # bound the loop
        resp = llm_client.complete(messages, tools=tools)
        if not resp.tool_calls:
            return resp.content                      # final answer
        messages.append(resp.message)                # model's tool request
        for call in resp.tool_calls:
            result = execute_tool(call, registry)    # YOUR code runs the tool
            messages.append({"role": "tool",
                             "tool_call_id": call.id,
                             "content": result})     # feed result back
    return "max steps exceeded"
```

Output:
```
user → model: get_weather(city="Cairo") → execute → result
     → model: "It is 34°C in Cairo."    (final answer)
```

The two non-negotiable details: (1) **you** execute the tool — the model only
requests; (2) results come back as `tool` messages referenced by
`tool_call_id`, so the model knows which call each result answers.

## 3. Validate Before You Execute (The Iron Rule)

The model's tool call is generated text. Parse + validate *before* any side
effect:

```python
from pydantic import BaseModel, Field, ValidationError
import json

class WeatherArgs(BaseModel):
    city: str = Field(min_length=1, max_length=100)

def parse_and_validate(call) -> dict:
    """Parse args JSON and validate against the tool's schema."""
    args = json.loads(call.arguments)                # L3: structured output
    schema = {"get_weather": WeatherArgs}.get(call.function.name)
    if schema is None:
        raise ValueError(f"unknown tool: {call.function.name}")
    return schema.model_validate(args).model_dump()

try:
    args = parse_and_validate(call)
    result = registry[call.function.name](**args)    # execute only now
except (ValidationError, json.JSONDecodeError) as e:
    # return the error to the model as a tool result — it can self-correct
    result = f"ERROR: invalid arguments: {e}"
```

Output:
```
Valid: {"city": "Cairo"} → executed → "34°C"
Invalid: {"city": 123}   → error fed back → model retries with a string
```

**The iron rule:** validation failure returns an *error message to the model*
(which can self-correct — a repair loop, L3) and **never** reaches the
executor.

## 4. Execute Safely: Allowlists, Timeouts, Errors

Tool execution is arbitrary code — treat it as an attack surface:

| Risk | Mitigation |
|---|---|
| Model calls a dangerous tool | **allowlist**: only registered tools execute |
| Tool hangs | timeout per tool call |
| Tool errors | map to clean messages back to the model |
| Args beyond schema | pydantic validation (above) |
| Sensitive tools | auth/approval gates (L19, L24) |

```python
def execute_tool(call, registry: dict, timeout_s: float = 10.0) -> str:
    if call.function.name not in registry:
        return f"ERROR: tool '{call.function.name}' does not exist"
    fn = registry[call.function.name]
    try:
        args = parse_and_validate(call)
        result = fn(**args)                 # allowlisted, validated
        return str(result)[:2000]           # bound the context back
    except ValidationError as e:
        return f"ERROR: invalid arguments: {e}"
    except Exception as e:                  # tool raised
        return f"ERROR: tool failed: {e}"
```

Output:
```
"ERROR: invalid arguments: ..."  — the model self-corrects; nothing crashed.
```

Bounding the result length matters: a tool returning 100k chars blows the
context window (L1) and the cost (L18).

## 5. Prompt-Based Tool Calling (Local Models)

Not every model has native tool calling. The fallback: prompt the model to
emit JSON that *looks like* a tool call (L3 structured output), parse it, and
run the same loop:

```python
TOOL_PROMPT = """You are an assistant with tools. To call a tool, output
exactly: {"tool": "get_weather", "args": {"city": "Cairo"}}. Otherwise output
plain text. Tools: {tool_descriptions}. User: {input}"""

# response → parse JSON → if "tool" key present → execute → loop
```

Output:
```
Local model emits the JSON tool call; same execution loop, no native support.
```

Same validation and safety rules apply — prompt-based calling is just a
less-guaranteed parsing path (L3's rungs matter even more).

## Every Use Case

- **Live-data grounding**: weather, prices, stock — tools fetch fresh data.
- **Database querying**: natural language → SQL tool (validated, read-only first).
- **Document search**: tools wrapping the RAG index (L9-L12).
- **Actions**: booking, ordering, scheduling — with approval gates (L19).
- **Code execution**: sandboxed run for calculations/analysis.
- **API orchestration**: composing multiple internal APIs.
- **Agent scaffolding**: the primitive that L14 agents loop on.
- **Internal copilots**: tools for the company's systems.

## Real-World Use Cases for AI Engineers

- **Customer-support copilot**: the assistant calls `search_docs` (RAG tool),
  `lookup_order` (DB tool), and `issue_refund` (approval-gated action). A
  malformed `issue_refund` args call is caught by pydantic and fed back as an
  error — the refund API is *never* called with garbage. The tool allowlist is
  the security boundary.
- **Financial analyst assistant**: the model calls a read-only SQL tool to
  answer "Q2 revenue by region?" The tool is allowlisted, read-only, and
  timeout-bounded; the answer's numbers are grounded in a live query, not
  hallucinated.
- **E-commerce**: "find me a gift under $50" → the model calls the product
  search tool with `{query, max_price}`, gets results, and answers — tool
  calling turns the LLM into a shopping agent's brain.
- **Operations copilot**: an SRE assistant calls `get_deploy_status` and
  `rollback_service` (the latter behind an approval gate — L19/L24). The
  allowlist + approval is what makes the copilot safe enough to run.
- **RAG system upgrade**: adding `search_docs` as a *tool* (instead of
  implicit retrieval) gives the model control over *when* to retrieve — the
  agentic retrieval pattern of L14.

## Common Mistakes to Avoid

### Mistake 1: Executing the model's call without validation
The model's args are text; garbage args reach side effects. Validate first.

### Mistake 2: No allowlist
"Run any function the model names" is code execution by prompt. Allowlist.

### Mistake 3: No loop bound
An agent that loops forever burns tokens and latency. Bound `MAX_STEPS`.

### Mistake 4: Unbounded tool results
Huge results blow the context window and cost. Bound + truncate.

### Mistake 5: Losing the tool_call_id contract
Results must reference the call or the model can't map them. Follow the
message contract.

### Mistake 6: No timeout on tools
A hung DB query blocks the whole loop. Timeout every tool.

### Mistake 7: Vague tool descriptions
The model selects tools by description; vague = wrong tool. Write precise
descriptions.

## Best Practices

1. Describe tools precisely — the model chooses by description
2. Validate args with pydantic before any execution
3. Return validation errors to the model (self-correction loop)
4. Allowlist tools; timeout every call; bound result length
5. Bound the loop (MAX_STEPS) — no infinite agent loops
6. Follow the tool_call_id message contract exactly
7. Gate sensitive tools behind approval (L19, L24)
8. Log every tool call (name, args, result, latency) — L17
9. Test tools with mock LLM outputs (malformed args) in CI
10. Prefer native tool calling; prompt-based as fallback with stricter parsing

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| One loop step | 1 LLM call | O(tokens) | fewer steps via better prompts |
| Tool execution | tool-dependent | O(result) | bound result length |
| Validation | µs | O(1) | pydantic |
| Prompt-based calling | +parsing risk | — | native tool calling if available |

## AI Engineering Relevance

**Where this shows up:** every agent (L14), every tool-using copilot, every
system where the model must act on live data. Tool calling is the primitive
that turns language into action — and the validation discipline is what keeps
that action safe.

| Concept here | Used for |
|---|---|
| Tool schemas | model-readable capabilities |
| Validate-before-execute | no garbage side effects |
| Result feedback | grounded, self-correcting loops |
| Allowlist + timeout | the security boundary |

**Scale note:** at 10M tool calls/day, validation + allowlisting + logging are
the *reliability* and *audit* backbone; a 0.1% unvalidated-call rate is 10k
potentially dangerous executions. The iron rule scales.

## Practice Exercises

### Exercise 1: Parse and Validate (Easy)
Implement `parse_and_validate(call)` for `get_weather`; test valid args,
string-where-int (reject), and unknown-tool cases.

### Exercise 2: The Loop (Medium)
Implement `run_with_tools` with a mock LLM that emits one tool call then an
answer; assert the tool executed once and the final answer reflects the
result.

### Exercise 3: Self-Correction (Medium)
Simulate: model emits invalid args → error fed back → model retries with
valid args; assert the second attempt succeeds and no side effect happened on
the first.

### Exercise 4: Safe Executor (Hard)
Build `execute_tool` with allowlist, validation, timeout, and result bounding;
test unknown tool, invalid args, tool raising, and oversized-result cases —
assert clean error messages and no crashes.

## Summary

| Concept | Description |
|---|---|
| Tool schema | model-readable capability |
| The loop | request → validate → execute → feed back |
| Iron rule | validate before any side effect |
| Safety | allowlist, timeout, bound, approval |
| Self-correction | errors fed back → model retries |

Tool calling is the bridge from language to action: the model requests, your
code validates and executes, and results flow back into the loop. It is the
primitive of every agent and every tool-using copilot — and its reliability
rests on the AI engineer's discipline: schema-first, validate-always, bound-
everything.

## Quick Reference

| Task | Idiom |
|---|---|
| Define tool | name + description + JSON-schema args |
| Validate args | pydantic model per tool |
| Execute | allowlist + timeout + bounded result |
| Feed back | `{"role": "tool", "tool_call_id": ..., "content": ...}` |
| Bound loop | MAX_STEPS |

## Next Steps

Next: **[14 Agent Patterns](14-agent-patterns-lecture.md)** — the loops and
architectures built on tool calling.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/guides/function-calling,
https://docs.anthropic.com/en/docs/build-with-claude/tool-use
