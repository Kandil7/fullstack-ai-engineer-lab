package chat

import (
	"encoding/json"
	"errors"
	"strings"
)

// InboundEvent is a message received from a client over the WebSocket.
type InboundEvent struct {
	Type      string `json:"type"`
	Content   string `json:"content,omitempty"`
	RoomID    string `json:"room_id,omitempty"`
	MessageID string `json:"message_id,omitempty"`
}

// OutboundEvent is a message broadcast to clients.
type OutboundEvent struct {
	Type string          `json:"type"`
	Data json.RawMessage `json:"data"`
}

// CreateRoomRequest is the payload for POST /chat/rooms.
type CreateRoomRequest struct {
	Name        string `json:"name"`
	Description string `json:"description"`
}

// Validate checks the create-room payload.
func (r CreateRoomRequest) Validate() error {
	if strings.TrimSpace(r.Name) == "" {
		return errors.New("room name is required")
	}
	if len(r.Name) > 255 {
		return errors.New("room name must be 255 characters or fewer")
	}
	return nil
}

// ListRoomsResponse is the envelope for GET /chat/rooms.
type ListRoomsResponse struct {
	Data []Room `json:"data"`
}

// MessageHistoryResponse is the envelope for GET /chat/rooms/:id/messages.
type MessageHistoryResponse struct {
	Data    []Message `json:"data"`
	HasMore bool      `json:"has_more"`
}

// ErrorResponse is the standard error envelope.
type ErrorResponse struct {
	Error string `json:"error"`
}

// newOutbound builds an OutboundEvent by marshaling the payload.
func newOutbound(eventType string, payload any) (OutboundEvent, error) {
	raw, err := json.Marshal(payload)
	if err != nil {
		return OutboundEvent{}, err
	}
	return OutboundEvent{Type: eventType, Data: raw}, nil
}
