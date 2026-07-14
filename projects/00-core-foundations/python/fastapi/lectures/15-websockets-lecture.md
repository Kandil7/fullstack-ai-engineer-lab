# Lecture 15: WebSockets in FastAPI

## Topic Overview

WebSockets provide a persistent, full-duplex communication channel between client and server over a single TCP connection. Unlike HTTP's request-response model, WebSockets allow real-time bidirectional messaging, making them ideal for chat applications, live notifications, gaming, and collaborative editing.

**Why WebSockets Matter:**
- **Real-time communication** - Instant message delivery
- **Full-duplex** - Both client and server can send messages
- **Persistent connection** - No need to repeatedly establish connections
- **Low latency** - No HTTP headers overhead per message
- **Efficient** - Less bandwidth than HTTP polling

**Common Use Cases:**
- Chat applications
- Live notifications (email, social media)
- Multiplayer games
- Collaborative document editing
- Live dashboards and metrics
- IoT device communication

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand WebSocket protocol** - How WebSockets differ from HTTP
2. **Create WebSocket endpoints** - Build real-time communication channels
3. **Handle connections** - Manage multiple client connections
4. **Implement broadcast** - Send messages to all connected clients
5. **Build chat application** - Complete real-time chat system
6. **Handle errors** - Manage disconnections and errors
7. **Secure WebSockets** - Implement authentication
8. **Scale connections** - Handle multiple server instances

---

## Key Concepts

### 1. WebSocket vs HTTP

```
HTTP (Request-Response):
Client ──GET /data──▶ Server
Client ◀──200 OK──── Server
Client ──GET /data──▶ Server  (repeated)
Client ◀──200 OK──── Server

WebSocket (Persistent):
Client ═══CONNECT═══▶ Server
Client ◀═══MESSAGE═══ Server  (bidirectional)
Client ═══MESSAGE═══▶ Server
Client ◀═══MESSAGE═══ Server
Client ◀═══MESSAGE═══ Server
Client ═══DISCONNECT═▶ Server
```

### 2. WebSocket Connection Lifecycle

```
1. Client sends HTTP upgrade request
2. Server responds with 101 Switching Protocols
3. WebSocket connection established
4. Bidirectional messaging
5. Either party can close connection
```

### 3. WebSocket Events

```
connect    → New client connection
message    → Receive message from client
disconnect → Client disconnected
error      → Error occurred
```

---

## Code Examples

### Example 1: Basic WebSocket

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Echo message back
            await websocket.send_text(f"Message: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### Example 2: WebSocket with Path Parameters

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws/{room_id}")
async def websocket_room(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await websocket.send_text(f"Connected to room: {room_id}")
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"[Room {room_id}] {data}")
    except WebSocketDisconnect:
        print(f"Client disconnected from room {room_id}")
```

### Example 3: Broadcasting to Multiple Clients

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
    
    async def send_personal(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to all clients
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Example 4: Chat Room Application

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
from pydantic import BaseModel
import json
from datetime import datetime

app = FastAPI()

class ChatRoom:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.connections: List[WebSocket] = []
        self.messages: List[dict] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        # Send message history
        for msg in self.messages[-50:]:  # Last 50 messages
            await websocket.send_json(msg)
    
    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        self.messages.append(message)
        for connection in self.connections:
            await connection.send_json(message)

class ChatManager:
    def __init__(self):
        self.rooms: Dict[str, ChatRoom] = {}
    
    def get_room(self, room_id: str) -> ChatRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id)
        return self.rooms[room_id]

chat_manager = ChatManager()

@app.websocket("/ws/chat/{room_id}")
async def chat_websocket(websocket: WebSocket, room_id: str):
    room = chat_manager.get_room(room_id)
    await room.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Create message
            message = {
                "user": data.get("user", "Anonymous"),
                "message": data.get("message", ""),
                "timestamp": datetime.utcnow().isoformat(),
                "room": room_id
            }
            
            await room.broadcast(message)
    except WebSocketDisconnect:
        room.disconnect(websocket)
```

### Example 5: WebSocket with Authentication

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError

app = FastAPI()

SECRET_KEY = "your-secret-key"

async def get_user_from_token(token: str):
    """Validate JWT token and return user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        return None

@app.websocket("/ws/secure")
async def secure_websocket(
    websocket: WebSocket,
    token: str = Query(...)
):
    # Authenticate before accepting connection
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    await websocket.accept()
    await websocket.send_json({"type": "welcome", "user": user})
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({
                "user": user,
                "message": data
            })
    except WebSocketDisconnect:
        print(f"User {user} disconnected")
```

### Example 6: WebSocket with Room Management

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

app = FastAPI()

class WebSocketManager:
    def __init__(self):
        # room_id -> set of websockets
        self.rooms: Dict[str, Set[WebSocket]] = {}
        # websocket -> user info
        self.user_info: Dict[WebSocket, dict] = {}
    
    async def join_room(self, websocket: WebSocket, room_id: str, user: str):
        await websocket.accept()
        
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        
        self.rooms[room_id].add(websocket)
        self.user_info[websocket] = {"user": user, "room": room_id}
        
        # Notify others
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user": user,
            "users": self.get_room_users(room_id)
        })
    
    async def leave_room(self, websocket: WebSocket):
        if websocket in self.user_info:
            room_id = self.user_info[websocket]["room"]
            user = self.user_info[websocket]["user"]
            
            self.rooms[room_id].discard(websocket)
            del self.user_info[websocket]
            
            if not self.rooms[room_id]:
                del self.rooms[room_id]
            else:
                await self.broadcast_to_room(room_id, {
                    "type": "user_left",
                    "user": user,
                    "users": self.get_room_users(room_id)
                })
    
    def get_room_users(self, room_id: str) -> list:
        return [
            self.user_info[ws]["user"]
            for ws in self.rooms.get(room_id, set())
            if ws in self.user_info
        ]
    
    async def broadcast_to_room(self, room_id: str, message: dict):
        for ws in self.rooms.get(room_id, set()):
            try:
                await ws.send_json(message)
            except:
                pass
    
    async def send_to_user(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

manager = WebSocketManager()

@app.websocket("/ws/chat/{room_id}")
async def chat(websocket: WebSocket, room_id: str, user: str):
    await manager.join_room(websocket, room_id, user)
    
    try:
        while True:
            data = await websocket.receive_json()
            message = {
                "type": "message",
                "user": user,
                "message": data.get("message", ""),
                "room": room_id
            }
            await manager.broadcast_to_room(room_id, message)
    except WebSocketDisconnect:
        await manager.leave_room(websocket)
```

### Example 7: Binary Data WebSocket

```python
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

@app.websocket("/ws/binary")
async def binary_websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive binary data
            data = await websocket.receive_bytes()
            
            # Process binary data
            processed = process_binary(data)
            
            # Send binary response
            await websocket.send_bytes(processed)
    except Exception as e:
        print(f"Error: {e}")

def process_binary(data: bytes) -> bytes:
    # Example: reverse bytes
    return data[::-1]

# Or with JSON for structured messages
@app.websocket("/ws/json")
async def json_websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process JSON data
            response = {
                "received": data,
                "processed": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await websocket.send_json(response)
    except Exception as e:
        print(f"Error: {e}")
```

### Example 8: WebSocket with Background Tasks

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
import asyncio
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

async def periodic_broadcast():
    """Background task that broadcasts periodically"""
    while True:
        await asyncio.sleep(10)
        timestamp = datetime.utcnow().isoformat()
        await manager.broadcast(f"Server time: {timestamp}")

@app.on_event("startup")
async def startup():
    asyncio.create_task(periodic_broadcast())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Handling Disconnections

```python
# ❌ WRONG - No disconnection handling
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()  # Crashes on disconnect
        await websocket.send_text(data)

# ✅ CORRECT - Handle disconnections
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print("Client disconnected")
```

### Mistake 2: Not Managing Connection State

```python
# ❌ WRONG - No connection tracking
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    # How do we know who's connected?
    while True:
        data = await websocket.receive_text()

# ✅ CORRECT - Track connections
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Mistake 3: Blocking the Event Loop

```python
# ❌ WRONG - Blocking operations
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # This blocks! Use async versions
        time.sleep(1)  # ❌
        result = requests.get("https://api.example.com")  # ❌
        await websocket.send_text(result)

# ✅ CORRECT - Non-blocking operations
@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Use async alternatives
        await asyncio.sleep(1)  # ✅
        async with httpx.AsyncClient() as client:
            result = await client.get("https://api.example.com")  # ✅
        await websocket.send_text(result.json())
```

---

## Best Practices

1. **Always handle disconnections** - Use try/except WebSocketDisconnect
2. **Track connections** - Maintain list of active connections
3. **Use async/await** - Never block the event loop
4. **Implement heartbeats** - Detect stale connections
5. **Add authentication** - Validate tokens before connection
6. **Limit message size** - Prevent abuse
7. **Use rooms/channels** - Organize connections logically
8. **Handle errors gracefully** - Don't crash on bad messages

---

## Practice Exercises

### Exercise 1: Real-time Notifications
Build a notification system:
- Connect users to personal notification channel
- Send notifications when events occur
- Mark notifications as read

### Exercise 2: Live Dashboard
Create a live metrics dashboard:
- Server sends updates every second
- Client displays real-time charts
- Support multiple dashboard views

### Exercise 3: Multiplayer Game
Implement a simple multiplayer game:
- Player joins game room
- Real-time position updates
- Game state synchronization

### Exercise 4: Collaborative Editor
Build a collaborative text editor:
- Multiple users edit same document
- Real-time text synchronization
- User cursors visible

### Exercise 5: Live Auction
Create a live auction system:
- Real-time bid updates
- Timer countdown
- Winner notification

---

## Summary

- **WebSockets** provide persistent, bidirectional communication
- **Connection lifecycle**: Upgrade → Connect → Messages → Disconnect
- **Use ConnectionManager** to track multiple clients
- **Always handle disconnections** gracefully
- **Never block** the event loop with sync operations
- **Add authentication** for secure connections
- **Use rooms/channels** for organized communication
- **Implement heartbeats** for connection health

---

## Further Reading

- [FastAPI WebSocket Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [WebSocket Protocol RFC 6455](https://tools.ietf.org/html/rfc6455)
- [WebSocket vs Server-Sent Events vs Polling](https://medium.com/system-design-blog/long-polling-vs-websockets-vs-server-sent-events-c43ba96df7c1)
