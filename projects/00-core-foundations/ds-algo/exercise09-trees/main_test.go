package main

import (
	"reflect"
	"testing"
)

func TestBSTInsertAndSearch(t *testing.T) {
	bst := &BST{}
	values := []int{8, 3, 10, 1, 6, 14, 4, 7, 13}
	for _, v := range values {
		bst.Insert(v)
	}

	// Search existing values
	for _, v := range values {
		if !bst.Search(v) {
			t.Errorf("expected to find %d in BST", v)
		}
	}

	// Search non-existing values
	nonExisting := []int{0, 2, 5, 9, 15, 100}
	for _, v := range nonExisting {
		if bst.Search(v) {
			t.Errorf("expected not to find %d in BST", v)
		}
	}
}

func TestBSTEmpty(t *testing.T) {
	bst := &BST{}
	if bst.Search(1) {
		t.Error("expected Search on empty BST to return false")
	}
}

func TestInorder(t *testing.T) {
	bst := &BST{}
	for _, v := range []int{8, 3, 10, 1, 6} {
		bst.Insert(v)
	}
	var result []int
	Inorder(bst.Root, &result)
	expected := []int{1, 3, 6, 8, 10}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("inorder: expected %v, got %v", expected, result)
	}
}

func TestPreorder(t *testing.T) {
	bst := &BST{}
	for _, v := range []int{8, 3, 10, 1, 6} {
		bst.Insert(v)
	}
	var result []int
	Preorder(bst.Root, &result)
	expected := []int{8, 3, 1, 6, 10}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("preorder: expected %v, got %v", expected, result)
	}
}

func TestPostorder(t *testing.T) {
	bst := &BST{}
	for _, v := range []int{8, 3, 10, 1, 6} {
		bst.Insert(v)
	}
	var result []int
	Postorder(bst.Root, &result)
	expected := []int{1, 6, 3, 10, 8}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("postorder: expected %v, got %v", expected, result)
	}
}

func TestBFS(t *testing.T) {
	bst := &BST{}
	for _, v := range []int{8, 3, 10, 1, 6} {
		bst.Insert(v)
	}
	result := BFS(bst.Root)
	expected := []int{8, 3, 10, 1, 6}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("BFS: expected %v, got %v", expected, result)
	}
}

func TestBFS_Empty(t *testing.T) {
	result := BFS(nil)
	if result != nil {
		t.Errorf("expected nil for empty tree, got %v", result)
	}
}

func TestMaxDepth(t *testing.T) {
	bst := &BST{}
	if d := maxDepth(bst.Root); d != 0 {
		t.Errorf("empty tree depth = %d; want 0", d)
	}
	bst.Insert(1)
	if d := maxDepth(bst.Root); d != 1 {
		t.Errorf("single node depth = %d; want 1", d)
	}
	bst.Insert(2)
	if d := maxDepth(bst.Root); d != 2 {
		t.Errorf("two-node depth = %d; want 2", d)
	}
}

func TestIsValidBST(t *testing.T) {
	// Valid BST
	bst := &BST{}
	for _, v := range []int{8, 3, 10, 1, 6} {
		bst.Insert(v)
	}
	if !isValidBST(bst.Root) {
		t.Error("expected valid BST")
	}

	// Invalid BST (manually created)
	invalid := &TreeNode{Val: 5}
	invalid.Left = &TreeNode{Val: 1}
	invalid.Right = &TreeNode{Val: 4}
	invalid.Right.Left = &TreeNode{Val: 3}
	invalid.Right.Right = &TreeNode{Val: 6}
	if isValidBST(invalid) {
		t.Error("expected invalid BST")
	}

	// Empty tree is valid
	if !isValidBST(nil) {
		t.Error("expected empty tree to be valid BST")
	}
}
