// Package handlers implements the HTTP handlers for the auth service.
package handlers

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/database"
)

// HealthHandler provides health check endpoints.
type HealthHandler struct {
	db *database.Postgres
}

// NewHealthHandler creates a health handler.
func NewHealthHandler(db *database.Postgres) *HealthHandler {
	return &HealthHandler{db: db}
}

// HealthCheck verifies the service and its dependencies are healthy.
func (h *HealthHandler) HealthCheck(w http.ResponseWriter, r *http.Request) {
	ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
	defer cancel()

	status := "healthy"
	dbStatus := "connected"

	if err := h.db.Ping(ctx); err != nil {
		status = "degraded"
		dbStatus = "disconnected"
	}

	resp := map[string]interface{}{
		"status":   status,
		"database": dbStatus,
	}

	if status == "healthy" {
		w.WriteHeader(http.StatusOK)
	} else {
		w.WriteHeader(http.StatusServiceUnavailable)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}
