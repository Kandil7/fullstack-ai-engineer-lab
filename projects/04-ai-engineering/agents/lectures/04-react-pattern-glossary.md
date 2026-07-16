# Glossary: ReAct Pattern

> Terms defined in alphabetical order. Each entry includes: definition, example usage, code snippet, and related terms.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Action | Tool invocation by the agent | Tool, Execution |
| Action Input | Parameters passed to a tool | Arguments, Parameters |
| Chain-of-Thought | Step-by-step reasoning process | Reasoning, Thinking |
| Final Answer | Agent's complete response to the question | Output, Response |
| Finish | Signal that agent has completed the task | Done, Complete |
| Loop Detection | Identifying when agent repeats itself | Self-Correction |
| Observation | Result returned from tool execution | Result, Feedback |
| ReAct | Reasoning + Acting pattern | Agent, Pattern |
| Reflection | Agent evaluating its own reasoning | Self-Correction |
| Step | Single iteration of think-act-observe | Iteration, Cycle |
| Thought | Agent's reasoning about what to do | Reasoning, Planning |
| Trace | Complete record of agent's steps | Log, History |
| Trajectory | Path of states agent has visited | Trace, Path |

---

## A

### Action

**Definition:** An operation that the agent performs by invoking a tool. Actions are the way agents effect change in the world or gather information. In ReAct, actions always follow a Thought.

**Example:**
```
Thought: I need to find the current weather in Paris.
Action: get_weather
Action Input: Paris, France
```

**Code:**
```python
@dataclass
class Action:
    """Represents an action taken by the agent."""
    name: str
    input_data: str
    timestamp: float = None
    
    def execute(self, tools: dict) -> str:
        """Execute this action using the appropriate tool."""
        if self.name not in tools:
            return f"Error: Unknown action '{self.name}'"
        
        try:
            result = tools[self.name](self.input_data)
            return str(result)
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"

# Usage
action = Action(name="search", input_data="AI agents")
result = action.execute(tools)
```

**Related terms:** Tool, Action Input, Execution

---

### Action Input

**Definition:** The parameters or arguments passed to a tool when executing an action. Action inputs must match the tool's expected schema.

**Example:**
```
Action: search_database
Action Input: SELECT * FROM users WHERE age > 30
```

**Code:**
```python
def parse_action_input(text: str) -> str:
    """Extract action input from LLM response."""
    import re
    match = re.search(r"Action Input:\s*(.+?)(?=Observation:|$)", 
                      text, re.DOTALL)
    return match.group(1).strip() if match else ""

# Validation
def validate_action_input(tool_name: str, action_input: str, 
                         tool_schemas: dict) -> tuple[bool, str]:
    """Validate action input against tool schema."""
    if tool_name not in tool_schemas:
        return False, f"Unknown tool: {tool_name}"
    
    schema = tool_schemas[tool_name]
    
    # Basic validation
    if not action_input:
        return False, "Action input is empty"
    
    # Type-specific validation
    if schema.get("type") == "json":
        try:
            import json
            json.loads(action_input)
        except json.JSONDecodeError:
            return False, "Invalid JSON input"
    
    return True, "Valid"
```

**Related terms:** Action, Parameters, Schema

---

## C

### Chain-of-Thought (CoT)

**Definition:** A prompting technique where the LLM is encouraged to show its reasoning step by step before arriving at an answer. ReAct extends CoT by adding action and observation steps.

**Example:**
```
Without CoT:
Q: What is the capital of France and its population?
A: Paris, 2.1 million

With CoT:
Q: What is the capital of France and its population?
Thought: France is a country in Europe. Its capital is Paris. 
I need to find the current population.
Action: search
Action Input: Paris France population 2024
Observation: Paris has approximately 2.1 million people in the city proper.
Thought: I now have both pieces of information.
Final Answer: The capital of France is Paris, with a population of approximately 2.1 million people.
```

**Code:**
```python
def chain_of_thought_prompt(question: str) -> str:
    """Create a CoT prompt."""
    return f"""Question: {question}

Let's think step by step:

Step 1: """
```

**Related terms:** Reasoning, ReAct, Prompting

---

## F

### Final Answer

**Definition:** The agent's complete response to the user's question, provided when the agent has gathered enough information to answer. In ReAct, the Final Answer signals the end of the think-act-observe loop.

**Example:**
```
Thought: I now have enough information to answer the question.
Final Answer: The Eiffel Tower is 330 meters tall and was built in 1889 for the World's Fair in Paris.
```

**Code:**
```python
def extract_final_answer(response: str) -> str | None:
    """Extract the final answer from a ReAct response."""
    import re
    
    match = re.search(r"Final Answer:\s*(.+)", response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# Check if response contains final answer
response = """Thought: I have all the information needed.
Final Answer: The answer is 42."""

answer = extract_final_answer(response)
print(answer)  # "The answer is 42."
```

**Related terms:** Output, Response, Finish

---

## L

### Loop Detection

**Definition:** Identifying when an agent is repeating the same thoughts, actions, or observations without making progress. Loop detection enables self-correction mechanisms.

**Example:**
```python
from collections import Counter
from typing import List

class LoopDetector:
    """Detects when agent is stuck in a loop."""
    
    def __init__(self, window_size: int = 3, threshold: float = 0.8):
        self.window_size = window_size
        self.threshold = threshold
        self.history: List[dict] = []
    
    def add_step(self, thought: str, action: str, observation: str):
        """Record a step for analysis."""
        self.history.append({
            "thought": thought,
            "action": action,
            "observation": observation
        })
    
    def detect_action_loop(self) -> bool:
        """Detect if agent is repeating the same action."""
        if len(self.history) < self.window_size:
            return False
        
        recent = self.history[-self.window_size:]
        actions = [h["action"] for h in recent]
        
        # All same action
        return len(set(actions)) == 1 and actions[0] is not None
    
    def detect_thought_loop(self) -> bool:
        """Detect if agent is repeating the same thought."""
        if len(self.history) < self.window_size:
            return False
        
        recent = self.history[-self.window_size:]
        thoughts = [h["thought"] for h in recent]
        
        # Similar thoughts (simple similarity)
        if all(thoughts):
            from difflib import SequenceMatcher
            similarities = []
            for i in range(len(thoughts) - 1):
                sim = SequenceMatcher(None, thoughts[i], thoughts[i+1]).ratio()
                similarities.append(sim)
            
            return sum(similarities) / len(similarities) > self.threshold
        
        return False
    
    def detect_error_loop(self) -> bool:
        """Detect if agent keeps getting errors."""
        if len(self.history) < 2:
            return False
        
        recent = self.history[-3:]
        errors = [h for h in recent if "Error" in str(h.get("observation", ""))]
        
        return len(errors) >= 2

# Usage
detector = LoopDetector()
detector.add_step("Searching...", "search", "Result 1")
detector.add_step("Searching...", "search", "Result 2")
detector.add_step("Searching...", "search", "Result 3")

if detector.detect_action_loop():
    print("Warning: Agent is stuck in a loop!")
```

**Related terms:** Self-Correction, Stuck, Repetition

---

## O

### Observation

**Definition:** The result or feedback received after an agent performs an action. Observations provide the agent with new information to inform its next thought and action.

**Example:**
```
Thought: I need to look up the weather in New York.
Action: get_weather
Action Input: New York
Observation: Current weather in New York: 72°F, partly cloudy, humidity 45%
```

**Code:**
```python
@dataclass
class Observation:
    """Structured observation from tool execution."""
    content: str
    source_tool: str
    success: bool
    timestamp: float
    metadata: dict = None
    
    def to_context_string(self) -> str:
        """Format for inclusion in LLM context."""
        status = "Success" if self.success else "Error"
        return f"[{status}] {self.source_tool}: {self.content[:500]}"
    
    def is_error(self) -> bool:
        """Check if observation represents an error."""
        return not self.success or "Error" in self.content

# Create observation
obs = Observation(
    content="Paris: 22°C, sunny",
    source_tool="get_weather",
    success=True,
    timestamp=time.time()
)

print(obs.to_context_string())
# [Success] get_weather: Paris: 22°C, sunny
```

**Related terms:** Result, Feedback, Tool Output

---

## R

### ReAct

**Definition:** A prompting pattern that combines Reasoning and Acting in an interleaved manner. The agent alternates between thinking (reasoning about what to do) and acting (using tools to gather information or effect change).

**Example:**
```
Question: What is the tallest building in the world and how tall is it?

Thought: I need to find information about the tallest building. Let me search for this.
Action: web_search
Action Input: tallest building in the world
Observation: The Burj Khalifa in Dubai is the tallest building at 828 meters.

Thought: I have the answer now.
Final Answer: The tallest building in the world is the Burj Khalifa in Dubai, standing at 828 meters tall.
```

**Code:**
```python
class ReActPattern:
    """
    Implementation of the ReAct pattern.
    """
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def execute(self, question: str, max_steps: int = 10) -> str:
        """Execute the ReAct loop."""
        context = [f"Question: {question}"]
        
        for step in range(max_steps):
            # Generate next step
            prompt = self._build_prompt(context)
            response = self.llm(prompt)
            
            # Parse response
            if "Final Answer:" in response:
                return self._extract_final_answer(response)
            
            # Execute action
            action, action_input = self._parse_action(response)
            if action:
                observation = self.tools[action](action_input)
                context.append(f"Thought: {self._extract_thought(response)}")
                context.append(f"Action: {action}")
                context.append(f"Action Input: {action_input}")
                context.append(f"Observation: {observation}")
        
        return "Maximum steps reached"
```

**Related terms:** Reasoning, Acting, Agent Pattern

---

### Reflection

**Definition:** The process of an agent evaluating its own reasoning and actions to identify errors, improve strategies, or detect when it's stuck. Reflection enables self-correction.

**Example:**
```python
class ReflectionModule:
    """Enables agent to reflect on its performance."""
    
    def __init__(self, llm):
        self.llm = llm
    
    def reflect_on_trace(self, trace: list) -> str:
        """Analyze the agent's trace and provide reflection."""
        trace_summary = "\n".join([
            f"Step {i+1}: {step}"
            for i, step in enumerate(trace)
        ])
        
        prompt = f"""Analyze this agent trace and identify:
1. What went well
2. What went wrong
3. What should be tried differently

Trace:
{trace_summary}

Reflection:"""
        
        return self.llm(prompt)
    
    def should_retry(self, trace: list, max_retries: int = 3) -> bool:
        """Determine if agent should retry."""
        # Check for errors
        errors = [s for s in trace if "Error" in str(s)]
        if len(errors) > max_retries:
            return False
        
        # Check for loops
        actions = [getattr(s, 'action', None) for s in trace]
        if len(set(actions[-3:])) == 1:
            return True  # Try different approach
        
        return False
```

**Related terms:** Self-Correction, Evaluation, Learning

---

## T

### Thought

**Definition:** The agent's internal reasoning about the current situation and what action to take next. In ReAct, every action must be preceded by a thought explaining the reasoning.

**Example:**
```
Thought: I found that Python was created by Guido van Rossum. Now I should find out when it was created to give a complete answer.
```

**Code:**
```python
def generate_thought(context: list, llm) -> str:
    """Generate a thought based on current context."""
    prompt = f"""Based on the following context, think about what to do next:

{chr(10).join(context)}

Thought:"""
    
    response = llm(prompt)
    
    # Extract thought
    if response.startswith("Thought:"):
        return response[8:].strip()
    return response.strip()

def validate_thought(thought: str) -> bool:
    """Validate that a thought makes sense."""
    if not thought:
        return False
    
    # Should not be too short
    if len(thought) < 10:
        return False
    
    # Should indicate reasoning
    reasoning_indicators = [
        "need to", "should", "because", "therefore",
        "first", "next", "now", "based on"
    ]
    
    return any(indicator in thought.lower() 
              for indicator in reasoning_indicators)
```

**Related terms:** Reasoning, Planning, Chain-of-Thought

---

### Trace

**Definition:** A complete record of all steps taken by a ReAct agent, including thoughts, actions, action inputs, and observations. Traces are essential for debugging and analysis.

**Example:**
```python
from dataclasses import dataclass
from typing import List, Optional
import json
from datetime import datetime

@dataclass
class TraceStep:
    """Single step in a ReAct trace."""
    step_number: int
    thought: str
    action: Optional[str]
    action_input: Optional[str]
    observation: Optional[str]
    timestamp: str
    
    def to_dict(self) -> dict:
        return {
            "step": self.step_number,
            "thought": self.thought,
            "action": self.action,
            "action_input": self.action_input,
            "observation": self.observation,
            "timestamp": self.timestamp
        }

class ReActTrace:
    """Complete trace of a ReAct execution."""
    
    def __init__(self, question: str):
        self.question = question
        self.steps: List[TraceStep] = []
        self.final_answer: Optional[str] = None
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
    
    def add_step(self, thought: str, action: str = None,
                action_input: str = None, observation: str = None):
        """Add a step to the trace."""
        step = TraceStep(
            step_number=len(self.steps) + 1,
            thought=thought,
            action=action,
            action_input=action_input,
            observation=observation,
            timestamp=datetime.now().isoformat()
        )
        self.steps.append(step)
    
    def finish(self, answer: str):
        """Mark trace as complete."""
        self.final_answer = answer
        self.end_time = datetime.now()
    
    def to_dict(self) -> dict:
        """Export trace as dictionary."""
        return {
            "question": self.question,
            "steps": [s.to_dict() for s in self.steps],
            "final_answer": self.final_answer,
            "duration_seconds": (
                (self.end_time or datetime.now()) - self.start_time
            ).total_seconds()
        }
    
    def to_json(self) -> str:
        """Export trace as JSON."""
        return json.dumps(self.to_dict(), indent=2)
    
    def print_trace(self):
        """Pretty-print the trace."""
        print(f"\nTrace for: {self.question}")
        print("=" * 50)
        
        for step in self.steps:
            print(f"\nStep {step.step_number}:")
            print(f"  Thought: {step.thought}")
            if step.action:
                print(f"  Action: {step.action}")
                print(f"  Input: {step.action_input}")
            if step.observation:
                print(f"  Observation: {step.observation[:100]}...")
        
        print(f"\nFinal Answer: {self.final_answer}")

# Usage
trace = ReActTrace("What is the capital of France?")
trace.add_step(
    thought="I need to find the capital of France.",
    action="search",
    action_input="capital of France",
    observation="Paris is the capital of France."
)
trace.finish("Paris")
trace.print_trace()
```

**Related terms:** History, Log, Trajectory

---

## Quick Reference: ReAct Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    ReAct Execution Flow                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                           │
│  │   Question  │                                           │
│  └──────┬──────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │   Thought   │◄──────────────────┐                      │
│  └──────┬──────┘                   │                      │
│         │                          │                      │
│         ▼                          │                      │
│  ┌─────────────┐                   │                      │
│  │   Action    │                   │                      │
│  └──────┬──────┘                   │                      │
│         │                          │                      │
│         ▼                          │                      │
│  ┌─────────────┐                   │                      │
│  │ Observation │───────────────────┘                      │
│  └──────┬──────┘                                          │
│         │                                                  │
│         ├── More info needed ──► Loop back                │
│         │                                                  │
│         └── Enough info ──► ┌─────────────┐              │
│                             │Final Answer │              │
│                             └─────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 04](./04-react-pattern-lecture.md)** | **[Next: Lecture 05 →](./05-planning-reasoning-glossary.md)**
