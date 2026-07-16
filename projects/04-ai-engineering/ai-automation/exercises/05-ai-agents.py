"""
Exercise 05: AI Agents
========================
Master AI agent patterns: ReAct reasoning, tool calling, agent memory,
planning, and multi-agent orchestration.

Prerequisites:
    pip install openai python-dotenv pydantic

Environment Variables (.env):
    OPENAI_API_KEY=sk-...
"""

import os
import json
import time
import re
from dataclasses import dataclass, field
from typing import Any, Callable
from enum import Enum


# ---------------------------------------------------------------------------
# 1. Agent Configuration
# ---------------------------------------------------------------------------

@dataclass
class AgentConfig:
    """Configuration for an AI agent."""
    name: str = "Agent"
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2048
    max_iterations: int = 10
    system_prompt: str = ""


# ---------------------------------------------------------------------------
# 2. Tool System
# ---------------------------------------------------------------------------

@dataclass
class Tool:
    """A tool that an agent can use."""
    name: str
    description: str
    parameters: dict[str, Any]
    function: Callable

    def to_schema(self) -> dict:
        """Convert to OpenAI function calling schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def execute(self, **kwargs) -> str:
        """Execute the tool with given arguments."""
        try:
            result = self.function(**kwargs)
            return str(result)
        except Exception as e:
            return f"Error: {e}"


class ToolRegistry:
    """Registry of available tools for agents."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def to_schemas(self) -> list[dict]:
        return [t.to_schema() for t in self._tools.values()]

    def execute(self, name: str, **kwargs) -> str:
        tool = self.get(name)
        if tool is None:
            return f"Error: Tool '{name}' not found"
        return tool.execute(**kwargs)


# ---------------------------------------------------------------------------
# 3. Agent Memory
# ---------------------------------------------------------------------------

@dataclass
class MemoryEntry:
    """A single memory entry."""
    content: str
    timestamp: float
    entry_type: str  # "observation", "thought", "action", "result"
    metadata: dict = field(default_factory=dict)


class AgentMemory:
    """Memory system for AI agents with short-term and long-term storage."""

    def __init__(self, max_short_term: int = 20):
        self.short_term: list[MemoryEntry] = []
        self.long_term: list[MemoryEntry] = []
        self.max_short_term = max_short_term

    def add(self, content: str, entry_type: str = "observation", **metadata):
        """Add an entry to short-term memory."""
        entry = MemoryEntry(
            content=content,
            timestamp=time.time(),
            entry_type=entry_type,
            metadata=metadata,
        )
        self.short_term.append(entry)

        # If short-term is full, summarize oldest entries into long-term
        if len(self.short_term) > self.max_short_term:
            self._consolidate()

    def get_context(self, n: int = 10) -> str:
        """Get recent memory as context string."""
        recent = self.short_term[-n:]
        lines = []
        for entry in recent:
            prefix = entry.entry_type.upper()
            lines.append(f"[{prefix}] {entry.content}")
        return "\n".join(lines)

    def search(self, query: str, n: int = 5) -> list[MemoryEntry]:
        """Search memory for relevant entries."""
        query_terms = set(query.lower().split())

        scored = []
        for entry in self.short_term + self.long_term:
            entry_terms = set(entry.content.lower().split())
            overlap = len(query_terms & entry_terms)
            if overlap > 0:
                scored.append((overlap, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scored[:n]]

    def _consolidate(self):
        """Move old short-term entries to long-term memory."""
        # Keep the most recent entries in short-term
        to_move = self.short_term[:5]
        self.short_term = self.short_term[5:]
        self.long_term.extend(to_move)

        # Keep long-term manageable
        if len(self.long_term) > 100:
            self.long_term = self.long_term[-100:]

    def summary(self) -> dict:
        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term),
        }


# ---------------------------------------------------------------------------
# 4. ReAct Agent Pattern
# ---------------------------------------------------------------------------

class ReActAgent:
    """
    ReAct (Reasoning + Acting) agent pattern.
    
    The agent follows a Thought → Action → Observation loop:
    1. Thought: Reason about what to do
    2. Action: Choose and execute a tool
    3. Observation: Process the result
    4. Repeat until done
    """

    def __init__(self, config: AgentConfig, tools: ToolRegistry):
        self.config = config
        self.tools = tools
        self.memory = AgentMemory()
        self._iteration = 0

    def _build_system_prompt(self) -> str:
        tool_descriptions = "\n".join(
            f"- {t.name}: {t.description}" for t in self.tools.list_tools()
        )

        return f"""You are {self.config.name}, an AI assistant that solves problems step by step.

You have access to these tools:
{tool_descriptions}

To use a tool, respond with:
Thought: [your reasoning about what to do next]
Action: tool_name
Action Input: {{"param": "value"}}

When you have the final answer, respond with:
Thought: I now have enough information to answer.
Final Answer: [your answer]

IMPORTANT: Always start with a Thought. Only use one tool per step.
If you don't need a tool, go directly to Final Answer."""

    def _parse_action(self, response: str) -> tuple[str, dict] | None:
        """Parse action from LLM response."""
        action_match = re.search(r"Action:\s*(\w+)", response)
        input_match = re.search(r"Action Input:\s*(\{.*?\})", response, re.DOTALL)

        if action_match:
            tool_name = action_match.group(1)
            try:
                args = json.loads(input_match.group(1)) if input_match else {}
            except json.JSONDecodeError:
                args = {}
            return tool_name, args
        return None

    def _llm_call(self, messages: list[dict]) -> str:
        """Make an LLM API call."""
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            messages=messages,
        )
        return response.choices[0].message.content or ""

    def run(self, task: str) -> str:
        """Execute a task using the ReAct loop."""
        self.memory.add(task, entry_type="task")
        self._iteration = 0

        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Task: {task}"},
        ]

        while self._iteration < self.config.max_iterations:
            self._iteration += 1

            # Get LLM response
            response = self._llm_call(messages)
            self.memory.add(response, entry_type="thought")
            messages.append({"role": "assistant", "content": response})

            # Check for final answer
            final_match = re.search(r"Final Answer:\s*(.*?)(?:\n|$)", response, re.DOTALL)
            if final_match:
                answer = final_match.group(1).strip()
                self.memory.add(answer, entry_type="answer")
                return answer

            # Parse and execute action
            action = self._parse_action(response)
            if action is None:
                # No action found, ask LLM to provide final answer
                messages.append({
                    "role": "user",
                    "content": "Please provide your Final Answer now.",
                })
                continue

            tool_name, args = action
            self.memory.add(f"Using tool: {tool_name} with {args}", entry_type="action")

            # Execute tool
            result = self.tools.execute(tool_name, **args)
            self.memory.add(f"Result: {result}", entry_type="result")

            messages.append({
                "role": "user",
                "content": f"Observation: {result}\n\nWhat should you do next?",
            })

        return "Max iterations reached without completing the task."


# ---------------------------------------------------------------------------
# 5. Tool-Calling Agent (Modern Pattern)
# ---------------------------------------------------------------------------

class ToolCallingAgent:
    """
    Modern tool-coding agent using OpenAI's function calling.
    
    More reliable than ReAct for structured tool use because
    the LLM outputs structured JSON for tool calls.
    """

    def __init__(self, config: AgentConfig, tools: ToolRegistry):
        self.config = config
        self.tools = tools
        self.memory = AgentMemory()

    def run(self, task: str) -> str:
        """Execute a task using tool calling."""
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        messages = [
            {"role": "system", "content": self.config.system_prompt or f"You are {self.config.name}."},
            {"role": "user", "content": task},
        ]

        schemas = self.tools.to_schemas()

        for iteration in range(self.config.max_iterations):
            response = client.chat.completions.create(
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                messages=messages,
                tools=schemas if schemas else None,
                tool_choice="auto" if schemas else None,
            )

            choice = response.choices[0]

            # If no tool call, return the response
            if not choice.message.tool_calls:
                answer = choice.message.content or ""
                self.memory.add(answer, entry_type="answer")
                return answer

            # Process tool calls
            messages.append(choice.message)

            for tool_call in choice.message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                self.memory.add(f"Calling {tool_name}({args})", entry_type="action")
                result = self.tools.execute(tool_name, **args)
                self.memory.add(f"Result: {result}", entry_type="result")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        return "Max iterations reached."


# ---------------------------------------------------------------------------
# 6. Planning Agent
# ---------------------------------------------------------------------------

class PlanningAgent:
    """
    Agent that creates a plan before execution.
    
    Workflow:
    1. Analyze the task
    2. Create a step-by-step plan
    3. Execute each step
    4. Replan if needed
    """

    def __init__(self, config: AgentConfig, tools: ToolRegistry):
        self.config = config
        self.tools = tools
        self.memory = AgentMemory()

    def _create_plan(self, task: str) -> list[str]:
        """Create a plan for the task."""
        tool_list = "\n".join(f"- {t.name}: {t.description}" for t in self.tools.list_tools())

        prompt = f"""Create a step-by-step plan to complete this task.

Task: {task}

Available tools:
{tool_list}

Return ONLY a JSON array of step descriptions. Example:
["Step 1 description", "Step 2 description"]

Plan:"""

        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model=self.config.model,
            temperature=0.3,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content or "[]"
        # Extract JSON array
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if match:
            return json.loads(match.group())
        return [task]

    def _execute_step(self, step: str, context: str) -> str:
        """Execute a single step using available tools."""
        tool_descriptions = "\n".join(
            f"- {t.name}: {t.description}" for t in self.tools.list_tools()
        )

        prompt = f"""Execute this step. Use a tool if needed.

Step: {step}

Previous context:
{context}

Available tools:
{tool_descriptions}

To use a tool, respond with:
Action: tool_name
Action Input: {{"param": "value"}}

If no tool is needed, provide the result directly.

Response:"""

        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content or ""

        # Check for tool call
        action_match = re.search(r"Action:\s*(\w+)", content)
        input_match = re.search(r"Action Input:\s*(\{.*?\})", content, re.DOTALL)

        if action_match:
            tool_name = action_match.group(1)
            try:
                args = json.loads(input_match.group(1)) if input_match else {}
            except json.JSONDecodeError:
                args = {}
            result = self.tools.execute(tool_name, **args)
            return f"[Used {tool_name}] {result}"

        return content

    def run(self, task: str) -> dict:
        """Execute a task with planning."""
        # Create plan
        steps = self._create_plan(task)
        self.memory.add(f"Plan created: {len(steps)} steps", entry_type="plan")

        results = []
        context = f"Task: {task}\n"

        for i, step in enumerate(steps, 1):
            self.memory.add(f"Executing step {i}: {step}", entry_type="action")
            result = self._execute_step(step, context)
            results.append({"step": i, "description": step, "result": result})
            context += f"\nStep {i} result: {result}"

        return {
            "task": task,
            "plan": steps,
            "results": results,
            "completed": len(results) == len(steps),
        }


# ---------------------------------------------------------------------------
# 7. Multi-Agent System
# ---------------------------------------------------------------------------

class AgentRole(Enum):
    PLANNER = "planner"
    EXECUTOR = "executor"
    CRITIC = "critic"
    COORDINATOR = "coordinator"


@dataclass
class AgentMessage:
    """Message between agents."""
    sender: str
    receiver: str
    content: str
    message_type: str = "task"  # task, result, feedback


class MultiAgentSystem:
    """
    Orchestrate multiple specialized agents.
    
    Architecture:
    - Coordinator: Routes tasks and manages workflow
    - Planner: Creates execution plans
    - Executor: Performs tasks using tools
    - Critic: Reviews and validates outputs
    """

    def __init__(self):
        self.agents: dict[str, ReActAgent] = {}
        self.message_queue: list[AgentMessage] = []

    def add_agent(self, name: str, role: AgentRole, tools: ToolRegistry | None = None):
        """Add a specialized agent."""
        prompts = {
            AgentRole.COORDINATOR: "You are a coordinator who routes tasks to the right agent.",
            AgentRole.PLANNER: "You are a planner who creates step-by-step execution plans.",
            AgentRole.EXECUTOR: "You are an executor who carries out specific tasks.",
            AgentRole.CRITIC: "You are a critic who reviews work for quality and correctness.",
        }

        config = AgentConfig(
            name=name,
            system_prompt=prompts.get(role, ""),
            temperature=0.5,
        )

        agent = ReActAgent(config, tools or ToolRegistry())
        self.agents[name] = agent

    def send_message(self, sender: str, receiver: str, content: str,
                     msg_type: str = "task"):
        """Send a message between agents."""
        msg = AgentMessage(sender=sender, receiver=receiver,
                          content=content, message_type=msg_type)
        self.message_queue.append(msg)

    def get_messages(self, receiver: str) -> list[AgentMessage]:
        """Get messages for a specific agent."""
        return [m for m in self.message_queue if m.receiver == receiver]

    def coordinate(self, task: str) -> dict:
        """Coordinate agents to complete a task."""
        results = {}

        # Step 1: Coordinator analyzes the task
        coordinator = self.agents.get("coordinator")
        if coordinator:
            analysis = coordinator.run(f"Analyze this task and break it into subtasks: {task}")
            results["analysis"] = analysis

        # Step 2: Planner creates a plan
        planner = self.agents.get("planner")
        if planner:
            plan = planner.run(f"Create a plan for: {task}")
            results["plan"] = plan

        # Step 3: Executor carries out the plan
        executor = self.agents.get("executor")
        if executor:
            execution = executor.run(f"Execute this task: {task}")
            results["execution"] = execution

        # Step 4: Critic reviews the output
        critic = self.agents.get("critic")
        if critic and "execution" in results:
            review = critic.run(
                f"Review this work for quality and correctness:\n{results['execution']}"
            )
            results["review"] = review

        return results


# ---------------------------------------------------------------------------
# 8. Built-in Tools
# ---------------------------------------------------------------------------

def create_default_tools() -> ToolRegistry:
    """Create a registry with common tools."""
    registry = ToolRegistry()

    def calculator(expression: str) -> str:
        """Evaluate a mathematical expression safely."""
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    def search_knowledge(query: str) -> str:
        """Search a knowledge base."""
        knowledge = {
            "python": "Python is a high-level programming language.",
            "rag": "RAG combines retrieval and generation.",
            "embedding": "Embeddings are vector representations of text.",
            "agent": "AI agents use tools and reasoning to complete tasks.",
        }
        results = []
        for key, value in knowledge.items():
            if key in query.lower():
                results.append(value)
        return "\n".join(results) if results else "No relevant information found."

    def web_search(query: str) -> str:
        """Search the web (simulated)."""
        return f"Search results for '{query}': [Simulated] Found relevant information about {query}."

    def code_executor(code: str) -> str:
        """Execute Python code in a sandbox."""
        try:
            # WARNING: In production, use a proper sandbox
            local_vars = {}
            exec(code, {"__builtins__": {}}, local_vars)
            return str(local_vars.get("result", "Code executed successfully"))
        except Exception as e:
            return f"Error: {e}"

    registry.register(Tool(
        name="calculator",
        description="Evaluate mathematical expressions. Input should be a valid math expression.",
        parameters={
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate"}
            },
            "required": ["expression"],
        },
        function=calculator,
    ))

    registry.register(Tool(
        name="search_knowledge",
        description="Search a knowledge base for information.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"],
        },
        function=search_knowledge,
    ))

    registry.register(Tool(
        name="web_search",
        description="Search the web for information.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"],
        },
        function=web_search,
    ))

    registry.register(Tool(
        name="code_executor",
        description="Execute Python code. Set a 'result' variable for the output.",
        parameters={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute"}
            },
            "required": ["code"],
        },
        function=code_executor,
    ))

    return registry


# ---------------------------------------------------------------------------
# 9. Demo Functions
# ---------------------------------------------------------------------------

def demo_tool_registry():
    """Demo: Creating and using tools."""
    print("=" * 60)
    print("DEMO 1: Tool Registry")
    print("=" * 60)

    registry = create_default_tools()

    print("Available tools:")
    for tool in registry.list_tools():
        print(f"  - {tool.name}: {tool.description}")

    # Direct tool execution
    print("\nDirect execution:")
    result = registry.execute("calculator", expression="2 + 3 * 4")
    print(f"  calculator(2 + 3 * 4) = {result}")

    result = registry.execute("search_knowledge", query="python")
    print(f"  search_knowledge(python) = {result}")

    result = registry.execute("web_search", query="latest AI news")
    print(f"  web_search(latest AI news) = {result[:80]}...")


def demo_agent_memory():
    """Demo: Agent memory system."""
    print("\n" + "=" * 60)
    print("DEMO 2: Agent Memory")
    print("=" * 60)

    memory = AgentMemory(max_short_term=5)

    # Add some entries
    entries = [
        ("User asked about RAG systems", "observation"),
        ("RAG combines retrieval and generation", "thought"),
        ("Searching for RAG documentation", "action"),
        ("Found 3 relevant documents", "result"),
        ("User asked about vector databases", "observation"),
        ("Vector DBs store embeddings for similarity search", "thought"),
    ]

    for content, entry_type in entries:
        memory.add(content, entry_type=entry_type)
        print(f"  Added [{entry_type}] {content[:50]}...")

    print(f"\nMemory stats: {memory.summary()}")
    print(f"\nContext:\n{memory.get_context(5)}")


def demo_react_agent():
    """Demo: ReAct agent pattern."""
    print("\n" + "=" * 60)
    print("DEMO 3: ReAct Agent")
    print("=" * 60)

    tools = create_default_tools()
    config = AgentConfig(
        name="Math Assistant",
        model="gpt-4o-mini",
        system_prompt="You are a helpful math assistant that uses tools to solve problems.",
    )

    agent = ReActAgent(config, tools)

    # This would work with an API key
    # result = agent.run("What is 15 * 23 + 47?")
    # print(f"Result: {result}")

    # Demo without API key
    print("ReAct Agent configured with tools:")
    print(f"  Name: {config.name}")
    print(f"  Model: {config.model}")
    print(f"  Tools: {[t.name for t in tools.list_tools()]}")
    print(f"  Max iterations: {config.max_iterations}")
    print("\nTo run: Uncomment the agent.run() call above (requires API key)")


def demo_tool_calling_agent():
    """Demo: Modern tool-calling agent."""
    print("\n" + "=" * 60)
    print("DEMO 4: Tool-Calling Agent")
    print("=" * 60)

    tools = create_default_tools()
    config = AgentConfig(
        name="Research Assistant",
        model="gpt-4o-mini",
        system_prompt="You are a research assistant. Use tools to find and process information.",
    )

    agent = ToolCallingAgent(config, tools)

    print("Tool-Calling Agent configured:")
    print(f"  Name: {config.name}")
    print(f"  Model: {config.model}")
    print(f"  Tools: {[t.name for t in tools.list_tools()]}")

    # Demo function calling schema
    print("\nTool schemas for OpenAI function calling:")
    for schema in tools.to_schemas():
        print(f"  {json.dumps(schema, indent=2)[:200]}...")


def demo_planning_agent():
    """Demo: Planning agent."""
    print("\n" + "=" * 60)
    print("DEMO 5: Planning Agent")
    print("=" * 60)

    tools = create_default_tools()
    config = AgentConfig(name="Planner", model="gpt-4o-mini")

    agent = PlanningAgent(config, tools)

    print("Planning Agent configured:")
    print(f"  Capabilities:")
    print(f"    1. Analyze task")
    print(f"    2. Create step-by-step plan")
    print(f"    3. Execute each step with tools")
    print(f"    4. Track results")

    # Simulated plan
    simulated_plan = {
        "task": "Calculate the average of numbers from 1 to 100",
        "plan": [
            "Calculate sum of 1 to 100",
            "Divide by 100 to get average",
            "Verify the result",
        ],
        "results": [
            {"step": 1, "description": "Calculate sum", "result": "[Used calculator] 5050"},
            {"step": 2, "description": "Calculate average", "result": "[Used calculator] 50.5"},
            {"step": 3, "description": "Verify", "result": "Average of 1-100 is 50.5"},
        ],
        "completed": True,
    }

    print(f"\nExample plan execution:")
    print(f"Task: {simulated_plan['task']}")
    for step in simulated_plan['results']:
        print(f"  Step {step['step']}: {step['result']}")


def demo_multi_agent():
    """Demo: Multi-agent system."""
    print("\n" + "=" * 60)
    print("DEMO 6: Multi-Agent System")
    print("=" * 60)

    system = MultiAgentSystem()

    # Add agents
    system.add_agent("coordinator", AgentRole.COORDINATOR)
    system.add_agent("planner", AgentRole.PLANNER)
    system.add_agent("executor", AgentRole.EXECUTOR)
    system.add_agent("critic", AgentRole.CRITIC)

    print("Multi-Agent System:")
    print(f"  Agents: {list(system.agents.keys())}")
    print(f"  Roles: coordinator, planner, executor, critic")

    # Simulated workflow
    print("\nSimulated workflow:")
    print("  1. Coordinator receives: 'Build a RAG chatbot'")
    print("  2. Coordinator -> Planner: 'Create execution plan'")
    print("  3. Planner -> Coordinator: 'Plan with 4 steps'")
    print("  4. Coordinator -> Executor: 'Execute step 1'")
    print("  5. Executor -> Coordinator: 'Step 1 complete'")
    print("  6. Coordinator -> Critic: 'Review output'")
    print("  7. Critic -> Coordinator: 'Looks good!'")
    print("  8. Coordinator returns final result")

    # Message passing demo
    system.send_message("coordinator", "planner", "Plan this task: Build a chatbot")
    system.send_message("planner", "coordinator", "Step 1: Set up env, Step 2: Build UI")
    system.send_message("coordinator", "executor", "Execute: Set up environment")

    print(f"\nMessages in queue: {len(system.message_queue)}")
    for msg in system.message_queue:
        print(f"  {msg.sender} -> {msg.receiver}: {msg.content[:50]}...")


# ---------------------------------------------------------------------------
# 10. Main Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("AI Agents Exercises")
    print("=" * 60)
    print()

    # Run demos (all work without API keys)
    demo_tool_registry()
    demo_agent_memory()
    demo_react_agent()
    demo_tool_calling_agent()
    demo_planning_agent()
    demo_multi_agent()

    print("\n" + "=" * 60)
    print("All demos complete!")
    print("=" * 60)
    print("\nTo run agents with LLM calls, uncomment the agent.run() calls")
    print("and set your OPENAI_API_KEY environment variable.")
