"""
FastAPI Exercise 15 - WebSockets
==================================

Topics covered:
- WebSocket connections in FastAPI
- Echo server
- Chat room implementation
- Broadcasting messages

Requirements:
    pip install fastapi uvicorn websockets

Run:
    uvicorn 15-websockets:app --reload
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Optional
import json

app = FastAPI(title="WebSocket Exercise")


# =============================================================================
# Exercise 1: Echo WebSocket
# =============================================================================

@app.websocket("/echo")
async def echo_websocket(websocket: WebSocket):
    """Echo WebSocket - receives messages and sends them back."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("  Client disconnected from echo")


# =============================================================================
# Exercise 2: Chat Room
# =============================================================================

class ConnectionManager:
    """Manages WebSocket connections for chat rooms."""

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def send_to_room(self, room: str, message: str, sender: Optional[str] = None):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                data = {"sender": sender or "system", "message": message, "room": room}
                await connection.send_text(json.dumps(data))


manager = ConnectionManager()


@app.websocket("/chat/{room}")
async def chat_websocket(websocket: WebSocket, room: str):
    """Chat room WebSocket - users can join rooms and send messages."""
    await manager.connect(websocket, room)
    try:
        await manager.send_to_room(room, f"New user joined {room}")
        while True:
            data = await websocket.receive_text()
            await manager.send_to_room(room, data, sender="user")
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.send_to_room(room, "User left the room")


# =============================================================================
# Exercise 3: Notification Broadcasting
# =============================================================================

notification_connections: list[WebSocket] = []


@app.websocket("/notifications")
async def notification_websocket(websocket: WebSocket):
    """Notification WebSocket - subscribes to broadcast notifications."""
    await websocket.accept()
    notification_connections.append(websocket)
    try:
        await websocket.send_text(json.dumps({"type": "connected", "message": "You are subscribed to notifications"}))
        while True:
            # Keep connection alive and listen for any client messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_connections.remove(websocket)


@app.post("/broadcast")
async def broadcast_notification(message: str):
    """Broadcast a notification to all connected WebSocket clients."""
    disconnected = []
    for connection in notification_connections:
        try:
            await connection.send_text(json.dumps({"type": "notification", "message": message}))
        except Exception:
            disconnected.append(connection)
    for conn in disconnected:
        notification_connections.remove(conn)
    return {"broadcast": True, "recipients": len(notification_connections)}
