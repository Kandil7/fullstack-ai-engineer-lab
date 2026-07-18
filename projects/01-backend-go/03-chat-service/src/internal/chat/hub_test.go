package chat

import (
	"encoding/json"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// newTestClient builds a client with a buffered send channel and no real conn.
// It is sufficient for exercising hub registration and broadcast routing.
func newTestClient(hub *Hub, userID, roomID string) *Client {
	return &Client{
		hub:    hub,
		send:   make(chan []byte, 8),
		userID: userID,
		roomID: roomID,
	}
}

func startHub(t *testing.T) (*Hub, func()) {
	t.Helper()
	hub := NewHub()
	stop := make(chan struct{})
	go hub.Run(stop)
	return hub, func() { close(stop) }
}

func TestHub_RegisterAndRoomSize(t *testing.T) {
	hub, stop := startHub(t)
	defer stop()

	a := newTestClient(hub, "u1", "room1")
	b := newTestClient(hub, "u2", "room1")
	c := newTestClient(hub, "u3", "room2")

	hub.Register(a)
	hub.Register(b)
	hub.Register(c)

	assert.Eventually(t, func() bool {
		return hub.RoomSize("room1") == 2 && hub.RoomSize("room2") == 1
	}, time.Second, 10*time.Millisecond)

	assert.Equal(t, 2, hub.Rooms())
}

func TestHub_UnregisterRemovesEmptyRoom(t *testing.T) {
	hub, stop := startHub(t)
	defer stop()

	a := newTestClient(hub, "u1", "room1")
	hub.Register(a)
	assert.Eventually(t, func() bool { return hub.RoomSize("room1") == 1 }, time.Second, 10*time.Millisecond)

	hub.Unregister(a)
	assert.Eventually(t, func() bool { return hub.RoomSize("room1") == 0 && hub.Rooms() == 0 }, time.Second, 10*time.Millisecond)
}

func TestHub_BroadcastReachesRoomMembers(t *testing.T) {
	hub, stop := startHub(t)
	defer stop()

	a := newTestClient(hub, "u1", "room1")
	b := newTestClient(hub, "u2", "room1")
	other := newTestClient(hub, "u3", "room2")
	hub.Register(a)
	hub.Register(b)
	hub.Register(other)

	assert.Eventually(t, func() bool { return hub.RoomSize("room1") == 2 }, time.Second, 10*time.Millisecond)

	msg := Message{RoomID: "room1", SenderID: "u1", Content: "hello"}
	require.NoError(t, hub.BroadcastEvent("room1", TypeMessage, msg, nil))

	// Both room1 clients receive it.
	assert.NotEmpty(t, receive(t, a))
	assert.NotEmpty(t, receive(t, b))

	// room2 client receives nothing.
	select {
	case <-other.send:
		t.Fatal("client in another room should not receive the broadcast")
	case <-time.After(100 * time.Millisecond):
	}
}

func TestHub_BroadcastExcludesSender(t *testing.T) {
	hub, stop := startHub(t)
	defer stop()

	sender := newTestClient(hub, "u1", "room1")
	receiver := newTestClient(hub, "u2", "room1")
	hub.Register(sender)
	hub.Register(receiver)
	assert.Eventually(t, func() bool { return hub.RoomSize("room1") == 2 }, time.Second, 10*time.Millisecond)

	require.NoError(t, hub.BroadcastEvent("room1", TypeTyping, map[string]string{"user_id": "u1"}, sender))

	assert.NotEmpty(t, receive(t, receiver))
	select {
	case <-sender.send:
		t.Fatal("sender should be excluded from its own typing broadcast")
	case <-time.After(100 * time.Millisecond):
	}
}

func TestHub_ConnectionsForUser(t *testing.T) {
	hub, stop := startHub(t)
	defer stop()

	hub.Register(newTestClient(hub, "u1", "room1"))
	hub.Register(newTestClient(hub, "u1", "room2"))
	hub.Register(newTestClient(hub, "u2", "room1"))

	assert.Eventually(t, func() bool { return hub.ConnectionsForUser("u1") == 2 }, time.Second, 10*time.Millisecond)
	assert.Equal(t, 1, hub.ConnectionsForUser("u2"))
	assert.Equal(t, 0, hub.ConnectionsForUser("nobody"))
}

// receive reads one payload from a client's send channel, decoding it as an event.
func receive(t *testing.T, c *Client) OutboundEvent {
	t.Helper()
	select {
	case raw := <-c.send:
		var evt OutboundEvent
		require.NoError(t, json.Unmarshal(raw, &evt))
		return evt
	case <-time.After(time.Second):
		t.Fatal("timed out waiting for broadcast")
		return OutboundEvent{}
	}
}
