package tests

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/fullstack-ai-engineer-lab/user-service/src/internal/user"
)

// fakeStore is an in-memory implementation of user.Store for unit tests.
type fakeStore struct {
	users     []user.User
	total     int
	deleted   map[string]bool
	updateErr error
}

func newFakeStore(users []user.User) *fakeStore {
	return &fakeStore{users: users, total: len(users), deleted: map[string]bool{}}
}

func (f *fakeStore) GetByID(_ context.Context, id string) (*user.User, error) {
	for i := range f.users {
		if f.users[i].ID == id && !f.deleted[id] {
			u := f.users[i]
			return &u, nil
		}
	}
	return nil, user.ErrNotFound
}

func (f *fakeStore) ListByCursor(_ context.Context, cursor string, limit int) ([]user.User, error) {
	var out []user.User
	started := cursor == ""
	for _, u := range f.users {
		if !started {
			if u.ID == cursor {
				started = true
			}
			continue
		}
		out = append(out, u)
		if len(out) > limit {
			break
		}
	}
	return out, nil
}

func (f *fakeStore) Count(_ context.Context) (int, error) { return f.total, nil }

func (f *fakeStore) UpdateProfile(_ context.Context, id string, req user.UpdateProfileRequest) (*user.User, error) {
	if f.updateErr != nil {
		return nil, f.updateErr
	}
	for i := range f.users {
		if f.users[i].ID == id {
			f.users[i].Name = req.Name
			f.users[i].Bio = req.Bio
			f.users[i].Avatar = req.Avatar
			u := f.users[i]
			return &u, nil
		}
	}
	return nil, user.ErrNotFound
}

func (f *fakeStore) SoftDelete(_ context.Context, id string) error {
	if _, err := f.GetByID(context.Background(), id); err != nil {
		return err
	}
	f.deleted[id] = true
	return nil
}

func (f *fakeStore) GetStats(_ context.Context, id string) (*user.Stats, error) {
	if _, err := f.GetByID(context.Background(), id); err != nil {
		return nil, err
	}
	return &user.Stats{UserID: id}, nil
}

func sampleUsers() []user.User {
	return []user.User{
		{ID: "usr_001", Email: "a@x.io", Name: "Alice", Role: user.RoleStudent, IsActive: true},
		{ID: "usr_002", Email: "b@x.io", Name: "Bob", Role: user.RoleStudent, IsActive: true},
		{ID: "usr_003", Email: "c@x.io", Name: "Carol", Role: user.RoleTeacher, IsActive: true},
	}
}

func TestService_ClampLimit(t *testing.T) {
	svc := user.NewService(newFakeStore(nil), 20, 100)
	tests := []struct {
		name      string
		requested int
		want      int
	}{
		{"zero uses default", 0, 20},
		{"negative uses default", -5, 20},
		{"within range", 50, 50},
		{"over max clamped", 500, 100},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			assert.Equal(t, tt.want, svc.ClampLimit(tt.requested))
		})
	}
}

func TestService_List_Pagination(t *testing.T) {
	store := newFakeStore(sampleUsers())
	svc := user.NewService(store, 20, 100)

	t.Run("page with more results", func(t *testing.T) {
		resp, err := svc.List(context.Background(), "", 2)
		require.NoError(t, err)
		assert.Len(t, resp.Data, 2)
		assert.True(t, resp.Pagination.HasMore)
		assert.Equal(t, "usr_002", resp.Pagination.Cursor)
		assert.Equal(t, 3, resp.Pagination.Total)
	})

	t.Run("final page", func(t *testing.T) {
		resp, err := svc.List(context.Background(), "usr_002", 2)
		require.NoError(t, err)
		assert.Len(t, resp.Data, 1)
		assert.False(t, resp.Pagination.HasMore)
		assert.Empty(t, resp.Pagination.Cursor)
	})
}

func TestService_UpdateProfile_Validation(t *testing.T) {
	store := newFakeStore(sampleUsers())
	svc := user.NewService(store, 20, 100)

	t.Run("empty name rejected", func(t *testing.T) {
		_, err := svc.UpdateProfile(context.Background(), "usr_001", user.UpdateProfileRequest{Name: "  "})
		require.Error(t, err)
		assert.ErrorIs(t, err, user.ErrValidation)
	})

	t.Run("valid update applied", func(t *testing.T) {
		u, err := svc.UpdateProfile(context.Background(), "usr_001", user.UpdateProfileRequest{Name: "Alice Smith", Bio: "hi"})
		require.NoError(t, err)
		assert.Equal(t, "Alice Smith", u.Name)
	})
}

func TestService_Delete_SoftDeletes(t *testing.T) {
	store := newFakeStore(sampleUsers())
	svc := user.NewService(store, 20, 100)

	require.NoError(t, svc.Delete(context.Background(), "usr_001"))

	_, err := svc.Get(context.Background(), "usr_001")
	assert.ErrorIs(t, err, user.ErrNotFound)
}
