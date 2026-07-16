# Glossary: Planning & Reasoning

> Terms defined in alphabetical order. Each entry includes: definition, example usage, code snippet, and related terms.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Beam Search | Keeping top-k most promising paths | Tree-of-Thought, Search |
| Brainstorming | Generating multiple possible approaches | Divergent Thinking |
| Chain-of-Thought | Step-by-step reasoning | Reasoning, CoT |
| DAG | Directed Acyclic Graph for dependencies | Dependency Graph |
| Decomposition | Breaking complex tasks into simpler ones | Task Decomposition |
| Goal Tree | Hierarchical goal decomposition | Planning, Hierarchy |
| Heuristic | Rule-of-thumb for decision making | Scoring, Evaluation |
| Planning | Pre-computing action sequences | Strategy, Preparation |
| Replanning | Modifying plan based on new information | Adaptation |
| State Space | Set of all possible states | Search, Exploration |
| Strategy | High-level approach to achieving goals | Planning |
| Task | A unit of work to be completed | Action, Job |
| Tree-of-Thought | Exploring multiple reasoning branches | ToT, Search |
| Workflow | Sequence of tasks with dependencies | Pipeline, Process |

---

## B

### Beam Search

**Definition:** A search algorithm that explores multiple paths in parallel, keeping only the top-k most promising candidates at each step. Used in Tree-of-Thought to efficiently explore reasoning branches.

**Example:**
```python
from typing import List
import heapq

class BeamSearch:
    def __init__(self, beam_width: int = 3):
        self.beam_width = beam_width
    
    def search(self, root, expand_fn, score_fn, 
               is_goal_fn, max_depth: int = 5):
        """
        Beam search from root node.
        
        Args:
            root: Starting node
            expand_fn: Function to generate children
            score_fn: Function to score nodes
            is_goal_fn: Function to check if goal reached
            max_depth: Maximum search depth
        """
        # Initialize beam with root
        current_beam = [(score_fn(root), root)]
        
        for depth in range(max_depth):
            all_candidates = []
            
            # Expand each node in beam
            for score, node in current_beam:
                if is_goal_fn(node):
                    return node, score
                
                children = expand_fn(node)
                for child in children:
                    child_score = score_fn(child)
                    all_candidates.append((child_score, child))
            
            if not all_candidates:
                break
            
            # Keep top-k candidates
            current_beam = heapq.nlargest(
                self.beam_width, 
                all_candidates
            )
        
        # Return best from final beam
        if current_beam:
            return max(current_beam, key=lambda x: x[0])
        return None, 0

# Usage
beam = BeamSearch(beam_width=3)
best_node, best_score = beam.search(
    root=initial_state,
    expand_fn=generate_thoughts,
    score_fn=evaluate_thought,
    is_goal_fn=check_if_done
)
```

**Related terms:** Search, Top-k, Pruning

---

## C

### Chain-of-Thought (CoT)

**Definition:** A prompting technique where the LLM shows its reasoning step by step. CoT helps with complex problems by making intermediate reasoning explicit.

**Example:**
```
Question: Roger has 5 tennis balls. He buys 2 more cans of 3. How many does he have?

Without CoT: 11

With CoT:
Roger starts with 5 balls.
2 cans of 3 balls = 2 × 3 = 6 balls
Total = 5 + 6 = 11 balls
Answer: 11
```

**Code:**
```python
def chain_of_thought_prompt(question: str) -> str:
    """Create a CoT prompt."""
    return f"""Question: {question}

Let's solve this step by step:

Step 1: Understand the problem.
"""
    
def chain_of_thought_with_examples(question: str, 
                                   examples: list) -> str:
    """Few-shot CoT with examples."""
    examples_text = "\n\n".join([
        f"Q: {ex['question']}\nA: {ex['reasoning']}\nAnswer: {ex['answer']}"
        for ex in examples
    ])
    
    return f"""Here are some examples of step-by-step reasoning:

{examples_text}

Now solve this:
Q: {question}
A: Let's think step by step.
"""
```

**Related terms:** ReAct, Reasoning, Prompting

---

## D

### DAG (Directed Acyclic Graph)

**Definition:** A graph structure with directed edges and no cycles. Used to represent task dependencies where tasks have a clear ordering.

**Example:**
```python
from typing import Dict, List, Set
from collections import deque

class TaskDAG:
    """Directed Acyclic Graph for task dependencies."""
    
    def __init__(self):
        self.tasks: Dict[str, dict] = {}
        self.edges: Dict[str, List[str]] = {}  # task -> dependents
    
    def add_task(self, task_id: str, description: str):
        """Add a task to the DAG."""
        self.tasks[task_id] = {
            "id": task_id,
            "description": description,
            "status": "pending"
        }
        if task_id not in self.edges:
            self.edges[task_id] = []
    
    def add_dependency(self, task_id: str, depends_on: str):
        """Add dependency: task_id depends on depends_on."""
        if depends_on not in self.edges:
            self.edges[depends_on] = []
        self.edges[depends_on].append(task_id)
    
    def topological_sort(self) -> List[str]:
        """Get tasks in valid execution order."""
        # Calculate in-degrees
        in_degree = {t: 0 for t in self.tasks}
        for task, dependents in self.edges.items():
            for dep in dependents:
                in_degree[dep] = in_degree.get(dep, 0) + 1
        
        # Start with tasks that have no dependencies
        queue = deque([t for t, d in in_degree.items() if d == 0])
        order = []
        
        while queue:
            task = queue.popleft()
            order.append(task)
            
            for dependent in self.edges.get(task, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        return order
    
    def get_ready_tasks(self, completed: Set[str]) -> List[str]:
        """Get tasks whose dependencies are all completed."""
        ready = []
        for task_id, dependents in self.edges.items():
            for dep in dependents:
                if dep not in completed:
                    # Check if all dependencies of dep are completed
                    deps_of_dep = [
                        t for t, d in self.edges.items() 
                        if dep in d
                    ]
                    if all(d in completed for d in deps_of_dep):
                        ready.append(dep)
        return ready

# Usage
dag = TaskDAG()
dag.add_task("A", "Design")
dag.add_task("B", "Implement")
dag.add_task("C", "Test")
dag.add_dependency("B", "A")  # B depends on A
dag.add_dependency("C", "B")  # C depends on B

execution_order = dag.topological_sort()
print(f"Execution order: {execution_order}")  # ['A', 'B', 'C']
```

**Related terms:** Dependency Graph, Topological Sort

---

## G

### Goal Tree

**Definition:** A hierarchical decomposition of goals into sub-goals. The root is the main goal, and each level breaks it down further until reaching actionable tasks.

**Example:**
```python
@dataclass
class GoalNode:
    """A node in the goal tree."""
    goal: str
    subgoals: List["GoalNode"] = field(default_factory=list)
    completed: bool = False
    result: str = None
    
    def is_leaf(self) -> bool:
        return len(self.subgoals) == 0
    
    def get_all_leaves(self) -> List["GoalNode"]:
        if self.is_leaf():
            return [self]
        leaves = []
        for subgoal in self.subgoals:
            leaves.extend(subgoal.get_all_leaves())
        return leaves
    
    def to_dict(self) -> dict:
        return {
            "goal": self.goal,
            "completed": self.completed,
            "subgoals": [sg.to_dict() for sg in self.subgoals]
        }

class GoalTreePlanner:
    """Plans by decomposing goals into a tree."""
    
    def __init__(self, llm):
        self.llm = llm
    
    def decompose(self, goal: str, max_depth: int = 3,
                  current_depth: int = 0) -> GoalNode:
        """Recursively decompose goal into subgoals."""
        node = GoalNode(goal=goal)
        
        if current_depth >= max_depth:
            return node  # Leaf node at max depth
        
        # Ask LLM to decompose
        prompt = f"""Break this goal into 2-4 sub-goals:
Goal: {goal}

Return JSON array of sub-goals:
["subgoal 1", "subgoal 2"]
"""
        response = self.llm(prompt)
        
        try:
            subgoals = json.loads(response)
            for sg in subgoals:
                child = self.decompose(sg, max_depth, current_depth + 1)
                node.subgoals.append(child)
        except:
            pass  # Keep as leaf node
        
        return node
```

**Related terms:** Hierarchy, Decomposition, Task Tree

---

## P

### Planning

**Definition:** The process of determining a sequence of actions to achieve a goal. Planning can be done upfront (classical planning) or adaptively (reactive planning).

**Example:**
```python
class Planner:
    """Base class for planning agents."""
    
    def __init__(self, llm, tools: dict):
        self.llm = llm
        self.tools = tools
    
    def create_plan(self, goal: str, context: dict = None) -> List[dict]:
        """Create an action plan for achieving the goal."""
        prompt = self._build_planning_prompt(goal, context)
        response = self.llm(prompt)
        
        try:
            return json.loads(response)
        except:
            return [{"action": "llm_complete", "input": goal}]
    
    def _build_planning_prompt(self, goal: str, context: dict) -> str:
        """Build prompt for plan generation."""
        tools_desc = "\n".join([
            f"- {name}: {tool.__doc__ or 'No description'}"
            for name, tool in self.tools.items()
        ])
        
        return f"""Create a plan to achieve this goal.

Goal: {goal}

Available tools:
{tools_desc}

Return a JSON array of steps:
[
  {{
    "action": "tool_name",
    "input": "what to pass",
    "description": "what this step does"
  }}
]
"""
    
    def replan(self, original_plan: list, completed_steps: list,
               failed_step: dict, error: str) -> List[dict]:
        """Create a new plan after a failure."""
        prompt = f"""The following plan has failed. Create a new plan.

Original goal: {original_plan[0].get('description', 'Unknown')}
Completed steps: {completed_steps}
Failed step: {failed_step}
Error: {error}

Create a new plan that:
1. Skips or works around the failed step
2. Completes the remaining goal

Return JSON array of new steps:
"""
        response = self.llm(prompt)
        
        try:
            return json.loads(response)
        except:
            return []

# Usage
planner = Planner(llm=my_llm, tools=my_tools)
plan = planner.create_plan("Research and summarize AI agent papers")
```

**Related terms:** Strategy, Task Decomposition, Replanning

---

### Pruning

**Definition:** Removing branches or paths from a search tree that are unlikely to lead to good solutions. Pruning reduces the search space and improves efficiency.

**Example:**
```python
class TreePruner:
    """Prune unpromising branches from search tree."""
    
    def __init__(self, threshold: float = 0.2):
        self.threshold = threshold
    
    def prune_by_score(self, nodes: list) -> list:
        """Remove nodes below score threshold."""
        return [n for n in nodes if n.score >= self.threshold]
    
    def prune_by_diversity(self, nodes: list, 
                          min_similarity: float = 0.8) -> list:
        """Remove highly similar nodes, keeping diverse options."""
        if not nodes:
            return []
        
        pruned = [nodes[0]]
        
        for node in nodes[1:]:
            is_diverse = True
            for kept in pruned:
                similarity = self._calculate_similarity(
                    node.thought, kept.thought
                )
                if similarity > min_similarity:
                    is_diverse = False
                    break
            
            if is_diverse:
                pruned.append(node)
        
        return pruned
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Simple text similarity."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union

# Usage
pruner = TreePruner(threshold=0.3)
promising_nodes = pruner.prune_by_score(all_nodes)
diverse_nodes = pruner.prune_by_diversity(promising_nodes)
```

**Related terms:** Search, Optimization, Efficiency

---

## R

### Replanning

**Definition:** The process of modifying or creating a new plan when the original plan fails or when new information becomes available. Replanning is essential for robust agents.

**Example:**
```python
class AdaptivePlanner:
    """Planner that can adapt to changes and failures."""
    
    def __init__(self, llm, max_replans: int = 3):
        self.llm = llm
        self.max_replans = max_replans
        self.replan_count = 0
    
    def execute_with_replanning(self, goal: str, executor):
        """Execute goal with automatic replanning on failure."""
        plan = self.create_plan(goal)
        
        while self.replan_count < self.max_replans:
            result = executor.execute(plan)
            
            if result["success"]:
                return result
            
            # Failure - need to replan
            self.replan_count += 1
            plan = self.replan(
                goal, 
                plan, 
                result["completed"],
                result["failed_step"],
                result["error"]
            )
        
        return {"success": False, "error": "Max replans exceeded"}
    
    def replan(self, goal, original_plan, completed, 
               failed_step, error):
        """Create new plan accounting for what's done."""
        prompt = f"""Original goal: {goal}
Completed steps: {completed}
Failed step: {failed_step}
Error: {error}

Create a new plan that achieves the remaining goal.
Only include steps not yet completed.
"""
        response = self.llm(prompt)
        
        try:
            return json.loads(response)
        except:
            return []
```

**Related terms:** Adaptation, Recovery, Failure Handling

---

## S

### State Space

**Definition:** The set of all possible states an agent can be in. Planning can involve searching through this space to find a path from initial state to goal state.

**Example:**
```python
class StateSpaceSearch:
    """Search through state space to find solution path."""
    
    def __init__(self, transitions, goal_test):
        self.transitions = transitions  # state -> [possible_next_states]
        self.goal_test = goal_test
    
    def bfs(self, initial_state) -> list:
        """Breadth-first search through state space."""
        from collections import deque
        
        queue = deque([(initial_state, [initial_state])])
        visited = {initial_state}
        
        while queue:
            state, path = queue.popleft()
            
            if self.goal_test(state):
                return path
            
            for next_state in self.transitions(state):
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [next_state]))
        
        return None  # No path found
    
    def a_star(self, initial_state, heuristic):
        """A* search with heuristic."""
        import heapq
        
        open_set = [(0, initial_state, [initial_state])]
        g_scores = {initial_state: 0}
        
        while open_set:
            f_score, state, path = heapq.heappop(open_set)
            
            if self.goal_test(state):
                return path
            
            for next_state in self.transitions(state):
                tentative_g = g_scores[state] + 1
                
                if next_state not in g_scores or \
                   tentative_g < g_scores[next_state]:
                    g_scores[next_state] = tentative_g
                    f_score = tentative_g + heuristic(next_state)
                    heapq.heappush(
                        open_set, 
                        (f_score, next_state, path + [next_state])
                    )
        
        return None

# Usage
def puzzle_transitions(state):
    """Generate possible moves in sliding puzzle."""
    # Implementation depends on puzzle type
    pass

def puzzle_goal_test(state):
    """Check if puzzle is solved."""
    return state == goal_state

search = StateSpaceSearch(puzzle_transitions, puzzle_goal_test)
solution_path = search.bfs(initial_puzzle_state)
```

**Related terms:** Search, BFS, A*, Heuristic

---

## T

### Task Decomposition

**Definition:** Breaking a complex task into smaller, more manageable sub-tasks. This makes tasks easier to reason about, execute, and verify.

**Example:**
```python
class TaskDecomposer:
    """Decompose complex tasks into sub-tasks."""
    
    def __init__(self, llm):
        self.llm = llm
    
    def decompose(self, task: str, 
                  max_subtasks: int = 5) -> List[dict]:
        """Break task into sub-tasks."""
        prompt = f"""Break this task into {max_subtasks} or fewer sub-tasks.

Task: {task}

Each sub-task should be:
1. Specific and actionable
2. Independent enough to work on separately
3. Clear about what "done" looks like

Return JSON array:
[
  {{
    "name": "subtask name",
    "description": "what to do",
    "done_when": "completion criteria"
  }}
]
"""
        response = self.llm(prompt)
        
        try:
            return json.loads(response)
        except:
            return [{"name": task, "description": task, 
                    "done_when": "Task completed"}]

# Usage
decomposer = TaskDecomposer(llm=my_llm)
subtasks = decomposer.decompose(
    "Build a REST API with authentication"
)
for st in subtasks:
    print(f"- {st['name']}: {st['description']}")
```

**Related terms:** Decomposition, Breaking Down, Sub-tasks

---

## Quick Reference: Planning Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Planning System                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Goal ──► Task Decomposer ──► Task List                     │
│                                     │                       │
│                                     ▼                       │
│                              ┌─────────────┐               │
│                              │ Dependency  │               │
│                              │   Graph     │               │
│                              └──────┬──────┘               │
│                                     │                       │
│                                     ▼                       │
│                              ┌─────────────┐               │
│                              │  Scheduler  │               │
│                              └──────┬──────┘               │
│                                     │                       │
│                    ┌────────────────┼────────────────┐     │
│                    ▼                ▼                ▼     │
│              ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│              │  Task 1  │    │  Task 2  │    │  Task 3  │ │
│              └──────────┘    └──────────┘    └──────────┘ │
│                    │                │                │     │
│                    └────────────────┼────────────────┘     │
│                                     ▼                       │
│                              ┌─────────────┐               │
│                              │  Replanner  │               │
│                              └─────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 05](./05-planning-reasoning-lecture.md)** | **[Next: Lecture 06 →](./06-multi-agent-orchestration-glossary.md)**
