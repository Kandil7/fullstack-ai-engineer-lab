package tests

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/handlers"
)

// newRegisterRequest builds a POST /auth/register request from a JSON body.
func newRegisterRequest(t *testing.T, body any) *http.Request {
	t.Helper()
	raw, err := json.Marshal(body)
	require.NoError(t, err)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(raw))
	req.Header.Set("Content-Type", "application/json")
	return req
}

// TestAuthHandler_Register_Validation exercises the real handler on the input-validation
// paths. These return before any database call, so a nil service is safe — no DB required.
func TestAuthHandler_Register_Validation(t *testing.T) {
	// The auth service is never dereferenced on the validation path.
	h := handlers.NewAuthHandler(nil)

	tests := []struct {
		name       string
		body       map[string]string
		wantStatus int
	}{
		{"missing email", map[string]string{"password": "securepass123"}, http.StatusBadRequest},
		{"missing password", map[string]string{"email": "test@example.com"}, http.StatusBadRequest},
		{"empty body", map[string]string{}, http.StatusBadRequest},
		{"short password", map[string]string{"email": "test@example.com", "password": "short"}, http.StatusBadRequest},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := newRegisterRequest(t, tt.body)
			w := httptest.NewRecorder()

			h.HandleRegister(w, req)

			assert.Equal(t, tt.wantStatus, w.Code)
			assert.Equal(t, "application/json", w.Header().Get("Content-Type"))
		})
	}
}

// TestAuthHandler_Register_MalformedBody verifies a non-JSON body returns 400.
func TestAuthHandler_Register_MalformedBody(t *testing.T) {
	h := handlers.NewAuthHandler(nil)

	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader([]byte("{not json")))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	h.HandleRegister(w, req)

	assert.Equal(t, http.StatusBadRequest, w.Code)
	assert.Equal(t, "application/json", w.Header().Get("Content-Type"))

	var resp map[string]string
	require.NoError(t, json.NewDecoder(w.Body).Decode(&resp))
	assert.NotEmpty(t, resp["error"])
}

// TestAuthHandler_Login_Validation exercises the login handler's DB-free validation path.
func TestAuthHandler_Login_Validation(t *testing.T) {
	h := handlers.NewAuthHandler(nil)

	tests := []struct {
		name string
		body map[string]string
	}{
		{"empty email", map[string]string{"email": "", "password": "pass"}},
		{"empty password", map[string]string{"email": "a@b.com", "password": ""}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			raw, err := json.Marshal(tt.body)
			require.NoError(t, err)
			req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(raw))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			h.HandleLogin(w, req)

			assert.Equal(t, http.StatusBadRequest, w.Code)
			assert.Equal(t, "application/json", w.Header().Get("Content-Type"))
		})
	}
}
