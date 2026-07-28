package main

import (
	"encoding/json"
	"os"
	"strings"
	"testing"
)

func TestFileWriteAndRead(t *testing.T) {
	content := "Test file content"
	tmpFile := "test_output.txt"
	defer os.Remove(tmpFile)

	err := os.WriteFile(tmpFile, []byte(content), 0644)
	if err != nil {
		t.Fatalf("failed to write file: %v", err)
	}

	data, err := os.ReadFile(tmpFile)
	if err != nil {
		t.Fatalf("failed to read file: %v", err)
	}

	if string(data) != content {
		t.Errorf("expected %q, got %q", content, string(data))
	}
}

func TestJSONMarshal(t *testing.T) {
	type Person struct {
		Name  string   `json:"name"`
		Age   int      `json:"age"`
		Email string   `json:"email,omitempty"`
		Tags  []string `json:"tags"`
	}

	p := Person{
		Name: "Alice",
		Age:  30,
		Tags: []string{"go", "json"},
	}

	jsonData, err := json.Marshal(p)
	if err != nil {
		t.Fatalf("marshal error: %v", err)
	}

	var result Person
	err = json.Unmarshal(jsonData, &result)
	if err != nil {
		t.Fatalf("unmarshal error: %v", err)
	}

	if result.Name != "Alice" || result.Age != 30 {
		t.Errorf("unmarshal gave %+v, want Name=Alice Age=30", result)
	}
}

func TestJSONMarshalIndent(t *testing.T) {
	type Item struct {
		ID   int    `json:"id"`
		Name string `json:"name"`
	}
	item := Item{ID: 1, Name: "test"}

	pretty, err := json.MarshalIndent(item, "", "  ")
	if err != nil {
		t.Fatalf("marshal error: %v", err)
	}

	if !strings.Contains(string(pretty), "\n") {
		t.Error("expected indented JSON to contain newlines")
	}
	if !strings.Contains(string(pretty), "  ") {
		t.Error("expected indented JSON to contain spaces")
	}
}

func TestJSONStreaming(t *testing.T) {
	multiJSON := `{"name":"Charlie","age":35}
{"name":"Diana","age":28}`

	type Person struct {
		Name string `json:"name"`
		Age  int    `json:"age"`
	}

	decoder := json.NewDecoder(strings.NewReader(multiJSON))
	var count int
	for {
		var person Person
		err := decoder.Decode(&person)
		if err != nil {
			break
		}
		count++
		if person.Name == "" {
			t.Error("expected non-empty name")
		}
	}
	if count != 2 {
		t.Errorf("expected 2 objects, got %d", count)
	}
}

func TestCustomJSONMarshaling(t *testing.T) {
	e := Event{ID: 1, Time: CustomTime{Value: "2024-01-15T10:30:00Z"}}

	jsonBytes, err := json.Marshal(e)
	if err != nil {
		t.Fatalf("marshal error: %v", err)
	}

	var result Event
	err = json.Unmarshal(jsonBytes, &result)
	if err != nil {
		t.Fatalf("unmarshal error: %v", err)
	}

	if result.ID != 1 || result.Time.Value != "2024-01-15T10:30:00Z" {
		t.Errorf("custom marshal/unmarshal gave %+v, want ID=1 Time=2024-01-15T10:30:00Z", result)
	}
}

func TestTempFile(t *testing.T) {
	tmpFile, err := os.CreateTemp("", "example-*.txt")
	if err != nil {
		t.Fatalf("temp file error: %v", err)
	}
	defer os.Remove(tmpFile.Name())

	_, err = tmpFile.WriteString("temporary")
	if err != nil {
		t.Fatalf("write error: %v", err)
	}
	tmpFile.Close()

	data, err := os.ReadFile(tmpFile.Name())
	if err != nil {
		t.Fatalf("read temp file error: %v", err)
	}
	if string(data) != "temporary" {
		t.Errorf("expected 'temporary', got %q", string(data))
	}
}

func TestJSONOmitEmpty(t *testing.T) {
	type Config struct {
		Name  string `json:"name"`
		Email string `json:"email,omitempty"`
	}
	c := Config{Name: "test"}
	jsonData, _ := json.Marshal(c)
	if strings.Contains(string(jsonData), "email") {
		t.Error("expected omitempty to exclude empty email field")
	}
}
