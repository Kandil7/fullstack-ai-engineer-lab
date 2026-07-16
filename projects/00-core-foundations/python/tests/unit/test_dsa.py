"""
Unit tests for Data Structures and Algorithms.
"""

import pytest
from dsa.introduction import (
    find_largest,
    get_first,
    linear_search,
    bubble_sort_step,
    binary_search_demo,
    sum_list,
    double_list,
    identity_matrix,
    count_occurrences,
    reverse_in_place,
    is_palindrome,
    factorial,
    fibonacci,
)


class TestDSAIntroduction:
    """Test DSA introduction examples."""

    def test_find_largest(self):
        assert find_largest([34, 78, 12, 99, 45]) == 99
        assert find_largest([1]) == 1
        assert find_largest([-5, -2, -10]) == -2
        assert find_largest([]) is None

    def test_get_first(self):
        assert get_first([1, 2, 3]) == 1
        assert get_first([100]) == 100

    def test_linear_search(self):
        assert linear_search([1, 2, 3, 4, 5], 3) == 2
        assert linear_search([1, 2, 3, 4, 5], 6) == -1
        assert linear_search([], 1) == -1

    def test_bubble_sort_step(self):
        sorted_list, comparisons = bubble_sort_step([5, 3, 8, 1, 2])
        assert sorted_list == [1, 2, 3, 5, 8]
        assert comparisons == 10  # n*(n-1)/2 for n=5

    def test_binary_search(self):
        test_list = list(range(1, 101))
        idx, steps = binary_search_demo(test_list, 50)
        assert idx == 49
        assert steps <= 7  # log2(100) < 7

    def test_sum_list(self):
        assert sum_list([1, 2, 3, 4, 5]) == 15
        assert sum_list([]) == 0

    def test_double_list(self):
        assert double_list([1, 2, 3]) == [2, 4, 6]
        assert double_list([]) == []

    def test_identity_matrix(self):
        assert identity_matrix(3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        assert identity_matrix(1) == [[1]]

    def test_count_occurrences(self):
        assert count_occurrences([1, 2, 3, 2, 4, 2, 5], 2) == 3
        assert count_occurrences([1, 2, 3], 5) == 0

    def test_reverse_in_place(self):
        nums = [1, 2, 3, 4, 5]
        reverse_in_place(nums)
        assert nums == [5, 4, 3, 2, 1]

        nums = [1]
        reverse_in_place(nums)
        assert nums == [1]

    def test_is_palindrome(self):
        assert is_palindrome("racecar") is True
        assert is_palindrome("hello") is False
        assert is_palindrome("A man a plan a canal Panama") is True
        assert is_palindrome("") is True

    def test_factorial(self):
        assert factorial(5) == 120
        assert factorial(0) == 1
        assert factorial(1) == 1

    def test_fibonacci(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(10) == 55
