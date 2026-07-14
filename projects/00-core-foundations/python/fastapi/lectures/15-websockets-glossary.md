# Glossary: WebSockets

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| WebSocket | Persistent bidirectional protocol | Real-time chat |
| Upgrade | HTTP to WebSocket conversion | 101 Switching Protocols |
| Frame | WebSocket message unit | Text/Binary frame |
| Channel | Message routing abstraction | Room/Topic |
| Broadcast | Send to all connections | Chat broadcast |
| Heartbeat | Keep-alive ping/pong | Ping every 30s |
| Connection Manager | Tracks WebSocket connections | ConnectionManager class |
| Disconnect | Client leaves connection | WebSocketDisconnect |
| Room | Group of connected clients | Chat room |
| Message | Data sent over WebSocket | JSON/Text/Binary |
| Ping/Pong | Connection health check | WebSocket frames |
| Close Code | Disconnect reason | 1000 Normal, 4001 Auth |
| Binary Data | Raw bytes over WebSocket | Files, images |
| JSON Message | Structured data format | `{"type": "message"}` |
| Async | Non-blocking I/O | `async def` |

---

## Terms - Alphabetical Order

### Binary Data

**Definition:** Raw bytes transmitted over WebSocket, used for files, images, or non-text data.

**Example:**
```python
@app.websocket("/ws/binary")
async def binary_websocket(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # Receive binary data
        data = await websocket.receive_bytes()
        
        # Process binary data
        processed = process_image(data)
        
        # Send binary response
        await websocket.send_bytes(processed)

def process_image(data: bytes) -> bytes:
    # Example: add watermark, resize, etc.
    return data
```

**Client-side:**
```javascript
// Send binary
const buffer = new ArrayBuffer(8);
const view = new Uint8Array(buffer);
view[0] = 1;
ws.send(buffer);

// Receive binary
ws.onmessage = (event) => {
    if (event.data instanceof ArrayBuffer) {
        const bytes = new Uint8Array(event.data);
    }
};
```

**Related Terms:** Bytes, Frame, Binary Frame

---

### Broadcast

**Definition:** Sending a message to all connected WebSocket clients.

**Example:**
```python
from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)
    
    async def broadcast(self, message: str):
        """Send message to all connected clients"""
        for connection in self.connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to everyone
            await manager.broadcast(f"New message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

**Related Terms:** Multicast, Unicast, Connection Manager

---

### Channel

**Definition:** Logical grouping for WebSocket messages, similar to rooms or topics.

**Example:**
```python
class ChannelManager:
    def __init__(self):
        self.channels: Dict[str, Set[WebSocket]] = {}
    
    async def subscribe(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.channels:
            self.channels[channel] = set()
        self.channels[channel].add(websocket)
    
    async def unsubscribe(self, websocket: WebSocket, channel: str):
        if channel in self.channels:
            self.channels[channel].discard(websocket)
    
    async def publish(self, channel: str, message: str):
        if channel in self.channels:
            for ws in self.channels[channel]:
                await ws.send_text(message)

manager = ChannelManager()

@app.websocket("/ws/{channel}")
async def channel_websocket(websocket: WebSocket, channel: str):
    await manager.subscribe(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(channel, f"[{channel}] {data}")
    except WebSocketDisconnect:
        await manager.unsubscribe(websocket, channel)
```

**Related Terms:** Room, Topic, Pub/Sub

---

### Close Code

**Definition:** Numeric code indicating why WebSocket connection was closed.

**Example:**
```python
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect as e:
        # e.code indicates why disconnect happened
        if e.code == 1000:
            print("Normal closure")
        elif e.code == 1001:
            print("Going away")
        elif e.code == 4001:
            print("Unauthorized")
        else:
            print(f"Closed with code: {e.code}")

# Client-side close
await websocket.close(code=4001, reason="Unauthorized")
```

| Code | Meaning |
|------|---------|
| 1000 | Normal closure |
| 1001 | Going away |
| 1002 | Protocol error |
| 1003 | Unsupported data |
| 1008 | Policy violation |
| 1011 | Internal error |
| 4001 | Custom: Unauthorized |
| 4002 | Custom: Forbidden |

**Related Terms:** Disconnect, Close Frame, Error Code

---

### Connect

**Definition:** Establishing a WebSocket connection between client and server.

**Example:**
```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_connect(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()
    
    # Connection is now established
    await websocket.send_text("Connected!")
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Connection closed")

# Client connects
# ws = new WebSocket("ws://localhost:8000/ws")
# ws.onopen = () => console.log("Connected");
```

**Related Terms:** Accept, Upgrade, Connection

---

### Connection Manager

**Definition:** Class that tracks and manages WebSocket connections for broadcasting and state management.

**Example:**
```python
from typing import List, Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str = None):
        """Accept and track new connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: str = None):
        """Remove connection from tracking"""
        self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
    
    async def broadcast(self, message: str):
        """Send to all connections"""
        for connection in self.active_connections:
            await connection.send_text(message)
    
    async def send_to_user(self, user_id: str, message: str):
        """Send to specific user"""
        if user_id in self.user_connections:
            await self.user_connections[user_id].send_text(message)
    
    def get_online_users(self) -> List[str]:
        """Get list of connected users"""
        return list(self.user_connections.keys())

manager = ConnectionManager()
```

**Related Terms:** Broadcast, User Tracking, State Management

---

### Disconnect

**Definition:** Closing a WebSocket connection, either by client or server.

**Example:**
```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        # Client disconnected
        print("Client disconnected gracefully")
    except Exception as e:
        # Unexpected error
        print(f"Error: {e}")
    finally:
        # Cleanup resources
        print("Connection closed")

# Server can also close
@app.websocket("/ws/close")
async def force_close(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Closing connection")
    await websocket.close(code=1000, reason="Normal closure")
```

**Related Terms:** Close Code, WebSocketDisconnect, Cleanup

---

### Frame

**Definition:** The unit of data transmission in WebSocket protocol.

**Example:**
```
WebSocket Frame Structure:
┌─────────────────────────────────────┐
│ Fin (1 bit) - Is this final frame? │
│ RSV1-3 (3 bits) - Reserved        │
│ Opcode (4 bits) - Frame type       │
├─────────────────────────────────────┤
│ Mask (1 bit) - Is data masked?     │
│ Payload Length (7/16/64 bits)      │
├─────────────────────────────────────┤
│ Masking Key (0 or 4 bytes)         │
├─────────────────────────────────────┤
│ Payload (application data)         │
└─────────────────────────────────────┘

Opcodes:
0x0 - Continuation
0x1 - Text
0x2 - Binary
0x8 - Close
0x9 - Ping
0xA - Pong
```

**Related Terms:** Text Frame, Binary Frame, Control Frame

---

### Heartbeat

**Definition:** Periodic ping/pong messages to detect stale connections.

**Example:**
```python
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

async def heartbeat(websocket: WebSocket):
    """Send periodic pings to check connection"""
    try:
        while True:
            await asyncio.sleep(30)  # Ping every 30 seconds
            await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        pass
    except Exception:
        await websocket.close()

@app.websocket("/ws")
async def websocket_with_heartbeat(websocket: WebSocket):
    await websocket.accept()
    
    # Start heartbeat task
    heartbeat_task = asyncio.create_task(heartbeat(websocket))
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "pong":
                # Connection is alive
                continue
            
            # Handle message
            await websocket.send_json({"type": "message", "data": data})
    except WebSocketDisconnect:
        heartbeat_task.cancel()
```

**Related Terms:** Ping, Pong, Keep-Alive

---

### JSON Message

**Definition:** Structured data formatted as JSON for WebSocket communication.

**Example:**
```python
from pydantic import BaseModel
from typing import Optional

class WSMessage(BaseModel):
    type: str
    payload: Optional[dict] = None
    timestamp: Optional[str] = None

@app.websocket("/ws/json")
async def json_websocket(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # Receive JSON
        data = await websocket.receive_json()
        message = WSMessage(**data)
        
        # Process based on type
        if message.type == "chat":
            response = {
                "type": "chat_response",
                "payload": {"echo": message.payload},
                "timestamp": datetime.utcnow().isoformat()
            }
        elif message.type == "ping":
            response = {"type": "pong"}
        else:
            response = {"type": "error", "payload": {"message": "Unknown type"}}
        
        # Send JSON response
        await websocket.send_json(response)
```

**Client-side:**
```javascript
// Send JSON
ws.send(JSON.stringify({
    type: "chat",
    payload: { text: "Hello!" }
}));

// Receive JSON
ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log(message.type, message.payload);
};
```

**Related Terms:** Text, Binary, Serialization

---

### Message

**Definition:** Data sent between client and server over WebSocket connection.

**Example:**
```python
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # Receive different message types
        data = await websocket.receive()
        
        if data["type"] == "websocket.receive":
            if "text" in data:
                # Text message
                text = data["text"]
                await websocket.send_text(f"Echo: {text}")
            elif "bytes" in data:
                # Binary message
                bytes_data = data["bytes"]
                await websocket.send_bytes(bytes_data)
        elif data["type"] == "websocket.disconnect":
            break
```

**Message Types:**
- Text: String data
- Binary: Raw bytes
- JSON: Structured data

**Related Terms:** Text, Binary, JSON, Frame

---

### Ping/Pong

**Definition:** Control frames used to check WebSocket connection health.

**Example:**
```python
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    
    # FastAPI automatically responds to pings with pongs
    # But you can implement custom logic
    
    while True:
        data = await websocket.receive()
        
        if data["type"] == "websocket.receive":
            if data.get("text") == "ping":
                await websocket.send_text("pong")
            else:
                await websocket.send_text(data["text"])

# Or use built-in ping/pong
@app.websocket("/ws/auto")
async def websocket_auto(websocket: WebSocket):
    await websocket.accept()
    
    # FastAPI handles ping/pong automatically
    while True:
        message = await websocket.receive_text()
        await websocket.send_text(f"Echo: {message}")
```

**Related Terms:** Heartbeat, Keep-Alive, Control Frame

---

### Room

**Definition:** Grouping of WebSocket connections for scoped message delivery.

**Example:**
```python
from typing import Dict, Set
from fastapi import WebSocket

class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.members: Set[WebSocket] = set()
    
    async def join(self, websocket: WebSocket):
        await websocket.accept()
        self.members.add(websocket)
        await self.broadcast(f"New member joined. Members: {len(self.members)}")
    
    async def leave(self, websocket: WebSocket):
        self.members.discard(websocket)
        if self.members:
            await self.broadcast(f"Member left. Members: {len(self.members)}")
    
    async def broadcast(self, message: str):
        for member in self.members:
            await member.send_text(message)

rooms: Dict[str, Room] = {}

def get_room(room_id: str) -> Room:
    if room_id not in rooms:
        rooms[room_id] = Room(room_id)
    return rooms[room_id]

@app.websocket("/ws/room/{room_id}")
async def room_websocket(websocket: WebSocket, room_id: str):
    room = get_room(room_id)
    await room.join(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            await room.broadcast(f"[{room_id}] {data}")
    except WebSocketDisconnect:
        await room.leave(websocket)
```

**Related Terms:** Channel, Group, Broadcast

---

### Topic

**Definition:** Named subscription channel for pub/sub WebSocket messaging.

**Example:**
```python
class PubSubManager:
    def __init__(self):
        self.topics: Dict[str, Set[WebSocket]] = {}
    
    async def subscribe(self, websocket: WebSocket, topic: str):
        await websocket.accept()
        if topic not in self.topics:
            self.topics[topic] = set()
        self.topics[topic].add(websocket)
    
    async def unsubscribe(self, websocket: WebSocket, topic: str):
        if topic in self.topics:
            self.topics[topic].discard(websocket)
    
    async def publish(self, topic: str, message: str):
        if topic in self.topics:
            for ws in self.topics[topic]:
                await ws.send_text(message)

manager = PubSubManager()

@app.websocket("/ws/subscribe/{topic}")
async def subscribe(websocket: WebSocket, topic: str):
    await manager.subscribe(websocket, topic)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(topic, data)
    except WebSocketDisconnect:
        await manager.unsubscribe(websocket, topic)
```

**Related Terms:** Channel, Pub/Sub, Subscription

---

### Upgrade

**Definition:** HTTP mechanism to switch protocol from HTTP to WebSocket.

**Example:**
```
Client Request:
GET /ws HTTP/1.1
Host: localhost:8000
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

Server Response:
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

```python
# FastAPI handles upgrade automatically
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    # Connection is already upgraded at this point
    await websocket.accept()
    # ...
```

**Related Terms:** 101 Switching Protocols, HTTP, WebSocket Handshake

---

### WebSocket

**Definition:** Communication protocol providing full-duplex communication over single TCP connection.

**Example:**
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept WebSocket connection
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            # Send message
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# Client
# const ws = new WebSocket("ws://localhost:8000/ws");
# ws.onopen = () => ws.send("Hello");
# ws.onmessage = (e) => console.log(e.data);
```

**Related Terms:** Protocol, Full-Duplex, Persistent Connection

---

### WebSocketDisconnect

**Definition:** Exception raised when WebSocket client disconnects.

**Example:**
```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect as exc:
        # Access disconnect details
        code = exc.code
        reason = exc.reason
        
        print(f"Disconnected: code={code}, reason={reason}")
        
        # Cleanup
        manager.disconnect(websocket)
```

**Related Terms:** Disconnect, Exception, Close Code

---

## Code Examples Collection

### Complete WebSocket Chat

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
from datetime import datetime
import json

app = FastAPI()

class ChatManager:
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {}
        self.messages: Dict[str, List[dict]] = {}
    
    async def connect(self, websocket: WebSocket, room: str, username: str):
        await websocket.accept()
        
        if room not in self.connections:
            self.connections[room] = []
            self.messages[room] = []
        
        self.connections[room].append(websocket)
        
        # Notify room
        await self.broadcast(room, {
            "type": "join",
            "username": username,
            "timestamp": datetime.utcnow().isoformat(),
            "users": len(self.connections[room])
        })
    
    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.connections:
            self.connections[room].remove(websocket)
    
    async def broadcast(self, room: str, message: dict):
        if room in self.connections:
            self.messages[room].append(message)
            for connection in self.connections[room]:
                try:
                    await connection.send_json(message)
                except:
                    pass
    
    def get_history(self, room: str, limit: int = 50) -> List[dict]:
        return self.messages.get(room, [])[-limit:]

manager = ChatManager()

@app.websocket("/ws/chat/{room}")
async def chat(websocket: WebSocket, room: str, username: str):
    await manager.connect(websocket, room, username)
    
    # Send history
    history = manager.get_history(room)
    await websocket.send_json({"type": "history", "messages": history})
    
    try:
        while True:
            data = await websocket.receive_json()
            
            message = {
                "type": "message",
                "username": username,
                "message": data.get("message", ""),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await manager.broadcast(room, message)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.broadcast(room, {
            "type": "leave",
            "username": username,
            "timestamp": datetime.utcnow().isoformat()
        })
```

### WebSocket Authentication Middleware

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError

app = FastAPI()

SECRET_KEY = "your-secret-key"

async def authenticate_ws(token: str) -> str:
    """Validate WebSocket token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            raise ValueError("Invalid token")
        return username
    except JWTError:
        raise ValueError("Invalid token")

@app.websocket("/ws/secure")
async def secure_websocket(
    websocket: WebSocket,
    token: str = Query(...)
):
    # Authenticate before accepting
    try:
        username = await authenticate_ws(token)
    except ValueError:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    await websocket.accept()
    await websocket.send_json({"type": "welcome", "user": username})
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({
                "user": username,
                "message": data
            })
    except WebSocketDisconnect:
        print(f"{username} disconnected")
```

---

## Quick Reference Card

### WebSocket Events

```python
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    # Connection established
    await websocket.accept()
    
    while True:
        # Receive message
        data = await websocket.receive_text()  # Text
        data = await websocket.receive_bytes()  # Binary
        data = await websocket.receive_json()   # JSON
        
        # Send message
        await websocket.send_text("text")
        await websocket.send_bytes(b"binary")
        await websocket.send_json({"key": "value"})
        
        # Close connection
        await websocket.close(code=1000, reason="Done")
```

### Connection States

```
Connecting → Open → Closing → Closed
    ↓         ↓       ↓         ↓
  accept()  ready  close()  disconnected
```

### Common Close Codes

| Code | Meaning |
|------|---------|
| 1000 | Normal closure |
| 1001 | Going away |
| 1002 | Protocol error |
| 1008 | Policy violation |
| 4001 | Unauthorized |
| 4003 | Forbidden |

### Manager Pattern

```python
class ConnectionManager:
    def __init__(self):
        self.connections = []
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)
    
    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)
    
    async def broadcast(self, message: str):
        for conn in self.connections:
            await conn.send_text(message)
```
