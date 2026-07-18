package tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/fullstack-ai-engineer-lab/user-service/src/internal/user"
)

func TestUpdateProfileRequest_Validate(t *testing.T) {
	tests := []struct {
		name    string
		req     user.UpdateProfileRequest
		wantErr bool
	}{
		{"valid", user.UpdateProfileRequest{Name: "Ahmed Hassan", Bio: "CS student"}, false},
		{"empty name", user.UpdateProfileRequest{Name: ""}, true},
		{"whitespace name", user.UpdateProfileRequest{Name: "   "}, true},
		{"name too long", user.UpdateProfileRequest{Name: strings.Repeat("x", 256)}, true},
		{"bio too long", user.UpdateProfileRequest{Name: "ok", Bio: strings.Repeat("y", 2001)}, true},
		{"avatar too long", user.UpdateProfileRequest{Name: "ok", Avatar: strings.Repeat("z", 501)}, true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.req.Validate()
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestIsValidRole(t *testing.T) {
	assert.True(t, user.IsValidRole(user.RoleStudent))
	assert.True(t, user.IsValidRole(user.RoleTeacher))
	assert.True(t, user.IsValidRole(user.RoleAdmin))
	assert.False(t, user.IsValidRole("superuser"))
	assert.False(t, user.IsValidRole(""))
}
