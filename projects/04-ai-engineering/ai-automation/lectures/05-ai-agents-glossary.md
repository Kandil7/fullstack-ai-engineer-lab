# Glossary: AI Agents

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Agent | Autonomous AI system | Perceives, reasons, acts |
| Tool | External capability | Extends agent abilities |
| ReAct | Reasoning + Acting pattern | Most common agent architecture |
| Memory | Stored context | Short-term, long-term, episodic |
| Planning | Task decomposition | Multi-step reasoning |
| Action | Agent operation | Tool use or response |
| Observation | Action result | Feedback for next step |
| Goal | Desired outcome | Drives agent behavior |
| Iteration | Single loop cycle | Think → Act → Observe |
| Termination | Stop condition | Prevents infinite loops |
| Error Recovery | Handling failures | Graceful degradation |
| Autonomous | Self-directed | Goal-driven behavior |

---

## Detailed Definitions

### Agent

**Definition:** An autonomous AI system that can perceive its environment, make decisions, and take actions to achieve goals. Agents combine LLMs with tools, memory, and planning capabilities.

**Example:**
```python
class SimpleAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.memory = []
    
    def run(self, goal):
        while not self.is_done():
            # Observe current state
            state = self.observe()
            
            # Think about what to do
            action = self.think(state, goal)
            
            # Act on decision
            result = self.act(action)
            
            # Update memory
            self.memory.append(result)
        
        return self.get_answer()
```

**Related Terms:** Tool, Memory, Planning, Autonomous

**Key Components:**
- LLM (brain/reasoning)
- Tools (capabilities)
- Memory (context)
- Loop (execution cycle)

---

### Tool

**Definition:** An external capability that an agent can use to interact with the world. Tools extend the agent beyond text generation to actions like web search, file operations, or API calls.

**Example:**
```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class Tool:
    name: str
    description: str
    function: Callable
    
    def execute(self, **kwargs):
        return self.function(**kwargs)

# Example tools
search_tool = Tool(
    name="search",
    description="Search the web for information",
    function=lambda query: f"Results for {query}"
)

file_tool = Tool(
    name="read_file",
    description="Read a file",
    function=lambda path: open(path).read()
)
```

**Related Terms:** Function Calling, API, Capability

**Common Types:**
- Search: Web, document, database
- Read/Write: Files, databases
- Compute: Calculations, analysis
- Communication: Email, messaging

---

### ReAct

**Definition:** Reasoning + Acting - an agent pattern where the LLM alternates between reasoning about what to do and taking actions. The most common agent architecture.

**Example:**
```python
# ReAct loop
for step in range(max_steps):
    # Reason: Think about what to do
    thought = llm.generate(f"""
    Goal: {goal}
    Current state: {current_state}
    What should I do next?
    """)
    
    # Act: Execute the chosen action
    if "use_tool" in thought:
        result = use_tool(thought)
    else:
        return thought  # Final answer
    
    # Observe: See the result
    current_state += f"\n{result}"
```

**Related Terms:** Chain-of-Thought, Tool Use, Loop

**Pattern:**
1. **Thought:** Reason about current state
2. **Action:** Choose and execute tool
3. **Observation:** See result
4. Repeat until done

---

### Memory

**Definition:** The system that stores and retrieves information for an agent. Enables context retention across steps and learning from experience.

**Example:**
```python
class AgentMemory:
    def __init__(self):
        self.short_term = []  # Current conversation
        self.long_term = []   # Important facts
        self.episodic = []    # Past experiences
    
    def add(self, content, memory_type="short_term"):
        if memory_type == "short_term":
            self.short_term.append(content)
        elif memory_type == "long_term":
            self.long_term.append(content)
        elif memory_type == "episodic":
            self.episodic.append(content)
    
    def get_context(self):
        return "\n".join(self.short_term[-10:])
```

**Related Terms:** Context, State, Learning

**Types:**
- **Short-term:** Current conversation/task
- **Long-term:** Persistent facts/knowledge
- **Episodic:** Past experiences/outcomes

---

### Planning

**Definition:** The process of breaking down complex goals into manageable steps. Enables agents to tackle multi-step tasks systematically.

**Example:**
```python
class Planner:
    def create_plan(self, goal):
        prompt = f"""
        Goal: {goal}
        
        Create a step-by-step plan:
        1. [First step]
        2. [Second step]
        ...
        """
        return llm.generate(prompt)
    
    def execute_plan(self, plan):
        results = []
        for step in plan:
            result = self.execute_step(step)
            results.append(result)
        return results
```

**Related Terms:** Decomposition, Strategy, Goal

**Approaches:**
- Sequential: One step at a time
- Hierarchical: Break into sub-goals
- Adaptive: Modify plan based on results

---

### Action

**Definition:** An operation the agent decides to perform, typically using a tool. Actions are the "doing" part of the agent loop.

**Example:**
```python
@dataclass
class Action:
    type: str  # "tool_use" or "respond"
    tool_name: str = ""
    tool_input: str = ""
    response: str = ""

# Agent decides on action
action = Action(
    type="tool_use",
    tool_name="search",
    tool_input="latest AI news"
)

# Execute action
if action.type == "tool_use":
    result = tools[action.tool_name].execute(action.tool_input)
```

**Related Terms:** Tool Use, Decision, Execution

**Action Types:**
- Tool use: External operation
- Response: Generate answer
- Finish: Task complete

---

### Observation

**Definition:** The result or feedback from executing an action. Observations inform the agent's next decision.

**Example:**
```python
# Agent takes action
action = "search('machine learning trends')"
observation = execute(action)

# Observation: "Top results: 1. LLMs dominate... 2. RAG adoption..."

# Agent uses observation for next thought
thought = f"""
I searched for ML trends and found that LLMs and RAG are popular.
I should get more specific information about...
"""
```

**Related Terms:** Result, Feedback, State Update

**Role in Loop:**
1. Thought → Decision
2. Action → Execution
3. Observation → Result
4. Next Thought (informed by observation)

---

### Goal

**Definition:** The desired outcome or objective the agent is trying to achieve. Goals drive agent behavior and decision-making.

**Example:**
```python
# Simple goal
goal = "Answer: What is the capital of France?"

# Complex goal
goal = """Research and write a report on the benefits of RAG systems:
1. Find at least 5 benefits
2. Include real-world examples
3. Write a 500-word summary
4. Save to a file"""
```

**Related Terms:** Objective, Task, Purpose

**Goal Types:**
- Simple: Single answer
- Complex: Multi-step task
- Open-ended: Exploration

---

### Iteration

**Definition:** A single cycle of the agent's think-act-observe loop. Each iteration moves the agent closer to the goal.

**Example:**
```python
max_iterations = 10

for iteration in range(max_iterations):
    print(f"\n=== Iteration {iteration + 1} ===")
    
    # Think
    thought = agent.think()
    print(f"Thought: {thought}")
    
    # Act
    action = agent.decide_action(thought)
    result = agent.execute(action)
    print(f"Action: {action}")
    print(f"Result: {result}")
    
    # Check if done
    if agent.is_done():
        return agent.get_answer()

return "Max iterations reached"
```

**Related Terms:** Loop, Cycle, Step

**Considerations:**
- Max iterations to prevent infinite loops
- Early stopping when goal achieved
- Cost per iteration (API calls)

---

### Termination

**Definition:** The condition that stops the agent loop. Prevents infinite loops and ensures the agent completes or gives up gracefully.

**Example:**
```python
class AgentLoop:
    def __init__(self, max_iterations=10, timeout=60):
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.start_time = time.time()
    
    def should_continue(self):
        # Check iteration limit
        if self.iteration >= self.max_iterations:
            return False
        
        # Check timeout
        if time.time() - self.start_time > self.timeout:
            return False
        
        # Check if goal achieved
        if self.goal_achieved():
            return False
        
        return True
    
    def run(self, goal):
        while self.should_continue():
            self.iteration += 1
            self.step()
        
        return self.get_result()
```

**Related Terms:** Stop Condition, Loop Control

**Common Conditions:**
- Max iterations reached
- Timeout exceeded
- Goal achieved
- Error threshold exceeded

---

### Error Recovery

**Definition:** The agent's ability to handle failures and continue working toward the goal. Includes retrying, alternative approaches, and graceful degradation.

**Example:**
```python
class ResilientAgent:
    def execute_with_recovery(self, action, max_retries=3):
        for attempt in range(max_retries):
            try:
                result = self.execute(action)
                return result
            except ToolError as e:
                if attempt < max_retries - 1:
                    # Try alternative approach
                    action = self.get_alternative(action, e)
                else:
                    # Give up on this action
                    return f"Failed after {max_retries} attempts: {e}"
```

**Related Terms:** Retry, Fallback, Resilience

**Strategies:**
- Retry with same tool
- Try alternative tool
- Reformulate approach
- Skip and continue
- Graceful failure

---

### Autonomous

**Definition:** The ability of an agent to operate independently, making decisions and taking actions without constant human input.

**Example:**
```python
# Non-autonomous (user-driven)
while True:
    user_input = input("What should I do? ")
    agent.execute(user_input)

# Autonomous (goal-driven)
goal = "Research and summarize the topic"
result = agent.run(goal)  # Runs until complete
print(result)
```

**Related Terms:** Self-directed, Independent, Goal-driven

**Levels:**
- Assisted: Human guides every step
- Semi-autonomous: Agent decides actions, human approves
- Fully autonomous: Agent completes task independently

---

### State

**Definition:** The current condition of the agent, including memory, context, and progress toward the goal.

**Example:**
```python
@dataclass
class AgentState:
    goal: str
    current_step: int
    memory: List[str]
    results: List[str]
    errors: List[str]
    
    def update(self, action, result):
        self.current_step += 1
        self.memory.append(f"Step {self.current_step}: {action}")
        self.results.append(result)
    
    def get_summary(self):
        return f"""
        Goal: {self.goal}
        Step: {self.current_step}
        Results so far: {len(self.results)}
        Errors: {len(self.errors)}
        """
```

**Related Terms:** Context, Memory, Progress

**Components:**
- Current goal
- Step number
- Memory contents
- Results collected
- Errors encountered

---

### Prompt Engineering (for Agents)

**Definition:** Crafting effective prompts that guide the LLM to make good decisions as an agent, including tool selection and reasoning.

**Example:**
```python
AGENT_SYSTEM_PROMPT = """You are an AI agent with access to tools.

Your role:
- Think carefully before acting
- Use tools when you need information
- Verify your answers
- Be efficient

Available tools:
{tool_descriptions}

Always respond in this format:
Thought: [your reasoning]
Action: [tool_name]
Action Input: [input]

When done:
Thought: I have the answer
Final Answer: [your response]
"""
```

**Related Terms:** System Prompt, Instructions, Guidelines

**Key Elements:**
- Role definition
- Tool descriptions
- Response format
- Constraints

---

### Tool Use

**Definition:** The mechanism by which an agent invokes external tools to accomplish tasks. Includes tool selection, input generation, and result interpretation.

**Example:**
```python
# Tool selection
available_tools = {
    "search": search_tool,
    "calculator": calc_tool,
    "file_reader": file_tool
}

# Agent selects tool
thought = "I need to find information about X"
action = "search"
tool_input = "latest research on X"

# Execute
result = available_tools[action].execute(query=tool_input)

# Interpret result
thought = f"Search returned: {result}. I should now..."
```

**Related Terms:** Function Calling, API, Capability

**Considerations:**
- Tool selection accuracy
- Input validation
- Error handling
- Result interpretation

---

### Function Calling

**Definition:** The LLM's ability to generate structured calls to external functions/tools. Enables seamless tool integration.

**Example:**
```python
# Define function for LLM
functions = [
    {
        "name": "search_web",
        "description": "Search the web",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }
]

# LLM generates function call
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Find info about AI"}],
    functions=functions,
    function_call="auto"
)

# Parse function call
function_call = response.choices[0].message.function_call
if function_call:
    args = json.loads(function_call.arguments)
    result = search_web(**args)
```

**Related Terms:** Tool Use, API, Structured Output

**Benefits:**
- Structured output
- Type safety
- Easy integration
- LLM-native support

---

### Multi-Step Reasoning

**Definition:** The ability to break down complex problems into sequential reasoning steps. Essential for agents tackling complex tasks.

**Example:**
```python
# Multi-step reasoning
thoughts = []
thoughts.append("First, I need to find the user's location")
location = get_location()

thoughts.append(f"User is in {location}. Now I need local weather")
weather = get_weather(location)

thoughts.append(f"Weather is {weather}. Now I can answer the question")
answer = f"In {location}, it's currently {weather}"
```

**Related Terms:** Chain-of-Thought, Planning, Decomposition

**Importance:**
- Complex problem solving
- Transparent reasoning
- Error detection
- Quality improvement

---

### Fallback

**Definition:** A backup plan or alternative approach when the primary method fails. Ensures the agent can still provide value even when tools fail.

**Example:**
```python
def search_with_fallback(query):
    # Try primary tool
    try:
        result = web_search(query)
        if result:
            return result
    except Exception:
        pass
    
    # Try alternative
    try:
        result = database_search(query)
        if result:
            return result
    except Exception:
        pass
    
    # Final fallback
    return f"I couldn't find information about '{query}'. Here's what I know from my training..."
```

**Related Terms:** Error Recovery, Resilience, Backup

**Strategies:**
- Alternative tools
- Cached results
- Training knowledge
- Graceful degradation

---

## Summary

Understanding these terms is essential for building effective AI agents:

1. **Agent:** Autonomous system with reasoning and action
2. **Tool:** External capability for interaction
3. **ReAct:** Reasoning + Acting pattern
4. **Memory:** Context retention system
5. **Planning:** Task decomposition
6. **Action:** Agent operations
7. **Observation:** Action results
8. **Goal:** Desired outcome
9. **Iteration:** Single loop cycle
10. **Termination:** Stop condition

**Next:** See Lecture 06 for AI evaluation.
