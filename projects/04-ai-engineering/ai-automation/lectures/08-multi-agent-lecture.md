# Lecture 08: Multi-Agent Systems

## Topic Overview

Multi-agent systems involve multiple AI agents working together to accomplish complex tasks. Instead of one agent doing everything, specialized agents collaborate, each handling different aspects of a problem. This lecture covers agent coordination patterns, communication protocols, task decomposition, and how to build effective multi-agent architectures.

**Duration:** 4-5 hours  
**Difficulty:** Advanced  
**Prerequisites:** Lecture 05 (AI Agents)

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Design** multi-agent architectures for complex tasks
2. **Implement** agent coordination and communication
3. **Build** orchestrator-worker patterns
4. **Create** agent teams with specialized roles
5. **Handle** inter-agent communication and state sharing
6. **Implement** parallel and sequential agent execution
7. **Debug** multi-agent systems
8. **Optimize** agent collaboration efficiency

---

## Key Concepts

### 1. Why Multi-Agent?

Single agent limitations:
- Context window limits
- Task complexity
- Specialization needs
- Parallel execution

```
Single Agent:
┌─────────────────────────────────────────┐
│  Agent 1                                │
│  - Understands task                     │
│  - Uses all tools                       │
│  - Handles everything                   │
│  - Limited by context window            │
└─────────────────────────────────────────┘

Multi-Agent:
┌─────────────────────────────────────────┐
│  Orchestrator                           │
│  ├─► Research Agent (search, analysis)  │
│  ├─► Code Agent (programming)           │
│  ├─► Review Agent (quality check)       │
│  └─► Writer Agent (documentation)       │
│                                         │
│  Each agent specialized, parallel work  │
└─────────────────────────────────────────┘
```

### 2. Multi-Agent Patterns

#### Orchestrator-Worker Pattern

```python
class Orchestrator:
    """Central coordinator for worker agents."""
    
    def __init__(self, workers: Dict[str, Agent]):
        self.workers = workers
        self.task_queue = []
        self.results = {}
    
    def execute(self, task: str) -> str:
        """Execute a task using worker agents."""
        
        # Step 1: Decompose task
        subtasks = self.decompose(task)
        
        # Step 2: Assign to workers
        assignments = self.assign(subtasks)
        
        # Step 3: Execute in parallel/sequential
        for assignment in assignments:
            worker = self.workers[assignment.worker_name]
            result = worker.execute(assignment.subtask)
            self.results[assignment.subtask_id] = result
        
        # Step 4: Synthesize results
        return self.synthesize(self.results)
    
    def decompose(self, task: str) -> List[Subtask]:
        """Break task into subtasks."""
        
        prompt = f"""Break this task into subtasks:

Task: {task}

Available workers: {list(self.workers.keys())}

Return a JSON list of subtasks:
[
    {{
        "id": "1",
        "description": "subtask description",
        "worker": "worker_name",
        "dependencies": []
    }}
]
"""
        
        response = self.llm.generate(prompt)
        return self.parse_subtasks(response)
    
    def assign(self, subtasks: List[Subtask]) -> List[Assignment]:
        """Assign subtasks to workers."""
        
        assignments = []
        for subtask in subtasks:
            assignments.append(Assignment(
                subtask_id=subtask.id,
                subtask=subtask.description,
                worker_name=subtask.worker
            ))
        
        return assignments
    
    def synthesize(self, results: Dict) -> str:
        """Combine results into final output."""
        
        results_text = "\n".join([
            f"Result {k}: {v}" for k, v in results.items()
        ])
        
        prompt = f"""Synthesize these results into a coherent response:

{results_text}

Provide a comprehensive final answer.
"""
        
        return self.llm.generate(prompt)
```

#### Peer-to-Peer Pattern

```python
class PeerAgent:
    """Agent that can communicate with other agents."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.peers = {}
        self.shared_memory = {}
    
    def register_peer(self, peer: 'PeerAgent'):
        """Register another agent as a peer."""
        self.peers[peer.name] = peer
    
    def send_message(self, to_agent: str, message: str):
        """Send a message to another agent."""
        if to_agent in self.peers:
            self.peers[to_agent].receive_message(self.name, message)
    
    def receive_message(self, from_agent: str, message: str):
        """Receive a message from another agent."""
        # Process message and potentially respond
        response = self.process_message(from_agent, message)
        if response:
            self.send_message(from_agent, response)
    
    def share_memory(self, key: str, value: Any):
        """Share information with all peers."""
        self.shared_memory[key] = value
        for peer in self.peers.values():
            peer.shared_memory[key] = value
```

#### Debate/Consensus Pattern

```python
class DebateSystem:
    """Multiple agents debate to reach consensus."""
    
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.rounds = []
    
    def debate(self, topic: str, rounds: int = 3) -> str:
        """Run a multi-round debate."""
        
        for round_num in range(rounds):
            round_responses = []
            
            # Each agent responds
            for agent in self.agents:
                context = self.build_context(round_num, round_responses)
                response = agent.generate(
                    f"Topic: {topic}\n\nContext: {context}\n\nYour position:"
                )
                round_responses.append({
                    "agent": agent.name,
                    "response": response
                })
            
            self.rounds.append(round_responses)
        
        # Final consensus
        return self.build_consensus()
    
    def build_context(self, round_num: int, responses: List[Dict]) -> str:
        """Build context from previous responses."""
        
        if round_num == 0:
            return "This is the first round of debate."
        
        context = "Previous responses:\n"
        for resp in responses:
            context += f"\n{resp['agent']}: {resp['response']}\n"
        
        return context
    
    def build_consensus(self) -> str:
        """Synthesize final consensus."""
        
        all_responses = []
        for round_responses in self.rounds:
            for resp in round_responses:
                all_responses.append(resp['response'])
        
        prompt = f"""Based on this debate, synthesize a consensus position:

{chr(10).join(all_responses)}

Provide a balanced conclusion that considers all perspectives.
"""
        
        return self.llm.generate(prompt)
```

### 3. Agent Communication

```python
from dataclasses import dataclass
from typing import Any, Dict, List
from enum import Enum
import json


class MessageType(Enum):
    """Types of messages between agents."""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    ERROR = "error"
    STATUS = "status"


@dataclass
class Message:
    """A message between agents."""
    sender: str
    receiver: str
    type: MessageType
    content: Any
    metadata: Dict = None
    reply_to: str = None


class MessageBus:
    """Central message bus for agent communication."""
    
    def __init__(self):
        self.agents: Dict[str, 'Agent'] = {}
        self.message_queue: List[Message] = []
        self.message_log: List[Message] = []
    
    def register_agent(self, agent: 'Agent'):
        """Register an agent with the message bus."""
        self.agents[agent.name] = agent
    
    def send(self, message: Message):
        """Send a message."""
        self.message_queue.append(message)
        self.message_log.append(message)
        
        # Deliver to receiver
        if message.receiver in self.agents:
            self.agents[message.receiver].on_message(message)
        elif message.receiver == "broadcast":
            for agent in self.agents.values():
                if agent.name != message.sender:
                    agent.on_message(message)
    
    def get_messages_for(self, agent_name: str) -> List[Message]:
        """Get all messages for an agent."""
        return [m for m in self.message_log if m.receiver == agent_name]


class CommunicatingAgent:
    """Agent with communication capabilities."""
    
    def __init__(self, name: str, message_bus: MessageBus):
        self.name = name
        self.message_bus = message_bus
        self.message_bus.register_agent(self)
        self.inbox: List[Message] = []
    
    def send(self, receiver: str, content: Any, msg_type: MessageType = MessageType.REQUEST):
        """Send a message to another agent."""
        message = Message(
            sender=self.name,
            receiver=receiver,
            type=msg_type,
            content=content
        )
        self.message_bus.send(message)
    
    def broadcast(self, content: Any):
        """Broadcast to all agents."""
        self.send("broadcast", content, MessageType.BROADCAST)
    
    def on_message(self, message: Message):
        """Handle incoming message."""
        self.inbox.append(message)
    
    def get_unread(self) -> List[Message]:
        """Get unread messages."""
        unread = self.inbox.copy()
        self.inbox.clear()
        return unread
```

### 4. Task Decomposition

```python
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Subtask:
    """A decomposed subtask."""
    id: str
    description: str
    required_capabilities: List[str]
    dependencies: List[str] = None
    estimated_complexity: int = 1  # 1-5
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class TaskDecomposer:
    """Decompose complex tasks into subtasks."""
    
    def __init__(self, llm):
        self.llm = llm
    
    def decompose(self, task: str, available_agents: List[str]) -> List[Subtask]:
        """Decompose task into subtasks."""
        
        prompt = f"""Decompose this task into subtasks for parallel execution.

Task: {task}

Available agents: {available_agents}

For each subtask, provide:
- id: unique identifier
- description: what needs to be done
- required_capabilities: skills needed
- dependencies: which subtasks must complete first
- estimated_complexity: 1-5

Return as JSON array.
"""
        
        response = self.llm.generate(prompt)
        return self.parse_subtasks(response)
    
    def optimize_order(self, subtasks: List[Subtask]) -> List[List[Subtask]]:
        """Optimize execution order considering dependencies."""
        
        # Build dependency graph
        graph = {st.id: st.dependencies for st in subtasks}
        
        # Topological sort
        execution_layers = []
        remaining = subtasks.copy()
        
        while remaining:
            # Find tasks with no unmet dependencies
            ready = [
                st for st in remaining
                if all(dep in [s.id for layer in execution_layers for s in layer] 
                       for dep in st.dependencies)
            ]
            
            if not ready:
                # Circular dependency - break it
                ready = [remaining[0]]
            
            execution_layers.append(ready)
            remaining = [st for st in remaining if st not in ready]
        
        return execution_layers
```

---

## Code Examples

### Example 1: Complete Multi-Agent Framework

```python
"""
Production multi-agent system framework.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
from openai import OpenAI
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json


class AgentRole(Enum):
    """Roles agents can play."""
    ORCHESTRATOR = "orchestrator"
    RESEARCHER = "researcher"
    CODER = "coder"
    REVIEWER = "reviewer"
    WRITER = "writer"
    ANALYZER = "analyzer"


@dataclass
class AgentCapability:
    """A capability an agent has."""
    name: str
    description: str
    tools: List[str] = field(default_factory=list)


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: AgentRole
    capabilities: List[AgentCapability]
    model: str = "gpt-4"
    max_iterations: int = 10


class MultiAgent:
    """An agent in a multi-agent system."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = OpenAI()
        self.memory = []
        self.peers = {}
    
    def think(self, task: str, context: str = "") -> str:
        """Reason about what to do."""
        
        prompt = f"""You are {self.config.name}, a {self.config.role.value}.

Your capabilities: {[c.name for c in self.config.capabilities]}

Task: {task}
Context: {context}

What should you do next? Provide your reasoning and plan.
"""
        
        return self._call_llm(prompt)
    
    def act(self, action: str, tools: Dict[str, Callable] = None) -> str:
        """Execute an action."""
        
        if tools and action in tools:
            return tools[action]()
        
        # Generate response
        prompt = f"""Execute this action:

{action}

Provide the result of this action.
"""
        
        return self._call_llm(prompt)
    
    def communicate(self, to_agent: str, message: str) -> str:
        """Send message to another agent."""
        
        if to_agent in self.peers:
            return self.peers[to_agent].receive(message)
        
        return f"Agent {to_agent} not found"
    
    def receive(self, message: str) -> str:
        """Receive and process a message."""
        
        self.memory.append({"type": "incoming", "content": message})
        
        prompt = f"""Process this message from a peer agent:

{message}

Provide your response.
"""
        
        response = self._call_llm(prompt)
        self.memory.append({"type": "outgoing", "content": response})
        
        return response
    
    def _call_llm(self, prompt: str) -> str:
        """Call the LLM."""
        
        messages = [
            {"role": "system", "content": f"You are {self.config.name}."},
            {"role": "user", "content": prompt}
        ]
        
        # Add memory context
        if self.memory:
            memory_context = "\n".join([
                f"[{m['type']}] {m['content'][:200]}"
                for m in self.memory[-5:]
            ])
            messages.append({
                "role": "user",
                "content": f"Recent context:\n{memory_context}"
            })
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=0.3
        )
        
        return response.choices[0].message.content


class MultiAgentSystem:
    """Orchestrate multiple agents."""
    
    def __init__(self):
        self.agents: Dict[str, MultiAgent] = {}
        self.task_results = {}
    
    def add_agent(self, agent: MultiAgent):
        """Add an agent to the system."""
        self.agents[agent.name] = agent
    
    def setup_communication(self):
        """Setup peer communication."""
        for agent in self.agents.values():
            for peer_name, peer_agent in self.agents.items():
                if peer_name != agent.name:
                    agent.peers[peer_name] = peer_agent
    
    def execute(self, task: str, strategy: str = "sequential") -> str:
        """Execute a task using agents."""
        
        if strategy == "sequential":
            return self._execute_sequential(task)
        elif strategy == "parallel":
            return self._execute_parallel(task)
        elif strategy == "orchestrated":
            return self._execute_orchestrated(task)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _execute_sequential(self, task: str) -> str:
        """Execute task sequentially through agents."""
        
        current_input = task
        results = []
        
        for agent_name, agent in self.agents.items():
            result = agent.think(current_input)
            action_result = agent.act(result)
            results.append({
                "agent": agent_name,
                "thought": result,
                "result": action_result
            })
            current_input = action_result
        
        return self._synthesize(results)
    
    def _execute_parallel(self, task: str) -> str:
        """Execute task in parallel across agents."""
        
        with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
            futures = {
                executor.submit(agent.think, task): agent.name
                for agent in self.agents.values()
            }
            
            results = []
            for future in futures:
                agent_name = futures[future]
                thought = future.result()
                agent = self.agents[agent_name]
                result = agent.act(thought)
                results.append({
                    "agent": agent_name,
                    "thought": thought,
                    "result": result
                })
        
        return self._synthesize(results)
    
    def _execute_orchestrated(self, task: str) -> str:
        """Orchestrator decomposes and coordinates."""
        
        # Find orchestrator
        orchestrator = next(
            (a for a in self.agents.values() 
             if a.config.role == AgentRole.ORCHESTRATOR),
            None
        )
        
        if not orchestrator:
            raise ValueError("No orchestrator agent found")
        
        # Decompose task
        decomposition = orchestrator.think(
            f"Decpose this task for your team:\n{task}\n\n"
            f"Team: {list(self.agents.keys())}"
        )
        
        # Execute subtasks
        results = []
        worker_agents = [a for a in self.agents.values() 
                        if a.config.role != AgentRole.ORCHESTRATOR]
        
        for worker in worker_agents:
            subtask_result = worker.think(decomposition)
            result = worker.act(subtask_result)
            results.append({
                "agent": worker.name,
                "thought": subtask_result,
                "result": result
            })
        
        # Orchestrator synthesizes
        synthesis = orchestrator.think(
            f"Synthesize these team results:\n"
            f"{json.dumps(results, indent=2)}"
        )
        
        return synthesis
    
    def _synthesize(self, results: List[Dict]) -> str:
        """Synthesize results from all agents."""
        
        results_text = "\n".join([
            f"Agent {r['agent']}:\n{r['result']}"
            for r in results
        ])
        
        # Use first agent to synthesize
        synthesizer = list(self.agents.values())[0]
        
        return synthesizer.think(
            f"Synthesize these results into a final answer:\n{results_text}"
        )


# Usage example
def create_software_team():
    """Create a multi-agent software development team."""
    
    system = MultiAgentSystem()
    
    # Add agents
    system.add_agent(MultiAgent(AgentConfig(
        name="architect",
        role=AgentRole.ORCHESTRATOR,
        capabilities=[
            AgentCapability("system_design", "Design system architecture"),
            AgentCapability("task_decomposition", "Break down tasks")
        ]
    )))
    
    system.add_agent(MultiAgent(AgentConfig(
        name="backend_dev",
        role=AgentRole.CODER,
        capabilities=[
            AgentCapability("python", "Write Python code"),
            AgentCapability("api", "Design APIs")
        ]
    )))
    
    system.add_agent(MultiAgent(AgentConfig(
        name="frontend_dev",
        role=AgentRole.CODER,
        capabilities=[
            AgentCapability("javascript", "Write JavaScript"),
            AgentCapability("react", "Build React UIs")
        ]
    )))
    
    system.add_agent(MultiAgent(AgentConfig(
        name="reviewer",
        role=AgentRole.REVIEWER,
        capabilities=[
            AgentCapability("code_review", "Review code quality"),
            AgentCapability("testing", "Write tests")
        ]
    )))
    
    # Setup communication
    system.setup_communication()
    
    return system


# Run
team = create_software_team()
result = team.execute(
    "Build a REST API for a todo application with user authentication",
    strategy="orchestrated"
)
print(result)
```

---

## Common Mistakes to Avoid

### 1. No Clear Roles
```python
# ❌ BAD: All agents same role
agents = [Agent("agent1"), Agent("agent2"), Agent("agent3")]

# ✅ GOOD: Specialized roles
agents = [
    Agent(role="researcher", capabilities=["search", "analysis"]),
    Agent(role="coder", capabilities=["python", "testing"]),
    Agent(role="reviewer", capabilities=["code_review", "quality"])
]
```

### 2. No Communication Protocol
```python
# ❌ BAD: Agents can't communicate
agent1.do_work()
agent2.do_work()

# ✅ GOOD: Structured communication
agent1.send_message(agent2, "Here's my output: ...")
response = agent2.receive_and_process()
```

---

## Best Practices

1. **Clear roles** - Each agent should have a specific purpose
2. **Communication protocols** - Define how agents interact
3. **Error handling** - Agents can fail; handle gracefully
4. **State management** - Share necessary context
5. **Monitoring** - Track agent interactions
6. **Testing** - Test agents individually and together
7. **Fallbacks** - What if an agent fails?
8. **Cost control** - Parallel agents = more API calls

---

## Practice Exercises

### Exercise 1: Research Team
Build a team that:
1. Researches a topic (multiple sources)
2. Analyzes findings
3. Writes a summary
4. Reviews for accuracy

### Exercise 2: Code Review System
Create agents that:
1. Write code
2. Review code
3. Suggest improvements
4. Iterate until approved

### Exercise 3: Debate System
Build a system where:
1. Multiple agents argue positions
2. They respond to each other
3. A judge determines the winner

### Exercise 4: Pipeline System
Create a data pipeline with agents:
1. Data collector
2. Data processor
3. Analyzer
4. Reporter

### Exercise 5: Collaborative Writer
Build a team that:
1. Outlines a document
2. Each agent writes a section
3. Agents review each other's work
4. Final editing and polish

---

## Summary

Multi-agent systems enable complex task completion through specialization and collaboration:

1. **Patterns** - Orchestrator, Peer-to-Peer, Debate
2. **Communication** - Message passing, shared state
3. **Decomposition** - Breaking tasks into subtasks
4. **Coordination** - Parallel and sequential execution
5. **Synthesis** - Combining agent outputs

**Key Success Factors:**
- Clear agent roles
- Effective communication
- Proper task decomposition
- Error handling
- Cost management

**Next lecture:** AI Safety - Building responsible AI systems.
