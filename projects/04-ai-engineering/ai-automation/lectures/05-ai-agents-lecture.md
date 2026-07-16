# Lecture 05: AI Agents

## Topic Overview

AI agents are autonomous systems that can perceive their environment, make decisions, and take actions to achieve goals. Unlike simple chatbots, agents can use tools, maintain memory, plan multi-step tasks, and adapt to new information. This lecture covers agent architectures, tool integration, planning strategies, and how to build production-ready autonomous systems.

**Duration:** 4-5 hours  
**Difficulty:** Advanced  
**Prerequisites:** Lecture 01-04 (LLM API, Prompt Engineering, Embeddings, RAG)

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** what makes an AI agent different from a chatbot
2. **Design** agent architectures (ReAct, Plan-and-Execute, etc.)
3. **Implement** tool use and function calling
4. **Build** memory systems for agents
5. **Create** planning and reasoning capabilities
6. **Handle** error recovery and graceful degradation
7. **Evaluate** agent performance and reliability
8. **Build** safe, controllable autonomous systems

---

## Key Concepts

### 1. What is an AI Agent?

An AI agent is an autonomous system that:
- **Perceives** its environment through observations
- **Reasons** about what to do next
- **Acts** using tools and capabilities
- **Learns** from feedback and experience

```
┌─────────────────────────────────────────────────────────┐
│                    AI AGENT ARCHITECTURE                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  LLM (Brain)                    │   │
│  │  - Reasoning                                    │   │
│  │  - Planning                                     │   │
│  │  - Decision making                              │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│            ┌────────────┼────────────┐                 │
│            ▼            ▼            ▼                 │
│     ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│     │  Memory  │  │  Tools   │  │   Loop   │         │
│     │          │  │          │  │          │         │
│     │ - Short  │  │ - APIs   │  │ - Observe│         │
│     │ - Long   │  │ - Code   │  │ - Think  │         │
│     │ - Vector │  │ - Search │  │ - Act    │         │
│     └──────────┘  └──────────┘  └──────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2. Agent vs Chatbot

| Feature | Chatbot | Agent |
|---------|---------|-------|
| Interaction | Single turn | Multi-turn |
| Capabilities | Text generation | Tools, memory, planning |
| Autonomy | User-driven | Goal-driven |
| State | Stateless | Stateful |
| Complexity | Simple | Complex |

### 3. Agent Architectures

#### ReAct (Reasoning + Acting)

The most common agent pattern:

```python
class ReActAgent:
    """Agent that reasons and acts in an loop."""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.memory = []
    
    def run(self, goal: str, max_steps: int = 10):
        """Execute a goal through reasoning and acting."""
        
        self.memory.append({"role": "user", "content": goal})
        
        for step in range(max_steps):
            # Generate next action
            action = self._reason()
            
            # Check if done
            if action["type"] == "finish":
                return action["output"]
            
            # Execute action
            observation = self._act(action)
            
            # Add to memory
            self.memory.append({
                "role": "assistant",
                "content": f"Thought: {action['thought']}\nAction: {action['tool']}"
            })
            self.memory.append({
                "role": "user",
                "content": f"Observation: {observation}"
            })
        
        return "Max steps reached"
    
    def _reason(self):
        """Generate the next action."""
        
        system_prompt = """You are an AI agent that reasons and acts.

Available tools:
{tools}

To use a tool, respond with:
Thought: [your reasoning]
Action: [tool_name]
Action Input: [input for the tool]

When you have the final answer, respond with:
Thought: I now have enough information
Final Answer: [your answer]
"""
        
        # Get LLM response
        response = self.llm.generate(
            system=system_prompt,
            messages=self.memory
        )
        
        # Parse response
        return self._parse_action(response)
    
    def _act(self, action):
        """Execute the chosen action."""
        
        tool = self.tools.get(action["tool"])
        if not tool:
            return f"Error: Tool '{action['tool']}' not found"
        
        try:
            return tool.run(action["input"])
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _parse_action(self, response):
        """Parse LLM response into action."""
        
        if "Final Answer:" in response:
            return {
                "type": "finish",
                "output": response.split("Final Answer:")[-1].strip()
            }
        
        # Extract tool and input
        lines = response.split("\n")
        thought = ""
        tool = ""
        tool_input = ""
        
        for line in lines:
            if line.startswith("Thought:"):
                thought = line[8:].strip()
            elif line.startswith("Action:"):
                tool = line[7:].strip()
            elif line.startswith("Action Input:"):
                tool_input = line[13:].strip()
        
        return {
            "type": "action",
            "thought": thought,
            "tool": tool,
            "input": tool_input
        }
```

#### Plan-and-Execute

Agent that plans first, then executes:

```python
class PlanAndExecuteAgent:
    """Agent that plans before executing."""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def run(self, goal: str):
        """Plan and execute a goal."""
        
        # Step 1: Create plan
        plan = self._create_plan(goal)
        print(f"Plan: {plan}")
        
        # Step 2: Execute each step
        results = []
        for i, step in enumerate(plan):
            print(f"\nExecuting step {i+1}: {step}")
            
            result = self._execute_step(step, results)
            results.append({"step": step, "result": result})
            
            print(f"Result: {result}")
        
        # Step 3: Synthesize final answer
        return self._synthesize(goal, results)
    
    def _create_plan(self, goal: str):
        """Create a plan for achieving the goal."""
        
        prompt = f"""Create a step-by-step plan to achieve this goal:

Goal: {goal}

Available tools: {[tool.name for tool in self.tools]}

Return the plan as a numbered list of steps.
Each step should be specific and actionable.
"""
        
        response = self.llm.generate(prompt)
        
        # Parse numbered list
        steps = []
        for line in response.split("\n"):
            if line.strip() and line.strip()[0].isdigit():
                step = line.split(".", 1)[-1].strip()
                steps.append(step)
        
        return steps
    
    def _execute_step(self, step: str, previous_results: list):
        """Execute a single step."""
        
        # Build context from previous results
        context = "\n".join([
            f"Step {i+1}: {r['step']}\nResult: {r['result']}"
            for i, r in enumerate(previous_results)
        ])
        
        prompt = f"""Execute this step:

Step: {step}

Previous context:
{context}

Available tools: {[tool.name for tool in self.tools]}

To use a tool, respond with:
Action: [tool_name]
Action Input: [input]

If you can answer directly, respond with:
Answer: [your answer]
"""
        
        response = self.llm.generate(prompt)
        
        # Parse and execute if needed
        if "Action:" in response:
            action_line = [l for l in response.split("\n") if l.startswith("Action:")][0]
            input_line = [l for l in response.split("\n") if l.startswith("Action Input:")][0]
            
            tool_name = action_line.split(":", 1)[1].strip()
            tool_input = input_line.split(":", 1)[1].strip()
            
            # Execute tool
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if tool:
                return tool.run(tool_input)
            else:
                return f"Tool {tool_name} not found"
        else:
            # Direct answer
            return response.split("Answer:")[-1].strip() if "Answer:" in response else response
    
    def _synthesize(self, goal: str, results: list):
        """Synthesize final answer from results."""
        
        results_text = "\n".join([
            f"Step {i+1}: {r['step']}\nResult: {r['result']}"
            for i, r in enumerate(results)
        ])
        
        prompt = f"""Based on these steps and results, provide a final answer.

Goal: {goal}

Steps and Results:
{results_text}

Provide a comprehensive final answer.
"""
        
        return self.llm.generate(prompt)
```

### 4. Tool System

Tools give agents capabilities beyond text generation:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable
import json


@dataclass
class Tool:
    """A tool that an agent can use."""
    name: str
    description: str
    parameters: dict
    function: Callable
    
    def run(self, input_data: str) -> str:
        """Execute the tool."""
        try:
            # Parse input
            if isinstance(input_data, str):
                try:
                    args = json.loads(input_data)
                except json.JSONDecodeError:
                    args = {"input": input_data}
            else:
                args = input_data
            
            # Execute function
            result = self.function(**args)
            return str(result)
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def to_schema(self) -> dict:
        """Convert to JSON schema for LLM."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }


# Example tools
def search_web(query: str) -> str:
    """Search the web for information."""
    # Placeholder - would use real search API
    return f"Search results for: {query}"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def read_file(path: str) -> str:
    """Read a file."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

# Create tools
tools = [
    Tool(
        name="search",
        description="Search the web for information",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        },
        function=search_web
    ),
    Tool(
        name="calculate",
        description="Calculate a mathematical expression",
        parameters={
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression"}
            },
            "required": ["expression"]
        },
        function=calculate
    ),
    Tool(
        name="read_file",
        description="Read a file from the filesystem",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"}
            },
            "required": ["path"]
        },
        function=read_file
    )
]
```

### 5. Memory Systems

Agents need memory to maintain context:

```python
from collections import deque
from dataclasses import dataclass
from typing import List, Optional
import chromadb


@dataclass
class MemoryItem:
    """A single memory item."""
    content: str
    memory_type: str  # "short_term", "long_term", "episodic"
    timestamp: float
    metadata: dict = None


class AgentMemory:
    """Memory system for agents."""
    
    def __init__(self, short_term_size: int = 20):
        self.short_term = deque(maxlen=short_term_size)
        self.long_term = []  # Could use vector DB
        self.episodic = []  # Task/episode memories
    
    def add_short_term(self, content: str, metadata: dict = None):
        """Add to short-term memory."""
        item = MemoryItem(
            content=content,
            memory_type="short_term",
            timestamp=time.time(),
            metadata=metadata
        )
        self.short_term.append(item)
    
    def add_long_term(self, content: str, metadata: dict = None):
        """Add to long-term memory."""
        item = MemoryItem(
            content=content,
            memory_type="long_term",
            timestamp=time.time(),
            metadata=metadata
        )
        self.long_term.append(item)
    
    def add_episodic(self, episode: str, metadata: dict = None):
        """Add episode/task memory."""
        item = MemoryItem(
            content=episode,
            memory_type="episodic",
            timestamp=time.time(),
            metadata=metadata
        )
        self.episodic.append(item)
    
    def get_context(self, max_items: int = 10) -> str:
        """Get recent context for LLM."""
        
        # Get recent short-term memories
        recent = list(self.short_term)[-max_items:]
        
        context_parts = []
        for item in recent:
            context_parts.append(f"[{item.memory_type}] {item.content}")
        
        return "\n".join(context_parts)
    
    def search_long_term(self, query: str, top_k: int = 5) -> List[str]:
        """Search long-term memory."""
        # Simple search - in production, use vector search
        results = []
        for item in self.long_term:
            if query.lower() in item.content.lower():
                results.append(item.content)
        
        return results[:top_k]
    
    def get_episodic_context(self, task: str) -> str:
        """Get relevant episodic memories."""
        relevant = []
        for item in self.episodic:
            if task.lower() in item.content.lower():
                relevant.append(item.content)
        
        return "\n".join(relevant[-5:])  # Last 5 relevant episodes
```

### 6. Agent Loop

The core execution loop:

```python
class AgentLoop:
    """Main agent execution loop."""
    
    def __init__(self, agent, max_iterations: int = 10):
        self.agent = agent
        self.max_iterations = max_iterations
    
    def run(self, task: str) -> str:
        """Run agent loop until task is complete."""
        
        # Initialize
        self.agent.memory.add_short_term(f"Task: {task}")
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Get current state
            context = self.agent.memory.get_context()
            
            # Decide next action
            action = self.agent.decide_action(task, context)
            print(f"Action: {action}")
            
            # Check if done
            if action["type"] == "finish":
                return action["result"]
            
            # Execute action
            try:
                result = self.agent.execute_action(action)
                print(f"Result: {result}")
            except Exception as e:
                result = f"Error: {str(e)}"
                print(f"Error: {result}")
            
            # Update memory
            self.agent.memory.add_short_term(
                f"Action: {action['tool']}\nResult: {result}"
            )
        
        return "Max iterations reached"
```

---

## Code Examples

### Example 1: Complete Agent Framework

```python
"""
Production-ready AI agent framework.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional
from enum import Enum
import json
from openai import OpenAI


class ActionType(Enum):
    """Types of actions an agent can take."""
    THINK = "think"
    ACT = "act"
    FINISH = "finish"
    ERROR = "error"


@dataclass
class Action:
    """An action the agent wants to take."""
    type: ActionType
    thought: str = ""
    tool: str = ""
    tool_input: str = ""
    result: str = ""


@dataclass
class Tool:
    """A tool available to the agent."""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def execute(self, **kwargs) -> str:
        """Execute the tool."""
        try:
            result = self.function(**kwargs)
            return str(result)
        except Exception as e:
            return f"Tool error: {str(e)}"


class AIAgent:
    """Complete AI agent with tools, memory, and reasoning."""
    
    def __init__(
        self,
        name: str = "Agent",
        model: str = "gpt-4",
        tools: List[Tool] = None,
        max_iterations: int = 15
    ):
        self.name = name
        self.model = model
        self.client = OpenAI()
        self.tools = {tool.name: tool for tool in (tools or [])}
        self.max_iterations = max_iterations
        self.memory: List[Dict[str, str]] = []
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with tool descriptions."""
        
        tool_descriptions = "\n".join([
            f"- {tool.name}: {tool.description}"
            for tool in self.tools.values()
        ])
        
        return f"""You are {self.name}, an AI agent that can use tools to accomplish tasks.

Available tools:
{tool_descriptions}

To use a tool, respond in this exact format:
Thought: [your reasoning about what to do next]
Action: [tool_name]
Action Input: [JSON input for the tool]

When you have completed the task, respond with:
Thought: I now have all the information needed
Final Answer: [your comprehensive answer]

Important:
- Always think before acting
- Use tools when needed, don't make things up
- If a tool fails, try a different approach
- Be thorough but efficient
"""
    
    def run(self, task: str) -> str:
        """Execute a task."""
        
        # Initialize memory
        self.memory = [{"role": "user", "content": task}]
        
        for iteration in range(self.max_iterations):
            # Get LLM response
            response = self._call_llm()
            
            # Parse action
            action = self._parse_action(response)
            
            print(f"\n{'='*50}")
            print(f"Iteration {iteration + 1}")
            print(f"Thought: {action.thought}")
            
            if action.type == ActionType.FINISH:
                print(f"Final Answer: {action.result}")
                return action.result
            
            if action.type == ActionType.ACT:
                print(f"Action: {action.tool}")
                print(f"Input: {action.tool_input}")
                
                # Execute tool
                result = self._execute_tool(action.tool, action.tool_input)
                print(f"Result: {result[:200]}...")
                
                # Add to memory
                self.memory.append({
                    "role": "assistant",
                    "content": response
                })
                self.memory.append({
                    "role": "user",
                    "content": f"Observation: {result}"
                })
            
            if action.type == ActionType.ERROR:
                print(f"Error: {action.result}")
                self.memory.append({
                    "role": "user",
                    "content": f"Error occurred: {action.result}. Please try a different approach."
                })
        
        return "Task could not be completed within maximum iterations"
    
    def _call_llm(self) -> str:
        """Call the LLM."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt}
            ] + self.memory,
            temperature=0.2,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    def _parse_action(self, response: str) -> Action:
        """Parse LLM response into an action."""
        
        if "Final Answer:" in response:
            answer = response.split("Final Answer:")[-1].strip()
            thought = response.split("Thought:")[-1].split("Final Answer:")[0].strip()
            return Action(
                type=ActionType.FINISH,
                thought=thought,
                result=answer
            )
        
        if "Action:" in response:
            try:
                thought = response.split("Thought:")[-1].split("Action:")[0].strip()
                tool = response.split("Action:")[-1].split("\n")[0].strip()
                tool_input = response.split("Action Input:")[-1].strip()
                
                return Action(
                    type=ActionType.ACT,
                    thought=thought,
                    tool=tool,
                    tool_input=tool_input
                )
            except Exception as e:
                return Action(
                    type=ActionType.ERROR,
                    result=f"Failed to parse action: {str(e)}"
                )
        
        # Default: treat as finish
        return Action(
            type=ActionType.FINISH,
            result=response
        )
    
    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool."""
        
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found. Available: {list(self.tools.keys())}"
        
        tool = self.tools[tool_name]
        
        # Parse input
        try:
            kwargs = json.loads(tool_input)
        except json.JSONDecodeError:
            kwargs = {"input": tool_input}
        
        return tool.execute(**kwargs)
    
    def reset(self):
        """Reset agent state."""
        self.memory = []


# Usage example
def create_research_agent():
    """Create an agent for research tasks."""
    
    # Define tools
    tools = [
        Tool(
            name="search",
            description="Search the web for information",
            function=lambda query: f"Search results for '{query}': [simulated results]",
            parameters={"query": {"type": "string"}}
        ),
        Tool(
            name="read_file",
            description="Read content from a file",
            function=lambda path: f"Content of {path}: [simulated content]",
            parameters={"path": {"type": "string"}}
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            function=lambda path, content: f"Written to {path}",
            parameters={"path": {"type": "string"}, "content": {"type": "string"}}
        ),
        Tool(
            name="calculate",
            description="Perform a calculation",
            function=lambda expression: str(eval(expression)),
            parameters={"expression": {"type": "string"}}
        )
    ]
    
    # Create agent
    agent = AIAgent(
        name="Research Assistant",
        model="gpt-4",
        tools=tools,
        max_iterations=10
    )
    
    return agent


# Run agent
agent = create_research_agent()
result = agent.run("Research the benefits of RAG systems and write a summary")
print("\n" + "="*50)
print("FINAL RESULT:")
print(result)
```

---

## Common Mistakes to Avoid

### 1. No Error Handling
```python
# ❌ BAD: Agent crashes on tool failure
def run_agent(goal):
    for step in plan:
        result = execute_tool(step)  # May crash
        process(result)

# ✅ GOOD: Handle errors gracefully
def run_agent(goal):
    for step in plan:
        try:
            result = execute_tool(step)
        except Exception as e:
            result = handle_error(e)
            if not recoverable(e):
                return fallback_answer()
        process(result)
```

### 2. No Termination Condition
```python
# ❌ BAD: Agent runs forever
while True:
    action = agent.decide()
    execute(action)

# ✅ GOOD: Max iterations and done condition
for i in range(MAX_ITERATIONS):
    action = agent.decide()
    if action.type == "finish":
        return action.result
    execute(action)
return "Max iterations reached"
```

---

## Best Practices

1. **Clear goals** - Agent needs well-defined objectives
2. **Tool descriptions** - Help LLM choose the right tool
3. **Error recovery** - Handle failures gracefully
4. **Memory management** - Don't let context grow unbounded
5. **Logging** - Track all actions for debugging
6. **Timeouts** - Prevent infinite loops
7. **Human oversight** - Allow intervention when needed
8. **Testing** - Test tools and agent loops thoroughly

---

## Practice Exercises

### Exercise 1: File Assistant Agent
Build an agent that can:
1. Read files from a directory
2. Search for specific content
3. Create summary reports
4. Handle errors (missing files, permission issues)

### Exercise 2: Code Review Agent
Create an agent that:
1. Reads code files
2. Identifies issues
3. Suggests improvements
4. Can run tests

### Exercise 3: Data Analysis Agent
Build an agent that:
1. Reads CSV/JSON data
2. Performs calculations
3. Generates insights
4. Creates visualizations

### Exercise 4: Multi-Tool Agent
Create an agent with 5+ tools that:
1. Researches a topic
2. Writes documentation
3. Creates examples
4. Validates output

### Exercise 5: Self-Correcting Agent
Build an agent that:
1. Detects its own errors
2. Forms new hypotheses
3. Retries with different approaches
4. Learns from failures

---

## Summary

AI agents are autonomous systems that combine reasoning with action:

1. **Architecture** - ReAct, Plan-and-Execute patterns
2. **Tools** - Extend agent capabilities
3. **Memory** - Maintain context across steps
4. **Loop** - Observe → Think → Act cycle
5. **Safety** - Error handling, termination conditions

**Key Success Factors:**
- Clear goal definition
- Well-designed tools
- Effective memory management
- Robust error handling
- Human oversight

**Next lecture:** AI Evaluation - Measuring agent and system quality.
