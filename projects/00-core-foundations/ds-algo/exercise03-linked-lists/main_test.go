package main

import (
	"reflect"
	"testing"
)

func TestLinkedListBasicOperations(t *testing.T) {
	ll := &LinkedList{}
	ll.InsertAtEnd(1)
	ll.InsertAtEnd(2)
	ll.InsertAtEnd(3)
	ll.InsertAtBeginning(0)

	expected := []int{0, 1, 2, 3}
	if got := ll.ToSlice(); !reflect.DeepEqual(got, expected) {
		t.Errorf("expected %v, got %v", expected, got)
	}
}

func TestLinkedListSearch(t *testing.T) {
	ll := &LinkedList{}
	ll.InsertAtEnd(10)
	ll.InsertAtEnd(20)
	ll.InsertAtEnd(30)

	if !ll.Search(20) {
		t.Error("expected to find 20")
	}
	if ll.Search(99) {
		t.Error("expected not to find 99")
	}
}

func TestLinkedListDelete(t *testing.T) {
	ll := &LinkedList{}
	ll.InsertAtEnd(1)
	ll.InsertAtEnd(2)
	ll.InsertAtEnd(3)

	if !ll.Delete(2) {
		t.Error("expected Delete(2) to return true")
	}
	expected := []int{1, 3}
	if got := ll.ToSlice(); !reflect.DeepEqual(got, expected) {
		t.Errorf("expected %v, got %v", expected, got)
	}

	if ll.Delete(99) {
		t.Error("expected Delete(99) to return false")
	}
}

func TestLinkedListDeleteHead(t *testing.T) {
	ll := &LinkedList{}
	ll.InsertAtEnd(1)
	ll.InsertAtEnd(2)

	if !ll.Delete(1) {
		t.Error("expected Delete(1) to return true")
	}
	expected := []int{2}
	if got := ll.ToSlice(); !reflect.DeepEqual(got, expected) {
		t.Errorf("expected %v, got %v", expected, got)
	}
}

func TestLinkedListEmpty(t *testing.T) {
	ll := &LinkedList{}
	if got := ll.ToSlice(); len(got) != 0 {
		t.Errorf("expected empty list, got %v", got)
	}
	if ll.Delete(1) {
		t.Error("expected Delete to return false on empty list")
	}
	if ll.Search(1) {
		t.Error("expected Search to return false on empty list")
	}
}

func TestHasCycle(t *testing.T) {
	// No cycle
	noCycle := &ListNode{Val: 1}
	noCycle.Next = &ListNode{Val: 2}
	noCycle.Next.Next = &ListNode{Val: 3}
	if hasCycle(noCycle) {
		t.Error("expected no cycle")
	}

	// With cycle
	withCycle := &ListNode{Val: 1}
	withCycle.Next = &ListNode{Val: 2}
	withCycle.Next.Next = &ListNode{Val: 3}
	withCycle.Next.Next.Next = withCycle.Next
	if !hasCycle(withCycle) {
		t.Error("expected cycle")
	}

	// Empty list
	if hasCycle(nil) {
		t.Error("expected no cycle in empty list")
	}
}

func TestReverseList(t *testing.T) {
	head := &ListNode{Val: 1}
	head.Next = &ListNode{Val: 2}
	head.Next.Next = &ListNode{Val: 3}

	reversed := reverseList(head)
	expected := []int{3, 2, 1}

	var got []int
	for current := reversed; current != nil; current = current.Next {
		got = append(got, current.Val)
	}
	if !reflect.DeepEqual(got, expected) {
		t.Errorf("expected %v, got %v", expected, got)
	}
}

func TestFindMiddle(t *testing.T) {
	// Odd length
	odd := &LinkedList{}
	odd.InsertAtEnd(1)
	odd.InsertAtEnd(2)
	odd.InsertAtEnd(3)
	mid := findMiddle(odd.Head)
	if mid.Val != 2 {
		t.Errorf("expected middle = 2, got %d", mid.Val)
	}

	// Even length
	even := &LinkedList{}
	even.InsertAtEnd(1)
	even.InsertAtEnd(2)
	even.InsertAtEnd(3)
	even.InsertAtEnd(4)
	mid = findMiddle(even.Head)
	if mid.Val != 3 {
		t.Errorf("expected middle = 3, got %d", mid.Val)
	}
}
