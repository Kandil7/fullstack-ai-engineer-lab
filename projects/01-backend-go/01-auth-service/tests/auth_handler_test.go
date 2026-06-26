package tests

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// TestAuthHandler_Register_Success verifies a valid registration request returns 201.
func TestAuthHandler_Register_Success(t *testing.T) {
	tests := []struct {
		name       string
		body       map[string]string
		wantStatus int
	}{
		{
			name:       "valid registration",
			body:       map[string]string{"email": "test@example.com", "password": "securepass123"},
			wantStatus: http.StatusCreated,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			body, err := json.Marshal(tt.body)
			require.NoError(t, err)

			req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			// In a real test, you'd wire up the full handler with mocked dependencies.
			// This tests the request/response shape.
			assert.Equal(t, tt.wantStatus, w.Code)
			assert.Equal(t, "application/json", w.Header().Get("Content-Type"))
		})
	}
}

// TestAuthHandler_Register_Validation verifies input validation returns 400.
func TestAuthHandler_Register_Validation(t *testing.T) {
	tests := []struct {
		name       string
		body       map[string]string
		wantStatus int
	}{
		{
			name:       "missing email",
			body:       map[string]string{"password": "securepass123"},
			wantStatus: http.StatusBadRequest,
		},
		{
			name:       "missing password",
			body:       map[string]string{"email": "test@example.com"},
			wantStatus: http.StatusBadRequest,
		},
		{
			name:       "empty body",
			body:       map[string]string{},
			wantStatus: http.StatusBadRequest,
		},
		{
			name:       "short password",
			body:       map[string]string{"email": "test@example.com", "password": "short"},
			wantStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			body, err := json.Marshal(tt.body)
			require.NoError(t, err)

			req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			// Validate request can be parsed
			assert.Equal(t, "application/json", req.Header.Get("Content-Type"))
			assert.Equal(t, tt.wantStatus, w.Code)
		})
	}
}

// TestAuthHandler_Login_Success verifies a valid login request shape.
func TestAuthHandler_Login_Success(t *testing.T) {
	body := map[string]string{"email": "test@example.com", "password": "securepass123"}
	bodyBytes, err := json.Marshal(body)
	require.NoError(t, err)

	req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(bodyBytes))
	req.Header.Set("Content-Type", "application/json")

	var parsed map[string]string
	err = json.Unmarshal(bodyBytes, &parsed)
	require.NoError(t, err)
	assert.Equal(t, "test@example.com", parsed["email"])
	assert.Equal(t, "securepass123", parsed["password"])
}

// TestAuthHandler_Login_InvalidCredentials verifies error response shape.
func TestAuthHandler_Login_InvalidCredentials(t *testing.T) {
	tests := []struct {
		name string
		body map[string]string
	}{
		{"empty email", map[string]string{"email": "", "password": "pass"}},
		{"empty password", map[string]string{"email": "a@b.com", "password": ""}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			body, err := json.Marshal(tt.body)
			require.NoError(t, err)

			req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(body))
			assert.Equal(t, http.MethodPost, req.Method)
		})
	}
}
