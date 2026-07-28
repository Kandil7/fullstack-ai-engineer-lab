package main

import (
	"errors"
	"os"
	"testing"
)

func TestDivide(t *testing.T) {
	result, err := divide(10, 2)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 5 {
		t.Errorf("expected 5, got %f", result)
	}

	_, err = divide(10, 0)
	if err == nil {
		t.Fatal("expected error for division by zero")
	}
}

func TestSentinelErrors(t *testing.T) {
	err := doSomething()
	if !errors.Is(err, ErrNotFound) {
		t.Errorf("expected ErrNotFound, got %v", err)
	}
}

func TestErrorWrapping(t *testing.T) {
	err := processFile("nonexistent.txt")
	if err == nil {
		t.Fatal("expected error")
	}
	if !errors.Is(err, os.ErrNotExist) {
		t.Errorf("expected underlying os.ErrNotExist, got %v", err)
	}
}

func TestCustomErrorType(t *testing.T) {
	err := validateUser("")
	if err == nil {
		t.Fatal("expected validation error")
	}
	var ve *ValidationError
	if !errors.As(err, &ve) {
		t.Fatalf("expected *ValidationError, got %T", err)
	}
	if ve.Field != "email" {
		t.Errorf("expected field 'email', got %s", ve.Field)
	}
}

func TestValidateUser_Valid(t *testing.T) {
	err := validateUser("user@example.com")
	if err != nil {
		t.Errorf("expected no error, got %v", err)
	}
}

func TestErrorsJoin(t *testing.T) {
	err1 := errors.New("error 1")
	err2 := errors.New("error 2")
	combined := errors.Join(err1, err2)

	if !errors.Is(combined, err1) {
		t.Error("expected combined to contain err1")
	}
	if !errors.Is(combined, err2) {
		t.Error("expected combined to contain err2")
	}
}

func TestPanicRecover(t *testing.T) {
	// safeOperation should recover from panic
	defer func() {
		if r := recover(); r != nil {
			t.Error("expected panic to be recovered")
		}
	}()
	safeOperation()
}

func TestReadConfigError(t *testing.T) {
	err := readConfig()
	if err == nil {
		t.Fatal("expected error")
	}
	if !errors.Is(err, os.ErrNotExist) {
		t.Errorf("expected os.ErrNotExist, got %v", err)
	}
}
