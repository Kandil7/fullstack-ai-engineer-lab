# Case Study: Agent — Glossary 24

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Agent Anatomy | Design | Prompt + tools + loop + budgets |
| Budget | Control | Caps on turns, calls, tokens |
| Executor | Tools | The safe code running a tool call |
| Guardrail | Safety | Checks on agent input/output |
| Loop | Control | Reason → call → observe → repeat |
| Tool Set | Design | The declared capabilities of an agent |
| Trace | Observability | A log of every agent step |
| Termination | Control | The check that ends the loop |

## Detailed Definitions
### Agent Anatomy
**Definition**: The four parts of an agent: prompt, tools, loop, budgets.
**Related**: Tool Set

### Budget
**Definition**: A hard cap (turns, calls, tokens) protecting cost and
liveness.
**Related**: Termination

### Executor
**Definition**: The validated code that safely runs a tool call.
**Related**: Tool Set

### Guardrail
**Definition**: A check applied to inputs and outputs around the loop.
**Related**: Trace

### Loop
**Definition**: The repeated reason-call-observe cycle.
**Related**: Termination

### Tool Set
**Definition**: The minimal set of schemas + executors exposed to the agent.
**Related**: Executor

### Trace
**Definition**: The step-by-step record enabling debugging and audit.
**Related**: Guardrail

### Termination
**Definition**: The condition or budget that ends the loop.
**Related**: Loop

## Key Concepts Summary
### The Rules
- Minimal tool sets
- Hard budgets
- Full traces
- Guard both sides

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Loop — ___
2. Budget — ___
3. Executor — ___
4. Trace — ___
5. Tool set — ___

**Answers:** 1-d, 2-b, 3-e, 4-c, 5-a where a=declared capabilities, b=hard cap,
c=step record, d=reason-act cycle, e=safe runner.
