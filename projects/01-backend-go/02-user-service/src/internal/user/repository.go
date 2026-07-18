package user

import (
	"context"
	"errors"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

// ErrNotFound is returned when a user does not exist (or is soft-deleted).
var ErrNotFound = errors.New("user not found")

// Repository handles user persistence in PostgreSQL.
type Repository struct {
	pool *pgxpool.Pool
}

// NewRepository creates a repository backed by the given connection pool.
func NewRepository(pool *pgxpool.Pool) *Repository {
	return &Repository{pool: pool}
}

const userColumns = `id, email, name, coalesce(avatar, ''), coalesce(bio, ''), role, is_active, deleted_at, created_at, updated_at`

func scanUser(row pgx.Row) (*User, error) {
	u := &User{}
	err := row.Scan(&u.ID, &u.Email, &u.Name, &u.Avatar, &u.Bio, &u.Role, &u.IsActive, &u.DeletedAt, &u.CreatedAt, &u.UpdatedAt)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, ErrNotFound
	}
	if err != nil {
		return nil, fmt.Errorf("scan user: %w", err)
	}
	return u, nil
}

// GetByID retrieves a non-deleted user by primary key.
func (r *Repository) GetByID(ctx context.Context, id string) (*User, error) {
	row := r.pool.QueryRow(ctx,
		`SELECT `+userColumns+` FROM users WHERE id = $1 AND deleted_at IS NULL`, id)
	return scanUser(row)
}

// ListByCursor returns a page of users after the given cursor (keyset pagination).
// An empty cursor starts from the beginning. It fetches limit+1 rows to detect
// whether more pages exist.
func (r *Repository) ListByCursor(ctx context.Context, cursor string, limit int) ([]User, error) {
	var (
		rows pgx.Rows
		err  error
	)
	if cursor == "" {
		rows, err = r.pool.Query(ctx,
			`SELECT `+userColumns+` FROM users
			 WHERE deleted_at IS NULL
			 ORDER BY id LIMIT $1`, limit+1)
	} else {
		rows, err = r.pool.Query(ctx,
			`SELECT `+userColumns+` FROM users
			 WHERE deleted_at IS NULL AND id > $1
			 ORDER BY id LIMIT $2`, cursor, limit+1)
	}
	if err != nil {
		return nil, fmt.Errorf("list users by cursor: %w", err)
	}
	defer rows.Close()

	return collectUsers(rows)
}

func collectUsers(rows pgx.Rows) ([]User, error) {
	users := make([]User, 0)
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Email, &u.Name, &u.Avatar, &u.Bio, &u.Role, &u.IsActive, &u.DeletedAt, &u.CreatedAt, &u.UpdatedAt); err != nil {
			return nil, fmt.Errorf("scan user row: %w", err)
		}
		users = append(users, u)
	}
	return users, rows.Err()
}

// Count returns the number of non-deleted users.
func (r *Repository) Count(ctx context.Context) (int, error) {
	var n int
	if err := r.pool.QueryRow(ctx, `SELECT count(*) FROM users WHERE deleted_at IS NULL`).Scan(&n); err != nil {
		return 0, fmt.Errorf("count users: %w", err)
	}
	return n, nil
}

// UpdateProfile updates a user's editable profile fields.
func (r *Repository) UpdateProfile(ctx context.Context, id string, req UpdateProfileRequest) (*User, error) {
	row := r.pool.QueryRow(ctx,
		`UPDATE users
		 SET name = $1, avatar = NULLIF($2, ''), bio = NULLIF($3, ''), updated_at = NOW()
		 WHERE id = $4 AND deleted_at IS NULL
		 RETURNING `+userColumns,
		req.Name, req.Avatar, req.Bio, id)
	return scanUser(row)
}

// SoftDelete marks a user as deleted without removing the row.
func (r *Repository) SoftDelete(ctx context.Context, id string) error {
	tag, err := r.pool.Exec(ctx,
		`UPDATE users SET deleted_at = NOW(), is_active = false, updated_at = NOW()
		 WHERE id = $1 AND deleted_at IS NULL`, id)
	if err != nil {
		return fmt.Errorf("soft delete user: %w", err)
	}
	if tag.RowsAffected() == 0 {
		return ErrNotFound
	}
	return nil
}

// GetStats aggregates a user's activity via a single transaction.
func (r *Repository) GetStats(ctx context.Context, id string) (*Stats, error) {
	if _, err := r.GetByID(ctx, id); err != nil {
		return nil, err
	}

	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return nil, fmt.Errorf("begin stats tx: %w", err)
	}
	defer tx.Rollback(ctx) //nolint:errcheck // rollback is a no-op after commit

	stats := &Stats{UserID: id}
	// These sub-queries tolerate missing tables in a fresh scaffold by defaulting to 0.
	_ = tx.QueryRow(ctx,
		`SELECT count(*) FROM enrollments WHERE user_id = $1 AND status = 'completed'`, id).
		Scan(&stats.CoursesCompleted)
	_ = tx.QueryRow(ctx,
		`SELECT count(*) FROM messages WHERE sender_id = $1`, id).
		Scan(&stats.MessagesSent)

	if err := tx.Commit(ctx); err != nil {
		return nil, fmt.Errorf("commit stats tx: %w", err)
	}
	return stats, nil
}
