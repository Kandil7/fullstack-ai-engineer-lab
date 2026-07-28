package main

import "fmt"

// Singly linked list node
type ListNode struct {
	Val  int
	Next *ListNode
}

// LinkedList with head pointer
type LinkedList struct {
	Head *ListNode
}

// InsertAtBeginning adds a new node at the front
func (ll *LinkedList) InsertAtBeginning(val int) {
	ll.Head = &ListNode{Val: val, Next: ll.Head}
}

// InsertAtEnd adds a new node at the end
func (ll *LinkedList) InsertAtEnd(val int) {
	newNode := &ListNode{Val: val}
	if ll.Head == nil {
		ll.Head = newNode
		return
	}
	current := ll.Head
	for current.Next != nil {
		current = current.Next
	}
	current.Next = newNode
}

// Delete removes the first occurrence of val
func (ll *LinkedList) Delete(val int) bool {
	if ll.Head == nil {
		return false
	}
	if ll.Head.Val == val {
		ll.Head = ll.Head.Next
		return true
	}
	current := ll.Head
	for current.Next != nil && current.Next.Val != val {
		current = current.Next
	}
	if current.Next == nil {
		return false
	}
	current.Next = current.Next.Next
	return true
}

// Search returns true if val exists in the list
func (ll *LinkedList) Search(val int) bool {
	current := ll.Head
	for current != nil {
		if current.Val == val {
			return true
		}
		current = current.Next
	}
	return false
}

// ToSlice converts the linked list to a slice for easy inspection
func (ll *LinkedList) ToSlice() []int {
	var result []int
	current := ll.Head
	for current != nil {
		result = append(result, current.Val)
		current = current.Next
	}
	return result
}

// hasCycle detects if the linked list has a cycle (Floyd's algorithm)
func hasCycle(head *ListNode) bool {
	if head == nil || head.Next == nil {
		return false
	}
	slow, fast := head, head.Next
	for fast != nil && fast.Next != nil {
		if slow == fast {
			return true
		}
		slow = slow.Next
		fast = fast.Next.Next
	}
	return false
}

// reverseList reverses a linked list in-place
func reverseList(head *ListNode) *ListNode {
	var prev *ListNode
	current := head
	for current != nil {
		next := current.Next
		current.Next = prev
		prev = current
		current = next
	}
	return prev
}

// findMiddle finds the middle node (tortoise and hare)
func findMiddle(head *ListNode) *ListNode {
	if head == nil {
		return nil
	}
	slow, fast := head, head
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}
	return slow
}

func printList(head *ListNode) {
	current := head
	for current != nil {
		fmt.Printf("%d", current.Val)
		if current.Next != nil {
			fmt.Print(" -> ")
		}
		current = current.Next
	}
	fmt.Println()
}

func main() {
	fmt.Println("=== Linked Lists Exercise ===")
	fmt.Println()

	// Basic operations
	fmt.Println("--- Basic Operations ---")
	ll := &LinkedList{}
	ll.InsertAtEnd(1)
	ll.InsertAtEnd(2)
	ll.InsertAtEnd(3)
	ll.InsertAtBeginning(0)
	fmt.Print("List: ")
	printList(ll.Head)
	fmt.Printf("ToSlice: %v\n", ll.ToSlice())

	// Search
	fmt.Printf("Search(2): %v\n", ll.Search(2))
	fmt.Printf("Search(99): %v\n", ll.Search(99))

	// Delete
	ll.Delete(2)
	fmt.Print("After delete(2): ")
	printList(ll.Head)

	// Reverse
	fmt.Println("\n--- Reverse List ---")
	reversed := reverseList(ll.Head)
	fmt.Print("Reversed: ")
	printList(reversed)

	// Find middle (fresh list for clarity)
	fmt.Println("\n--- Find Middle ---")
	middleList := &LinkedList{}
	middleList.InsertAtEnd(1)
	middleList.InsertAtEnd(2)
	middleList.InsertAtEnd(3)
	middleList.InsertAtEnd(4)
	middleList.InsertAtEnd(5)
	mid := findMiddle(middleList.Head)
	fmt.Printf("Middle of 1->2->3->4->5: %d\n", mid.Val)

	// Cycle detection
	fmt.Println("\n--- Cycle Detection ---")
	noCycle := &ListNode{Val: 1}
	noCycle.Next = &ListNode{Val: 2}
	noCycle.Next.Next = &ListNode{Val: 3}
	fmt.Printf("Has cycle (no cycle): %v\n", hasCycle(noCycle))

	withCycle := &ListNode{Val: 1}
	withCycle.Next = &ListNode{Val: 2}
	withCycle.Next.Next = &ListNode{Val: 3}
	withCycle.Next.Next.Next = withCycle.Next // create cycle
	fmt.Printf("Has cycle (cycle): %v\n", hasCycle(withCycle))
}
