// Package main is the entry point for the auth service.
package main

import (
	"context"
	"encoding/json"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/go-chi/chi/v5"

	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/config"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/database"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/handlers"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/middleware"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/repository"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/services"
	"github.com/fullstack-ai-engineer-lab/auth-service/src/internal/tokens"
)

func main() {
	// Structured logging
	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	}))

	// Load configuration
	cfg := config.Load()
	slog.Info("config loaded", "port", cfg.ServerPort)

	// Connect to database
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	db, err := database.New(ctx, cfg.DBURL)
	if err != nil {
		slog.Error("database connection failed", "error", err)
		os.Exit(1)
	}
	defer db.Close()
	slog.Info("database connected")

	// Wire up dependencies
	tokenMgr := tokens.NewManager(cfg.JWTSecret, cfg.JWTExpiry)
	userRepo := repository.NewUserRepository(db.Pool)
	authSvc := services.NewAuthService(userRepo, tokenMgr)
	userSvc := services.NewUserService(userRepo)

	authHandler := handlers.NewAuthHandler(authSvc)
	healthHandler := handlers.NewHealthHandler(db)

	// Setup routes
	r := chi.NewRouter()
	r.Use(middleware.RequestLogging)

	r.Get("/health", healthHandler.HealthCheck)

	r.Route("/auth", func(r chi.Router) {
		r.Post("/register", authHandler.HandleRegister)
		r.Post("/login", authHandler.HandleLogin)
	})

	// Protected routes
	r.Group(func(r chi.Router) {
		r.Use(middleware.JWTAuth(authSvc))

		r.Get("/users/me", func(w http.ResponseWriter, r *http.Request) {
			userID, ok := middleware.GetUserID(r)
			if !ok {
				http.Error(w, "unauthorized", http.StatusUnauthorized)
				return
			}
			user, err := userSvc.GetProfile(r.Context(), userID)
			if err != nil {
				http.Error(w, "user not found", http.StatusNotFound)
				return
			}
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(user)
		})
	})

	// Start server
	srv := &http.Server{
		Addr:         ":" + cfg.ServerPort,
		Handler:      r,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Graceful shutdown
	go func() {
		slog.Info("server starting", "addr", srv.Addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			slog.Error("server error", "error", err)
			os.Exit(1)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	slog.Info("shutting down server...")
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 15*time.Second)
	defer shutdownCancel()

	if err := srv.Shutdown(shutdownCtx); err != nil {
		slog.Error("server forced to shutdown", "error", err)
	}
	slog.Info("server stopped")
}
