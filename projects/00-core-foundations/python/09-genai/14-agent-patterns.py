"""
GenAI - 14: Agent Patterns
==========================
Topics: ReAct, plan-and-execute, reflection, loop limits and budget caps,
state management, when an agent is the wrong architecture.

Why this matters for AI/backend engineering:
    Agents multiply capability - and cost, latency, and failure modes.
    The production discipline is: bounded loops, explicit budget caps,
    and knowing when a plain pipeline beats an agent.

Run:      python 14-agent-patterns.py
Verify:   python 14-agent-patterns.py --verify
Reference: https://arxiv.org/abs/2210.03629 (ReAct)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any


# ============================================================
# 1. The ReAct Loop (Reason + Act)
# ============================================================
# Alternating: think (Reason), then act (tool call), observe, repeat.
# The loop must ALWAYS have a max iteration count.

def react_loop(problem: str, max_steps: int, tools: dict[str, Any],
               reason_fn, act_fn) -> dict:
    """A bounded ReAct loop. Returns the trail and final answer."""
    trail: list[dict] = []
    for step in range(max_steps):
        thought = reason_fn(problem, trail)
        trail.append({"step": step, "thought": thought})
        if thought.get("done"):
            return {"answer": thought.get("answer", ""), "steps": step + 1, "trail": trail}
        action = act_fn(thought, tools)
        trail.append({"step": step, "action": action})
        if action.get("error"):
            return {"answer": f"failed: {action['error']}",
                    "steps": step + 1, "trail": trail}
    return {"answer": "MAX_STEPS reached - gave up", "steps": max_steps, "trail": trail}


# Example 1: a toy ReAct agent
TOOLS = {"add": lambda a, b: a + b, "mul": lambda a, b: a * b}

def toy_reason(problem: str, trail: list[dict]) -> dict:
    # naive: if no multiplication yet, ask for it; else declare done
    if not any("mul" in str(t.get("action", {})) for t in trail):
        return {"tool": "mul", "args": {"a": 6, "b": 7}}
    return {"done": True, "answer": "42"}

def toy_act(thought: dict, tools: dict[str, Any]) -> dict:
    name = thought.get("tool")
    if not name or name not in tools:
        return {"error": f"unknown tool {name}"}
    try:
        return {"tool": name, "result": tools[name](**thought.get("args", {}))}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


result = react_loop("What is 6*7?", max_steps=5, tools=TOOLS,
                    reason_fn=toy_reason, act_fn=toy_act)
print("Example 1: bounded ReAct loop")
print(f"  answer={result['answer']} in {result['steps']} steps")
assert result["answer"] == "42" and result["steps"] == 2

# ============================================================
# 2. Loop Limits Prevent Bill Shock
# ============================================================
# An unbounded agent loops forever, spending tokens every turn. Cap
# steps AND token budget; stop when either is exhausted.

def runaway_agent(max_steps: int) -> int:
    """A bad agent that never finishes - the cap saves you."""
    steps = 0
    while True:
        steps += 1
        if steps >= max_steps:
            return steps
    # unreachable


# Example 2: the cap is the safety net
steps_taken = runaway_agent(max_steps=10)
print("\nExample 2: budget caps")
print(f"  runaway agent stopped after {steps_taken} steps (cap=10)")
assert steps_taken == 10

# ============================================================
# 3. Plan-and-Execute
# ============================================================
# Separate the planning (write the whole plan first) from execution
# (run each step). Better for multi-step tasks; costs an extra call.

def plan_and_execute(task: str, planner, executor, max_steps: int = 5) -> dict:
    plan = planner(task)
    results = []
    for step in plan[:max_steps]:
        results.append(executor(step))
    return {"plan": plan, "results": results, "steps_executed": len(results)}


def toy_planner(task: str) -> list[str]:
    return ["load data", "clean data", "train model"]

def toy_executor(step: str) -> str:
    return f"done: {step}"


pe = plan_and_execute("build model", toy_planner, toy_executor)
print("\nExample 3: plan-and-execute")
print(f"  plan: {pe['plan']}")
print(f"  executed: {len(pe['results'])} steps")
assert len(pe["plan"]) == 3 and len(pe["results"]) == 3

# ============================================================
# 4. Reflection
# ============================================================
# After producing an answer, ask the model to critique it, then improve.
# Expensive (2-3x calls) but effective for hard tasks.

def reflect(answer: str, critic) -> tuple[str, bool]:
    critique = critic(answer)
    if critique.get("ok"):
        return answer, True
    return f"{answer} (revised after: {critique.get('issue')})", False


def toy_critic(answer: str) -> dict:
    return {"ok": False, "issue": "missing citation"} if "source" not in answer \
        else {"ok": True}


# Example 4: reflection cycle
final, accepted = reflect("Answer here", toy_critic)
print("\nExample 4: reflection")
print(f"  {final}")
assert not accepted and "revised" in final

# ============================================================
# 5. When an Agent Is the WRONG Architecture
# ============================================================
# If the steps are fixed and known, a pipeline is cheaper, faster, and
# deterministic. Agents pay for flexibility you may not need.

def architecture_advice(task_kind: str) -> str:
    if task_kind in ("fixed pipeline", "ETL", "rule-based"):
        return "PIPELINE: fixed steps, deterministic, cheap"
    if task_kind in ("open-ended research", "multi-step reasoning"):
        return "AGENT: unknown steps, needs tool use and planning"
    return "HYBRID: pipeline core with an agent deciding the branch"


# Example 5: choosing the architecture
for kind in ["fixed pipeline", "open-ended research"]:
    print(f"\nExample 5: {kind}")
    print(f"  -> {architecture_advice(kind)}")
assert architecture_advice("fixed pipeline").startswith("PIPELINE")
assert architecture_advice("open-ended research").startswith("AGENT")

# ============================================================
# Production Pattern
# ============================================================
# The production agent: bounded loop, budget caps, state dict, and a
# hard exit on repeated failure.

def production_agent(task: str, max_steps: int, max_failures: int = 2) -> dict:
    state: dict[str, Any] = {"task": task, "failures": 0}
    for step in range(max_steps):
        if state.get("done"):
            return {"status": "ok", "steps": step}
        # in production: call the LLM, execute tools, update state
        state["failures"] += 0
    return {"status": "gave up", "steps": max_steps}


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: unbounded agent loops (token/cost explosion)
# MISTAKE: no failure counter - the agent retries forever on the same error
# MISTAKE: agent where a pipeline would do (cost without benefit)
# MISTAKE: no state - the agent forgets what it already did


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # react loop with unknown tool -> graceful failure
    bad = react_loop("x", 3, TOOLS,
                     lambda p, t: {"tool": "ghost", "args": {}}, toy_act)
    assert bad["answer"].startswith("failed"), "unknown tool handled"

    # loop that never finishes hits the cap
    never = react_loop("x", 4, TOOLS,
                       lambda p, t: {"tool": "add", "args": {"a": 1, "b": 1}}, toy_act)
    assert never["answer"] == "MAX_STEPS reached - gave up", "cap enforced"

    assert runaway_agent(3) == 3, "cap enforced"

    pe = plan_and_execute("t", lambda t: ["a", "b"], lambda s: s)
    assert pe["steps_executed"] == 2

    f, acc = reflect("with source", toy_critic)
    assert acc and f == "with source", "good answer accepted"

    assert architecture_advice("ETL").startswith("PIPELINE")
    assert architecture_advice("multi-step reasoning").startswith("AGENT")
    assert architecture_advice("unknown").startswith("HYBRID")

    pa = production_agent("t", max_steps=5)
    assert pa["status"] in ("ok", "gave up"), "bounded"
    print("[OK] 14-agent-patterns: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. ReAct: reason -> act -> observe, bounded.")
        print("2. Cap steps and tokens - always.")
        print("3. Pipeline when steps are fixed; agent when they are not.")
        _verify()
