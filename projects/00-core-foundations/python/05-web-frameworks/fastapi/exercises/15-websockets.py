"""
FastAPI Exercise 15 - WebSockets
=================================

Topics covered:
- WebSocket connections in FastAPI
- Bidirectional communication
- WebSocket rooms/channels
- Real-time data streaming

Requirements:
    pip install fastapi uvicorn websockets

Run any exercise:
    uvicorn 15-websockets:app1 --reload
    uvicorn 15-websockets:app2 --reload
    uvicorn 15-websockets:app3 --reload
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
import json


# =============================================================================
# Exercise 1: Basic WebSocket Echo
# =============================================================================
# Create a WebSocket endpoint that:
#   - Accepts connection at /ws/echo
#   - Echoes back any message received
#   - Adds "[Echo]" prefix to message
#   - Handles connection/disconnection gracefully
#
# Hints:
#   - Use @app.websocket("/ws/echo")
#   - Use websocket.accept() to accept connection
#   - Use await websocket.receive_text() to receive messages
#   - Use await websocket.send_text() to send messages
#   - Handle WebSocketDisconnect exception
#
# Expected behavior:
#   Client connects to ws://localhost:8000/ws/echo
#   Client sends: "Hello"
#   Server responds: "[Echo] Hello"
#
# Test with (using websocat or similar):
#   websocat ws://localhost:8000/ws/echo
#   > Hello
#   < [Echo] Hello
# =============================================================================

app1 = FastAPI(title="Exercise 1 - WebSocket Echo")


@app1.websocket("/ws/echo")
async def websocket_echo(websocket: WebSocket):
    # TODO: Implement echo WebSocket
    pass


# =============================================================================
# Exercise 2: WebSocket Chat Room
# =============================================================================
# Create a simple chat room:
#   - WebSocket at /ws/chat/{room_name}
#   - Each room has multiple clients
#   - When a client sends a message, broadcast to ALL clients in same room
#   - Messages format: {"username": "...", "message": "..."}
#   - Notify room when user joins/leaves
#
# Hints:
#   - Create a ChatRoomManager class to track connections
#   - Store active connections by room name
#   - Use asyncio for concurrent message handling
#   - Broadcast to all connections in a room
#
# Expected behavior:
#   Client 1 connects to /ws/chat/general
#   Client 2 connects to /ws/chat/general
#   Client 1 sends {"username": "Alice", "message": "Hi!"}
#   Both clients receive the message
#   Client 2 sends {"username": "Bob", "message": "Hello!"}
#   Both clients receive the message
#
# Test with multiple websocat terminals:
#   Terminal 1: websocat ws://localhost:8000/ws/chat/general
#   Terminal 2: websocat ws://localhost:8000/ws/chat/general
# =============================================================================

app2 = FastAPI(title="Exercise 2 - WebSocket Chat Room")


class ChatRoomManager:
    def __init__(self):
        # TODO: Initialize connection storage
        pass

    async def connect(self, websocket: WebSocket, room: str, username: str):
        # TODO: Accept connection and add to room
        pass

    def disconnect(self, websocket: WebSocket, room: str):
        # TODO: Remove connection from room
        pass

    async def broadcast(self, message: str, room: str):
        # TODO: Send message to all clients in room
        pass


chat_manager = ChatRoomManager()


@app2.websocket("/ws/chat/{room}")
async def websocket_chat(websocket: WebSocket, room: str):
    # TODO: Handle chat room connection
    pass


# =============================================================================
# Exercise 3: Real-time Notifications
# =============================================================================
# Create a notification system:
#   - WebSocket at /ws/notifications
#   - Server can push notifications to connected clients
#   - POST /notify sends a notification to ALL connected clients
#   - Notifications have types: "info", "warning", "error"
#   - Client receives: {"type": "...", "message": "...", "timestamp": "..."}
#
# Hints:
#   - Store active WebSocket connections in a list
#   - POST endpoint iterates over connections and sends
#   - Add timestamp using datetime
#   - Handle disconnections when sending
#
# Expected behavior:
#   Client connects to /ws/notifications
#   POST http://localhost:8000/notify {"type": "info", "message": "New update!"}
#   Client receives: {"type": "info", "message": "New update!", "timestamp": "..."}
#
# Test with:
#   Terminal 1: websocat ws://localhost:8000/ws/notifications
#   Terminal 2: curl -X POST http://localhost:8000/notify \
#     -H "Content-Type: application/json" \
#     -d '{"type": "info", "message": "Hello everyone!"}'
# =============================================================================

app3 = FastAPI(title="Exercise 3 - Real-time Notifications")

# TODO: Create a list to store active notification connections
active_connections: List[WebSocket] = []


class Notification(BaseModel):
    type: str
    message: str


@app3.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    # TODO: Handle notification subscription
    pass


@app3.post("/notify")
async def send_notification(notification: Notification):
    # TODO: Broadcast notification to all connected clients
    pass


# =============================================================================
# VERIFICATION CHECKLIST
# =============================================================================
# After completing the exercises:
#
# 1. Run: uvicorn 15-websockets:app1 --reload
#    - Connect with websocat
#    - Verify messages are echoed with [Echo] prefix
#
# 2. Run: uvicorn 15-websockets:app2 --reload
#    - Open two terminals with websocat
#    - Send messages from both, verify both receive
#    - Test different rooms (isolated)
#
# 3. Run: uvicorn 15-websockets:app3 --reload
#    - Connect multiple clients
#    - Send POST /notify from curl
#    - Verify all clients receive notification
# =============================================================================
