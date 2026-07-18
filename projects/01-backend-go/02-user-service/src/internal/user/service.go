package user

import (
	"context"
	"errors"
	"fmt"
)

// ErrValidation wraps input-validation failures so handlers can map them to 400.
var ErrValidation = errors.New("validation failed")

// Store is the persistence contract the service depends on.
// Defined here (where it is used) to keep the interface small and testable.
type Store interface {
	GetByID(ctx context.Context, id string) (*User, error)
	ListByCursor(ctx context.Context, cursor string, limit int) ([]User, error)
	Count(ctx context.Context) (int, error)
	UpdateProfile(ctx context.Context, id string, req UpdateProfileRequest) (*User, error)
	SoftDelete(ctx context.Context, id string) error
	GetStats(ctx context.Context, id string) (*Stats, error)
}

// Service holds user business logic.
type Service struct {
	store       Store
	defaultSize int
	maxSize     int
}

// NewService wires the user service with its store and page-size limits.
func NewService(store Store, defaultSize, maxSize int) *Service {
	return &Service{store: store, defaultSize: defaultSize, maxSize: maxSize}
}

// ClampLimit normalizes a requested page size into the allowed range.
func (s *Service) ClampLimit(requested int) int {
	if requested <= 0 {
		return s.defaultSize
	}
	if requested > s.maxSize {
		return s.maxSize
	}
	return requested
}

// Get returns a single user by ID.
func (s *Service) Get(ctx context.Context, id string) (*User, error) {
	return s.store.GetByID(ctx, id)
}

// List returns a page of users plus pagination metadata.
func (s *Service) List(ctx context.Context, cursor string, limit int) (*ListResponse, error) {
	limit = s.ClampLimit(limit)

	users, err := s.store.ListByCursor(ctx, cursor, limit)
	if err != nil {
		return nil, err
	}

	total, err := s.store.Count(ctx)
	if err != nil {
		return nil, err
	}

	page := Pagination{Total: total}
	if len(users) > limit {
		page.HasMore = true
		users = users[:limit]
	}
	if page.HasMore && len(users) > 0 {
		page.Cursor = users[len(users)-1].ID
	}

	return &ListResponse{Data: users, Pagination: page}, nil
}

// UpdateProfile validates and applies a profile update.
func (s *Service) UpdateProfile(ctx context.Context, id string, req UpdateProfileRequest) (*User, error) {
	if err := req.Validate(); err != nil {
		return nil, fmt.Errorf("%w: %s", ErrValidation, err.Error())
	}
	return s.store.UpdateProfile(ctx, id, req)
}

// Delete soft-deletes a user account.
func (s *Service) Delete(ctx context.Context, id string) error {
	return s.store.SoftDelete(ctx, id)
}

// Stats returns aggregated activity for a user.
func (s *Service) Stats(ctx context.Context, id string) (*Stats, error) {
	return s.store.GetStats(ctx, id)
}
