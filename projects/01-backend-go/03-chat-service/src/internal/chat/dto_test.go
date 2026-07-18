package chat

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestCreateRoomRequest_Validate(t *testing.T) {
	tests := []struct {
		name    string
		req     CreateRoomRequest
		wantErr bool
	}{
		{"valid", CreateRoomRequest{Name: "Math Study Group"}, false},
		{"empty name", CreateRoomRequest{Name: ""}, true},
		{"whitespace name", CreateRoomRequest{Name: "   "}, true},
		{"name too long", CreateRoomRequest{Name: strings.Repeat("x", 256)}, true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.wantErr {
				assert.Error(t, tt.req.Validate())
			} else {
				assert.NoError(t, tt.req.Validate())
			}
		})
	}
}

func TestNewOutbound_MarshalsPayload(t *testing.T) {
	evt, err := newOutbound(TypeMessage, Message{Content: "hi", RoomID: "r1"})
	require.NoError(t, err)
	assert.Equal(t, TypeMessage, evt.Type)
	assert.Contains(t, string(evt.Data), `"content":"hi"`)
}

func TestClampLimit(t *testing.T) {
	svc := NewService(nil)
	assert.Equal(t, 50, svc.ClampLimit(0))
	assert.Equal(t, 50, svc.ClampLimit(-1))
	assert.Equal(t, 30, svc.ClampLimit(30))
	assert.Equal(t, 100, svc.ClampLimit(999))
}
