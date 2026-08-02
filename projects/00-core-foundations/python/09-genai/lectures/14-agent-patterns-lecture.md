# GenAI — 14: Agent Patterns

## Topic Overview

An agent is a loop: the LLM **observes** (reads context/tool results),
**decides** (what to do next), and **acts** (calls tools, L13) — repeating
until the task is done. Where a single LLM call is a function, an agent is a
*process*: it can plan, gather information across steps, use tools, and
recover from failures. This lecture covers the canonical agent architectures
and the engineering that makes them reliable — because the difference between
a demo agent and a production agent is entirely in the loop control: bounds,
state, error recovery, and evaluation.

The canonical patterns:

| Pattern | Shape | Use when |
|---|---|---|
| **ReAct** | Reason → Act → Observe loop | general problem solving |
| **Plan-and-Execute** | plan first, then execute steps | multi-step tasks, predictability |
| **Reflection** | generate → critique → revise | quality-critical outputs |
| **Router/Orchestrator** | a planner dispatches sub-agents | complex compositions (L15) |
| **State machine** | explicit states + transitions | regulated, auditable workflows |

Why this matters: agents are where GenAI's value gets *operational* — and
where unreliability gets expensive. Every production agent needs: a bounded
loop, a persisted state, tool validation (L13), error recovery, and
evaluation (L20). This lecture gives you the patterns and the guardrails that
make agents shippable.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Implement the ReAct loop (reason → act → observe)
2. Implement plan-and-execute (decompose → execute steps)
3. Implement reflection (generate → critique → revise)
4. Choose the right pattern for the task and reliability needs
5. Bound and control the loop (max steps, budgets, cancellation)
6. Persist agent state and recover from failures
7. Evaluate agents (task completion, step efficiency — L20)

## Prerequisites

| Need | Where |
|---|---|
| Tool calling | `09-genai/lectures/13-tool-calling-lecture.md` |
| Structured output | `09-genai/lectures/03-structured-output-lecture.md` |
| Prompt engineering | `09-genai/lectures/04-prompt-engineering-lecture.md` |
| Evaluation (preview) | `09-genai/lectures/20-evaluation-frameworks-lecture.md` |

## 1. ReAct: Reason → Act → Observe

The foundational pattern. Each loop step: the model reasons about what to do,
calls a tool (or answers), and observes the result — a text trace of the
whole process:

```python
def react_agent(task: str, llm_client, registry: dict, max_steps: int = 8) -> str:
    trace = [{"role": "user", "content": task}]
    for step in range(max_steps):
        resp = llm_client.complete(trace)
        trace.append(resp.message)
        if not resp.tool_calls:
            return resp.content                      # task complete
        for call in resp.tool_calls:
            result = execute_tool(call, registry)    # L13 (validated)
            trace.append({"role": "tool", "tool_call_id": call.id,
                          "content": result})
            print(f"[{step}] {call.function.name} -> {result[:60]}")
    return "ERROR: max steps exceeded"
```

Output:
```
[0] search_docs -> "The refund policy is in section 3..."
[1] lookup_order -> "Order #1042 is eligible"
[2] (final) "Your order qualifies for a refund under section 3."
```

**The trace is the product**: ReAct's chain of tool results is both the
reasoning evidence and the audit trail (L17/L24).

## 2. Plan-and-Execute

Plan first, then execute steps — more predictable than free-form ReAct for
multi-step tasks:

```python
PLAN_PROMPT = """Break this task into 2-5 ordered steps. Output JSON:
{"steps": [{"step": str, "tool": str, "input": {...}}]}. Task: {task}"""

def plan_and_execute(task: str, llm_client, registry: dict) -> str:
    import json
    plan = json.loads(llm_client.complete(PLAN_PROMPT.format(task=task)))
    results = []
    for s in plan["steps"]:
        out = execute_tool({"function": {"name": s["tool"], "arguments":
                             json.dumps(s["input"])}}, registry)
        results.append(f"Step '{s['step']}': {out}")
    return llm_client.complete(
        f"Task: {task}\nStep results:\n" + "\n".join(results) + "\nFinal answer:")
```

Output:
```
Plan: [search product docs, lookup pricing, compose answer]
→ each step executes → final answer synthesizes the step results.
```

**The trade:** plan-and-execute is more predictable and cheaper (fewer
re-decisions), but less adaptive — if step 2 discovers the plan was wrong,
ReAct recovers better. Choose by task predictability.

## 3. Reflection: Generate → Critique → Revise

For quality-critical output (code, writing, analysis), the model critiques its
own draft and revises:

```python
def reflect_generate(task: str, llm_client, rounds: int = 2) -> str:
    draft = llm_client.complete(f"Task: {task}\nProduce the best output.")
    for _ in range(rounds):
        critique = llm_client.complete(
            f"Critique this output for correctness and completeness.\n"
            f"Task: {task}\nOutput: {draft}\nCritique:")
        draft = llm_client.complete(
            f"Revise the output addressing this critique.\n"
            f"Task: {task}\nCritique: {critique}\nRevised output:")
    return draft
```

Output:
```
draft → critique ("missing edge case for empty input") → revised draft
```

**Cost note:** reflection multiplies calls (L18) — it pays only where quality
is worth 2-3x the tokens. Use it for code/legal/analysis, not for every chat
turn.

## 4. State Machines: The Regulated Pattern

For workflows with mandatory steps (order → payment → fulfillment) or audit
requirements, replace free-form loops with an explicit **state machine** —
the agent can only transition to allowed states:

```python
TRANSITIONS = {
    "start": {"collect_order"},
    "collect_order": {"validate", "cancel"},
    "validate": {"payment", "rejected"},
    "payment": {"fulfill", "failed"},
    "fulfill": {"done"},
}

def run_state_machine(task: str, llm_client, registry: dict) -> str:
    state = "start"
    ctx = {}
    while state != "done":
        allowed = TRANSITIONS[state]
        resp = llm_client.complete(
            f"State: {state}. Allowed next: {allowed}. Context: {ctx}. Task: {task}.")
        state = parse_state(resp)              # L3: constrained enum
        if state not in allowed:
            return f"ERROR: illegal transition to {state}"
        ctx[state] = execute_state(state, registry)
    return "workflow complete: " + json.dumps(ctx)
```

Output:
```
start → collect_order → validate → payment → fulfill → done
(illegal transitions rejected; every step recorded)
```

**Why it matters:** the transitions *are* the compliance policy — an agent
cannot skip validation and jump to payment. State machines are the default for
regulated domains (fintech, healthcare, procurement).

## 5. Loop Control: The Production Guardrails

Every production agent needs the same controls:

```python
class AgentBudget:
    def __init__(self, max_steps: int = 10, max_tokens: int = 20_000,
                 max_cost: float = 1.0):
        self.steps = 0
        self.tokens = 0
        self.cost = 0.0
        self.limits = (max_steps, max_tokens, max_cost)

    def ok(self, last_tokens: int, cost_per_token: float) -> bool:
        self.steps += 1
        self.tokens += last_tokens
        self.cost += last_tokens * cost_per_token
        return (self.steps <= self.limits[0] and
                self.tokens <= self.limits[1] and
                self.cost <= self.limits[2])
```

Output:
```
Loop stops when steps, tokens, or cost exceed budget — no runaway agents.
```

Without budgets, an agent is a cost explosion waiting for a tricky task. With
them, it is a bounded, predictable process (L18 discipline).

## 6. State, Persistence, and Recovery

Production agents outlive one process: persist state (the message trace +
step results), and resume from failure. If step 4 of 6 crashes, restarting
from scratch is waste; resuming from the persisted trace is cheap.

```python
import json

def save_state(agent_id: str, trace: list) -> None:
    json.dump(trace, open(f"outputs/agents/{agent_id}.json", "w"))

def load_state(agent_id: str) -> list | None:
    try:
        return json.load(open(f"outputs/agents/{agent_id}.json"))
    except FileNotFoundError:
        return None
```

Output:
```
Agent resumes from its persisted trace after a crash — no lost work.
```

## 7. Evaluating Agents

Agents need their own eval (L20): **task completion** (did it finish
correctly?) and **efficiency** (steps/tokens per task):

```python
def evaluate_agent(agent_fn, tasks: list[dict]) -> dict:
    """tasks: [{"input": ..., "expected": ...}]. Score completion + efficiency."""
    done = sum(1 for t in tasks if agent_fn(t["input"]) == t["expected"])
    return {"completion_rate": round(done / len(tasks), 3),
            "avg_steps": ... }   # from the agent's step counter
```

Output:
```
{'completion_rate': 0.87, 'avg_steps': 4.2}  — the agent's scoreboard (L20).
```

## Every Use Case

- **Research assistants**: ReAct gathering and synthesizing across sources.
- **Data analysis agents**: plan + execute (query, plot, summarize).
- **Support resolution**: tool-using agents that actually resolve issues.
- **Code agents**: reflection (write → test → fix) is the dominant pattern.
- **Procurement/fulfillment**: state-machine workflows.
- **Report generation**: plan-and-execute across systems.
- **RAG + tools hybrid**: retrieval as one of several tools (L13).
- **Multi-agent systems**: orchestrator + workers (L15).

## Real-World Use Cases for AI Engineers

- **Support resolution agent (SaaS)**: ReAct with `search_docs`,
  `lookup_account`, and `issue_refund` tools, bounded at 8 steps with a cost
  budget. The trace is the ticket audit — the agent resolves 40% of tickets
  end-to-end, and every resolution is reconstructable from the trace.
- **Code agent**: reflection (write → run tests → fix) turns a one-shot
  codegen into a "keep trying until tests pass" loop — completion rate on
  the eval (L20) is the gate for shipping the capability.
- **Fintech onboarding**: a state machine enforces
  identity-verify → risk-check → account-open; the transitions are the
  compliance policy, and the agent *cannot* skip a step. The state log is the
  regulatory record.
- **Research analyst**: plan-and-execute (gather market data → compute → draft
  → cite) produces a report with every number traceable to a tool result —
  grounded, not hallucinated.
- **Operations**: an incident-response agent uses ReAct to check deploy
  status, query logs, and — with approval gates (L19/L24) — roll back. The
  budget control means a confused agent cannot burn the whole incident budget.

## Common Mistakes to Avoid

### Mistake 1: Unbounded loops
No MAX_STEPS/token/cost budget = runaway cost. Budget everything.

### Mistake 2: No validation of tool calls
The L13 iron rule applies in every loop iteration.

### Mistake 3: Free-form loops for regulated workflows
Where compliance matters, a state machine beats a free-form agent.

### Mistake 4: No state persistence
Crashed agents lose work and cost money to restart. Persist the trace.

### Mistake 5: No evaluation
Agents are stochastic processes — ship only measured completion rates (L20).

### Mistake 6: Reflection everywhere
Reflection multiplies cost 2-3x. Use it where quality is worth it.

### Mistake 7: Ignoring the trace
The trace is the audit trail and the debugger. Log it (L17).

## Best Practices

1. Choose the pattern by task: ReAct (adaptive), plan-execute (predictable),
   reflection (quality), state machine (regulated)
2. Budget steps, tokens, and cost on every agent
3. Validate every tool call (L13) in every loop
4. Persist state; resume from failure
5. Evaluate completion rate + efficiency (L20); gate changes on it
6. Log the full trace (L17) — it's the audit trail
7. Use structured output for plan/state parsing (L3)
8. Gate sensitive actions behind approval (L19, L24)
9. Start with the simplest pattern that works; add complexity when measured
10. Test with mock LLMs in CI (deterministic loop tests)

## Complexity and Cost

| Pattern | Calls per task | Cost multiplier | When to use |
|---|---|---|---|
| Single call | 1 | 1x | simple tasks |
| ReAct | 2-8+ | 2-8x | adaptive problem solving |
| Plan-and-execute | plan + steps | 1.5-3x | predictable multi-step |
| Reflection | 3-5x | 3-5x | quality-critical output |
| State machine | per state | 1.5-4x | regulated workflows |

The pattern choice *is* a cost decision (L18) — measured against completion
rate (L20).

## AI Engineering Relevance

**Where this shows up:** every agentic feature — research, support, code,
operations, workflow automation. The patterns are the architecture; the
guardrails (budgets, validation, state, eval) are what make agents shippable.

| Concept here | Used for |
|---|---|
| ReAct / plan-execute | the loops that act |
| Reflection | quality-critical output |
| State machine | regulated workflows |
| Budgets + persistence + eval | production guardrails |

**Scale note:** at 1M agent runs/day, a 1-step saving per run is real
latency + cost; budgets are what keep a confused agent from becoming a cost
incident. The trace at scale is a monitoring stream (L17).

## Practice Exercises

### Exercise 1: ReAct Loop (Easy)
Implement `react_agent` with a mock LLM + two mock tools; assert it stops when
the model answers without a tool call.

### Exercise 2: Budget Control (Medium)
Implement `AgentBudget` and assert it halts on step, token, and cost limits —
each limit independently.

### Exercise 3: State Machine (Medium)
Implement the order-flow state machine; assert illegal transitions are
rejected and the workflow completes in the correct order.

### Exercise 4: Agent Eval (Hard)
Build `evaluate_agent` over 20 mock tasks (completion + efficiency) and use
it to compare two agent configs (e.g. max_steps 8 vs 3) — assert the report
drives the config choice.

## Summary

| Concept | Description |
|---|---|
| ReAct | reason → act → observe loop |
| Plan-and-execute | decompose then execute |
| Reflection | generate → critique → revise |
| State machine | regulated, auditable workflows |
| Guardrails | budgets, validation, persistence, eval |

Agents turn LLMs from functions into processes — and the patterns (ReAct,
plan-execute, reflection, state machines) plus the guardrails (budgets,
validation, persistence, evaluation) are what make those processes reliable
enough for production. Choose the simplest pattern the task allows; measure
it; guard it.

## Quick Reference

| Task | Idiom |
|---|---|
| Adaptive loop | ReAct: reason → tool → observe |
| Predictable | plan JSON → execute steps |
| Quality | generate → critique → revise |
| Regulated | explicit state transitions |
| Safety | budget steps/tokens/cost + validate tools |

## Next Steps

Next: **[15 Multi-Agent](15-multi-agent-lecture.md)** — orchestrating multiple
specialized agents into one system.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://www.anthropic.com/research/building-effective-agents,
https://python.langchain.com/docs/concepts/agents/
