# Lecture 05: Planning & Reasoning

## 🎯 Topic Overview

**Planning** is the ability of an agent to break down complex goals into manageable sub-tasks and determine the optimal sequence of actions to achieve them. While ReAct agents reason step-by-step during execution, planning agents think ahead before acting.

This lecture covers:
- Different planning strategies (task decomposition, goal trees, state-space search)
- How to implement planning in agents
- Combining planning with execution
- Handling plan failures and replanning
- Advanced reasoning techniques (Chain-of-Thought, Tree-of-Thought)

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** why planning is important for complex tasks
2. **Implement** task decomposition using LLMs
3. **Build** goal trees and dependency graphs
4. **Create** adaptive agents that can replan when plans fail
5. **Apply** advanced reasoning patterns (CoT, ToT)
6. **Handle** multi-step tasks with dependencies
7. **Evaluate** plan quality and efficiency
8. **Design** planning systems for real-world applications

---

## 🧩 Key Concepts

### 1. Planning vs. Reasoning

```
┌─────────────────────────────────────────────────────────────┐
│               Planning vs. Reasoning                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PLANNING (Before Acting)                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Goal: Build a website                                │   │
│  │                                                      │   │
│  │ Plan:                                                │   │
│  │ 1. Design layout (Task A)                           │   │
│  │ 2. Create HTML structure (Task B) [depends on A]    │   │
│  │ 3. Style with CSS (Task C) [depends on B]          │   │
│  │ 4. Add JavaScript (Task D) [depends on B]          │   │
│  │ 5. Test and deploy (Task E) [depends on C, D]      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  REASONING (During Acting)                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Current State: Task A complete                       │   │
│  │                                                      │   │
│  │ Thought: Now I need to create HTML.                  │   │
│  │          Should I use semantic HTML5 tags?            │   │
│  │          Yes, for better accessibility.               │   │
│  │ Action: Create index.html with semantic structure    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Planning Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Task Decomposition** | Break goal into sub-tasks | Complex multi-step tasks |
| **Goal Tree** | Hierarchical goal decomposition | Strategic planning |
| **State-Space Search** | Explore possible states | Puzzle-solving, optimization |
| **Reactive Planning** | Adapt plans as you go | Dynamic environments |
| **Hierarchical Task Network** | Task + constraints | Workflow automation |

### 3. Plan Representation

```python
@dataclass
class PlanStep:
    """A single step in a plan."""
    id: str
    description: str
    tool: Optional[str]
    dependencies: List[str]  # IDs of required prior steps
    status: PlanStatus = PlanStatus.PENDING
    
@dataclass
class Plan:
    """A complete plan with steps and dependencies."""
    goal: str
    steps: List[PlanStep]
    created_at: float
    metadata: dict = field(default_factory=dict)
```

---

## 💻 Code Examples

### Example 1: Task Decomposition Agent

```python
"""
Task Decomposition Agent
Breaks complex goals into manageable sub-tasks.
"""
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import time


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """A single task in the decomposition."""
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    result: Optional[str] = None
    subtasks: List["Task"] = field(default_factory=list)
    tool: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "result": self.result,
            "subtasks": [t.to_dict() for t in self.subtasks]
        }


class PlanningAgent:
    """
    Agent that decomposes goals into tasks and executes them.
    
    Features:
    - LLM-based task decomposition
    - Dependency tracking
    - Parallel task execution
    - Failure handling and replanning
    """
    
    def __init__(self, llm_caller, tools: Dict = None):
        self.llm = llm_caller
        self.tools = tools or {}
        self.execution_history: List[Dict] = []
    
    def decompose_goal(self, goal: str, max_depth: int = 2) -> List[Task]:
        """
        Break a goal into sub-tasks using LLM.
        
        Args:
            goal: The high-level goal to decompose
            max_depth: Maximum nesting depth for sub-tasks
            
        Returns:
            List of tasks with dependencies
        """
        prompt = f"""Break down the following goal into specific, actionable tasks.

Goal: {goal}

For each task, specify:
1. A clear description
2. Which tool to use (if any)
3. Dependencies (which tasks must complete first)

Return as JSON array:
[
  {{
    "description": "Task description",
    "tool": "tool_name or null",
    "dependencies": []
  }},
  ...
]

Make tasks specific and executable. Order them logically.
"""
        
        response = self.llm(prompt)
        
        try:
            tasks_data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback: create single task
            tasks_data = [{"description": goal, "tool": None, "dependencies": []}]
        
        # Create Task objects
        tasks = []
        for i, task_data in enumerate(tasks_data):
            task = Task(
                id=f"task_{i}",
                description=task_data["description"],
                tool=task_data.get("tool"),
                dependencies=task_data.get("dependencies", [])
            )
            tasks.append(task)
        
        return tasks
    
    def build_dependency_graph(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """Build adjacency list for dependency graph."""
        graph = {task.id: [] for task in tasks}
        
        for task in tasks:
            for dep in task.dependencies:
                if dep in graph:
                    graph[dep].append(task.id)
        
        return graph
    
    def get_ready_tasks(self, tasks: List[Task]) -> List[Task]:
        """Get tasks whose dependencies are all completed."""
        completed = {t.id for t in tasks if t.status == TaskStatus.COMPLETED}
        
        ready = []
        for task in tasks:
            if task.status != TaskStatus.PENDING:
                continue
            
            deps_met = all(dep in completed for dep in task.dependencies)
            if deps_met:
                ready.append(task)
        
        return ready
    
    def execute_task(self, task: Task) -> str:
        """Execute a single task."""
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            if task.tool and task.tool in self.tools:
                result = self.tools[task.tool](task.description)
            else:
                # Use LLM to complete the task
                result = self.llm(f"Complete this task: {task.description}")
            
            task.status = TaskStatus.COMPLETED
            task.result = result
            
            self.execution_history.append({
                "task_id": task.id,
                "description": task.description,
                "result": result[:200],
                "status": "completed"
            })
            
            return result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = str(e)
            
            self.execution_history.append({
                "task_id": task.id,
                "description": task.description,
                "error": str(e),
                "status": "failed"
            })
            
            return f"Error: {str(e)}"
    
    def execute_plan(self, tasks: List[Task], max_iterations: int = 20) -> Dict:
        """
        Execute all tasks in dependency order.
        
        Returns:
            Execution summary
        """
        results = {}
        
        for iteration in range(max_iterations):
            ready = self.get_ready_tasks(tasks)
            
            if not ready:
                # Check if all done
                pending = [t for t in tasks if t.status == TaskStatus.PENDING]
                if not pending:
                    break
                # Deadlock - tasks with unmet dependencies
                break
            
            # Execute ready tasks
            for task in ready:
                result = self.execute_task(task)
                results[task.id] = result
        
        return {
            "total_tasks": len(tasks),
            "completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in tasks if t.status == TaskStatus.FAILED),
            "results": results
        }
    
    def replan_after_failure(self, failed_task: Task, 
                            remaining_tasks: List[Task],
                            error: str) -> List[Task]:
        """
        Create a new plan after a task failure.
        
        Strategies:
        1. Skip the failed task
        2. Find alternative approach
        3. Break task into smaller pieces
        """
        prompt = f"""A task has failed. Help me replan.

Failed task: {failed_task.description}
Error: {error}

Remaining tasks:
{json.dumps([t.description for t in remaining_tasks], indent=2)}

Should we:
1. Skip this task and continue?
2. Try a different approach?
3. Break this task into smaller pieces?

Provide new tasks as JSON array, or empty array to skip:
"""
        
        response = self.llm(prompt)
        
        try:
            new_tasks_data = json.loads(response)
            new_tasks = []
            for i, task_data in enumerate(new_tasks_data):
                new_tasks.append(Task(
                    id=f"replan_{failed_task.id}_{i}",
                    description=task_data["description"],
                    tool=task_data.get("tool"),
                    dependencies=task_data.get("dependencies", [])
                ))
            return new_tasks
        except:
            return []


# === Usage Example ===

def search_tool(query: str) -> str:
    """Simulated search tool."""
    return f"Search results for: {query}"

def write_file(content: str) -> str:
    """Simulated file write."""
    return f"File written: {content[:50]}..."

# Mock LLM
def mock_llm(prompt: str) -> str:
    """Mock LLM for demonstration."""
    if "Break down" in prompt:
        return json.dumps([
            {"description": "Research topic", "tool": "search", "dependencies": []},
            {"description": "Create outline", "tool": None, "dependencies": ["task_0"]},
            {"description": "Write content", "tool": "write_file", "dependencies": ["task_1"]},
            {"description": "Review and edit", "tool": None, "dependencies": ["task_2"]}
        ])
    return "Task completed successfully."

# Create agent
agent = PlanningAgent(
    llm_caller=mock_llm,
    tools={"search": search_tool, "write_file": write_file}
)

# Decompose and execute
tasks = agent.decompose_goal("Write a technical blog post about AI agents")
print("Plan:")
for task in tasks:
    print(f"  - {task.id}: {task.description} (deps: {task.dependencies})")

results = agent.execute_plan(tasks)
print(f"\nResults: {results['completed']}/{results['total_tasks']} completed")
```

### Example 2: Tree-of-Thought Reasoning

```python
"""
Tree-of-Thought (ToT) Reasoning
Explores multiple reasoning paths and selects the best one.
"""
from typing import List, Tuple
from dataclasses import dataclass
import heapq


@dataclass
class ThoughtNode:
    """A node in the thought tree."""
    thought: str
    score: float
    depth: int
    parent: "ThoughtNode" = None
    children: List["ThoughtNode"] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    def __lt__(self, other):
        return self.score > other.score  # Higher score = better


class TreeOfThought:
    """
    Tree-of-Thought reasoning agent.
    
    Explores multiple reasoning branches and selects
    the most promising path.
    """
    
    def __init__(self, llm_caller, num_branches: int = 3,
                 max_depth: int = 5):
        self.llm = llm_caller
        self.num_branches = num_branches
        self.max_depth = max_depth
    
    def generate_thoughts(self, state: str, 
                         num_thoughts: int = 3) -> List[str]:
        """Generate multiple possible next thoughts."""
        prompt = f"""Given the current state:
{state}

Generate {num_thoughts} different possible next steps or thoughts.
Each should be a distinct approach.

Return as JSON array of strings:
["thought 1", "thought 2", "thought 3"]
"""
        response = self.llm(prompt)
        
        try:
            thoughts = json.loads(response)
            return thoughts[:num_thoughts]
        except:
            return [response]
    
    def evaluate_thought(self, thought: str, goal: str) -> float:
        """Score a thought's potential (0-1)."""
        prompt = f"""Evaluate how promising this thought is for achieving the goal.

Goal: {goal}
Thought: {thought}

Score from 0.0 to 1.0 (where 1.0 is most promising):
"""
        response = self.llm(prompt)
        
        try:
            score = float(response.strip())
            return max(0.0, min(1.0, score))
        except:
            return 0.5
    
    def search(self, initial_state: str, goal: str,
               beam_width: int = 2) -> ThoughtNode:
        """
        Search the thought tree for best reasoning path.
        
        Uses beam search to explore most promising branches.
        """
        # Initialize root
        root = ThoughtNode(
            thought=initial_state,
            score=1.0,
            depth=0
        )
        
        # Beam search
        current_beam = [root]
        
        for depth in range(self.max_depth):
            all_candidates = []
            
            for node in current_beam:
                # Generate thought branches
                thoughts = self.generate_thoughts(
                    node.thought, 
                    self.num_branches
                )
                
                for thought in thoughts:
                    score = self.evaluate_thought(thought, goal)
                    child = ThoughtNode(
                        thought=thought,
                        score=score * node.score,  # Cumulative score
                        depth=depth + 1,
                        parent=node
                    )
                    node.children.append(child)
                    all_candidates.append(child)
            
            if not all_candidates:
                break
            
            # Keep top beam_width candidates
            all_candidates.sort(reverse=True)
            current_beam = all_candidates[:beam_width]
            
            # Check if any thought reaches the goal
            for node in current_beam:
                if self._is_goal_reached(node.thought, goal):
                    return node
        
        # Return best leaf node
        best = max(
            [n for n in self._get_all_leaves(root)],
            key=lambda n: n.score,
            default=root
        )
        return best
    
    def _is_goal_reached(self, thought: str, goal: str) -> bool:
        """Check if the goal has been reached."""
        prompt = f"Has this thought reached the goal?\nThought: {thought}\nGoal: {goal}\nAnswer (yes/no):"
        response = self.llm(prompt).lower()
        return "yes" in response
    
    def _get_all_leaves(self, node: ThoughtNode) -> List[ThoughtNode]:
        """Get all leaf nodes from a tree."""
        if not node.children:
            return [node]
        leaves = []
        for child in node.children:
            leaves.extend(self._get_all_leaves(child))
        return leaves
    
    def get_reasoning_path(self, node: ThoughtNode) -> List[str]:
        """Extract the reasoning path from root to node."""
        path = []
        current = node
        while current:
            path.insert(0, current.thought)
            current = current.parent
        return path
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Planning Too Far Ahead
```python
# ❌ BAD: Creating 100-step plans that are impossible to follow
plan = create_detailed_plan(goal, steps=100)

# ✅ GOOD: Plan a few steps ahead, then replan
plan = create_detailed_plan(goal, steps=5)
while not complete:
    execute_current_steps(plan)
    replan(plan)
```

### Mistake 2: Not Handling Failures
```python
# ❌ BAD: Assuming plan will succeed
for step in plan:
    execute(step)  # What if this fails?

# ✅ GOOD: Handle failures gracefully
for step in plan:
    try:
        execute(step)
    except Exception as e:
        replan_after_failure(step, e)
```

### Mistake 3: Over-Planning Simple Tasks
```python
# ❌ BAD: Planning for simple questions
plan = create_plan("What is 2 + 2?")  # Just answer it!

# ✅ GOOD: Use planning only when needed
if is_complex_task(goal):
    plan = create_plan(goal)
else:
    answer = llm(goal)
```

---

## ✅ Best Practices

1. **Plan Just-in-Time**: Don't plan too far ahead; replan as you go
2. **Handle Failures**: Always have fallback strategies
3. **Validate Plans**: Check that dependencies are satisfiable
4. **Track Progress**: Monitor plan execution and adjust
5. **Use Heuristics**: Score and prioritize tasks
6. **Consider Resources**: Account for tool limitations and costs
7. **Be Adaptive**: Change plans when new information emerges
8. **Document Decisions**: Keep a record of why choices were made

---

## 🏋️ Practice Exercises

### Exercise 1: Task Decomposition
Build an agent that decomposes "Plan a vacation to Japan" into detailed sub-tasks.

### Exercise 2: Dependency Resolution
Implement a system that correctly executes tasks with complex dependencies.

### Exercise 3: Tree-of-Thought
Create a ToT agent that solves word puzzles by exploring multiple solution paths.

---

## 📝 Summary

| Concept | Description |
|---------|-------------|
| **Planning** | Breaking goals into actionable steps |
| **Task Decomposition** | Dividing complex tasks into simpler ones |
| **Dependency Graph** | Relationships between tasks |
| **Replanning** | Adapting plans when things go wrong |
| **Tree-of-Thought** | Exploring multiple reasoning paths |
| **Beam Search** | Keeping top-k promising paths |

---

## 🔗 Next Lecture

In **Lecture 06: Multi-Agent Orchestration**, we'll explore how to coordinate multiple agents working together.
