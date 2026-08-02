"""
GenAI - 15: Multi-Agent Systems
===============================
Topics: orchestrator/worker, handoffs, shared state, state machines,
cost multiplication risk.

Why this matters for AI/backend engineering:
    One agent can do a lot; several agents can do more - and cost Nx
    more and fail Nx more ways. Multi-agent is an architecture you
    EARN: orchestrator/worker with explicit handoffs and shared state,
    or you get chaos.

Run:      python 15-multi-agent.py
Verify:   python 15-multi-agent.py --verify
Reference: https://arxiv.org/abs/2308.00352 (AutoGen)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# 1. Orchestrator/Worker
# ============================================================
# One orchestrator decides WHAT and assigns; workers execute. The
# orchestrator holds the plan; workers are interchangeable.

@dataclass
class Agent:
    name: str
    skill: str
    cost_per_call: float = 0.01
    calls: int = 0

    def work(self, task: str) -> str:
        self.calls += 1
        return f"[{self.name}] {self.skill}: {task}"


class Orchestrator:
    def __init__(self, workers: list[Agent]) -> None:
        self.workers = workers
        self.plan: list[tuple[str, str]] = []

    def assign(self, task: str, skill: str) -> Agent:
        """Route a task to the worker with the matching skill."""
        for w in self.workers:
            if w.skill == skill:
                self.plan.append((task, w.name))
                return w
        raise KeyError(f"no worker with skill: {skill}")

    def run(self, tasks: list[tuple[str, str]]) -> list[str]:
        return [self.assign(task, skill).work(task) for task, skill in tasks]

    def total_cost(self) -> float:
        return sum(w.calls * w.cost_per_call for w in self.workers)


# Example 1: orchestrator routing
researcher = Agent("researcher", "research", cost_per_call=0.02)
coder = Agent("coder", "code", cost_per_call=0.03)
reviewer = Agent("reviewer", "review", cost_per_call=0.01)
orch = Orchestrator([researcher, coder, reviewer])

outputs = orch.run([
    ("find best libraries", "research"),
    ("implement the solution", "code"),
    ("review the solution", "review"),
])
print("Example 1: orchestrator/worker")
for out in outputs:
    print(f"  {out}")
assert coder.calls == 1
assert abs(orch.total_cost() - (0.02 + 0.03 + 0.01)) < 1e-9, "cost sums"

# ============================================================
# 2. Handoffs
# ============================================================
# A worker can hand its output to the next worker. Handoffs carry
# context, so state must be explicit.

@dataclass
class Handoff:
    from_agent: str
    to_agent: str
    payload: Any


def handoff_chain(start: Agent, chain: list[tuple[Agent, Callable[[Any], Any]]],
                  initial: Any) -> list[Handoff]:
    """Run a chain of agents, handing results forward."""
    handoffs: list[Handoff] = []
    payload = initial
    prev = start.name
    for agent, transform in chain:
        payload = transform(agent.work(str(payload)))
        handoffs.append(Handoff(prev, agent.name, payload))
        prev = agent.name
    return handoffs


# Example 2: research -> code -> review chain
chain = [
    (coder, lambda s: f"implemented: {s}"),
    (reviewer, lambda s: f"reviewed: {s}"),
]
handoffs = handoff_chain(researcher, chain, "design a scraper")
print("\nExample 2: handoffs")
for h in handoffs:
    print(f"  {h.from_agent} -> {h.to_agent}: {str(h.payload)[:40]}")
assert handoffs[0].from_agent == "researcher" and handoffs[0].to_agent == "coder"
assert handoffs[-1].to_agent == "reviewer"

# ============================================================
# 3. Shared State
# ============================================================
# Agents share a state dict. Reads and writes must be explicit or
# workers silently work on stale information.

class SharedState:
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def snapshot(self) -> dict:
        return dict(self._data)


# Example 3: shared state across workers
state = SharedState()
state.set("query", "scraper design")
coder.work("implement from: " + state.get("query"))
state.set("code", "done")
reviewer.work("review " + state.get("code"))
print("\nExample 3: shared state")
print(f"  snapshot: {state.snapshot()}")
assert state.get("query") == "scraper design" and state.get("code") == "done"

# ============================================================
# 4. Cost Multiplication Risk
# ============================================================
# N agents x M turns x tokens = bill shock. Always model the cost
# BEFORE building the team.

def multi_agent_cost(n_agents: int, turns_per_agent: int,
                     tokens_per_turn: int, price_per_1m: float) -> float:
    total_tokens = n_agents * turns_per_agent * tokens_per_turn
    return total_tokens / 1_000_000 * price_per_1m


# Example 4: cost model
cost = multi_agent_cost(n_agents=4, turns_per_agent=5, tokens_per_turn=2000,
                        price_per_1m=15.0)
print("\nExample 4: cost multiplication")
print(f"  4 agents x 5 turns x 2k tokens -> ${cost:.2f} per task")
assert cost == 4 * 5 * 2000 / 1_000_000 * 15.0

# ============================================================
# 5. State Machine vs Free-Flow
# ============================================================
# State machines (finite steps, guarded transitions) are predictable.
# Free-flow agents are flexible but untraceable. Start with a state
# machine; loosen only with measurement.

STATES = ["init", "research", "code", "review", "done"]

def valid_transition(frm: str, to: str) -> bool:
    """Guarded transitions: research -> code -> review -> done."""
    order = {s: i for i, s in enumerate(STATES)}
    if frm not in order or to not in order:
        return False
    # allow skip-ahead only to done (abort), otherwise +1
    return to == "done" or order[to] == order[frm] + 1


# Example 5: guarded transitions
print("\nExample 5: state machine")
for frm, to in [("init", "research"), ("research", "code"),
                ("review", "init"), ("code", "research")]:
    print(f"  {frm} -> {to}: {'OK' if valid_transition(frm, to) else 'BLOCKED'}")
assert valid_transition("init", "research")
assert not valid_transition("review", "init"), "no going back"
assert not valid_transition("code", "research"), "no skipping back"

# ============================================================
# Production Pattern
# ============================================================
def build_team(skills: list[str]) -> tuple[Orchestrator, SharedState]:
    workers = [Agent(f"agent-{i}", skill) for i, skill in enumerate(skills)]
    return Orchestrator(workers), SharedState()


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: adding agents for tasks one agent does fine (cost without value)
# MISTAKE: free-flowing agents with no shared state (lost context)
# MISTAKE: no cost model - N agents is Nx the bill
# MISTAKE: no state machine - impossible to trace or debug


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    a1 = Agent("a1", "x")
    a2 = Agent("a2", "y")
    o = Orchestrator([a1, a2])
    assert o.assign("t", "y") is a2, "routes by skill"
    try:
        o.assign("t", "z")
        raised = False
    except KeyError:
        raised = True
    assert raised, "unknown skill raises"
    o.run([("t1", "x")])
    assert a1.calls == 1 and abs(o.total_cost() - a1.cost_per_call) < 1e-12

    hs = handoff_chain(Agent("s", "s"), [(Agent("n", "n"), lambda v: v)], "p")
    assert hs[0].from_agent == "s" and hs[0].to_agent == "n"

    st = SharedState()
    st.set("k", 1)
    assert st.get("k") == 1 and st.get("missing") is None
    assert st.snapshot() == {"k": 1}

    assert multi_agent_cost(2, 3, 1000, 10.0) == 2 * 3 * 1000 / 1e6 * 10.0

    assert valid_transition("init", "research")
    assert not valid_transition("code", "review") is False or True  # code->review is +1
    assert valid_transition("code", "review"), "code -> review allowed"
    assert not valid_transition("review", "code"), "backward blocked"
    print("[OK] 15-multi-agent: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Orchestrator/worker: route by skill, hold the plan.")
        print("2. Handoffs and shared state must be explicit.")
        print("3. Model cost; prefer state machines over free flow.")
        _verify()
