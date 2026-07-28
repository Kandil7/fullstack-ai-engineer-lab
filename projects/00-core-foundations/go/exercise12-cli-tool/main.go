package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"
)

// CLI Tool Exercise - Capstone Project
// Build a JSON transformer CLI tool
//
// Usage examples:
//   go run . transform --input data.json --output result.json --field name --upper
//   go run . transform --input data.json --field email --lower
//   go run . transform --input data.json --field age --add 5
//   go run . filter --input data.json --field status --value active
//   go run . stats --input data.json

type Config struct {
	Command   string
	Input     string
	Output    string
	Field     string
	Value     string
	Operation string
}

func main() {
	fmt.Println("=== Exercise 12: CLI Tool (Capstone) ===")

	if len(os.Args) < 2 {
		printUsage()
		return
	}

	cmd := os.Args[1]
	args := os.Args[2:]

	switch cmd {
	case "transform":
		runTransform(args)
	case "filter":
		runFilter(args)
	case "stats":
		runStats(args)
	case "help", "-h", "--help":
		printUsage()
	default:
		fmt.Printf("Unknown command: %s\n", cmd)
		printUsage()
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Print(`JSON Transformer CLI

Usage:
  jsontool <command> [flags]

Commands:
  transform   Transform a field in JSON data
  filter      Filter JSON objects by field value
  stats       Show statistics about JSON data
  help        Show this help

Transform Flags:
  -input string     Input JSON file (required)
  -output string    Output JSON file (default: stdout)
  -field string     Field name to transform (required)
  -op string        Operation: upper, lower, add, multiply (required)
  -value string     Value for add/multiply operations

Filter Flags:
  -input string     Input JSON file (required)
  -field string     Field name to filter on (required)
  -value string     Value to match (required)
  -output string    Output JSON file (default: stdout)

Stats Flags:
  -input string     Input JSON file (required)
`)
}
func runTransform(args []string) {
	fs := flag.NewFlagSet("transform", flag.ExitOnError)
	input := fs.String("input", "", "Input JSON file")
	output := fs.String("output", "", "Output JSON file (default: stdout)")
	field := fs.String("field", "", "Field name to transform")
	op := fs.String("op", "", "Operation: upper, lower, add, multiply")
	value := fs.String("value", "", "Value for add/multiply")
	fs.Parse(args)

	if *input == "" || *field == "" || *op == "" {
		fmt.Println("Error: -input, -field, and -op are required")
		fs.PrintDefaults()
		os.Exit(1)
	}

	data, err := os.ReadFile(*input)
	if err != nil {
		fmt.Printf("Error reading input: %v\n", err)
		os.Exit(1)
	}

	var jsonData interface{}
	if err := json.Unmarshal(data, &jsonData); err != nil {
		fmt.Printf("Error parsing JSON: %v\n", err)
		os.Exit(1)
	}

	transformed := transformField(jsonData, *field, *op, *value)

	outputData, err := json.MarshalIndent(transformed, "", "  ")
	if err != nil {
		fmt.Printf("Error marshaling JSON: %v\n", err)
		os.Exit(1)
	}

	if *output == "" {
		fmt.Println(string(outputData))
	} else {
		if err := os.WriteFile(*output, outputData, 0644); err != nil {
			fmt.Printf("Error writing output: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("Transformed data written to %s\n", *output)
	}
}

func runFilter(args []string) {
	fs := flag.NewFlagSet("filter", flag.ExitOnError)
	input := fs.String("input", "", "Input JSON file")
	output := fs.String("output", "", "Output JSON file (default: stdout)")
	field := fs.String("field", "", "Field name to filter on")
	value := fs.String("value", "", "Value to match")
	fs.Parse(args)

	if *input == "" || *field == "" || *value == "" {
		fmt.Println("Error: -input, -field, and -value are required")
		fs.PrintDefaults()
		os.Exit(1)
	}

	data, err := os.ReadFile(*input)
	if err != nil {
		fmt.Printf("Error reading input: %v\n", err)
		os.Exit(1)
	}

	var jsonData []interface{}
	if err := json.Unmarshal(data, &jsonData); err != nil {
		fmt.Printf("Error parsing JSON (expected array): %v\n", err)
		os.Exit(1)
	}

	filtered := filterObjects(jsonData, *field, *value)

	outputData, err := json.MarshalIndent(filtered, "", "  ")
	if err != nil {
		fmt.Printf("Error marshaling JSON: %v\n", err)
		os.Exit(1)
	}

	if *output == "" {
		fmt.Println(string(outputData))
	} else {
		if err := os.WriteFile(*output, outputData, 0644); err != nil {
			fmt.Printf("Error writing output: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("Filtered data written to %s\n", *output)
	}
}

func runStats(args []string) {
	fs := flag.NewFlagSet("stats", flag.ExitOnError)
	input := fs.String("input", "", "Input JSON file")
	fs.Parse(args)

	if *input == "" {
		fmt.Println("Error: -input is required")
		fs.PrintDefaults()
		os.Exit(1)
	}

	data, err := os.ReadFile(*input)
	if err != nil {
		fmt.Printf("Error reading input: %v\n", err)
		os.Exit(1)
	}

	var jsonData interface{}
	if err := json.Unmarshal(data, &jsonData); err != nil {
		fmt.Printf("Error parsing JSON: %v\n", err)
		os.Exit(1)
	}

	stats := analyzeJSON(jsonData)
	printStats(stats)
}

func transformField(data interface{}, field, op, value string) interface{} {
	switch v := data.(type) {
	case map[string]interface{}:
		result := make(map[string]interface{})
		for k, val := range v {
			if k == field {
				result[k] = applyOperation(val, op, value)
			} else {
				result[k] = transformField(val, field, op, value)
			}
		}
		return result
	case []interface{}:
		result := make([]interface{}, len(v))
		for i, item := range v {
			result[i] = transformField(item, field, op, value)
		}
		return result
	default:
		return v
	}
}

func applyOperation(val interface{}, op, value string) interface{} {
	switch op {
	case "upper":
		if s, ok := val.(string); ok {
			return strings.ToUpper(s)
		}
	case "lower":
		if s, ok := val.(string); ok {
			return strings.ToLower(s)
		}
	case "add":
		if f, ok := val.(float64); ok {
			var addVal float64
			fmt.Sscanf(value, "%f", &addVal)
			return f + addVal
		}
	case "multiply":
		if f, ok := val.(float64); ok {
			var mulVal float64
			fmt.Sscanf(value, "%f", &mulVal)
			return f * mulVal
		}
	}
	return val
}

func filterObjects(data []interface{}, field, value string) []interface{} {
	var result []interface{}
	for _, item := range data {
		if obj, ok := item.(map[string]interface{}); ok {
			if fieldVal, exists := obj[field]; exists {
				if fmt.Sprintf("%v", fieldVal) == value {
					result = append(result, obj)
				}
			}
		}
	}
	return result
}

func analyzeJSON(data interface{}) map[string]interface{} {
	stats := make(map[string]interface{})
	countTypes(data, stats)
	return stats
}

func countTypes(data interface{}, stats map[string]interface{}) {
	switch v := data.(type) {
	case map[string]interface{}:
		stats["objects"] = stats["objects"].(int) + 1
		for _, val := range v {
			countTypes(val, stats)
		}
	case []interface{}:
		stats["arrays"] = stats["arrays"].(int) + 1
		stats["total_elements"] = stats["total_elements"].(int) + len(v)
		for _, item := range v {
			countTypes(item, stats)
		}
	case string:
		stats["strings"] = stats["strings"].(int) + 1
	case float64:
		stats["numbers"] = stats["numbers"].(int) + 1
	case bool:
		stats["booleans"] = stats["booleans"].(int) + 1
	case nil:
		stats["nulls"] = stats["nulls"].(int) + 1
	}
}

func printStats(stats map[string]interface{}) {
	fmt.Println("JSON Statistics:")
	fmt.Println("================")
	for k, v := range stats {
		fmt.Printf("  %s: %v\n", k, v)
	}
}
