"""
=============================================================
Exercise 07: Agent Communication
=============================================================

Topic Overview:
Agent communication enables multiple agents to coordinate,
share information, and collaborate on complex tasks. This
exercise covers:

1. Message Passing Protocols - Structured communication between agents
2. Shared State Management - Concurrent access to shared data
3. Event-Driven Communication - Pub/sub and event patterns
4. Agent Handshake - Connection establishment protocols
5. Broadcast vs Unicast - Different messaging patterns

Key Concepts:
- Message passing decouples agents for flexibility
- Shared state requires synchronization mechanisms
- Event-driven patterns enable loose coupling
- Handshakes establish communication contracts
- Different patterns suit different use cases

Prerequisites:
- Understanding of async/await patterns
- Familiarity with agent fundamentals (Exercise 01)
=============================================================
"""

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from collections import defaultdict
from asyncio import Queue, Event
import threading


# ============================================================
# Core Data Structures
# ============================================================

class MessageType(Enum):
    """Types of messages in the communication system."""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"
    ERROR = "error"
    ACK = "ack"
    SHUTDOWN = "shutdown"
    SUBSCRIBE = "subscribe"
    PUBLISH = "publish"


class AgentState(Enum):
    """Communication state of an agent."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    PROCESSING = "processing"
    ERROR = "error"


@dataclass
class Message:
    """Structured message format for agent communication."""
    message_id: str
    sender_id: str
    receiver_id: Optional[str]  # None for broadcasts
    message_type: MessageType
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None  # For request-response pairing
    ttl: int = 30  # Time to live in seconds
    priority: int = 0  # Higher = more priority

    def is_expired(self) -> bool:
        """Check if message has expired."""
        age = (datetime.now() - self.timestamp).total_seconds()
        return age > self.ttl

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "message_type": self.message_type.value,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "ttl": self.ttl,
            "priority": self.priority
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create message from dictionary."""
        return cls(
            message_id=data["message_id"],
            sender_id=data["sender_id"],
            receiver_id=data.get("receiver_id"),
            message_type=MessageType(data["message_type"]),
            payload=data["payload"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            correlation_id=data.get("correlation_id"),
            ttl=data.get("ttl", 30),
            priority=data.get("priority", 0)
        )


@dataclass
class MessageEnvelope:
    """Wraps a message with delivery metadata."""
    message: Message
    attempts: int = 0
    delivered: bool = False
    acknowledged: bool = False


# ============================================================
# Example 1: Message Passing Protocols
# ============================================================

class MessageBus:
    """
    Central message bus for agent communication.
    
    Implements multiple delivery patterns:
    - Point-to-point (unicast)
    - Publish-subscribe (broadcast)
    - Request-response (synchronous)
    """

    def __init__(self):
        self.queues: Dict[str, Queue] = {}
        self.subscribers: Dict[str, Set[str]] = defaultdict(set)
        self.message_log: List[Message] = []
        self._lock = asyncio.Lock()
        self._running = True

    def register_agent(self, agent_id: str) -> Queue:
        """Register an agent and create its message queue."""
        if agent_id not in self.queues:
            self.queues[agent_id] = Queue(maxsize=100)
            print(f"  Registered agent: {agent_id}")
        return self.queues[agent_id]

    async def send(self, message: Message) -> bool:
        """Send a message to a specific agent."""
        async with self._lock:
            self.message_log.append(message)

            if message.receiver_id in self.queues:
                try:
                    self.queues[message.receiver_id].put_nowait(message)
                    print(f"  Sent: {message.message_type.value} "
                          f"from {message.sender_id} to {message.receiver_id}")
                    return True
                except asyncio.QueueFull:
                    print(f"  Queue full for {message.receiver_id}")
                    return False
            else:
                print(f"  Agent not found: {message.receiver_id}")
                return False

    async def broadcast(self, message: Message) -> int:
        """Broadcast a message to all registered agents."""
        async with self._lock:
            self.message_log.append(message)
            delivered = 0

            for agent_id, queue in self.queues.items():
                if agent_id != message.sender_id:
                    try:
                        queue.put_nowait(message)
                        delivered += 1
                    except asyncio.QueueFull:
                        pass

            print(f"  Broadcast from {message.sender_id}: "
                  f"delivered to {delivered} agents")
            return delivered

    def subscribe(self, agent_id: str, topic: str) -> None:
        """Subscribe an agent to a topic."""
        self.subscribers[topic].add(agent_id)
        print(f"  {agent_id} subscribed to '{topic}'")

    async def publish(self, message: Message, topic: str) -> int:
        """Publish a message to a topic."""
        async with self._lock:
            self.message_log.append(message)
            delivered = 0

            for agent_id in self.subscribers.get(topic, set()):
                if agent_id != message.sender_id:
                    try:
                        self.queues[agent_id].put_nowait(message)
                        delivered += 1
                    except asyncio.QueueFull:
                        pass

            print(f"  Published to '{topic}': delivered to {delivered}")
            return delivered

    async def request_response(
        self,
        request: Message,
        timeout: float = 5.0
    ) -> Optional[Message]:
        """
        Synchronous request-response pattern.
        
        Sends a request and waits for a correlated response.
        """
        correlation_id = str(uuid.uuid4())[:8]
        request.correlation_id = correlation_id

        # Send request
        await self.send(request)

        # Wait for response
        queue = self.queues.get(request.sender_id)
        if not queue:
            return None

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = await asyncio.wait_for(queue.get(), timeout=0.1)
                if (response.correlation_id == correlation_id and
                    response.message_type == MessageType.RESPONSE):
                    return response
                else:
                    # Put back unrelated messages
                    queue.put_nowait(response)
            except asyncio.TimeoutError:
                continue

        print(f"  Request timeout for {request.message_id}")
        return None


class MessagePassingAgent:
    """Agent that communicates via message passing."""

    def __init__(self, agent_id: str, bus: MessageBus):
        self.agent_id = agent_id
        self.bus = bus
        self.message_queue: Optional[Queue] = None
        self.handlers: Dict[MessageType, Callable] = {}
        self.state = AgentState.DISCONNECTED
        self._task: Optional[asyncio.Task] = None

    async def connect(self) -> None:
        """Connect to the message bus."""
        self.state = AgentState.CONNECTING
        self.message_queue = self.bus.register_agent(self.agent_id)
        self.state = AgentState.CONNECTED
        print(f"  {self.agent_id} connected to bus")

    def register_handler(
        self,
        message_type: MessageType,
        handler: Callable
    ) -> None:
        """Register a handler for a message type."""
        self.handlers[message_type] = handler

    async def send_message(
        self,
        receiver_id: str,
        message_type: MessageType,
        payload: Dict[str, Any]
    ) -> None:
        """Send a message to another agent."""
        message = Message(
            message_id=str(uuid.uuid4())[:8],
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_type=message_type,
            payload=payload
        )
        await self.bus.send(message)

    async def process_messages(self) -> None:
        """Process incoming messages."""
        if not self.message_queue:
            return

        self.state = AgentState.PROCESSING
        while self.state != AgentState.DISCONNECTED:
            try:
                message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=1.0
                )

                if message.is_expired():
                    continue

                handler = self.handlers.get(message.message_type)
                if handler:
                    await handler(message)
                else:
                    print(f"  {self.agent_id}: No handler for "
                          f"{message.message_type.value}")

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"  {self.agent_id} error: {e}")

    async def disconnect(self) -> None:
        """Disconnect from the message bus."""
        self.state = AgentState.DISCONNECTED
        print(f"  {self.agent_id} disconnected")


# ============================================================
# Example 2: Shared State Management
# ============================================================

class SharedStateManager:
    """
    Thread-safe shared state manager for multi-agent systems.
    
    Implements:
    - Read-write locks for concurrent access
    - State versioning for conflict detection
    - Change notifications
    - Atomic operations
    """

    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._version: Dict[str, int] = defaultdict(int)
        self._lock = asyncio.RLock()
        self._read_locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        self._write_lock = asyncio.Lock()
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._history: List[Dict] = []

    async def read(self, key: str) -> Any:
        """Read a value from shared state."""
        async with self._read_locks[key]:
            return self._state.get(key)

    async def write(self, key: str, value: Any, agent_id: str) -> bool:
        """Write a value to shared state with version tracking."""
        async with self._write_lock:
            old_value = self._state.get(key)
            old_version = self._version[key]

            # Optimistic concurrency check
            if key in self._state and old_version > 0:
                # Simulate version check
                pass

            self._state[key] = value
            self._version[key] += 1

            # Record history
            self._history.append({
                "key": key,
                "old_value": old_value,
                "new_value": value,
                "agent_id": agent_id,
                "version": self._version[key],
                "timestamp": datetime.now().isoformat()
            })

            # Notify listeners
            for listener in self._listeners.get(key, []):
                await listener(key, value, agent_id)

            print(f"  {agent_id} wrote to '{key}' "
                  f"(v{self._version[key]})")
            return True

    async def compare_and_swap(
        self,
        key: str,
        expected: Any,
        new_value: Any,
        agent_id: str
    ) -> bool:
        """Atomic compare-and-swap operation."""
        async with self._write_lock:
            current = self._state.get(key)
            if current == expected:
                self._state[key] = new_value
                self._version[key] += 1
                print(f"  {agent_id} CAS on '{key}': success")
                return True
            print(f"  {agent_id} CAS on '{key}': failed (expected mismatch)")
            return False

    async def atomic_update(
        self,
        key: str,
        update_fn: Callable[[Any], Any],
        agent_id: str
    ) -> Any:
        """Atomically update a value using a function."""
        async with self._write_lock:
            old_value = self._state.get(key)
            new_value = update_fn(old_value)
            self._state[key] = new_value
            self._version[key] += 1
            print(f"  {agent_id} atomic update on '{key}'")
            return new_value

    def on_change(self, key: str, listener: Callable) -> None:
        """Register a listener for state changes."""
        self._listeners[key].append(listener)

    async def get_state_snapshot(self) -> Dict[str, Any]:
        """Get a snapshot of the current state."""
        async with self._lock:
            return {
                "state": dict(self._state),
                "versions": dict(self._version),
                "history_length": len(self._history)
            }


class StatefulAgent:
    """Agent that uses shared state for coordination."""

    def __init__(self, agent_id: str, state_manager: SharedStateManager):
        self.agent_id = agent_id
        self.state_manager = state_manager
        self.local_cache: Dict[str, Any] = {}

    async def update_shared_counter(self, key: str, increment: int) -> None:
        """Atomically increment a counter in shared state."""
        def increment_fn(current: Optional[int]) -> int:
            return (current or 0) + increment

        new_value = await self.state_manager.atomic_update(
            key, increment_fn, self.agent_id
        )
        self.local_cache[key] = new_value

    async def read_and_cache(self, key: str) -> Any:
        """Read from shared state and cache locally."""
        value = await self.state_manager.read(key)
        self.local_cache[key] = value
        return value


# ============================================================
# Example 3: Event-Driven Communication
# ============================================================

class EventBus:
    """
    Event-driven communication system using publish-subscribe pattern.
    
    Supports:
    - Topic-based routing
    - Event filtering
    - Event chaining
    - Dead letter queue
    """

    def __init__(self):
        self.handlers: Dict[str, List[Tuple[str, Callable]]] = defaultdict(list)
        self.event_history: List[Dict] = []
        self.dead_letters: List[Dict] = []
        self._lock = asyncio.Lock()

    def subscribe(
        self,
        topic: str,
        handler: Callable,
        agent_id: str
    ) -> None:
        """Subscribe to an event topic."""
        self.handlers[topic].append((agent_id, handler))
        print(f"  {agent_id} subscribed to '{topic}'")

    def unsubscribe(self, topic: str, agent_id: str) -> None:
        """Unsubscribe from an event topic."""
        self.handlers[topic] = [
            (aid, h) for aid, h in self.handlers[topic]
            if aid != agent_id
        ]

    async def publish(
        self,
        topic: str,
        event_data: Dict[str, Any],
        source_agent: str
    ) -> int:
        """Publish an event to a topic."""
        async with self._lock:
            event = {
                "event_id": str(uuid.uuid4())[:8],
                "topic": topic,
                "source": source_agent,
                "data": event_data,
                "timestamp": datetime.now().isoformat()
            }
            self.event_history.append(event)

            delivered = 0
            for agent_id, handler in self.handlers.get(topic, []):
                try:
                    await handler(event)
                    delivered += 1
                except Exception as e:
                    self.dead_letters.append({
                        "event": event,
                        "error": str(e),
                        "agent_id": agent_id
                    })

            print(f"  Event '{topic}' published by {source_agent}: "
                  f"{delivered} handlers invoked")
            return delivered

    async def emit_pattern(
        self,
        pattern: str,
        event_data: Dict[str, Any],
        source_agent: str
    ) -> int:
        """Publish to all topics matching a pattern."""
        delivered = 0
        for topic in self.handlers:
            if pattern in topic:
                count = await self.publish(topic, event_data, source_agent)
                delivered += count
        return delivered


class EventDrivenAgent:
    """Agent that communicates via events."""

    def __init__(self, agent_id: str, event_bus: EventBus):
        self.agent_id = agent_id
        self.event_bus = event_bus
        self.processed_events: List[Dict] = []

    def on(self, topic: str, handler: Callable) -> None:
        """Register an event handler."""
        self.event_bus.subscribe(topic, handler, self.agent_id)

    async def emit(self, topic: str, data: Dict[str, Any]) -> int:
        """Emit an event."""
        return await self.event_bus.publish(topic, data, self.agent_id)

    async def handle_event(self, event: Dict[str, Any]) -> None:
        """Process an incoming event."""
        self.processed_events.append(event)
        print(f"  {self.agent_id} processed event: {event['topic']}")


# ============================================================
# Example 4: Agent Handshake Protocol
# ============================================================

class HandshakeProtocol:
    """
    Implements agent connection handshake protocol.
    
    Phases:
    1. INIT - Sender initiates connection
    2. CAPABILITIES - Exchange capability information
    3. ACKNOWLEDGE - Confirm connection
    4. ESTABLISHED - Connection ready
    """

    def __init__(self):
        self.connections: Dict[str, Dict] = {}
        self.handshake_log: List[Dict] = []

    async def initiate_handshake(
        self,
        initiator_id: str,
        responder_id: str,
        initiator_caps: List[str]
    ) -> bool:
        """Initiate a handshake with another agent."""
        print(f"\n  Handshake: {initiator_id} -> {responder_id}")

        # Phase 1: INIT
        init_msg = {
            "phase": "INIT",
            "sender": initiator_id,
            "receiver": responder_id,
            "timestamp": datetime.now().isoformat()
        }
        self.handshake_log.append(init_msg)
        print(f"    Phase 1: INIT sent")

        # Phase 2: CAPABILITIES
        caps_msg = {
            "phase": "CAPABILITIES",
            "sender": initiator_id,
            "receiver": responder_id,
            "capabilities": initiator_caps,
            "timestamp": datetime.now().isoformat()
        }
        self.handshake_log.append(caps_msg)
        print(f"    Phase 2: CAPABILITIES exchanged")

        # Phase 3: ACKNOWLEDGE
        ack_msg = {
            "phase": "ACKNOWLEDGE",
            "sender": responder_id,
            "receiver": initiator_id,
            "accepted": True,
            "timestamp": datetime.now().isoformat()
        }
        self.handshake_log.append(ack_msg)
        print(f"    Phase 3: ACKNOWLEDGE received")

        # Phase 4: ESTABLISHED
        self.connections[initiator_id] = {
            "peer": responder_id,
            "capabilities": initiator_caps,
            "established_at": datetime.now().isoformat()
        }
        self.connections[responder_id] = {
            "peer": initiator_id,
            "established_at": datetime.now().isoformat()
        }

        print(f"    Phase 4: ESTABLISHED")
        return True

    def get_connection(self, agent_id: str) -> Optional[Dict]:
        """Get connection info for an agent."""
        return self.connections.get(agent_id)


class HandshakeAgent:
    """Agent that uses handshake protocol for connections."""

    def __init__(self, agent_id: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.peers: Dict[str, Dict] = {}
        self.protocol = HandshakeProtocol()

    async def connect_to(self, other_agent: "HandshakeAgent") -> bool:
        """Initiate connection with another agent."""
        success = await self.protocol.initiate_handshake(
            self.agent_id,
            other_agent.agent_id,
            self.capabilities
        )

        if success:
            self.peers[other_agent.agent_id] = {
                "capabilities": other_agent.capabilities
            }

        return success


# ============================================================
# Example 5: Broadcast vs Unicast Patterns
# ============================================================

class CommunicationPatterns:
    """
    Demonstrates different communication patterns:
    - Unicast: Point-to-point
    - Multicast: One-to-many
    - Broadcast: One-to-all
    - Anycast: One-to-nearest
    """

    def __init__(self):
        self.agents: Dict[str, Dict] = {}
        self.message_log: List[Dict] = []

    def register_agent(self, agent_id: str, metadata: Dict) -> None:
        """Register an agent with metadata."""
        self.agents[agent_id] = {
            "metadata": metadata,
            "messages_received": 0,
            "last_message": None
        }

    async def unicast(
        self,
        sender_id: str,
        receiver_id: str,
        content: Dict[str, Any]
    ) -> bool:
        """Send a message to a single agent."""
        if receiver_id not in self.agents:
            print(f"  Unicast failed: {receiver_id} not found")
            return False

        self.agents[receiver_id]["messages_received"] += 1
        self.agents[receiver_id]["last_message"] = content

        self.message_log.append({
            "pattern": "unicast",
            "sender": sender_id,
            "receiver": receiver_id,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        print(f"  Unicast: {sender_id} -> {receiver_id}")
        return True

    async def multicast(
        self,
        sender_id: str,
        receiver_ids: List[str],
        content: Dict[str, Any]
    ) -> int:
        """Send a message to multiple specific agents."""
        delivered = 0
        for receiver_id in receiver_ids:
            if receiver_id in self.agents and receiver_id != sender_id:
                self.agents[receiver_id]["messages_received"] += 1
                self.agents[receiver_id]["last_message"] = content
                delivered += 1

        self.message_log.append({
            "pattern": "multicast",
            "sender": sender_id,
            "receivers": receiver_ids,
            "content": content,
            "delivered": delivered,
            "timestamp": datetime.now().isoformat()
        })

        print(f"  Multicast: {sender_id} -> {delivered} agents")
        return delivered

    async def broadcast(
        self,
        sender_id: str,
        content: Dict[str, Any]
    ) -> int:
        """Send a message to all agents."""
        delivered = 0
        for agent_id in self.agents:
            if agent_id != sender_id:
                self.agents[agent_id]["messages_received"] += 1
                self.agents[agent_id]["last_message"] = content
                delivered += 1

        self.message_log.append({
            "pattern": "broadcast",
            "sender": sender_id,
            "content": content,
            "delivered": delivered,
            "timestamp": datetime.now().isoformat()
        })

        print(f"  Broadcast: {sender_id} -> {delivered} agents")
        return delivered

    async def anycast(
        self,
        sender_id: str,
        content: Dict[str, Any],
        criteria: Callable[[Dict], bool]
    ) -> Optional[str]:
        """Send a message to one agent matching criteria."""
        for agent_id, agent_data in self.agents.items():
            if agent_id != sender_id and criteria(agent_data["metadata"]):
                agent_data["messages_received"] += 1
                agent_data["last_message"] = content

                self.message_log.append({
                    "pattern": "anycast",
                    "sender": sender_id,
                    "receiver": agent_id,
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                })

                print(f"  Anycast: {sender_id} -> {agent_id}")
                return agent_id

        print(f"  Anycast: no matching agent found")
        return None


# ============================================================
# Example 6: Complete Communication System
# ============================================================

class AgentCommunicationSystem:
    """Complete agent communication system combining all patterns."""

    def __init__(self):
        self.message_bus = MessageBus()
        self.state_manager = SharedStateManager()
        self.event_bus = EventBus()
        self.patterns = CommunicationPatterns()
        self.agents: Dict[str, MessagePassingAgent] = {}

    async def setup_agents(self) -> None:
        """Set up a team of communicating agents."""
        agent_configs = [
            ("coordinator", ["planning", "delegation"]),
            ("researcher", ["research", "analysis"]),
            ("executor", ["coding", "implementation"]),
            ("reviewer", ["review", "testing"]),
        ]

        for agent_id, caps in agent_configs:
            agent = MessagePassingAgent(agent_id, self.message_bus)
            await agent.connect()

            # Register message handlers
            agent.register_handler(
                MessageType.REQUEST,
                lambda msg: self._handle_request(msg)
            )
            agent.register_handler(
                MessageType.RESPONSE,
                lambda msg: self._handle_response(msg)
            )

            self.agents[agent_id] = agent
            self.patterns.register_agent(agent_id, {"capabilities": caps})

    async def _handle_request(self, message: Message) -> None:
        """Handle incoming request messages."""
        print(f"    Request received: {message.payload}")

    async def _handle_response(self, message: Message) -> None:
        """Handle incoming response messages."""
        print(f"    Response received: {message.payload}")

    async def run_communication_demo(self) -> None:
        """Demonstrate all communication patterns."""
        print("\n" + "="*60)
        print("AGENT COMMUNICATION DEMO")
        print("="*60)

        # Set up agents
        await self.setup_agents()

        # Start message processing tasks
        tasks = []
        for agent in self.agents.values():
            task = asyncio.create_task(agent.process_messages())
            tasks.append(task)

        # 1. Unicast
        print("\n--- Unicast Example ---")
        await self.patterns.unicast(
            "coordinator",
            "researcher",
            {"task": "Analyze market trends"}
        )

        # 2. Multicast
        print("\n--- Multicast Example ---")
        await self.patterns.multicast(
            "coordinator",
            ["researcher", "executor"],
            {"task": "Prepare project plan"}
        )

        # 3. Broadcast
        print("\n--- Broadcast Example ---")
        await self.patterns.broadcast(
            "coordinator",
            {"announcement": "System update in 5 minutes"}
        )

        # 4. Event-driven
        print("\n--- Event-Driven Example ---")
        event_agent = EventDrivenAgent("event_handler", self.event_bus)
        event_agent.on("task.completed", event_agent.handle_event)
        await event_agent.emit("task.completed", {"task_id": "t1"})

        # 5. Shared state
        print("\n--- Shared State Example ---")
        state_agent = StatefulAgent("state_user", self.state_manager)
        await state_agent.update_shared_counter("task_count", 1)
        await state_agent.read_and_cache("task_count")

        # Cleanup
        await asyncio.sleep(0.5)
        for task in tasks:
            task.cancel()

        # Print summary
        snapshot = await self.state_manager.get_state_snapshot()
        print(f"\nSystem State: {json.dumps(snapshot, indent=2)}")


# ============================================================
# Main Entry Point
# ============================================================

async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("EXERCISE 07: AGENT COMMUNICATION")
    print("="*60)

    system = AgentCommunicationSystem()
    await system.run_communication_demo()

    print("\n" + "="*60)
    print("EXERCISE COMPLETE")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
