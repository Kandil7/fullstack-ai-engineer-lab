package chat

import (
	"encoding/json"
	"log/slog"
	"sync"
)

// Hub maintains the set of active clients grouped by room and broadcasts
// messages to the members of a room. All mutation of shared state happens on
// the single run() goroutine via channels, so the maps need no external locks.
type Hub struct {
	// rooms maps a room ID to the set of clients currently in it.
	rooms map[string]map[*Client]struct{}

	register   chan *Client
	unregister chan *Client
	broadcast  chan broadcastMsg

	mu sync.RWMutex // guards rooms for read-only accessors (RoomSize/Rooms)
}

// broadcastMsg is an outbound event targeted at a room, optionally excluding
// the sender client.
type broadcastMsg struct {
	roomID  string
	payload []byte
	exclude *Client
}

// NewHub creates an unstarted hub.
func NewHub() *Hub {
	return &Hub{
		rooms:      make(map[string]map[*Client]struct{}),
		register:   make(chan *Client),
		unregister: make(chan *Client),
		broadcast:  make(chan broadcastMsg, 256),
	}
}

// Run starts the hub's event loop. It blocks until stop is closed.
func (h *Hub) Run(stop <-chan struct{}) {
	for {
		select {
		case c := <-h.register:
			h.addClient(c)
		case c := <-h.unregister:
			h.removeClient(c)
		case m := <-h.broadcast:
			h.dispatch(m)
		case <-stop:
			return
		}
	}
}

func (h *Hub) addClient(c *Client) {
	h.mu.Lock()
	defer h.mu.Unlock()
	if h.rooms[c.roomID] == nil {
		h.rooms[c.roomID] = make(map[*Client]struct{})
	}
	h.rooms[c.roomID][c] = struct{}{}
	slog.Info("client registered", "room", c.roomID, "user", c.userID)
}

func (h *Hub) removeClient(c *Client) {
	h.mu.Lock()
	defer h.mu.Unlock()
	clients, ok := h.rooms[c.roomID]
	if !ok {
		return
	}
	if _, exists := clients[c]; exists {
		delete(clients, c)
		close(c.send)
		slog.Info("client unregistered", "room", c.roomID, "user", c.userID)
	}
	if len(clients) == 0 {
		delete(h.rooms, c.roomID)
	}
}

func (h *Hub) dispatch(m broadcastMsg) {
	h.mu.RLock()
	clients := h.rooms[m.roomID]
	targets := make([]*Client, 0, len(clients))
	for c := range clients {
		if c == m.exclude {
			continue
		}
		targets = append(targets, c)
	}
	h.mu.RUnlock()

	for _, c := range targets {
		select {
		case c.send <- m.payload:
		default:
			// Slow consumer: drop and schedule removal to avoid blocking the hub.
			go func(cl *Client) { h.unregister <- cl }(c)
		}
	}
}

// Register adds a client to its room.
func (h *Hub) Register(c *Client) { h.register <- c }

// Unregister removes a client from its room.
func (h *Hub) Unregister(c *Client) { h.unregister <- c }

// Broadcast sends an already-encoded event to every client in a room.
func (h *Hub) Broadcast(roomID string, payload []byte, exclude *Client) {
	h.broadcast <- broadcastMsg{roomID: roomID, payload: payload, exclude: exclude}
}

// BroadcastEvent marshals and broadcasts a typed event to a room.
func (h *Hub) BroadcastEvent(roomID string, eventType string, data any, exclude *Client) error {
	evt, err := newOutbound(eventType, data)
	if err != nil {
		return err
	}
	payload, err := json.Marshal(evt)
	if err != nil {
		return err
	}
	h.Broadcast(roomID, payload, exclude)
	return nil
}

// RoomSize returns the number of clients currently in a room.
func (h *Hub) RoomSize(roomID string) int {
	h.mu.RLock()
	defer h.mu.RUnlock()
	return len(h.rooms[roomID])
}

// Rooms returns the count of active rooms.
func (h *Hub) Rooms() int {
	h.mu.RLock()
	defer h.mu.RUnlock()
	return len(h.rooms)
}

// ConnectionsForUser counts how many active sockets a user has across all rooms.
func (h *Hub) ConnectionsForUser(userID string) int {
	h.mu.RLock()
	defer h.mu.RUnlock()
	n := 0
	for _, clients := range h.rooms {
		for c := range clients {
			if c.userID == userID {
				n++
			}
		}
	}
	return n
}
