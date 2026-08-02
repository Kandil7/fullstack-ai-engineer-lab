"""
GenAI - 13: Tool Calling
========================
Topics: tool schemas from type hints, the execution loop, parallel tools,
error handling, validating model-chosen arguments.

Why this matters for AI/backend engineering:
    Tool calling is how an LLM becomes an agent that can DO things:
    query databases, call APIs, run code. The production skill is not
    the schema - it is the loop: validate the model's arguments, execute
    safely, handle errors, and feed results back.

Run:      python 13-tool-calling.py
Verify:   python 13-tool-calling.py --verify
Reference: https://platform.openai.com/docs/guides/function-calling
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# 1. Tools: Schema + Implementation
# ============================================================

@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, str]       # name -> type
    required: list[str]
    impl: Callable[..., Any]

    def schema(self) -> dict:
        properties = {n: {"type": t} for n, t in self.parameters.items()}
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {"type": "object", "properties": properties,
                               "required": self.required},
            },
        }

    def validate_args(self, args: dict) -> list[str]:
        errors = []
        for req in self.required:
            if req not in args:
                errors.append(f"missing required arg: {req}")
        for name, expected in self.parameters.items():
            if name in args:
                if expected == "integer" and not isinstance(args[name], int):
                    errors.append(f"{name} must be integer, got {type(args[name]).__name__}")
                elif expected == "number" and not isinstance(args[name], (int, float)):
                    errors.append(f"{name} must be number")
                elif expected == "string" and not isinstance(args[name], str):
                    errors.append(f"{name} must be string")
        return errors

    def execute(self, args: dict) -> Any:
        errors = self.validate_args(args)
        if errors:
            raise ValueError(f"invalid tool args: {errors}")
        return self.impl(**args)


# Example 1: define a tool
def search_db(query: str, limit: int = 5) -> list[str]:
    return [f"result-{i} for {query!r}" for i in range(min(limit, 3))]


search_tool = Tool("search_db", "Search the database", 
                   {"query": "string", "limit": "integer"}, ["query"], search_db)
print("Example 1: tool schema")
print(f"  {search_tool.schema()['function']['name']} required={search_tool.required}")

# ============================================================
# 2. The Execution Loop
# ============================================================
# Model returns a tool call -> validate args -> execute -> feed result
# back as a 'tool' message -> model continues.

def run_tool_loop(tools: dict[str, Tool], initial_tool_call: dict,
                  rounds: int = 3) -> list[dict]:
    """Execute a model-requested tool call and return the message trail."""
    trail: list[dict] = [{"role": "assistant", "tool_calls": [initial_tool_call]}]
    for _ in range(rounds):
        call = initial_tool_call
        name = call.get("name", "")
        args = call.get("arguments", {})
        if name not in tools:
            trail.append({"role": "tool", "name": name, "error": "unknown tool"})
            break
        tool = tools[name]
        try:
            result = tool.execute(args)
            trail.append({"role": "tool", "name": name, "content": str(result)})
            break  # in a real loop the model would see this and continue
        except ValueError as e:
            trail.append({"role": "tool", "name": name, "error": str(e)})
            break
    return trail


# Example 2: valid call
trail = run_tool_loop({"search_db": search_tool},
                      {"name": "search_db", "arguments": {"query": "users", "limit": 2}})
print("\nExample 2: valid tool call")
for m in trail:
    print(f"  [{m['role']}] {m.get('content', m.get('error', ''))}")
assert trail[-1]["role"] == "tool" and "result-0" in trail[-1]["content"]

# ============================================================
# 3. Invalid Arguments Are Rejected
# ============================================================
# The model will hallucinate arguments. Validate BEFORE executing -
# never run tools with unvalidated input.

# Example 3: bad args rejected
bad_trail = run_tool_loop({"search_db": search_tool},
                          {"name": "search_db", "arguments": {"limit": "ten"}})
print("\nExample 3: invalid args")
print(f"  {bad_trail[-1]}")
assert "error" in bad_trail[-1] and "limit" in bad_trail[-1]["error"], "args validated"

# ============================================================
# 4. Parallel Tool Calls
# ============================================================
# Models can request several tools at once. Execute them (ideally in
# parallel) and merge the results.

def run_parallel(tools: dict[str, Tool], calls: list[dict]) -> list[dict]:
    results = []
    for call in calls:
        name, args = call["name"], call["arguments"]
        if name in tools:
            try:
                results.append({"name": name, "content": str(tools[name].execute(args))})
            except ValueError as e:
                results.append({"name": name, "error": str(e)})
        else:
            results.append({"name": name, "error": "unknown tool"})
    return results


# Example 4: parallel calls
parallel = run_parallel({"search_db": search_tool}, [
    {"name": "search_db", "arguments": {"query": "a"}},
    {"name": "search_db", "arguments": {"query": "b"}},
])
print("\nExample 4: parallel tool calls")
for r in parallel:
    print(f"  {r}")
assert len(parallel) == 2 and all("result-0" in r["content"] for r in parallel)

# ============================================================
# Production Pattern
# ============================================================
# The production loop: schema from type hints, validate args, execute
# with a safety wrapper, never expose raw errors to the model.

def tool_from_callable(name: str, description: str, fn: Callable,
                       required: list[str]) -> Tool:
    """Derive a Tool from a callable's annotated signature.

    Works whether annotations are evaluated (str class) or deferred
    (string forms under `from __future__ import annotations`).
    """
    import inspect
    hints = inspect.signature(fn).parameters
    params: dict[str, str] = {}
    for p in hints:
        ann = hints[p].annotation
        raw = getattr(ann, "__name__", str(ann))
        if raw in ("int", "integer"):
            params[p] = "integer"
        elif raw in ("float", "number"):
            params[p] = "number"
        else:
            params[p] = "string"
    return Tool(name, description, params, required, fn)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: executing tool calls without validating arguments
# MISTAKE: letting the model run destructive tools (shell, delete) freely
# MISTAKE: no error path - a failed tool crashes the whole loop
# MISTAKE: unbounded loop - cap tool rounds to stop runaway agents


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    t = Tool("add", "add two numbers", {"a": "number", "b": "number"},
             ["a", "b"], lambda a, b: a + b)
    assert t.execute({"a": 1, "b": 2}) == 3
    assert t.schema()["function"]["name"] == "add"

    # missing required
    try:
        t.execute({"a": 1})
        raised = False
    except ValueError:
        raised = True
    assert raised, "missing required arg rejected"

    # wrong type
    try:
        t.execute({"a": "x", "b": 1})
        raised = False
    except ValueError:
        raised = True
    assert raised, "wrong type rejected"

    # unknown tool in loop
    trail = run_tool_loop({"add": t}, {"name": "nope", "arguments": {}})
    assert "unknown tool" in trail[-1].get("error", ""), "unknown tool handled"

    # parallel
    par = run_parallel({"add": t}, [{"name": "add", "arguments": {"a": 1, "b": 1}}])
    assert par[0]["content"] == "2", "parallel executes"

    # derived tool
    def greet(name: str) -> str:
        return f"hi {name}"
    gt = tool_from_callable("greet", "greet a user", greet, ["name"])
    assert gt.execute({"name": "bob"}) == "hi bob"
    print("[OK] 13-tool-calling: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Tools = schema + implementation + validation.")
        print("2. Validate model-chosen arguments before executing.")
        print("3. Handle errors, support parallel calls, cap the loop.")
        _verify()
