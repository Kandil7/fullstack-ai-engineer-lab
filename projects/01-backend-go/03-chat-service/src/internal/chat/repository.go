package chat

import (
	"context"
	"errors"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

// ErrNotFound is returned when a room or message does not exist.
var ErrNotFound = errors.New("not found")

// ErrValidation wraps input-validation failures so handlers can map them to 400.
var ErrValidation = errors.New("validation failed")

// Repository handles chat persistence in PostgreSQL.
type Repository struct {
	pool *pgxpool.Pool
}

// NewRepository creates a chat repository.
func NewRepository(pool *pgxpool.Pool) *Repository {
	return &Repository{pool: pool}
}

// CreateRoom inserts a new room owned by the given user and adds them as owner.
func (r *Repository) CreateRoom(ctx context.Context, name, description, createdBy string) (*Room, error) {
	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return nil, fmt.Errorf("begin create room: %w", err)
	}
	defer tx.Rollback(ctx) //nolint:errcheck

	room := &Room{}
	err = tx.QueryRow(ctx,
		`INSERT INTO chat_rooms (name, description, created_by)
		 VALUES ($1, NULLIF($2,''), $3)
		 RETURNING id, name, coalesce(description,''), created_by, created_at`,
		name, description, createdBy).
		Scan(&room.ID, &room.Name, &room.Description, &room.CreatedBy, &room.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("insert room: %w", err)
	}

	if _, err := tx.Exec(ctx,
		`INSERT INTO room_members (room_id, user_id, role) VALUES ($1, $2, $3)`,
		room.ID, createdBy, RoleOwner); err != nil {
		return nil, fmt.Errorf("add owner membership: %w", err)
	}

	if err := tx.Commit(ctx); err != nil {
		return nil, fmt.Errorf("commit create room: %w", err)
	}
	room.Members = 1
	return room, nil
}

// ListRooms returns rooms with member counts and last message previews.
func (r *Repository) ListRooms(ctx context.Context) ([]Room, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT r.id, r.name, coalesce(r.description,''), r.created_by, r.created_at,
		        (SELECT count(*) FROM room_members m WHERE m.room_id = r.id) AS members
		 FROM chat_rooms r
		 ORDER BY r.created_at DESC`)
	if err != nil {
		return nil, fmt.Errorf("list rooms: %w", err)
	}
	defer rows.Close()

	rooms := make([]Room, 0)
	for rows.Next() {
		var rm Room
		if err := rows.Scan(&rm.ID, &rm.Name, &rm.Description, &rm.CreatedBy, &rm.CreatedAt, &rm.Members); err != nil {
			return nil, fmt.Errorf("scan room: %w", err)
		}
		rooms = append(rooms, rm)
	}
	return rooms, rows.Err()
}

// SaveMessage persists a chat message and returns it with generated fields.
func (r *Repository) SaveMessage(ctx context.Context, m Message) (*Message, error) {
	saved := m
	err := r.pool.QueryRow(ctx,
		`INSERT INTO messages (room_id, sender_id, content, type)
		 VALUES ($1, $2, $3, $4)
		 RETURNING id, created_at`,
		m.RoomID, m.SenderID, m.Content, m.Type).
		Scan(&saved.ID, &saved.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("save message: %w", err)
	}
	return &saved, nil
}

// MessageHistory returns messages for a room, newest first, before an optional
// cursor. It fetches limit+1 rows to compute has_more.
func (r *Repository) MessageHistory(ctx context.Context, roomID, before string, limit int) ([]Message, bool, error) {
	var (
		rows pgx.Rows
		err  error
	)
	if before == "" {
		rows, err = r.pool.Query(ctx,
			`SELECT id, room_id, sender_id, content, type, created_at
			 FROM messages WHERE room_id = $1 AND deleted_at IS NULL
			 ORDER BY created_at DESC LIMIT $2`, roomID, limit+1)
	} else {
		rows, err = r.pool.Query(ctx,
			`SELECT id, room_id, sender_id, content, type, created_at
			 FROM messages
			 WHERE room_id = $1 AND deleted_at IS NULL
			   AND created_at < (SELECT created_at FROM messages WHERE id = $2)
			 ORDER BY created_at DESC LIMIT $3`, roomID, before, limit+1)
	}
	if err != nil {
		return nil, false, fmt.Errorf("message history: %w", err)
	}
	defer rows.Close()

	msgs := make([]Message, 0)
	for rows.Next() {
		var m Message
		if err := rows.Scan(&m.ID, &m.RoomID, &m.SenderID, &m.Content, &m.Type, &m.CreatedAt); err != nil {
			return nil, false, fmt.Errorf("scan message: %w", err)
		}
		msgs = append(msgs, m)
	}
	if err := rows.Err(); err != nil {
		return nil, false, err
	}

	hasMore := len(msgs) > limit
	if hasMore {
		msgs = msgs[:limit]
	}
	return msgs, hasMore, nil
}

// AddMember adds a user to a room (idempotent).
func (r *Repository) AddMember(ctx context.Context, roomID, userID string) error {
	_, err := r.pool.Exec(ctx,
		`INSERT INTO room_members (room_id, user_id, role) VALUES ($1, $2, $3)
		 ON CONFLICT (room_id, user_id) DO NOTHING`,
		roomID, userID, RoleMember)
	if err != nil {
		return fmt.Errorf("add member: %w", err)
	}
	return nil
}

// RemoveMember removes a user from a room.
func (r *Repository) RemoveMember(ctx context.Context, roomID, userID string) error {
	_, err := r.pool.Exec(ctx,
		`DELETE FROM room_members WHERE room_id = $1 AND user_id = $2`, roomID, userID)
	if err != nil {
		return fmt.Errorf("remove member: %w", err)
	}
	return nil
}
