package main

import (
	"context"
	"testing"
	"time"
)

func TestContextTimeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	select {
	case <-ctx.Done():
		if ctx.Err() != context.DeadlineExceeded {
			t.Errorf("expected DeadlineExceeded, got %v", ctx.Err())
		}
	case <-time.After(100 * time.Millisecond):
		t.Error("expected context to timeout")
	}
}

func TestContextCancel(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()

	select {
	case <-ctx.Done():
		if ctx.Err() != context.Canceled {
			t.Errorf("expected Canceled, got %v", ctx.Err())
		}
	default:
		t.Error("expected context to be cancelled")
	}
}

func TestContextValues(t *testing.T) {
	ctx := context.WithValue(context.Background(), "userID", 12345)
	val := ctx.Value("userID")
	if val != 12345 {
		t.Errorf("expected userID=12345, got %v", val)
	}
}

func TestContextPropagation(t *testing.T) {
	ctx := context.WithValue(context.Background(), "requestID", "req-123")
	result := step2(ctx)
	if result != "Processed: req-123" {
		t.Errorf("expected 'Processed: req-123', got %s", result)
	}
}

func TestContextCancelPropagation(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	childCtx, childCancel := context.WithCancel(ctx)
	defer childCancel()
	cancel() // Cancel parent

	select {
	case <-childCtx.Done():
		// Parent cancellation propagates to child
	default:
		t.Error("expected child context to be cancelled when parent is cancelled")
	}
}

func TestContextNotCancelled(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	select {
	case <-ctx.Done():
		t.Error("context should not be cancelled yet")
	default:
		// Expected: context is not cancelled
	}
}
