// Package main is the entry point for the user service.
package main

import (
	"context"
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/go-chi/chi/v5"

	"github.com/fullstack-ai-engineer-lab/user-service/src/internal/config"
	"github.com/fullstack-ai-engineer-lab/user-service/src/internal/database"
	"github.com/fullstack-ai-engineer-lab/user-service/src/internal/middleware"
	"github.com/fullstack-ai-engineer-lab/user-service/src/internal/user"
)

func main() {
	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	})))

	cfg := config.Load()
	slog.Info("config loaded", "port", cfg.ServerPort)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	db, err := database.New(ctx, cfg.DBURL)
	if err != nil {
		slog.Error("database connection failed", "error", err)
		os.Exit(1)
	}
	defer db.Close()
	slog.Info("database connected")

	// Wire dependencies.
	repo := user.NewRepository(db.Pool)
	svc := user.NewService(repo, cfg.DefaultPageSize, cfg.MaxPageSize)
	handler := user.NewHandler(svc)

	r := chi.NewRouter()
	r.Use(middleware.RequestLogging)

	r.Get("/health", healthCheck(db))
	r.Get("/ready", healthCheck(db))

	// Protected user routes.
	r.Group(func(pr chi.Router) {
		pr.Use(middleware.RequireAuth)
		pr.Mount("/users", handler.Routes())
	})

	srv := &http.Server{
		Addr:              ":" + cfg.ServerPort,
		Handler:           r,
		ReadHeaderTimeout: 5 * time.Second,
	}

	go func() {
		slog.Info("user service listening", "addr", srv.Addr)
		if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			slog.Error("server error", "error", err)
			os.Exit(1)
		}
	}()

	// Graceful shutdown.
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
	<-stop
	slog.Info("shutting down")

	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer shutdownCancel()
	if err := srv.Shutdown(shutdownCtx); err != nil {
		slog.Error("graceful shutdown failed", "error", err)
	}
}

func healthCheck(db *database.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		status := "ok"
		code := http.StatusOK
		if err := db.Ping(r.Context()); err != nil {
			status = "unavailable"
			code = http.StatusServiceUnavailable
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(code)
		_ = json.NewEncoder(w).Encode(map[string]string{"status": status})
	}
}
