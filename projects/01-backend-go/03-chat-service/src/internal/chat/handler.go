package chat

import (
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/gorilla/websocket"
)

// Handler exposes chat HTTP + WebSocket endpoints.
type Handler struct {
	hub       *Hub
	svc       *Service
	upgrader  websocket.Upgrader
	clientCfg ClientConfig
	maxConns  int
}

// NewHandler creates a chat handler.
func NewHandler(hub *Hub, svc *Service, clientCfg ClientConfig, maxConns int) *Handler {
	return &Handler{
		hub: hub,
		svc: svc,
		upgrader: websocket.Upgrader{
			ReadBufferSize:  1024,
			WriteBufferSize: 1024,
			// CheckOrigin is permissive here; tighten to an allowlist in production.
			CheckOrigin: func(_ *http.Request) bool { return true },
		},
		clientCfg: clientCfg,
		maxConns:  maxConns,
	}
}

// Routes mounts REST routes (WebSocket is mounted separately at /ws).
func (h *Handler) Routes() chi.Router {
	r := chi.NewRouter()
	r.Get("/rooms", h.ListRooms)
	r.Post("/rooms", h.CreateRoom)
	r.Get("/rooms/{id}/messages", h.MessageHistory)
	r.Post("/rooms/{id}/join", h.JoinRoom)
	r.Post("/rooms/{id}/leave", h.LeaveRoom)
	return r
}

// ServeWS handles GET /ws/chat/:room_id — the WebSocket upgrade.
func (h *Handler) ServeWS(w http.ResponseWriter, r *http.Request) {
	roomID := chi.URLParam(r, "room_id")
	if roomID == "" {
		http.Error(w, "room_id required", http.StatusBadRequest)
		return
	}

	// Identity comes from the auth middleware / token query param.
	userID := r.URL.Query().Get("user_id")
	if userID == "" {
		userID = "anonymous"
	}
	name := r.URL.Query().Get("name")
	if name == "" {
		name = userID
	}

	if h.maxConns > 0 && h.hub.ConnectionsForUser(userID) >= h.maxConns {
		http.Error(w, "connection limit reached", http.StatusTooManyRequests)
		return
	}

	conn, err := h.upgrader.Upgrade(w, r, nil)
	if err != nil {
		slog.Warn("ws upgrade failed", "error", err)
		return
	}

	client := NewClient(h.hub, conn, h.svc, userID, name, roomID, h.clientCfg)
	h.hub.Register(client)

	// Announce arrival.
	_ = h.hub.BroadcastEvent(roomID, TypeUserJoined, map[string]string{
		"user_id": userID, "user_name": name, "room_id": roomID,
	}, client)

	go client.WritePump()
	go client.ReadPump()
}

// ListRooms handles GET /chat/rooms.
func (h *Handler) ListRooms(w http.ResponseWriter, r *http.Request) {
	rooms, err := h.svc.ListRooms(r.Context())
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to list rooms")
		return
	}
	writeJSON(w, http.StatusOK, ListRoomsResponse{Data: rooms})
}

// CreateRoom handles POST /chat/rooms.
func (h *Handler) CreateRoom(w http.ResponseWriter, r *http.Request) {
	var req CreateRoomRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	createdBy := userIDOrAnon(r)
	room, err := h.svc.CreateRoom(r.Context(), req, createdBy)
	if err != nil {
		writeChatError(w, err)
		return
	}
	writeJSON(w, http.StatusCreated, room)
}

// MessageHistory handles GET /chat/rooms/:id/messages.
func (h *Handler) MessageHistory(w http.ResponseWriter, r *http.Request) {
	roomID := chi.URLParam(r, "id")
	before := r.URL.Query().Get("before")
	limit := 0
	if v := r.URL.Query().Get("limit"); v != "" {
		limit, _ = strconv.Atoi(v)
	}
	msgs, hasMore, err := h.svc.History(r.Context(), roomID, before, limit)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to fetch history")
		return
	}
	writeJSON(w, http.StatusOK, MessageHistoryResponse{Data: msgs, HasMore: hasMore})
}

// JoinRoom handles POST /chat/rooms/:id/join.
func (h *Handler) JoinRoom(w http.ResponseWriter, r *http.Request) {
	roomID := chi.URLParam(r, "id")
	if err := h.svc.Join(r.Context(), roomID, userIDOrAnon(r)); err != nil {
		writeChatError(w, err)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// LeaveRoom handles POST /chat/rooms/:id/leave.
func (h *Handler) LeaveRoom(w http.ResponseWriter, r *http.Request) {
	roomID := chi.URLParam(r, "id")
	if err := h.svc.Leave(r.Context(), roomID, userIDOrAnon(r)); err != nil {
		writeChatError(w, err)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func userIDOrAnon(r *http.Request) string {
	if v := r.Header.Get("X-User-ID"); v != "" {
		return v
	}
	if v := r.URL.Query().Get("user_id"); v != "" {
		return v
	}
	return "anonymous"
}

func writeChatError(w http.ResponseWriter, err error) {
	switch {
	case errors.Is(err, ErrNotFound):
		writeError(w, http.StatusNotFound, "not found")
	case errors.Is(err, ErrValidation):
		writeError(w, http.StatusBadRequest, err.Error())
	default:
		writeError(w, http.StatusInternalServerError, "internal error")
	}
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, status int, msg string) {
	writeJSON(w, status, ErrorResponse{Error: msg})
}
