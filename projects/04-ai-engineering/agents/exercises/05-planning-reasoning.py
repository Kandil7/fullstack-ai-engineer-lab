"""
=============================================================
EXERCISE 05: Planning and Reasoning
=============================================================
Topic: Task Decomposition, Tree-of-Thought, and Plan Execution

Learning Objectives:
- Decompose complex tasks into subtasks
- Implement goal-oriented planning
- Use tree-of-thought reasoning
- Handle backtracking and replanning
- Add self-reflection and evaluation
- Execute plans with verification

Prerequisites:
- Python 3.10+
- json, dataclasses, enum, datetime
=============================================================
"""

import json
import time
import uuid
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Callable
from datetime import datetime
from collections import deque


# ============================================================
# SECTION 1: Task Decomposition
# ============================================================

class TaskStatus(Enum):
    """Status of a task in the planning system."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """A single task in a plan."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: list[str] = field(default_factory=list)
    subtasks: list["Task"] = field(default_factory=list)
    result: Any = None
    error: str = ""
    max_retries: int = 2
    retry_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    estimated_duration: float = 0.0
    actual_duration: float = 0.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "priority": self.priority.value,
            "dependencies": self.dependencies,
            "subtasks": len(self.subtasks),
            "result": str(self.result)[:100] if self.result else None,
            "error": self.error,
        }

    def can_execute(self, completed_tasks: set[str]) -> bool:
        """Check if all dependencies are met."""
        return all(dep in completed_tasks for dep in self.dependencies)

    def mark_complete(self, result: Any = None):
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now()

    def mark_failed(self, error: str):
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.error = error

    def mark_in_progress(self):
        """Mark task as in progress."""
        self.status = TaskStatus.IN_PROGRESS


# ============================================================
# SECTION 2: Task Decomposer
# ============================================================

class TaskDecomposer:
    """
    Breaks down complex tasks into manageable subtasks.
    Supports different decomposition strategies.
    """

    @staticmethod
    def decompose_by_steps(goal: str, steps: list[str]) -> Task:
        """Decompose a goal into sequential steps."""
        root = Task(name=f"Achieve: {goal}", description=f"Main goal: {goal}")
        prev_id = None

        for i, step in enumerate(steps):
            task = Task(
                name=step,
                description=f"Step {i+1} of the plan",
                priority=TaskPriority.HIGH if i < 2 else TaskPriority.MEDIUM,
            )
            if prev_id:
                task.dependencies = [prev_id]
            root.subtasks.append(task)
            prev_id = task.id

        return root

    @staticmethod
    def decompose_by_phases(goal: str, phases: dict[str, list[str]]) -> Task:
        """Decompose a goal into parallel phases."""
        root = Task(name=f"Achieve: {goal}", description=f"Main goal: {goal}")

        for phase_name, phase_steps in phases.items():
            phase_task = Task(
                name=phase_name,
                description=f"Phase: {phase_name}",
                priority=TaskPriority.HIGH,
            )
            for i, step in enumerate(phase_steps):
                subtask = Task(name=step, description=f"Step {i+1} in {phase_name}")
                phase_task.subtasks.append(subtask)
            root.subtasks.append(phase_task)

        return root

    @staticmethod
    def decompose_by_criteria(goal: str, criteria: list[str]) -> Task:
        """Decompose based on evaluation criteria."""
        root = Task(name=f"Achieve: {goal}", description=f"Goal with {len(criteria)} criteria")

        for criterion in criteria:
            task = Task(
                name=f"Verify: {criterion}",
                description=f"Ensure {criterion}",
                priority=TaskPriority.HIGH,
            )
            root.subtasks.append(task)

        return root

    @staticmethod
    def estimate_durations(task: Task, estimates: dict[str, float]):
        """Estimate durations for tasks based on name mapping."""
        for subtask in task.subtasks:
            if subtask.name in estimates:
                subtask.estimated_duration = estimates[subtask.name]
            if subtask.subtasks:
                TaskDecomposer.estimate_durations(subtask, estimates)


# ============================================================
# SECTION 3: Planner
# ============================================================

@dataclass
class Plan:
    """A complete execution plan."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    goal: str = ""
    root_task: Task = None
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "active"
    execution_log: list[dict] = field(default_factory=list)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks in the plan (flattened)."""
        tasks = []

        def collect(task: Task):
            tasks.append(task)
            for sub in task.subtasks:
                collect(sub)

        if self.root_task:
            collect(self.root_task)
        return tasks

    def get_ready_tasks(self, completed: set[str] = None) -> list[Task]:
        """Get tasks that are ready to execute (all deps met)."""
        completed = completed or set()
        ready = []
        for task in self.get_all_tasks():
            if task.status == TaskStatus.PENDING and task.can_execute(completed):
                ready.append(task)
        return ready

    def get_progress(self) -> dict:
        """Get plan execution progress."""
        all_tasks = self.get_all_tasks()
        completed = sum(1 for t in all_tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in all_tasks if t.status == TaskStatus.FAILED)
        in_progress = sum(1 for t in all_tasks if t.status == TaskStatus.IN_PROGRESS)
        total = len(all_tasks)

        return {
            "goal": self.goal,
            "total_tasks": total,
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "pending": total - completed - failed - in_progress,
            "progress_pct": round(completed / max(total, 1) * 100, 1),
            "status": self.status,
        }


class Planner:
    """
    Creates and manages execution plans.
    Supports different planning strategies.
    """

    def __init__(self):
        self.plans: list[Plan] = []
        self.decomposer = TaskDecomposer()

    def create_plan(self, goal: str, steps: list[str] = None) -> Plan:
        """Create a plan for a goal."""
        if steps:
            root_task = self.decomposer.decompose_by_steps(goal, steps)
        else:
            root_task = self.decomposer.decompose_by_steps(goal, [
                "Analyze the goal",
                "Gather required resources",
                "Execute core tasks",
                "Verify results",
                "Finalize",
            ])

        plan = Plan(goal=goal, root_task=root_task)
        self.plans.append(plan)
        return plan

    def create_phased_plan(self, goal: str, phases: dict[str, list[str]]) -> Plan:
        """Create a plan with parallel phases."""
        root_task = self.decomposer.decompose_by_phases(goal, phases)
        plan = Plan(goal=goal, root_task=root_task)
        self.plans.append(plan)
        return plan

    def replan(self, plan: Plan, failed_task: Task, reason: str) -> Plan:
        """Create a new plan to handle a failed task."""
        # Create alternative steps
        alternative_steps = [
            f"Retry: {failed_task.name} with different approach",
            "Verify the alternative approach",
            "Continue with remaining tasks",
        ]

        new_root = self.decomposer.decompose_by_steps(
            f"Recover from: {failed_task.name}",
            alternative_steps
        )

        new_plan = Plan(
            goal=f"Recovery plan for: {plan.goal}",
            root_task=new_root,
        )
        self.plans.append(new_plan)
        return new_plan


# ============================================================
# SECTION 4: Tree-of-Thought Reasoning
# ============================================================

@dataclass
class ThoughtNode:
    """A node in the thought tree."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content: str = ""
    score: float = 0.0
    depth: int = 0
    parent_id: Optional[str] = None
    children: list["ThoughtNode"] = field(default_factory=list)
    is_terminal: bool = False
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content[:80],
            "score": self.score,
            "depth": self.depth,
            "children": len(self.children),
            "terminal": self.is_terminal,
        }


class TreeOfThought:
    """
    Implements Tree-of-Thought reasoning.
    Explores multiple reasoning paths and selects the best one.
    """

    def __init__(self, max_depth: int = 3, branching_factor: int = 3, max_leaves: int = 10):
        self.max_depth = max_depth
        self.branching_factor = branching_factor
        self.max_leaves = max_leaves
        self.root: Optional[ThoughtNode] = None
        self.all_nodes: list[ThoughtNode] = []

    def _generate_thoughts(self, node: ThoughtNode, problem: str) -> list[ThoughtNode]:
        """Generate child thoughts from a parent node."""
        thoughts = []
        problem_lower = problem.lower()

        # Generate diverse thoughts based on the problem context
        thought_templates = [
            f"Approach A: Direct computation for '{problem[:50]}...'",
            f"Approach B: Research-based solution for '{problem[:50]}...'",
            f"Approach C: Step-by-step decomposition of '{problem[:50]}...'",
            f"Approach D: Analogy-based reasoning for '{problem[:50]}...'",
            f"Approach E: Process of elimination for '{problem[:50]}...'",
        ]

        # Select thoughts based on depth
        start_idx = node.depth * 2 % len(thought_templates)
        for i in range(self.branching_factor):
            idx = (start_idx + i) % len(thought_templates)
            child = ThoughtNode(
                content=thought_templates[idx],
                depth=node.depth + 1,
                parent_id=node.id,
            )
            thoughts.append(child)

        return thoughts[:self.branching_factor]

    def _evaluate_thought(self, node: ThoughtNode, problem: str) -> float:
        """Evaluate the quality of a thought (heuristic scoring)."""
        # In production, this would use an LLM
        content = node.content.lower()
        problem_words = set(problem.lower().split())

        # Score based on various factors
        score = 0.5  # Base score

        # Specificity bonus
        if any(w in content for w in problem_words):
            score += 0.1

        # Depth penalty (prefer shallower solutions)
        score -= node.depth * 0.05

        # Approach diversity bonus
        if "direct" in content:
            score += 0.1
        elif "step-by-step" in content:
            score += 0.15
        elif "research" in content:
            score += 0.12

        return min(max(score, 0.0), 1.0)

    def _is_terminal(self, node: ThoughtNode, problem: str) -> bool:
        """Check if a node is a terminal (solution found)."""
        return node.depth >= self.max_depth

    def solve(self, problem: str, verbose: bool = True) -> list[ThoughtNode]:
        """
        Run Tree-of-Thought reasoning to solve a problem.
        Returns the path of best thoughts.
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Tree-of-Thought: {problem[:80]}")
            print(f"{'='*60}")

        # Initialize root
        self.root = ThoughtNode(
            content=f"Initial reasoning for: {problem}",
            depth=0,
        )
        self.all_nodes = [self.root]

        # BFS exploration
        queue = deque([self.root])
        leaves = []

        while queue and len(leaves) < self.max_leaves:
            current = queue.popleft()

            # Evaluate current node
            current.score = self._evaluate_thought(current, problem)
            if verbose:
                print(f"\n  Depth {current.depth}: {current.content[:60]}... (score: {current.score:.2f})")

            # Check if terminal
            if self._is_terminal(current, problem):
                current.is_terminal = True
                leaves.append(current)
                continue

            # Generate children
            children = self._generate_thoughts(current, problem)
            for child in children:
                child.score = self._evaluate_thought(child, problem)
                current.children.append(child)
                self.all_nodes.append(child)
                queue.append(child)

                if verbose:
                    print(f"    → {child.content[:50]}... (score: {child.score:.2f})")

        # Find best path
        best_leaf = max(leaves, key=lambda n: n.score) if leaves else self.root
        path = self._trace_path(best_leaf)

        if verbose:
            print(f"\n  Best path ({len(path)} nodes):")
            for node in path:
                print(f"    [{node.depth}] {node.content[:60]}... (score: {node.score:.2f})")

        return path

    def _trace_path(self, node: ThoughtNode) -> list[ThoughtNode]:
        """Trace the path from root to a leaf node."""
        path = []
        current = node
        while current:
            path.append(current)
            # Find parent
            parent = None
            for n in self.all_nodes:
                if n.id == current.parent_id:
                    parent = n
                    break
            current = parent
        path.reverse()
        return path

    def get_tree_stats(self) -> dict:
        """Get statistics about the thought tree."""
        if not self.all_nodes:
            return {"nodes": 0}

        depths = [n.depth for n in self.all_nodes]
        scores = [n.score for n in self.all_nodes]

        return {
            "total_nodes": len(self.all_nodes),
            "max_depth": max(depths) if depths else 0,
            "avg_score": round(sum(scores) / len(scores), 3) if scores else 0,
            "leaves": sum(1 for n in self.all_nodes if n.is_terminal),
            "branching_factor": self.branching_factor,
        }


# ============================================================
# SECTION 5: Backtracking and Replanning
# ============================================================

class BacktrackingPlanner:
    """
    Planner that supports backtracking when a step fails.
    Tries alternative approaches before giving up.
    """

    def __init__(self, max_backtracks: int = 3):
        self.max_backtracks = max_backtracks
        self.backtrack_count = 0
        self.execution_history: list[dict] = []

    def execute_with_backtrack(
        self,
        steps: list[dict],
        executor: Callable,
        verbose: bool = True,
    ) -> dict:
        """
        Execute steps with backtracking on failure.
        Each step: {"name": str, "args": dict, "alternatives": list[dict]}
        """
        results = []
        completed_steps = set()

        for i, step in enumerate(steps):
            if verbose:
                print(f"\n  Step {i+1}: {step['name']}")

            success = False
            attempts = [step] + step.get("alternatives", [])

            for attempt_idx, attempt in enumerate(attempts):
                if attempt_idx > 0 and verbose:
                    print(f"    Backtrack attempt {attempt_idx}: {attempt['name']}")

                try:
                    result = executor(attempt["name"], **attempt.get("args", {}))
                    results.append({
                        "step": attempt["name"],
                        "result": result,
                        "attempt": attempt_idx,
                        "success": True,
                    })
                    completed_steps.add(attempt["name"])
                    success = True

                    if verbose:
                        print(f"    ✅ Success: {str(result)[:60]}...")
                    break

                except Exception as e:
                    if verbose:
                        print(f"    ❌ Failed: {e}")
                    self.backtrack_count += 1

                    if self.backtrack_count >= self.max_backtracks:
                        if verbose:
                            print(f"    ⚠️ Max backtracks reached")
                        break

            if not success:
                results.append({
                    "step": step["name"],
                    "result": None,
                    "success": False,
                    "error": "All attempts failed",
                })

        self.execution_history = results
        return {
            "completed": len([r for r in results if r["success"]]),
            "failed": len([r for r in results if not r["success"]]),
            "total_backtracks": self.backtrack_count,
            "results": results,
        }


# ============================================================
# SECTION 6: Self-Reflection and Evaluation
# ============================================================

@dataclass
class ReflectionEntry:
    """A single reflection entry."""
    timestamp: datetime = field(default_factory=datetime.now)
    what_went_well: list[str] = field(default_factory=list)
    what_went_wrong: list[str] = field(default_factory=list)
    lessons_learned: list[str] = field(default_factory=list)
    improvements: list[str] = field(default_factory=list)
    overall_score: float = 0.0


class SelfReflector:
    """
    Evaluates agent performance and generates reflections
    for continuous improvement.
    """

    def __init__(self):
        self.reflections: list[ReflectionEntry] = []
        self._lessons_db: list[str] = []

    def reflect_on_plan(self, plan: Plan) -> ReflectionEntry:
        """Reflect on a completed or failed plan."""
        all_tasks = plan.get_all_tasks()
        completed = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
        failed = [t for t in all_tasks if t.status == TaskStatus.FAILED]

        reflection = ReflectionEntry()

        # Analyze successes
        if completed:
            reflection.what_went_well = [
                f"Completed: {t.name}" for t in completed[:5]
            ]

        # Analyze failures
        if failed:
            reflection.what_went_wrong = [
                f"Failed: {t.name} - {t.error}" for t in failed[:5]
            ]

        # Generate lessons
        if failed:
            reflection.lessons_learned.append(
                f"Need better error handling for tasks like: {failed[0].name}"
            )
        if completed:
            reflection.lessons_learned.append(
                f"Successfully completed {len(completed)}/{len(all_tasks)} tasks"
            )

        # Generate improvements
        if failed:
            reflection.improvements.append("Add retry logic for critical tasks")
            reflection.improvements.append("Better input validation before execution")

        # Calculate score
        total = len(all_tasks) or 1
        reflection.overall_score = round(len(completed) / total, 2)

        self.reflections.append(reflection)
        self._lessons_db.extend(reflection.lessons_learned)

        return reflection

    def reflect_on_step(self, step_name: str, success: bool, result: Any = None, error: str = "") -> ReflectionEntry:
        """Reflect on a single step execution."""
        reflection = ReflectionEntry()

        if success:
            reflection.what_went_well.append(f"{step_name} completed successfully")
        else:
            reflection.what_went_wrong.append(f"{step_name} failed: {error}")
            reflection.lessons_learned.append(f"Handle edge cases in {step_name}")
            reflection.improvements.append(f"Add validation for {step_name} inputs")

        reflection.overall_score = 1.0 if success else 0.0
        self.reflections.append(reflection)

        return reflection

    def get_improvement_suggestions(self) -> list[str]:
        """Get improvement suggestions based on reflection history."""
        suggestions = set()
        for reflection in self.reflections:
            suggestions.update(reflection.improvements)
        return list(suggestions)

    def get_stats(self) -> dict:
        """Get reflection statistics."""
        if not self.reflections:
            return {"total_reflections": 0}

        scores = [r.overall_score for r in self.reflections]
        return {
            "total_reflections": len(self.reflections),
            "avg_score": round(sum(scores) / len(scores), 2),
            "total_lessons": sum(len(r.lessons_learned) for r in self.reflections),
            "total_improvements": sum(len(r.improvements) for r in self.reflections),
        }


# ============================================================
# SECTION 7: Plan Executor with Verification
# ============================================================

class PlanExecutor:
    """
    Executes plans with step verification, error handling,
    and progress tracking.
    """

    def __init__(self):
        self.planner = Planner()
        self.reflector = SelfReflector()
        self.backtracker = BacktrackingPlanner(max_backtracks=3)
        self.execution_results: list[dict] = []

    def execute_plan(self, plan: Plan, executor: Callable, verbose: bool = True) -> dict:
        """Execute a plan with verification."""
        if verbose:
            print(f"\n{'='*60}")
            print(f"Executing Plan: {plan.goal}")
            print(f"{'='*60}")

        completed_tasks = set()
        results = []

        # Get all tasks in dependency order
        all_tasks = plan.get_all_tasks()

        # Simple topological sort
        ordered = self._topological_sort(all_tasks)

        for task in ordered:
            if task.status != TaskStatus.PENDING:
                continue

            # Check dependencies
            if not task.can_execute(completed_tasks):
                if verbose:
                    print(f"\n  ⏳ Waiting: {task.name} (deps: {task.dependencies})")
                continue

            if verbose:
                print(f"\n  ▶ Executing: {task.name}")

            task.mark_in_progress()

            try:
                start_time = time.time()
                result = executor(task.name, task.description)
                duration = (time.time() - start_time) * 1000

                task.mark_complete(result)
                task.actual_duration = duration
                completed_tasks.add(task.id)

                results.append({
                    "task": task.name,
                    "status": "completed",
                    "result": str(result)[:100],
                    "duration_ms": round(duration, 2),
                })

                # Reflect on success
                self.reflector.reflect_on_step(task.name, True, result)

                if verbose:
                    print(f"  ✅ {task.name}: {str(result)[:60]}...")

            except Exception as e:
                task.mark_failed(str(e))

                results.append({
                    "task": task.name,
                    "status": "failed",
                    "error": str(e),
                })

                # Reflect on failure
                self.reflector.reflect_on_step(task.name, False, error=str(e))

                if verbose:
                    print(f"  ❌ {task.name}: {e}")

        # Final reflection
        reflection = self.reflector.reflect_on_plan(plan)

        progress = plan.get_progress()
        if verbose:
            print(f"\n  Progress: {progress['progress_pct']}% complete")
            print(f"  Score: {reflection.overall_score}")

        return {
            "plan_progress": progress,
            "results": results,
            "reflection": {
                "score": reflection.overall_score,
                "lessons": reflection.lessons_learned,
                "improvements": reflection.improvements,
            },
        }

    def _topological_sort(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by dependencies."""
        task_map = {t.id: t for t in tasks}
        visited = set()
        result = []

        def dfs(task_id: str):
            if task_id in visited:
                return
            visited.add(task_id)
            task = task_map.get(task_id)
            if task:
                for dep in task.dependencies:
                    if dep in task_map:
                        dfs(dep)
                result.append(task)

        for task in tasks:
            dfs(task.id)

        return result


# ============================================================
# SECTION 8: Complete Planning System
# ============================================================

class PlanningSystem:
    """
    Complete planning system combining decomposition, planning,
    Tree-of-Thought reasoning, and execution with verification.
    """

    def __init__(self):
        self.executor = PlanExecutor()
        self.tot = TreeOfThought(max_depth=3, branching_factor=3)

    def solve_problem(self, problem: str, steps: list[str] = None, verbose: bool = True) -> dict:
        """
        End-to-end problem solving:
        1. Tree-of-Thought reasoning
        2. Task decomposition
        3. Planning
        4. Execution with verification
        5. Reflection
        """
        if verbose:
            print(f"\n{'#' * 60}")
            print(f"  PLANNING SYSTEM: Solving '{problem[:60]}'")
            print(f"{'#' * 60}")

        # Step 1: Tree-of-Thought reasoning
        if verbose:
            print(f"\n  Phase 1: Tree-of-Thought Reasoning")
        thought_path = self.tot.solve(problem, verbose=verbose)

        # Step 2: Create plan
        if verbose:
            print(f"\n  Phase 2: Task Decomposition & Planning")

        if not steps:
            steps = [
                "Analyze the problem requirements",
                "Gather necessary information",
                "Apply the chosen approach",
                "Verify the solution",
                "Document the results",
            ]

        plan = self.executor.planner.create_plan(problem, steps)

        if verbose:
            print(f"  Plan created with {len(plan.get_all_tasks())} tasks")

        # Step 3: Execute plan
        if verbose:
            print(f"\n  Phase 3: Plan Execution")

        def mock_executor(task_name: str, description: str) -> str:
            """Mock executor for demonstration."""
            time.sleep(0.01)  # Simulate work
            return f"Completed: {task_name}"

        execution_result = self.executor.execute_plan(plan, mock_executor, verbose=verbose)

        # Step 4: Summary
        if verbose:
            print(f"\n  Phase 4: Summary")

        return {
            "problem": problem,
            "thought_path": [n.to_dict() for n in thought_path],
            "plan": plan.get_progress(),
            "execution": execution_result,
            "tree_stats": self.tot.get_tree_stats(),
            "reflection_stats": self.executor.reflector.get_stats(),
            "improvement_suggestions": self.executor.reflector.get_improvement_suggestions(),
        }


# ============================================================
# SECTION 9: Running the Exercises
# ============================================================

def exercise_1_task_decomposition():
    """Exercise 5.1: Task decomposition."""
    print("\n" + "=" * 60)
    print("EXERCISE 5.1: Task Decomposition")
    print("=" * 60)

    decomposer = TaskDecomposer()

    # Sequential decomposition
    print("\n  Sequential Decomposition:")
    plan = decomposer.decompose_by_steps("Build a RAG system", [
        "Design data pipeline",
        "Implement document loader",
        "Set up vector store",
        "Create retrieval engine",
        "Build generation pipeline",
        "Test end-to-end",
    ])

    for i, task in enumerate(plan.subtasks):
        deps = f" (deps: {task.dependencies})" if task.dependencies else ""
        print(f"    {i+1}. {task.name}{deps}")

    # Phased decomposition
    print("\n  Phased Decomposition:")
    phased = decomposer.decompose_by_phases("Launch product", {
        "Planning": ["Define requirements", "Create timeline", "Assign resources"],
        "Development": ["Build core features", "Write tests", "Code review"],
        "Deployment": ["Set up CI/CD", "Deploy to staging", "Production release"],
    })

    for phase in phased.subtasks:
        print(f"\n    Phase: {phase.name}")
        for step in phase.subtasks:
            print(f"      - {step.name}")


def exercise_2_planner():
    """Exercise 5.2: Planner operations."""
    print("\n" + "=" * 60)
    print("EXERCISE 5.2: Planner Operations")
    print("=" * 60)

    planner = Planner()

    # Create a plan
    plan = planner.create_plan("Analyze customer feedback", [
        "Collect feedback data",
        "Clean and preprocess",
        "Run sentiment analysis",
        "Generate insights report",
    ])

    print(f"\n  Plan: {plan.goal}")
    print(f"  Tasks: {len(plan.get_all_tasks())}")

    # Show task details
    for task in plan.get_all_tasks():
        print(f"\n    Task: {task.name}")
        print(f"    Status: {task.status.value}")
        print(f"    ID: {task.id}")

    # Check ready tasks
    ready = plan.get_ready_tasks()
    print(f"\n  Ready tasks: {[t.name for t in ready]}")


def exercise_3_tree_of_thought():
    """Exercise 5.3: Tree-of-Thought reasoning."""
    print("\n" + "=" * 60)
    print("EXERCISE 5.3: Tree-of-Thought Reasoning")
    print("=" * 60)

    tot = TreeOfThought(max_depth=3, branching_factor=2)
    path = tot.solve("How to build a scalable AI system?")

    print(f"\n  Tree Statistics: {json.dumps(tot.get_tree_stats(), indent=4)}")


def exercise_4_backtracking():
    """Exercise 5.4: Backtracking and replanning."""
    print("\n" + "=" * 60)
    print("EXERCISE 5.4: Backtracking and Replanning")
    print("=" * 60)

    planner = BacktrackingPlanner(max_backtracks=3)

    # Define steps with alternatives
    steps = [
        {
            "name": "fetch_data",
            "args": {"source": "api"},
            "alternatives": [
                {"name": "fetch_data", "args": {"source": "cache"}},
                {"name": "fetch_data", "args": {"source": "backup"}},
            ],
        },
        {
            "name": "process_data",
            "args": {},
            "alternatives": [
                {"name": "process_data_simple", "args": {}},
            ],
        },
    ]

    # Mock executor that fails on first attempt
    call_count = {"fetch_data": 0}

    def mock_executor(task_name: str, **kwargs) -> str:
        call_count[task_name] = call_count.get(task_name, 0) + 1
        source = kwargs.get("source", "")

        if task_name == "fetch_data" and source == "api" and call_count["fetch_data"] <= 1:
            raise ConnectionError("API unavailable")

        return f"Result from {task_name}({source})"

    result = planner.execute_with_backtrack(steps, mock_executor, verbose=True)
    print(f"\n  Result: {json.dumps({k: v for k, v in result.items() if k != 'results'}, indent=4)}")


def exercise_5_self_reflection():
    """Exercise 5.5: Self-reflection and evaluation."""
    print("\n" + "=" * 60)
    print("EXERCISE 5.5: Self-Reflection")
    print("=" * 60)

    reflector = SelfReflector()

    # Simulate some task completions
    test_cases = [
        ("Data collection", True, "Data collected successfully"),
        ("Data processing", True, "Data processed"),
        ("Model training", False, "Out of memory error"),
        ("Model evaluation", True, "Evaluation complete"),
    ]

    for task_name, success, result_or_error in test_cases:
        if success:
            reflection = reflector.reflect_on_step(task_name, True, result=result_or_error)
        else:
            reflection = reflector.reflect_on_step(task_name, False, error=result_or_error)
        print(f"\n  Reflected on: {task_name}")
        print(f"    Score: {reflection.overall_score}")
        if reflection.lessons_learned:
            print(f"    Lessons: {reflection.lessons_learned}")

    # Get improvement suggestions
    suggestions = reflector.get_improvement_suggestions()
    print(f"\n  Improvement Suggestions:")
    for s in suggestions:
        print(f"    - {s}")

    print(f"\n  Reflection Stats: {json.dumps(reflector.get_stats(), indent=4)}")


def exercise_6_plan_execution():
    """Exercise 5.6: Complete plan execution with verification."""
    print("\n" + "=" * 60)
    print("EXERCISE 5.6: Plan Execution with Verification")
    print("=" * 60)

    system = PlanningSystem()
    result = system.solve_problem(
        "Optimize database query performance",
        steps=[
            "Profile current queries",
            "Identify slow queries",
            "Add appropriate indexes",
            "Optimize query patterns",
            "Benchmark improvements",
        ],
        verbose=True,
    )

    print(f"\n  Final Summary:")
    print(f"    Tree nodes explored: {result['tree_stats']['total_nodes']}")
    print(f"    Plan progress: {result['plan']['progress_pct']}%")
    print(f"    Reflection score: {result['reflection_stats']['avg_score']}")
    print(f"    Improvements suggested: {len(result['improvement_suggestions'])}")


def exercise_7_advanced_planning():
    """Exercise 5.7: Advanced planning patterns."""
    print("\n" + "=" * 60)
    print("EXERCISE 5.7: Advanced Planning Patterns")
    print("=" * 60)

    # Pattern 1: Hierarchical Planning
    print("\n  Pattern 1: Hierarchical Planning")
    print("  " + "-" * 40)

    class HierarchicalPlanner:
        def __init__(self):
            self.levels = {}

        def add_level(self, name: str, tasks: list[str]):
            self.levels[name] = tasks

        def plan(self, goal: str) -> dict:
            """Create a hierarchical plan."""
            return {
                "goal": goal,
                "strategic": ["Define success criteria", "Identify resources", "Set timeline"],
                "tactical": ["Break into phases", "Assign responsibilities", "Set milestones"],
                "operational": ["Daily tasks", "Weekly reviews", "Monthly adjustments"],
            }

    h_planner = HierarchicalPlanner()
    h_plan = h_planner.plan("Improve system reliability")
    for level, tasks in h_plan.items():
        if isinstance(tasks, list):
            print(f"\n    {level.upper()}:")
            for task in tasks:
                print(f"      - {task}")

    # Pattern 2: Conditional Planning
    print("\n  Pattern 2: Conditional Planning")
    print("  " + "-" * 40)

    class ConditionalPlanner:
        def plan_with_conditions(self, goal: str, conditions: dict) -> dict:
            """Create a plan that adapts based on conditions."""
            plan = {"goal": goal, "branches": []}

            for condition, steps in conditions.items():
                plan["branches"].append({
                    "condition": condition,
                    "steps": steps,
                })

            return plan

    c_planner = ConditionalPlanner()
    c_plan = c_planner.plan_with_conditions("Deploy application", {
        "if tests_pass": ["Deploy to staging", "Run smoke tests", "Deploy to production"],
        "if tests_fail": ["Fix failing tests", "Re-run test suite", "Deploy to staging"],
        "if performance_issue": ["Profile application", "Optimize bottlenecks", "Re-test"],
    })

    for branch in c_plan["branches"]:
        print(f"\n    IF {branch['condition']}:")
        for step in branch["steps"]:
            print(f"      → {step}")

    # Pattern 3: Iterative Refinement
    print("\n  Pattern 3: Iterative Refinement")
    print("  " + "-" * 40)

    class IterativePlanner:
        def __init__(self, max_iterations: int = 5):
            self.max_iterations = max_iterations
            self.iterations = []

        def refine(self, initial_plan: list[str], feedback_fn) -> list[str]:
            """Refine a plan through iterations."""
            current_plan = initial_plan

            for i in range(self.max_iterations):
                feedback = feedback_fn(current_plan)
                if feedback["score"] >= 0.9:
                    break

                # Refine based on feedback
                improved = []
                for step in current_plan:
                    if step in feedback.get("weak_steps", []):
                        improved.append(f"[IMPROVED] {step}")
                    else:
                        improved.append(step)

                current_plan = improved
                self.iterations.append({
                    "iteration": i + 1,
                    "score": feedback["score"],
                    "changes": len(feedback.get("weak_steps", [])),
                })

            return current_plan

    planner = IterativePlanner(max_iterations=3)
    initial = ["Analyze", "Design", "Implement", "Test", "Deploy"]

    def feedback(plan):
        weak = [p for p in plan if "IMPROVED" not in p and p != plan[-1]]
        return {"score": 0.5 + len([p for p in plan if "IMPROVED" in p]) * 0.2, "weak_steps": weak[:2]}

    refined = planner.refine(initial, feedback)
    print(f"\n    Initial: {initial}")
    print(f"    Refined: {refined}")
    print(f"    Iterations: {len(planner.iterations)}")


def exercise_8_full_pipeline():
    """Exercise 5.8: End-to-end planning pipeline."""
    print("\n" + "=" * 60)
    print("EXERCISE 5.8: Full Planning Pipeline")
    print("=" * 60)

    system = PlanningSystem()
    result = system.solve_problem(
        "Build a production-ready chatbot",
        verbose=False,
    )

    print(f"\n  Problem: {result['problem']}")
    print(f"  Thought path: {len(result['thought_path'])} nodes explored")
    print(f"  Plan progress: {result['plan']['progress_pct']}%")
    print(f"  Execution: {len(result['execution']['results'])} tasks")
    print(f"  Reflection score: {result['reflection_stats']['avg_score']}")
    print(f"  Suggestions: {result['improvement_suggestions']}")


# ============================================================
# Main: Run all exercises
# ============================================================

if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║  EXERCISE 05: Planning and Reasoning                       ║")
    print("║  Task Decomposition, ToT, Backtracking, Reflection         ║")
    print("╚" + "═" * 58 + "╝")

    exercises = [
        ("5.1", "Task Decomposition", exercise_1_task_decomposition),
        ("5.2", "Planner Operations", exercise_2_planner),
        ("5.3", "Tree-of-Thought", exercise_3_tree_of_thought),
        ("5.4", "Backtracking", exercise_4_backtracking),
        ("5.5", "Self-Reflection", exercise_5_self_reflection),
        ("5.6", "Plan Execution", exercise_6_plan_execution),
        ("5.7", "Advanced Patterns", exercise_7_advanced_planning),
        ("5.8", "Full Pipeline", exercise_8_full_pipeline),
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
1. Task decomposition breaks complex goals into manageable steps
2. Tree-of-Thought explores multiple reasoning paths
3. Backtracking enables recovery from failed approaches
4. Self-reflection drives continuous improvement
5. Plan verification ensures quality execution
6. Hierarchical planning addresses different abstraction levels
7. The complete pipeline: Think → Plan → Execute → Reflect → Improve
""")
