// Package handlers implements the HTTP handlers for the auth service.
package handlers

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/models"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/services"
)

// AuthHandler holds dependencies for auth endpoints.
type AuthHandler struct {
	auth *services.AuthService
}

// NewAuthHandler creates an auth handler.
func NewAuthHandler(auth *services.AuthService) *AuthHandler {
	return &AuthHandler{auth: auth}
}

// HandleRegister processes POST /auth/register.
func (h *AuthHandler) HandleRegister(w http.ResponseWriter, r *http.Request) {
	var req models.RegisterRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{
			Error: "invalid request body",
		})
		return
	}

	if req.Email == "" || req.Password == "" {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{
			Error: "email and password are required",
		})
		return
	}

	if len(req.Password) < 8 {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{
			Error: "password must be at least 8 characters",
		})
		return
	}

	resp, err := h.auth.Register(r.Context(), req.Email, req.Password)
	if err != nil {
		status := http.StatusInternalServerError
		if errors.Is(err, services.ErrEmailTaken) {
			status = http.StatusConflict
		}
		writeJSON(w, status, models.ErrorResponse{
			Error: err.Error(),
		})
		return
	}

	writeJSON(w, http.StatusCreated, resp)
}

// HandleLogin processes POST /auth/login.
func (h *AuthHandler) HandleLogin(w http.ResponseWriter, r *http.Request) {
	var req models.LoginRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{
			Error: "invalid request body",
		})
		return
	}

	if req.Email == "" || req.Password == "" {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{
			Error: "email and password are required",
		})
		return
	}

	resp, err := h.auth.Login(r.Context(), req.Email, req.Password)
	if err != nil {
		status := http.StatusUnauthorized
		if !errors.Is(err, services.ErrInvalidCredentials) {
			status = http.StatusInternalServerError
		}
		writeJSON(w, status, models.ErrorResponse{
			Error: "invalid credentials",
		})
		return
	}

	writeJSON(w, http.StatusOK, resp)
}

// writeJSON is a helper to write a JSON response.
func writeJSON(w http.ResponseWriter, status int, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(v)
}
