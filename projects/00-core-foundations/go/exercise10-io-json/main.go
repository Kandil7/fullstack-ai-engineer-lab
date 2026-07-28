package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strings"
)

// Custom JSON Marshaling
type CustomTime struct {
	Value string `json:"value"`
}

type Event struct {
	ID   int        `json:"id"`
	Time CustomTime `json:"time"`
}

func main() {
	fmt.Println("=== Exercise 10: I/O and JSON ===")

	// 1. Reading from stdin
	fmt.Println("--- 1. Standard Input/Output ---")
	fmt.Print("Enter your name: ")
	var name string
	fmt.Scanln(&name)
	fmt.Println("Hello,", name)

	// 2. File I/O
	fmt.Println("\n--- 2. File I/O ---")
	content := "Hello, Go!\nThis is a test file.\nLine 3."
	err := os.WriteFile("test.txt", []byte(content), 0644)
	if err != nil {
		fmt.Println("Write error:", err)
	} else {
		fmt.Println("File written")
	}

	data, err := os.ReadFile("test.txt")
	if err != nil {
		fmt.Println("Read error:", err)
	} else {
		fmt.Println("File content:")
		fmt.Print(string(data))
	}

	// 3. Reading with io.Reader
	fmt.Println("\n--- 3. io.Reader Pattern ---")
	reader := strings.NewReader("Hello, io.Reader!\nLine 2\nLine 3")
	buf := make([]byte, 50)
	for {
		n, err := reader.Read(buf)
		if n > 0 {
			fmt.Print(string(buf[:n]))
		}
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Println("Error:", err)
			break
		}
	}

	// 4. Writing with io.Writer
	fmt.Println("\n--- 4. io.Writer Pattern ---")
	var builder strings.Builder
	writer := io.Writer(&builder)
	writer.Write([]byte("Written via io.Writer\n"))
	writer.Write([]byte("Second write\n"))
	fmt.Print(builder.String())

	// 5. JSON Marshal/Unmarshal
	fmt.Println("\n--- 5. JSON ---")
	type Person struct {
		Name  string   `json:"name"`
		Age   int      `json:"age"`
		Email string   `json:"email,omitempty"`
		Tags  []string `json:"tags"`
	}

	p := Person{
		Name:  "Alice",
		Age:   30,
		Email: "alice@example.com",
		Tags:  []string{"go", "json", "backend"},
	}

	// Marshal to JSON
	jsonData, err := json.Marshal(p)
	if err != nil {
		fmt.Println("Marshal error:", err)
	} else {
		fmt.Println("JSON:", string(jsonData))
	}

	// Marshal with indentation
	jsonPretty, _ := json.MarshalIndent(p, "", "  ")
	fmt.Println("Pretty JSON:")
	fmt.Println(string(jsonPretty))

	// Unmarshal from JSON
	jsonStr := `{"name":"Bob","age":25,"tags":["dev","ops"]}`
	var p2 Person
	err = json.Unmarshal([]byte(jsonStr), &p2)
	if err != nil {
		fmt.Println("Unmarshal error:", err)
	} else {
		fmt.Printf("Unmarshaled: %+v\n", p2)
	}

	// 6. JSON Streaming (Decoder/Encoder)
	fmt.Println("\n--- 6. JSON Streaming ---")
	multiJSON := `{"name":"Charlie","age":35}
{"name":"Diana","age":28}
{"name":"Eve","age":42}`
	decoder := json.NewDecoder(strings.NewReader(multiJSON))
	for {
		var person Person
		if err := decoder.Decode(&person); err == io.EOF {
			break
		} else if err != nil {
			fmt.Println("Decode error:", err)
			break
		}
		fmt.Printf("  Streamed: %s, %d\n", person.Name, person.Age)
	}

	// 7. Custom JSON Marshaling
	fmt.Println("\n--- 7. Custom JSON ---")
	e := Event{ID: 1, Time: CustomTime{Value: "2024-01-15T10:30:00Z"}}
	jsonBytes, _ := json.Marshal(e)
	fmt.Println("Custom marshal:", string(jsonBytes))

	// 8. File operations
	fmt.Println("\n--- 8. File Operations ---")
	// Create temp file
	tmpFile, err := os.CreateTemp("", "example-*.txt")
	if err != nil {
		fmt.Println("Temp file error:", err)
	} else {
		defer os.Remove(tmpFile.Name())
		tmpFile.WriteString("Temporary data\n")
		tmpFile.Close()
		fmt.Println("Temp file:", tmpFile.Name())
	}

	// Directory operations
	entries, err := os.ReadDir(".")
	if err != nil {
		fmt.Println("ReadDir error:", err)
	} else {
		fmt.Println("Files in current dir:")
		for _, e := range entries {
			info, _ := e.Info()
			fmt.Printf("  %s (size: %d, dir: %v)\n", e.Name(), info.Size(), e.IsDir())
		}
	}

	// 9. Buffered I/O
	fmt.Println("\n--- 9. Buffered I/O ---")
	// bufio is useful for reading line by line
	// (demonstrated in scanner example below)

	// 10. os.Stdout, os.Stderr
	fmt.Println("\n--- 10. Standard Streams ---")
	fmt.Fprintln(os.Stdout, "This goes to stdout")
	fmt.Fprintln(os.Stderr, "This goes to stderr")
}

// Custom JSON marshaling
func (ct CustomTime) MarshalJSON() ([]byte, error) {
	return json.Marshal(ct.Value)
}

func (ct *CustomTime) UnmarshalJSON(data []byte) error {
	var s string
	if err := json.Unmarshal(data, &s); err != nil {
		return err
	}
	ct.Value = s
	return nil
}
