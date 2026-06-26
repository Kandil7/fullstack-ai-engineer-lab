// Package database provides PostgreSQL connection management.
package database

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

// Postgres wraps a pgx connection pool.
type Postgres struct {
	Pool *pgxpool.Pool
}

// New creates a connection pool with sensible defaults.
func New(ctx context.Context, dbURL string) (*Postgres, error) {
	cfg, err := pgxpool.ParseConfig(dbURL)
	if err != nil {
		return nil, fmt.Errorf("parse db url: %w", err)
	}

	cfg.MaxConns = 10
	cfg.MinConns = 2
	cfg.MaxConnLifetime = 30 * time.Minute
	cfg.MaxConnIdleTime = 5 * time.Minute

	pool, err := pgxpool.NewWithConfig(ctx, cfg)
	if err != nil {
		return nil, fmt.Errorf("create pool: %w", err)
	}

	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, fmt.Errorf("ping db: %w", err)
	}

	return &Postgres{Pool: pool}, nil
}

// Close shuts down the connection pool gracefully.
func (p *Postgres) Close() {
	if p.Pool != nil {
		p.Pool.Close()
	}
}

// Ping verifies the database is reachable.
func (p *Postgres) Ping(ctx context.Context) error {
	return p.Pool.Ping(ctx)
}
