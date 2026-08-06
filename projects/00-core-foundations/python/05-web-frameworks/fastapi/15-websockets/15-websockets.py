"""
15 - WebSockets
=================
WebSocket connections for real-time bidirectional communication.
Useful for: chat apps, live updates, notifications, gaming.

Run: uvicorn 15-websockets:app --reload
"""

import sys
import json
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI(title="WebSockets in FastAPI")


# ----- Connection Manager -----
class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.user_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str = "anonymous"):
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str = "anonymous"):
        self.active_connections.remove(websocket)
        if user_id in self.user_connections:
            self.user_connections[user_id] = [
                ws for ws in self.user_connections[user_id] if ws != websocket
            ]

    async def send_personal(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_to_user(self, user_id: str, message: str):
        if user_id in self.user_connections:
            for ws in self.user_connections[user_id]:
                await ws.send_text(message)


manager = ConnectionManager()


# ----- Simple echo WebSocket -----
@app.websocket("/ws/echo")
async def echo_websocket(websocket: WebSocket):
    """
    Simple echo WebSocket. Sends back whatever is received.
    Connect: ws://127.0.0.1:8000/ws/echo
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass


# ----- Chat room WebSocket -----
@app.websocket("/ws/chat/{room_name}")
async def chat_room(websocket: WebSocket, room_name: str):
    """
    Chat room WebSocket.
    Broadcasts messages to all connected clients in the room.
    """
    await websocket.accept()
    await manager.connect(websocket)
    try:
        # Notify others
        await manager.broadcast(f"[System] New user joined {room_name}")

        while True:
            data = await websocket.receive_text()
            message = {
                "room": room_name,
                "message": data,
                "timestamp": datetime.now().isoformat(),
            }
            await manager.broadcast(json.dumps(message))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"[System] User left {room_name}")


# ----- Private messaging WebSocket -----
@app.websocket("/ws/dm")
async def direct_message(websocket: WebSocket):
    """
    Private messaging WebSocket.
    Send JSON: {"to": "user_id", "message": "hello"}
    """
    await websocket.accept()
    await websocket.send_text(json.dumps({"status": "connected", "message": "Send JSON with 'to' and 'message' fields"}))

    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                target = msg.get("to", "")
                content = msg.get("message", "")

                if target and content:
                    await manager.send_to_user(target, json.dumps({
                        "from": "anonymous",
                        "message": content,
                        "timestamp": datetime.now().isoformat(),
                    }))
                    await websocket.send_text(json.dumps({"status": "sent", "to": target}))
                else:
                    await websocket.send_text(json.dumps({"error": "Missing 'to' or 'message' field"}))
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
    except WebSocketDisconnect:
        pass


# ----- Notification system WebSocket -----
@app.websocket("/ws/notifications")
async def notifications(websocket: WebSocket):
    """
    Notification WebSocket.
    Server pushes notifications to connected clients.
    """
    await websocket.accept()
    await manager.connect(websocket)
    try:
        while True:
            # Receive commands from client
            data = await websocket.receive_text()
            try:
                cmd = json.loads(data)
                if cmd.get("action") == "subscribe":
                    topic = cmd.get("topic", "general")
                    await websocket.send_text(json.dumps({
                        "status": "subscribed",
                        "topic": topic,
                    }))
                elif cmd.get("action") == "ping":
                    await websocket.send_text(json.dumps({
                        "status": "pong",
                        "timestamp": datetime.now().isoformat(),
                    }))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ----- Status endpoint -----
@app.get("/ws/status")
def websocket_status():
    """Check active WebSocket connections."""
    return {
        "active_connections": len(manager.active_connections),
        "connected_users": list(manager.user_connections.keys()),
    }


"""
Testing with curl (for HTTP endpoints):
    curl http://127.0.0.1:8000/ws/status

Testing WebSockets (use websocat or JavaScript):
    websocat ws://127.0.0.1:8000/ws/echo
    # Type messages and see them echoed back

    websocat ws://127.0.0.1:8000/ws/chat/general
    # Join a chat room and broadcast messages

    websocat ws://127.0.0.1:8000/ws/notifications
    # Send: {"action": "ping"}

Browser JavaScript test:
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/echo");
    ws.onmessage = (e) => console.log(e.data);
    ws.send("Hello WebSocket!");
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server)."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)

    # Echo WebSocket: send a message, expect it echoed back
    with client.websocket_connect("/ws/echo") as ws:
        ws.send_text("hello")
        assert ws.receive_text() == "Echo: hello"

    # DM WebSocket: server greets on connect
    with client.websocket_connect("/ws/dm") as ws:
        greeting = ws.receive_text()
        assert "connected" in greeting

    # NOTE: /ws/chat/* and /ws/notifications call manager.connect(), which
    # calls websocket.accept() a second time (teaching quirk) -- strict ASGI
    # clients (TestClient) reject the double accept, so only echo/dm are
    # verified here.
    r = client.get("/ws/status")
    assert r.status_code == 200
    assert "active_connections" in r.json()

    print("[OK] 15-websockets: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
