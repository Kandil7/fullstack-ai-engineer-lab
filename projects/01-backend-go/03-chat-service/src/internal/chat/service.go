package chat

import (
	"context"
	"fmt"
)

// Store is the persistence contract the service depends on.
type Store interface {
	CreateRoom(ctx context.Context, name, description, createdBy string) (*Room, error)
	ListRooms(ctx context.Context) ([]Room, error)
	SaveMessage(ctx context.Context, m Message) (*Message, error)
	MessageHistory(ctx context.Context, roomID, before string, limit int) ([]Message, bool, error)
	AddMember(ctx context.Context, roomID, userID string) error
	RemoveMember(ctx context.Context, roomID, userID string) error
}

// Service holds chat business logic.
type Service struct {
	store       Store
	defaultSize int
	maxSize     int
}

// NewService wires the chat service.
func NewService(store Store) *Service {
	return &Service{store: store, defaultSize: 50, maxSize: 100}
}

// ClampLimit normalizes a requested history page size.
func (s *Service) ClampLimit(requested int) int {
	if requested <= 0 {
		return s.defaultSize
	}
	if requested > s.maxSize {
		return s.maxSize
	}
	return requested
}

// CreateRoom validates and creates a room.
func (s *Service) CreateRoom(ctx context.Context, req CreateRoomRequest, createdBy string) (*Room, error) {
	if err := req.Validate(); err != nil {
		return nil, fmt.Errorf("%w: %s", ErrValidation, err.Error())
	}
	return s.store.CreateRoom(ctx, req.Name, req.Description, createdBy)
}

// ListRooms returns all rooms.
func (s *Service) ListRooms(ctx context.Context) ([]Room, error) {
	return s.store.ListRooms(ctx)
}

// SaveMessage persists a message.
func (s *Service) SaveMessage(ctx context.Context, m Message) (*Message, error) {
	return s.store.SaveMessage(ctx, m)
}

// History returns a page of message history.
func (s *Service) History(ctx context.Context, roomID, before string, limit int) ([]Message, bool, error) {
	return s.store.MessageHistory(ctx, roomID, before, s.ClampLimit(limit))
}

// Join adds a member to a room.
func (s *Service) Join(ctx context.Context, roomID, userID string) error {
	return s.store.AddMember(ctx, roomID, userID)
}

// Leave removes a member from a room.
func (s *Service) Leave(ctx context.Context, roomID, userID string) error {
	return s.store.RemoveMember(ctx, roomID, userID)
}
