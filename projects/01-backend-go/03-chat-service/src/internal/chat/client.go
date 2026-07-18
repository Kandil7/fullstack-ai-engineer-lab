package chat

import (
	"context"
	"encoding/json"
	"log/slog"
	"time"

	"github.com/gorilla/websocket"
)

// Client is a single WebSocket connection belonging to a user in a room.
type Client struct {
	hub    *Hub
	conn   *websocket.Conn
	send   chan []byte
	svc    *Service
	userID string
	name   string
	roomID string

	writeWait  time.Duration
	pongWait   time.Duration
	pingPeriod time.Duration
	maxMsgSize int64
}

// ClientConfig carries the timing parameters for a client's read/write pumps.
type ClientConfig struct {
	WriteWait      time.Duration
	PongWait       time.Duration
	PingPeriod     time.Duration
	MaxMessageSize int64
}

// NewClient constructs a client bound to a hub and connection.
func NewClient(hub *Hub, conn *websocket.Conn, svc *Service, userID, name, roomID string, cfg ClientConfig) *Client {
	return &Client{
		hub:        hub,
		conn:       conn,
		send:       make(chan []byte, 64),
		svc:        svc,
		userID:     userID,
		name:       name,
		roomID:     roomID,
		writeWait:  cfg.WriteWait,
		pongWait:   cfg.PongWait,
		pingPeriod: cfg.PingPeriod,
		maxMsgSize: cfg.MaxMessageSize,
	}
}

// ReadPump reads messages from the WebSocket and processes them. It runs in its
// own goroutine and unregisters the client on return.
func (c *Client) ReadPump() {
	defer func() {
		c.hub.Unregister(c)
		_ = c.conn.Close()
	}()

	c.conn.SetReadLimit(c.maxMsgSize)
	_ = c.conn.SetReadDeadline(time.Now().Add(c.pongWait))
	c.conn.SetPongHandler(func(string) error {
		return c.conn.SetReadDeadline(time.Now().Add(c.pongWait))
	})

	for {
		_, raw, err := c.conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseNormalClosure) {
				slog.Warn("unexpected ws close", "user", c.userID, "error", err)
			}
			break
		}
		c.handleInbound(raw)
	}
}

func (c *Client) handleInbound(raw []byte) {
	var evt InboundEvent
	if err := json.Unmarshal(raw, &evt); err != nil {
		slog.Warn("bad inbound event", "user", c.userID, "error", err)
		return
	}

	switch evt.Type {
	case TypeMessage:
		c.handleMessage(evt)
	case TypeTyping:
		_ = c.hub.BroadcastEvent(c.roomID, TypeTyping, map[string]string{
			"user_id":   c.userID,
			"user_name": c.name,
			"room_id":   c.roomID,
		}, c)
	case TypeRead:
		// Read receipts are best-effort; persistence is a future enhancement.
		slog.Debug("read receipt", "user", c.userID, "message", evt.MessageID)
	default:
		slog.Warn("unknown event type", "type", evt.Type)
	}
}

func (c *Client) handleMessage(evt InboundEvent) {
	if evt.Content == "" {
		return
	}
	msg := Message{
		RoomID:     c.roomID,
		SenderID:   c.userID,
		SenderName: c.name,
		Content:    evt.Content,
		Type:       "text",
		CreatedAt:  time.Now().UTC(),
	}

	// Persist (best-effort in the scaffold; service may be nil in tests).
	if c.svc != nil {
		saved, err := c.svc.SaveMessage(context.Background(), msg)
		if err != nil {
			slog.Error("persist message failed", "error", err)
		} else {
			msg = *saved
		}
	}

	if err := c.hub.BroadcastEvent(c.roomID, TypeMessage, msg, nil); err != nil {
		slog.Error("broadcast failed", "error", err)
	}
}

// WritePump writes queued messages and periodic pings to the WebSocket.
func (c *Client) WritePump() {
	ticker := time.NewTicker(c.pingPeriod)
	defer func() {
		ticker.Stop()
		_ = c.conn.Close()
	}()

	for {
		select {
		case msg, ok := <-c.send:
			_ = c.conn.SetWriteDeadline(time.Now().Add(c.writeWait))
			if !ok {
				// Hub closed the channel.
				_ = c.conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}
			if err := c.conn.WriteMessage(websocket.TextMessage, msg); err != nil {
				return
			}
		case <-ticker.C:
			_ = c.conn.SetWriteDeadline(time.Now().Add(c.writeWait))
			if err := c.conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}
}
