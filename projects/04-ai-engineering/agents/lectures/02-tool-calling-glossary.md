# Glossary: Tool Calling

> Terms defined in alphabetical order. Each entry includes: definition, example usage, code snippet, and related terms.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Action Space | Set of all possible actions an agent can take | Tool, Capability |
| API Gateway | Entry point for managing API access | Tool, Authentication |
| Circuit Breaker | Pattern to stop calling failing tools | Retry, Fallback |
| Error Handling | Graceful recovery from tool failures | Retry, Fallback |
| Fallback | Alternative tool when primary fails | Retry, Resilience |
| Function Calling | LLM mechanism for structured tool invocation | Tool, Schema |
| Input Validation | Checking tool parameters before execution | Schema, Safety |
| Middleware | Code that runs before/after tool execution | Hook, Interceptor |
| Parameter Schema | JSON definition of tool inputs | Tool, Schema |
| Rate Limiting | Controlling tool execution frequency | Throttling, Quota |
| Retry | Attempting tool execution again after failure | Backoff, Circuit Breaker |
| Schema | Structured definition of tool interface | JSON Schema, API |
| Tool | External function an agent can invoke | Action, Function |
| Tool Chain | Sequential execution of multiple tools | Pipeline, Workflow |
| Tool Registry | Central management of available tools | Tool, Registry |
| Tool Use | Pattern of agents calling external tools | Function Calling |

---

## A

### Action Space

**Definition:** The complete set of actions available to an agent at any given time. The action space can be dynamic — changing based on context, permissions, or environment state.

**Example:**
```python
class ActionSpace:
    def __init__(self):
        self.available_tools = {}
        self.restricted_tools = {}
        self.context_restrictions = []
    
    def add_tool(self, tool, restrictions=None):
        """Add a tool to the action space."""
        if restrictions:
            self.restricted_tools[tool.name] = {
                "tool": tool,
                "restrictions": restrictions
            }
        else:
            self.available_tools[tool.name] = tool
    
    def get_available(self, context=None) -> list:
        """Get tools available in current context."""
        available = list(self.available_tools.values())
        
        # Add restricted tools that match context
        for name, info in self.restricted_tools.items():
            if self._check_restrictions(info["restrictions"], context):
                available.append(info["tool"])
        
        return available
    
    def _check_restrictions(self, restrictions, context):
        """Check if tool is allowed in current context."""
        if context is None:
            return False
        return all(r(context) for r in restrictions)

# Usage
space = ActionSpace()
space.add_tool(search_tool)
space.add_tool(delete_tool, restrictions=[
    lambda ctx: ctx.get("user_role") == "admin"
])
```

**Related terms:** Tool, Capability, Permission

---

## C

### Circuit Breaker

**Definition:** A resilience pattern that stops attempting to call a tool after it fails a certain number of times. This prevents cascading failures and gives failing services time to recover.

**Example:**
```python
from enum import Enum
from time import time

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject calls
    HALF_OPEN = "half_open" # Testing if recovered

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def record_success(self):
        """Record a successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def record_failure(self):
        """Record a failed call."""
        self.failure_count += 1
        self.last_failure_time = time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def allow_request(self) -> bool:
        """Check if a request should be allowed."""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        
        # HALF_OPEN: allow one test request
        return True

# Usage
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

def call_tool_with_breaker(tool, args):
    if not breaker.allow_request():
        return "Circuit breaker open - tool temporarily unavailable"
    
    try:
        result = tool(**args)
        breaker.record_success()
        return result
    except Exception as e:
        breaker.record_failure()
        raise
```

**Related terms:** Retry, Fallback, Resilience

---

## F

### Fallback

**Definition:** An alternative tool or strategy used when the primary tool fails. Fallbacks ensure the agent can still make progress even when preferred tools are unavailable.

**Example:**
```python
class FallbackChain:
    """Chain of tools to try in order."""
    
    def __init__(self):
        self.fallbacks = {}
    
    def register(self, primary: str, *alternatives: str):
        """Register fallback chain for a tool."""
        self.fallbacks[primary] = list(alternatives)
    
    def execute(self, tool_name: str, args: dict, registry) -> str:
        """Try primary tool, then fallbacks."""
        tools_to_try = [tool_name] + self.fallbacks.get(tool_name, [])
        
        errors = []
        for tool in tools_to_try:
            try:
                result = registry.execute(tool, args)
                if not result.startswith("Error"):
                    return result
                errors.append(f"{tool}: {result}")
            except Exception as e:
                errors.append(f"{tool}: {str(e)}")
        
        return f"All tools failed: {'; '.join(errors)}"

# Usage
fallbacks = FallbackChain()
fallbacks.register("web_search", "local_search", "knowledge_base")
fallbacks.register("openai_api", "local_model", "template_response")

result = fallbacks.execute("web_search", {"query": "AI agents"}, registry)
```

**Related terms:** Retry, Circuit Breaker, Resilience

---

## I

### Input Validation

**Definition:** The process of checking that tool parameters meet expected types, ranges, and formats before execution. Validation prevents errors and security vulnerabilities.

**Example:**
```python
from typing import Any, Dict
import re

class InputValidator:
    def __init__(self, schema: dict):
        self.schema = schema
    
    def validate(self, inputs: dict) -> tuple[bool, list]:
        """
        Validate inputs against schema.
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        for param in self.schema.get("required", []):
            if param not in inputs:
                errors.append(f"Missing required parameter: {param}")
        
        # Validate each parameter
        for param_name, param_schema in self.schema.get("properties", {}).items():
            if param_name in inputs:
                value = inputs[param_name]
                param_errors = self._validate_param(param_name, value, param_schema)
                errors.extend(param_errors)
        
        return len(errors) == 0, errors
    
    def _validate_param(self, name: str, value: Any, schema: dict) -> list:
        """Validate a single parameter."""
        errors = []
        
        # Type check
        expected_type = schema.get("type")
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        if expected_type in type_map:
            if not isinstance(value, type_map[expected_type]):
                errors.append(f"{name}: Expected {expected_type}, got {type(value).__name__}")
        
        # Enum check
        if "enum" in schema and value not in schema["enum"]:
            errors.append(f"{name}: Must be one of {schema['enum']}")
        
        # String pattern
        if "pattern" in schema and isinstance(value, str):
            if not re.match(schema["pattern"], value):
                errors.append(f"{name}: Must match pattern {schema['pattern']}")
        
        return errors

# Usage
schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"},
        "age": {"type": "integer"},
        "role": {"type": "string", "enum": ["admin", "user", "guest"]}
    },
    "required": ["email", "age"]
}

validator = InputValidator(schema)
is_valid, errors = validator.validate({
    "email": "user@example.com",
    "age": 25,
    "role": "admin"
})
```

**Related terms:** Schema, Safety, Tool

---

## M

### Middleware

**Definition:** Code that runs before and/or after tool execution, used for logging, validation, authentication, rate limiting, or transformation. Middleware wraps tool calls without modifying the tool itself.

**Example:**
```python
from typing import Callable, Any
import time
from functools import wraps

class ToolMiddleware:
    """Base class for tool middleware."""
    
    def before(self, tool_name: str, args: dict) -> dict:
        """Runs before tool execution. Can modify args."""
        return args
    
    def after(self, tool_name: str, args: dict, result: Any) -> Any:
        """Runs after tool execution. Can modify result."""
        return result
    
    def on_error(self, tool_name: str, args: dict, error: Exception) -> str:
        """Runs when tool execution fails."""
        return f"Error: {str(error)}"

class LoggingMiddleware(ToolMiddleware):
    """Logs all tool executions."""
    
    def __init__(self):
        self.logs = []
    
    def before(self, tool_name, args):
        self.logs.append({
            "tool": tool_name,
            "args": args,
            "timestamp": time.time()
        })
        return args
    
    def after(self, tool_name, args, result):
        if self.logs:
            self.logs[-1]["result"] = str(result)[:200]
            self.logs[-1]["success"] = True
        return result

class RateLimitMiddleware(ToolMiddleware):
    """Limits tool execution frequency."""
    
    def __init__(self, max_calls_per_minute: int = 60):
        self.max_calls = max_calls_per_minute
        self.calls = []
    
    def before(self, tool_name, args):
        now = time.time()
        # Remove calls older than 1 minute
        self.calls = [t for t in self.calls if now - t < 60]
        
        if len(self.calls) >= self.max_calls:
            raise Exception("Rate limit exceeded")
        
        self.calls.append(now)
        return args

class ToolWithMiddleware:
    """Execute tools with middleware pipeline."""
    
    def __init__(self):
        self.middleware = []
    
    def add_middleware(self, mw: ToolMiddleware):
        self.middleware.append(mw)
    
    def execute(self, tool_name: str, tool_func: Callable, args: dict) -> Any:
        """Execute tool through middleware pipeline."""
        # Before hooks
        for mw in self.middleware:
            args = mw.before(tool_name, args)
        
        # Execute tool
        try:
            result = tool_func(**args)
        except Exception as e:
            # Error hooks
            for mw in self.middleware:
                result = mw.on_error(tool_name, args, e)
            return result
        
        # After hooks
        for mw in self.middleware:
            result = mw.after(tool_name, args, result)
        
        return result
```

**Related terms:** Hook, Interceptor, Pipeline

---

## P

### Parameter Schema

**Definition:** A structured definition describing the inputs a tool accepts. Schemas specify parameter names, types, descriptions, defaults, and constraints. They enable LLMs to generate correct tool calls.

**Example:**
```python
# JSON Schema format for tool parameters
search_schema = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "The search query"
        },
        "max_results": {
            "type": "integer",
            "description": "Maximum number of results to return",
            "default": 10,
            "minimum": 1,
            "maximum": 100
        },
        "filters": {
            "type": "object",
            "description": "Optional search filters",
            "properties": {
                "date_range": {
                    "type": "string",
                    "enum": ["day", "week", "month", "year"]
                },
                "language": {
                    "type": "string",
                    "description": "ISO language code"
                }
            }
        }
    },
    "required": ["query"]
}

# Generate schema from function signature
from typing import get_type_hints
import inspect

def generate_schema(func) -> dict:
    """Auto-generate parameter schema from function."""
    hints = get_type_hints(func)
    sig = inspect.signature(func)
    
    properties = {}
    required = []
    
    for name, param in sig.parameters.items():
        prop = {
            "type": _python_type_to_json(hints.get(name, str)),
            "description": f"Parameter: {name}"
        }
        
        if param.default is inspect.Parameter.empty:
            required.append(name)
        else:
            prop["default"] = param.default
        
        properties[name] = prop
    
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }

def _python_type_to_json(python_type) -> str:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object"
    }
    return type_map.get(python_type, "string")
```

**Related terms:** Tool, Schema, Validation

---

## R

### Rate Limiting

**Definition:** Controlling how frequently a tool can be called, typically to protect external APIs from being overwhelmed or to manage costs.

**Example:**
```python
import time
from collections import defaultdict
from threading import Lock

class RateLimiter:
    def __init__(self, limits: dict):
        """
        Args:
            limits: {tool_name: max_calls_per_window}
        """
        self.limits = limits
        self.calls = defaultdict(list)
        self.lock = Lock()
    
    def can_execute(self, tool_name: str) -> bool:
        """Check if tool can be called now."""
        if tool_name not in self.limits:
            return True  # No limit
        
        with self.lock:
            now = time.time()
            window = 60  # 1 minute window
            
            # Remove old calls
            self.calls[tool_name] = [
                t for t in self.calls[tool_name] 
                if now - t < window
            ]
            
            # Check limit
            return len(self.calls[tool_name]) < self.limits[tool_name]
    
    def record_call(self, tool_name: str):
        """Record a tool execution."""
        with self.lock:
            self.calls[tool_name].append(time.time())
    
    def wait_time(self, tool_name: str) -> float:
        """Seconds until tool can be called again."""
        if tool_name not in self.limits:
            return 0
        
        with self.lock:
            if not self.calls[tool_name]:
                return 0
            
            oldest = self.calls[tool_name][0]
            return max(0, 60 - (time.time() - oldest))

# Usage
limiter = RateLimiter({
    "openai_api": 60,      # 60 calls per minute
    "web_search": 30,      # 30 searches per minute
    "send_email": 10       # 10 emails per minute
})

def execute_with_rate_limit(tool_name, func, args):
    if not limiter.can_execute(tool_name):
        wait = limiter.wait_time(tool_name)
        return f"Rate limited. Try again in {wait:.1f} seconds"
    
    limiter.record_call(tool_name)
    return func(**args)
```

**Related terms:** Quota, Throttling, Cost

---

### Retry

**Definition:** The pattern of attempting tool execution again after a failure. Retries can be immediate, delayed, or use exponential backoff to avoid overwhelming a struggling service.

**Example:**
```python
import time
import random
from typing import Callable, Any

class RetryHandler:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with retry logic.
        
        Uses exponential backoff with jitter.
        """
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                if attempt < self.max_retries:
                    # Exponential backoff with jitter
                    base_delay = self.backoff_factor ** attempt
                    jitter = random.uniform(0, base_delay * 0.5)
                    delay = base_delay + jitter
                    
                    print(f"Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {delay:.2f}s...")
                    time.sleep(delay)
        
        raise last_error

# Decorator version
def retry(max_retries=3, backoff_factor=2.0, 
          exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = RetryHandler(max_retries, backoff_factor)
            return handler.execute_with_retry(
                lambda: func(*args, **kwargs)
            )
        return wrapper
    return decorator

# Usage
@retry(max_retries=3, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url):
    import requests
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

**Related terms:** Backoff, Circuit Breaker, Fallback

---

## S

### Schema

**Definition:** A structured definition that describes the interface of a tool, including its name, description, parameters, and return type. Schemas enable LLMs to understand and correctly invoke tools.

**Example:**
```python
# Complete tool schema example
tool_schema = {
    "type": "function",
    "function": {
        "name": "create_user",
        "description": "Create a new user account in the system. "
                      "Requires admin privileges. Returns the created user ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "User's email address",
                    "format": "email"
                },
                "name": {
                    "type": "string",
                    "description": "User's full name"
                },
                "role": {
                    "type": "string",
                    "description": "User role",
                    "enum": ["admin", "editor", "viewer"],
                    "default": "viewer"
                }
            },
            "required": ["email", "name"]
        }
    }
}

# Schema validation
from jsonschema import validate, ValidationError

def validate_tool_input(schema: dict, inputs: dict) -> bool:
    """Validate tool inputs against schema."""
    try:
        validate(instance=inputs, schema=schema["function"]["parameters"])
        return True
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        return False
```

**Related terms:** Parameter Schema, Tool, JSON Schema

---

## T

### Tool

**Definition:** An external function or service that an agent can invoke to perform actions beyond the LLM's native capabilities. Tools extend agents with abilities like web search, database access, file operations, and API calls.

**Example:**
```python
from typing import Callable
from dataclasses import dataclass

@dataclass
class Tool:
    """Represents a tool available to an agent."""
    name: str
    description: str
    function: Callable
    schema: dict
    requires_auth: bool = False
    cost_per_call: float = 0.0
    
    def execute(self, **kwargs) -> str:
        """Execute the tool with given arguments."""
        try:
            result = self.function(**kwargs)
            return str(result)
        except Exception as e:
            return f"Error executing {self.name}: {str(e)}"

# Tool definitions
tools = [
    Tool(
        name="calculator",
        description="Evaluate mathematical expressions",
        function=eval,
        schema={
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    ),
    Tool(
        name="web_search",
        description="Search the web for information",
        function=search_web,
        schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "num_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        },
        requires_auth=True,
        cost_per_call=0.001
    )
]
```

**Related terms:** Function Calling, Action, Tool Use

---

### Tool Chain

**Definition:** A sequence of tools executed in order, where the output of one tool becomes the input to the next. Tool chains enable complex multi-step workflows.

**Example:**
```python
from typing import List, Dict

class ToolChain:
    def __init__(self, name: str, steps: List[Dict]):
        """
        Args:
            name: Chain identifier
            steps: List of {tool, input_mapping} dicts
        """
        self.name = name
        self.steps = steps
    
    def execute(self, registry, initial_input: dict) -> dict:
        """Execute the chain, passing data between steps."""
        context = initial_input.copy()
        results = {}
        
        for i, step in enumerate(self.steps):
            tool_name = step["tool"]
            input_map = step.get("input_mapping", {})
            
            # Map inputs from context
            tool_inputs = {}
            for param, source in input_map.items():
                if source.startswith("$"):
                    tool_inputs[param] = context[source[1:]]
                else:
                    tool_inputs[param] = source
            
            # Execute
            result = registry.execute(tool_name, tool_inputs)
            results[f"step_{i+1}"] = result
            context[f"step_{i+1}"] = result
        
        return results

# Define a chain
research_chain = ToolChain("research_report", [
    {
        "tool": "web_search",
        "input_mapping": {"query": "$topic", "num_results": "5"}
    },
    {
        "tool": "summarize",
        "input_mapping": {"text": "$step_1"}
    },
    {
        "tool": "send_email",
        "input_mapping": {"to": "$recipient", "body": "$step_2"}
    }
])

# Execute
results = research_chain.execute(registry, {
    "topic": "AI agents",
    "recipient": "team@company.com"
})
```

**Related terms:** Pipeline, Workflow, Composition

---

### Tool Registry

**Definition:** A central repository that manages all tools available to an agent. The registry handles tool registration, schema generation, execution, and lifecycle management.

**Example:**
```python
class ToolRegistry:
    """Central registry for all agent tools."""
    
    def __init__(self):
        self.tools = {}
        self.categories = {}
    
    def register(self, tool: Tool, category: str = "general"):
        """Register a tool."""
        self.tools[tool.name] = tool
        
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(tool.name)
    
    def unregister(self, name: str):
        """Remove a tool."""
        if name in self.tools:
            del self.tools[name]
            for cat_tools in self.categories.values():
                if name in cat_tools:
                    cat_tools.remove(name)
    
    def get_schemas(self, category: str = None) -> list:
        """Get schemas for LLM function calling."""
        schemas = []
        for name, tool in self.tools.items():
            if category is None or name in self.categories.get(category, []):
                schemas.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.schema
                    }
                })
        return schemas
    
    def execute(self, name: str, args: dict) -> str:
        """Execute a tool by name."""
        if name not in self.tools:
            return f"Unknown tool: {name}"
        return self.tools[name].execute(**args)
    
    def list_tools(self) -> list:
        """List all registered tools."""
        return [
            {"name": t.name, "description": t.description}
            for t in self.tools.values()
        ]

# Usage
registry = ToolRegistry()
registry.register(search_tool, category="information")
registry.register(calculator_tool, category="utility")

schemas = registry.get_schemas()
result = registry.execute("calculator", {"expression": "2+2"})
```

**Related terms:** Tool, Registry, Management

---

### Tool Use

**Definition:** The pattern where an LLM generates structured output to invoke external tools. Tool use enables agents to interact with the world beyond generating text.

**Example:**
```python
# Tool use in OpenAI API
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]

# LLM generates tool call
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

# Response contains tool call
tool_call = response.choices[0].message.tool_calls[0]
# {
#   "id": "call_abc123",
#   "function": {
#     "name": "get_weather",
#     "arguments": '{"city": "Paris"}'
#   }
# }

# Execute and return result
weather_data = get_weather(city="Paris")
# {
#   "tool_call_id": "call_abc123",
#   "role": "tool",
#   "content": '{"temp": 22, "condition": "sunny"}'
# }
```

**Related terms:** Function Calling, Tool, LLM

---

## Quick Reference: Tool Calling Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Tool Calling System                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐                                        │
│  │  LLM        │ Generates structured tool calls        │
│  └──────┬──────┘                                        │
│         │                                               │
│         ▼                                               │
│  ┌─────────────┐                                        │
│  │  Parser     │ Extracts tool name + arguments         │
│  └──────┬──────┘                                        │
│         │                                               │
│         ▼                                               │
│  ┌─────────────┐     ┌──────────────┐                  │
│  │  Validator  │────►│  Middleware   │                  │
│  └──────┬──────┘     │  (logging,   │                  │
│         │            │   rate limit) │                  │
│         ▼            └──────┬───────┘                  │
│  ┌─────────────┐            │                           │
│  │  Executor   │◄───────────┘                           │
│  └──────┬──────┘                                        │
│         │                                               │
│         ├── Success ──► Return result to LLM            │
│         │                                               │
│         └── Failure ──► Retry/Fallback/Error to LLM     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 02](./02-tool-calling-lecture.md)** | **[Next: Lecture 03 →](./03-agent-memory-glossary.md)**
