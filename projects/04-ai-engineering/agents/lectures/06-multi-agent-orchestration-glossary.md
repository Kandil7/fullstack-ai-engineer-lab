# Glossary: Multi-Agent Orchestration

> Terms defined in alphabetical order.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Agent | Autonomous entity performing specific tasks | Worker, Specialist |
| Communication | Information exchange between agents | Message Passing |
| Coordination | Managing agent interactions | Orchestration |
| Delegation | Assigning tasks to appropriate agents | Assignment |
| Hierarchy | Organizational structure of agents | Manager, Worker |
| Message Bus | System for routing messages between agents | Communication |
| Orchestration | Coordinating multiple agents | Coordination |
| Pipeline | Sequential chain of agent tasks | Workflow |
| Registry | Directory of available agents | Discovery |
| Role | Specialized function of an agent | Specialization |
| Shared Memory | Common storage for agent collaboration | Memory |
| Specialization | Focusing agents on specific tasks | Role |
| Task | Unit of work assigned to an agent | Job, Assignment |
| Worker | Agent that executes specific tasks | Executor |

---

## A

### Agent

**Definition:** An autonomous entity that performs specific tasks within a multi-agent system. Each agent typically has a specialized role and capabilities.

**Example:**
```python
class Agent:
    def __init__(self, name: str, role: str, capabilities: list):
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.task_queue = []
    
    def can_handle(self, task_type: str) -> bool:
        """Check if agent can handle this task type."""
        return task_type in self.capabilities
    
    def execute(self, task: dict) -> dict:
        """Execute an assigned task."""
        return {"agent": self.name, "result": "completed"}

# Usage
researcher = Agent("researcher", "research", ["search", "analyze"])
writer = Agent("writer", "writing", ["draft", "edit"])
```

**Related terms:** Worker, Specialist, Executor

---

## C

### Communication

**Definition:** The exchange of information between agents in a multi-agent system. Communication can be synchronous (request-response) or asynchronous (message passing).

**Example:**
```python
from dataclasses import dataclass
from typing import Any
import time

@dataclass
class Message:
    sender: str
    receiver: str
    content: Any
    timestamp: float
    message_type: str = "task"

class CommunicationChannel:
    """Handles message passing between agents."""
    
    def __init__(self):
        self.messages = []
        self.queues = {}  # agent_name -> [messages]
    
    def send(self, message: Message):
        """Send a message to an agent's queue."""
        self.messages.append(message)
        
        if message.receiver not in self.queues:
            self.queues[message.receiver] = []
        self.queues[message.receiver].append(message)
    
    def receive(self, agent_name: str) -> list:
        """Get all messages for an agent."""
        return self.queues.get(agent_name, [])
    
    def broadcast(self, sender: str, content: Any):
        """Send message to all agents except sender."""
        for agent in self.queues:
            if agent != sender:
                self.send(Message(
                    sender=sender,
                    receiver=agent,
                    content=content,
                    timestamp=time.time(),
                    message_type="broadcast"
                ))

# Usage
channel = CommunicationChannel()
channel.send(Message("manager", "worker1", {"task": "research"}, time.time()))
messages = channel.receive("worker1")
```

**Related terms:** Message Passing, Message Bus

---

## D

### Delegation

**Definition:** The process of assigning tasks from one agent (typically a manager) to other agents (workers) based on their capabilities and availability.

**Example:**
```python
class DelegationSystem:
    """Manages task delegation to agents."""
    
    def __init__(self):
        self.agents = {}
        self.task_assignments = {}
    
    def register_agent(self, name: str, capabilities: list):
        """Register an agent with its capabilities."""
        self.agents[name] = {
            "capabilities": capabilities,
            "current_load": 0,
            "max_load": 5
        }
    
    def delegate(self, task: dict) -> str:
        """Delegate task to best available agent."""
        task_type = task.get("type", "general")
        
        # Find agents that can handle this task
        capable = [
            name for name, info in self.agents.items()
            if task_type in info["capabilities"] 
            and info["current_load"] < info["max_load"]
        ]
        
        if not capable:
            return None
        
        # Select agent with lowest load
        best_agent = min(capable, key=lambda a: self.agents[a]["current_load"])
        self.agents[best_agent]["current_load"] += 1
        self.task_assignments[task.get("id")] = best_agent
        
        return best_agent

# Usage
delegation = DelegationSystem()
delegation.register_agent("researcher", ["research", "analysis"])
delegation.register_agent("writer", ["writing", "editing"])

agent = delegation.delegate({"id": "task1", "type": "research"})
print(f"Task delegated to: {agent}")
```

**Related terms:** Assignment, Task Distribution

---

## H

### Hierarchy

**Definition:** An organizational structure where agents are arranged in levels, typically with managers at higher levels delegating to workers at lower levels.

**Example:**
```python
from typing import List, Optional

class HierarchicalAgent:
    """Agent that can manage other agents."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.subordinates: List[HierarchicalAgent] = []
        self.parent: Optional[HierarchicalAgent] = None
    
    def add_subordinate(self, agent: "HierarchicalAgent"):
        """Add a subordinate agent."""
        agent.parent = self
        self.subordinates.append(agent)
    
    def delegate_to_subordinates(self, task: dict) -> dict:
        """Delegate task to appropriate subordinate."""
        results = {}
        
        for sub in self.subordinates:
            if self._can_subordinate_handle(sub, task):
                results[sub.name] = sub.execute(task)
        
        return results
    
    def _can_subordinate_handle(self, subordinate, task) -> bool:
        """Check if subordinate can handle the task."""
        # Simple capability matching
        return True
    
    def execute(self, task: dict) -> dict:
        """Execute task, delegating if needed."""
        if self.subordinates:
            return self.delegate_to_subordinates(task)
        return {"agent": self.name, "result": "executed"}
    
    def get_hierarchy(self, depth: int = 0) -> str:
        """Visualize the hierarchy."""
        result = "  " * depth + f"- {self.name} ({self.role})\n"
        for sub in self.subordinates:
            result += sub.get_hierarchy(depth + 1)
        return result

# Build hierarchy
ceo = HierarchicalAgent("CEO", "executive")
cto = HierarchicalAgent("CTO", "technical")
dev1 = HierarchicalAgent("Dev1", "developer")
dev2 = HierarchicalAgent("Dev2", "developer")

cto.add_subordinate(dev1)
cto.add_subordinate(dev2)
ceo.add_subordinate(cto)

print(ceo.get_hierarchy())
# - CEO (executive)
#   - CTO (technical)
#     - Dev1 (developer)
#     - Dev2 (developer)
```

**Related terms:** Manager, Worker, Reporting Structure

---

## M

### Message Bus

**Definition:** A communication infrastructure that routes messages between agents. Decouples agents from each other, allowing flexible communication patterns.

**Example:**
```python
from typing import Callable, Dict, List
from collections import defaultdict
import time

class MessageBus:
    """Publish-subscribe message bus for agent communication."""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.message_log = []
    
    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to a topic."""
        self.subscribers[topic].append(handler)
    
    def publish(self, topic: str, message: dict):
        """Publish a message to a topic."""
        self.message_log.append({
            "topic": topic,
            "message": message,
            "timestamp": time.time()
        })
        
        for handler in self.subscribers.get(topic, []):
            handler(message)
    
    def unsubscribe(self, topic: str, handler: Callable):
        """Unsubscribe from a topic."""
        if handler in self.subscribers[topic]:
            self.subscribers[topic].remove(handler)

# Usage
bus = MessageBus()

def handle_task_assigned(message):
    print(f"Task assigned: {message}")

def handle_task_completed(message):
    print(f"Task completed: {message}")

bus.subscribe("task.assigned", handle_task_assigned)
bus.subscribe("task.completed", handle_task_completed)

bus.publish("task.assigned", {"task_id": "123", "agent": "worker1"})
```

**Related terms:** Pub-Sub, Event System, Communication

---

## O

### Orchestration

**Definition:** The coordination and management of multiple agents to achieve a common goal. Orchestration determines which agents work on what, in what order, and how they share results.

**Example:**
```python
from typing import List, Dict
from enum import Enum

class OrchestrationPattern(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"

class Orchestrator:
    """Manages execution of multiple agents."""
    
    def __init__(self, pattern: OrchestrationPattern):
        self.pattern = pattern
        self.agents = {}
        self.execution_history = []
    
    def register_agent(self, name: str, agent):
        """Register an agent."""
        self.agents[name] = agent
    
    def execute(self, tasks: List[Dict]) -> List[Dict]:
        """Execute tasks according to the orchestration pattern."""
        if self.pattern == OrchestrationPattern.SEQUENTIAL:
            return self._execute_sequential(tasks)
        elif self.pattern == OrchestrationPattern.PARALLEL:
            return self._execute_parallel(tasks)
        elif self.pattern == OrchestrationPattern.HIERARCHICAL:
            return self._execute_hierarchical(tasks)
    
    def _execute_sequential(self, tasks: List[Dict]) -> List[Dict]:
        """Execute tasks one after another."""
        results = []
        for task in tasks:
            agent_name = task["agent"]
            agent = self.agents[agent_name]
            result = agent.execute(task)
            results.append(result)
            self.execution_history.append({
                "task": task, "result": result, "pattern": "sequential"
            })
        return results
    
    def _execute_parallel(self, tasks: List[Dict]) -> List[Dict]:
        """Execute tasks simultaneously."""
        from concurrent.futures import ThreadPoolExecutor
        
        results = []
        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            futures = []
            for task in tasks:
                agent_name = task["agent"]
                agent = self.agents[agent_name]
                futures.append(executor.submit(agent.execute, task))
            
            for future in futures:
                results.append(future.result())
        return results
    
    def _execute_hierarchical(self, tasks: List[Dict]) -> List[Dict]:
        """Execute with manager-worker pattern."""
        # Find manager agent
        manager = self.agents.get("manager")
        if manager:
            return manager.execute({"subtasks": tasks})
        return self._execute_sequential(tasks)

# Usage
orchestrator = Orchestrator(OrchestrationPattern.SEQUENTIAL)
orchestrator.register_agent("researcher", researcher_agent)
orchestrator.register_agent("writer", writer_agent)

results = orchestrator.execute([
    {"agent": "researcher", "task": "research AI"},
    {"agent": "writer", "task": "write article"}
])
```

**Related terms:** Coordination, Management, Workflow

---

## P

### Pipeline

**Definition:** A sequential chain of agents where each agent's output becomes the next agent's input. Pipelines are common for linear workflows like research → write → review.

**Example:**
```python
from typing import List, Callable, Any

class Pipeline:
    """Sequential chain of processing steps."""
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[dict] = []
        self.results = []
    
    def add_step(self, name: str, processor: Callable, 
                config: dict = None):
        """Add a processing step."""
        self.steps.append({
            "name": name,
            "processor": processor,
            "config": config or {}
        })
        return self
    
    def execute(self, initial_input: Any) -> Any:
        """Execute the pipeline."""
        current_input = initial_input
        self.results = []
        
        for step in self.steps:
            print(f"Executing: {step['name']}")
            
            result = step["processor"](current_input, step["config"])
            self.results.append({
                "step": step["name"],
                "input": str(current_input)[:100],
                "output": str(result)[:100]
            })
            
            current_input = result
        
        return current_input

# Usage
def research_processor(input_data, config):
    return f"Research results for: {input_data}"

def writing_processor(input_data, config):
    return f"Article based on: {input_data}"

def review_processor(input_data, config):
    return f"Review of: {input_data}"

pipeline = Pipeline("content-creation")
pipeline.add_step("research", research_processor)
pipeline.add_step("writing", writing_processor)
pipeline.add_step("review", review_processor)

result = pipeline.execute("AI agents in 2024")
print(f"Final output: {result}")
```

**Related terms:** Workflow, Sequential, Chain

---

## R

### Role

**Definition:** The specialized function or responsibility assigned to an agent in a multi-agent system. Clear roles help agents focus on specific capabilities.

**Example:**
```python
from dataclasses import dataclass
from typing import List

@dataclass
class AgentRole:
    name: str
    description: str
    capabilities: List[str]
    responsibilities: List[str]

# Define common roles
RESEARCHER = AgentRole(
    name="Researcher",
    description="Gathers and analyzes information",
    capabilities=["search", "analyze", "summarize"],
    responsibilities=[
        "Find relevant information",
        "Verify facts",
        "Provide sources"
    ]
)

WRITER = AgentRole(
    name="Writer",
    description="Creates written content",
    capabilities=["draft", "edit", "format"],
    responsibilities=[
        "Write clear content",
        "Follow style guidelines",
        "Meet word count targets"
    ]
)

REVIEWER = AgentRole(
    name="Reviewer",
    description="Reviews and provides feedback",
    capabilities=["review", "critique", "score"],
    responsibilities=[
        "Check accuracy",
        "Provide constructive feedback",
        "Determine quality"
    ]
)

class RoleBasedAgent:
    def __init__(self, role: AgentRole):
        self.role = role
    
    def can_perform(self, capability: str) -> bool:
        return capability in self.role.capabilities

# Usage
agent = RoleBasedAgent(RESEARCHER)
print(f"Can search: {agent.can_perform('search')}")  # True
print(f"Can write: {agent.can_perform('write')}")  # False
```

**Related terms:** Specialization, Responsibility, Capability

---

## S

### Shared Memory

**Definition:** Common storage accessible by multiple agents for sharing information and coordinating state. Enables agents to collaborate without direct communication.

**Example:**
```python
import threading
from typing import Any, Dict
import time

class SharedMemory:
    """Thread-safe shared memory for agents."""
    
    def __init__(self):
        self._memory: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._readers = {}
    
    def write(self, key: str, value: Any, agent_name: str):
        """Write to shared memory."""
        with self._lock:
            self._memory[key] = {
                "value": value,
                "writer": agent_name,
                "timestamp": time.time()
            }
    
    def read(self, key: str) -> Any:
        """Read from shared memory."""
        with self._lock:
            if key in self._memory:
                return self._memory[key]["value"]
            return None
    
    def read_all(self) -> Dict[str, Any]:
        """Read all values."""
        with self._lock:
            return {k: v["value"] for k, v in self._memory.items()}
    
    def delete(self, key: str):
        """Delete from shared memory."""
        with self._lock:
            if key in self._memory:
                del self._memory[key]

# Usage
shared = SharedMemory()

# Agent 1 writes research
shared.write("research_results", {"facts": ["AI agents are..."]}, "researcher")

# Agent 2 reads research
research = shared.read("research_results")

# Agent 2 writes article based on research
shared.write("article_draft", "AI agents are...", "writer")
```

**Related terms:** Memory, State, Collaboration

---

### Specialization

**Definition:** The process of assigning specific capabilities or focus areas to agents. Specialized agents become experts in their domain, improving overall system performance.

**Example:**
```python
class SpecializedAgent:
    """Agent with specific domain expertise."""
    
    def __init__(self, name: str, domain: str, skills: list):
        self.name = name
        self.domain = domain
        self.skills = skills
        self.expertise_level = 0.5  # Improves with experience
    
    def assess_task(self, task: dict) -> float:
        """Assess how well agent can handle task (0-1)."""
        task_type = task.get("type", "")
        
        if task_type in self.skills:
            return 0.8 + (self.expertise_level * 0.2)
        return 0.1
    
    def learn_from_task(self, task: dict, result: dict):
        """Improve expertise from task completion."""
        if result.get("success", False):
            self.expertise_level = min(1.0, self.expertise_level + 0.05)

# Create specialized agents
code_agent = SpecializedAgent("CodeBot", "programming", 
                             ["python", "javascript", "debugging"])
research_agent = SpecializedAgent("ResearchBot", "research",
                                 ["search", "analysis", "citation"])

# Assess tasks
coding_task = {"type": "python", "description": "Write a function"}
research_task = {"type": "search", "description": "Find papers on AI"}

print(f"CodeBot for coding: {code_agent.assess_task(coding_task):.2f}")
print(f"CodeBot for research: {code_agent.assess_task(research_task):.2f}")
```

**Related terms:** Expertise, Domain, Capability

---

## Quick Reference: Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                 Orchestration Patterns                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SEQUENTIAL                                                 │
│  A ──► B ──► C ──► D                                        │
│                                                             │
│  PARALLEL                                                   │
│       ┌──► A ──┐                                           │
│  Start ──► B ──┼──► End                                    │
│       └──► C ──┘                                           │
│                                                             │
│  HIERARCHICAL                                               │
│           Manager                                           │
│          /   |   \                                          │
│         A    B    C                                         │
│        / \       |                                          │
│       D   E      F                                          │
│                                                             │
│  PIPELINE                                                   │
│  [Research] → [Write] → [Review] → [Publish]               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 06](./06-multi-agent-orchestration-lecture.md)** | **[Next: Lecture 07 →](./07-agent-communication-glossary.md)**
