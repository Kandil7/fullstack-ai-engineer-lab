# Lecture 06: Multi-Agent Orchestration

## 🎯 Topic Overview

**Multi-agent orchestration** is the coordination of multiple AI agents working together to solve complex problems. Instead of one agent doing everything, specialized agents collaborate, each handling specific aspects of a task.

This lecture covers:
- Why use multiple agents
- Orchestration patterns (sequential, parallel, hierarchical)
- Agent communication protocols
- Task delegation and specialization
- Building multi-agent systems in Python

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** the benefits of multi-agent systems over single agents
2. **Implement** different orchestration patterns
3. **Design** agent roles and specializations
4. **Build** communication systems between agents
5. **Handle** agent failures and coordination issues
6. **Optimize** multi-agent workflows
7. **Debug** multi-agent systems
8. **Evaluate** when multi-agent is appropriate

---

## 🧩 Key Concepts

### 1. Why Multiple Agents?

```
┌─────────────────────────────────────────────────────────────┐
│              Single Agent vs. Multi-Agent                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SINGLE AGENT                  MULTI-AGENT                  │
│  ┌─────────────────┐          ┌─────────────────┐          │
│  │                 │          │   Researcher    │          │
│  │  One Agent      │          │   ┌─────────┐  │          │
│  │  (Does          │    vs.   │   └────┬────┘  │          │
│  │   Everything)   │          │        │       │          │
│  │                 │          │   ┌────▼────┐  │          │
│  │                 │          │   │ Planner │  │          │
│  │                 │          │   └────┬────┘  │          │
│  └─────────────────┘          │        │       │          │
│                               │   ┌────▼────┐  │          │
│  Pros:                        │   │ Coder   │  │          │
│  - Simple                     │   └─────────┘  │          │
│  - No coordination            └─────────────────┘          │
│                                                             │
│                               Pros:                        │
│                               - Specialization              │
│                               - Parallel work               │
│                               - Better at complex tasks     │
└─────────────────────────────────────────────────────────────┘
```

### 2. Orchestration Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| **Sequential** | Agents work one after another | Linear workflows |
| **Parallel** | Agents work simultaneously | Independent tasks |
| **Hierarchical** | Manager delegates to workers | Complex projects |
| **Collaborative** | Agents discuss and reach consensus | Creative tasks |
| **Competitive** | Multiple agents race to solution | Optimization |

### 3. Multi-Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Multi-Agent System                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Orchestrator / Manager                  │   │
│  │  • Assigns tasks                                    │   │
│  │  • Coordinates agents                               │   │
│  │  • Aggregates results                               │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐              │
│         │                 │                 │              │
│         ▼                 ▼                 ▼              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│  │  Agent A    │   │  Agent B    │   │  Agent C    │      │
│  │  (Research) │   │  (Writing)  │   │  (Review)   │      │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘      │
│         │                 │                 │              │
│         └─────────────────┼─────────────────┘              │
│                           ▼                                 │
│                  ┌─────────────────┐                        │
│                  │  Shared Memory  │                        │
│                  │  / Message Bus  │                        │
│                  └─────────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Examples

### Example 1: Complete Multi-Agent System

```python
"""
Multi-Agent Orchestration System
Demonstrates sequential, parallel, and hierarchical patterns.
"""
import json
import time
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid


class AgentRole(Enum):
    """Different agent specializations."""
    RESEARCHER = "researcher"
    WRITER = "writer"
    REVIEWER = "reviewer"
    CODER = "coder"
    PLANNER = "planner"
    MANAGER = "manager"


@dataclass
class Message:
    """Message between agents."""
    id: str
    sender: str
    receiver: str
    content: Any
    timestamp: float
    message_type: str = "task"  # task, result, feedback
    
    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "timestamp": self.timestamp,
            "type": self.message_type
        }


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: AgentRole
    tools: List[str] = field(default_factory=list)
    max_iterations: int = 10
    model: str = "gpt-4"


class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, config: AgentConfig, llm_caller: Callable):
        self.config = config
        self.llm = llm_caller
        self.name = config.name
        self.role = config.role
        self.inbox: List[Message] = []
        self.outbox: List[Message] = []
        self.memory: List[Dict] = []
    
    def receive_message(self, message: Message):
        """Receive a message from another agent."""
        self.inbox.append(message)
    
    def send_message(self, receiver: str, content: Any, 
                    msg_type: str = "task"):
        """Send a message to another agent."""
        msg = Message(
            id=str(uuid.uuid4()),
            sender=self.name,
            receiver=receiver,
            content=content,
            timestamp=time.time(),
            message_type=msg_type
        )
        self.outbox.append(msg)
        return msg
    
    def process_task(self, task: Dict) -> Dict:
        """Process a task - to be overridden by subclasses."""
        raise NotImplementedError
    
    def get_system_prompt(self) -> str:
        """Get role-specific system prompt."""
        return f"You are {self.name}, a {self.role.value} agent."


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering."""
    
    def process_task(self, task: Dict) -> Dict:
        """Research a topic and return findings."""
        topic = task.get("topic", task.get("description", ""))
        
        prompt = f"""Research the following topic thoroughly:
Topic: {topic}

Provide:
1. Key facts and information
2. Relevant data points
3. Sources and references
4. Confidence level in findings

Return as JSON:
{{
    "findings": [...],
    "sources": [...],
    "confidence": 0.0-1.0,
    "summary": "brief summary"
}}
"""
        
        response = self.llm(prompt)
        
        try:
            findings = json.loads(response)
        except:
            findings = {
                "findings": [response],
                "sources": [],
                "confidence": 0.5,
                "summary": response[:200]
            }
        
        # Store in memory
        self.memory.append({
            "task": task,
            "result": findings,
            "timestamp": time.time()
        })
        
        return findings


class WriterAgent(BaseAgent):
    """Agent specialized in content creation."""
    
    def process_task(self, task: Dict) -> Dict:
        """Write content based on provided information."""
        content_type = task.get("type", "article")
        information = task.get("information", "")
        requirements = task.get("requirements", "")
        
        prompt = f"""Write a {content_type} based on the following information:

Information:
{information}

Requirements:
{requirements}

Create well-structured, engaging content.
"""
        
        response = self.llm(prompt)
        
        return {
            "content": response,
            "type": content_type,
            "word_count": len(response.split()),
            "status": "completed"
        }


class ReviewerAgent(BaseAgent):
    """Agent specialized in reviewing and providing feedback."""
    
    def process_task(self, task: Dict) -> Dict:
        """Review content and provide feedback."""
        content = task.get("content", "")
        criteria = task.get("criteria", ["accuracy", "clarity", "completeness"])
        
        prompt = f"""Review the following content:
{content}

Review criteria: {', '.join(criteria)}

Provide:
1. Overall quality score (0-10)
2. Specific feedback for each criterion
3. Suggestions for improvement
4. Whether it passes review (true/false)

Return as JSON:
{{
    "score": 8.5,
    "feedback": {{
        "accuracy": "...",
        "clarity": "...",
        "completeness": "..."
    }},
    "suggestions": [...],
    "passed": true
}}
"""
        
        response = self.llm(prompt)
        
        try:
            return json.loads(response)
        except:
            return {
                "score": 5.0,
                "feedback": {"general": response},
                "suggestions": [],
                "passed": False
            }


class Orchestrator:
    """
    Manages multiple agents and coordinates their work.
    
    Supports:
    - Sequential execution
    - Parallel execution
    - Hierarchical delegation
    """
    
    def __init__(self, llm_caller: Callable):
        self.llm = llm_caller
        self.agents: Dict[str, BaseAgent] = {}
        self.message_bus: List[Message] = []
        self.execution_log: List[Dict] = []
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator."""
        self.agents[agent.name] = agent
    
    def send_message(self, sender: str, receiver: str, 
                    content: Any, msg_type: str = "task"):
        """Route message between agents."""
        msg = Message(
            id=str(uuid.uuid4()),
            sender=sender,
            receiver=receiver,
            content=content,
            timestamp=time.time(),
            message_type=msg_type
        )
        self.message_bus.append(msg)
        
        if receiver in self.agents:
            self.agents[receiver].receive_message(msg)
        
        return msg
    
    def execute_sequential(self, pipeline: List[Dict]) -> List[Dict]:
        """
        Execute agents in sequence.
        
        Each agent's output becomes the next agent's input.
        """
        results = []
        current_input = None
        
        for step in pipeline:
            agent_name = step["agent"]
            task = step.get("task", current_input)
            
            if agent_name not in self.agents:
                raise ValueError(f"Agent '{agent_name}' not found")
            
            agent = self.agents[agent_name]
            
            # Log execution
            self.execution_log.append({
                "agent": agent_name,
                "task": str(task)[:100],
                "timestamp": time.time(),
                "status": "started"
            })
            
            # Execute
            result = agent.process_task(task)
            
            # Update log
            self.execution_log[-1]["status"] = "completed"
            self.execution_log[-1]["result"] = str(result)[:100]
            
            results.append({
                "agent": agent_name,
                "result": result
            })
            
            current_input = result
        
        return results
    
    def execute_parallel(self, tasks: List[Dict], 
                        max_workers: int = 3) -> List[Dict]:
        """
        Execute multiple agents in parallel.
        
        Each agent works independently on its task.
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            
            for task in tasks:
                agent_name = task["agent"]
                task_data = task.get("task", task)
                
                if agent_name in self.agents:
                    agent = self.agents[agent_name]
                    future = executor.submit(agent.process_task, task_data)
                    futures[future] = agent_name
            
            for future in as_completed(futures):
                agent_name = futures[future]
                try:
                    result = future.result()
                    results.append({
                        "agent": agent_name,
                        "result": result,
                        "status": "success"
                    })
                except Exception as e:
                    results.append({
                        "agent": agent_name,
                        "error": str(e),
                        "status": "failed"
                    })
        
        return results
    
    def execute_hierarchical(self, manager_task: Dict) -> Dict:
        """
        Execute with a manager agent delegating to workers.
        
        The manager breaks down the task and assigns subtasks.
        """
        # Get manager agent
        manager_name = manager_task.get("manager", "manager")
        if manager_name not in self.agents:
            raise ValueError(f"Manager agent '{manager_name}' not found")
        
        manager = self.agents[manager_name]
        
        # Manager creates a plan
        plan = manager.process_task({
            "type": "plan",
            "goal": manager_task["goal"],
            "available_agents": list(self.agents.keys())
        })
        
        # Execute subtasks
        subtask_results = []
        for subtask in plan.get("subtasks", []):
            agent_name = subtask.get("assigned_to", "default")
            
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                result = agent.process_task(subtask)
                subtask_results.append({
                    "subtask": subtask,
                    "result": result
                })
        
        # Manager aggregates results
        final_result = manager.process_task({
            "type": "aggregate",
            "original_goal": manager_task["goal"],
            "subtask_results": subtask_results
        })
        
        return final_result
    
    def get_execution_summary(self) -> Dict:
        """Get summary of all agent executions."""
        return {
            "total_executions": len(self.execution_log),
            "agents_used": list(set(
                log["agent"] for log in self.execution_log
            )),
            "execution_log": self.execution_log
        }


# === Usage Example ===

def mock_llm(prompt: str) -> str:
    """Mock LLM for demonstration."""
    if "Research" in prompt:
        return json.dumps({
            "findings": ["AI agents are autonomous systems"],
            "sources": ["Paper 1", "Paper 2"],
            "confidence": 0.85,
            "summary": "AI agents are systems that can perceive, reason, and act."
        })
    elif "Write" in prompt:
        return "AI agents represent a significant advancement in artificial intelligence..."
    elif "Review" in prompt:
        return json.dumps({
            "score": 8.0,
            "feedback": {"accuracy": "Good", "clarity": "Excellent"},
            "suggestions": ["Add more examples"],
            "passed": True
        })
    return "Task completed."

# Create orchestrator
orchestrator = Orchestrator(llm_caller=mock_llm)

# Register agents
orchestrator.register_agent(ResearchAgent(
    config=AgentConfig(name="researcher", role=AgentRole.RESEARCHER),
    llm_caller=mock_llm
))
orchestrator.register_agent(WriterAgent(
    config=AgentConfig(name="writer", role=AgentRole.WRITER),
    llm_caller=mock_llm
))
orchestrator.register_agent(ReviewerAgent(
    config=AgentConfig(name="reviewer", role=AgentRole.REVIEWER),
    llm_caller=mock_llm
))

# Sequential pipeline
print("=== Sequential Execution ===")
results = orchestrator.execute_sequential([
    {"agent": "researcher", "task": {"topic": "AI agents"}},
    {"agent": "writer", "task": {"type": "article", "information": "AI agents..."}},
    {"agent": "reviewer", "task": {"content": "AI agents represent..."}}
])

for r in results:
    print(f"{r['agent']}: {str(r['result'])[:50]}...")

# Parallel execution
print("\n=== Parallel Execution ===")
results = orchestrator.execute_parallel([
    {"agent": "researcher", "task": {"topic": "Topic A"}},
    {"agent": "researcher", "task": {"topic": "Topic B"}},
    {"agent": "researcher", "task": {"topic": "Topic C"}}
])

for r in results:
    print(f"{r['agent']}: {r['status']}")
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Too Many Agents
```python
# ❌ BAD: Creating unnecessary agents
agents = [Agent(f"agent_{i}") for i in range(20)]

# ✅ GOOD: Only create agents with clear roles
agents = {
    "researcher": ResearchAgent(),
    "writer": WriterAgent(),
    "reviewer": ReviewerAgent()
}
```

### Mistake 2: No Clear Communication Protocol
```python
# ❌ BAD: Agents talking over each other
agent1.send(agent2, "do this")
agent2.send(agent3, "also do this")  # Confusion!

# ✅ GOOD: Structured message passing
message = {
    "type": "task",
    "from": "manager",
    "to": "worker",
    "content": {...},
    "requires_response": True
}
```

### Mistake 3: No Error Handling
```python
# ❌ BAD: Assuming all agents succeed
for agent in agents:
    agent.execute()  # What if one fails?

# ✅ GOOD: Handle agent failures
for agent in agents:
    try:
        agent.execute()
    except AgentError as e:
        handle_failure(agent, e)
```

---

## ✅ Best Practices

1. **Specialize Agents**: Give each agent a clear, focused role
2. **Structured Communication**: Use formal message formats
3. **Handle Failures**: Plan for agent failures and retries
4. **Limit Agent Count**: More agents = more complexity
5. **Use Shared Memory**: For agents that need common context
6. **Monitor Performance**: Track agent execution and results
7. **Start Simple**: Begin with 2-3 agents, add more as needed
8. **Document Roles**: Clear documentation of each agent's responsibilities

---

## 🏋️ Practice Exercises

### Exercise 1: Research Team
Build a multi-agent system with:
- A researcher agent
- A writer agent
- A reviewer agent
Working together to produce a report.

### Exercise 2: Parallel Processing
Create agents that process different data sources simultaneously.

### Exercise 3: Hierarchical System
Implement a manager-worker pattern where:
- Manager decomposes tasks
- Workers execute subtasks
- Manager aggregates results

---

## 📝 Summary

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Sequential** | One after another | Linear pipelines |
| **Parallel** | Simultaneous | Independent tasks |
| **Hierarchical** | Manager + workers | Complex projects |
| **Collaborative** | Discussion-based | Creative work |

---

## 🔗 Next Lecture

In **Lecture 07: Agent Communication**, we'll dive deeper into how agents communicate and share information.
