// Package config loads service configuration from environment variables.
package config

import (
	"os"
	"time"
)

// Config holds runtime configuration for the chat service.
type Config struct {
	DBURL      string
	ServerPort string
	// WriteWait is how long to wait for a write to complete.
	WriteWait time.Duration
	// PongWait is how long to wait for the next pong from a peer.
	PongWait time.Duration
	// PingPeriod must be less than PongWait.
	PingPeriod time.Duration
	// MaxMessageSize is the maximum inbound message size in bytes.
	MaxMessageSize int64
	// MaxConnectionsPerUser caps concurrent sockets per user.
	MaxConnectionsPerUser int
}

// Load reads configuration with sensible defaults.
func Load() *Config {
	pongWait := 60 * time.Second
	return &Config{
		DBURL:                 getEnv("DB_URL", "postgres://fslab:fslab_dev_2026@localhost:5432/fslab?sslmode=disable"),
		ServerPort:            getEnv("SERVER_PORT", "8082"),
		WriteWait:             10 * time.Second,
		PongWait:              pongWait,
		PingPeriod:            (pongWait * 9) / 10,
		MaxMessageSize:        4096,
		MaxConnectionsPerUser: 5,
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
