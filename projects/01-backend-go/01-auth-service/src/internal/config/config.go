// Package config loads service configuration from environment variables.
package config

import (
	"os"
	"time"
)

// Config holds all runtime configuration for the auth service.
type Config struct {
	DBURL      string
	JWTSecret  string
	JWTExpiry  time.Duration
	ServerPort string
}

// Load reads configuration from environment variables with sensible defaults.
func Load() *Config {
	return &Config{
		DBURL:      getEnv("DB_URL", "postgres://postgres:postgres@localhost:5432/auth_db?sslmode=disable"),
		JWTSecret:  getEnv("JWT_SECRET", "change-me-in-production"),
		JWTExpiry:  parseDuration(getEnv("JWT_EXPIRY", "24h")),
		ServerPort: getEnv("SERVER_PORT", "8080"),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func parseDuration(s string) time.Duration {
	d, err := time.ParseDuration(s)
	if err != nil {
		return 24 * time.Hour
	}
	return d
}
