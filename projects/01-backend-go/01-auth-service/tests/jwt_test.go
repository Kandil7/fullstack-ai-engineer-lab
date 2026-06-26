package tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/tokens"
)

func TestJWT_GenerateAndValidate(t *testing.T) {
	secret := "test-secret-key-for-jwt"
	expiry := 1 * time.Hour
	mgr := tokens.NewManager(secret, expiry)

	tests := []struct {
		name   string
		userID int64
	}{
		{"user id 1", 1},
		{"user id 42", 42},
		{"user id 999999", 999999},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Generate token
			tokenStr, err := mgr.GenerateToken(tt.userID)
			require.NoError(t, err)
			assert.NotEmpty(t, tokenStr)

			// Validate token
			claims, err := mgr.ValidateToken(tokenStr)
			require.NoError(t, err)
			assert.Equal(t, tt.userID, claims.UserID)
		})
	}
}

func TestJWT_ValidateInvalidToken(t *testing.T) {
	secret := "test-secret"
	mgr := tokens.NewManager(secret, 1*time.Hour)

	tests := []struct {
		name      string
		tokenStr  string
		wantError bool
	}{
		{"empty token", "", true},
		{"garbage token", "not.a.jwt", true},
		{"wrong secret", func() string {
			other := tokens.NewManager("wrong-secret", 1*time.Hour)
			tok, _ := other.GenerateToken(1)
			return tok
		}(), true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := mgr.ValidateToken(tt.tokenStr)
			if tt.wantError {
				assert.Error(t, err)
				assert.ErrorIs(t, err, tokens.ErrInvalidToken)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestJWT_ExtractUserID(t *testing.T) {
	claims := &tokens.Claims{UserID: 42}

	id, err := tokens.ExtractUserID(claims)
	require.NoError(t, err)
	assert.Equal(t, int64(42), id)

	// nil claims should error
	_, err = tokens.ExtractUserID(nil)
	assert.Error(t, err)
	assert.ErrorIs(t, err, tokens.ErrMissingClaim)
}

func TestJWT_TokenExpiry(t *testing.T) {
	// Very short expiry
	mgr := tokens.NewManager("secret", 1*time.Millisecond)

	tokenStr, err := mgr.GenerateToken(1)
	require.NoError(t, err)

	// Wait for token to expire
	time.Sleep(10 * time.Millisecond)

	_, err = mgr.ValidateToken(tokenStr)
	assert.Error(t, err)
	assert.ErrorIs(t, err, tokens.ErrInvalidToken)
}
