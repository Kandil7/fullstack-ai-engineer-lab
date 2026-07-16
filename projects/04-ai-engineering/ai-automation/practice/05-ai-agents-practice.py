"""
Practice Problems — Module 05: AI Agents (NO SOLUTIONS)
========================================================
Solve these yourself! No hints, no solutions.

Run: python 05-ai-agents-practice.py
Select a problem number to see the description.

Categories:
  EASY (20 XP):   Problems 1-5
  MEDIUM (50 XP): Problems 6-10
  HARD (100 XP):  Problems 11-15

Prerequisites:
    pip install openai python-dotenv pydantic
"""

from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: Tool Definition
# Write a Tool class that:
# - Has name, description, parameters (JSON schema), and a function
# - Has an execute(**kwargs) method that calls the function
# - Has a to_schema() method that returns OpenAI function-calling format
# - Handles errors gracefully (returns error string, doesn't raise)
class Tool:
    def __init__(self, name, description, parameters, function):
        pass  # Write your code here

    def execute(self, **kwargs) -> str:
        pass  # Write your code here

    def to_schema(self) -> dict:
        pass  # Write your code here


# Problem 2: Tool Registry
# Write a ToolRegistry class that:
# - Stores tools by name
# - Has register(tool), get(name), list_tools(), list_schemas()
# - Has execute(name, **kwargs) that looks up and runs a tool
# - Raises ValueError if tool not found
class ToolRegistry:
    def __init__(self):
        pass  # Write your code here

    def register(self, tool: Tool):
        pass  # Write your code here

    def get(self, name: str):
        pass  # Write your code here

    def list_tools(self) -> list[str]:
        pass  # Write your code here

    def list_schemas(self) -> list[dict]:
        pass  # Write your code here

    def execute(self, name: str, **kwargs) -> str:
        pass  # Write your code here


# Problem 3: Simple ReAct Agent
# Write a function that implements a basic ReAct loop:
# 1. Send prompt + tool schemas to LLM
# 2. If LLM wants to use a tool, execute it and send result back
# 3. If LLM gives a final answer, return it
# 4. Max 5 iterations to prevent infinite loops
def problem_03():
    pass  # Write your code here


# Problem 4: Agent Memory
# Write an AgentMemory class that:
# - Stores short-term memory (last N messages, default 10)
# - Stores long-term memory (key facts, unlimited)
# - Has add_message(role, content)
# - Has add_fact(key, value) for long-term
# - Has get_context() that returns formatted memory for prompts
# - Auto-trims short-term when exceeding limit
class AgentMemory:
    def __init__(self, short_term_limit: int = 10):
        pass  # Write your code here

    def add_message(self, role: str, content: str):
        pass  # Write your code here

    def add_fact(self, key: str, value: str):
        pass  # Write your code here

    def get_context(self) -> str:
        pass  # Write your code here


# Problem 5: Observation Formatter
# Write a function that formats agent observations for LLM consumption:
# - Takes a list of observations (tool results, errors, etc.)
# - Formats them with timestamps and types
# - Truncates long observations to max 500 chars
# - Returns a formatted string suitable for injection into prompts
def problem_05():
    pass  # Write your code here


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 6: Task Decomposer
# Write a function that takes a high-level goal and breaks it into steps:
# - Use LLM to decompose: "Research topic X, then write a report"
# - Return a list of Step objects: {id, description, dependencies, status}
# - Detect circular dependencies
# - Return execution order (topological sort)
@dataclass
class Step:
    id: str
    description: str
    dependencies: list[str] = field(default_factory=list)
    status: str = "pending"

def problem_06():
    pass  # Write your code here


# Problem 7: Goal Tracker
# Write a GoalTracker class that:
# - Tracks a hierarchy of goals (parent → subgoals)
# - Has methods: add_goal, complete_goal, get_progress, get_next_action
# - Computes overall progress as percentage
# - Detects blocked goals (subgoals incomplete)
# - Returns a status summary
class GoalTracker:
    def __init__(self):
        pass  # Write your code here

    def add_goal(self, goal_id: str, description: str, parent_id: str = None):
        pass  # Write your code here

    def complete_goal(self, goal_id: str):
        pass  # Write your code here

    def get_progress(self) -> dict:
        pass  # Write your code here

    def get_next_action(self) -> str:
        pass  # Write your code here


# Problem 8: Error Recovery Agent
# Write a function that wraps an agent with error recovery:
# - Catches tool execution errors
# - Logs the error with context
# - Asks LLM "Tool X failed with error Y. How should I recover?"
# - Implements the suggested recovery
# - Tracks error history
# - Gives up after 3 consecutive errors
def problem_08():
    pass  # Write your code here


# Problem 9: Conversational Memory Manager
# Write a ConversationalMemory class that:
# - Stores full conversation history
# - Has a summarize() method that compresses old messages into a summary
# - Keeps last 5 messages verbatim, summarizes everything before
# - Supports search (find messages mentioning a keyword)
# - Has get_window(center_index, window_size) for context extraction
class ConversationalMemory:
    def __init__(self):
        pass  # Write your code here

    def add(self, role: str, content: str):
        pass  # Write your code here

    def summarize(self):
        pass  # Write your code here

    def search(self, keyword: str) -> list[dict]:
        pass  # Write your code here

    def get_window(self, center: int, size: int = 5):
        pass  # Write your code here


# Problem 10: Prompt Injection Detector
# Write a function that detects prompt injection in user input:
# - Check for instruction override patterns ("ignore previous instructions")
# - Check for role manipulation ("you are now X")
# - Check for encoded/obfuscated attacks (base64, leetspeak)
# - Check for delimiter attacks (---, ===, system:)
# - Return {"safe": bool, "risk_level": str, "findings": list[str]}
def problem_10():
    pass  # Write your code here


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 11: Context Pruner
# Write a ContextPruner class that manages what goes into LLM context:
# - Takes a max_token_limit
# - Tracks importance scores for each piece of information
# - Prunes least important items when limit exceeded
# - Always keeps: system prompt, current task, last 3 messages
# - Has importance_decay() that reduces importance over time
class ContextPruner:
    def __init__(self, max_tokens: int = 4000):
        pass  # Write your code here

    def add(self, content: str, importance: float = 1.0, category: str = "general"):
        pass  # Write your code here

    def get_context(self) -> str:
        pass  # Write your code here

    def importance_decay(self, decay_rate: float = 0.9):
        pass  # Write your code here


# Problem 12: Tool Selector
# Write a ToolSelector class that:
# - Given a user query and available tools, selects the best tool
# - Uses LLM to analyze the query and recommend a tool
# - Considers tool descriptions, parameters, and past success rates
# - Falls back to "no tool needed" if no tool is appropriate
# - Tracks selection accuracy over time
class ToolSelector:
    def __init__(self, tools: list[Tool]):
        pass  # Write your code here

    def select(self, query: str) -> dict:
        pass  # Write your code here

    def record_outcome(self, tool_name: str, success: bool):
        pass  # Write your code here

    def get_stats(self) -> dict:
        pass  # Write your code here


# Problem 13: Agent Evaluator
# Write an AgentEvaluator class that:
# - Takes a test suite: list of {task, expected_tool, expected_answer_pattern}
# - Runs each task through the agent
# - Scores: tool_selection_accuracy, answer_quality, efficiency (steps taken)
# - Returns a detailed evaluation report
# - Supports comparison between agent versions
class AgentEvaluator:
    def __init__(self, agent_fn: Callable):
        pass  # Write your code here

    def evaluate(self, test_suite: list[dict]) -> dict:
        pass  # Write your code here

    def compare(self, other_eval: "AgentEvaluator") -> dict:
        pass  # Write your code here


# Problem 14: Self-Improving Agent
# Write a SelfImprovingAgent class that:
# - Tracks successes and failures
# - After each task, reflects: "What went well? What went wrong?"
# - Stores reflections as learned rules
# - Modifies its system prompt based on accumulated rules
# - Has a learning_rate that controls how quickly it adapts
# - Exports learned rules to a JSON file
class SelfImprovingAgent:
    def __init__(self):
        pass  # Write your code here

    def run_task(self, task: str) -> dict:
        pass  # Write your code here

    def reflect(self, task: str, result: dict):
        pass  # Write your code here

    def get_system_prompt(self) -> str:
        pass  # Write your code here

    def export_rules(self, path: str):
        pass  # Write your code here


# Problem 15: Full Agent Framework
# Build a complete Agent class that combines everything:
# - ToolRegistry for tools
# - AgentMemory for context
# - GoalTracker for task management
# - ReAct reasoning loop
# - Error recovery with max retries
# - Prompt injection defense
# - Observation formatting
# - Usage tracking (tokens, cost, time)
# - export_session(path) for debugging
class Agent:
    def __init__(self, name: str, model: str = "gpt-4o-mini"):
        pass  # Write your code here

    def register_tool(self, tool: Tool):
        pass  # Write your code here

    def run(self, task: str) -> dict:
        pass  # Write your code here

    def get_usage(self) -> dict:
        pass  # Write your code here

    def export_session(self, path: str):
        pass  # Write your code here


# ============================================================
# MAIN — Run to see problem descriptions
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Module 05: AI Agents — Practice Problems")
    print("=" * 60)
    print()

    problems = {
        1: ("Tool Definition", "Easy", 20),
        2: ("Tool Registry", "Easy", 20),
        3: ("Simple ReAct Agent", "Easy", 20),
        4: ("Agent Memory", "Easy", 20),
        5: ("Observation Formatter", "Easy", 20),
        6: ("Task Decomposer", "Medium", 50),
        7: ("Goal Tracker", "Medium", 50),
        8: ("Error Recovery Agent", "Medium", 50),
        9: ("Conversational Memory Manager", "Medium", 50),
        10: ("Prompt Injection Detector", "Medium", 50),
        11: ("Context Pruner", "Hard", 100),
        12: ("Tool Selector", "Hard", 100),
        13: ("Agent Evaluator", "Hard", 100),
        14: ("Self-Improving Agent", "Hard", 100),
        15: ("Full Agent Framework", "Hard", 100),
    }

    total_xp = sum(p[2] for p in problems.values())
    print(f"Total Problems: {len(problems)}")
    print(f"Total XP: {total_xp}")
    print()

    for num, (name, diff, xp) in problems.items():
        print(f"  [{num:2d}] {name:<40} {diff:<8} +{xp} XP")

    print()
    print("Select a problem number to see its full description.")
    print("Solve each function by replacing 'pass' with your implementation.")
    print("No solutions are provided — figure it out yourself!")
    print("=" * 60)
