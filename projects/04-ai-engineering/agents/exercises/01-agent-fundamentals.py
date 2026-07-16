"""
=============================================================
EXERCISE 01: Agent Fundamentals
=============================================================
Topic: What is an AI Agent, Agent Architecture, and Core Loops

Learning Objectives:
- Understand what makes an AI agent different from a chatbot
- Implement the perceive-think-act loop
- Build agent state management
- Create a basic agent loop with LLM as reasoning engine
- Compare agent vs chatbot vs copilot patterns

Prerequisites:
- Python 3.10+
- openai library (pip install openai)
=============================================================
"""

import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
from datetime import datetime


# ============================================================
# SECTION 1: Core Concepts — Agent vs Chatbot vs Copilot
# ============================================================

class AgentType(Enum):
    """Classification of AI interaction patterns."""
    CHATBOT = "chatbot"       # Stateless Q&A, no autonomy
    COPILOT = "copilot"       # Suggests, user executes
    AGENT = "agent"           # Autonomous perceive-think-act


@dataclass
class InteractionPattern:
    """Describes the behavioral differences between AI patterns."""
    agent_type: AgentType
    autonomy_level: str       # "none", "partial", "full"
    statefulness: bool        # Does it remember context?
    tool_use: bool            # Can it call external tools?
    goal_oriented: bool       # Does it pursue multi-step goals?
    description: str

    def summary(self) -> str:
        return (
            f"[{self.agent_type.value.upper()}]\n"
            f"  Autonomy: {self.autonomy_level}\n"
            f"  Stateful: {self.statefulness}\n"
            f"  Tools:    {self.tool_use}\n"
            f"  Goals:    {self.goal_oriented}\n"
            f"  About:    {self.description}"
        )


# Define the three patterns
CHATBOT_PATTERN = InteractionPattern(
    agent_type=AgentType.CHATBOT,
    autonomy_level="none",
    statefulness=False,
    tool_use=False,
    goal_oriented=False,
    description="Responds to prompts with no memory or action capability."
)

COPILOT_PATTERN = InteractionPattern(
    agent_type=AgentType.COPILOT,
    autonomy_level="partial",
    statefulness=True,
    tool_use=True,
    goal_oriented=False,
    description="Suggests actions or completions; user decides and executes."
)

AGENT_PATTERN = InteractionPattern(
    agent_type=AgentType.AGENT,
    autonomy_level="full",
    statefulness=True,
    tool_use=True,
    goal_oriented=True,
    description="Autonomously perceives, reasons, and acts to achieve goals."
)


def compare_patterns():
    """Print comparison of all three AI interaction patterns."""
    print("=" * 60)
    print("  AI Interaction Patterns Comparison")
    print("=" * 60)
    for pattern in [CHATBOT_PATTERN, COPILOT_PATTERN, AGENT_PATTERN]:
        print(pattern.summary())
        print()


# ============================================================
# SECTION 2: Agent State Management
# ============================================================

class AgentState(Enum):
    """Possible states for an agent in its lifecycle."""
    IDLE = "idle"
    PERCEIVING = "perceiving"
    THINKING = "thinking"
    ACTING = "acting"
    WAITING = "waiting"
    ERROR = "error"
    DONE = "done"


@dataclass
class Message:
    """A single message in agent conversation history."""
    role: str               # "system", "user", "assistant", "tool"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class AgentMemory:
    """Manages agent's conversation history and context window."""
    messages: list[Message] = field(default_factory=list)
    max_messages: int = 50
    system_prompt: str = ""

    def add_message(self, role: str, content: str, metadata: dict = None):
        """Add a message to memory, evicting oldest if at capacity."""
        msg = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(msg)
        # Evict oldest non-system messages when over capacity
        if len(self.messages) > self.max_messages:
            non_system = [m for m in self.messages if m.role != "system"]
            if non_system:
                self.messages.remove(non_system[0])

    def get_context(self, last_n: int = 20) -> list[dict]:
        """Get formatted context for LLM, including system prompt."""
        context = []
        if self.system_prompt:
            context.append({"role": "system", "content": self.system_prompt})
        recent = self.messages[-last_n:]
        for msg in recent:
            context.append({"role": msg.role, "content": msg.content})
        return context

    def clear(self):
        """Clear all messages except system prompt."""
        self.messages = [m for m in self.messages if m.role == "system"]


@dataclass
class AgentContext:
    """Complete agent runtime context."""
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    state: AgentState = AgentState.IDLE
    memory: AgentMemory = field(default_factory=AgentMemory)
    metadata: dict = field(default_factory=dict)
    iteration: int = 0
    max_iterations: int = 10
    created_at: datetime = field(default_factory=datetime.now)

    def transition(self, new_state: AgentState):
        """Transition agent to a new state with validation."""
        valid_transitions = {
            AgentState.IDLE: [AgentState.PERCEIVING],
            AgentState.PERCEIVING: [AgentState.THINKING, AgentState.ERROR],
            AgentState.THINKING: [AgentState.ACTING, AgentState.DONE, AgentState.ERROR],
            AgentState.ACTING: [AgentState.WAITING, AgentState.THINKING, AgentState.DONE, AgentState.ERROR],
            AgentState.WAITING: [AgentState.PERCEIVING],
            AgentState.ERROR: [AgentState.IDLE],
            AgentState.DONE: [AgentState.IDLE],
        }
        allowed = valid_transitions.get(self.state, [])
        if new_state not in allowed:
            raise ValueError(
                f"Invalid transition: {self.state.value} -> {new_state.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )
        old_state = self.state
        self.state = new_state
        self.metadata["last_transition"] = {
            "from": old_state.value,
            "to": new_state.value,
            "time": datetime.now().isoformat(),
        }


# ============================================================
# SECTION 3: The Perceive-Think-Act Loop
# ============================================================

class Tool:
    """Base class for tools an agent can use."""

    def __init__(self, name: str, description: str, parameters: dict = None):
        self.name = name
        self.description = description
        self.parameters = parameters or {}

    def execute(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement execute()")

    def to_schema(self) -> dict:
        """Convert tool to OpenAI function-calling schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }


class CalculatorTool(Tool):
    """A calculator tool for mathematical operations."""

    def __init__(self):
        super().__init__(
            name="calculator",
            description="Evaluate a mathematical expression. Supports +, -, *, /, **, sqrt.",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate, e.g. '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            }
        )

    def execute(self, expression: str = "", **kwargs) -> str:
        """Evaluate a math expression safely."""
        import math
        allowed_names = {
            "sqrt": math.sqrt,
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
        }
        try:
            # Simple eval with restricted namespace
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return json.dumps({"result": result, "expression": expression})
        except Exception as e:
            return json.dumps({"error": str(e), "expression": expression})


class WebSearchTool(Tool):
    """Mock web search tool for demonstration."""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information on a topic.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    }
                },
                "required": ["query"]
            }
        )

    def execute(self, query: str = "", **kwargs) -> str:
        """Simulate a web search (returns mock data)."""
        mock_results = [
            {"title": f"Result about: {query}", "url": "https://example.com", "snippet": f"Information about {query}..."},
            {"title": f"Guide to: {query}", "url": "https://guide.example.com", "snippet": f"A comprehensive guide to {query}..."},
        ]
        return json.dumps({"results": mock_results, "query": query})


class TextAnalysisTool(Tool):
    """Analyze text for sentiment, word count, etc."""

    def __init__(self):
        super().__init__(
            name="analyze_text",
            description="Analyze text for word count, sentence count, and basic sentiment indicators.",
            parameters={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to analyze"}
                },
                "required": ["text"]
            }
        )

    def execute(self, text: str = "", **kwargs) -> str:
        """Analyze text and return statistics."""
        words = text.split()
        sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        positive_words = {"good", "great", "excellent", "happy", "love", "best", "amazing", "wonderful"}
        negative_words = {"bad", "terrible", "hate", "worst", "awful", "poor", "horrible", "sad"}
        pos_count = sum(1 for w in words if w.lower() in positive_words)
        neg_count = sum(1 for w in words if w.lower() in negative_words)

        sentiment = "neutral"
        if pos_count > neg_count:
            sentiment = "positive"
        elif neg_count > pos_count:
            sentiment = "negative"

        return json.dumps({
            "word_count": len(words),
            "sentence_count": len(sentences),
            "character_count": len(text),
            "sentiment": sentiment,
            "positive_indicators": pos_count,
            "negative_indicators": neg_count,
        })


# ============================================================
# SECTION 4: Complete Agent Loop Implementation
# ============================================================

class BaseAgent:
    """
    A complete agent implementation with the perceive-think-act loop.
    This is the core pattern for building AI agents.
    """

    def __init__(
        self,
        system_prompt: str = "",
        tools: list[Tool] = None,
        model: str = "gpt-4o-mini",
        max_iterations: int = 10,
    ):
        self.context = AgentContext(max_iterations=max_iterations)
        self.context.memory.system_prompt = system_prompt or self._default_system_prompt()
        self.tools = {tool.name: tool for tool in (tools or [])}
        self.model = model
        self._step_log: list[dict] = []

    @staticmethod
    def _default_system_prompt() -> str:
        return (
            "You are a helpful AI agent. You can use tools to accomplish tasks. "
            "Think step by step before acting. Always explain your reasoning."
        )

    def perceive(self, user_input: str) -> dict:
        """
        PERCEIVE: Process the user's input and environment.
        This is where the agent receives and parses signals.
        """
        self.context.transition(AgentState.PERCEIVING)
        perception = {
            "raw_input": user_input,
            "timestamp": datetime.now().isoformat(),
            "iteration": self.context.iteration,
            "available_tools": list(self.tools.keys()),
        }
        self.context.memory.add_message("user", user_input)
        return perception

    def think(self, perception: dict) -> dict:
        """
        THINK: Reason about what to do next.
        In a real agent, this calls the LLM. Here we simulate the reasoning.
        """
        self.context.transition(AgentState.THINKING)
        reasoning = {
            "analysis": f"Received input: {perception['raw_input']}",
            "plan": "Determine if tools are needed or respond directly.",
            "tool_needed": False,
            "tool_name": None,
            "tool_args": {},
            "response": None,
        }

        # Check if any tool keyword is present in the input
        user_input = perception["raw_input"].lower()
        if "calculate" in user_input or "compute" in user_input or "math" in user_input:
            reasoning["tool_needed"] = True
            reasoning["tool_name"] = "calculator"
            # Extract expression from input
            for word in perception["raw_input"].split():
                if any(c.isdigit() for c in word):
                    reasoning["tool_args"]["expression"] = word
            if not reasoning["tool_args"].get("expression"):
                reasoning["tool_args"]["expression"] = "0"
        elif "search" in user_input or "find" in user_input or "look up" in user_input:
            reasoning["tool_needed"] = True
            reasoning["tool_name"] = "web_search"
            reasoning["tool_args"]["query"] = perception["raw_input"]
        elif "analyze" in user_input or "count words" in user_input:
            reasoning["tool_needed"] = True
            reasoning["tool_name"] = "analyze_text"
            reasoning["tool_args"]["text"] = perception["raw_input"]
        else:
            reasoning["response"] = f"I understand: '{perception['raw_input']}'. How can I help you further?"

        return reasoning

    def act(self, reasoning: dict) -> str:
        """
        ACT: Execute the decided action (tool call or direct response).
        """
        self.context.transition(AgentState.ACTING)

        if reasoning["tool_needed"] and reasoning["tool_name"]:
            tool_name = reasoning["tool_name"]
            if tool_name in self.tools:
                result = self.tools[tool_name].execute(**reasoning["tool_args"])
                response = f"Tool '{tool_name}' result: {result}"
                self.context.memory.add_message(
                    "assistant",
                    f"Called {tool_name} with {reasoning['tool_args']}",
                    metadata={"tool": tool_name, "result": result}
                )
            else:
                response = f"Tool '{tool_name}' not found in my toolkit."
        else:
            response = reasoning.get("response", "I'm not sure how to help with that.")

        self.context.memory.add_message("assistant", response)
        return response

    def run(self, user_input: str) -> str:
        """
        RUN: Execute the full perceive-think-act loop.
        This is the main entry point for agent interaction.
        """
        self.context.iteration += 1
        print(f"\n--- Agent Loop Iteration {self.context.iteration} ---")

        try:
            # Step 1: Perceive
            print(f"[PERCEIVE] Processing input...")
            perception = self.perceive(user_input)
            print(f"  Input: {perception['raw_input'][:80]}...")

            # Step 2: Think
            print(f"[THINK] Reasoning about action...")
            reasoning = self.think(perception)
            if reasoning["tool_needed"]:
                print(f"  Decision: Use tool '{reasoning['tool_name']}'")
            else:
                print(f"  Decision: Respond directly")

            # Step 3: Act
            print(f"[ACT] Executing...")
            response = self.act(reasoning)
            print(f"  Response: {response[:100]}...")

            self.context.transition(AgentState.DONE)
            self._log_step(user_input, reasoning, response)
            return response

        except Exception as e:
            self.context.transition(AgentState.ERROR)
            error_msg = f"Agent error: {str(e)}"
            print(f"  ERROR: {error_msg}")
            return error_msg

    def _log_step(self, user_input: str, reasoning: dict, response: str):
        """Log the step for debugging and analysis."""
        self._step_log.append({
            "iteration": self.context.iteration,
            "input": user_input,
            "reasoning": reasoning,
            "response": response,
            "state": self.context.state.value,
            "timestamp": datetime.now().isoformat(),
        })

    def get_history(self) -> list[dict]:
        """Get the full interaction history."""
        return [msg.to_dict() for msg in self.context.memory.messages]


# ============================================================
# SECTION 5: Advanced — Self-Reflecting Agent
# ============================================================

class SelfReflectingAgent(BaseAgent):
    """
    An agent that reflects on its own outputs and iterates.
    Adds self-evaluation and improvement to the basic loop.
    """

    def __init__(self, *args, max_reflections: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_reflections = max_reflections
        self.reflections: list[dict] = []

    def reflect(self, response: str, original_input: str) -> dict:
        """
        REFLECT: Evaluate the quality of the agent's own response.
        Returns reflection with score and improvement suggestions.
        """
        # Simple heuristic reflection (in production, use LLM for this)
        word_count = len(response.split())
        has_tool_result = "Tool" in response or "result" in response
        is_substantive = word_count > 10

        reflection = {
            "score": 0,
            "feedback": "",
            "improvements": [],
            "should_retry": False,
        }

        if is_substantive:
            reflection["score"] += 1
        else:
            reflection["improvements"].append("Response is too short, add more detail.")

        if has_tool_result:
            reflection["score"] += 1
        else:
            reflection["improvements"].append("Consider using tools for more accurate information.")

        if len(response) > 50:
            reflection["score"] += 1
        else:
            reflection["improvements"].append("Response lacks detail.")

        # Determine if retry is needed
        if reflection["score"] < 2 and len(self.reflections) < self.max_reflections:
            reflection["should_retry"] = True
            reflection["feedback"] = "Response could be improved. Retrying..."
        else:
            reflection["feedback"] = "Response meets quality threshold."

        return reflection

    def run_with_reflection(self, user_input: str) -> str:
        """Run with self-reflection loop for quality assurance."""
        self.reflections = []
        best_response = ""
        best_score = -1

        for attempt in range(self.max_reflections + 1):
            print(f"\n{'='*40}")
            print(f"  Attempt {attempt + 1}/{self.max_reflections + 1}")
            print(f"{'='*40}")

            response = self.run(user_input)
            reflection = self.reflect(response, user_input)
            self.reflections.append(reflection)

            print(f"  Reflection Score: {reflection['score']}/3")
            print(f"  Feedback: {reflection['feedback']}")

            if reflection["score"] > best_score:
                best_score = reflection["score"]
                best_response = response

            if not reflection["should_retry"]:
                break

            print(f"  Improvements needed:")
            for imp in reflection["improvements"]:
                print(f"    - {imp}")

        return best_response


# ============================================================
# SECTION 6: Running the Exercises
# ============================================================

def exercise_1_pattern_comparison():
    """Exercise 1.1: Compare agent interaction patterns."""
    print("\n" + "=" * 60)
    print("EXERCISE 1.1: AI Interaction Pattern Comparison")
    print("=" * 60)
    compare_patterns()


def exercise_2_state_management():
    """Exercise 1.2: Agent state management and transitions."""
    print("\n" + "=" * 60)
    print("EXERCISE 1.2: Agent State Management")
    print("=" * 60)

    ctx = AgentContext()
    print(f"Initial state: {ctx.state.value}")

    transitions = [
        AgentState.PERCEIVING,
        AgentState.THINKING,
        AgentState.ACTING,
        AgentState.WAITING,
        AgentState.PERCEIVING,
        AgentState.THINKING,
        AgentState.DONE,
    ]

    for target in transitions:
        try:
            ctx.transition(target)
            print(f"  Transitioned to: {ctx.state.value}")
        except ValueError as e:
            print(f"  BLOCKED: {e}")

    print(f"\nFinal state: {ctx.state.value}")
    print(f"Transition log: {json.dumps(ctx.metadata.get('last_transition', {}), indent=2)}")


def exercise_3_memory_management():
    """Exercise 1.3: Agent memory and context management."""
    print("\n" + "=" * 60)
    print("EXERCISE 1.3: Agent Memory Management")
    print("=" * 60)

    memory = AgentMemory(system_prompt="You are a helpful assistant.", max_messages=5)
    print(f"System prompt: {memory.system_prompt}")

    # Add messages
    test_messages = [
        ("user", "Hello!"),
        ("assistant", "Hi there! How can I help?"),
        ("user", "What's 2+2?"),
        ("assistant", "2+2 equals 4."),
        ("user", "What about 5*5?"),
        ("assistant", "5*5 equals 25."),
        ("user", "Thanks!"),
    ]

    for role, content in test_messages:
        memory.add_message(role, content)
        print(f"  Added [{role}]: {content[:40]}")

    print(f"\nTotal messages: {len(memory.messages)}")
    print(f"\nContext window (last 5):")
    for msg in memory.get_context(last_n=5):
        print(f"  [{msg['role']}]: {msg['content'][:50]}")


def exercise_4_basic_agent():
    """Exercise 1.4: Build and run a basic agent."""
    print("\n" + "=" * 60)
    print("EXERCISE 1.4: Basic Agent Loop (Perceive-Think-Act)")
    print("=" * 60)

    agent = BaseAgent(
        system_prompt="You are a helpful assistant with access to calculation, search, and analysis tools.",
        tools=[CalculatorTool(), WebSearchTool(), TextAnalysisTool()],
        max_iterations=5,
    )

    # Test cases
    test_inputs = [
        "Calculate 42 * 17",
        "Search for Python tutorials",
        "Analyze this text: The quick brown fox jumps over the lazy dog",
        "Tell me about agents",
    ]

    for user_input in test_inputs:
        response = agent.run(user_input)
        print(f"\n  User: {user_input}")
        print(f"  Agent: {response[:120]}...")

    print(f"\nInteraction history ({len(agent.get_history())} messages):")
    for msg in agent.get_history():
        print(f"  [{msg['role']}]: {msg['content'][:60]}")


def exercise_5_self_reflecting_agent():
    """Exercise 1.5: Self-reflecting agent with quality loop."""
    print("\n" + "=" * 60)
    print("EXERCISE 1.5: Self-Reflecting Agent")
    print("=" * 60)

    agent = SelfReflectingAgent(
        system_prompt="You are a reflective assistant that improves its responses.",
        tools=[CalculatorTool(), WebSearchTool()],
        max_iterations=5,
        max_reflections=2,
    )

    response = agent.run_with_reflection("Calculate 15 + 27")
    print(f"\nFinal response: {response}")

    print(f"\nReflection history:")
    for i, ref in enumerate(agent.reflections):
        print(f"  Reflection {i+1}: score={ref['score']}/3, retry={ref['should_retry']}")


def exercise_6_tool_registry():
    """Exercise 1.6: Tool registry and management."""
    print("\n" + "=" * 60)
    print("EXERCISE 1.6: Tool Registry Pattern")
    print("=" * 60)

    # Create a tool registry
    registry = {}

    def register_tool(tool: Tool):
        """Register a tool in the global registry."""
        registry[tool.name] = tool
        print(f"  Registered tool: {tool.name}")

    def list_tools() -> list[dict]:
        """List all registered tools with their schemas."""
        tools_info = []
        for name, tool in registry.items():
            tools_info.append({
                "name": name,
                "description": tool.description,
                "parameters": tool.parameters,
            })
        return tools_info

    def execute_tool(name: str, **kwargs) -> str:
        """Execute a registered tool by name."""
        if name not in registry:
            return json.dumps({"error": f"Tool '{name}' not found"})
        return registry[name].execute(**kwargs)

    # Register tools
    register_tool(CalculatorTool())
    register_tool(WebSearchTool())
    register_tool(TextAnalysisTool())

    print(f"\nRegistered tools: {list(registry.keys())}")

    # List tool schemas
    print("\nTool Schemas:")
    for tool_info in list_tools():
        print(f"  {tool_info['name']}: {tool_info['description'][:50]}...")

    # Execute tools
    print("\nTool Execution:")
    result = execute_tool("calculator", expression="100 / 7")
    print(f"  calculator(100/7) = {result}")

    result = execute_tool("web_search", query="AI agents")
    parsed = json.loads(result)
    print(f"  web_search('AI agents') = {len(parsed['results'])} results")

    result = execute_tool("analyze_text", text="This is a great example of amazing code!")
    parsed = json.loads(result)
    print(f"  analyze_text(...) = {parsed}")


# ============================================================
# Main: Run all exercises
# ============================================================

if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║  EXERCISE 01: AI Agent Fundamentals                     ║")
    print("║  Perceive-Think-Act Loop, State Management, Memory       ║")
    print("╚" + "═" * 58 + "╝")

    exercises = [
        ("1.1", "Pattern Comparison", exercise_1_pattern_comparison),
        ("1.2", "State Management", exercise_2_state_management),
        ("1.3", "Memory Management", exercise_3_memory_management),
        ("1.4", "Basic Agent Loop", exercise_4_basic_agent),
        ("1.5", "Self-Reflecting Agent", exercise_5_self_reflecting_agent),
        ("1.6", "Tool Registry", exercise_6_tool_registry),
    ]

    for num, name, func in exercises:
        try:
            func()
        except Exception as e:
            print(f"\n  [ERROR in {num}: {name}] {e}")

    print("\n" + "=" * 60)
    print("  All exercises completed!")
    print("=" * 60)

    # Key takeaways
    print("""
KEY TAKEAWAYS:
1. Agents perceive their environment, think about what to do, then act
2. State management is critical — agents must track their lifecycle
3. Memory lets agents maintain context across interactions
4. The tool registry pattern enables extensible agent capabilities
5. Self-reflection improves response quality through iterative refinement
6. Agent > Copilot > Chatbot in terms of autonomy and capability
""")
