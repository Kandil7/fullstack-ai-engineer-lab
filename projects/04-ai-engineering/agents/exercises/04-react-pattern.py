"""
=============================================================
EXERCISE 04: ReAct Pattern (Reasoning + Acting)
=============================================================
Topic: Thought → Action → Observation Loop for Agents

Learning Objectives:
- Implement the ReAct (Reasoning + Acting) pattern
- Define action spaces for agents
- Parse observations from tool results
- Design loop termination conditions
- Build multi-tool ReAct agents
- Handle errors and recovery in ReAct loops

Prerequisites:
- Python 3.10+
- json, re, dataclasses
=============================================================
"""

import json
import re
import time
import uuid
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
from datetime import datetime


# ============================================================
# SECTION 1: ReAct Core Concepts
# ============================================================

class ActionType(Enum):
    """Types of actions an agent can take."""
    TOOL_CALL = "tool_call"
    THINK = "think"
    ANSWER = "answer"
    WAIT = "wait"
    RETRY = "retry"
    ABORT = "abort"


@dataclass
class Thought:
    """Represents the agent's internal reasoning."""
    content: str
    reasoning: str = ""
    confidence: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
        }


@dataclass
class Action:
    """Represents an action the agent takes."""
    action_type: ActionType
    tool_name: str = ""
    arguments: dict = field(default_factory=dict)
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "action_type": self.action_type.value,
            "tool_name": self.tool_name,
            "arguments": self.arguments,
            "description": self.description,
        }


@dataclass
class Observation:
    """Represents the result of an action."""
    content: str
    success: bool = True
    metadata: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "success": self.success,
            "metadata": self.metadata,
        }


@dataclass
class ReActStep:
    """A single step in the ReAct loop."""
    step_number: int
    thought: Thought
    action: Action
    observation: Observation
    duration_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "step": self.step_number,
            "thought": self.thought.to_dict(),
            "action": self.action.to_dict(),
            "observation": self.observation.to_dict(),
            "duration_ms": self.duration_ms,
        }


# ============================================================
# SECTION 2: Action Space Definition
# ============================================================

class ActionSpace:
    """
    Defines the available actions for the agent.
    Maps action names to handlers and schemas.
    """

    def __init__(self):
        self._actions: dict[str, dict] = {}

    def register(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        parameters: dict = None,
        category: str = "general",
    ):
        """Register an action in the action space."""
        self._actions[name] = {
            "name": name,
            "handler": handler,
            "description": description,
            "parameters": parameters or {},
            "category": category,
        }

    def get_handler(self, name: str) -> Optional[Callable]:
        """Get the handler for an action."""
        action = self._actions.get(name)
        return action["handler"] if action else None

    def get_description(self, name: str) -> str:
        """Get the description of an action."""
        action = self._actions.get(name)
        return action["description"] if action else ""

    def list_actions(self, category: str = None) -> list[dict]:
        """List all available actions."""
        actions = []
        for name, info in self._actions.items():
            if category and info["category"] != category:
                continue
            actions.append({
                "name": name,
                "description": info["description"],
                "category": info["category"],
                "parameters": info["parameters"],
            })
        return actions

    def to_prompt(self) -> str:
        """Generate a prompt describing available actions."""
        lines = ["Available actions:"]
        for name, info in self._actions.items():
            params = ", ".join(info["parameters"].keys()) if info["parameters"] else "none"
            lines.append(f"  - {name}: {info['description']} (params: {params})")
        return "\n".join(lines)

    def execute(self, name: str, **kwargs) -> dict:
        """Execute an action by name."""
        handler = self.get_handler(name)
        if not handler:
            return {"success": False, "error": f"Unknown action: {name}"}
        try:
            result = handler(**kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ============================================================
# SECTION 3: Built-in Actions/Tools
# ============================================================

def calculator_action(expression: str = "0") -> Any:
    """Calculate a mathematical expression."""
    allowed = {
        "sqrt": math.sqrt, "abs": abs, "round": round,
        "sin": math.sin, "cos": math.cos, "pi": math.pi,
    }
    return eval(expression, {"__builtins__": {}}, allowed)


def search_action(query: str = "") -> list[dict]:
    """Search for information (mock implementation)."""
    return [
        {"title": f"About {query}", "snippet": f"Detailed info about {query}..."},
        {"title": f"{query} Guide", "snippet": f"How to use {query}..."},
    ]


def text_analysis_action(text: str = "") -> dict:
    """Analyze text statistics."""
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "avg_word_length": round(sum(len(w) for w in words) / max(len(words), 1), 2),
    }


def summary_action(text: str = "", max_length: int = 100) -> str:
    """Create a simple summary of text."""
    if len(text) <= max_length:
        return text
    sentences = text.split(". ")
    summary = ". ".join(sentences[:2]) + "."
    return summary[:max_length] + "..." if len(summary) > max_length else summary


def code_analysis_action(code: str = "") -> dict:
    """Analyze code for basic patterns."""
    lines = code.split("\n")
    functions = [l.strip() for l in lines if l.strip().startswith("def ")]
    classes = [l.strip() for l in lines if l.strip().startswith("class ")]
    imports = [l.strip() for l in lines if l.strip().startswith("import ") or l.strip().startswith("from ")]
    return {
        "line_count": len(lines),
        "function_count": len(functions),
        "class_count": len(classes),
        "import_count": len(imports),
        "functions": [f.split("(")[0].replace("def ", "") for f in functions],
    }


# Create the standard action space
def create_standard_action_space() -> ActionSpace:
    """Create an action space with common tools."""
    space = ActionSpace()
    space.register("calculator", calculator_action,
                    "Evaluate mathematical expressions",
                    {"expression": "Math expression to evaluate"},
                    "computation")
    space.register("search", search_action,
                    "Search for information on a topic",
                    {"query": "Search query"},
                    "information")
    space.register("analyze_text", text_analysis_action,
                    "Analyze text for statistics",
                    {"text": "Text to analyze"},
                    "text")
    space.register("summarize", summary_action,
                    "Create a summary of text",
                    {"text": "Text to summarize", "max_length": "Max summary length"},
                    "text")
    space.register("analyze_code", code_analysis_action,
                    "Analyze code structure",
                    {"code": "Code to analyze"},
                    "code")
    return space


# ============================================================
# SECTION 4: ReAct Agent Implementation
# ============================================================

class ReActAgent:
    """
    Implements the ReAct (Reasoning + Acting) pattern.

    The ReAct pattern alternates between:
    1. THOUGHT: The agent reasons about the current situation
    2. ACTION: The agent takes an action (tool call)
    3. OBSERVATION: The agent observes the result

    This continues until the agent has enough information to answer.
    """

    def __init__(
        self,
        action_space: ActionSpace = None,
        max_steps: int = 10,
        max_retries: int = 2,
        system_prompt: str = "",
    ):
        self.action_space = action_space or create_standard_action_space()
        self.max_steps = max_steps
        self.max_retries = max_retries
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.steps: list[ReActStep] = []
        self.observations_history: list[Observation] = []
        self._iteration = 0

    @staticmethod
    def _default_system_prompt() -> str:
        return (
            "You are a ReAct agent that solves problems by thinking step by step.\n"
            "For each step:\n"
            "1. THINK: Analyze the situation and decide what to do\n"
            "2. ACTION: Take a specific action using available tools\n"
            "3. OBSERVE: Examine the result\n"
            "Repeat until you have enough information to provide a final answer."
        )

    def _think(self, user_input: str, history: list[ReActStep]) -> Thought:
        """
        Generate a thought based on the current situation.
        In production, this calls the LLM. Here we simulate reasoning.
        """
        # Analyze what's been done so far
        previous_observations = [s.observation.content for s in history]
        tools_used = [s.action.tool_name for s in history if s.action.tool_name]

        # Simple reasoning heuristics
        input_lower = user_input.lower()

        # Determine if we have enough info
        if len(history) >= 2 and not any("error" in obs.lower() for obs in previous_observations):
            return Thought(
                content="I have gathered enough information to provide a final answer.",
                reasoning=f"Used {len(history)} steps, tools: {tools_used}",
                confidence=0.8,
            )

        # Decide what to do next
        if "calculate" in input_lower or "math" in input_lower or any(c.isdigit() for c in user_input):
            if "calculator" not in tools_used:
                return Thought(
                    content="I should calculate the mathematical expression.",
                    reasoning="Input contains mathematical operations.",
                    confidence=0.9,
                )

        if "search" in input_lower or "find" in input_lower or "what is" in input_lower:
            if "search" not in tools_used:
                return Thought(
                    content="I should search for information on this topic.",
                    reasoning="The question requires external information.",
                    confidence=0.8,
                )

        if "analyze" in input_lower or "count" in input_lower or "statistics" in input_lower:
            if "analyze_text" not in tools_used:
                return Thought(
                    content="I should analyze the text for statistics.",
                    reasoning="The request involves text analysis.",
                    confidence=0.85,
                )

        if "summarize" in input_lower or "summary" in input_lower:
            if "summarize" not in tools_used:
                return Thought(
                    content="I should create a summary of the provided text.",
                    reasoning="The user wants a summary.",
                    confidence=0.9,
                )

        if "code" in input_lower:
            if "analyze_code" not in tools_used:
                return Thought(
                    content="I should analyze the code structure.",
                    reasoning="The request involves code analysis.",
                    confidence=0.85,
                )

        # Default: try to answer directly if we have observations
        if previous_observations:
            return Thought(
                content="I have enough information to formulate an answer.",
                reasoning=f"Based on {len(previous_observations)} observations.",
                confidence=0.7,
            )

        return Thought(
            content="I need to gather more information to answer this question.",
            reasoning="Initial analysis requires more data.",
            confidence=0.5,
        )

    def _decide_action(self, thought: Thought, user_input: str) -> Action:
        """
        Based on the thought, decide which action to take.
        """
        input_lower = user_input.lower()

        # Map thought to action
        if "calculate" in thought.content.lower():
            # Extract numbers from input
            numbers = re.findall(r'\d+\.?\d*', user_input)
            if len(numbers) >= 2:
                expression = f"{numbers[0]} + {numbers[1]}"
            elif numbers:
                expression = numbers[0]
            else:
                expression = "0"
            return Action(
                action_type=ActionType.TOOL_CALL,
                tool_name="calculator",
                arguments={"expression": expression},
                description="Calculating the result",
            )

        if "search" in thought.content.lower():
            return Action(
                action_type=ActionType.TOOL_CALL,
                tool_name="search",
                arguments={"query": user_input},
                description="Searching for information",
            )

        if "analyze" in thought.content.lower() and "code" not in thought.content.lower():
            return Action(
                action_type=ActionType.TOOL_CALL,
                tool_name="analyze_text",
                arguments={"text": user_input},
                description="Analyzing text statistics",
            )

        if "analyze" in thought.content.lower() and "code" in thought.content.lower():
            return Action(
                action_type=ActionType.TOOL_CALL,
                tool_name="analyze_code",
                arguments={"code": user_input},
                description="Analyzing code structure",
            )

        if "summarize" in thought.content.lower():
            return Action(
                action_type=ActionType.TOOL_CALL,
                tool_name="summarize",
                arguments={"text": user_input},
                description="Creating summary",
            )

        if "enough information" in thought.content.lower():
            # Generate answer
            answer = self._generate_answer(user_input)
            return Action(
                action_type=ActionType.ANSWER,
                description="Providing final answer",
            )

        return Action(
            action_type=ActionType.TOOL_CALL,
            tool_name="search",
            arguments={"query": user_input},
            description="Default: searching for information",
        )

    def _generate_answer(self, user_input: str) -> str:
        """Generate a final answer based on observations."""
        if not self.observations_history:
            return f"I wasn't able to find specific information about '{user_input}'."

        # Combine observations into an answer
        answers = []
        for obs in self.observations_history:
            if obs.success:
                try:
                    data = json.loads(obs.content) if isinstance(obs.content, str) else obs.content
                    if isinstance(data, dict):
                        if "result" in data:
                            answers.append(f"Result: {data['result']}")
                        elif "word_count" in data:
                            answers.append(f"Text analysis: {data}")
                        else:
                            answers.append(str(data))
                    else:
                        answers.append(str(data))
                except (json.JSONDecodeError, TypeError):
                    answers.append(obs.content[:200])

        return " | ".join(answers) if answers else "No results found."

    def _execute_action(self, action: Action) -> Observation:
        """Execute an action and return an observation."""
        if action.action_type == ActionType.ANSWER:
            answer = self._generate_answer(action.arguments.get("query", ""))
            return Observation(content=answer, success=True)

        if action.action_type != ActionType.TOOL_CALL:
            return Observation(
                content=f"Action type {action.action_type.value} not implemented",
                success=False,
            )

        # Execute the tool
        result = self.action_space.execute(action.tool_name, **action.arguments)

        if result.get("success"):
            return Observation(
                content=json.dumps(result["result"], default=str),
                success=True,
                metadata={"tool": action.tool_name},
            )
        else:
            return Observation(
                content=result.get("error", "Unknown error"),
                success=False,
                metadata={"tool": action.tool_name},
            )

    def run(self, user_input: str, verbose: bool = True) -> str:
        """
        Execute the ReAct loop for a given user input.

        The loop:
        1. Think about what to do
        2. Decide on an action
        3. Execute the action
        4. Observe the result
        5. Repeat until done or max steps reached
        """
        self.steps = []
        self.observations_history = []
        self._iteration = 0

        if verbose:
            print(f"\n{'='*60}")
            print(f"ReAct Agent: {user_input[:80]}")
            print(f"{'='*60}")

        for step_num in range(1, self.max_steps + 1):
            self._iteration = step_num
            step_start = time.time()

            # THOUGHT
            if verbose:
                print(f"\n--- Step {step_num} ---")
            thought = self._think(user_input, self.steps)
            if verbose:
                print(f"  THINK: {thought.content}")
                print(f"    Reasoning: {thought.reasoning}")

            # ACTION
            action = self._decide_action(thought, user_input)
            if verbose:
                print(f"  ACTION: {action.action_type.value}")
                if action.tool_name:
                    print(f"    Tool: {action.tool_name}")
                    print(f"    Args: {json.dumps(action.arguments, default=str)[:100]}")

            # OBSERVATION
            observation = self._execute_action(action)
            self.observations_history.append(observation)
            if verbose:
                print(f"  OBSERVE: {observation.content[:150]}...")

            # Record step
            duration = (time.time() - step_start) * 1000
            step = ReActStep(
                step_number=step_num,
                thought=thought,
                action=action,
                observation=observation,
                duration_ms=duration,
            )
            self.steps.append(step)

            # Check termination
            if action.action_type == ActionType.ANSWER:
                if verbose:
                    print(f"\n  [AGENT] Providing final answer")
                return observation.content

            if not observation.success:
                if verbose:
                    print(f"  [AGENT] Action failed, retrying...")
                # The next iteration will handle retry

        # Max steps reached
        if verbose:
            print(f"\n  [AGENT] Max steps ({self.max_steps}) reached")
        return self._generate_answer(user_input)

    def get_trace(self) -> list[dict]:
        """Get the full execution trace."""
        return [step.to_dict() for step in self.steps]

    def get_stats(self) -> dict:
        """Get execution statistics."""
        if not self.steps:
            return {"steps": 0}

        total_time = sum(s.duration_ms for s in self.steps)
        tools_used = {}
        for step in self.steps:
            if step.action.tool_name:
                tools_used[step.action.tool_name] = tools_used.get(step.action.tool_name, 0) + 1

        return {
            "steps": len(self.steps),
            "total_time_ms": round(total_time, 2),
            "avg_step_time_ms": round(total_time / len(self.steps), 2),
            "tools_used": tools_used,
            "final_answer": self.steps[-1].observation.content[:100] if self.steps else None,
        }


# ============================================================
# SECTION 5: Advanced ReAct — With Error Recovery
# ============================================================

class ResilientReActAgent(ReActAgent):
    """
    ReAct agent with error recovery and backtracking.
    Can recover from failed actions and try alternative approaches.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_actions: list[str] = []
        self.backtrack_count: int = 0

    def _think_with_recovery(self, user_input: str, history: list[ReActStep]) -> Thought:
        """Enhanced thinking that considers failures."""
        # Check if we have failures to recover from
        if self.failed_actions:
            failed_tools = list(set(self.failed_actions))
            return Thought(
                content=f"Previous actions failed: {failed_tools}. Trying alternative approach.",
                reasoning="Need to find alternative tool or method.",
                confidence=0.6,
            )

        return self._think(user_input, history)

    def _decide_action_with_recovery(self, thought: Thought, user_input: str) -> Action:
        """Enhanced action decision that avoids failed tools."""
        if self.failed_actions:
            # Try a different tool
            available_tools = ["calculator", "search", "analyze_text", "summarize", "analyze_code"]
            failed_tools = set(self.failed_actions)
            alternative_tools = [t for t in available_tools if t not in failed_tools]

            if alternative_tools:
                tool = alternative_tools[0]
                return Action(
                    action_type=ActionType.TOOL_CALL,
                    tool_name=tool,
                    arguments={"text": user_input, "query": user_input, "expression": "1+1"}.get(tool, {"text": user_input}),
                    description=f"Trying alternative tool: {tool}",
                )

        return self._decide_action(thought, user_input)

    def run_with_recovery(self, user_input: str, verbose: bool = True) -> str:
        """Run with error recovery and backtracking."""
        self.failed_actions = []
        self.backtrack_count = 0

        if verbose:
            print(f"\n{'='*60}")
            print(f"Resilient ReAct Agent: {user_input[:80]}")
            print(f"{'='*60}")

        for step_num in range(1, self.max_steps + 1):
            step_start = time.time()

            # THOUGHT (with recovery awareness)
            thought = self._think_with_recovery(user_input, self.steps)
            if verbose:
                print(f"\n  Step {step_num}:")
                print(f"    THINK: {thought.content}")

            # ACTION (with recovery awareness)
            action = self._decide_action_with_recovery(thought, user_input)
            if verbose:
                print(f"    ACTION: {action.action_type.value} ({action.tool_name or 'direct'})")

            # OBSERVE
            observation = self._execute_action(action)

            if not observation.success:
                self.failed_actions.append(action.tool_name)
                self.backtrack_count += 1
                if verbose:
                    print(f"    OBSERVE: FAILED - {observation.content}")
                    print(f"    [RECOVERY] Backtracking (attempt {self.backtrack_count})")
            else:
                self.observations_history.append(observation)
                if verbose:
                    print(f"    OBSERVE: {observation.content[:120]}...")

            duration = (time.time() - step_start) * 1000
            self.steps.append(ReActStep(
                step_number=step_num, thought=thought, action=action,
                observation=observation, duration_ms=duration,
            ))

            if action.action_type == ActionType.ANSWER:
                return observation.content

        return self._generate_answer(user_input)


# ============================================================
# SECTION 6: ReAct Pattern Variants
# ============================================================

class PlanAndExecuteAgent:
    """
    Variant: Plan first, then execute the plan step by step.
    This is a simplification of the ReAct pattern for predictable tasks.
    """

    def __init__(self, action_space: ActionSpace = None):
        self.action_space = action_space or create_standard_action_space()

    def plan(self, goal: str) -> list[dict]:
        """Generate a plan of actions to achieve the goal."""
        goal_lower = goal.lower()
        plan = []

        if "calculate" in goal_lower or "compute" in goal_lower:
            plan.append({"step": 1, "action": "calculator", "args": {"expression": "1+1"}, "purpose": "Perform calculation"})
            plan.append({"step": 2, "action": "summarize", "args": {"text": "Calculation result"}, "purpose": "Format result"})

        elif "analyze" in goal_lower:
            plan.append({"step": 1, "action": "analyze_text", "args": {"text": goal}, "purpose": "Analyze content"})
            plan.append({"step": 2, "action": "summarize", "args": {"text": "Analysis results"}, "purpose": "Summarize findings"})

        elif "search" in goal_lower or "find" in goal_lower:
            plan.append({"step": 1, "action": "search", "args": {"query": goal}, "purpose": "Search for information"})
            plan.append({"step": 2, "action": "summarize", "args": {"text": "Search results"}, "purpose": "Summarize findings"})

        else:
            plan.append({"step": 1, "action": "search", "args": {"query": goal}, "purpose": "Initial research"})
            plan.append({"step": 2, "action": "analyze_text", "args": {"text": "Research findings"}, "purpose": "Analyze results"})
            plan.append({"step": 3, "action": "summarize", "args": {"text": "Analysis"}, "purpose": "Create final summary"})

        return plan

    def execute_plan(self, plan: list[dict], verbose: bool = True) -> str:
        """Execute a plan step by step."""
        results = []

        for step in plan:
            if verbose:
                print(f"\n  Step {step['step']}: {step['purpose']}")
                print(f"    Action: {step['action']}")

            result = self.action_space.execute(step["action"], **step["args"])
            results.append(result)

            if verbose:
                status = "OK" if result.get("success") else "FAIL"
                print(f"    Result: {status}")

        # Return combined results
        successful = [r for r in results if r.get("success")]
        return json.dumps([r.get("result") for r in successful], default=str, indent=2)

    def run(self, goal: str, verbose: bool = True) -> str:
        """Plan and execute a goal."""
        if verbose:
            print(f"\n{'='*60}")
            print(f"Plan & Execute Agent: {goal}")
            print(f"{'='*60}")

        plan = self.plan(goal)
        if verbose:
            print(f"\n  Plan ({len(plan)} steps):")
            for step in plan:
                print(f"    {step['step']}. {step['purpose']} → {step['action']}")

        return self.execute_plan(plan, verbose)


class MultiToolReActAgent(ReActAgent):
    """
    ReAct agent that can use multiple tools simultaneously.
    Demonstrates parallel tool execution within the ReAct loop.
    """

    def _decide_parallel_actions(self, thought: Thought, user_input: str) -> list[Action]:
        """Decide on multiple actions to execute in parallel."""
        actions = []
        input_lower = user_input.lower()

        # If the input has multiple aspects, use multiple tools
        if "analyze" in input_lower and "search" in input_lower:
            actions.append(Action(
                action_type=ActionType.TOOL_CALL,
                tool_name="analyze_text",
                arguments={"text": user_input},
                description="Analyzing text",
            ))
            actions.append(Action(
                action_type=ActionType.TOOL_CALL,
                tool_name="search",
                arguments={"query": user_input},
                description="Searching for info",
            ))
        else:
            # Default to single action
            actions.append(self._decide_action(thought, user_input))

        return actions

    def run_parallel(self, user_input: str, verbose: bool = True) -> str:
        """Execute ReAct loop with parallel tool calls."""
        if verbose:
            print(f"\n{'='*60}")
            print(f"Multi-Tool ReAct Agent: {user_input[:80]}")
            print(f"{'='*60}")

        for step_num in range(1, self.max_steps + 1):
            thought = self._think(user_input, self.steps)
            actions = self._decide_parallel_actions(thought, user_input)

            if verbose:
                print(f"\n  Step {step_num}:")
                print(f"    THINK: {thought.content}")
                print(f"    ACTIONS ({len(actions)}):")

            # Execute all actions
            for action in actions:
                observation = self._execute_action(action)
                self.observations_history.append(observation)
                if verbose:
                    print(f"      → {action.tool_name}: {observation.content[:80]}...")

                self.steps.append(ReActStep(
                    step_number=step_num, thought=thought, action=action,
                    observation=observation,
                ))

            # Check if we should stop
            if any(a.action_type == ActionType.ANSWER for a in actions):
                return self._generate_answer(user_input)

        return self._generate_answer(user_input)


# ============================================================
# SECTION 7: Running the Exercises
# ============================================================

def exercise_1_react_basics():
    """Exercise 4.1: Basic ReAct loop."""
    print("\n" + "=" * 60)
    print("EXERCISE 4.1: Basic ReAct Loop")
    print("=" * 60)

    agent = ReActAgent(max_steps=5)
    agent.run("Calculate 42 + 58", verbose=True)

    print(f"\n  Stats: {json.dumps(agent.get_stats(), indent=4)}")


def exercise_2_react_tracing():
    """Exercise 4.2: ReAct execution trace."""
    print("\n" + "=" * 60)
    print("EXERCISE 4.2: ReAct Execution Trace")
    print("=" * 60)

    agent = ReActAgent(max_steps=5)
    agent.run("What is 100 * 200?", verbose=False)

    print("  Execution Trace:")
    for step in agent.get_trace():
        print(f"\n  Step {step['step']}:")
        print(f"    Thought: {step['thought']['content']}")
        print(f"    Action: {step['action']['action_type']} ({step['action']['tool_name']})")
        print(f"    Observation: {step['observation']['content'][:80]}...")

    stats = agent.get_stats()
    print(f"\n  Stats:")
    print(f"    Steps: {stats['steps']}")
    print(f"    Total time: {stats['total_time_ms']:.2f}ms")
    print(f"    Tools used: {stats['tools_used']}")


def exercise_3_action_space():
    """Exercise 4.3: Custom action spaces."""
    print("\n" + "=" * 60)
    print("EXERCISE 4.3: Custom Action Spaces")
    print("=" * 60)

    # Create a specialized action space for data analysis
    data_space = ActionSpace()

    def csv_parser(data: str = "") -> dict:
        """Parse CSV-like data."""
        lines = data.strip().split("\n")
        if len(lines) < 2:
            return {"error": "Insufficient data"}
        headers = lines[0].split(",")
        rows = [line.split(",") for line in lines[1:]]
        return {"headers": headers, "row_count": len(rows), "columns": len(headers)}

    def stats_calculator(values: str = "") -> dict:
        """Calculate basic statistics."""
        nums = [float(x.strip()) for x in values.split(",") if x.strip()]
        if not nums:
            return {"error": "No numbers provided"}
        return {
            "mean": round(sum(nums) / len(nums), 2),
            "min": min(nums),
            "max": max(nums),
            "count": len(nums),
            "sum": round(sum(nums), 2),
        }

    data_space.register("parse_csv", csv_parser, "Parse CSV data", {"data": "CSV string"})
    data_space.register("calc_stats", stats_calculator, "Calculate statistics", {"values": "Comma-separated numbers"})

    print("  Custom Action Space:")
    for action in data_space.list_actions():
        print(f"    {action['name']}: {action['description']}")

    # Test
    result = data_space.execute("parse_csv", data="name,age,score\nAlice,30,95\nBob,25,87")
    print(f"\n  CSV Parse: {result}")

    result = data_space.execute("calc_stats", values="10, 20, 30, 40, 50")
    print(f"  Stats: {result}")


def exercise_4_resilient_agent():
    """Exercise 4.4: ReAct with error recovery."""
    print("\n" + "=" * 60)
    print("EXERCISE 4.4: Resilient ReAct Agent")
    print("=" * 60)

    agent = ResilientReActAgent(max_steps=5)
    agent.run_with_recovery("Analyze this text: The quick brown fox jumps over the lazy dog", verbose=True)

    print(f"\n  Failed actions: {agent.failed_actions}")
    print(f"  Backtracks: {agent.backtrack_count}")


def exercise_5_plan_execute():
    """Exercise 4.5: Plan and Execute pattern."""
    print("\n" + "=" * 60)
    print("EXERCISE 4.5: Plan & Execute Pattern")
    print("=" * 60)

    agent = PlanAndExecuteAgent()
    result = agent.run("Analyze and summarize this data: 10, 20, 30, 40, 50", verbose=True)
    print(f"\n  Final Result: {result[:200]}")


def exercise_6_multi_tool():
    """Exercise 4.6: Multi-tool ReAct agent."""
    print("\n" + "=" * 60)
    print("EXERCISE 4.6: Multi-Tool ReAct Agent")
    print("=" * 60)

    agent = MultiToolReActAgent(max_steps=3)
    agent.run_parallel("Analyze and search for information about Python", verbose=True)


def exercise_7_react_comparison():
    """Exercise 4.7: Compare ReAct variants."""
    print("\n" + "=" * 60)
    print("EXERCISE 4.7: ReAct Pattern Comparison")
    print("=" * 60)

    test_inputs = [
        "Calculate 15 + 27",
        "Analyze this text: Hello world this is a test",
    ]

    agents = {
        "Basic ReAct": ReActAgent(max_steps=3),
        "Resilient ReAct": ResilientReActAgent(max_steps=3),
        "Plan & Execute": PlanAndExecuteAgent(),
    }

    for input_text in test_inputs:
        print(f"\n  Input: {input_text}")
        for name, agent in agents.items():
            if isinstance(agent, PlanAndExecuteAgent):
                result = agent.run(input_text, verbose=False)
            elif isinstance(agent, ResilientReActAgent):
                result = agent.run_with_recovery(input_text, verbose=False)
            else:
                result = agent.run(input_text, verbose=False)
            print(f"    {name}: {result[:80]}...")


def exercise_8_react_visualization():
    """Exercise 4.8: Visualize the ReAct loop."""
    print("\n" + "=" * 60)
    print("EXERCISE 4.8: ReAct Loop Visualization")
    print("=" * 60)

    agent = ReActAgent(max_steps=3)
    agent.run("Calculate 10 * 5", verbose=False)

    print("\n  ReAct Loop Visualization:")
    print("  " + "=" * 50)

    for step in agent.steps:
        # Thought
        print(f"  ┌─ Step {step.step_number} ─────────────────────")
        print(f"  │ 💭 THINK: {step.thought.content[:50]}...")

        # Action
        if step.action.tool_name:
            print(f"  │ ⚡ ACTION: {step.action.tool_name}({json.dumps(step.action.arguments, default=str)[:40]})")
        else:
            print(f"  │ ⚡ ACTION: {step.action.action_type.value}")

        # Observation
        obs_preview = step.observation.content[:50]
        status = "✅" if step.observation.success else "❌"
        print(f"  │ 👁 OBSERVE: {status} {obs_preview}...")
        print(f"  └───────────────────────────────────────")

    # Final answer
    if agent.steps:
        print(f"\n  🎯 FINAL ANSWER: {agent.steps[-1].observation.content[:100]}...")


# ============================================================
# Main: Run all exercises
# ============================================================

if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║  EXERCISE 04: ReAct Pattern (Reasoning + Acting)          ║")
    print("║  Thought → Action → Observation Loop                       ║")
    print("╚" + "═" * 58 + "╝")

    exercises = [
        ("4.1", "Basic ReAct Loop", exercise_1_react_basics),
        ("4.2", "Execution Trace", exercise_2_react_tracing),
        ("4.3", "Custom Action Spaces", exercise_3_action_space),
        ("4.4", "Resilient Agent", exercise_4_resilient_agent),
        ("4.5", "Plan & Execute", exercise_5_plan_execute),
        ("4.6", "Multi-Tool ReAct", exercise_6_multi_tool),
        ("4.7", "ReAct Comparison", exercise_7_react_comparison),
        ("4.8", "Loop Visualization", exercise_8_react_visualization),
    ]

    for num, name, func in exercises:
        try:
            func()
        except Exception as e:
            print(f"\n  [ERROR in {num}: {name}] {e}")

    print("\n" + "=" * 60)
    print("  All exercises completed!")
    print("=" * 60)

    print("""
KEY TAKEAWAYS:
1. ReAct = Reasoning + Acting in a tight loop
2. Each step: THINK → ACTION → OBSERVE
3. Action spaces define what the agent can do
4. Error recovery adds resilience to the loop
5. Plan & Execute is a simpler variant for predictable tasks
6. Multi-tool agents can use several tools in parallel
7. Tracing and visualization help debug agent behavior
""")
