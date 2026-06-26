// Package middleware provides HTTP middleware for the auth service.
package middleware

import (
	"context"
	"encoding/json"
	"net/http"
	"strings"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/models"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/services"
)

type contextKey string

// UserIDKey is the context key for the authenticated user's ID.
const UserIDKey contextKey = "user_id"

// JWTAuth returns middleware that validates JWT Bearer tokens.
func JWTAuth(auth *services.AuthService) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			header := r.Header.Get("Authorization")
			if header == "" {
				writeAuthError(w, "missing authorization header")
				return
			}

			parts := strings.SplitN(header, " ", 2)
			if len(parts) != 2 || !strings.EqualFold(parts[0], "bearer") {
				writeAuthError(w, "invalid authorization format, expected: Bearer <token>")
				return
			}

			userID, err := auth.ValidateToken(parts[1])
			if err != nil {
				writeAuthError(w, "invalid or expired token")
				return
			}

			ctx := context.WithValue(r.Context(), UserIDKey, userID)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

// GetUserID extracts the user ID from the request context.
func GetUserID(r *http.Request) (int64, bool) {
	id, ok := r.Context().Value(UserIDKey).(int64)
	return id, ok
}

func writeAuthError(w http.ResponseWriter, msg string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusUnauthorized)
	json.NewEncoder(w).Encode(models.ErrorResponse{Error: msg})
}
