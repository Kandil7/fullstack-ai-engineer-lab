package main

import (
	"fmt"
	"hash/fnv"
)

// HashTable — simple hash table with chaining (separate chaining)
type HashTable struct {
	buckets  [][]KeyValue
	size     int
	capacity int
}

type KeyValue struct {
	Key   string
	Value int
}

func NewHashTable(capacity int) *HashTable {
	return &HashTable{
		buckets:  make([][]KeyValue, capacity),
		capacity: capacity,
	}
}

func (ht *HashTable) hash(key string) int {
	h := fnv.New32a()
	h.Write([]byte(key))
	return int(h.Sum32()) % ht.capacity
}

func (ht *HashTable) Put(key string, value int) {
	idx := ht.hash(key)
	// Check if key already exists
	for i, kv := range ht.buckets[idx] {
		if kv.Key == key {
			ht.buckets[idx][i].Value = value
			return
		}
	}
	// Add new key-value pair
	ht.buckets[idx] = append(ht.buckets[idx], KeyValue{Key: key, Value: value})
	ht.size++
}

func (ht *HashTable) Get(key string) (int, bool) {
	idx := ht.hash(key)
	for _, kv := range ht.buckets[idx] {
		if kv.Key == key {
			return kv.Value, true
		}
	}
	return 0, false
}

func (ht *HashTable) Delete(key string) bool {
	idx := ht.hash(key)
	for i, kv := range ht.buckets[idx] {
		if kv.Key == key {
			ht.buckets[idx] = append(ht.buckets[idx][:i], ht.buckets[idx][i+1:]...)
			ht.size--
			return true
		}
	}
	return false
}

func (ht *HashTable) Contains(key string) bool {
	_, ok := ht.Get(key)
	return ok
}

// twoSum finds two indices that add up to target (classic problem)
func twoSum(nums []int, target int) []int {
	seen := make(map[int]int) // value -> index
	for i, num := range nums {
		complement := target - num
		if idx, ok := seen[complement]; ok {
			return []int{idx, i}
		}
		seen[num] = i
	}
	return nil
}

// firstNonRepeating finds the first non-repeating character in a string
func firstNonRepeating(s string) rune {
	counts := make(map[rune]int)
	for _, r := range s {
		counts[r]++
	}
	for _, r := range s {
		if counts[r] == 1 {
			return r
		}
	}
	return 0
}

func main() {
	fmt.Println("=== Hash Tables Exercise ===")
	fmt.Println()

	// Custom hash table
	fmt.Println("--- Custom Hash Table ---")
	ht := NewHashTable(10)
	ht.Put("apple", 5)
	ht.Put("banana", 3)
	ht.Put("cherry", 7)

	val, ok := ht.Get("apple")
	fmt.Printf("  Get(apple) = %d (exists=%v)\n", val, ok)

	val, ok = ht.Get("grape")
	fmt.Printf("  Get(grape) = %d (exists=%v)\n", val, ok)

	fmt.Printf("  Contains(banana): %v\n", ht.Contains("banana"))
	ht.Delete("banana")
	fmt.Printf("  After delete, Contains(banana): %v\n", ht.Contains("banana"))

	// Two-sum (classic LeetCode problem)
	fmt.Println("\n--- Two Sum ---")
	nums := []int{2, 7, 11, 15}
	fmt.Printf("  twoSum(%v, 9) = %v\n", nums, twoSum(nums, 9))

	// First non-repeating character
	fmt.Println("\n--- First Non-Repeating Character ---")
	tests := []string{"leetcode", "loveleetcode", "aabb"}
	for _, s := range tests {
		r := firstNonRepeating(s)
		if r != 0 {
			fmt.Printf("  firstNonRepeating(%q) = %c\n", s, r)
		} else {
			fmt.Printf("  firstNonRepeating(%q) = none\n", s)
		}
	}
}
