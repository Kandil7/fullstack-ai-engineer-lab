# Lecture 01: Agent Fundamentals

## 🎯 Topic Overview

An **AI agent** is an autonomous software entity that perceives its environment, makes decisions, and takes actions to achieve specific goals. Unlike traditional programs that follow fixed instructions, agents use AI models (typically LLMs) to reason about situations, choose appropriate actions, and adapt their behavior based on feedback.

This lecture covers the foundational concepts that underpin all AI agent systems — from simple single-step agents to complex multi-agent architectures.

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Define** what an AI agent is and distinguish it from chatbots, copilots, and traditional software
2. **Identify** the core components of an agent system (perception, reasoning, action, memory)
3. **Explain** the agent loop and how agents decide what to do next
4. **Classify** different types of agents by capability and architecture
5. **Implement** a basic agent in Python using an LLM
6. **Evaluate** when an agent approach is appropriate vs. simpler alternatives
7. **Avoid** common pitfalls in agent design

---

## 🧩 Key Concepts

### 1. What Is an AI Agent?

An AI agent is a system that:

```
┌─────────────────────────────────────────────────┐
│                  AI AGENT                        │
│                                                  │
│   Perception → Reasoning → Action → Observation  │
│       ↑                                    │     │
│       └────────────────────────────────────┘     │
│                    (Agent Loop)                   │
└─────────────────────────────────────────────────┘
```

**Core properties:**
- **Autonomy**: Operates without constant human intervention
- **Reactivity**: Perceives and responds to environment changes
- **Pro-activeness**: Takes initiative to achieve goals
- **Social ability**: Interacts with other agents or humans

### 2. Agent vs. Chatbot vs. Copilot

| Feature | Chatbot | Copilot | Agent |
|---------|---------|---------|-------|
| **Interaction** | Q&A only | Suggests with approval | Acts autonomously |
| **Tools** | None | Limited | Full tool access |
| **Memory** | Session only | Limited context | Persistent memory |
| **Reasoning** | Simple | Moderate | Multi-step planning |
| **Autonomy** | Low | Medium | High |
| **Example** | FAQ bot | GitHub Copilot | AutoGPT, Claude Agent |

### 3. The Agent Loop

Every agent follows some variation of this cycle:

```python
def agent_loop(goal, max_iterations=10):
    """
    The fundamental agent loop.
    
    1. Observe the current state
    2. Think about what to do
    3. Take an action
    4. Observe the result
    5. Repeat until goal is achieved or limit reached
    """
    context = {"goal": goal, "history": [], "observations": []}
    
    for i in range(max_iterations):
        # Step 1: Perception - observe current state
        observation = perceive(context)
        
        # Step 2: Reasoning - decide what to do
        thought = llm_reason(observation, context["history"])
        
        # Step 3: Action - execute the chosen action
        action = decide_action(thought)
        result = execute(action)
        
        # Step 4: Update context with what happened
        context["history"].append({
            "thought": thought,
            "action": action,
            "result": result
        })
        context["observations"].append(result)
        
        # Step 5: Check if goal is achieved
        if goal_achieved(result, goal):
            return result
    
    return "Max iterations reached"
```

### 4. Agent Architecture Components

```
┌──────────────────────────────────────────────────────────┐
│                     Agent Architecture                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────┐    ┌──────────┐    ┌─────────┐             │
│  │  LLM    │◄──►│  Memory  │◄──►│  Tools  │             │
│  │ (Brain) │    │ (State)  │    │(Actions)│             │
│  └────┬────┘    └────┬─────┘    └────┬────┘             │
│       │              │               │                    │
│       ▼              ▼               ▼                    │
│  ┌─────────────────────────────────────────┐             │
│  │           Environment / User            │             │
│  └─────────────────────────────────────────┘             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Components:**
- **LLM (Brain)**: The reasoning engine that processes information and decides actions
- **Memory (State)**: Stores past interactions, learned facts, and context
- **Tools (Actions)**: Capabilities the agent can invoke (APIs, databases, code execution)
- **Environment**: The external world the agent interacts with

---

## 💻 Code Examples

### Example 1: Simple ReAct Agent

```python
"""
Simple ReAct Agent Implementation
ReAct = Reasoning + Acting
"""
import openai
from typing import Callable, Dict, List, Optional

class SimpleAgent:
    """
    A minimal agent that follows the ReAct pattern:
    Thought → Action → Observation → Thought → ...
    """
    
    def __init__(self, model: str = "gpt-4"):
        self.client = openai.OpenAI()
        self.model = model
        self.tools: Dict[str, Callable] = {}
        self.max_iterations = 10
    
    def register_tool(self, name: str, func: Callable, description: str):
        """Register a tool the agent can use."""
        self.tools[name] = {
            "function": func,
            "description": description
        }
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with available tools."""
        tool_descriptions = "\n".join(
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        )
        
        return f"""You are an AI agent that helps users accomplish tasks.

Available tools:
{tool_descriptions}

To use a tool, respond with:
Action: <tool_name>
Input: <input_for_the_tool>

When you have the final answer, respond with:
Final Answer: <your_answer>

Always think step by step.
"""
    
    def _call_llm(self, messages: List[Dict]) -> str:
        """Call the LLM for reasoning."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def _execute_tool(self, action: str, tool_input: str) -> str:
        """Execute a tool and return the result."""
        if action not in self.tools:
            return f"Error: Unknown tool '{action}'. Available: {list(self.tools.keys())}"
        
        try:
            result = self.tools[action]["function"](tool_input)
            return str(result)
        except Exception as e:
            return f"Error executing {action}: {str(e)}"
    
    def run(self, user_goal: str) -> str:
        """
        Run the agent loop until the goal is achieved.
        
        Args:
            user_goal: What the user wants the agent to do
            
        Returns:
            The final answer or result
        """
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Goal: {user_goal}"}
        ]
        
        for iteration in range(self.max_iterations):
            # Get agent's reasoning
            response = self._call_llm(messages)
            print(f"\n--- Iteration {iteration + 1} ---")
            print(f"Agent: {response}")
            
            # Check if agent has reached a final answer
            if "Final Answer:" in response:
                final = response.split("Final Answer:")[-1].strip()
                return final
            
            # Parse and execute action
            if "Action:" in response and "Input:" in response:
                lines = response.split("\n")
                action = None
                tool_input = None
                
                for line in lines:
                    if line.strip().startswith("Action:"):
                        action = line.strip().split("Action:")[-1].strip()
                    elif line.strip().startswith("Input:"):
                        tool_input = line.strip().split("Input:")[-1].strip()
                
                if action and tool_input:
                    # Execute tool
                    result = self._execute_tool(action, tool_input)
                    print(f"Tool Result: {result}")
                    
                    # Add to conversation
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user",
                        "content": f"Observation: {result}\n\nWhat should I do next?"
                    })
            
            # Safety check
            if "Action:" not in response and "Final Answer:" not in response:
                messages.append({
                    "role": "user",
                    "content": "Please either use a tool (Action: ... Input: ...) or provide a Final Answer."
                })
        
        return "Maximum iterations reached without completing the task."


# === Usage Example ===

# Define tools
def search_knowledge_base(query: str) -> str:
    """Simulate searching a knowledge base."""
    knowledge = {
        "python": "Python is a high-level programming language created by Guido van Rossum.",
        "agents": "AI agents are autonomous systems that perceive, reason, and act.",
        "llm": "LLMs are large language models trained on text data.",
    }
    
    query_lower = query.lower()
    results = []
    for key, value in knowledge.items():
        if key in query_lower:
            results.append(value)
    
    return "\n".join(results) if results else "No relevant information found."


def calculate(expression: str) -> str:
    """Safely evaluate a math expression."""
    try:
        # Only allow safe math operations
        allowed_chars = set("0123456789+-*/.() ")
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"Result: {result}"
        return "Error: Invalid characters in expression"
    except Exception as e:
        return f"Error: {str(e)}"


# Create and run agent
agent = SimpleAgent()
agent.register_tool("search", search_knowledge_base, "Search the knowledge base for information")
agent.register_tool("calculate", calculate, "Calculate a math expression")

# Run it
result = agent.run("What is Python? And what is 234 * 56?")
print(f"\nFinal Result: {result}")
```

### Example 2: Agent with State Management

```python
"""
Agent with persistent state and context management.
Demonstrates how agents maintain memory across iterations.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
import json

class ActionStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AgentStep:
    """Represents a single step in the agent's execution."""
    step_id: int
    thought: str
    action: str
    action_input: Any
    observation: str
    status: ActionStatus
    timestamp: float = 0.0

@dataclass
class AgentState:
    """
    Maintains the full state of an agent during execution.
    
    This is the 'memory' of the agent - it tracks:
    - What the agent has thought
    - What actions it has taken
    - What results it observed
    - What goals it's working toward
    """
    goal: str
    steps: List[AgentStep] = field(default_factory=list)
    current_step: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_step(self, step: AgentStep):
        """Record a new step."""
        self.steps.append(step)
        self.current_step += 1
    
    def get_history_summary(self) -> str:
        """Get a human-readable summary of what's happened."""
        if not self.steps:
            return "No steps taken yet."
        
        summary = []
        for step in self.steps:
            summary.append(
                f"Step {step.step_id}:\n"
                f"  Thought: {step.thought}\n"
                f"  Action: {step.action}({step.action_input})\n"
                f"  Result: {step.observation}\n"
                f"  Status: {step.status.value}"
            )
        return "\n\n".join(summary)
    
    def to_dict(self) -> Dict:
        """Serialize state for persistence."""
        return {
            "goal": self.goal,
            "current_step": self.current_step,
            "steps": [
                {
                    "step_id": s.step_id,
                    "thought": s.thought,
                    "action": s.action,
                    "action_input": s.action_input,
                    "observation": s.observation,
                    "status": s.status.value
                }
                for s in self.steps
            ],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "AgentState":
        """Deserialize state from persistence."""
        state = cls(goal=data["goal"])
        state.current_step = data["current_step"]
        state.metadata = data.get("metadata", {})
        
        for step_data in data.get("steps", []):
            step = AgentStep(
                step_id=step_data["step_id"],
                thought=step_data["thought"],
                action=step_data["action"],
                action_input=step_data["action_input"],
                observation=step_data["observation"],
                status=ActionStatus(step_data["status"])
            )
            state.steps.append(step)
        
        return state


class StatefulAgent:
    """
    An agent that maintains state across its execution.
    
    Key features:
    - Persists reasoning history
    - Can resume from saved state
    - Tracks progress toward goal
    """
    
    def __init__(self, tools: Dict[str, Callable], llm_caller):
        self.tools = tools
        self.llm = llm_caller
    
    def think(self, state: AgentState) -> tuple[str, str, str]:
        """
        Agent thinks about what to do next.
        Returns: (thought, action_name, action_input)
        """
        prompt = self._build_think_prompt(state)
        response = self.llm(prompt)
        return self._parse_think_response(response)
    
    def act(self, action_name: str, action_input: str) -> str:
        """Execute an action using the appropriate tool."""
        if action_name not in self.tools:
            return f"Unknown action: {action_name}"
        
        try:
            return str(self.tools[action_name](action_input))
        except Exception as e:
            return f"Action failed: {str(e)}"
    
    def run(self, goal: str, state: Optional[AgentState] = None) -> AgentState:
        """
        Main agent loop with state management.
        
        Can resume from an existing state or start fresh.
        """
        if state is None:
            state = AgentState(goal=goal)
        
        max_steps = 10
        
        while state.current_step < max_steps:
            # Think
            thought, action, action_input = self.think(state)
            
            # Create step
            step = AgentStep(
                step_id=state.current_step + 1,
                thought=thought,
                action=action,
                action_input=action_input,
                observation="",
                status=ActionStatus.IN_PROGRESS
            )
            
            # Act
            observation = self.act(action, action_input)
            step.observation = observation
            step.status = ActionStatus.COMPLETED
            
            # Record step
            state.add_step(step)
            
            # Check if done
            if action == "finish":
                break
        
        return state
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: No Exit Condition
```python
# ❌ BAD: Agent might loop forever
def bad_agent(goal):
    while True:
        thought = think(goal)
        result = act(thought)
        # No check for completion!

# ✅ GOOD: Always have exit conditions
def good_agent(goal, max_iterations=10, goal_checker=None):
    for i in range(max_iterations):
        thought = think(goal)
        result = act(thought)
        if goal_checker and goal_checker(result, goal):
            return result
    return "Max iterations reached"
```

### Mistake 2: Ignoring Errors
```python
# ❌ BAD: Silently swallowing errors
try:
    result = tool(input)
except:
    pass  # Agent doesn't know what went wrong

# ✅ GOOD: Feeding errors back for reasoning
try:
    result = tool(input)
except Exception as e:
    result = f"Error: {str(e)}. Agent should try alternative approach."
```

### Mistake 3: No Observability
```python
# ❌ BAD: Agent runs invisibly
result = agent.run(goal)

# ✅ GOOD: Agent logs its reasoning
for step in agent.run_with_logging(goal):
    print(f"Step {step.number}: {step.thought}")
    print(f"Action: {step.action}")
    print(f"Result: {step.observation[:100]}...")
```

### Mistake 4: Oversized Prompts
```python
# ❌ BAD: Dumping everything into context
system_prompt = f"""
You are an agent. Here is all the data: {huge_dataset}
And all the tools: {tool_descriptions}
And the full history: {entire_history}
"""

# ✅ GOOD: Curated, relevant context
system_prompt = f"""
You are an agent. Current goal: {goal}
Available tools: {relevant_tools}
Recent history: {last_5_steps}
"""
```

---

## ✅ Best Practices

1. **Start Simple**: Begin with a single-purpose agent before adding complexity
2. **Instrument Everything**: Log all LLM calls, tool executions, and decisions
3. **Set Limits**: Always have `max_iterations` and timeout guards
4. **Validate Outputs**: Check LLM outputs before executing actions
5. **Graceful Degradation**: Handle tool failures without crashing the agent
6. **Test Incrementally**: Test each tool independently before testing the full agent
7. **Version Your Prompts**: Track prompt changes like code changes

---

## 🏋️ Practice Exercises

### Exercise 1: Build a Weather Agent
Create an agent that can:
- Look up current weather for a city
- Convert between temperature units
- Suggest what to wear based on weather

```python
# Starter code
tools = {
    "get_weather": get_weather,
    "convert_temp": convert_temperature,
    "suggest_outfit": suggest_outfit
}

# Your implementation here
weather_agent = SimpleAgent()
for name, func in tools.items():
    weather_agent.register_tool(name, func, f"Tool: {name}")

result = weather_agent.run("What should I wear in Tokyo right now?")
```

### Exercise 2: Add Memory to Your Agent
Extend the weather agent to remember:
- Cities the user has asked about
- Their preferred temperature unit
- Past outfit recommendations

### Exercise 3: Build a Multi-Tool Agent
Create an agent with at least 5 tools that can:
- Search for information
- Perform calculations
- Save/load data
- Send notifications
- Schedule tasks

---

## 📝 Summary

| Concept | Description |
|---------|-------------|
| **Agent** | Autonomous system that perceives, reasons, and acts |
| **Agent Loop** | Observe → Think → Act → Observe (repeat) |
| **Autonomy** | Agent's ability to operate without human intervention |
| **Tool Use** | Extending agent capabilities through external functions |
| **State** | Memory of past actions and observations |
| **Goal** | The objective the agent is working toward |
| **ReAct** | Pattern combining reasoning and acting |

**Key Takeaways:**
1. Agents are more than chatbots — they take autonomous actions
2. The agent loop (think → act → observe) is the core pattern
3. Tools extend what agents can do
4. State/memory lets agents build on past work
5. Always include safety limits and error handling
6. Start simple, iterate toward complexity

---

## 🔗 Next Lecture

In **Lecture 02: Tool Calling**, we'll dive deep into how agents use tools, how to design tool interfaces, and advanced patterns for tool selection and chaining.
