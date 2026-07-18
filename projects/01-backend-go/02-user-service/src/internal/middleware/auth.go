package middleware

import (
	"context"
	"net/http"
	"strings"
)

type contextKey string

// UserIDKey is the context key holding the authenticated user's ID.
const UserIDKey contextKey = "user_id"

// RequireAuth is a lightweight bearer-token gate.
//
// In production this validates a JWT issued by the auth-service (service-to-service
// verification of the shared RS256 public key). For this scaffold it only enforces
// the presence of a bearer token and stashes the raw token as the subject so
// downstream handlers can be wired to real claims later.
func RequireAuth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		header := r.Header.Get("Authorization")
		token, ok := strings.CutPrefix(header, "Bearer ")
		if !ok || strings.TrimSpace(token) == "" {
			http.Error(w, `{"error":"missing or invalid authorization header"}`, http.StatusUnauthorized)
			return
		}
		ctx := context.WithValue(r.Context(), UserIDKey, token)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// UserIDFromContext extracts the authenticated user ID, if present.
func UserIDFromContext(ctx context.Context) (string, bool) {
	id, ok := ctx.Value(UserIDKey).(string)
	return id, ok
}
