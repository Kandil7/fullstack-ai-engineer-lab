// Package services contains the business logic layer.
package services

import (
	"context"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/models"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/repository"
)

// UserService handles user profile operations.
type UserService struct {
	repo *repository.UserRepository
}

// NewUserService creates a new user service.
func NewUserService(repo *repository.UserRepository) *UserService {
	return &UserService{repo: repo}
}

// GetProfile returns a user by ID.
func (s *UserService) GetProfile(ctx context.Context, userID int64) (*models.User, error) {
	user, err := s.repo.GetUserByID(ctx, userID)
	if err != nil {
		return nil, ErrUserNotFound
	}
	return user, nil
}

// UpdateProfile updates a user's email.
func (s *UserService) UpdateProfile(ctx context.Context, userID int64, email string) (*models.User, error) {
	user, err := s.repo.UpdateProfile(ctx, userID, email)
	if err != nil {
		return nil, ErrUserNotFound
	}
	return user, nil
}

// ListUsers returns a paginated list of users.
func (s *UserService) ListUsers(ctx context.Context, limit, offset int) ([]models.User, error) {
	if limit <= 0 {
		limit = 20
	}
	if limit > 100 {
		limit = 100
	}
	if offset < 0 {
		offset = 0
	}
	return s.repo.ListUsers(ctx, limit, offset)
}
