# Chat Service

> Phase 01, Project 03: Real-time messaging service with WebSocket support.

## Goals

Build a chat service that handles real-time messaging between users. This service demonstrates WebSocket connections, message persistence, and real-time features essential for the ThanaweyaGPT capstone project.

**Learning outcomes:**
- WebSocket connections in Go
- Real-time message broadcasting
- Message persistence and history
- Connection management and cleanup
- Presence indicators (online/offline)
- Message delivery guarantees

## API Endpoints

### WebSocket /ws/chat/:room_id
Real-time chat connection.

```
Connection: ws://localhost:8080/ws/chat/room_abc123?token=eyJhbGciOiJSUzI1NiIs...
```

### GET /chat/rooms
List chat rooms.

```json
// Response (200)
{
  "data": [
    {
      "id": "room_abc123",
      "name": "Math Study Group",
      "members": 12,
      "last_message": {
        "content": "Can someone explain derivatives?",
        "sender": "Ahmed",
        "created_at": "2025-01-15T14:30:00Z"
      }
    }
  ]
}
```

### GET /chat/rooms/:id/messages
Get message history with pagination.

```json
// Query: ?limit=50&before=msg_xyz789

// Response (200)
{
  "data": [
    {
      "id": "msg_xyz789",
      "room_id": "room_abc123",
      "sender_id": "usr_abc123",
      "sender_name": "Ahmed",
      "content": "Can someone explain derivatives?",
      "type": "text",
      "created_at": "2025-01-15T14:30:00Z"
    }
  ],
  "has_more": true
}
```

### POST /chat/rooms
Create a new chat room.

### POST /chat/rooms/:id/join
Join a chat room.

### POST /chat/rooms/:id/leave
Leave a chat room.

## WebSocket Protocol

### Client → Server
```json
// Send message
{
  "type": "message",
  "content": "Hello everyone!",
  "room_id": "room_abc123"
}

// Typing indicator
{
  "type": "typing",
  "room_id": "room_abc123"
}

// Read receipt
{
  "type": "read",
  "message_id": "msg_xyz789"
}
```

### Server → Client
```json
// New message broadcast
{
  "type": "message",
  "data": {
    "id": "msg_def456",
    "room_id": "room_abc123",
    "sender_id": "usr_abc123",
    "sender_name": "Ahmed",
    "content": "Hello everyone!",
    "created_at": "2025-01-15T14:35:00Z"
  }
}

// User joined
{
  "type": "user_joined",
  "data": {
    "user_id": "usr_abc123",
    "user_name": "Ahmed",
    "room_id": "room_abc123"
  }
}

// Typing indicator
{
  "type": "typing",
  "data": {
    "user_id": "usr_abc123",
    "user_name": "Ahmed",
    "room_id": "room_abc123"
  }
}
```

## Project Structure

```
03-chat-service/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── chat/
│   │   ├── handler.go         # HTTP + WebSocket handlers
│   │   ├── hub.go             # Connection hub (broadcasting)
│   │   ├── client.go          # WebSocket client
│   │   ├── service.go         # Business logic
│   │   ├── repository.go      # Database queries
│   │   ├── model.go           # Domain models
│   │   └── dto.go             # Request/response types
│   ├── middleware/
│   │   ├── auth.go
│   │   └── websocket.go       # WebSocket upgrade middleware
│   └── config/
│       └── config.go
├── migrations/
│   ├── 000001_create_rooms.up.sql
│   ├── 000002_create_messages.up.sql
│   └── 000003_create_members.up.sql
├── tests/
├── Dockerfile
├── docker-compose.yml
├── go.mod
└── Makefile
```

## Database Schema

```sql
-- Chat rooms
CREATE TABLE chat_rooms (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    created_by  UUID REFERENCES users(id),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id     UUID REFERENCES chat_rooms(id),
    sender_id   UUID REFERENCES users(id),
    content     TEXT NOT NULL,
    type        VARCHAR(50) DEFAULT 'text',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ
);

-- Room members
CREATE TABLE room_members (
    room_id     UUID REFERENCES chat_rooms(id),
    user_id     UUID REFERENCES users(id),
    role        VARCHAR(50) DEFAULT 'member',
    joined_at   TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (room_id, user_id)
);

CREATE INDEX idx_messages_room_id ON messages(room_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_room_members_user_id ON room_members(user_id);
```

## Architecture

### Connection Hub Pattern
```
┌─────────────────────────────────────────────────────┐
│                    Client A                         │
│                    (WebSocket)                      │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   Hub                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ Room 1      │  │ Room 2      │  │ Room 3      │ │
│  │ [A, B, C]   │  │ [D, E]      │  │ [F, G, H]   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└───┬────────────────────┬─────────────────────┬──────┘
    │                    │                     │
┌───▼────┐          ┌────▼───┐           ┌────▼────┐
│Client B│          │Client D│           │Client F │
└────────┘          └────────┘           └─────────┘
```

### Message Flow
1. Client connects via WebSocket
2. Hub registers connection in room
3. Client sends message
4. Hub broadcasts to all room members
5. Message persisted to database
6. Read receipts tracked

## Key Features

### Presence Tracking
```go
type Presence struct {
    UserID    string
    RoomID    string
    Status    string // "online", "away", "offline"
    LastSeen  time.Time
}
```

### Message Delivery Guarantees
- **At-least-once delivery**: Messages retried on failure
- **Ordering**: Messages ordered by server timestamp
- **Deduplication**: Client-side dedup using message IDs

### Connection Management
- Heartbeat every 30 seconds
- Auto-reconnect with exponential backoff
- Connection limits per user (max 5)

## Setup

```bash
cd projects/01-backend-go/03-chat-service

# Start dependencies
docker-compose up -d

# Run migrations
make migrate-up

# Start server
make run

# Test WebSocket connection
make ws-test
```

## Status

| Milestone | Status |
|-----------|--------|
| Project structure | ✅ Complete |
| WebSocket hub | ✅ Complete |
| Room management | ✅ Complete |
| Message persistence | ✅ Complete |
| Presence tracking | ✅ Join/leave + typing broadcasts |
| Read receipts | 🔄 Protocol wired (persistence TODO) |
| Tests (hub, DTO, service) | ✅ Complete |

---

*Next: [Phase 02 - Frontend](../../02-frontend/) — Build Flutter and Next.js apps that consume these services.*
