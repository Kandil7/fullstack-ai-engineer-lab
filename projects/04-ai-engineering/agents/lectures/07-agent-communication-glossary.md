# Glossary: Agent Communication

> Terms defined in alphabetical order.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Asynchronous | Non-blocking communication | Message Queue |
| Broadcast | One-to-all message delivery | Publish |
| Channel | Communication pathway | Bus, Pipe |
| Correlation ID | Links requests to responses | Request-Response |
| Deadlock | Agents waiting forever | Timeout |
| Heartbeat | Periodic health signal | Health Check |
| Inbox | Agent's message queue | Mailbox |
| Message | Unit of communication | Packet |
| Message Bus | Central routing infrastructure | Broker |
| Publish | Send to topic subscribers | Pub-Sub |
| Queue | FIFO message storage | Buffer |
| Request | Message expecting response | Query |
| Response | Reply to a request | Answer |
| Subscribe | Register interest in a topic | Listener |
| Synchronous | Blocking request-response | Blocking |
| Timeout | Maximum wait time | Deadline |

---

## A

### Asynchronous

**Definition:** A communication pattern where messages are sent without waiting for an immediate response. The sender continues processing while the receiver handles the message independently.

**Example:**
```python
import asyncio
from typing import Any, Callable

class AsyncMessageBus:
    """Asynchronous message passing system."""
    
    def __init__(self):
        self.handlers = {}
        self.message_queue = asyncio.Queue()
    
    def register(self, agent_id: str, handler: Callable):
        """Register async handler for an agent."""
        self.handlers[agent_id] = handler
    
    async def send(self, receiver: str, message: Any):
        """Send message asynchronously."""
        await self.message_queue.put({
            "receiver": receiver,
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def process_messages(self):
        """Process messages from queue."""
        while True:
            msg = await self.message_queue.get()
            handler = self.handlers.get(msg["receiver"])
            if handler:
                asyncio.create_task(handler(msg["message"]))

# Usage
async def agent_handler(message):
    print(f"Received: {message}")
    await asyncio.sleep(1)  # Simulate processing
    print("Processing complete")

bus = AsyncMessageBus()
bus.register("agent1", agent_handler)

async def main():
    await bus.send("agent1", {"task": "do something"})
    await bus.process_messages()

# asyncio.run(main())
```

**Related terms:** Non-blocking, Message Queue, Concurrency

---

## B

### Broadcast

**Definition:** Sending a message to all agents in the system, or to all agents in a group. Broadcast is useful for announcements, state synchronization, or emergency notifications.

**Example:**
```python
from typing import Dict, Set

class BroadcastSystem:
    """Handles broadcast messaging between agents."""
    
    def __init__(self):
        self.agents: Dict[str, callable] = {}
        self.groups: Dict[str, Set[str]] = {}
        self.message_log = []
    
    def register_agent(self, agent_id: str, handler: callable):
        """Register an agent."""
        self.agents[agent_id] = handler
    
    def create_group(self, group_name: str, agent_ids: Set[str]):
        """Create a broadcast group."""
        self.groups[group_name] = agent_ids
    
    def broadcast(self, sender: str, message: Any, 
                 group: str = None):
        """Broadcast message to all agents or group."""
        targets = set(self.agents.keys())
        
        if group and group in self.groups:
            targets = self.groups[group]
        
        # Remove sender from targets
        targets.discard(sender)
        
        # Deliver to all targets
        for agent_id in targets:
            handler = self.agents.get(agent_id)
            if handler:
                handler({
                    "sender": sender,
                    "message": message,
                    "type": "broadcast"
                })
        
        self.message_log.append({
            "sender": sender,
            "targets": list(targets),
            "message": message
        })

# Usage
broadcaster = BroadcastSystem()

def agent_handler(msg):
    print(f"Agent received broadcast from {msg['sender']}: {msg['message']}")

broadcaster.register_agent("agent1", agent_handler)
broadcaster.register_agent("agent2", agent_handler)
broadcaster.register_agent("agent3", agent_handler)

broadcaster.broadcast("agent1", "System update available")
```

**Related terms:** One-to-All, Group Message, Announcement

---

## C

### Correlation ID

**Definition:** A unique identifier that links a response message to its original request. Essential for request-response patterns where multiple requests may be in flight.

**Example:**
```python
import uuid
import time
from typing import Dict, Optional

class RequestTracker:
    """Tracks requests and matches responses using correlation IDs."""
    
    def __init__(self, timeout: float = 30.0):
        self.pending_requests: Dict[str, dict] = {}
        self.timeout = timeout
    
    def create_request(self, receiver: str, content: Any) -> str:
        """Create a new request with correlation ID."""
        correlation_id = str(uuid.uuid4())
        
        self.pending_requests[correlation_id] = {
            "receiver": receiver,
            "content": content,
            "timestamp": time.time(),
            "response": None
        }
        
        return correlation_id
    
    def match_response(self, correlation_id: str, 
                      response: Any) -> bool:
        """Match a response to its request."""
        if correlation_id in self.pending_requests:
            self.pending_requests[correlation_id]["response"] = response
            return True
        return False
    
    def get_response(self, correlation_id: str,
                    wait: bool = True) -> Optional[Any]:
        """Get response for a request."""
        if correlation_id not in self.pending_requests:
            return None
        
        request = self.pending_requests[correlation_id]
        
        if request["response"]:
            return request["response"]
        
        if wait:
            start = time.time()
            while time.time() - start < self.timeout:
                if request["response"]:
                    return request["response"]
                time.sleep(0.01)
        
        return None
    
    def cleanup_expired(self):
        """Remove expired requests."""
        now = time.time()
        expired = [
            cid for cid, req in self.pending_requests.items()
            if now - req["timestamp"] > self.timeout
        ]
        for cid in expired:
            del self.pending_requests[cid]

# Usage
tracker = RequestTracker(timeout=5.0)

# Create request
correlation_id = tracker.create_request("agent_b", {"task": "research"})

# Later, match response
tracker.match_response(correlation_id, {"result": "found info"})

# Get response
response = tracker.get_response(correlation_id, wait=False)
print(response)  # {'result': 'found info'}
```

**Related terms:** Request-Response, Message ID, Tracking

---

## D

### Deadlock

**Definition:** A situation where two or more agents are each waiting for the other to respond, resulting in neither making progress. Deadlocks must be prevented through careful design.

**Example:**
```python
import threading
import time

class DeadlockDetector:
    """Detects potential deadlocks in agent communication."""
    
    def __init__(self):
        self.waiting_for: Dict[str, str] = {}  # agent -> waiting_for_agent
        self._lock = threading.Lock()
    
    def register_wait(self, waiter: str, target: str):
        """Register that agent is waiting for another."""
        with self._lock:
            self.waiting_for[waiter] = target
    
    def clear_wait(self, waiter: str):
        """Clear waiting status."""
        with self._lock:
            self.waiting_for.pop(waiter, None)
    
    def detect_deadlock(self) -> Optional[tuple]:
        """Detect if there's a deadlock cycle."""
        with self._lock:
            visited = set()
            
            for start_agent in self.waiting_for:
                if start_agent in visited:
                    continue
                
                path = [start_agent]
                current = start_agent
                
                while current in self.waiting_for:
                    next_agent = self.waiting_for[current]
                    
                    if next_agent in path:
                        # Found cycle
                        cycle_start = path.index(next_agent)
                        return tuple(path[cycle_start:])
                    
                    path.append(next_agent)
                    current = next_agent
                    visited.add(current)
            
            return None

# Example of deadlock scenario
detector = DeadlockDetector()

# Agent A waiting for B, B waiting for A
detector.register_wait("agent_a", "agent_b")
detector.register_wait("agent_b", "agent_a")

deadlock = detector.detect_deadlock()
if deadlock:
    print(f"Deadlock detected: {deadlock}")
```

**Related terms:** Circular Wait, Livelock, Starvation

---

## M

### Message

**Definition:** A unit of information exchanged between agents. Messages contain a sender, receiver, content, and metadata for routing and processing.

**Example:**
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import time
import uuid

@dataclass
class Message:
    """Standard message format for agent communication."""
    
    sender: str
    receiver: str
    content: Any
    message_type: str = "general"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)
    
    def is_request(self) -> bool:
        return self.message_type == "request"
    
    def is_response(self) -> bool:
        return self.message_type == "response"
    
    def create_response(self, content: Any) -> "Message":
        """Create a response to this message."""
        return Message(
            sender=self.receiver,
            receiver=self.sender,
            content=content,
            message_type="response",
            metadata={"correlation_id": self.id}
        )

# Usage
request = Message(
    sender="agent_a",
    receiver="agent_b",
    content={"task": "analyze data"},
    message_type="request"
)

response = request.create_response(
    {"result": "Analysis complete", "findings": [...]}
)

print(f"Request ID: {request.id}")
print(f"Response correlates to: {response.metadata['correlation_id']}")
```

**Related terms:** Packet, Signal, Data

---

### Message Bus

**Definition:** Central infrastructure that routes messages between agents. Decouples agents from direct knowledge of each other, enabling flexible communication patterns.

**Example:**
```python
from typing import Callable, Dict, List
from collections import defaultdict
import threading

class MessageBus:
    """Central message routing system."""
    
    def __init__(self):
        self.agents: Dict[str, Callable] = {}
        self.queues: Dict[str, List] = defaultdict(list)
        self._lock = threading.Lock()
    
    def register(self, agent_id: str, handler: Callable):
        """Register an agent handler."""
        with self._lock:
            self.agents[agent_id] = handler
    
    def unregister(self, agent_id: str):
        """Remove an agent."""
        with self._lock:
            self.agents.pop(agent_id, None)
            self.queues.pop(agent_id, None)
    
    def send(self, message: dict) -> bool:
        """Route a message to its destination."""
        receiver = message.get("receiver")
        
        with self._lock:
            if receiver in self.agents:
                self.queues[receiver].append(message)
                return True
            return False
    
    def deliver(self, agent_id: str) -> List[dict]:
        """Deliver queued messages to an agent."""
        with self._lock:
            messages = self.queues.get(agent_id, []).copy()
            self.queues[agent_id] = []
        return messages
    
    def broadcast(self, sender: str, message: Any):
        """Send to all agents except sender."""
        with self._lock:
            for agent_id in self.agents:
                if agent_id != sender:
                    self.queues[agent_id].append({
                        "sender": sender,
                        "receiver": agent_id,
                        "content": message,
                        "type": "broadcast"
                    })

# Usage
bus = MessageBus()

def handler_a(msg):
    print(f"Agent A received: {msg}")

bus.register("agent_a", handler_a)
bus.send({"sender": "agent_b", "receiver": "agent_a", "content": "Hello"})
```

**Related terms:** Router, Broker, Middleware

---

## P

### Publish-Subscribe

**Definition:** A messaging pattern where senders (publishers) send messages to topics without knowledge of receivers (subscribers). Subscribers express interest in topics and receive relevant messages.

**Example:**
```python
from typing import Callable, Dict, Set
from collections import defaultdict

class PubSubSystem:
    """Publish-Subscribe messaging system."""
    
    def __init__(self):
        self.subscribers: Dict[str, Set[Callable]] = defaultdict(set)
        self.publisher_topics: Dict[str, Set[str]] = defaultdict(set)
        self.message_log = []
    
    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to a topic."""
        self.subscribers[topic].add(handler)
    
    def unsubscribe(self, topic: str, handler: Callable):
        """Unsubscribe from a topic."""
        self.subscribers[topic].discard(handler)
    
    def publish(self, topic: str, message: Any, 
               publisher: str = None):
        """Publish a message to a topic."""
        self.message_log.append({
            "topic": topic,
            "message": message,
            "publisher": publisher
        })
        
        for handler in self.subscribers.get(topic, []):
            handler({
                "topic": topic,
                "message": message,
                "publisher": publisher
            })
    
    def get_topics(self) -> list:
        """Get all active topics."""
        return list(self.subscribers.keys())

# Usage
pubsub = PubSubSystem()

def handle_weather_update(msg):
    print(f"Weather update: {msg['message']}")

def handle_news(msg):
    print(f"News: {msg['message']}")

pubsub.subscribe("weather", handle_weather_update)
pubsub.subscribe("news", handle_news)

pubsub.publish("weather", {"temp": 72, "condition": "sunny"})
pubsub.publish("news", {"headline": "AI breakthrough"})
```

**Related terms:** Topic, Subscriber, Event-Driven

---

## Q

### Queue

**Definition:** A FIFO (First-In-First-Out) data structure used to buffer messages for agents. Queues decouple message sending from processing, enabling asynchronous communication.

**Example:**
```python
import threading
import time
from typing import Any
from collections import deque

class MessageQueue:
    """Thread-safe message queue."""
    
    def __init__(self, max_size: int = 1000):
        self.queue = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self.not_empty = threading.Condition(self._lock)
    
    def put(self, message: Any, timeout: float = None) -> bool:
        """Add message to queue."""
        with self._lock:
            if len(self.queue) >= self.queue.maxlen:
                return False
            self.queue.append(message)
            self.not_empty.notify()
            return True
    
    def get(self, timeout: float = None) -> Any:
        """Get message from queue."""
        with self._lock:
            if timeout:
                end_time = time.time() + timeout
                while not self.queue:
                    remaining = end_time - time.time()
                    if remaining <= 0:
                        return None
                    self.not_empty.wait(remaining)
            else:
                while not self.queue:
                    self.not_empty.wait()
            
            return self.queue.popleft() if self.queue else None
    
    def size(self) -> int:
        """Get queue size."""
        with self._lock:
            return len(self.queue)
    
    def clear(self):
        """Clear the queue."""
        with self._lock:
            self.queue.clear()

# Usage
queue = MessageQueue(max_size=100)

# Producer thread
def producer():
    for i in range(10):
        queue.put(f"Message {i}")
        time.sleep(0.1)

# Consumer thread
def consumer():
    while True:
        msg = queue.get(timeout=1.0)
        if msg:
            print(f"Processing: {msg}")
        else:
            break
```

**Related terms:** Buffer, FIFO, Inbox

---

## S

### Synchronous

**Definition:** A communication pattern where the sender waits for the receiver to process the message and send a response before continuing. Also called blocking or request-response.

**Example:**
```python
import time
from typing import Any, Optional

class SyncCommunicator:
    """Synchronous request-response communication."""
    
    def __init__(self):
        self.agents = {}
        self.pending_responses = {}
    
    def register_agent(self, agent_id: str, handler):
        """Register agent handler."""
        self.agents[agent_id] = handler
    
    def request(self, sender: str, receiver: str, 
               content: Any, timeout: float = 30.0) -> Optional[Any]:
        """
        Send request and wait for response.
        
        Args:
            sender: Who is asking
            receiver: Who to ask
            content: Request content
            timeout: Max wait time
            
        Returns:
            Response or None if timeout
        """
        if receiver not in self.agents:
            return None
        
        # Create request with callback
        request_id = f"{sender}_{time.time()}"
        response = [None]  # Mutable container for closure
        event = threading.Event()
        
        def response_callback(resp):
            response[0] = resp
            event.set()
        
        self.pending_responses[request_id] = response_callback
        
        # Send request
        self.agents[receiver]({
            "sender": sender,
            "content": content,
            "request_id": request_id,
            "respond": response_callback
        })
        
        # Wait for response
        event.wait(timeout)
        
        # Cleanup
        self.pending_responses.pop(request_id, None)
        
        return response[0]

# Usage
sync = SyncCommunicator()

def agent_handler(request):
    # Process and respond
    result = f"Processed: {request['content']}"
    request["respond"](result)

sync.register_agent("worker", agent_handler)

response = sync.request("manager", "worker", {"task": "analyze"})
print(response)  # "Processed: {'task': 'analyze'}"
```

**Related terms:** Blocking, Request-Response, Return Value

---

## Quick Reference: Communication Patterns

```
┌─────────────────────────────────────────────────────────────┐
│              Communication Patterns Summary                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SYNCHRONOUS                                                │
│  A ──request──► B                                           │
│  A ◄──response── B    (A blocks until response)            │
│                                                             │
│  ASYNCHRONOUS                                               │
│  A ──message──► [Queue] ──► B                               │
│  A continues immediately                                    │
│                                                             │
│  BROADCAST                                                  │
│  A ──message──► [All B, C, D]                               │
│                                                             │
│  PUBLISH-SUBSCRIBE                                          │
│  A ──publish("topic")──► [Broker]                           │
│                             ├──► B (subscribed)             │
│                             └──► C (subscribed)             │
│                                                             │
│  REQUEST-RESPONSE (with Correlation)                        │
│  A ──{id:123, req}──► B                                     │
│  A ◄──{correlates:123, resp}── B                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 07](./07-agent-communication-lecture.md)** | **[Next: Lecture 08 →](./08-agent-evaluation-glossary.md)**
