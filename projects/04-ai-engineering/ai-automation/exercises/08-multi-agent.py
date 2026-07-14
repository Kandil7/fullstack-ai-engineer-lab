"""
Exercise 08: Multi-Agent Systems
==================================
Master multi-agent architectures: orchestrator-worker patterns, agent
communication, sequential vs parallel execution, consensus patterns,
and message passing.

Prerequisites:
    pip install openai asyncio pydantic

Environment Variables (.env):
    OPENAI_API_KEY=sk-...
"""

import os
import json
import time
import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from datetime import datetime
from collections import defaultdict
from enum import Enum


# ---------------------------------------------------------------------------
# 1. Agent Base Classes
# ---------------------------------------------------------------------------

class AgentRole(Enum):
    """Roles agents can play in a system."""
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    ROUTER = "router"
    EVALUATOR = "evaluator"
    CRITIC = "critic"


@dataclass
class AgentMessage:
    """Message passed between agents."""
    sender: str
    receiver: str
    content: Any
    message_type: str = "task"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)


@dataclass
class AgentState:
    """Current state of an agent."""
    agent_id: str
    status: str = "idle"  # idle, busy, error
    current_task: str | None = None
    tasks_completed: int = 0
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())


class BaseAgent:
    """Base class for all agents."""

    def __init__(self, agent_id: str, role: AgentRole):
        self.agent_id = agent_id
        self.role = role
        self.state = AgentState(agent_id=agent_id)
        self.inbox: list[AgentMessage] = []
        self.outbox: list[AgentMessage] = []
        self.capabilities: list[str] = []

    async def process_message(self, message: AgentMessage) -> AgentMessage | None:
        """Process an incoming message."""
        raise NotImplementedError

    def send_message(self, receiver: str, content: Any,
                    message_type: str = "task") -> AgentMessage:
        """Create and queue an outgoing message."""
        message = AgentMessage(
            sender=self.agent_id,
            receiver=receiver,
            content=content,
            message_type=message_type,
        )
        self.outbox.append(message)
        return message

    def receive_message(self, message: AgentMessage):
        """Receive a message."""
        self.inbox.append(message)

    def get_state(self) -> dict:
        """Get agent state."""
        return {
            "agent_id": self.agent_id,
            "role": self.role.value,
            "status": self.state.status,
            "tasks_completed": self.state.tasks_completed,
            "inbox_size": len(self.inbox),
            "outbox_size": len(self.outbox),
        }


# ---------------------------------------------------------------------------
# 2. Orchestrator-Worker Pattern
# ---------------------------------------------------------------------------

class OrchestratorAgent(BaseAgent):
    """Orchestrator that coordinates multiple worker agents."""

    def __init__(self, agent_id: str = "orchestrator"):
        super().__init__(agent_id, AgentRole.ORCHESTRATOR)
        self.workers: dict[str, BaseAgent] = {}
        self.task_queue: list[dict] = []
        self.results: dict[str, Any] = {}

    def register_worker(self, worker: BaseAgent):
        """Register a worker agent."""
        self.workers[worker.agent_id] = worker

    def decompose_task(self, task: str) -> list[dict]:
        """Break a task into subtasks for workers."""
        # Simple decomposition (in real use, use LLM)
        subtasks = [
            {"id": f"subtask_{i}", "description": f"Part {i+1} of: {task}",
             "assigned_to": None}
            for i in range(3)
        ]
        return subtasks

    def assign_task(self, subtask: dict, worker_id: str):
        """Assign a subtask to a worker."""
        subtask["assigned_to"] = worker_id
        message = self.send_message(
            worker_id,
            {"type": "task", "subtask": subtask},
            "task_assignment"
        )
        if worker_id in self.workers:
            self.workers[worker_id].receive_message(message)

    async def coordinate(self, task: str) -> dict[str, Any]:
        """Coordinate task execution across workers."""
        self.state.status = "busy"
        self.state.current_task = task

        # Decompose task
        subtasks = self.decompose_task(task)

        # Assign to workers
        worker_ids = list(self.workers.keys())
        for i, subtask in enumerate(subtasks):
            worker_id = worker_ids[i % len(worker_ids)]
            self.assign_task(subtask, worker_id)

        # Collect results
        results = {}
        for worker_id, worker in self.workers.items():
            result = await self._execute_worker_task(worker)
            results[worker_id] = result

        # Aggregate results
        final_result = self._aggregate_results(results)

        self.state.status = "idle"
        self.state.tasks_completed += 1
        self.state.current_task = None

        return {
            "task": task,
            "subtasks": subtasks,
            "results": results,
            "final_result": final_result,
        }

    async def _execute_worker_task(self, worker: BaseAgent) -> Any:
        """Execute a task on a worker."""
        # Simulate worker execution
        worker.state.status = "busy"
        await asyncio.sleep(0.1)
        worker.state.status = "idle"
        worker.state.tasks_completed += 1
        return {"status": "completed", "output": f"Result from {worker.agent_id}"}

    def _aggregate_results(self, results: dict[str, Any]) -> str:
        """Aggregate results from multiple workers."""
        outputs = [r.get("output", "") for r in results.values()]
        return " | ".join(outputs)


class WorkerAgent(BaseAgent):
    """Worker agent that executes specific tasks."""

    def __init__(self, agent_id: str, capabilities: list[str] = None):
        super().__init__(agent_id, AgentRole.WORKER)
        self.capabilities = capabilities or []

    async def process_message(self, message: AgentMessage) -> AgentMessage | None:
        """Process a task message."""
        if message.message_type == "task_assignment":
            task = message.content.get("subtask", {})
            result = await self._execute_task(task)
            return self.send_message(
                message.sender,
                {"type": "task_result", "result": result},
                "task_result"
            )
        return None

    async def _execute_task(self, task: dict) -> dict:
        """Execute a specific task."""
        self.state.status = "busy"
        self.state.current_task = task.get("description", "")

        # Simulate work
        await asyncio.sleep(0.05)

        self.state.status = "idle"
        self.state.tasks_completed += 1
        self.state.current_task = None

        return {
            "status": "completed",
            "output": f"Completed: {task.get('description', 'unknown')}",
        }


def demo_orchestrator_worker():
    """Demonstrate orchestrator-worker pattern."""
    print("\n" + "=" * 60)
    print("1. ORCHESTRATOR-WORKER PATTERN")
    print("=" * 60)

    # Create orchestrator
    orchestrator = OrchestratorAgent()

    # Create workers with different capabilities
    workers = [
        WorkerAgent("worker_research", ["research", "analysis"]),
        WorkerAgent("worker_writing", ["writing", "summarization"]),
        WorkerAgent("worker_coding", ["coding", "testing"]),
    ]

    # Register workers
    for worker in workers:
        orchestrator.register_worker(worker)

    # Coordinate a task
    task = "Write a comprehensive report on AI trends"
    result = asyncio.run(orchestrator.coordinate(task))

    print(f"\nTask: {task}")
    print(f"\nSubtasks created: {len(result['subtasks'])}")
    for subtask in result['subtasks']:
        print(f"  - {subtask['description']} -> {subtask['assigned_to']}")

    print(f"\nFinal Result: {result['final_result']}")

    # Show worker states
    print("\nWorker States:")
    for worker in workers:
        state = worker.get_state()
        print(f"  {state['agent_id']}: {state['tasks_completed']} tasks completed")


# ---------------------------------------------------------------------------
# 3. Agent Communication Patterns
# ---------------------------------------------------------------------------

class MessageBus:
    """Central message bus for agent communication."""

    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = defaultdict(list)
        self.message_history: list[AgentMessage] = []
        self.channels: dict[str, list[AgentMessage]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to a topic."""
        self.subscribers[topic].append(callback)

    def publish(self, message: AgentMessage, topic: str = "default"):
        """Publish a message to a topic."""
        self.message_history.append(message)
        self.channels[topic].append(message)

        # Notify subscribers
        for callback in self.subscribers.get(topic, []):
            callback(message)

    def get_messages(self, topic: str, limit: int = 10) -> list[AgentMessage]:
        """Get recent messages from a topic."""
        return self.channels[topic][-limit:]

    def broadcast(self, message: AgentMessage):
        """Broadcast to all topics."""
        for topic in self.channels:
            self.publish(message, topic)


class CommunicationAgent(BaseAgent):
    """Agent that communicates via message bus."""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentRole.WORKER)
        self.message_bus = message_bus
        self.message_bus.subscribe("tasks", self._handle_task)

    def _handle_task(self, message: AgentMessage):
        """Handle incoming task messages."""
        if message.receiver == self.agent_id or message.receiver == "all":
            self.receive_message(message)

    async def process_message(self, message: AgentMessage) -> AgentMessage | None:
        """Process a message and respond."""
        # Process task
        result = await self._work(message.content)

        # Publish result
        response = self.send_message(
            message.sender,
            {"type": "result", "data": result},
            "results"
        )
        self.message_bus.publish(response, "results")

        return response

    async def _work(self, content: Any) -> Any:
        """Perform work on the content."""
        await asyncio.sleep(0.05)
        return f"Processed by {self.agent_id}"


def demo_agent_communication():
    """Demonstrate agent communication patterns."""
    print("\n" + "=" * 60)
    print("2. AGENT COMMUNICATION PATTERNS")
    print("=" * 60)

    # Create message bus
    bus = MessageBus()

    # Create communicating agents
    agent_a = CommunicationAgent("agent_a", bus)
    agent_b = CommunicationAgent("agent_b", bus)

    # Subscribe to results
    results_received = []
    def on_result(msg: AgentMessage):
        results_received.append(msg)

    bus.subscribe("results", on_result)

    # Send task
    task_message = AgentMessage(
        sender="user",
        receiver="agent_a",
        content={"task": "Analyze data"},
        message_type="task",
    )
    bus.publish(task_message, "tasks")

    # Process messages
    async def process():
        for msg in agent_a.inbox:
            await agent_a.process_message(msg)

    asyncio.run(process())

    print(f"\nMessages in history: {len(bus.message_history)}")
    print(f"Results received: {len(results_received)}")

    # Show communication flow
    print("\nCommunication Flow:")
    for msg in bus.message_history:
        print(f"  {msg.sender} -> {msg.receiver}: {msg.message_type}")


# ---------------------------------------------------------------------------
# 4. Sequential vs Parallel Execution
# ---------------------------------------------------------------------------

class TaskGraph:
    """Define task dependencies for sequential/parallel execution."""

    def __init__(self):
        self.tasks: dict[str, dict] = {}
        self.dependencies: dict[str, list[str]] = defaultdict(list)

    def add_task(self, task_id: str, func: Callable, **kwargs):
        """Add a task to the graph."""
        self.tasks[task_id] = {"func": func, "kwargs": kwargs, "result": None}

    def add_dependency(self, task_id: str, depends_on: str):
        """Add a dependency between tasks."""
        self.dependencies[task_id].append(depends_on)

    def get_ready_tasks(self, completed: set[str]) -> list[str]:
        """Get tasks whose dependencies are all completed."""
        ready = []
        for task_id in self.tasks:
            if task_id in completed:
                continue
            deps = self.dependencies[task_id]
            if all(d in completed for d in deps):
                ready.append(task_id)
        return ready


async def execute_sequential(tasks: list[Callable]) -> list[Any]:
    """Execute tasks sequentially."""
    results = []
    for task in tasks:
        result = await task()
        results.append(result)
    return results


async def execute_parallel(tasks: list[Callable]) -> list[Any]:
    """Execute tasks in parallel."""
    results = await asyncio.gather(*[task() for task in tasks])
    return list(results)


async def execute_dag(graph: TaskGraph) -> dict[str, Any]:
    """Execute tasks according to DAG dependencies."""
    completed = set()
    results = {}

    while len(completed) < len(graph.tasks):
        ready = graph.get_ready_tasks(completed)
        if not ready:
            break

        # Execute ready tasks in parallel
        async def run_task(task_id):
            task = graph.tasks[task_id]
            result = await task["func"](**task["kwargs"])
            return task_id, result

        task_results = await asyncio.gather(*[run_task(tid) for tid in ready])

        for task_id, result in task_results:
            results[task_id] = result
            completed.add(task_id)

    return results


def demo_sequential_vs_parallel():
    """Demonstrate sequential vs parallel execution."""
    print("\n" + "=" * 60)
    print("3. SEQUENTIAL VS PARALLEL EXECUTION")
    print("=" * 60)

    # Define sample tasks
    async def task_a():
        await asyncio.sleep(0.1)
        return "Result A"

    async def task_b():
        await asyncio.sleep(0.1)
        return "Result B"

    async def task_c():
        await asyncio.sleep(0.1)
        return "Result C"

    tasks = [task_a, task_b, task_c]

    # Sequential execution
    start = time.time()
    seq_results = asyncio.run(execute_sequential(tasks))
    seq_time = time.time() - start
    print(f"\nSequential: {seq_time:.3f}s")
    print(f"  Results: {seq_results}")

    # Parallel execution
    start = time.time()
    par_results = asyncio.run(execute_parallel(tasks))
    par_time = time.time() - start
    print(f"\nParallel: {par_time:.3f}s")
    print(f"  Results: {par_results}")

    # DAG execution
    graph = TaskGraph()
    graph.add_task("fetch_data", task_a)
    graph.add_task("process_data", task_b)
    graph.add_task("generate_report", task_c)
    graph.add_dependency("process_data", "fetch_data")
    graph.add_dependency("generate_report", "process_data")

    start = time.time()
    dag_results = asyncio.run(execute_dag(graph))
    dag_time = time.time() - start
    print(f"\nDAG Execution: {dag_time:.3f}s")
    print(f"  Results: {dag_results}")

    print(f"\nSpeedup (Parallel vs Sequential): {seq_time/par_time:.1f}x")


# ---------------------------------------------------------------------------
# 5. Consensus Patterns
# ---------------------------------------------------------------------------

class ConsensusProtocol:
    """Implement consensus patterns for multi-agent decision making."""

    def __init__(self, agents: list[BaseAgent]):
        self.agents = agents
        self.votes: dict[str, list] = defaultdict(list)

    async def majority_vote(self, proposal: Any) -> dict[str, Any]:
        """Majority vote consensus."""
        votes = []
        for agent in self.agents:
            # Each agent votes (simulated)
            vote = await self._get_vote(agent, proposal)
            votes.append({"agent": agent.agent_id, "vote": vote})

        # Count votes
        vote_counts = defaultdict(int)
        for v in votes:
            vote_counts[v["vote"]] += 1

        # Determine winner
        winner = max(vote_counts, key=vote_counts.get)
        consensus_reached = vote_counts[winner] > len(votes) / 2

        return {
            "proposal": proposal,
            "votes": votes,
            "winner": winner,
            "consensus_reached": consensus_reached,
            "vote_counts": dict(vote_counts),
        }

    async def weighted_voting(self, proposal: Any,
                             weights: dict[str, float]) -> dict[str, Any]:
        """Weighted voting consensus."""
        votes = []
        for agent in self.agents:
            vote = await self._get_vote(agent, proposal)
            weight = weights.get(agent.agent_id, 1.0)
            votes.append({"agent": agent.agent_id, "vote": vote, "weight": weight})

        # Calculate weighted votes
        weighted_counts = defaultdict(float)
        for v in votes:
            weighted_counts[v["vote"]] += v["weight"]

        winner = max(weighted_counts, key=weighted_counts.get)
        total_weight = sum(v["weight"] for v in votes)
        consensus_reached = weighted_counts[winner] > total_weight / 2

        return {
            "proposal": proposal,
            "votes": votes,
            "winner": winner,
            "consensus_reached": consensus_reached,
            "weighted_counts": dict(weighted_counts),
        }

    async def _get_vote(self, agent: BaseAgent, proposal: Any) -> str:
        """Get vote from an agent (simulated)."""
        # Simulate different agents having different opinions
        import random
        return random.choice(["approve", "reject", "abstain"])


class DebateProtocol:
    """Multi-round debate protocol for decision making."""

    def __init__(self, agents: list[BaseAgent], max_rounds: int = 3):
        self.agents = agents
        self.max_rounds = max_rounds
        self.rounds: list[dict] = []

    async def debate(self, topic: str) -> dict[str, Any]:
        """Run a multi-round debate."""
        arguments = []

        for round_num in range(self.max_rounds):
            round_arguments = []

            for agent in self.agents:
                # Each agent provides argument
                argument = await self._get_argument(agent, topic, arguments)
                round_arguments.append({
                    "agent": agent.agent_id,
                    "round": round_num + 1,
                    "argument": argument,
                })

            arguments.extend(round_arguments)
            self.rounds.append({"round": round_num + 1, "arguments": round_arguments})

        # Determine winner based on argument quality
        winner = self._determine_winner(arguments)

        return {
            "topic": topic,
            "total_rounds": self.max_rounds,
            "arguments": arguments,
            "winner": winner,
        }

    async def _get_argument(self, agent: BaseAgent, topic: str,
                           previous_arguments: list) -> str:
        """Get argument from an agent."""
        # Simulate argument generation
        return f"Argument from {agent.agent_id} on round {len(previous_arguments) // len(self.agents) + 1}"

    def _determine_winner(self, arguments: list) -> str:
        """Determine debate winner."""
        # Simple heuristic: most arguments wins
        agent_counts = defaultdict(int)
        for arg in arguments:
            agent_counts[arg["agent"]] += 1
        return max(agent_counts, key=agent_counts.get)


def demo_consensus_patterns():
    """Demonstrate consensus patterns."""
    print("\n" + "=" * 60)
    print("4. CONSENSUS PATTERNS")
    print("=" * 60)

    # Create agents
    agents = [
        WorkerAgent("analyst_1", ["analysis"]),
        WorkerAgent("analyst_2", ["analysis"]),
        WorkerAgent("analyst_3", ["analysis"]),
    ]

    # Majority vote
    protocol = ConsensusProtocol(agents)
    proposal = "Should we adopt microservices architecture?"

    result = asyncio.run(protocol.majority_vote(proposal))
    print(f"\nMajority Vote:")
    print(f"  Proposal: {proposal}")
    print(f"  Winner: {result['winner']}")
    print(f"  Consensus: {result['consensus_reached']}")
    print(f"  Vote counts: {result['vote_counts']}")

    # Debate
    debate = DebateProtocol(agents, max_rounds=2)
    topic = "Best approach for scaling AI services"

    debate_result = asyncio.run(debate.debate(topic))
    print(f"\nDebate:")
    print(f"  Topic: {topic}")
    print(f"  Total Rounds: {debate_result['total_rounds']}")
    print(f"  Winner: {debate_result['winner']}")
    print(f"  Total Arguments: {len(debate_result['arguments'])}")


# ---------------------------------------------------------------------------
# 6. Message Passing Patterns
# ---------------------------------------------------------------------------

class Mailbox:
    """Mailbox for asynchronous message passing."""

    def __init__(self, owner_id: str, capacity: int = 100):
        self.owner_id = owner_id
        self.capacity = capacity
        self.messages: deque[AgentMessage] = deque(maxlen=capacity)
        self.lock = asyncio.Lock()

    async def send(self, message: AgentMessage):
        """Send a message to the mailbox."""
        async with self.lock:
            if len(self.messages) >= self.capacity:
                raise MailboxFullError(f"Mailbox for {self.owner_id} is full")
            self.messages.append(message)

    async def receive(self) -> AgentMessage | None:
        """Receive a message from the mailbox."""
        async with self.lock:
            if self.messages:
                return self.messages.popleft()
            return None

    async def peek(self) -> AgentMessage | None:
        """Peek at the next message without removing it."""
        async with self.lock:
            if self.messages:
                return self.messages[0]
            return None

    def size(self) -> int:
        """Get mailbox size."""
        return len(self.messages)


class MailboxFullError(Exception):
    """Raised when mailbox is full."""
    pass


class MessagePassingAgent(BaseAgent):
    """Agent that communicates via mailboxes."""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentRole.WORKER)
        self.mailbox = Mailbox(agent_id)
        self.mailboxes: dict[str, Mailbox] = {}  # Other agents' mailboxes

    def register_mailbox(self, agent_id: str, mailbox: Mailbox):
        """Register another agent's mailbox."""
        self.mailboxes[agent_id] = mailbox

    async def send_to(self, receiver_id: str, content: Any,
                     message_type: str = "task"):
        """Send a message to another agent's mailbox."""
        if receiver_id not in self.mailboxes:
            raise ValueError(f"No mailbox registered for {receiver_id}")

        message = AgentMessage(
            sender=self.agent_id,
            receiver=receiver_id,
            content=content,
            message_type=message_type,
        )
        await self.mailboxes[receiver_id].send(message)

    async def receive_from(self) -> AgentMessage | None:
        """Receive a message from own mailbox."""
        return await self.mailbox.receive()

    async def process_message(self, message: AgentMessage) -> AgentMessage | None:
        """Process a received message."""
        # Process based on type
        if message.message_type == "task":
            result = await self._handle_task(message.content)
            return self.send_message(
                message.sender,
                {"type": "result", "data": result},
                "result"
            )
        return None

    async def _handle_task(self, content: Any) -> Any:
        """Handle a task."""
        await asyncio.sleep(0.05)
        return f"Task completed by {self.agent_id}"


async def demo_message_passing():
    """Demonstrate message passing patterns."""
    print("\n" + "=" * 60)
    print("5. MESSAGE PASSING PATTERNS")
    print("=" * 60)

    # Create agents
    agent_a = MessagePassingAgent("agent_a")
    agent_b = MessagePassingAgent("agent_b")
    agent_c = MessagePassingAgent("agent_c")

    # Register mailboxes
    agent_a.register_mailbox("agent_b", agent_b.mailbox)
    agent_a.register_mailbox("agent_c", agent_c.mailbox)
    agent_b.register_mailbox("agent_a", agent_a.mailbox)
    agent_b.register_mailbox("agent_c", agent_c.mailbox)
    agent_c.register_mailbox("agent_a", agent_a.mailbox)
    agent_c.register_mailbox("agent_b", agent_b.mailbox)

    # Send messages
    await agent_a.send_to("agent_b", {"task": "Analyze data"})
    await agent_b.send_to("agent_c", {"task": "Generate report"})
    await agent_c.send_to("agent_a", {"task": "Validate results"})

    # Process messages
    print("\nMessage Flow:")

    # Agent A processes
    msg = await agent_a.receive_from()
    if msg:
        print(f"  {msg.sender} -> {msg.receiver}: {msg.message_type}")

    # Agent B processes
    msg = await agent_b.receive_from()
    if msg:
        print(f"  {msg.sender} -> {msg.receiver}: {msg.message_type}")

    # Agent C processes
    msg = await agent_c.receive_from()
    if msg:
        print(f"  {msg.sender} -> {msg.receiver}: {msg.message_type}")

    # Show mailbox states
    print(f"\nMailbox Sizes:")
    print(f"  Agent A: {agent_a.mailbox.size()}")
    print(f"  Agent B: {agent_b.mailbox.size()}")
    print(f"  Agent C: {agent_c.mailbox.size()}")


# ---------------------------------------------------------------------------
# Main: Run All Demos
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("EXERCISE 08: MULTI-AGENT SYSTEMS")
    print("=" * 60)

    demo_orchestrator_worker()
    demo_agent_communication()
    demo_sequential_vs_parallel()
    demo_consensus_patterns()
    asyncio.run(demo_message_passing())

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("1. Orchestrator-worker pattern enables task decomposition")
    print("2. Message buses enable loose coupling between agents")
    print("3. Parallel execution provides significant speedup")
    print("4. Consensus patterns enable reliable decision making")
    print("5. Message passing enables asynchronous agent coordination")
    print("=" * 60)
