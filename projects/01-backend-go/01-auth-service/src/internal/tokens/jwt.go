// Package tokens handles JWT generation, validation, and claim extraction.
package tokens

import (
	"errors"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var (
	ErrInvalidToken = errors.New("invalid or expired token")
	ErrMissingClaim = errors.New("missing expected claim")
)

// Claims extends the standard JWT claims with a user ID.
type Claims struct {
	UserID int64 `json:"user_id"`
	jwt.RegisteredClaims
}

// Manager produces and validates JWTs.
type Manager struct {
	secret []byte
	expiry time.Duration
}

// NewManager creates a token manager with the given secret and expiry.
func NewManager(secret string, expiry time.Duration) *Manager {
	return &Manager{
		secret: []byte(secret),
		expiry: expiry,
	}
}

// GenerateToken creates a signed JWT for the given user ID.
func (m *Manager) GenerateToken(userID int64) (string, error) {
	claims := Claims{
		UserID: userID,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(m.expiry)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Subject:   fmt.Sprintf("%d", userID),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(m.secret)
}

// ValidateToken parses and validates a JWT string, returning the claims.
func (m *Manager) ValidateToken(tokenStr string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenStr, &Claims{}, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
		}
		return m.secret, nil
	})
	if err != nil {
		return nil, ErrInvalidToken
	}

	claims, ok := token.Claims.(*Claims)
	if !ok || !token.Valid {
		return nil, ErrInvalidToken
	}

	return claims, nil
}

// ExtractUserID returns the user ID from validated claims.
func ExtractUserID(claims *Claims) (int64, error) {
	if claims == nil {
		return 0, ErrMissingClaim
	}
	return claims.UserID, nil
}
