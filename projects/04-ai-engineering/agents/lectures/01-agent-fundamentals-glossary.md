# Glossary: Agent Fundamentals

> Terms defined in alphabetical order. Each entry includes: definition, example usage, code snippet, and related terms.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Action | An operation performed by an agent on its environment | Tool, Observation |
| Agent | Autonomous system that perceives, reasons, and acts | LLM, Tool, Memory |
| Agent Loop | The Observe→Think→Act→Observe cycle | ReAct, Planning |
| Autonomy | Agent's ability to operate without human intervention | Human-in-the-loop |
| Context Window | LLM's maximum input token capacity | Token, Prompt |
| Environment | External world the agent interacts with | Perception |
| Goal | The objective an agent is working toward | Task, Objective |
| Human-in-the-loop | Pattern where humans oversee agent actions | Autonomy |
| LLM | Large Language Model — the agent's "brain" | Foundation Model |
| Memory | Stored information from past interactions | State, Context |
| Observation | Feedback received after an action | Action, Result |
| Perception | Gathering information from the environment | Observation |
| Prompt | Input text given to an LLM | System Prompt |
| ReAct | Pattern combining reasoning and acting | Chain-of-Thought |
| Reasoning | LLM's process of deciding what to do | Thinking, Planning |
| State | Current condition of the agent and its context | Memory |
| System Prompt | Instructions that define agent behavior | Prompt |
| Token | Unit of text processed by LLMs | Context Window |
| Tool | External function an agent can invoke | Action, Function Calling |
| Tool Use | Pattern of agents calling external tools | Function Calling |
| Trajectory | Record of steps an agent has taken | Trace, History |

---

## A

### Action

**Definition:** An operation that an agent performs on its environment. Actions are the way agents effect change in the world — they might call an API, write to a database, send a message, or execute code.

**Example:**
```python
# An action is a specific operation the agent decides to perform
action = {
    "name": "search_web",
    "input": "best practices for Python agents",
    "description": "Search the web for information"
}

# Execution of an action
result = execute_action(action)
```

**Related terms:** Tool, Observation, Agent Loop

---

### Agent

**Definition:** An autonomous software entity that perceives its environment through sensors (inputs), reasons about what to do (using an LLM), and acts through actuators (tools/functions) to achieve specific goals.

**Example:**
```python
class Agent:
    def __init__(self, llm, tools, memory):
        self.llm = llm           # The reasoning engine
        self.tools = tools       # Available actions
        self.memory = memory     # Past experiences
    
    def run(self, goal):
        while not self.is_done():
            observation = self.perceive()
            thought = self.llm.reason(observation, self.memory)
            action = self.decide_action(thought)
            result = self.act(action)
            self.memory.store(thought, action, result)
        return self.get_result()
```

**Related terms:** LLM, Tool, Memory, Agent Loop

---

### Agent Loop

**Definition:** The fundamental cycle that all agents follow: perceive the environment, reason about what to do, take an action, observe the result, and repeat. This loop continues until the agent achieves its goal or reaches a stopping condition.

**Example:**
```
Goal: "Find the weather in Paris and convert to Fahrenheit"

Iteration 1:
  Observation: (starting)
  Thought: I need to get the weather for Paris
  Action: get_weather("Paris")
  Observation: 22°C, sunny

Iteration 2:
  Thought: Now I need to convert 22°C to Fahrenheit
  Action: convert_temp("22", "C", "F")
  Observation: 71.6°F

Iteration 3:
  Thought: I have the answer
  Action: finish("The weather in Paris is 71.6°F (22°C), sunny.")
```

**Code:**
```python
def agent_loop(agent, goal, max_iterations=10):
    for i in range(max_iterations):
        observation = agent.perceive()
        thought = agent.think(observation)
        action = agent.plan_action(thought)
        result = agent.execute(action)
        
        if agent.goal_achieved(result, goal):
            return result
    
    return "Max iterations reached"
```

**Related terms:** ReAct, Perception, Reasoning, Action

---

### Autonomy

**Definition:** The degree to which an agent can operate independently without human intervention. Full autonomy means the agent can perceive, decide, and act entirely on its own. Partial autonomy may require human approval for certain actions.

**Levels of Autonomy:**
```python
class AutonomyLevel:
    # Level 0: No autonomy — human does everything
    MANUAL = 0
    
    # Level 1: Agent suggests, human decides
    SUGGESTIONS = 1
    
    # Level 2: Agent acts, human can override
    SUPERVISED = 2
    
    # Level 3: Agent acts, human reviews after
    AUTONOMOUS_WITH_REVIEW = 3
    
    # Level 4: Full autonomy, no human needed
    FULL = 4

# Example: Agent with approval requirement
class SupervisedAgent:
    def __init__(self, require_approval_for=None):
        self.require_approval = require_approval_for or []
    
    def execute_action(self, action):
        if action.name in self.require_approval:
            if not human_approve(action):
                return "Action cancelled by user"
        return action.execute()
```

**Related terms:** Human-in-the-loop, Agent

---

## B

### Brain

**Definition:** Informal term for the LLM (Large Language Model) component of an agent. The brain is responsible for reasoning, planning, and decision-making. It processes observations and generates thoughts and actions.

**Example:**
```python
# The "brain" of our agent
brain = ChatOpenAI(model="gpt-4")

def think(brain, context):
    """Use the brain to reason about what to do."""
    prompt = f"""
    You are an AI agent. Current context:
    {context}
    
    What should you do next? Respond with:
    Thought: <your reasoning>
    Action: <action name>
    """
    return brain.generate(prompt)
```

**Related terms:** LLM, Reasoning

---

## C

### Context

**Definition:** The information available to an agent at any point in time. This includes the current prompt, conversation history, tool outputs, memory, and environmental state. The context window limits how much information the LLM can process at once.

**Example:**
```python
class AgentContext:
    def __init__(self):
        self.system_prompt = ""      # Permanent instructions
        self.conversation = []       # Chat history
        self.tool_results = []       # Outputs from tools
        self.memory = []             # Long-term memory
        self.environment = {}        # External state
    
    def to_messages(self):
        """Convert context to LLM messages format."""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation)
        return messages
    
    def add_observation(self, observation):
        """Add new information to context."""
        self.tool_results.append(observation)
        self.conversation.append({
            "role": "user",
            "content": f"Observation: {observation}"
        })
```

**Related terms:** Context Window, Memory, Prompt

---

### Context Window

**Definition:** The maximum number of tokens (text units) that an LLM can process in a single request. This limits how much history, context, and instructions the agent can pass to its reasoning engine. Exceeding the context window causes errors or truncation.

**Example:**
```python
def manage_context(messages, max_tokens=4000):
    """
    Ensure messages fit within the context window.
    
    Strategy: Keep system prompt + most recent messages.
    """
    # Always keep system prompt
    system_msg = messages[0]
    
    # Calculate remaining tokens for history
    remaining_tokens = max_tokens - count_tokens(system_msg["content"])
    
    # Add messages from most recent, skipping oldest
    history = []
    for msg in reversed(messages[1:]):
        msg_tokens = count_tokens(msg["content"])
        if remaining_tokens - msg_tokens >= 0:
            history.insert(0, msg)
            remaining_tokens -= msg_tokens
        else:
            break
    
    return [system_msg] + history

def count_tokens(text):
    """Estimate token count."""
    return len(text.split()) // 3  # Rough estimate
```

**Related terms:** Context, Token, Prompt

---

## D

### Deterministic vs. Non-deterministic

**Definition:** Refers to whether an agent produces the same output for the same input. LLMs are inherently non-deterministic (temperature > 0), meaning the same prompt can produce different responses. This affects agent reproducibility.

**Example:**
```python
# Non-deterministic (default LLM behavior)
response1 = llm.generate("What is 2+2?")
response2 = llm.generate("What is 2+2?")
# response1 != response2 (potentially)

# Making it more deterministic
response = llm.generate(
    "What is 2+2?",
    temperature=0,      # More deterministic
    seed=42              # Reproducible (if supported)
)

# Fully deterministic (no LLM involved)
def deterministic_agent(goal):
    """An agent with fixed rules — always same output."""
    rules = {
        "weather": lookup_weather,
        "math": evaluate_math,
    }
    action_type = classify_goal(goal)
    return rules[action_type](goal)
```

**Related terms:** Temperature, LLM, Reproducibility

---

## E

### Environment

**Definition:** The external world or system that an agent interacts with. The environment provides inputs (perceptions) to the agent and receives outputs (actions) from it. Can be real (APIs, databases, file systems) or simulated.

**Example:**
```python
class Environment:
    def __init__(self):
        self.state = {}
        self.observers = []
    
    def perceive(self):
        """Agent observes the environment."""
        return {
            "time": datetime.now(),
            "state": self.state,
            "available_actions": self.get_actions()
        }
    
    def execute(self, action):
        """Agent acts on the environment."""
        # Apply the action
        new_state = self.apply_action(action)
        self.state = new_state
        
        # Return observation
        return {
            "action_taken": action,
            "new_state": new_state,
            "reward": self.calculate_reward(action)
        }
    
    def apply_action(self, action):
        """Apply an action and return new state."""
        # Implementation depends on the environment
        pass
```

**Related terms:** Perception, Action, Agent Loop

---

### Execution Trace

**Definition:** A complete record of an agent's actions, thoughts, and observations during a run. Traces are essential for debugging, analysis, and understanding agent behavior.

**Example:**
```python
from dataclasses import dataclass
from typing import List

@dataclass
class TraceStep:
    step_number: int
    thought: str
    action: str
    action_input: str
    observation: str

@dataclass
class ExecutionTrace:
    goal: str
    steps: List[TraceStep]
    
    def print_trace(self):
        """Pretty-print the execution trace."""
        print(f"Goal: {self.goal}\n")
        for step in self.steps:
            print(f"Step {step.step_number}:")
            print(f"  Thought: {step.thought}")
            print(f"  Action: {step.action}({step.action_input})")
            print(f"  Observation: {step.observation}\n")
    
    def to_dict(self):
        """Serialize trace for logging."""
        return {
            "goal": self.goal,
            "steps": [
                {
                    "step": s.step_number,
                    "thought": s.thought,
                    "action": s.action,
                    "input": s.action_input,
                    "result": s.observation
                }
                for s in self.steps
            ]
        }

# Usage
trace = ExecutionTrace(goal="Find weather", steps=[
    TraceStep(1, "Need weather data", "search", "Paris weather", "22°C sunny"),
    TraceStep(2, "Have the answer", "finish", "22°C sunny", "Done"),
])
trace.print_trace()
```

**Related terms:** Agent Loop, Observation, Logging

---

## F

### Function Calling

**Definition:** The mechanism by which LLMs generate structured output that specifies a function to call with specific arguments. This is how agents translate natural language reasoning into concrete tool executions.

**Example:**
```python
# Defining tools for function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature units"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# LLM responds with function call
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

# Response includes function call
# {
#   "tool_calls": [{
#     "function": {
#       "name": "get_weather",
#       "arguments": '{"city": "Paris", "units": "celsius"}'
#     }
#   }]
# }
```

**Related terms:** Tool, Action, LLM

---

## G

### Goal

**Definition:** The objective that an agent is working to achieve. Goals can be explicit (user-provided instructions) or implicit (derived from context). Clear goals are essential for agent success.

**Example:**
```python
class GoalManager:
    def __init__(self):
        self.primary_goal = None
        self.sub_goals = []
        self.completed_goals = []
    
    def set_goal(self, goal: str):
        """Set the primary objective."""
        self.primary_goal = goal
        self.sub_goals = self.decompose(goal)
    
    def decompose(self, goal: str) -> list:
        """Break a complex goal into sub-goals."""
        # Could use LLM for dynamic decomposition
        return [goal]  # Simplified
    
    def check_completion(self, state) -> bool:
        """Check if goal has been achieved."""
        # Compare current state against goal criteria
        return self.evaluate(state, self.primary_goal)
    
    def evaluate(self, state, goal) -> float:
        """Score how well the goal is being achieved (0-1)."""
        # Could use LLM to evaluate
        return 0.0
```

**Related terms:** Task, Objective, Planning

---

## H

### Human-in-the-loop (HITL)

**Definition:** A design pattern where human oversight is incorporated into the agent's decision-making process. The agent may pause to request approval, clarification, or input from a human before proceeding with certain actions.

**Example:**
```python
class HumanInTheLoopAgent:
    def __init__(self, approval_required_actions=None):
        self.approval_required = approval_required_actions or []
    
    def execute_with_approval(self, action):
        """Execute action, asking for human approval if needed."""
        if action.name in self.approval_required:
            print(f"\n[APPROVAL REQUIRED]")
            print(f"Action: {action.name}")
            print(f"Input: {action.input}")
            print(f"Reasoning: {action.thought}")
            
            response = input("Approve? (yes/no/modify): ")
            
            if response.lower() == "yes":
                return action.execute()
            elif response.lower() == "modify":
                new_input = input("Enter modified input: ")
                action.input = new_input
                return action.execute()
            else:
                return "Action cancelled by user"
        
        return action.execute()

# Usage
agent = HumanInTheLoopAgent(
    approval_required_actions=["send_email", "delete_file", "make_payment"]
)
```

**Related terms:** Autonomy, Safety, Oversight

---

## K

### Knowledge Retrieval

**Definition:** The process by which an agent gathers relevant information from external sources (databases, documents, APIs, web searches) to inform its reasoning and decision-making.

**Example:**
```python
class KnowledgeRetriever:
    def __init__(self, vector_store, web_search=None):
        self.vector_store = vector_store
        self.web_search = web_search
    
    def retrieve(self, query: str, sources: list = None) -> dict:
        """
        Retrieve relevant knowledge from multiple sources.
        
        Args:
            query: What to search for
            sources: List of sources to query (default: all)
        """
        results = {}
        sources = sources or ["vector_store", "web"]
        
        if "vector_store" in sources:
            docs = self.vector_store.search(query, k=5)
            results["documents"] = docs
        
        if "web" in sources and self.web_search:
            web_results = self.web_search(query)
            results["web"] = web_results
        
        return results

# Usage in agent
retriever = KnowledgeRetriever(vector_store)
knowledge = retriever.retrieve("What are AI agent patterns?")
```

**Related terms:** RAG, Memory, Context

---

## L

### LLM (Large Language Model)

**Definition:** A neural network trained on large amounts of text data that can generate, understand, and reason about natural language. In agents, the LLM serves as the "brain" — processing inputs, reasoning about situations, and generating actions.

**Example:**
```python
from openai import OpenAI

# Basic LLM call
client = OpenAI()

def llm_reason(context: str) -> str:
    """Use LLM for agent reasoning."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI agent. Think step by step."},
            {"role": "user", "content": context}
        ],
        temperature=0.7  # Balance creativity and consistency
    )
    return response.choices[0].message.content

# LLM with structured output
def llm_plan(goal: str) -> dict:
    """LLM generates a structured plan."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Create a plan for: {goal}"}
        ],
        response_format={"type": "json_object"}  # JSON mode
    )
    return json.loads(response.choices[0].message.content)
```

**Related terms:** Agent, Brain, Reasoning, Token

---

## M

### Memory

**Definition:** The component that stores information an agent needs to remember. Memory can be short-term (current conversation) or long-term (persisted across sessions). It helps agents maintain context, learn from past actions, and avoid repeating mistakes.

**Example:**
```python
class AgentMemory:
    def __init__(self, max_short_term=10, long_term_db=None):
        self.short_term = []           # Recent interactions
        self.long_term = long_term_db   # Persistent storage
    
    def store_short_term(self, item):
        """Store in working memory (limited size)."""
        self.short_term.append(item)
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)  # Remove oldest
    
    def store_long_term(self, key, value, importance=0.5):
        """Store in persistent memory."""
        if self.long_term:
            self.long_term.store(key, value, importance)
    
    def recall(self, query: str, scope: str = "short") -> list:
        """Retrieve relevant memories."""
        if scope == "short":
            return [m for m in self.short_term if query in str(m)]
        elif scope == "long" and self.long_term:
            return self.long_term.search(query)
        return []
    
    def summarize(self) -> str:
        """Get a summary of important memories."""
        return "\n".join(str(m) for m in self.short_term[-5:])

# Usage
memory = AgentMemory(max_short_term=10)
memory.store_short_term({"action": "search", "result": "found answer"})
memory.store_long_term("user_prefers_celsius", True, importance=0.8)
```

**Related terms:** State, Context, Short-term Memory, Long-term Memory

---

## O

### Observation

**Definition:** The result or feedback received after an agent performs an action. Observations are how agents learn about the effects of their actions and the current state of the environment.

**Example:**
```python
class Observation:
    def __init__(self, content, source, success=True, metadata=None):
        self.content = content
        self.source = source
        self.success = success
        self.metadata = metadata or {}
    
    def __str__(self):
        status = "✓" if self.success else "✗"
        return f"[{status}] {self.source}: {self.content[:100]}"

# Observations in agent loop
def agent_step(agent, action):
    # Execute action
    raw_result = agent.tools[action.name](action.input)
    
    # Create observation
    observation = Observation(
        content=raw_result,
        source=action.name,
        success=not raw_result.startswith("Error"),
        metadata={"action": action, "timestamp": time.time()}
    )
    
    # Feed observation back to agent
    agent.context.add_observation(observation)
    
    return observation
```

**Related terms:** Action, Agent Loop, Environment

---

## P

### Perception

**Definition:** The process by which an agent gathers information about its environment. Perception is the first step in the agent loop — before an agent can reason or act, it must understand what's happening around it.

**Example:**
```python
class AgentPerception:
    def __init__(self):
        self.sensors = {}  # Different perception channels
    
    def add_sensor(self, name, func):
        """Register a new perception channel."""
        self.sensors[name] = func
    
    def perceive(self) -> dict:
        """Gather all available information."""
        observations = {}
        for name, sensor in self.sensors.items():
            try:
                observations[name] = sensor()
            except Exception as e:
                observations[name] = {"error": str(e)}
        return observations

# Example sensors
def read_user_input():
    """Perceive user's message."""
    return input("You: ")

def read_tool_output():
    """Perceive results from tool execution."""
    # Read from tool output buffer
    pass

def read_environment():
    """Perceive environment state."""
    return {"time": datetime.now(), "status": "running"}
```

**Related terms:** Observation, Environment, Agent Loop

---

### Planning

**Definition:** The process by which an agent breaks down a complex goal into actionable steps. Planning can be done upfront (before acting) or dynamically (adapting as new information is discovered).

**Example:**
```python
def plan_with_llm(goal: str, llm) -> list:
    """Use LLM to generate a plan."""
    response = llm.generate(f"""
    Create a step-by-step plan to achieve: {goal}
    
    Return a JSON list of steps, each with:
    - description: What to do
    - tools: Which tools to use
    - dependencies: Steps that must complete first
    """)
    
    return json.loads(response)

# Example output
plan = [
    {"step": 1, "description": "Gather requirements", "tools": ["ask_user"], "dependencies": []},
    {"step": 2, "description": "Research solutions", "tools": ["search", "read_docs"], "dependencies": [1]},
    {"step": 3, "description": "Implement solution", "tools": ["write_code"], "dependencies": [2]},
    {"step": 4, "description": "Test and verify", "tools": ["run_tests"], "dependencies": [3]}
]
```

**Related terms:** Goal, Task Decomposition, ReAct

---

## R

### Reasoning

**Definition:** The LLM's process of analyzing information, considering options, and deciding what action to take. Reasoning is what makes agents more than simple scripts — they can handle novel situations by thinking through them.

**Example:**
```python
def agent_reason(context: dict, llm) -> str:
    """
    Agent reasons about the current situation.
    
    This is the 'Think' step in ReAct.
    """
    prompt = f"""
    You are an AI agent working on: {context['goal']}
    
    Current state: {context['current_state']}
    Available tools: {context['available_tools']}
    History so far: {context['history']}
    
    Think about what you should do next.
    Consider:
    1. What information do you have?
    2. What information do you need?
    3. Which tool can help you get it?
    4. What's the most efficient approach?
    
    Respond with your reasoning.
    """
    
    return llm.generate(prompt)

# Chain-of-Thought reasoning
def chain_of_thought(question: str, llm) -> str:
    """Explicit step-by-step reasoning."""
    prompt = f"""
    Question: {question}
    
    Let's think step by step:
    Step 1: 
    Step 2: 
    Step 3: 
    Answer:
    """
    return llm.generate(prompt)
```

**Related terms:** LLM, Planning, ReAct, Chain-of-Thought

---

## S

### State

**Definition:** The current condition of an agent and its environment at any point in time. State includes the agent's memory, current context, environment variables, and any other relevant information.

**Example:**
```python
@dataclass
class AgentState:
    """Complete representation of agent state."""
    # Agent internals
    goal: str
    plan: list
    current_step: int
    
    # Memory
    short_term_memory: list
    long_term_memory: dict
    
    # Environment
    environment: dict
    
    # Conversation
    messages: list
    
    def snapshot(self) -> dict:
        """Create a snapshot of current state."""
        return {
            "goal": self.goal,
            "plan": self.plan,
            "current_step": self.current_step,
            "memory_size": len(self.short_term_memory),
            "message_count": len(self.messages),
            "timestamp": time.time()
        }
    
    def restore(self, snapshot: dict):
        """Restore state from a snapshot."""
        self.goal = snapshot["goal"]
        self.plan = snapshot["plan"]
        self.current_step = snapshot["current_step"]
```

**Related terms:** Memory, Context, Environment

---

## T

### Tool

**Definition:** An external function or service that an agent can invoke to perform actions beyond what the LLM can do natively. Tools extend an agent's capabilities — they can search the web, query databases, execute code, control hardware, and more.

**Example:**
```python
from typing import Callable

class Tool:
    def __init__(self, name: str, description: str, func: Callable, 
                 parameters: dict = None):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters or {}
    
    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters."""
        try:
            result = self.func(**kwargs)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

# Registering tools
def search(query: str) -> str:
    """Search the web."""
    # Implementation...
    return "Search results..."

def calculate(expression: str) -> str:
    """Evaluate math."""
    return str(eval(expression))

tools = [
    Tool("search", "Search the web", search, {"query": {"type": "string"}}),
    Tool("calculate", "Calculate math", calculate, {"expression": {"type": "string"}}),
]
```

**Related terms:** Action, Function Calling, Tool Use

---

### Token

**Definition:** The basic unit of text that LLMs process. Tokens are typically parts of words (e.g., "agent" might be 1 token, "artificial" might be 2 tokens: "artif" + "icial"). Token counts affect cost, latency, and context window usage.

**Example:**
```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Token awareness
def manage_token_budget(messages: list, max_tokens: int = 4000):
    """Ensure messages fit within token budget."""
    total = 0
    kept = []
    
    for msg in reversed(messages):
        msg_tokens = count_tokens(msg["content"])
        if total + msg_tokens <= max_tokens:
            kept.insert(0, msg)
            total += msg_tokens
        else:
            break
    
    return kept, total

# Usage
text = "AI agents are autonomous systems"
tokens = count_tokens(text)
print(f"Text: '{text}' = {tokens} tokens")
# Text: 'AI agents are autonomous systems' = 6 tokens
```

**Related terms:** Context Window, LLM, Cost

---

## Quick Reference: Key Relationships

```
┌─────────────────────────────────────────────────────────┐
│                  Agent Fundamentals                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  LLM (Brain) ◄─────► Memory (State)                    │
│       │                     │                           │
│       │ Reasoning           │ Context                   │
│       │                     │                           │
│       ▼                     ▼                           │
│  ┌─────────────────────────────────┐                   │
│  │         Agent Loop              │                   │
│  │  Perceive → Think → Act → Observe │                 │
│  └────────────┬────────────────────┘                   │
│               │                                        │
│               ▼                                        │
│  ┌─────────┐     ┌─────────────────┐                  │
│  │  Tools  │────►│   Environment   │                  │
│  └─────────┘     └─────────────────┘                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 01](./01-agent-fundamentals-lecture.md)** | **[Next: Lecture 02 →](./02-tool-calling-glossary.md)**
