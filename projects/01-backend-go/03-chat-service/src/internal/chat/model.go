// Package chat implements real-time messaging: domain models, hub, and handlers.
package chat

import "time"

// Room is a chat room.
type Room struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description,omitempty"`
	CreatedBy   string    `json:"created_by"`
	Members     int       `json:"members"`
	LastMessage *Message  `json:"last_message,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
}

// Message is a single chat message.
type Message struct {
	ID         string    `json:"id"`
	RoomID     string    `json:"room_id"`
	SenderID   string    `json:"sender_id"`
	SenderName string    `json:"sender_name"`
	Content    string    `json:"content"`
	Type       string    `json:"type"`
	CreatedAt  time.Time `json:"created_at"`
}

// Member is a room membership record.
type Member struct {
	RoomID   string    `json:"room_id"`
	UserID   string    `json:"user_id"`
	Role     string    `json:"role"`
	JoinedAt time.Time `json:"joined_at"`
}

// Message types exchanged over the WebSocket protocol.
const (
	TypeMessage    = "message"
	TypeTyping     = "typing"
	TypeRead       = "read"
	TypeUserJoined = "user_joined"
	TypeUserLeft   = "user_left"
)

// Member roles.
const (
	RoleOwner  = "owner"
	RoleMember = "member"
)
