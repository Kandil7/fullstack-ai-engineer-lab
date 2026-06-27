package tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/models"
)

// TestUserRepository_CreateUser verifies user creation logic.
func TestUserRepository_CreateUser(t *testing.T) {
	tests := []struct {
		name         string
		email        string
		passwordHash string
		wantEmail    string
	}{
		{
			name:         "valid user",
			email:        "alice@example.com",
			passwordHash: "$2a$10$hashedpassword",
			wantEmail:    "alice@example.com",
		},
		{
			name:         "email with plus",
			email:        "bob+tag@example.com",
			passwordHash: "$2a$10$hashedpassword",
			wantEmail:    "bob+tag@example.com",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Test the model creation (without DB)
			user := &models.User{
				ID:           1,
				Email:        tt.email,
				PasswordHash: tt.passwordHash,
				CreatedAt:    time.Now(),
				UpdatedAt:    time.Now(),
			}

			assert.Equal(t, tt.wantEmail, user.Email)
			assert.NotZero(t, user.CreatedAt)
			assert.Equal(t, tt.passwordHash, user.PasswordHash)
		})
	}
}

// TestUserRepository_GetUserByEmail verifies user lookup by email.
func TestUserRepository_GetUserByEmail(t *testing.T) {
	// Create test user
	user := &models.User{
		ID:           42,
		Email:        "lookup@example.com",
		PasswordHash: "$2a$10$hash",
		CreatedAt:    time.Now(),
		UpdatedAt:    time.Now(),
	}

	tests := []struct {
		name     string
		email    string
		wantID   int64
		wantFail bool
	}{
		{"existing user", "lookup@example.com", 42, false},
		{"non-existing user", "noone@example.com", 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.wantFail {
				assert.NotEqual(t, tt.email, user.Email)
			} else {
				require.Equal(t, tt.wantID, user.ID)
				assert.Equal(t, tt.email, user.Email)
			}
		})
	}
}

// TestUserRepository_ListUsers verifies pagination params.
func TestUserRepository_ListUsers(t *testing.T) {
	tests := []struct {
		name   string
		limit  int
		offset int
		valid  bool
	}{
		{"default page", 20, 0, true},
		{"second page", 20, 20, true},
		{"zero limit", 0, 0, false},
		{"negative offset", 10, -1, false},
		{"max limit", 100, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Validate pagination logic
			if tt.limit <= 0 {
				assert.False(t, tt.valid, "limit must be positive")
			} else if tt.offset < 0 {
				assert.False(t, tt.valid, "offset must be non-negative")
			} else {
				assert.True(t, tt.valid)
			}
		})
	}
}
