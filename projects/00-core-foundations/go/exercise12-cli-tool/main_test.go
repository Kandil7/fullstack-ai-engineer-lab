package main

import (
	"os"
	"strings"
	"testing"
)

func TestTransformField(t *testing.T) {
	data := map[string]interface{}{
		"name": "hello",
		"age":  25,
	}

	// Upper operation
	result := transformField(data, "name", "upper", "")
	obj := result.(map[string]interface{})
	if obj["name"] != "HELLO" {
		t.Errorf("expected 'HELLO', got %v", obj["name"])
	}
}

func TestTransformFieldNested(t *testing.T) {
	data := map[string]interface{}{
		"user": map[string]interface{}{
			"name": "alice",
		},
	}
	result := transformField(data, "name", "upper", "")
	obj := result.(map[string]interface{})
	nested := obj["user"].(map[string]interface{})
	if nested["name"] != "ALICE" {
		t.Errorf("expected 'ALICE', got %v", nested["name"])
	}
}

func TestApplyOperation(t *testing.T) {
	tests := []struct {
		val      interface{}
		op       string
		value    string
		expected interface{}
	}{
		{"hello", "upper", "", "HELLO"},
		{"WORLD", "lower", "", "world"},
		{10.0, "add", "5", 15.0},
		{10.0, "multiply", "3", 30.0},
		{42, "upper", "", 42}, // non-string, no-op
	}
	for _, tt := range tests {
		result := applyOperation(tt.val, tt.op, tt.value)
		if result != tt.expected {
			t.Errorf("applyOperation(%v, %s, %s) = %v; want %v",
				tt.val, tt.op, tt.value, result, tt.expected)
		}
	}
}

func TestFilterObjects(t *testing.T) {
	data := []interface{}{
		map[string]interface{}{"name": "Alice", "status": "active"},
		map[string]interface{}{"name": "Bob", "status": "inactive"},
		map[string]interface{}{"name": "Charlie", "status": "active"},
	}

	result := filterObjects(data, "status", "active")
	if len(result) != 2 {
		t.Errorf("expected 2 active users, got %d", len(result))
	}
}

func TestAnalyzeJSON(t *testing.T) {
	data := map[string]interface{}{
		"items": []interface{}{
			map[string]interface{}{"name": "a", "count": float64(1)},
			map[string]interface{}{"name": "b", "count": float64(2), "active": true},
		},
		"metadata": map[string]interface{}{
			"version": "1.0",
			"legacy":  nil,
		},
	}

	stats := analyzeJSON(data)
	if stats["objects"] == nil || stats["objects"].(int) == 0 {
		t.Error("expected object count > 0")
	}
	if stats["strings"] == nil || stats["strings"].(int) == 0 {
		t.Error("expected string count > 0")
	}
}

func TestTransformWithArray(t *testing.T) {
	data := []interface{}{
		map[string]interface{}{"name": "one"},
		map[string]interface{}{"name": "two"},
	}
	result := transformField(data, "name", "upper", "")
	arr := result.([]interface{})
	first := arr[0].(map[string]interface{})
	second := arr[1].(map[string]interface{})
	if first["name"] != "ONE" || second["name"] != "TWO" {
		t.Errorf("expected ['ONE', 'TWO'], got [%v, %v]", first["name"], second["name"])
	}
}

func TestPrintUsage(t *testing.T) {
	// Ensure printUsage doesn't panic and produces expected content
	output := captureStdout(printUsage)
	if !strings.Contains(output, "jsontool") {
		t.Error("expected usage to mention 'jsontool'")
	}
	if !strings.Contains(output, "transform") {
		t.Error("expected usage to list 'transform' command")
	}
}

// Helper to capture stdout
func captureStdout(fn func()) string {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	fn()
	w.Close()
	var buf strings.Builder
	_, _ = io.Copy(&buf, r)
	os.Stdout = old
	return buf.String()
}
