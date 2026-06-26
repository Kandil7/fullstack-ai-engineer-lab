// Package repository provides data access for user entities.
package repository

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/models"
)

// UserRepository handles user persistence.
type UserRepository struct {
	pool *pgxpool.Pool
}

// NewUserRepository creates a repository backed by the given connection pool.
func NewUserRepository(pool *pgxpool.Pool) *UserRepository {
	return &UserRepository{pool: pool}
}

// CreateUser inserts a new user and returns the generated ID.
func (r *UserRepository) CreateUser(ctx context.Context, email, passwordHash string) (*models.User, error) {
	user := &models.User{}
	err := r.pool.QueryRow(ctx,
		`INSERT INTO users (email, password_hash)
		 VALUES ($1, $2)
		 RETURNING id, email, password_hash, created_at, updated_at`,
		email, passwordHash,
	).Scan(&user.ID, &user.Email, &user.PasswordHash, &user.CreatedAt, &user.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("insert user: %w", err)
	}
	return user, nil
}

// GetUserByEmail looks up a user by their email address.
func (r *UserRepository) GetUserByEmail(ctx context.Context, email string) (*models.User, error) {
	user := &models.User{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, email, password_hash, created_at, updated_at
		 FROM users WHERE email = $1`, email,
	).Scan(&user.ID, &user.Email, &user.PasswordHash, &user.CreatedAt, &user.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get user by email: %w", err)
	}
	return user, nil
}

// GetUserByID retrieves a user by primary key.
func (r *UserRepository) GetUserByID(ctx context.Context, id int64) (*models.User, error) {
	user := &models.User{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, email, password_hash, created_at, updated_at
		 FROM users WHERE id = $1`, id,
	).Scan(&user.ID, &user.Email, &user.PasswordHash, &user.CreatedAt, &user.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get user by id: %w", err)
	}
	return user, nil
}

// ListUsers returns a page of users (simple offset-based pagination).
func (r *UserRepository) ListUsers(ctx context.Context, limit, offset int) ([]models.User, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, email, password_hash, created_at, updated_at
		 FROM users ORDER BY id LIMIT $1 OFFSET $2`, limit, offset,
	)
	if err != nil {
		return nil, fmt.Errorf("list users: %w", err)
	}
	defer rows.Close()

	var users []models.User
	for rows.Next() {
		var u models.User
		if err := rows.Scan(&u.ID, &u.Email, &u.PasswordHash, &u.CreatedAt, &u.UpdatedAt); err != nil {
			return nil, fmt.Errorf("scan user: %w", err)
		}
		users = append(users, u)
	}
	return users, rows.Err()
}

// UpdateProfile updates a user's email and sets updated_at.
func (r *UserRepository) UpdateProfile(ctx context.Context, id int64, email string) (*models.User, error) {
	user := &models.User{}
	err := r.pool.QueryRow(ctx,
		`UPDATE users SET email = $1, updated_at = NOW()
		 WHERE id = $2
		 RETURNING id, email, password_hash, created_at, updated_at`,
		email, id,
	).Scan(&user.ID, &user.Email, &user.PasswordHash, &user.CreatedAt, &user.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("update profile: %w", err)
	}
	return user, nil
}
