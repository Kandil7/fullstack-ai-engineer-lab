# Lecture 02: Tool Calling

## 🎯 Topic Overview

**Tool calling** (also called function calling) is the mechanism that allows AI agents to interact with the external world. While LLMs excel at reasoning and language understanding, they cannot natively access databases, APIs, file systems, or perform calculations. Tool calling bridges this gap by letting agents invoke external functions with structured parameters.

This lecture covers:
- How tool calling works at the protocol level
- Designing effective tool interfaces
- Tool selection strategies
- Error handling and recovery
- Advanced patterns like tool chaining

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** how LLMs generate tool calls using structured output
2. **Design** clear, well-documented tool interfaces for agents
3. **Implement** tool registration and execution systems
4. **Handle** tool errors gracefully and feed them back to the agent
5. **Implement** tool selection when multiple tools are available
6. **Chain** multiple tools together for complex workflows
7. **Debug** tool calling issues using logs and traces
8. **Optimize** tool definitions for better agent performance

---

## 🧩 Key Concepts

### 1. How Tool Calling Works

```
┌──────────────────────────────────────────────────────────┐
│                    Tool Calling Flow                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. Define Tools     2. Send to LLM    3. LLM Decides    │
│  ┌─────────┐        ┌──────────┐      ┌──────────┐     │
│  │Tool     │───────►│ Prompt + │─────►│ Generate │     │
│  │Schemas  │        │ Tools    │      │ Call     │     │
│  └─────────┘        └──────────┘      └────┬─────┘     │
│                                            │             │
│  4. Parse Response  5. Execute    6. Return to LLM       │
│  ┌──────────┐      ┌──────────┐  ┌──────────┐          │
│  │ Extract  │─────►│ Run Tool │─►│ Feed     │          │
│  │ Call     │      │ Function │  │ Results  │          │
│  └──────────┘      └──────────┘  └──────────┘          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 2. Tool Schema Definition

Every tool needs a schema that tells the LLM:
- **Name**: How to reference the tool
- **Description**: What the tool does (critical for selection)
- **Parameters**: What inputs the tool accepts
- **Required/Optional**: Which parameters are mandatory

```python
# Tool schema for OpenAI-style function calling
weather_tool_schema = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a specified city. Returns temperature, conditions, humidity, and wind speed.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g., 'Paris', 'New York', 'Tokyo'"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature units (default: celsius)"
                }
            },
            "required": ["city"]
        }
    }
}
```

### 3. Tool Categories

```
┌─────────────────────────────────────────────────────────┐
│                    Tool Categories                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Informational          Action-Oriented                 │
│  ┌─────────────┐       ┌─────────────┐                │
│  │ • Search    │       │ • Send email│                │
│  │ • Read file │       │ • Write file│                │
│  │ • API query │       │ • Execute   │                │
│  │ • Database  │       │   code      │                │
│  │   lookup    │       │ • Call API  │                │
│  └─────────────┘       └─────────────┘                │
│                                                         │
│  Transformation         Communication                   │
│  ┌─────────────┐       ┌─────────────┐                │
│  │ • Calculate │       │ • Chat with │                │
│  │ • Convert   │       │   user      │                │
│  │ • Format    │       │ • Talk to   │                │
│  │ • Parse     │       │   other     │                │
│  │ • Validate  │       │   agents    │                │
│  └─────────────┘       └─────────────┘                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Code Examples

### Example 1: Complete Tool Calling System

```python
"""
Complete Tool Calling Implementation
Handles tool definition, registration, execution, and error handling.
"""
import json
import inspect
from typing import Any, Callable, Dict, List, Optional, get_type_hints
from dataclasses import dataclass
from enum import Enum

class ParameterType(Enum):
    """Supported parameter types."""
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


@dataclass
class ToolParameter:
    """Definition of a single tool parameter."""
    name: str
    type: ParameterType
    description: str
    required: bool = True
    default: Any = None
    enum_values: Optional[List[str]] = None
    
    def to_schema(self) -> dict:
        """Convert to JSON Schema format."""
        schema = {
            "type": self.type.value,
            "description": self.description
        }
        if self.enum_values:
            schema["enum"] = self.enum_values
        if self.default is not None:
            schema["default"] = self.default
        return schema


@dataclass
class ToolDefinition:
    """Complete tool definition including schema and implementation."""
    name: str
    description: str
    parameters: List[ToolParameter]
    function: Callable
    requires_confirmation: bool = False
    category: str = "general"
    
    def to_openai_schema(self) -> dict:
        """Convert to OpenAI function calling format."""
        properties = {}
        required = []
        
        for param in self.parameters:
            properties[param.name] = param.to_schema()
            if param.required:
                required.append(param.name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }


class ToolRegistry:
    """
    Registry for managing and executing tools.
    
    Handles:
    - Tool registration from functions or manual schemas
    - Schema generation for LLMs
    - Tool execution with validation
    - Error handling and logging
    """
    
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.execution_log: List[dict] = []
    
    def register_function(self, func: Callable, name: str = None, 
                          description: str = None,
                          requires_confirmation: bool = False):
        """
        Auto-register a Python function as a tool.
        
        Uses type hints and docstrings to generate schema.
        """
        tool_name = name or func.__name__
        tool_desc = description or func.__doc__ or f"Execute {tool_name}"
        
        # Extract parameters from type hints
        hints = get_type_hints(func)
        sig = inspect.signature(func)
        parameters = []
        
        for param_name, param in sig.parameters.items():
            # Skip 'self' parameter
            if param_name == 'self':
                continue
            
            # Determine type
            param_type = hints.get(param_name, str)
            type_mapping = {
                str: ParameterType.STRING,
                int: ParameterType.INTEGER,
                float: ParameterType.NUMBER,
                bool: ParameterType.BOOLEAN,
                list: ParameterType.ARRAY,
                dict: ParameterType.OBJECT
            }
            ptype = type_mapping.get(param_type, ParameterType.STRING)
            
            # Check if required
            required = param.default == inspect.Parameter.empty
            default = None if required else param.default
            
            parameters.append(ToolParameter(
                name=param_name,
                type=ptype,
                description=f"The {param_name} parameter",
                required=required,
                default=default
            ))
        
        tool = ToolDefinition(
            name=tool_name,
            description=tool_desc,
            parameters=parameters,
            function=func,
            requires_confirmation=requires_confirmation
        )
        
        self.tools[tool_name] = tool
        return tool
    
    def register_manual(self, name: str, description: str, 
                       parameters: List[ToolParameter],
                       function: Callable, **kwargs):
        """Register a tool with manual schema definition."""
        tool = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            function=function,
            **kwargs
        )
        self.tools[name] = tool
        return tool
    
    def get_schemas_for_llm(self, category: str = None) -> List[dict]:
        """Get all tool schemas in OpenAI format."""
        schemas = []
        for tool in self.tools.values():
            if category is None or tool.category == category:
                schemas.append(tool.to_openai_schema())
        return schemas
    
    def execute(self, tool_name: str, arguments: dict) -> str:
        """
        Execute a tool with validation and error handling.
        
        Returns:
            Tool result as string, or error message
        """
        # Check tool exists
        if tool_name not in self.tools:
            error = f"Unknown tool: {tool_name}"
            self._log_execution(tool_name, arguments, error, success=False)
            return error
        
        tool = self.tools[tool_name]
        
        # Validate required parameters
        for param in tool.parameters:
            if param.required and param.name not in arguments:
                if param.default is not None:
                    arguments[param.name] = param.default
                else:
                    error = f"Missing required parameter: {param.name}"
                    self._log_execution(tool_name, arguments, error, success=False)
                    return error
        
        # Execute with error handling
        try:
            result = tool.function(**arguments)
            result_str = str(result)
            self._log_execution(tool_name, arguments, result_str, success=True)
            return result_str
            
        except Exception as e:
            error = f"Tool execution failed: {type(e).__name__}: {str(e)}"
            self._log_execution(tool_name, arguments, error, success=False)
            return error
    
    def _log_execution(self, tool_name: str, arguments: dict, 
                      result: str, success: bool):
        """Log tool execution for debugging."""
        self.execution_log.append({
            "tool": tool_name,
            "arguments": arguments,
            "result": result[:500],  # Truncate long results
            "success": success,
            "timestamp": __import__('time').time()
        })
    
    def get_log(self) -> List[dict]:
        """Get execution history."""
        return self.execution_log.copy()


# === Usage Example ===

# Create registry
registry = ToolRegistry()

# Register tools using decorators
@registry.register_function
def search_web(query: str, num_results: int = 5) -> str:
    """Search the web and return results."""
    # Simulated search results
    return f"Found {num_results} results for: {query}"

@registry.register_function
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    # Basic safety check
    allowed = set("0123456789+-*/.() ")
    if all(c in allowed for c in expression):
        result = eval(expression)
        return f"Result: {expression} = {result}"
    return "Error: Invalid characters in expression"

@registry.register_function
def read_file(filepath: str) -> str:
    """Read contents of a file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return content[:1000]  # Truncate for safety
    except FileNotFoundError:
        return f"Error: File not found: {filepath}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Register with manual schema
registry.register_manual(
    name="send_notification",
    description="Send a notification to a user",
    parameters=[
        ToolParameter("user_id", ParameterType.STRING, "Target user ID"),
        ToolParameter("message", ParameterType.STRING, "Notification message"),
        ToolParameter("priority", ParameterType.STRING, "Priority level", 
                     required=False, default="normal",
                     enum_values=["low", "normal", "high", "urgent"])
    ],
    function=lambda user_id, message, priority="normal": 
        f"Notification sent to {user_id}: [{priority}] {message}"
)

# Get schemas for LLM
schemas = registry.get_schemas_for_llm()
print("Tool schemas for LLM:")
print(json.dumps(schemas, indent=2))

# Execute tools
result1 = registry.execute("search_web", {"query": "AI agents", "num_results": 3})
print(f"\nSearch result: {result1}")

result2 = registry.execute("calculate", {"expression": "2 + 2 * 3"})
print(f"Calculation: {result2}")

# View execution log
print("\nExecution log:")
for entry in registry.get_log():
    status = "✓" if entry["success"] else "✗"
    print(f"  [{status}] {entry['tool']}: {entry['result'][:50]}")
```

### Example 2: Tool Chaining

```python
"""
Tool Chaining: Using multiple tools in sequence.
Demonstrates how agents can compose tools for complex tasks.
"""
from typing import List, Callable
from dataclasses import dataclass

@dataclass
class ToolChainStep:
    """A single step in a tool chain."""
    tool_name: str
    input_mapping: dict  # Maps step outputs to tool inputs
    description: str

class ToolChain:
    """
    Executes a sequence of tools, passing outputs between steps.
    
    Useful for:
    - Multi-step workflows
    - Data pipelines
    - Complex task decomposition
    """
    
    def __init__(self, registry):
        self.registry = registry
        self.steps: List[ToolChainStep] = []
        self.results: dict = {}
    
    def add_step(self, tool_name: str, input_mapping: dict, description: str = ""):
        """Add a step to the chain."""
        self.steps.append(ToolChainStep(tool_name, input_mapping, description))
        return self  # Allow chaining
    
    def execute(self, initial_inputs: dict = None) -> dict:
        """
        Execute the entire chain.
        
        Args:
            initial_inputs: Starting values for the chain
            
        Returns:
            Dictionary of all step results
        """
        self.results = initial_inputs or {}
        
        for i, step in enumerate(self.steps):
            print(f"\n--- Step {i+1}: {step.description} ---")
            
            # Map inputs based on configuration
            step_inputs = {}
            for param_name, source in step.input_mapping.items():
                if source.startswith("$"):
                    # Reference to previous result
                    key = source[1:]
                    step_inputs[param_name] = self.results.get(key, "")
                else:
                    # Literal value
                    step_inputs[param_name] = source
            
            print(f"  Inputs: {step_inputs}")
            
            # Execute step
            result = self.registry.execute(step.tool_name, step_inputs)
            self.results[f"step_{i+1}"] = result
            
            print(f"  Result: {result[:100]}")
        
        return self.results
    
    def visualize(self) -> str:
        """Visualize the chain as ASCII art."""
        lines = ["Tool Chain:"]
        for i, step in enumerate(self.steps):
            lines.append(f"  {i+1}. {step.tool_name}")
            lines.append(f"     │ {step.description}")
            if i < len(self.steps) - 1:
                lines.append(f"     ▼")
        return "\n".join(lines)


# === Tool Chain Examples ===

# Example 1: Research and Report Chain
research_chain = ToolChain(registry)
research_chain.add_step(
    "search_web",
    {"query": "$topic", "num_results": "5"},
    description="Search for information"
)
research_chain.add_step(
    "calculate",
    {"expression": "'Result count: ' + $step_1.count('Result')"},
    description="Count results"
)
research_chain.add_step(
    "send_notification",
    {"user_id": "$user", "message": "$step_1"},
    description="Send report"
)

print(research_chain.visualize())
results = research_chain.execute({
    "topic": "AI agents",
    "user": "user123"
})

# Example 2: Data Processing Chain
data_chain = ToolChain(registry)
data_chain.add_step(
    "read_file",
    {"filepath": "$input_file"},
    description="Read input data"
)
data_chain.add_step(
    "calculate",
    {"expression": "'Length: ' + str(len($step_1))"},
    description="Calculate statistics"
)
data_chain.add_step(
    "send_notification",
    {"user_id": "$owner", "message": "$step_2"},
    description="Notify owner"
)

print("\n" + data_chain.visualize())
```

### Example 3: Error-Resilient Tool Calling

```python
"""
Error-Resilient Tool Calling
Handles failures, retries, and fallbacks gracefully.
"""
import time
from typing import Optional, Callable
from enum import Enum

class RetryStrategy(Enum):
    NONE = "none"
    IMMEDIATE = "immediate"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    ALTERNATIVE_TOOL = "alternative_tool"


class ResilientToolExecutor:
    """
    Executes tools with retry logic, fallbacks, and circuit breakers.
    
    Features:
    - Automatic retries with backoff
    - Fallback to alternative tools
    - Circuit breaker pattern
    - Detailed error logging
    """
    
    def __init__(self, registry, max_retries: int = 3):
        self.registry = registry
        self.max_retries = max_retries
        self.failure_counts: dict = {}
        self.circuit_breakers: dict = {}
        self.fallbacks: dict = {}
    
    def register_fallback(self, primary_tool: str, fallback_tool: str):
        """Register a fallback tool for when primary fails."""
        self.fallbacks[primary_tool] = fallback_tool
    
    def execute_with_retry(self, tool_name: str, arguments: dict,
                          strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF) -> str:
        """
        Execute a tool with retry logic.
        
        Args:
            tool_name: Tool to execute
            arguments: Tool arguments
            strategy: How to handle failures
            
        Returns:
            Tool result or error message
        """
        # Check circuit breaker
        if self._is_circuit_open(tool_name):
            return self._try_fallback(tool_name, arguments, "Circuit breaker open")
        
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                result = self.registry.execute(tool_name, arguments)
                
                # Check if result indicates failure
                if not result.startswith("Error"):
                    # Success - reset failure count
                    self.failure_counts[tool_name] = 0
                    return result
                
                last_error = result
                
            except Exception as e:
                last_error = f"{type(e).__name__}: {str(e)}"
            
            # Log attempt
            print(f"  Attempt {attempt + 1} failed: {last_error}")
            
            # Update failure count
            self.failure_counts[tool_name] = self.failure_counts.get(tool_name, 0) + 1
            
            # Check if we should continue retrying
            if attempt < self.max_retries:
                if strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
                    wait_time = 2 ** attempt
                    print(f"  Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                elif strategy == RetryStrategy.IMMEDIATE:
                    continue
                else:
                    break
        
        # All retries exhausted - try fallback
        return self._try_fallback(tool_name, arguments, last_error)
    
    def _try_fallback(self, tool_name: str, arguments: dict, 
                     original_error: str) -> str:
        """Attempt to use a fallback tool."""
        if tool_name in self.fallbacks:
            fallback = self.fallbacks[tool_name]
            print(f"  Trying fallback: {fallback}")
            return self.registry.execute(fallback, arguments)
        
        return f"Tool '{tool_name}' failed after retries: {original_error}"
    
    def _is_circuit_open(self, tool_name: str) -> bool:
        """Check if circuit breaker is tripped."""
        failure_count = self.failure_counts.get(tool_name, 0)
        if failure_count >= 5:  # Threshold
            print(f"  Circuit breaker open for {tool_name}")
            return True
        return False
    
    def get_health_report(self) -> dict:
        """Get health status of all tools."""
        return {
            "failure_counts": self.failure_counts.copy(),
            "circuit_breakers": {
                tool: self._is_circuit_open(tool)
                for tool in self.registry.tools
            }
        }


# === Usage ===

executor = ResilientToolExecutor(registry, max_retries=2)

# Register fallbacks
executor.register_fallback("search_web", "read_file")  # Fallback to local docs

# Execute with resilience
result = executor.execute_with_retry(
    "search_web",
    {"query": "nonexistent"},
    strategy=RetryStrategy.EXPONENTIAL_BACKOFF
)
print(f"Result: {result}")

# Health report
print("\nHealth Report:")
print(json.dumps(executor.get_health_report(), indent=2))
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Vague Tool Descriptions
```python
# ❌ BAD: Description doesn't explain when to use the tool
{
    "name": "search",
    "description": "Searches stuff"
}

# ✅ GOOD: Clear, specific description with use cases
{
    "name": "web_search",
    "description": "Search the web for current information. Use this when you need to find "
                   "recent news, factual information, or anything not in your training data. "
                   "Returns a list of relevant web pages with snippets."
}
```

### Mistake 2: No Input Validation
```python
# ❌ BAD: No validation, crashes on bad input
def calculate(expression):
    return eval(expression)  # Security risk!

# ✅ GOOD: Validate before execution
def calculate(expression: str) -> str:
    import re
    # Only allow safe characters
    if not re.match(r'^[\d\s\+\-\*\/\.\(\)]+$', expression):
        return "Error: Invalid characters in expression"
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Mistake 3: Not Handling Tool Failures
```python
# ❌ BAD: Agent crashes if tool fails
def agent_act(action):
    result = tools[action.name](action.input)
    return result  # What if this throws?

# ✅ GOOD: Graceful error handling
def agent_act(action):
    try:
        result = tools[action.name](action.input)
        return result
    except ToolNotFoundError as e:
        return f"I don't have access to tool '{action.name}'. Available tools: {list(tools.keys())}"
    except ToolExecutionError as e:
        return f"Tool failed: {str(e)}. I should try a different approach."
    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

### Mistake 4: Tool Descriptions That Don't Match Behavior
```python
# ❌ BAD: Description promises more than tool delivers
{
    "name": "search",
    "description": "Search the entire internet and return comprehensive results"
}
# But the tool only searches a small local database

# ✅ GOOD: Accurate description
{
    "name": "search_local_docs",
    "description": "Search the local documentation database. Contains official "
                   "project documentation up to v2.0. For internet searches, "
                   "use the 'web_search' tool instead."
}
```

---

## ✅ Best Practices

1. **Be Specific in Descriptions**: Tell the LLM exactly when to use each tool
2. **Include Examples**: Show example inputs in descriptions
3. **Validate Inputs**: Always check parameters before execution
4. **Return Helpful Errors**: Error messages should guide the agent toward alternatives
5. **Log Everything**: Keep execution logs for debugging
6. **Use Type Hints**: Help both humans and tools understand expected inputs
7. **Set Timeouts**: Prevent tools from hanging indefinitely
8. **Rate Limit**: Protect external APIs from being overwhelmed
9. **Provide Fallbacks**: Have backup tools for critical operations
10. **Test Tools Independently**: Verify each tool works before integrating

---

## 🏋️ Practice Exercises

### Exercise 1: Build a Tool Registry
Create a tool registry that:
- Auto-generates schemas from Python function signatures
- Supports parameter validation
- Logs all executions
- Handles tool conflicts (same name registration)

### Exercise 2: Implement Tool Chaining
Build a system that can:
- Chain tools together automatically
- Pass outputs between tools
- Handle chain failures gracefully
- Visualize the chain

### Exercise 3: Error Recovery System
Implement:
- Retry logic with exponential backoff
- Fallback tools
- Circuit breaker pattern
- Health monitoring

---

## 📝 Summary

| Concept | Description |
|---------|-------------|
| **Tool Calling** | LLM-generated structured function invocations |
| **Tool Schema** | JSON description of tool inputs/outputs |
| **Tool Registry** | Central management of available tools |
| **Tool Chaining** | Composing multiple tools in sequence |
| **Error Handling** | Graceful recovery from tool failures |
| **Circuit Breaker** | Pattern to stop calling failing tools |
| **Fallback** | Alternative tool when primary fails |

**Key Takeaways:**
1. Tool schemas must be clear and accurate for good agent performance
2. Always validate inputs and handle errors gracefully
3. Tool chaining enables complex multi-step workflows
4. Retry logic and fallbacks make agents more resilient
5. Logging tool executions is essential for debugging

---

## 🔗 Next Lecture

In **Lecture 03: Agent Memory**, we'll explore how agents remember past interactions and use that memory to improve future performance.
