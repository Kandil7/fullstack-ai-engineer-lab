"""
=============================================================
Exercise 06: Multi-Agent Orchestration
=============================================================

Topic Overview:
Multi-agent orchestration coordinates multiple specialized agents
to solve complex tasks. This exercise covers:

1. Orchestrator-Worker Pattern - Central coordinator delegating tasks
2. Sequential vs Parallel Execution - Running agents in different orders
3. DAG-Based Workflows - Complex dependency graphs
4. Task Delegation - Intelligent routing to specialist agents
5. Result Aggregation - Combining outputs from multiple agents

Key Concepts:
- Orchestration reduces complexity by decomposing problems
- Parallel execution improves throughput for independent tasks
- DAGs model real-world dependencies between tasks
- Proper delegation matches tasks to agent capabilities
- Aggregation patterns include merge, reduce, and consensus

Prerequisites:
- Understanding of agent fundamentals (Exercise 01)
- Familiarity with LLM integration patterns
=============================================================
"""

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import heapq


# ============================================================
# Core Data Structures
# ============================================================

class AgentStatus(Enum):
    """Status of an agent in the system."""
    IDLE = "idle"
    BUSY = "busy"
    FAILED = "failed"
    OFFLINE = "offline"


class TaskStatus(Enum):
    """Status of a task."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Priority levels for task scheduling."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """Represents a unit of work for agents."""
    task_id: str
    name: str
    description: str
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    agent_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other):
        """Enable priority queue ordering."""
        return self.priority.value > other.priority.value


@dataclass
class Agent:
    """Represents an agent capable of executing tasks."""
    agent_id: str
    name: str
    capabilities: List[str]
    status: AgentStatus = AgentStatus.IDLE
    max_concurrent: int = 1
    current_tasks: List[str] = field(default_factory=list)
    completed_tasks: int = 0
    failed_tasks: int = 0
    avg_latency_ms: float = 0.0

    def can_handle(self, task: Task) -> bool:
        """Check if agent can handle a given task."""
        return task.name in self.capabilities or "general" in self.capabilities

    def is_available(self) -> bool:
        """Check if agent can accept new tasks."""
        return (self.status == AgentStatus.IDLE and
                len(self.current_tasks) < self.max_concurrent)


@dataclass
class WorkflowResult:
    """Result of a complete workflow execution."""
    workflow_id: str
    status: str
    task_results: Dict[str, Any]
    execution_time_ms: float
    total_tokens: int = 0
    total_cost: float = 0.0
    errors: List[str] = field(default_factory=list)


# ============================================================
# Example 1: Orchestrator-Worker Pattern
# ============================================================

class OrchestratorWorkerSystem:
    """
    Orchestrator-Worker pattern implementation.
    
    The orchestrator coordinates multiple worker agents, delegating
    tasks based on capabilities and managing the overall workflow.
    """

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.orchestrator_agent = Agent(
            agent_id="orchestrator",
            name="Orchestrator",
            capabilities=["general"],
            max_concurrent=10
        )
        self.task_queue: List[Task] = []
        self.completed_tasks: Dict[str, Task] = {}
        self._lock = asyncio.Lock()

    def register_agent(self, agent: Agent) -> None:
        """Register a worker agent with the orchestrator."""
        self.agents[agent.agent_id] = agent
        print(f"  Registered agent: {agent.name} ({agent.agent_id})")
        print(f"    Capabilities: {agent.capabilities}")

    def _find_best_agent(self, task: Task) -> Optional[Agent]:
        """Find the best available agent for a task."""
        candidates = [
            agent for agent in self.agents.values()
            if agent.can_handle(task) and agent.is_available()
        ]
        if not candidates:
            return None

        # Select agent with lowest current load
        return min(candidates, key=lambda a: len(a.current_tasks))

    async def delegate_task(self, task: Task) -> None:
        """Delegate a task to the best available agent."""
        async with self._lock:
            agent = self._find_best_agent(task)
            if agent:
                task.status = TaskStatus.RUNNING
                task.agent_id = agent.agent_id
                agent.current_tasks.append(task.task_id)
                agent.status = AgentStatus.BUSY
                print(f"  Delegated '{task.name}' to {agent.name}")
            else:
                self.task_queue.append(task)
                print(f"  Queued '{task.name}' (no available agents)")

    async def execute_task(self, task: Task) -> Any:
        """Execute a task (simulated with async sleep)."""
        agent = self.agents.get(task.agent_id)
        if not agent:
            raise ValueError(f"No agent assigned to task {task.task_id}")

        # Simulate task execution
        execution_time = 0.1 + (hash(task.task_id) % 100) / 1000
        await asyncio.sleep(execution_time)

        # Simulate result
        result = {
            "task_id": task.task_id,
            "agent_id": agent.agent_id,
            "output": f"Result for {task.name}",
            "latency_ms": execution_time * 1000
        }

        return result

    async def process_task(self, task: Task) -> Any:
        """Process a single task through the orchestration pipeline."""
        try:
            await self.delegate_task(task)

            if task.status == TaskStatus.PENDING:
                return None  # Still in queue

            result = await self.execute_task(task)

            async with self._lock:
                task.status = TaskStatus.COMPLETED
                task.result = result
                task.completed_at = datetime.now()
                self.completed_tasks[task.task_id] = task

                agent = self.agents[task.agent_id]
                agent.current_tasks.remove(task.task_id)
                agent.completed_tasks += 1
                agent.avg_latency_ms = (
                    (agent.avg_latency_ms * (agent.completed_tasks - 1) +
                     result["latency_ms"]) / agent.completed_tasks
                )
                if not agent.current_tasks:
                    agent.status = AgentStatus.IDLE

            print(f"  Completed: {task.name} (by {agent.name})")
            return result

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            print(f"  Failed: {task.name} - {e}")
            return None

    async def run_workflow(self, tasks: List[Task]) -> WorkflowResult:
        """Execute a complete workflow with multiple tasks."""
        workflow_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        print(f"\n{'='*60}")
        print(f"Orchestrator-Worker Workflow: {workflow_id}")
        print(f"{'='*60}")

        # Process tasks based on dependencies
        completed_ids: Set[str] = set()
        results: Dict[str, Any] = {}
        errors: List[str] = []

        while len(completed_ids) < len(tasks):
            # Find tasks whose dependencies are met
            ready = [
                t for t in tasks
                if t.task_id not in completed_ids and
                t.status == TaskStatus.PENDING and
                all(dep in completed_ids for dep in t.dependencies)
            ]

            if not ready:
                break

            # Process ready tasks concurrently
            batch_results = await asyncio.gather(
                *[self.process_task(task) for task in ready],
                return_exceptions=True
            )

            for task, result in zip(ready, batch_results):
                if isinstance(result, Exception):
                    errors.append(f"{task.name}: {result}")
                elif result:
                    results[task.task_id] = result
                    completed_ids.add(task.task_id)

        execution_time = (time.time() - start_time) * 1000

        return WorkflowResult(
            workflow_id=workflow_id,
            status="completed" if not errors else "partial",
            task_results=results,
            execution_time_ms=execution_time,
            errors=errors
        )


# ============================================================
# Example 2: Sequential vs Parallel Execution
# ============================================================

class ExecutionStrategy:
    """
    Demonstrates different execution strategies for multi-agent systems.
    """

    @staticmethod
    async def sequential_execution(
        tasks: List[Task],
        execute_fn: Callable
    ) -> List[Any]:
        """
        Execute tasks one after another.
        
        Pros:
        - Simple to implement
        - Predictable execution order
        - Easy debugging
        
        Cons:
        - Slow for independent tasks
        - One failure blocks all subsequent tasks
        """
        results = []
        for task in tasks:
            result = await execute_fn(task)
            results.append(result)
        return results

    @staticmethod
    async def parallel_execution(
        tasks: List[Task],
        execute_fn: Callable
    ) -> List[Any]:
        """
        Execute all tasks concurrently.
        
        Pros:
        - Maximum throughput for independent tasks
        - Better resource utilization
        
        Cons:
        - More complex error handling
        - Potential resource contention
        - Order of results not guaranteed
        """
        results = await asyncio.gather(
            *[execute_fn(task) for task in tasks],
            return_exceptions=True
        )
        return results

    @staticmethod
    async def bounded_parallel_execution(
        tasks: List[Task],
        execute_fn: Callable,
        max_concurrent: int = 3
    ) -> List[Any]:
        """
        Execute tasks concurrently with a concurrency limit.
        
        Pros:
        - Controls resource usage
        - Balances speed and stability
        
        Cons:
        - May be slower than unlimited parallel
        - Requires careful tuning
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        results = []

        async def bounded_execute(task: Task) -> Any:
            async with semaphore:
                return await execute_fn(task)

        results = await asyncio.gather(
            *[bounded_execute(task) for task in tasks],
            return_exceptions=True
        )
        return results

    @staticmethod
    async def adaptive_execution(
        tasks: List[Task],
        execute_fn: Callable,
        initial_concurrent: int = 2
    ) -> List[Any]:
        """
        Adaptive execution that adjusts concurrency based on success rate.
        
        Features:
        - Starts conservative
        - Increases concurrency on success
        - Backs off on failures
        """
        current_concurrent = initial_concurrent
        results = []
        batch_size = 3

        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            batch_concurrent = min(current_concurrent, len(batch))

            semaphore = asyncio.Semaphore(batch_concurrent)

            async def bounded(task: Task) -> Any:
                async with semaphore:
                    return await execute_fn(task)

            batch_results = await asyncio.gather(
                *[bounded(task) for task in batch],
                return_exceptions=True
            )

            # Count successes and failures
            successes = sum(1 for r in batch_results if not isinstance(r, Exception))
            failures = sum(1 for r in batch_results if isinstance(r, Exception))

            # Adapt concurrency
            if failures == 0 and current_concurrent < 10:
                current_concurrent = min(current_concurrent + 1, 10)
            elif failures > successes:
                current_concurrent = max(current_concurrent - 1, 1)

            results.extend(batch_results)

        return results


# ============================================================
# Example 3: DAG-Based Workflow Engine
# ============================================================

class DAGWorkflowEngine:
    """
    Directed Acyclic Graph workflow engine for complex agent orchestration.
    
    Supports:
    - Dependency tracking
    - Topological execution ordering
    - Parallel execution of independent nodes
    - Conditional branching
    - Error propagation
    """

    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[str, List[str]] = defaultdict(list)
        self.in_degree: Dict[str, int] = defaultdict(int)
        self.results: Dict[str, Any] = {}

    def add_node(
        self,
        node_id: str,
        name: str,
        executor: Callable,
        metadata: Optional[Dict] = None
    ) -> None:
        """Add a node to the DAG."""
        self.nodes[node_id] = {
            "name": name,
            "executor": executor,
            "metadata": metadata or {}
        }
        if node_id not in self.in_degree:
            self.in_degree[node_id] = 0

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add a dependency edge between nodes."""
        self.edges[from_node].append(to_node)
        self.in_degree[to_node] += 1

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the DAG has no cycles."""
        visited = set()
        rec_stack = set()
        errors = []

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.edges.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    errors.append(f"Cycle detected: {node} -> {neighbor}")
                    return True

            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                dfs(node)

        return len(errors) == 0, errors

    def get_ready_nodes(self) -> List[str]:
        """Get nodes with all dependencies satisfied."""
        ready = []
        for node_id, degree in self.in_degree.items():
            if degree == 0 and node_id not in self.results:
                ready.append(node_id)
        return ready

    def topological_sort(self) -> List[str]:
        """Get topological ordering of nodes."""
        in_degree_copy = dict(self.in_degree)
        queue = [n for n, d in in_degree_copy.items() if d == 0]
        order = []

        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in self.edges.get(node, []):
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)

        return order

    async def execute(self) -> Dict[str, Any]:
        """Execute the DAG workflow."""
        valid, errors = self.validate()
        if not valid:
            raise ValueError(f"Invalid DAG: {errors}")

        execution_order = self.topological_sort()
        print(f"\nDAG Execution Order: {' -> '.join(execution_order)}")

        for node_id in execution_order:
            node = self.nodes[node_id]

            # Gather inputs from predecessors
            inputs = {}
            for prev_node in self.edges:
                if node_id in self.edges[prev_node]:
                    inputs[prev_node] = self.results.get(prev_node)

            # Execute node
            print(f"  Executing: {node['name']}")
            result = await node["executor"](inputs, **node["metadata"])
            self.results[node_id] = result

        return self.results


# ============================================================
# Example 4: Intelligent Task Delegation
# ============================================================

class TaskDelegator:
    """
    Intelligent task delegation system that routes tasks to
    the most appropriate agents based on multiple factors.
    """

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.task_history: List[Dict] = []
        self.capability_scores: Dict[str, Dict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )

    def register_agent(self, agent: Agent) -> None:
        """Register an agent."""
        self.agents[agent.agent_id] = agent
        # Initialize capability scores
        for cap in agent.capabilities:
            self.capability_scores[agent.agent_id][cap] = 1.0

    def update_scores(self, agent_id: str, capability: str, success: bool) -> None:
        """Update agent capability scores based on performance."""
        current = self.capability_scores[agent_id][capability]
        if success:
            self.capability_scores[agent_id][capability] = min(2.0, current * 1.1)
        else:
            self.capability_scores[agent_id][capability] = max(0.1, current * 0.9)

    def calculate_agent_score(self, agent: Agent, task: Task) -> float:
        """
        Calculate a score for assigning a task to an agent.
        
        Factors:
        - Capability match (0-1)
        - Current load (0-1)
        - Historical performance (0-2)
        - Availability bonus (0-0.5)
        """
        # Capability match
        cap_score = self.capability_scores[agent.agent_id].get(task.name, 0.5)

        # Current load (lower is better)
        load = len(agent.current_tasks) / max(agent.max_concurrent, 1)
        load_score = 1.0 - load

        # Historical performance
        perf_score = 1.0
        if agent.completed_tasks > 0:
            success_rate = 1 - (agent.failed_tasks / agent.completed_tasks)
            perf_score = success_rate

        # Availability bonus
        avail_bonus = 0.5 if agent.is_available() else 0.0

        return cap_score * 0.4 + load_score * 0.2 + perf_score * 0.3 + avail_bonus

    def delegate(self, task: Task) -> Optional[Agent]:
        """Delegate a task to the best scoring agent."""
        candidates = [
            agent for agent in self.agents.values()
            if task.name in agent.capabilities or "general" in agent.capabilities
        ]

        if not candidates:
            return None

        # Score each candidate
        scored = [
            (agent, self.calculate_agent_score(agent, task))
            for agent in candidates
        ]
        scored.sort(key=lambda x: x[1], reverse=True)

        # Return best agent
        best_agent, best_score = scored[0]
        print(f"  Delegating '{task.name}' to {best_agent.name} "
              f"(score: {best_score:.2f})")
        return best_agent

    def record_outcome(self, task: Task, agent_id: str, success: bool) -> None:
        """Record task outcome for learning."""
        self.task_history.append({
            "task_id": task.task_id,
            "task_name": task.name,
            "agent_id": agent_id,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
        self.update_scores(agent_id, task.name, success)


# ============================================================
# Example 5: Result Aggregation Patterns
# ============================================================

class ResultAggregator:
    """
    Aggregates results from multiple agents using various patterns.
    """

    @staticmethod
    def merge_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge results from multiple agents into a single dict.
        
        Use when: Combining complementary information from different agents.
        """
        merged = {}
        for result in results:
            if result and "output" in result:
                merged.update(result["output"] if isinstance(result["output"], dict)
                            else {"output": result["output"]})
        return merged

    @staticmethod
    def reduce_results(
        results: List[Any],
        reducer: Callable[[Any, Any], Any]
    ) -> Any:
        """
        Reduce multiple results to a single value.
        
        Use when: Aggregating numerical results or finding a single answer.
        """
        if not results:
            return None

        acc = results[0]
        for result in results[1:]:
            acc = reducer(acc, result)
        return acc

    @staticmethod
    def consensus_results(
        results: List[str],
        threshold: float = 0.5
    ) -> Optional[str]:
        """
        Find consensus among agent results using majority voting.
        
        Use when: Multiple agents provide the same type of answer.
        """
        from collections import Counter
        counts = Counter(results)
        total = len(results)

        for answer, count in counts.most_common():
            if count / total >= threshold:
                return answer
        return None

    @staticmethod
    def best_of_results(
        results: List[Dict[str, Any]],
        scoring_fn: Callable[[Dict], float]
    ) -> Optional[Dict]:
        """
        Select the best result based on a scoring function.
        
        Use when: Multiple agents provide competing answers.
        """
        if not results:
            return None

        scored = [(result, scoring_fn(result)) for result in results]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0]

    @staticmethod
    def weighted_aggregate(
        results: List[Dict[str, Any]],
        weights: List[float]
    ) -> Dict[str, Any]:
        """
        Aggregate results using weighted averages.
        
        Use when: Some agents are more reliable than others.
        """
        if not results or not weights:
            return {}

        weighted_sum = defaultdict(float)
        total_weight = sum(weights)

        for result, weight in zip(results, weights):
            if result and "scores" in result:
                for key, value in result["scores"].items():
                    weighted_sum[key] += value * weight

        return {k: v / total_weight for k, v in weighted_sum.items()}


# ============================================================
# Example 6: Complete Multi-Agent System
# ============================================================

class MultiAgentOrchestrator:
    """
    Complete multi-agent orchestrator combining all patterns.
    """

    def __init__(self):
        self.orchestrator = OrchestratorWorkerSystem()
        self.delegator = TaskDelegator()
        self.aggregator = ResultAggregator()
        self.workflow_engine = DAGWorkflowEngine()

    async def create_specialized_agents(self) -> None:
        """Create a team of specialized agents."""
        agents = [
            Agent(
                agent_id="researcher",
                name="Research Agent",
                capabilities=["research", "analysis"],
                max_concurrent=3
            ),
            Agent(
                agent_id="coder",
                name="Coding Agent",
                capabilities=["coding", "debugging"],
                max_concurrent=2
            ),
            Agent(
                agent_id="reviewer",
                name="Review Agent",
                capabilities=["review", "testing"],
                max_concurrent=2
            ),
            Agent(
                agent_id="writer",
                name="Writing Agent",
                capabilities=["writing", "documentation"],
                max_concurrent=2
            ),
            Agent(
                agent_id="generalist",
                name="General Agent",
                capabilities=["general"],
                max_concurrent=5
            ),
        ]

        for agent in agents:
            self.orchestrator.register_agent(agent)
            self.delegator.register_agent(agent)

    async def execute_research_task(self) -> Dict[str, Any]:
        """Execute a research workflow using DAG."""
        print("\n" + "="*60)
        print("Research Workflow (DAG-based)")
        print("="*60)

        # Define DAG nodes
        async def gather_info(inputs: Dict) -> Dict:
            await asyncio.sleep(0.1)
            return {"sources": ["source1", "source2"], "raw_data": "gathered"}

        async def analyze_data(inputs: Dict) -> Dict:
            await asyncio.sleep(0.15)
            return {"insights": ["insight1", "insight2"], "patterns": ["p1"]}

        async def generate_report(inputs: Dict) -> Dict:
            await asyncio.sleep(0.1)
            return {"report": "Research report content", "recommendations": ["r1"]}

        async def review_report(inputs: Dict) -> Dict:
            await asyncio.sleep(0.08)
            return {"feedback": "Looks good", "score": 0.9}

        # Build DAG
        self.workflow_engine.add_node("gather", "Gather Information", gather_info)
        self.workflow_engine.add_node("analyze", "Analyze Data", analyze_data)
        self.workflow_engine.add_node("report", "Generate Report", generate_report)
        self.workflow_engine.add_node("review", "Review Report", review_report)

        # Add dependencies
        self.workflow_engine.add_edge("gather", "analyze")
        self.workflow_engine.add_edge("analyze", "report")
        self.workflow_engine.add_edge("report", "review")

        # Execute
        results = await self.workflow_engine.execute()
        print(f"\nFinal Results: {json.dumps(results, indent=2, default=str)}")
        return results

    async def run_example(self) -> None:
        """Run the complete multi-agent orchestration example."""
        print("\n" + "="*60)
        print("MULTI-AGENT ORCHESTRATION EXAMPLE")
        print("="*60)

        await self.create_specialized_agents()

        # Create tasks with dependencies
        tasks = [
            Task("t1", "research", "Gather market data",
                 TaskPriority.HIGH, dependencies=[]),
            Task("t2", "analysis", "Analyze trends",
                 TaskPriority.HIGH, dependencies=["t1"]),
            Task("t3", "coding", "Build prototype",
                 TaskPriority.MEDIUM, dependencies=["t2"]),
            Task("t4", "review", "Code review",
                 TaskPriority.MEDIUM, dependencies=["t3"]),
            Task("t5", "documentation", "Write docs",
                 TaskPriority.LOW, dependencies=["t3"]),
        ]

        # Run orchestration workflow
        result = await self.orchestrator.run_workflow(tasks)
        print(f"\nWorkflow Result: {result.status}")
        print(f"Execution Time: {result.execution_time_ms:.1f}ms")

        # Execute DAG-based research workflow
        await self.execute_research_task()


# ============================================================
# Main Entry Point
# ============================================================

async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("EXERCISE 06: MULTI-AGENT ORCHESTRATION")
    print("="*60)

    # Example 1-6: Complete multi-agent system
    system = MultiAgentOrchestrator()
    await system.run_example()

    # Example 2: Execution strategies demonstration
    print("\n" + "="*60)
    print("EXECUTION STRATEGIES COMPARISON")
    print("="*60)

    async def simple_execute(task: Task) -> str:
        await asyncio.sleep(0.05)
        return f"Done: {task.name}"

    tasks = [Task(f"t{i}", "general", f"Task {i}") for i in range(5)]

    strategy = ExecutionStrategy()

    # Sequential
    start = time.time()
    await strategy.sequential_execution(tasks, simple_execute)
    seq_time = time.time() - start
    print(f"  Sequential: {seq_time*1000:.1f}ms")

    # Parallel
    start = time.time()
    await strategy.parallel_execution(tasks, simple_execute)
    par_time = time.time() - start
    print(f"  Parallel: {par_time*1000:.1f}ms")

    # Bounded parallel
    start = time.time()
    await strategy.bounded_parallel_execution(tasks, simple_execute, max_concurrent=3)
    bp_time = time.time() - start
    print(f"  Bounded Parallel (3): {bp_time*1000:.1f}ms")

    print(f"\nSpeedup (parallel): {seq_time/par_time:.1f}x")

    print("\n" + "="*60)
    print("EXERCISE COMPLETE")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
