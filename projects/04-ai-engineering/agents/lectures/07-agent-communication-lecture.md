# Lecture 07: Agent Communication

## 🎯 Topic Overview

**Agent communication** is how AI agents exchange information, coordinate actions, and collaborate to achieve shared goals. Effective communication protocols are essential for multi-agent systems to function properly.

This lecture covers:
- Communication patterns (synchronous, asynchronous, broadcast)
- Message formats and protocols
- Shared state vs. message passing
- Building communication infrastructure
- Handling communication failures

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Design** communication protocols for multi-agent systems
2. **Implement** message passing between agents
3. **Build** shared memory systems for collaboration
4. **Handle** asynchronous communication patterns
5. **Debug** communication issues in multi-agent systems
6. **Optimize** communication for performance
7. **Implement** error handling for message delivery
8. **Design** scalable communication architectures

---

## 🧩 Key Concepts

### 1. Communication Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                 Communication Patterns                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SYNCHRONOUS (Request-Response)                             │
│  Agent A ──request──► Agent B                               │
│  Agent A ◄──response── Agent B                              │
│                                                             │
│  ASYNCHRONOUS (Message Queue)                               │
│  Agent A ──message──► [Queue] ──► Agent B                   │
│                                                             │
│  BROADCAST                                                  │
│  Agent A ──message──► All Agents                            │
│                                                             │
│  PUBLISH-SUBSCRIBE                                          │
│  Publisher ──topic──► [Broker] ──► Subscriber A             │
│                                   ──► Subscriber B          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Message Format

```python
@dataclass
class AgentMessage:
    id: str                    # Unique message ID
    sender: str                # Sender agent ID
    receiver: str              # Receiver agent ID (or "all")
    content: Any               # Message payload
    message_type: str          # request, response, notification
    timestamp: float           # When message was sent
    correlation_id: str = None # For matching requests to responses
    metadata: dict = None      # Additional information
```

### 3. Communication Infrastructure

```
┌─────────────────────────────────────────────────────────────┐
│              Communication Infrastructure                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Message Router                    │   │
│  │  • Routes messages to correct agents                │   │
│  │  • Handles broadcasts                               │   │
│  │  • Manages delivery guarantees                      │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐              │
│         │                 │                 │              │
│         ▼                 ▼                 ▼              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│  │  Agent A    │   │  Agent B    │   │  Agent C    │      │
│  │  ┌───────┐  │   │  ┌───────┐  │   │  ┌───────┐  │      │
│  │  │ Inbox │  │   │  │ Inbox │  │   │  │ Inbox │  │      │
│  │  └───────┘  │   │  └───────┘  │   │  └───────┘  │      │
│  └─────────────┘   └─────────────┘   └─────────────┘      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Shared Memory Store                  │   │
│  │  • Common state accessible to all agents            │   │
│  │  • Thread-safe read/write operations                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Examples

### Example 1: Complete Communication System

```python
"""
Multi-Agent Communication System
Implements various communication patterns.
"""
import json
import time
import uuid
import threading
from typing import Any, Callable, Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from queue import Queue


class MessageType(Enum):
    """Types of messages agents can send."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    ERROR = "error"


@dataclass
class Message:
    """A message between agents."""
    id: str
    sender: str
    receiver: str
    content: Any
    message_type: MessageType
    timestamp: float
    correlation_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "type": self.message_type.value,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        return cls(
            id=data["id"],
            sender=data["sender"],
            receiver=data["receiver"],
            content=data["content"],
            message_type=MessageType(data["type"]),
            timestamp=data["timestamp"],
            correlation_id=data.get("correlation_id"),
            metadata=data.get("metadata", {})
        )


class MessageBus:
    """
    Central message bus for agent communication.
    
    Features:
    - Message routing
    - Topic-based pub/sub
    - Message history
    - Delivery guarantees
    """
    
    def __init__(self):
        self.agents: Dict[str, Callable] = {}
        self.inboxes: Dict[str, Queue] = defaultdict(Queue)
        self.subscribers: Dict[str, Set[str]] = defaultdict(set)
        self.message_history: List[Message] = []
        self._lock = threading.Lock()
    
    def register_agent(self, agent_id: str, 
                      message_handler: Callable):
        """Register an agent with the message bus."""
        self.agents[agent_id] = message_handler
    
    def unregister_agent(self, agent_id: str):
        """Unregister an agent."""
        self.agents.pop(agent_id, None)
        self.inboxes.pop(agent_id, None)
    
    def send(self, message: Message) -> bool:
        """
        Send a message to a specific agent.
        
        Returns True if delivered, False otherwise.
        """
        with self._lock:
            self.message_history.append(message)
        
        # Direct message
        if message.receiver in self.agents:
            self.inboxes[message.receiver].put(message)
            return True
        
        return False
    
    def broadcast(self, sender: str, content: Any,
                 message_type: MessageType = MessageType.BROADCAST):
        """Broadcast a message to all agents except sender."""
        message = Message(
            id=str(uuid.uuid4()),
            sender=sender,
            receiver="all",
            content=content,
            message_type=message_type,
            timestamp=time.time()
        )
        
        with self._lock:
            self.message_history.append(message)
        
        for agent_id in self.agents:
            if agent_id != sender:
                self.inboxes[agent_id].put(message)
    
    def publish(self, topic: str, sender: str, content: Any):
        """Publish a message to a topic."""
        message = Message(
            id=str(uuid.uuid4()),
            sender=sender,
            receiver=topic,
            content=content,
            message_type=MessageType.NOTIFICATION,
            timestamp=time.time(),
            metadata={"topic": topic}
        )
        
        with self._lock:
            self.message_history.append(message)
        
        # Deliver to topic subscribers
        for subscriber in self.subscribers.get(topic, []):
            if subscriber != sender:
                self.inboxes[subscriber].put(message)
    
    def subscribe(self, agent_id: str, topic: str):
        """Subscribe an agent to a topic."""
        self.subscribers[topic].add(agent_id)
    
    def unsubscribe(self, agent_id: str, topic: str):
        """Unsubscribe an agent from a topic."""
        self.subscribers[topic].discard(agent_id)
    
    def get_messages(self, agent_id: str) -> List[Message]:
        """Get all pending messages for an agent."""
        messages = []
        while not self.inboxes[agent_id].empty():
            messages.append(self.inboxes[agent_id].get())
        return messages
    
    def get_message_history(self, agent_id: str = None,
                          limit: int = 100) -> List[Message]:
        """Get message history, optionally filtered by agent."""
        with self._lock:
            history = self.message_history.copy()
        
        if agent_id:
            history = [m for m in history 
                      if m.sender == agent_id or m.receiver == agent_id]
        
        return history[-limit:]


class CommunicatingAgent:
    """
    Agent with built-in communication capabilities.
    """
    
    def __init__(self, agent_id: str, message_bus: MessageBus,
                 llm_caller: Callable = None):
        self.agent_id = agent_id
        self.bus = message_bus
        self.llm = llm_caller
        self.message_handlers: Dict[str, Callable] = {}
        
        # Register with message bus
        self.bus.register_agent(agent_id, self.handle_message)
    
    def send_message(self, receiver: str, content: Any,
                    msg_type: MessageType = MessageType.REQUEST,
                    correlation_id: str = None) -> Message:
        """Send a message to another agent."""
        message = Message(
            id=str(uuid.uuid4()),
            sender=self.agent_id,
            receiver=receiver,
            content=content,
            message_type=msg_type,
            timestamp=time.time(),
            correlation_id=correlation_id
        )
        
        self.bus.send(message)
        return message
    
    def send_request(self, receiver: str, content: Any) -> Message:
        """Send a request and wait for response."""
        return self.send_message(
            receiver, content, MessageType.REQUEST
        )
    
    def send_response(self, receiver: str, content: Any,
                     correlation_id: str) -> Message:
        """Send a response to a request."""
        return self.send_message(
            receiver, content, MessageType.RESPONSE, correlation_id
        )
    
    def broadcast(self, content: Any):
        """Broadcast a message to all agents."""
        self.bus.broadcast(self.agent_id, content)
    
    def publish(self, topic: str, content: Any):
        """Publish to a topic."""
        self.bus.publish(topic, self.agent_id, content)
    
    def subscribe(self, topic: str):
        """Subscribe to a topic."""
        self.bus.subscribe(self.agent_id, topic)
    
    def receive_messages(self) -> List[Message]:
        """Get pending messages."""
        return self.bus.get_messages(self.agent_id)
    
    def handle_message(self, message: Message):
        """Handle an incoming message."""
        # Default handling - can be overridden
        pass
    
    def register_handler(self, message_type: str, 
                        handler: Callable):
        """Register a handler for a specific message type."""
        self.message_handlers[message_type] = handler
    
    def process_inbox(self):
        """Process all messages in inbox."""
        messages = self.receive_messages()
        
        for message in messages:
            # Check for registered handler
            handler = self.message_handlers.get(
                message.message_type.value
            )
            if handler:
                handler(message)
            
            # Handle responses to our requests
            if message.message_type == MessageType.RESPONSE:
                self._handle_response(message)
    
    def _handle_response(self, message: Message):
        """Handle a response message."""
        # Store response for request correlation
        pass


class RequestResponseAgent(CommunicatingAgent):
    """
    Agent that implements request-response pattern.
    
    Can send requests and await responses.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pending_requests: Dict[str, dict] = {}
        self._lock = threading.Lock()
    
    def request_and_wait(self, receiver: str, content: Any,
                        timeout: float = 30.0) -> Optional[Message]:
        """
        Send a request and wait for response.
        
        Args:
            receiver: Target agent
            content: Request content
            timeout: Max seconds to wait
            
        Returns:
            Response message or None if timeout
        """
        request_id = str(uuid.uuid4())
        
        # Store pending request
        with self._lock:
            self.pending_requests[request_id] = {
                "receiver": receiver,
                "timestamp": time.time(),
                "response": None
            }
        
        # Send request
        self.send_message(
            receiver, content, MessageType.REQUEST, request_id
        )
        
        # Wait for response
        start_time = time.time()
        while time.time() - start_time < timeout:
            messages = self.receive_messages()
            
            for msg in messages:
                if (msg.message_type == MessageType.RESPONSE and 
                    msg.correlation_id == request_id):
                    return msg
            
            time.sleep(0.1)
        
        # Timeout
        return None


# === Usage Example ===

# Create message bus
bus = MessageBus()

# Create agents
agent_a = CommunicatingAgent("agent_a", bus)
agent_b = CommunicatingAgent("agent_b", bus)
agent_c = CommunicatingAgent("agent_c", bus)

# Send messages
agent_a.send_message("agent_b", {"task": "research AI"})
agent_b.send_message("agent_a", {"result": "Found 5 papers"})

# Broadcast
agent_a.broadcast({"announcement": "Meeting at 3pm"})

# Pub/Sub
agent_b.subscribe("updates")
agent_c.publish("updates", {"status": "Task complete"})

# Check messages
print("Agent A messages:", len(agent_a.receive_messages()))
print("Agent B messages:", len(agent_b.receive_messages()))
print("Message history:", len(bus.get_message_history()))
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Synchronous Deadlocks
```python
# ❌ BAD: Agents waiting for each other indefinitely
def agent_a():
    response = request_from_b()  # Waits for B
    process(response)

def agent_b():
    response = request_from_a()  # Waits for A - DEADLOCK!
    process(response)

# ✅ GOOD: Use async communication
def agent_a():
    send_to_b(message)
    # Don't wait - handle response asynchronously

def agent_b():
    send_to_a(message)
    # Don't wait - handle response asynchronously
```

### Mistake 2: No Message IDs
```python
# ❌ BAD: Can't match responses to requests
send_request("do something")
# Later...
process_response(response)  # Which request is this for?

# ✅ GOOD: Use correlation IDs
request_id = send_request("do something")
# Later...
process_response(response, request_id)  # Clear which request
```

### Mistake 3: Unbounded Message Queues
```python
# ❌ BAD: Queue grows forever
class BadAgent:
    def __init__(self):
        self.messages = []  # Never cleaned up!
    
    def receive(self, msg):
        self.messages.append(msg)  # Memory leak!

# ✅ GOOD: Process and clear messages
class GoodAgent:
    def __init__(self, max_queue=100):
        self.messages = deque(maxlen=max_queue)
    
    def process_messages(self):
        while self.messages:
            msg = self.messages.popleft()
            self.handle(msg)
```

---

## ✅ Best Practices

1. **Use Message IDs**: Always include unique IDs for request-response matching
2. **Set Timeouts**: Don't wait indefinitely for responses
3. **Handle Failures**: Plan for message delivery failures
4. **Limit Queue Size**: Prevent memory issues with bounded queues
5. **Log Communications**: Keep records for debugging
6. **Use Structured Messages**: Define clear message formats
7. **Implement Heartbeats**: Detect disconnected agents
8. **Test Communication**: Verify message delivery works correctly

---

## 🏋️ Practice Exercises

### Exercise 1: Request-Response System
Build agents that can send requests and receive responses with proper correlation.

### Exercise 2: Pub/Sub System
Create a topic-based publish-subscribe system for agent communication.

### Exercise 3: Broadcast System
Implement broadcasting where one agent can send messages to all other agents.

---

## 📝 Summary

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Request-Response** | Synchronous exchange | Queries |
| **Message Queue** | Asynchronous delivery | Background tasks |
| **Pub-Sub** | Topic-based distribution | Events |
| **Broadcast** | One-to-all messaging | Announcements |

---

## 🔗 Next Lecture

In **Lecture 08: Agent Evaluation**, we'll explore how to measure and improve agent performance.
