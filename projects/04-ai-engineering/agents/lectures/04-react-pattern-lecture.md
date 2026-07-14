# Lecture 04: ReAct Pattern

## 🎯 Topic Overview

**ReAct** (Reasoning + Acting) is a prompting framework that combines chain-of-thought reasoning with action-taking in an interleaved manner. Rather than thinking first and then acting, or acting without thinking, ReAct agents alternate between reasoning about what to do and taking actions to gather information or effect change.

This pattern was introduced in the paper "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022) and has become one of the most widely used agent architectures.

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** the ReAct pattern and why it works
2. **Implement** a ReAct agent from scratch
3. **Design** effective prompts for ReAct agents
4. **Handle** multi-step reasoning with tool use
5. **Debug** ReAct agent failures
6. **Compare** ReAct to other agent patterns
7. **Optimize** ReAct for different use cases
8. **Build** production-ready ReAct agents

---

## 🧩 Key Concepts

### 1. The ReAct Loop

```
┌─────────────────────────────────────────────────────────────┐
│                     ReAct Pattern                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Thought 1: I need to find information about X              │
│      │                                                      │
│      ▼                                                      │
│  Action 1: search("information about X")                    │
│      │                                                      │
│      ▼                                                      │
│  Observation 1: [Search results...]                         │
│      │                                                      │
│      ▼                                                      │
│  Thought 2: Based on the results, I now know Y.             │
│             I need to verify by checking Z.                 │
│      │                                                      │
│      ▼                                                      │
│  Action 2: lookup("Z")                                      │
│      │                                                      │
│      ▼                                                      │
│  Observation 2: [Lookup results...]                         │
│      │                                                      │
│      ▼                                                      │
│  Thought 3: Now I have all the information needed.           │
│             The answer is W.                                 │
│      │                                                      │
│      ▼                                                      │
│  Finish: The answer is W.                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. ReAct vs. Other Patterns

| Pattern | Approach | Pros | Cons |
|---------|----------|------|------|
| **ReAct** | Think → Act → Observe (interleaved) | Transparent, debuggable | Can be slow |
| **Chain-of-Thought** | Think → Think → Think | Good reasoning | No actions |
| **Plan-then-Execute** | Plan all → Execute all | Efficient | Less adaptive |
| **Reflexion** | Act → Reflect → Improve | Learns from mistakes | Complex |

### 3. ReAct Prompt Template

```
Answer the following questions as best you can. You have access to the 
following tools:

{tool_descriptions}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
```

---

## 💻 Code Examples

### Example 1: Complete ReAct Agent

```python
"""
Complete ReAct Agent Implementation
Demonstrates the full ReAct pattern with tool use and reasoning.
"""
import re
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class AgentState(Enum):
    """Possible states of the ReAct agent."""
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    FINISHED = "finished"
    ERROR = "error"


@dataclass
class AgentStep:
    """A single step in the ReAct trace."""
    thought: Optional[str] = None
    action: Optional[str] = None
    action_input: Optional[str] = None
    observation: Optional[str] = None
    
    def __str__(self):
        parts = []
        if self.thought:
            parts.append(f"Thought: {self.thought}")
        if self.action:
            parts.append(f"Action: {self.action}")
        if self.action_input:
            parts.append(f"Action Input: {self.action_input}")
        if self.observation:
            parts.append(f"Observation: {self.observation}")
        return "\n".join(parts)


class ReActAgent:
    """
    A ReAct agent that interleaves reasoning and acting.
    
    Features:
    - Step-by-step reasoning with tool use
    - Full trace logging
    - Error handling and recovery
    - Configurable max steps
    """
    
    def __init__(self, llm_caller: Callable, tools: Dict[str, Callable],
                 max_steps: int = 10, verbose: bool = True):
        self.llm = llm_caller
        self.tools = tools
        self.max_steps = max_steps
        self.verbose = verbose
        self.steps: List[AgentStep] = []
        self.state = AgentState.THINKING
    
    def _build_system_prompt(self) -> str:
        """Build the ReAct system prompt."""
        tool_descriptions = "\n".join(
            f"- {name}: {func.__doc__ or 'No description'}"
            for name, func in self.tools.items()
        )
        tool_names = ", ".join(self.tools.keys())
        
        return f"""You are a helpful assistant that uses tools to answer questions.

You have access to the following tools:
{tool_descriptions}

To use a tool, you must follow this EXACT format:

Thought: [your reasoning about what to do next]
Action: [tool name from: {tool_names}]
Action Input: [input for the chosen tool]

When you have gathered enough information to answer, use:

Thought: I now have enough information to answer
Final Answer: [your complete answer]

Important rules:
1. Always start with a Thought
2. Only use tools that are listed above
3. Wait for the Observation after each Action
4. You may repeat Thought/Action/Observation multiple times
5. Stop when you have the final answer
"""
    
    def _parse_llm_response(self, response: str) -> Dict[str, Optional[str]]:
        """Parse the LLM response into components."""
        result = {
            "thought": None,
            "action": None,
            "action_input": None,
            "final_answer": None
        }
        
        # Extract thought
        thought_match = re.search(r"Thought:\s*(.+?)(?=Action:|Final Answer:|$)", 
                                  response, re.DOTALL)
        if thought_match:
            result["thought"] = thought_match.group(1).strip()
        
        # Check for final answer
        if "Final Answer:" in response:
            final_match = re.search(r"Final Answer:\s*(.+)", response, re.DOTALL)
            if final_match:
                result["final_answer"] = final_match.group(1).strip()
            return result
        
        # Extract action
        action_match = re.search(r"Action:\s*(.+?)(?=Action Input:|$)", 
                                 response, re.DOTALL)
        if action_match:
            result["action"] = action_match.group(1).strip()
        
        # Extract action input
        input_match = re.search(r"Action Input:\s*(.+)", response, re.DOTALL)
        if input_match:
            result["action_input"] = input_match.group(1).strip()
        
        return result
    
    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool and return the result."""
        if tool_name not in self.tools:
            return f"Error: Unknown tool '{tool_name}'. Available: {list(self.tools.keys())}"
        
        try:
            result = self.tools[tool_name](tool_input)
            return str(result)
        except Exception as e:
            return f"Error executing {tool_name}: {type(e).__name__}: {str(e)}"
    
    def _log(self, message: str):
        """Log messages when verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def run(self, question: str) -> str:
        """
        Run the ReAct agent on a question.
        
        Args:
            question: The question to answer
            
        Returns:
            The final answer
        """
        self.steps = []
        self.state = AgentState.THINKING
        
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Question: {question}"}
        ]
        
        self._log(f"\n{'='*60}")
        self._log(f"Question: {question}")
        self._log(f"{'='*60}")
        
        for step_num in range(1, self.max_steps + 1):
            self._log(f"\n--- Step {step_num} ---")
            
            # Get LLM response
            response = self.llm(messages)
            self._log(f"\n{response}")
            
            # Parse response
            parsed = self._parse_llm_response(response)
            
            # Create step record
            step = AgentStep(
                thought=parsed["thought"],
                action=parsed["action"],
                action_input=parsed["action_input"]
            )
            
            # Check for final answer
            if parsed["final_answer"]:
                self.state = AgentState.FINISHED
                step.observation = "Final answer provided"
                self.steps.append(step)
                return parsed["final_answer"]
            
            # Execute action
            if parsed["action"]:
                self.state = AgentState.ACTING
                observation = self._execute_tool(
                    parsed["action"], 
                    parsed["action_input"] or ""
                )
                step.observation = observation
                self._log(f"\nObservation: {observation}")
                
                # Add to messages for context
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user", 
                    "content": f"Observation: {observation}"
                })
            else:
                # No action or final answer - ask for clarification
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user",
                    "content": "Please provide either an Action or a Final Answer."
                })
            
            self.steps.append(step)
        
        # Max steps reached
        self.state = AgentState.ERROR
        return "Maximum steps reached without completing the task."
    
    def get_trace(self) -> str:
        """Get a formatted trace of all steps."""
        trace = ["ReAct Agent Trace:", "=" * 40]
        for i, step in enumerate(self.steps, 1):
            trace.append(f"\nStep {i}:")
            trace.append(str(step))
        return "\n".join(trace)


# === Usage Example ===

# Define tools
def search(query: str) -> str:
    """Search the web for information."""
    # Simulated search results
    results = {
        "python": "Python is a programming language created by Guido van Rossum.",
        "react": "React is a JavaScript library for building user interfaces.",
        "ai": "AI stands for Artificial Intelligence."
    }
    
    for key, value in results.items():
        if key in query.lower():
            return value
    return f"No results found for: {query}"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        # Safety: only allow basic math
        allowed = set("0123456789+-*/.() ")
        if all(c in allowed for c in expression):
            return str(eval(expression))
        return "Error: Invalid characters"
    except Exception as e:
        return f"Error: {str(e)}"

# Simple LLM mock (replace with real LLM call)
def mock_llm(messages):
    """Mock LLM that follows ReAct format."""
    last_msg = messages[-1]["content"]
    
    if "Question:" in last_msg:
        return "Thought: I need to search for information about this topic.\nAction: search\nAction Input: python"
    elif "Observation:" in last_msg:
        return "Thought: I now have enough information to answer.\nFinal Answer: Python is a programming language created by Guido van Rossum."
    return "Thought: I need more information.\nFinal Answer: I don't have enough information."

# Create and run agent
agent = ReActAgent(
    llm_caller=mock_llm,
    tools={"search": search, "calculate": calculate},
    max_steps=5,
    verbose=True
)

answer = agent.run("What is Python?")
print(f"\nFinal Answer: {answer}")
print(f"\n{agent.get_trace()}")
```

### Example 2: ReAct with Self-Correction

```python
"""
ReAct Agent with Self-Correction
Can detect and recover from reasoning errors.
"""
from typing import List

class SelfCorrectingReActAgent(ReActAgent):
    """
    Extended ReAct agent that can:
    - Detect when it's going in circles
    - Retry with different approaches
    - Reflect on failed attempts
    """
    
    def __init__(self, *args, max_retries: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = max_retries
        self.failed_attempts: List[str] = []
    
    def _detect_loop(self) -> bool:
        """Detect if agent is repeating the same actions."""
        if len(self.steps) < 3:
            return False
        
        # Check for repeated actions
        recent_actions = [s.action for s in self.steps[-3:]]
        if len(set(recent_actions)) == 1 and recent_actions[0] is not None:
            return True
        
        # Check for repeated thoughts
        recent_thoughts = [s.thought for s in self.steps[-3:]]
        if len(set(recent_thoughts)) == 1 and recent_thoughts[0] is not None:
            return True
        
        return False
    
    def _generate_reflection(self) -> str:
        """Generate a reflection prompt when stuck."""
        failed_actions = [s.action for s in self.steps if s.observation and "Error" in s.observation]
        
        return f"""I notice I'm repeating myself. Let me reflect:

Previous attempts:
{chr(10).join(f"- Tried: {a}" for a in failed_actions[-3:])}

I should try a completely different approach. Let me think about what other tools or strategies I could use."""
    
    def run_with_correction(self, question: str) -> str:
        """Run agent with self-correction capabilities."""
        self.steps = []
        retries = 0
        
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Question: {question}"}
        ]
        
        for step_num in range(1, self.max_steps + 1):
            # Check for loops
            if self._detect_loop():
                retries += 1
                if retries > self.max_retries:
                    return "Unable to make progress after multiple attempts."
                
                reflection = self._generate_reflection()
                messages.append({
                    "role": "user",
                    "content": reflection
                })
                self._log(f"\n[Self-Correction] Retry {retries}")
            
            # Continue with normal ReAct loop
            response = self.llm(messages)
            parsed = self._parse_llm_response(response)
            
            # ... (rest of the logic same as parent)
            
            if parsed["final_answer"]:
                return parsed["final_answer"]
            
            if parsed["action"]:
                observation = self._execute_tool(parsed["action"], 
                                                parsed["action_input"] or "")
                
                step = AgentStep(
                    thought=parsed["thought"],
                    action=parsed["action"],
                    action_input=parsed["action_input"],
                    observation=observation
                )
                self.steps.append(step)
                
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user",
                    "content": f"Observation: {observation}"
                })
        
        return "Maximum steps reached."
```

### Example 3: ReAct with Structured Output

```python
"""
ReAct Agent with Structured Output
Produces JSON-formatted traces for easy parsing.
"""
import json
from datetime import datetime

class StructuredReActAgent(ReActAgent):
    """ReAct agent that produces structured JSON output."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run_id = datetime.now().isoformat()
    
    def run_structured(self, question: str) -> dict:
        """
        Run agent and return structured result.
        
        Returns:
            {
                "question": str,
                "answer": str,
                "trace": [...],
                "metadata": {...}
            }
        """
        start_time = datetime.now()
        self.steps = []
        
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Question: {question}"}
        ]
        
        answer = None
        error = None
        
        for step_num in range(1, self.max_steps + 1):
            try:
                response = self.llm(messages)
                parsed = self._parse_llm_response(response)
                
                step_record = {
                    "step": step_num,
                    "thought": parsed["thought"],
                    "action": parsed["action"],
                    "action_input": parsed["action_input"],
                    "observation": None,
                    "timestamp": datetime.now().isoformat()
                }
                
                if parsed["final_answer"]:
                    answer = parsed["final_answer"]
                    step_record["observation"] = "Final answer provided"
                    self.steps.append(step_record)
                    break
                
                if parsed["action"]:
                    observation = self._execute_tool(
                        parsed["action"],
                        parsed["action_input"] or ""
                    )
                    step_record["observation"] = observation
                    
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user",
                        "content": f"Observation: {observation}"
                    })
                
                self.steps.append(step_record)
                
            except Exception as e:
                error = str(e)
                break
        
        end_time = datetime.now()
        
        return {
            "run_id": self.run_id,
            "question": question,
            "answer": answer,
            "trace": self.steps,
            "metadata": {
                "total_steps": len(self.steps),
                "duration_seconds": (end_time - start_time).total_seconds(),
                "completed": answer is not None,
                "error": error,
                "tools_used": list(set(
                    s["action"] for s in self.steps if s.get("action")
                ))
            }
        }

# Usage
agent = StructuredReActAgent(
    llm_caller=mock_llm,
    tools={"search": search, "calculate": calculate}
)

result = agent.run_structured("What is Python?")
print(json.dumps(result, indent=2))
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Confusing Thought with Action
```python
# ❌ BAD: Skipping the thinking step
response = "Action: search\nAction Input: python"

# ✅ GOOD: Always think first
response = """Thought: I need to find information about Python. 
I'll search for it.
Action: search
Action Input: python"""
```

### Mistake 2: Not Parsing Observations
```python
# ❌ BAD: Ignoring tool results
def agent_step():
    response = llm.generate(prompt)
    action = parse_action(response)
    result = execute(action)
    # What happened? Agent doesn't know!

# ✅ GOOD: Feed observations back
def agent_step(messages):
    response = llm.generate(messages)
    action = parse_action(response)
    result = execute(action)
    messages.append({"role": "user", "content": f"Observation: {result}"})
```

### Mistake 3: No Max Steps Limit
```python
# ❌ BAD: Agent might loop forever
def run_agent(question):
    while True:  # No exit condition!
        step = think_and_act()
        if done:
            break

# ✅ GOOD: Always have limits
def run_agent(question, max_steps=10):
    for i in range(max_steps):
        step = think_and_act()
        if done:
            return answer
    return "Max steps reached"
```

### Mistake 4: Vague Tool Descriptions
```python
# ❌ BAD: Agent doesn't know when to use tools
tools = {
    "search": "Searches",
    "calc": "Calculates"
}

# ✅ GOOD: Clear, specific descriptions
tools = {
    "search": "Use this to find factual information from the web. "
              "Good for: current events, definitions, data.",
    "calculate": "Use this for mathematical computations. "
                 "Good for: arithmetic, statistics, conversions."
}
```

---

## ✅ Best Practices

1. **Always Think First**: Require a Thought before every Action
2. **Log Everything**: Keep complete traces for debugging
3. **Set Step Limits**: Prevent infinite loops
4. **Handle Errors Gracefully**: Feed errors back as observations
5. **Use Clear Tool Descriptions**: Help the LLM choose the right tool
6. **Validate Outputs**: Check LLM responses before executing
7. **Implement Self-Correction**: Detect and recover from loops
8. **Structure Your Output**: Make traces machine-readable

---

## 🏋️ Practice Exercises

### Exercise 1: Build a Research Agent
Create a ReAct agent that can:
- Search for information
- Read and summarize documents
- Synthesize findings into a report

### Exercise 2: Multi-Tool Problem Solving
Build an agent that solves math word problems by:
- Breaking down complex problems
- Using calculation tools
- Verifying answers

### Exercise 3: Code Debugging Agent
Create an agent that:
- Reads error messages
- Searches for solutions
- Suggests fixes

---

## 📝 Summary

| Concept | Description |
|---------|-------------|
| **ReAct** | Reasoning + Acting pattern |
| **Thought** | Agent's reasoning about what to do |
| **Action** | Tool invocation by the agent |
| **Observation** | Result returned from tool execution |
| **Trace** | Complete record of agent's steps |
| **Self-Correction** | Detecting and recovering from errors |

**Key Takeaways:**
1. ReAct combines thinking and doing in an interleaved loop
2. Each step includes Thought → Action → Observation
3. Observations feed back into the agent's reasoning
4. Traces make agent behavior transparent and debuggable
5. Always include safeguards like max steps and error handling

---

## 🔗 Next Lecture

In **Lecture 05: Planning & Reasoning**, we'll explore how agents can plan complex multi-step tasks before executing them.
