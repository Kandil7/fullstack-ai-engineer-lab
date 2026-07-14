"""
=============================================================
EXERCISE 02: Tool Calling / Function Calling
=============================================================
Topic: How agents use tools, schemas, and execution

Learning Objectives:
- Define tools with JSON schemas
- Build a tool registry pattern
- Parse and validate tool calls from LLMs
- Handle tool execution errors gracefully
- Implement parallel tool execution
- Chain tools for complex workflows

Prerequisites:
- Python 3.10+
- openai library (pip install openai)
=============================================================
"""

import json
import time
import uuid
import math
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional, Union
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


# ============================================================
# SECTION 1: Tool Schema Definition
# ============================================================

@dataclass
class ToolParameter:
    """Defines a single parameter for a tool."""
    name: str
    type: str          # "string", "number", "boolean", "array", "object"
    description: str
    required: bool = True
    enum: list = None
    default: Any = None

    def to_schema(self) -> dict:
        """Convert to JSON Schema format."""
        schema = {
            "type": self.type,
            "description": self.description,
        }
        if self.enum:
            schema["enum"] = self.enum
        if self.default is not None:
            schema["default"] = self.default
        return schema


@dataclass
class ToolDefinition:
    """
    Complete tool definition with schema and execution logic.
    This is the standard format for defining tools in an agent system.
    """
    name: str
    description: str
    parameters: list[ToolParameter]
    handler: Callable
    tags: list[str] = field(default_factory=list)
    timeout: float = 30.0

    def to_openai_schema(self) -> dict:
        """Convert to OpenAI function-calling format."""
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
                    "required": required,
                }
            }
        }

    def validate_args(self, args: dict) -> tuple[bool, str]:
        """Validate arguments against the parameter schema."""
        for param in self.parameters:
            if param.required and param.name not in args:
                return False, f"Missing required parameter: {param.name}"
            if param.name in args:
                value = args[param.name]
                if param.enum and value not in param.enum:
                    return False, f"Invalid value for {param.name}: {value}. Must be one of {param.enum}"
        return True, "Valid"

    def execute(self, **kwargs) -> dict:
        """Execute the tool with validation."""
        start_time = time.time()
        is_valid, message = self.validate_args(kwargs)
        if not is_valid:
            return {
                "success": False,
                "error": message,
                "tool": self.name,
                "execution_time_ms": 0,
            }

        try:
            result = self.handler(**kwargs)
            elapsed = (time.time() - start_time) * 1000
            return {
                "success": True,
                "result": result,
                "tool": self.name,
                "execution_time_ms": round(elapsed, 2),
            }
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return {
                "success": False,
                "error": str(e),
                "tool": self.name,
                "execution_time_ms": round(elapsed, 2),
            }


# ============================================================
# SECTION 2: Built-in Tools
# ============================================================

def calculator_handler(expression: str = "0") -> Any:
    """Evaluate a mathematical expression."""
    allowed = {
        "sqrt": math.sqrt, "abs": abs, "round": round,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "pi": math.pi, "e": math.e, "log": math.log,
    }
    return eval(expression, {"__builtins__": {}}, allowed)


def web_search_handler(query: str = "", max_results: int = 3) -> list[dict]:
    """Search the web (mock implementation)."""
    # Simulated search latency
    time.sleep(0.1)
    return [
        {"title": f"About {query}", "url": f"https://example.com/{query.replace(' ', '-')}",
         "snippet": f"Comprehensive information about {query}.", "relevance": 0.95 - i * 0.05}
        for i in range(min(max_results, 5))
    ]


def file_read_handler(path: str = "") -> str:
    """Read a file's contents (mock — returns simulated content)."""
    mock_files = {
        "config.json": '{"debug": true, "version": "1.0"}',
        "data.csv": "name,age\nAlice,30\nBob,25",
        "readme.md": "# Project\nThis is a sample project.",
    }
    return mock_files.get(path, f"[File not found: {path}]")


def text_transform_handler(text: str = "", operation: str = "uppercase") -> str:
    """Transform text with various operations."""
    operations = {
        "uppercase": text.upper(),
        "lowercase": text.lower(),
        "reverse": text[::-1],
        "word_count": str(len(text.split())),
        "char_count": str(len(text)),
        "title": text.title(),
        "strip": text.strip(),
        "slug": text.lower().replace(" ", "-"),
    }
    return operations.get(operation, f"Unknown operation: {operation}")


def hash_handler(text: str = "", algorithm: str = "sha256") -> str:
    """Generate a hash of the input text."""
    algos = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256}
    if algorithm not in algos:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    return algos[algorithm](text.encode()).hexdigest()


def timestamp_handler(format: str = "iso") -> str:
    """Get the current timestamp."""
    now = datetime.now()
    if format == "iso":
        return now.isoformat()
    elif format == "unix":
        return str(int(now.timestamp()))
    elif format == "readable":
        return now.strftime("%Y-%m-%d %H:%M:%S")
    return now.isoformat()


# Create tool definitions
CALCULATOR_TOOL = ToolDefinition(
    name="calculator",
    description="Evaluate mathematical expressions. Supports +, -, *, /, **, sqrt, sin, cos, tan, log.",
    parameters=[
        ToolParameter("expression", "string", "Mathematical expression to evaluate", required=True),
    ],
    handler=calculator_handler,
    tags=["math", "computation"],
)

WEB_SEARCH_TOOL = ToolDefinition(
    name="web_search",
    description="Search the web for information on any topic.",
    parameters=[
        ToolParameter("query", "string", "Search query", required=True),
        ToolParameter("max_results", "number", "Maximum results to return", required=False, default=3),
    ],
    handler=web_search_handler,
    tags=["search", "information"],
)

FILE_READ_TOOL = ToolDefinition(
    name="file_read",
    description="Read the contents of a file.",
    parameters=[
        ToolParameter("path", "string", "File path to read", required=True),
    ],
    handler=file_read_handler,
    tags=["filesystem", "io"],
)

TEXT_TRANSFORM_TOOL = ToolDefinition(
    name="text_transform",
    description="Transform text using various operations.",
    parameters=[
        ToolParameter("text", "string", "Text to transform", required=True),
        ToolParameter("operation", "string", "Operation to apply",
                       required=True, enum=["uppercase", "lowercase", "reverse",
                                            "word_count", "char_count", "title", "strip", "slug"]),
    ],
    handler=text_transform_handler,
    tags=["text", "transformation"],
)

HASH_TOOL = ToolDefinition(
    name="hash",
    description="Generate a cryptographic hash of text.",
    parameters=[
        ToolParameter("text", "string", "Text to hash", required=True),
        ToolParameter("algorithm", "string", "Hash algorithm",
                       required=False, default="sha256", enum=["md5", "sha1", "sha256"]),
    ],
    handler=hash_handler,
    tags=["crypto", "text"],
)

TIMESTAMP_TOOL = ToolDefinition(
    name="timestamp",
    description="Get the current timestamp in various formats.",
    parameters=[
        ToolParameter("format", "string", "Timestamp format",
                       required=False, default="iso", enum=["iso", "unix", "readable"]),
    ],
    handler=timestamp_handler,
    tags=["time", "utility"],
)


# ============================================================
# SECTION 3: Tool Registry
# ============================================================

class ToolRegistry:
    """
    Central registry for managing tools.
    Supports registration, lookup, validation, and execution.
    """

    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}
        self._execution_log: list[dict] = []
        self._lock = threading.Lock()

    def register(self, tool: ToolDefinition) -> None:
        """Register a tool in the registry."""
        with self._lock:
            if tool.name in self._tools:
                raise ValueError(f"Tool '{tool.name}' is already registered")
            self._tools[tool.name] = tool

    def unregister(self, name: str) -> bool:
        """Remove a tool from the registry."""
        with self._lock:
            if name in self._tools:
                del self._tools[name]
                return True
            return False

    def get(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self, tag: str = None) -> list[dict]:
        """List all registered tools, optionally filtered by tag."""
        tools = []
        for tool in self._tools.values():
            if tag and tag not in tool.tags:
                continue
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": len(tool.parameters),
                "tags": tool.tags,
            })
        return tools

    def get_schemas(self) -> list[dict]:
        """Get OpenAI-format schemas for all registered tools."""
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: dict) -> dict:
        """Execute a tool by name with arguments."""
        tool = self._tools.get(name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found. Available: {list(self._tools.keys())}",
                "tool": name,
                "execution_time_ms": 0,
            }

        result = tool.execute(**arguments)

        # Log execution
        with self._lock:
            self._execution_log.append({
                "tool": name,
                "arguments": arguments,
                "success": result.get("success", False),
                "execution_time_ms": result.get("execution_time_ms", 0),
                "timestamp": datetime.now().isoformat(),
            })

        return result

    def execute_parallel(self, calls: list[dict], max_workers: int = 4) -> list[dict]:
        """
        Execute multiple tool calls in parallel.
        Each call: {"tool": "name", "arguments": {...}}
        """
        results = []

        def _exec(call):
            return self.execute(call["tool"], call["arguments"])

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_exec, call): call for call in calls}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"success": False, "error": str(e)})

        return results

    def get_execution_stats(self) -> dict:
        """Get statistics about tool executions."""
        if not self._execution_log:
            return {"total": 0}

        total = len(self._execution_log)
        successful = sum(1 for log in self._execution_log if log["success"])
        avg_time = sum(log["execution_time_ms"] for log in self._execution_log) / total

        tool_counts = {}
        for log in self._execution_log:
            tool_counts[log["tool"]] = tool_counts.get(log["tool"], 0) + 1

        return {
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "avg_execution_time_ms": round(avg_time, 2),
            "tool_usage": tool_counts,
        }


# ============================================================
# SECTION 4: LLM Tool Call Parser
# ============================================================

@dataclass
class ToolCall:
    """Parsed tool call from LLM output."""
    id: str
    name: str
    arguments: dict
    raw_text: str = ""

    @classmethod
    def from_openai(cls, tool_call: dict) -> "ToolCall":
        """Parse an OpenAI-format tool call."""
        return cls(
            id=tool_call.get("id", str(uuid.uuid4())[:8]),
            name=tool_call.get("function", {}).get("name", ""),
            arguments=json.loads(tool_call.get("function", {}).get("arguments", "{}")),
            raw_text=json.dumps(tool_call),
        )

    @classmethod
    def from_text(cls, text: str) -> list["ToolCall"]:
        """
        Parse tool calls from natural language text.
        Looks for patterns like:
            tool_call: calculator(expression="2+2")
            tool: web_search(query="python tutorials")
        """
        import re
        calls = []
        pattern = r'(?:tool_call|tool)\s*:\s*(\w+)\(([^)]*)\)'
        matches = re.findall(pattern, text, re.IGNORECASE)

        for match_name, args_str in matches:
            args = {}
            # Parse key=value pairs
            arg_pattern = r'(\w+)\s*=\s*["\']?([^"\')]+)["\']?'
            for arg_match in re.finditer(arg_pattern, args_str):
                key, value = arg_match.groups()
                # Try to parse as number
                try:
                    value = float(value)
                    if value == int(value):
                        value = int(value)
                except ValueError:
                    pass
                args[key] = value

            calls.append(cls(
                id=str(uuid.uuid4())[:8],
                name=match_name,
                arguments=args,
                raw_text=f"tool_call: {match_name}({args_str})",
            ))

        return calls


# ============================================================
# SECTION 5: Tool Execution Pipeline
# ============================================================

class ToolPipeline:
    """
    Pipeline for executing tools with validation, error handling,
    and result aggregation.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.max_retries = 2
        self.results: list[dict] = []

    def validate_call(self, name: str, arguments: dict) -> tuple[bool, str]:
        """Pre-validate a tool call before execution."""
        tool = self.registry.get(name)
        if not tool:
            return False, f"Unknown tool: {name}"
        is_valid, msg = tool.validate_args(arguments)
        return is_valid, msg

    def execute_with_retry(self, name: str, arguments: dict) -> dict:
        """Execute a tool call with retry logic."""
        last_error = None
        for attempt in range(self.max_retries + 1):
            result = self.registry.execute(name, arguments)
            if result.get("success"):
                return result
            last_error = result.get("error", "Unknown error")
            if attempt < self.max_retries:
                time.sleep(0.1 * (attempt + 1))  # Exponential backoff

        return {
            "success": False,
            "error": f"Failed after {self.max_retries + 1} attempts: {last_error}",
            "tool": name,
            "retries": self.max_retries,
        }

    def execute_sequence(self, calls: list[ToolCall]) -> list[dict]:
        """
        Execute tool calls sequentially, passing results as context.
        Each call can reference previous results.
        """
        results = []
        context = {}

        for call in calls:
            # Substitute context variables in arguments
            resolved_args = {}
            for key, value in call.arguments.items():
                if isinstance(value, str) and value.startswith("$"):
                    ref = value[1:]
                    resolved_args[key] = context.get(ref, value)
                else:
                    resolved_args[key] = value

            result = self.execute_with_retry(call.name, resolved_args)
            results.append(result)

            # Store result in context for next calls
            context[f"result_{len(results)}"] = result.get("result")
            context["last_result"] = result.get("result")

        self.results = results
        return results

    def aggregate_results(self, results: list[dict]) -> dict:
        """Aggregate multiple tool results into a summary."""
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]

        return {
            "total_calls": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": [r.get("result") for r in successful],
            "errors": [r.get("error") for r in failed],
            "total_time_ms": sum(r.get("execution_time_ms", 0) for r in results),
        }


# ============================================================
# SECTION 6: Running the Exercises
# ============================================================

def exercise_1_tool_schemas():
    """Exercise 2.1: Define and inspect tool schemas."""
    print("\n" + "=" * 60)
    print("EXERCISE 2.1: Tool Schema Definition")
    print("=" * 60)

    tools = [CALCULATOR_TOOL, WEB_SEARCH_TOOL, TEXT_TRANSFORM_TOOL, HASH_TOOL, TIMESTAMP_TOOL]

    for tool in tools:
        print(f"\n  Tool: {tool.name}")
        print(f"  Description: {tool.description}")
        print(f"  Tags: {tool.tags}")
        print(f"  Parameters:")
        for param in tool.parameters:
            required = "required" if param.required else "optional"
            print(f"    - {param.name} ({param.type}, {required}): {param.description}")
        print(f"  OpenAI Schema: {json.dumps(tool.to_openai_schema(), indent=4)[:200]}...")


def exercise_2_registry():
    """Exercise 2.2: Tool registry operations."""
    print("\n" + "=" * 60)
    print("EXERCISE 2.2: Tool Registry")
    print("=" * 60)

    registry = ToolRegistry()

    # Register tools
    for tool in [CALCULATOR_TOOL, WEB_SEARCH_TOOL, TEXT_TRANSFORM_TOOL, HASH_TOOL, TIMESTAMP_TOOL]:
        registry.register(tool)
        print(f"  Registered: {tool.name}")

    # List all tools
    print(f"\n  All tools: {[t['name'] for t in registry.list_tools()]}")

    # Filter by tag
    print(f"  Math tools: {[t['name'] for t in registry.list_tools(tag='math')]}")
    print(f"  Text tools: {[t['name'] for t in registry.list_tools(tag='text')]}")
    print(f"  Search tools: {[t['name'] for t in registry.list_tools(tag='search')]}")

    # Get schemas
    schemas = registry.get_schemas()
    print(f"\n  Total schemas: {len(schemas)}")

    # Execute tools
    print("\n  Tool Execution:")
    result = registry.execute("calculator", {"expression": "2**10"})
    print(f"    calculator(2^10) = {result}")

    result = registry.execute("timestamp", {"format": "readable"})
    print(f"    timestamp() = {result}")

    result = registry.execute("hash", {"text": "hello world", "algorithm": "sha256"})
    print(f"    hash('hello world') = {result['result'][:20]}...")

    # Execution stats
    stats = registry.get_execution_stats()
    print(f"\n  Execution Stats: {json.dumps(stats, indent=4)}")


def exercise_3_tool_parsing():
    """Exercise 2.3: Parse tool calls from LLM output."""
    print("\n" + "=" * 60)
    print("EXERCISE 2.3: Tool Call Parsing")
    print("=" * 60)

    # Simulated LLM output with tool calls
    llm_output_1 = """
    I'll calculate that for you.
    tool_call: calculator(expression="15 * 23 + 7")
    The result should be correct.
    """

    llm_output_2 = """
    Let me search for that and transform the text.
    tool_call: web_search(query="Python best practices")
    tool_call: text_transform(text="hello world", operation="uppercase")
    """

    print("\n  Parsing LLM output 1:")
    calls_1 = ToolCall.from_text(llm_output_1)
    for call in calls_1:
        print(f"    Found: {call.name}({call.arguments})")

    print("\n  Parsing LLM output 2:")
    calls_2 = ToolCall.from_text(llm_output_2)
    for call in calls_2:
        print(f"    Found: {call.name}({call.arguments})")

    # Parse OpenAI format
    print("\n  Parsing OpenAI format:")
    openai_call = {
        "id": "call_abc123",
        "function": {
            "name": "calculator",
            "arguments": '{"expression": "sqrt(144)"}'
        }
    }
    parsed = ToolCall.from_openai(openai_call)
    print(f"    ID: {parsed.id}, Tool: {parsed.name}, Args: {parsed.arguments}")


def exercise_4_error_handling():
    """Exercise 2.4: Tool execution with error handling."""
    print("\n" + "=" * 60)
    print("EXERCISE 2.4: Error Handling")
    print("=" * 60)

    registry = ToolRegistry()
    for tool in [CALCULATOR_TOOL, WEB_SEARCH_TOOL, TEXT_TRANSFORM_TOOL]:
        registry.register(tool)

    # Test various error scenarios
    test_cases = [
        ("calculator", {"expression": "1/0"}, "Division by zero"),
        ("unknown_tool", {"query": "test"}, "Tool not found"),
        ("calculator", {}, "Missing required param"),
        ("text_transform", {"text": "hello", "operation": "invalid_op"}, "Invalid enum"),
        ("calculator", {"expression": "2 + 2"}, "Valid execution"),
    ]

    for name, args, description in test_cases:
        print(f"\n  Test: {description}")
        result = registry.execute(name, args)
        status = "SUCCESS" if result.get("success") else "FAILED"
        print(f"    Status: {status}")
        if result.get("success"):
            print(f"    Result: {result.get('result')}")
        else:
            print(f"    Error: {result.get('error')}")
        print(f"    Time: {result.get('execution_time_ms', 0):.2f}ms")


def exercise_5_parallel_execution():
    """Exercise 2.5: Parallel tool execution."""
    print("\n" + "=" * 60)
    print("EXERCISE 2.5: Parallel Tool Execution")
    print("=" * 60)

    registry = ToolRegistry()
    for tool in [CALCULATOR_TOOL, WEB_SEARCH_TOOL, TEXT_TRANSFORM_TOOL, HASH_TOOL, TIMESTAMP_TOOL]:
        registry.register(tool)

    # Define parallel calls
    calls = [
        {"tool": "calculator", "arguments": {"expression": "2**20"}},
        {"tool": "web_search", "arguments": {"query": "parallel computing", "max_results": 2}},
        {"tool": "text_transform", "arguments": {"text": "parallel execution is powerful", "operation": "reverse"}},
        {"tool": "hash", "arguments": {"text": "test data", "algorithm": "md5"}},
        {"tool": "timestamp", "arguments": {"format": "unix"}},
    ]

    print(f"\n  Executing {len(calls)} tools in parallel...")
    start = time.time()
    results = registry.execute_parallel(calls, max_workers=4)
    elapsed = time.time() - start

    print(f"  Completed in {elapsed*1000:.2f}ms")
    for i, result in enumerate(results):
        status = "OK" if result.get("success") else "FAIL"
        print(f"    [{i+1}] {status}: {result.get('tool', 'unknown')} = {str(result.get('result', result.get('error', '')))[:50]}")

    # Stats
    stats = registry.get_execution_stats()
    print(f"\n  Stats: {json.dumps(stats, indent=4)}")


def exercise_6_pipeline():
    """Exercise 2.6: Tool execution pipeline with chaining."""
    print("\n" + "=" * 60)
    print("EXERCISE 2.6: Tool Execution Pipeline")
    print("=" * 60)

    registry = ToolRegistry()
    for tool in [CALCULATOR_TOOL, TEXT_TRANSFORM_TOOL, HASH_TOOL, TIMESTAMP_TOOL]:
        registry.register(tool)

    pipeline = ToolPipeline(registry)

    # Sequential execution with context passing
    calls = [
        ToolCall(id="1", name="timestamp", arguments={"format": "readable"}),
        ToolCall(id="2", name="text_transform", arguments={"text": "hello world", "operation": "uppercase"}),
        ToolCall(id="3", name="hash", arguments={"text": "hello world", "algorithm": "sha256"}),
        ToolCall(id="4", name="calculator", arguments={"expression": "42 * 100"}),
    ]

    print("\n  Sequential execution:")
    results = pipeline.execute_sequence(calls)
    for i, result in enumerate(results):
        status = "OK" if result.get("success") else "FAIL"
        print(f"    Step {i+1} [{status}]: {result.get('result', result.get('error'))}")

    # Aggregate results
    summary = pipeline.aggregate_results(results)
    print(f"\n  Summary: {json.dumps(summary, indent=4)}")


def exercise_7_custom_tool():
    """Exercise 2.7: Create a custom tool."""
    print("\n" + "=" * 60)
    print("EXERCISE 2.7: Creating Custom Tools")
    print("=" * 60)

    # Define a custom tool: Unit Converter
    def convert_units(value: float = 0, from_unit: str = "", to_unit: str = "") -> dict:
        """Convert between common units."""
        conversions = {
            ("km", "miles"): lambda v: v * 0.621371,
            ("miles", "km"): lambda v: v * 1.60934,
            ("kg", "lbs"): lambda v: v * 2.20462,
            ("lbs", "kg"): lambda v: v * 0.453592,
            ("celsius", "fahrenheit"): lambda v: v * 9/5 + 32,
            ("fahrenheit", "celsius"): lambda v: (v - 32) * 5/9,
            ("meters", "feet"): lambda v: v * 3.28084,
            ("feet", "meters"): lambda v: v * 0.3048,
        }

        key = (from_unit.lower(), to_unit.lower())
        if key not in conversions:
            raise ValueError(f"Unknown conversion: {from_unit} -> {to_unit}")

        result = conversions[key](value)
        return {
            "input": f"{value} {from_unit}",
            "output": f"{round(result, 4)} {to_unit}",
            "factor": round(result / value if value != 0 else 0, 6),
        }

    unit_converter = ToolDefinition(
        name="convert_units",
        description="Convert between measurement units (km/miles, kg/lbs, celsius/fahrenheit, etc.)",
        parameters=[
            ToolParameter("value", "number", "Value to convert", required=True),
            ToolParameter("from_unit", "string", "Source unit", required=True),
            ToolParameter("to_unit", "string", "Target unit", required=True),
        ],
        handler=convert_units,
        tags=["conversion", "utility"],
    )

    # Register and use
    registry = ToolRegistry()
    registry.register(unit_converter)

    print("  Custom tool: convert_units")
    tests = [
        {"value": 100, "from_unit": "km", "to_unit": "miles"},
        {"value": 72, "from_unit": "fahrenheit", "to_unit": "celsius"},
        {"value": 1.8, "from_unit": "meters", "to_unit": "feet"},
    ]

    for args in tests:
        result = registry.execute("convert_units", args)
        print(f"    {args['value']} {args['from_unit']} = {result['result']['output']}")


# ============================================================
# Main: Run all exercises
# ============================================================

if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║  EXERCISE 02: Tool Calling / Function Calling            ║")
    print("║  Schemas, Registry, Execution, Error Handling             ║")
    print("╚" + "═" * 58 + "╝")

    exercises = [
        ("2.1", "Tool Schemas", exercise_1_tool_schemas),
        ("2.2", "Tool Registry", exercise_2_registry),
        ("2.3", "Tool Call Parsing", exercise_3_tool_parsing),
        ("2.4", "Error Handling", exercise_4_error_handling),
        ("2.5", "Parallel Execution", exercise_5_parallel_execution),
        ("2.6", "Tool Pipeline", exercise_6_pipeline),
        ("2.7", "Custom Tools", exercise_7_custom_tool),
    ]

    for num, name, func in exercises:
        try:
            func()
        except Exception as e:
            print(f"\n  [ERROR in {num}: {name}] {e}")

    print("\n" + "=" * 60)
    print("  All exercises completed!")
    print("=" * 60)

    print("""
KEY TAKEAWAYS:
1. Tools are defined with JSON schemas (name, description, parameters)
2. The tool registry provides centralized management and lookup
3. Always validate arguments before execution
4. Parallel execution significantly improves throughput
5. Error handling with retries makes agents more robust
6. Tool chaining enables complex multi-step workflows
7. Custom tools extend agent capabilities without changing core logic
""")
