// Package config loads service configuration from environment variables.
package config

import (
	"os"
	"strconv"
)

// Config holds all runtime configuration for the user service.
type Config struct {
	DBURL          string
	ServerPort     string
	AuthServiceURL string
	DefaultPageSize int
	MaxPageSize     int
}

// Load reads configuration from environment variables with sensible defaults.
func Load() *Config {
	return &Config{
		DBURL:           getEnv("DB_URL", "postgres://fslab:fslab_dev_2026@localhost:5432/fslab?sslmode=disable"),
		ServerPort:      getEnv("SERVER_PORT", "8081"),
		AuthServiceURL:  getEnv("AUTH_SERVICE_URL", "http://localhost:8080"),
		DefaultPageSize: getEnvInt("DEFAULT_PAGE_SIZE", 20),
		MaxPageSize:     getEnvInt("MAX_PAGE_SIZE", 100),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func getEnvInt(key string, fallback int) int {
	if v := os.Getenv(key); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return fallback
}
