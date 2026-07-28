package main

import "fmt"

// TreeNode represents a binary tree node
type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

// BST is a binary search tree
type BST struct {
	Root *TreeNode
}

// Insert adds a value to the BST
func (bst *BST) Insert(val int) {
	bst.Root = insertNode(bst.Root, val)
}

func insertNode(node *TreeNode, val int) *TreeNode {
	if node == nil {
		return &TreeNode{Val: val}
	}
	if val < node.Val {
		node.Left = insertNode(node.Left, val)
	} else {
		node.Right = insertNode(node.Right, val)
	}
	return node
}

// Search finds a value in the BST
func (bst *BST) Search(val int) bool {
	return searchNode(bst.Root, val)
}

func searchNode(node *TreeNode, val int) bool {
	if node == nil {
		return false
	}
	if val == node.Val {
		return true
	}
	if val < node.Val {
		return searchNode(node.Left, val)
	}
	return searchNode(node.Right, val)
}

// TREE TRAVERSALS

// Inorder — left, root, right (sorted for BST)
func Inorder(node *TreeNode, result *[]int) {
	if node == nil {
		return
	}
	Inorder(node.Left, result)
	*result = append(*result, node.Val)
	Inorder(node.Right, result)
}

// Preorder — root, left, right
func Preorder(node *TreeNode, result *[]int) {
	if node == nil {
		return
	}
	*result = append(*result, node.Val)
	Preorder(node.Left, result)
	Preorder(node.Right, result)
}

// Postorder — left, right, root
func Postorder(node *TreeNode, result *[]int) {
	if node == nil {
		return
	}
	Postorder(node.Left, result)
	Postorder(node.Right, result)
	*result = append(*result, node.Val)
}

// BFS (Level Order) — breadth-first traversal
func BFS(root *TreeNode) []int {
	if root == nil {
		return nil
	}
	var result []int
	queue := []*TreeNode{root}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		result = append(result, node.Val)
		if node.Left != nil {
			queue = append(queue, node.Left)
		}
		if node.Right != nil {
			queue = append(queue, node.Right)
		}
	}
	return result
}

// maxDepth returns the maximum depth of the tree
func maxDepth(root *TreeNode) int {
	if root == nil {
		return 0
	}
	leftDepth := maxDepth(root.Left)
	rightDepth := maxDepth(root.Right)
	if leftDepth > rightDepth {
		return leftDepth + 1
	}
	return rightDepth + 1
}

// isValidBST checks if a binary tree is a valid BST
func isValidBST(root *TreeNode) bool {
	return validateBST(root, nil, nil)
}

func validateBST(node *TreeNode, min, max *int) bool {
	if node == nil {
		return true
	}
	if min != nil && node.Val <= *min {
		return false
	}
	if max != nil && node.Val >= *max {
		return false
	}
	return validateBST(node.Left, min, &node.Val) &&
		validateBST(node.Right, &node.Val, max)
}

func main() {
	fmt.Println("=== Trees & Binary Search Tree Exercise ===")
	fmt.Println()

	// Build a BST
	bst := &BST{}
	values := []int{8, 3, 10, 1, 6, 14, 4, 7, 13}
	for _, v := range values {
		bst.Insert(v)
	}

	fmt.Println("BST Structure:")
	fmt.Println("       8")
	fmt.Println("     /   \\")
	fmt.Println("    3     10")
	fmt.Println("   / \\      \\")
	fmt.Println("  1   6     14")
	fmt.Println("     / \\    /")
	fmt.Println("    4   7  13")
	fmt.Println()

	// Traversals
	fmt.Print("Inorder (sorted):   ")
	var inorder []int
	Inorder(bst.Root, &inorder)
	fmt.Println(inorder)

	fmt.Print("Preorder:           ")
	var preorder []int
	Preorder(bst.Root, &preorder)
	fmt.Println(preorder)

	fmt.Print("Postorder:          ")
	var postorder []int
	Postorder(bst.Root, &postorder)
	fmt.Println(postorder)

	fmt.Print("BFS (level order):  ")
	fmt.Println(BFS(bst.Root))

	// Search
	fmt.Printf("\nSearch(6): %v\n", bst.Search(6))
	fmt.Printf("Search(99): %v\n", bst.Search(99))

	// Tree properties
	fmt.Printf("\nMax depth: %d\n", maxDepth(bst.Root))
	fmt.Printf("Is valid BST: %v\n", isValidBST(bst.Root))
}
