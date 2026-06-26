// Package services contains the business logic layer.
package services

import (
	"context"
	"errors"
	"fmt"

	"golang.org/x/crypto/bcrypt"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/models"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/repository"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/tokens"
)

var (
	ErrInvalidCredentials = errors.New("invalid email or password")
	ErrEmailTaken         = errors.New("email is already registered")
	ErrUserNotFound       = errors.New("user not found")
)

// AuthService handles authentication-related operations.
type AuthService struct {
	repo  *repository.UserRepository
	tokens *tokens.Manager
}

// NewAuthService wires up the auth business logic.
func NewAuthService(repo *repository.UserRepository, tm *tokens.Manager) *AuthService {
	return &AuthService{repo: repo, tokens: tm}
}

// Register creates a new user account and returns a JWT.
func (s *AuthService) Register(ctx context.Context, email, password string) (*models.AuthResponse, error) {
	// Check if email is already taken
	existing, _ := s.repo.GetUserByEmail(ctx, email)
	if existing != nil {
		return nil, ErrEmailTaken
	}

	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, fmt.Errorf("hash password: %w", err)
	}

	user, err := s.repo.CreateUser(ctx, email, string(hash))
	if err != nil {
		return nil, fmt.Errorf("create user: %w", err)
	}

	token, err := s.tokens.GenerateToken(user.ID)
	if err != nil {
		return nil, fmt.Errorf("generate token: %w", err)
	}

	return &models.AuthResponse{Token: token, User: *user}, nil
}

// Login authenticates a user and returns a JWT.
func (s *AuthService) Login(ctx context.Context, email, password string) (*models.AuthResponse, error) {
	user, err := s.repo.GetUserByEmail(ctx, email)
	if err != nil {
		return nil, ErrInvalidCredentials
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(password)); err != nil {
		return nil, ErrInvalidCredentials
	}

	token, err := s.tokens.GenerateToken(user.ID)
	if err != nil {
		return nil, fmt.Errorf("generate token: %w", err)
	}

	return &models.AuthResponse{Token: token, User: *user}, nil
}

// ValidateToken checks that a JWT is valid and returns the user ID.
func (s *AuthService) ValidateToken(tokenStr string) (int64, error) {
	claims, err := s.tokens.ValidateToken(tokenStr)
	if err != nil {
		return 0, err
	}
	return tokens.ExtractUserID(claims)
}
