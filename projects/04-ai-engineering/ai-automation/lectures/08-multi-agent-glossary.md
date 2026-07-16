# Glossary: Multi-Agent Systems

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Multi-Agent | System with multiple agents | Collaboration for complex tasks |
| Orchestrator | Central coordinator | Manages task delegation |
| Worker | Specialized agent | Executes specific tasks |
| Peer-to-Peer | Decentralized communication | Agents talk directly |
| Message Bus | Communication channel | Routes messages between agents |
| Task Decomposition | Breaking down tasks | Divide and conquer |
| Consensus | Agreement among agents | Collaborative decision |
| Parallel Execution | Simultaneous processing | Speed through concurrency |
| State Sharing | Shared memory/context | Information exchange |
| Agent Role | Specialized function | Defines agent capabilities |
| Synthesis | Combining results | Merging agent outputs |
| Orchestration | Coordinating agents | Managing the workflow |

---

## Detailed Definitions

### Multi-Agent

**Definition:** A system composed of multiple autonomous agents that interact and collaborate to accomplish tasks beyond individual capabilities.

**Example:**
```python
class MultiAgentSystem:
    def __init__(self):
        self.agents = {}
    
    def add_agent(self, name, agent):
        self.agents[name] = agent
    
    def execute(self, task):
        # Coordinate agents to complete task
        results = []
        for name, agent in self.agents.items():
            result = agent.execute(task)
            results.append(result)
        return self.synthesize(results)

# Create system
system = MultiAgentSystem()
system.add_agent("researcher", ResearchAgent())
system.add_agent("coder", CoderAgent())
system.add_agent("reviewer", ReviewAgent())

# Execute
result = system.execute("Build a web scraper")
```

**Related Terms:** Agent, Collaboration, Orchestration

**Benefits:**
- Specialization
- Parallel execution
- Fault tolerance
- Scalability

---

### Orchestrator

**Definition:** A central agent that coordinates other agents, managing task decomposition, delegation, and result synthesis.

**Example:**
```python
class Orchestrator:
    def __init__(self, workers):
        self.workers = workers
    
    def execute(self, task):
        # Decompose task
        subtasks = self.decompose(task)
        
        # Assign to workers
        assignments = self.assign(subtasks)
        
        # Collect results
        results = {}
        for assignment in assignments:
            worker = self.workers[assignment.worker]
            result = worker.execute(assignment.subtask)
            results[assignment.id] = result
        
        # Synthesize
        return self.synthesize(results)
    
    def decompose(self, task):
        # Break task into subtasks
        return [{"id": 1, "task": "research"}, 
                {"id": 2, "task": "implement"},
                {"id": 3, "task": "review"}]
```

**Related Terms:** Coordinator, Manager, Central

**Responsibilities:**
- Task decomposition
- Worker assignment
- Progress monitoring
- Result synthesis

---

### Worker

**Definition:** A specialized agent that performs specific tasks assigned by the orchestrator or other agents.

**Example:**
```python
class WorkerAgent:
    def __init__(self, specialization):
        self.specialization = specialization
    
    def execute(self, task):
        # Perform specialized work
        if self.specialization == "research":
            return self.research(task)
        elif self.specialization == "coding":
            return self.code(task)
        elif self.specialization == "review":
            return self.review(task)
    
    def research(self, task):
        # Search and analyze
        return f"Research results for: {task}"
```

**Related Terms:** Specialist, Executor, Processor

**Types:**
- Research workers
- Code workers
- Review workers
- Writing workers

---

### Peer-to-Peer

**Definition:** A decentralized communication pattern where agents communicate directly without a central coordinator.

**Example:**
```python
class PeerAgent:
    def __init__(self, name):
        self.name = name
        self.peers = {}
        self.inbox = []
    
    def register_peer(self, peer):
        self.peers[peer.name] = peer
    
    def send(self, to_name, message):
        if to_name in self.peers:
            self.peers[to_name].receive(self.name, message)
    
    def receive(self, from_name, message):
        self.inbox.append({"from": from_name, "message": message})
        return self.process(message)
    
    def process(self, message):
        # Process and potentially respond
        return f"Processed: {message}"
```

**Related Terms:** Decentralized, Direct, Distributed

**Benefits:**
- No single point of failure
- Flexible communication
- Scalable

---

### Message Bus

**Definition:** A central communication channel that routes messages between agents, decoupling sender and receiver.

**Example:**
```python
class MessageBus:
    def __init__(self):
        self.agents = {}
        self.message_log = []
    
    def register(self, agent):
        self.agents[agent.name] = agent
    
    def publish(self, message):
        self.message_log.append(message)
        
        # Route to recipient
        if message.receiver in self.agents:
            self.agents[message.receiver].on_message(message)
        elif message.receiver == "broadcast":
            for agent in self.agents.values():
                if agent.name != message.sender:
                    agent.on_message(message)
    
    def subscribe(self, agent_name, topic):
        # Subscribe agent to topic
        pass
```

**Related Terms:** Channel, Router, Pub/Sub

**Patterns:**
- Point-to-point
- Publish/Subscribe
- Request/Response

---

### Task Decomposition

**Definition:** Breaking complex tasks into smaller, manageable subtasks that can be assigned to different agents.

**Example:**
```python
def decompose_task(task):
    """Break task into subtasks."""
    
    subtasks = {
        "Build a web app": [
            {"id": 1, "task": "Design database schema", "agent": "architect"},
            {"id": 2, "task": "Build API endpoints", "agent": "backend"},
            {"id": 3, "task": "Create UI components", "agent": "frontend"},
            {"id": 4, "task": "Write tests", "agent": "tester"},
            {"id": 5, "task": "Review code", "agent": "reviewer"}
        ]
    }
    
    return subtasks.get(task, [])

# Usage
subtasks = decompose_task("Build a web app")
for st in subtasks:
    print(f"Assign to {st['agent']}: {st['task']}")
```

**Related Terms:** Decomposition, Breakdown, Partitioning

**Strategies:**
- By function
- By expertise
- By complexity
- By dependency

---

### Consensus

**Definition:** An agreement among multiple agents on a decision or conclusion, often through discussion or voting.

**Example:**
```python
class ConsensusSystem:
    def __init__(self, agents):
        self.agents = agents
    
    def vote(self, topic, options):
        """Collect votes from agents."""
        votes = {}
        
        for agent in self.agents:
            vote = agent.decide(topic, options)
            votes[agent.name] = vote
        
        # Count votes
        tally = {}
        for vote in votes.values():
            tally[vote] = tally.get(vote, 0) + 1
        
        # Find winner
        winner = max(tally, key=tally.get)
        return winner, tally
    
    def debate(self, topic, rounds=3):
        """Multi-round debate to reach consensus."""
        positions = {}
        
        for round_num in range(rounds):
            for agent in self.agents:
                position = agent.argue(topic, positions)
                positions[agent.name] = position
        
        return self.synthesize(positions)
```

**Related Terms:** Agreement, Decision, Voting

**Methods:**
- Voting
- Debate
- Delphi method
- Weighted consensus

---

### Parallel Execution

**Definition:** Running multiple agent tasks simultaneously to improve speed and efficiency.

**Example:**
```python
from concurrent.futures import ThreadPoolExecutor

def execute_parallel(agents, task):
    """Execute task across agents in parallel."""
    
    with ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = {
            executor.submit(agent.execute, task): agent.name
            for agent in agents
        }
        
        results = {}
        for future in futures:
            agent_name = futures[future]
            result = future.result()
            results[agent_name] = result
    
    return results

# Usage
agents = [ResearchAgent(), CoderAgent(), ReviewAgent()]
results = execute_parallel(agents, "Analyze this code")
```

**Related Terms:** Concurrency, Simultaneous, Asynchronous

**Benefits:**
- Faster execution
- Better resource utilization
- Improved throughput

---

### State Sharing

**Definition:** Exchanging information and context between agents to maintain coherent workflow.

**Example:**
```python
class SharedState:
    def __init__(self):
        self.data = {}
        self.lock = None  # For thread safety
    
    def get(self, key):
        return self.data.get(key)
    
    def set(self, key, value):
        self.data[key] = value
    
    def update(self, updates):
        self.data.update(updates)

class StateAwareAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state
    
    def execute(self, task):
        # Read from shared state
        context = self.shared_state.get("context")
        
        # Do work
        result = self.process(task, context)
        
        # Write to shared state
        self.shared_state.set("last_result", result)
        
        return result
```

**Related Terms:** Context, Memory, Synchronization

**Challenges:**
- Race conditions
- Consistency
- Scalability

---

### Agent Role

**Definition:** The specialized function or capability assigned to an agent in a multi-agent system.

**Example:**
```python
from enum import Enum

class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    RESEARCHER = "researcher"
    CODER = "coder"
    REVIEWER = "reviewer"
    WRITER = "writer"
    TESTER = "tester"

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.capabilities = self.get_capabilities()
    
    def get_capabilities(self):
        capabilities = {
            AgentRole.RESEARCHER: ["search", "analyze", "summarize"],
            AgentRole.CODER: ["python", "javascript", "debug"],
            AgentRole.REVIEWER: ["review", "feedback", "quality"],
        }
        return capabilities.get(self.role, [])
```

**Related Terms:** Specialization, Function, Responsibility

**Common Roles:**
- Orchestrator: Coordinates others
- Researcher: Gathers information
- Coder: Implements solutions
- Reviewer: Validates quality

---

### Synthesis

**Definition:** Combining outputs from multiple agents into a coherent final result.

**Example:**
```python
def synthesize_results(results):
    """Combine agent results into final output."""
    
    # Organize by agent
    research = results.get("researcher", "")
    code = results.get("coder", "")
    review = results.get("reviewer", "")
    
    # Build synthesis
    synthesis = f"""
## Research Findings
{research}

## Implementation
{code}

## Code Review
{review}

## Summary
Based on the research, implementation, and review above...
"""
    
    return synthesis

# Usage
results = {
    "researcher": "Found that we need X, Y, Z...",
    "coder": "Implemented using Python with...",
    "reviewer": "Code looks good, minor suggestions..."
}

final = synthesize_results(results)
```

**Related Terms:** Combination, Integration, Merging

**Techniques:**
- Concatenation
- Summarization
- Voting
- Weighted combination

---

### Orchestration

**Definition:** The process of coordinating multiple agents to work together effectively toward a common goal.

**Example:**
```python
class Orchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.workflow = []
    
    def define_workflow(self, steps):
        """Define execution workflow."""
        self.workflow = steps
    
    def execute(self, task):
        """Execute task following workflow."""
        
        context = {"task": task}
        
        for step in self.workflow:
            agent = self.agents[step["agent"]]
            result = agent.execute(
                step["task"],
                context=context
            )
            context[step["output_key"]] = result
        
        return context

# Usage
orchestrator = Orchestrator(agents)
orchestrator.define_workflow([
    {"agent": "researcher", "task": "Research topic", "output_key": "research"},
    {"agent": "coder", "task": "Implement solution", "output_key": "code"},
    {"agent": "reviewer", "task": "Review code", "output_key": "review"}
])

result = orchestrator.execute("Build a REST API")
```

**Related Terms:** Coordination, Management, Control

**Patterns:**
- Sequential
- Parallel
- Conditional
- Loop

---

### Workflow

**Definition:** A defined sequence of tasks and their execution order in a multi-agent system.

**Example:**
```python
workflow = {
    "name": "software_development",
    "steps": [
        {
            "id": 1,
            "name": "requirements",
            "agent": "analyst",
            "inputs": ["task"],
            "outputs": ["requirements"]
        },
        {
            "id": 2,
            "name": "design",
            "agent": "architect",
            "inputs": ["requirements"],
            "outputs": ["design"]
        },
        {
            "id": 3,
            "name": "implement",
            "agent": "coder",
            "inputs": ["design"],
            "outputs": ["code"],
            "parallel": True  # Can run in parallel with step 4
        },
        {
            "id": 4,
            "name": "test",
            "agent": "tester",
            "inputs": ["code"],
            "outputs": ["tests"]
        },
        {
            "id": 5,
            "name": "review",
            "agent": "reviewer",
            "inputs": ["code", "tests"],
            "outputs": ["review"]
        }
    ]
}
```

**Related Terms:** Pipeline, Process, Sequence

**Types:**
- Sequential workflow
- Parallel workflow
- Conditional workflow
- Dynamic workflow

---

### Handoff

**Definition:** Transferring control or responsibility from one agent to another during task execution.

**Example:**
```python
class AgentWithHandoff:
    def __init__(self, name):
        self.name = name
        self.next_agent = None
    
    def set_next(self, agent):
        self.next_agent = agent
    
    def execute(self, task, context):
        # Do my part
        result = self.do_work(task, context)
        context[f"{self.name}_result"] = result
        
        # Handoff to next agent
        if self.next_agent:
            return self.next_agent.execute(task, context)
        
        return result
    
    def do_work(self, task, context):
        return f"{self.name} completed: {task}"

# Chain agents
researcher = AgentWithHandoff("researcher")
coder = AgentWithHandoff("coder")
reviewer = AgentWithHandoff("reviewer")

researcher.set_next(coder)
coder.set_next(reviewer)

# Execute with handoff
result = researcher.execute("Build feature", {})
```

**Related Terms:** Transfer, Pass, Delegation

**When to Use:**
- Sequential processing
- Specialization chains
- Pipeline workflows

---

### Supervisor

**Definition:** An agent that monitors and controls other agents, ensuring proper execution and handling failures.

**Example:**
```python
class Supervisor:
    def __init__(self, workers):
        self.workers = workers
        self.status = {}
    
    def monitor(self):
        """Monitor worker status."""
        for name, worker in self.workers.items():
            self.status[name] = worker.get_status()
    
    def handle_failure(self, worker_name, error):
        """Handle worker failure."""
        print(f"Worker {worker_name} failed: {error}")
        
        # Retry or reassign
        worker = self.workers[worker_name]
        if worker.retries < 3:
            worker.retry()
        else:
            self.reassign_task(worker_name)
    
    def reassign_task(self, failed_worker):
        """Reassign task to another worker."""
        # Find available worker
        for name, worker in self.workers.items():
            if name != failed_worker and worker.is_available():
                return worker
    
    def get_report(self):
        """Get status report."""
        return {
            "workers": self.status,
            "completed": sum(1 for s in self.status.values() if s == "done"),
            "failed": sum(1 for s in self.status.values() if s == "failed")
        }
```

**Related Terms:** Monitor, Controller, Manager

**Responsibilities:**
- Monitor progress
- Handle failures
- Reallocate resources
- Report status

---

### Conflict Resolution

**Definition:** Mechanisms for resolving disagreements or conflicts between agents in a multi-agent system.

**Example:**
```python
class ConflictResolver:
    def __init__(self, agents):
        self.agents = agents
    
    def resolve_by_voting(self, conflict):
        """Resolve through voting."""
        votes = {}
        
        for agent in self.agents:
            position = agent.vote(conflict)
            votes[position] = votes.get(position, 0) + 1
        
        return max(votes, key=votes.get)
    
    def resolve_by_ranking(self, conflict):
        """Resolve by agent authority ranking."""
        rankings = {}
        
        for agent in self.agents:
            ranking = agent.rank_options(conflict.options)
            rankings[agent.name] = ranking
        
        # Weighted average based on authority
        # ...
    
    def resolve_by_negotiation(self, conflict, rounds=3):
        """Resolve through negotiation."""
        proposals = {}
        
        for round_num in range(rounds):
            for agent in self.agents:
                proposal = agent.negotiate(conflict, proposals)
                proposals[agent.name] = proposal
        
        return self.find_compromise(proposals)
```

**Related Terms:** Mediation, Negotiation, Voting

**Methods:**
- Voting
- Authority hierarchy
- Negotiation
- Compromise

---

## Summary

Understanding these terms is essential for building effective multi-agent systems:

1. **Multi-Agent:** Multiple agents collaborating
2. **Orchestrator:** Central coordinator
3. **Worker:** Specialized agent
4. **Peer-to-Peer:** Decentralized communication
5. **Message Bus:** Communication channel
6. **Task Decomposition:** Breaking down tasks
7. **Consensus:** Agreement among agents
8. **Parallel Execution:** Simultaneous processing
9. **State Sharing:** Information exchange
10. **Synthesis:** Combining results

**Next:** See Lecture 09 for AI safety.
