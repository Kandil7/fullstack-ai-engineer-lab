"""
GenAI - 24: Case Study - Tool-Using Agent
==========================================
Topics: a bounded tool-using agent with budget caps, retries, tracing,
and state - assembled from topics 13-17.

Why this matters for AI/backend engineering:
    The production agent is the boring one: bounded loops, validated
    tool arguments, budget caps, a failure counter, and a trace of
    everything it did. This case study assembles those parts into one
    working system.

Run:      python 24-case-study-agent.py
Verify:   python 24-case-study-agent.py --verify
Reference: https://platform.openai.com/docs/guides/function-calling
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# Components (compact forms of topics 13, 14, 17)
# ============================================================

@dataclass
class Tool:
    name: str
    params: dict[str, str]
    impl: Callable[..., Any]

    def execute(self, args: dict) -> Any:
        for name, expected in self.params.items():
            if name in args and expected == "int" and not isinstance(args[name], int):
                raise ValueError(f"{name} must be int")
        return self.impl(**args)


@dataclass
class AgentTrace:
    request_id: str
    events: list[dict] = field(default_factory=list)
    start_ns: int = 0
    end_ns: int = 0

    def log(self, kind: str, detail: str = "") -> None:
        self.events.append({"kind": kind, "detail": detail, "at_ms": round(
            (time.perf_counter_ns() - self.start_ns) / 1e6, 2)})

    def summary(self) -> dict:
        return {"request_id": self.request_id, "events": len(self.events),
                "duration_ms": round((self.end_ns - self.start_ns) / 1e6, 2)}


# ============================================================
# The Agent
# ============================================================

@dataclass
class Agent:
    tools: dict[str, Tool]
    max_steps: int = 6
    max_failures: int = 2
    token_budget: int = 4000

    def run(self, task: str, planner) -> tuple[str, AgentTrace]:
        """Run the task; planner() returns a list of (tool, args) steps."""
        trace = AgentTrace(request_id=f"agent-{time.time_ns() % 100000}")
        trace.start_ns = time.perf_counter_ns()
        failures = 0
        steps = 0
        tokens_used = 0

        plan = planner(task)
        trace.log("plan", f"{len(plan)} steps")

        for tool_name, args in plan:
            if steps >= self.max_steps:
                trace.log("cap", "max_steps reached")
                break
            if failures >= self.max_failures:
                trace.log("cap", "max_failures reached")
                break

            steps += 1
            tokens_used += 100  # each step costs tokens
            if tokens_used > self.token_budget:
                trace.log("cap", "token budget exceeded")
                break

            if tool_name not in self.tools:
                failures += 1
                trace.log("error", f"unknown tool {tool_name}")
                continue

            tool = self.tools[tool_name]
            try:
                result = tool.execute(args)
                trace.log("tool", f"{tool_name}({args}) -> {result}")
            except (ValueError, KeyError) as e:
                failures += 1
                trace.log("error", f"{tool_name} failed: {e}")

        trace.end_ns = time.perf_counter_ns()
        verdict = "ok" if failures < self.max_failures else "failed"
        return verdict, trace


# ============================================================
# Worked example: a data-analysis agent
# ============================================================
TOOLS = {
    "add": Tool("add", {"a": "int", "b": "int"}, lambda a, b: a + b),
    "mul": Tool("mul", {"a": "int", "b": "int"}, lambda a, b: a * b),
    "sum_list": Tool("sum_list", {"values": "list"}, lambda values: sum(values)),
}


def demo_planner(task: str) -> list[tuple[str, dict]]:
    return [
        ("add", {"a": 1, "b": 2}),
        ("mul", {"a": 3, "b": 4}),
        ("sum_list", {"values": [10, 20, 30]}),
    ]


print("=== Case study: tool-using agent ===")
agent = Agent(TOOLS, max_steps=6, max_failures=2, token_budget=4000)
verdict, trace = agent.run("compute the numbers", demo_planner)
print(f"  verdict: {verdict}")
for event in trace.events:
    print(f"  [{event['at_ms']:>6.1f}ms] {event['kind']}: {event['detail'][:60]}")
print(f"  summary: {trace.summary()}")

# Failing path: an agent that repeatedly hits unknown tools
def broken_planner(task: str) -> list[tuple[str, dict]]:
    return [("ghost_tool", {}), ("ghost_tool", {}), ("ghost_tool", {})]

bad_verdict, bad_trace = agent.run("x", broken_planner)
print(f"\n  broken planner verdict: {bad_verdict}")
print(f"  failures logged: {sum(1 for e in bad_trace.events if e['kind'] == 'error')}")

# ============================================================
# Production Pattern
# ============================================================
# The production agent wraps everything: bounded steps, budget caps,
# retries on transient tool errors, and a trace for every request.

def production_agent_run(agent: Agent, task: str, planner,
                         on_error: Callable[[str], None] | None = None) -> dict:
    verdict, trace = agent.run(task, planner)
    if verdict == "failed" and on_error:
        on_error(trace.summary())
    return {"verdict": verdict, "trace": trace.summary()}


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: unbounded loops / no token budget (bill shock)
# MISTAKE: unvalidated tool arguments (crashes + security)
# MISTAKE: no failure counter - infinite retry loops
# MISTAKE: no trace - impossible to debug what the agent did


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    tools = {"add": Tool("add", {"a": "int", "b": "int"}, lambda a, b: a + b)}
    a = Agent(tools, max_steps=3, max_failures=2, token_budget=1000)

    verdict, trace = a.run("t", lambda t: [("add", {"a": 1, "b": 2})])
    assert verdict == "ok" and trace.events, "agent succeeds"

    # bad args cause a failure but the loop continues
    verdict2, trace2 = a.run("t", lambda t: [("add", {"a": "x", "b": 2}),
                                             ("add", {"a": 1, "b": 2})])
    assert verdict2 == "ok", "recovered after one failure"
    assert any("failed" in e["detail"] for e in trace2.events), "failure logged"

    # unknown tools exhaust max_failures
    verdict3, _ = a.run("t", lambda t: [("nope", {})] * 5)
    assert verdict3 == "failed", "too many failures -> failed"

    # step cap
    a2 = Agent(tools, max_steps=1, max_failures=5, token_budget=1000)
    verdict4, trace4 = a2.run("t", lambda t: [("add", {"a": 1, "b": 1})] * 5)
    assert any(e["kind"] == "cap" and "max_steps" in e["detail"]
               for e in trace4.events), "step cap logged"

    t = Tool("t", {"x": "int"}, lambda x: x)
    try:
        t.execute({"x": "str"})
        raised = False
    except ValueError:
        raised = True
    assert raised, "tool validates args"
    print("[OK] 24-case-study-agent: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Bounded agent: max steps, budget caps, failure counter.")
        print("2. Validate every tool argument before executing.")
        print("3. Trace every action - the audit trail for debugging.")
        _verify()
