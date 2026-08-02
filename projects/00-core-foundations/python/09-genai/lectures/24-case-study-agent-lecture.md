# GenAI — 24: Case Study — Production Agent

## Topic Overview

This lecture is the second capstone: a complete, production-grade **agent
system** — a tool-using, multi-step assistant that actually *does* things —
integrating Lectures 13–22 on the Phase 8 assembly line. Where the RAG service
(L23) answers questions, the agent *acts*: it plans, calls tools (L13), loops
(ReAct/plan-execute, L14), persists state (L16), is budgeted (L14/L18),
guarded (L19), traced (L17), and gated by evaluation (L20). This is the
hardest system in the phase — and the most valuable.

The scenario: **"TicketSolver"** — a support agent that resolves customer
tickets end to end: it reads the ticket, searches docs (RAG tool), looks up
the account (DB tool), and — when policy permits and a human approves —
executes actions (issue refund, change plan, escalate). Every step is
validated, budgeted, traced, and approved where it matters.

The master lesson: a production agent is a **bounded, auditable, measurable
process** — not a "smart loop." The engineering is in the guardrails: budgets
(L14), tool validation (L13), action approval (L19/L24), state persistence
(L16), traces (L17), and the eval that gates every change (L20).

## Learning Objectives

By the end of this lecture, you will be able to:
1. Design a production agent architecture (tools, loop, state, gates)
2. Wire the tool registry with schemas, validation, and allowlists (L13)
3. Implement the bounded loop (ReAct/plan-execute) with budgets (L14)
4. Add action approval (read vs write, human-in-the-loop)
5. Persist state and resume after failures (L16)
6. Trace the full run for audit and debugging (L17)
7. Eval the agent (completion + efficiency) and gate changes (L20)

## Prerequisites

| Need | Where |
|---|---|
| Agent patterns | `09-genai/lectures/14-agent-patterns-lecture.md` |
| Tool calling | `09-genai/lectures/13-tool-calling-lecture.md` |
| Guardrails | `09-genai/lectures/19-guardrails-and-safety-lecture.md` |
| Evaluation | `09-genai/lectures/20-evaluation-frameworks-lecture.md` |
| Phase 8 serving/CI | `08-mlops/lectures/07,12` |

## 1. The Architecture

```
[ticket arrives] → [input gate L19] → [agent loop L14]
                                        │
                    ┌───────────────────┼────────────────────┐
                    ▼                   ▼                    ▼
               [RAG tool: search_docs]  [DB tool: lookup]   [action tools]
                    │                   │                  (issue_refund,
                    │                   │                   change_plan)
                    └──── [L13: schemas + validation + allowlist] ────┘
                                        │
                    [budgets L14/L18] ←─┘ → [approval gate L19 for writes]
                                        │
                    [state persistence L16] → [trace L17] → [eval L20 gate]
                                        ▼
                              [resolution + summary]
```

Every arrow is a Lecture; the system is the integration.

## 2. The Tool Registry (L13)

The agent's capabilities are a registered, schema'd, allowlisted set:

```python
TOOL_REGISTRY = {
    "search_docs": {
        "fn": rag_search, "level": "read",
        "schema": SearchArgs, "desc": "Search the knowledge base."},
    "lookup_account": {
        "fn": lookup_account, "level": "read",
        "schema": AccountArgs, "desc": "Look up an account by id."},
    "issue_refund": {
        "fn": issue_refund, "level": "write",
        "schema": RefundArgs, "desc": "Issue a refund (requires approval)."},
    "escalate": {
        "fn": create_escalation, "level": "write",
        "schema": EscalationArgs, "desc": "Escalate to a human agent."},
}
```

Output:
```
4 tools: 2 read (auto), 2 write (approval-gated). Unknown tools don't exist.
```

**The registry is the security boundary** (L13/L19): the agent can only
request what's registered, args are schema-validated before execution, and
write actions wait for human approval.

## 3. The Bounded Loop (L14)

The agent runs a ReAct loop (or plan-execute for predictable tickets) with
hard budgets:

```python
def run_agent(ticket: Ticket, *, llm_client, max_steps=8, max_tokens=20_000,
              max_cost=0.50) -> AgentResult:
    trace = [{"role": "user", "content": ticket.render()}]
    budget = AgentBudget(max_steps, max_tokens, max_cost)     # L14
    for _ in range(max_steps):
        resp = llm_client.complete(trace)
        trace.append(resp.message)
        if not resp.tool_calls:
            return AgentResult(resolved=resp.content, trace=trace)
        for call in resp.tool_calls:
            if not budget.ok(resp.usage):          # L14/L18: budgets
                return AgentResult(resolved="budget exceeded; escalated",
                                   trace=trace)
            decision = authorize(call, actor="support_bot")   # L19 gate
            if decision == "approve":
                result = execute_tool(call, TOOL_REGISTRY)    # L13
            elif decision == "pending":
                result = "waiting for human approval"         # L24 pattern
            else:
                result = f"denied: {decision}"
            trace.append({"role": "tool", "tool_call_id": call.id,
                          "content": result})
    return AgentResult(resolved="max steps; escalated to human", trace=trace)
```

Output:
```
[0] search_docs → "Refund policy §3..."
[1] lookup_account → "eligible"
[2] issue_refund → "waiting for human approval" → approved → "refund issued"
[3] (final) "Resolved: refund of $49 issued. Reference R-2049."
```

## 4. The Approval Gate (L19/L24)

Write actions are the safety-critical boundary. The approval flow:

```python
def authorize(call, *, actor: str) -> str:
    """read → approve; write → human approval; unknown → deny."""
    level = TOOL_REGISTRY[call.function.name]["level"]
    if level == "read":
        return "approve"
    if level == "write":
        return "pending"          # queued for human approval (async)
    return "deny"                 # unknown tool — default deny

def approve_action(action_id: str, approver: str, decision: bool) -> None:
    # recorded in the trace + approval log (audit evidence)
    log_approval(action_id, approver, decision)
```

Output:
```
read tools auto-run; write tools pause for a human; every approval is logged.
```

**Why this matters (real-world):** the human in the loop is not a friction —
it is the control that lets the agent *exist* in production with write
capability. A support agent that issues refunds with human approval is
shippable; one that doesn't is a liability.

## 5. State, Resume, and Failure Handling (L16)

Long-running agents persist their trace; a crash resumes instead of
restarting:

```python
def run_with_resume(ticket_id: str, ticket: Ticket, *, llm_client):
    saved = load_state(ticket_id)          # L16: persisted trace
    trace = saved or [{"role": "user", "content": ticket.render()}]
    # ... loop continues from the persisted trace ...
    save_state(ticket_id, trace)           # persist every step
```

Output:
```
Agent crashed at step 4 → resumed from the persisted trace → completed.
```

Tool failures (L13) are fed back as tool results (self-correction); a
persistent failure path *escalates* rather than looping forever.

## 6. Observability and Audit (L17)

The trace IS the audit trail: every tool call, approval, token, and cost —
a ticket resolution can be reconstructed end to end:

```python
def audit_ticket(ticket_id: str) -> dict:
    trace = load_state(ticket_id)                     # L16
    logs = load_trace_log(ticket_id)                  # L17
    return {"ticket": ticket_id, "steps": len(trace),
            "tool_calls": [t for t in logs if t["kind"] == "tool"],
            "approvals": [t for t in logs if t["kind"] == "approval"],
            "total_cost_usd": sum(t["cost_usd"] for t in logs)}
```

Output:
```
{'ticket': 'T-1042', 'steps': 6, 'tool_calls': [...], 'approvals': [...],
 'total_cost_usd': 0.18}   — the full story of one resolution.
```

## 7. Evaluation and CI Gate (L20)

The agent is a stochastic process — it ships only with measured completion
and efficiency:

```python
def agent_release_gate(candidate_agent, suite) -> tuple[bool, dict]:
    report = run_suite(suite, candidate_agent, AGENT_EVALUATORS)   # L20
    ok = (report.scores["completion"] >= 0.80 and          # resolves correctly
          report.scores["efficiency"] >= BASELINE["efficiency"] - 0.1)
    return ok, report.scores
```

Output:
```
(True, {'completion': 0.87, 'efficiency': 0.82, 'avg_steps': 4.3})
— the agent's scoreboard; regressions block merges (L12).
```

## Every Use Case

- **Support resolution**: the TicketSolver shape — read docs, check account, act.
- **Operations copilots**: diagnose + fix (with approval) for infra.
- **Procurement/fulfillment workflows**: state-machine agents (L14).
- **Research agents**: gather + synthesize with tool-grounded facts.
- **Code agents**: plan → edit → test loops (L14 reflection).
- **Sales/CRM assistants**: lookups + follow-up actions.
- **Any "reads and acts" system**: the pattern is universal.

## Real-World Use Cases for AI Engineers

- **SaaS support (TicketSolver)**: 40% of tickets resolve end to end with
  human-approved refunds; the approval log + trace is the finance audit trail
  for every refund issued. The completion eval (L20) gates each prompt/tool
  change.
- **Fintech operations**: an agent that investigates failed transfers
  (read-only tools) and *proposes* fixes for human approval — the
  write-default-approval rule is the compliance story.
- **Infrastructure ops**: an incident agent reads deploy status, queries
  logs, and proposes rollbacks; the rollback tool is approval-gated, and the
  trace is the postmortem's raw material.
- **Healthcare admin**: an agent gathers patient-doc info (read-only) and
  drafts forms; no write actions exist — the tool registry *is* the safety
  design.
- **E-commerce**: a shopping agent searches products and — with approval —
  places an order; the budget control caps its spend, the trace records every
  step.

## Common Mistakes to Avoid

### Mistake 1: Write tools without approval
An auto-refunding agent is a financial incident waiting to happen. Gate writes.

### Mistake 2: Unbounded loops
No budgets = runaway cost on a tricky ticket. Budget steps/tokens/cost (L14/L18).

### Mistake 3: No tool validation
Args reaching tools unvalidated (L13 iron rule) — validate in every loop.

### Mistake 4: No state persistence
A crashed agent restarts from zero, wasting work and money. Persist (L16).

### Mistake 5: No trace/audit
A ticket resolution with no trace is un-debuggable and un-auditable. Trace all.

### Mistake 6: No evaluation
"Agents are new, so we ship and see" — completion/efficiency eval (L20)
first. Always.

### Mistake 7: Unknown tools allowed
Unknown tool → deny (L19). The registry is the boundary.

## Best Practices

1. Registry = capabilities: schemas, levels, allowlist (L13)
2. Read auto-runs; write requires human approval; unknown denies (L19)
3. Budget steps, tokens, and cost on every run (L14/L18)
4. Persist state every step; resume from failure (L16)
5. Trace everything: calls, approvals, tokens, cost (L17)
6. Feed tool errors back to the model (self-correction) but escalate on persistence
7. Eval completion + efficiency on a frozen suite; gate changes (L20/L12)
8. Escalate instead of looping forever
9. Keep the tool registry narrow — capability is controlled surface
10. Test with mock LLMs and mock tools in CI (deterministic loop tests)

## Complexity and Cost

| Component | Cost | Levers |
|---|---|---|
| Loop calls | 2-8 × generation | better prompts, plan-execute for predictability |
| Tool execution | per tool | validated, bounded results (L13) |
| Approvals | human latency | only for write actions |
| Traces + state | storage | retention policy (L17) |
| Eval suite | per release | subset in CI, full nightly |

## AI Engineering Relevance

**Where this shows up:** the highest-value GenAI systems — ones that act.
TicketSolver is the template: a bounded, auditable, measured agent — tools
registered and gated, loop budgeted, state persisted, traces everywhere, and
an eval that decides what ships.

| Concept here | Used for |
|---|---|
| Tool registry + gates | controlled capability |
| Bounded loop | no runaway agents |
| Approval flow | safe write actions |
| Trace + audit | reconstructable resolutions |
| Eval gates | measured agent quality |

**Scale note:** at 10k tickets/day, budgets and traces are the cost-control
and audit backbone; the completion eval + approval logs are what the finance
and compliance teams read. The agent is only as production-ready as its
guardrails — which is to say, completely.

## Practice Exercises

### Exercise 1: Registry + Auth (Easy)
Build `authorize(call, actor)` over a small registry; assert read auto-
approves, write pends, unknown denies.

### Exercise 2: Bounded Loop (Medium)
Implement `run_agent` with a mock LLM that would loop forever; assert the
budget stops it and the result says "escalated."

### Exercise 3: Resume (Medium)
Implement `run_with_resume` with a mock crash at step 3; assert the resumed
run completes from the persisted trace (no repeated steps 1-2 work).

### Exercise 4: Audit + Gate (Hard)
Build `audit_ticket` from a mock trace log, and `agent_release_gate` over a
10-task suite; assert: the audit reports calls/approvals/cost, and a
candidate with completion < 0.80 is blocked.

## Summary

| Concept | Description |
|---|---|
| Tool registry | controlled, gated capabilities |
| Bounded loop | budgets stop runaway agents |
| Approval gate | writes need humans |
| State + resume | crash-safe execution |
| Trace + audit | reconstructable resolutions |
| Eval gate | measured completion/efficiency |

TicketSolver is the production agent template: a bounded, auditable, measured
process — tools registered and gated (L13/L19), loop budgeted (L14/L18),
state persisted (L16), every step traced (L17), and every change gated by
evaluation (L20). The "smart loop" is a demo; the *system* is the product.

## Quick Reference

| Task | Idiom |
|---|---|
| Register tool | schema + level + fn in the registry |
| Gate action | read auto, write approve, unknown deny |
| Bound loop | AgentBudget(steps, tokens, cost) |
| Persist | save/load trace per ticket |
| Audit | trace + approval log per ticket |
| Ship | completion + efficiency eval gate (L20) |

## Next Steps

Next: **[25 Case Study: Extraction](25-case-study-extraction-lecture.md)** — the
production structured-extraction pipeline.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/guides/function-calling
