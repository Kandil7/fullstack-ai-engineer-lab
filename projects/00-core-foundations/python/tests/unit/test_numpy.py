"""
Unit tests for NumPy examples.
"""

import pytest
import numpy as np


class TestNumpyBasics:
    """Test NumPy basic functionality."""

    def test_introduction_imports(self):
        """Test that introduction imports work."""
        from numpy.introduction import python_list, numpy_array

        assert python_list == [1, 2, 3, 4, 5]
        assert np.array_equal(numpy_array, np.array([1, 2, 3, 4, 5]))

    def test_array_attributes(self):
        """Test array attributes."""
        from numpy.introduction import arr

        assert arr.shape == (2, 5)
        assert arr.size == 10
        assert arr.ndim == 2
        assert arr.dtype == np.int64
        assert arr.itemsize == 8
        assert arr.nbytes == 80

    def test_creating_arrays(self):
        """Test array creation."""
        from numpy.creating_arrays import arr_1d, arr_2d, arr_3d

        assert arr_1d.shape == (3,)
        assert arr_2d.shape == (2, 3)
        assert arr_3d.shape == (2, 2, 2)

    def test_array_indexing(self):
        """Test array indexing."""
        from numpy.array_indexing import arr_2d

        assert arr_2d[0, 0] == 1
        assert arr_2d[1, 2] == 6
        assert np.array_equal(arr_2d[0], np.array([1, 2, 3]))
        assert np.array_equal(arr_2d[:, 1], np.array([2, 5]))

    def test_array_slicing(self):
        """Test array slicing."""
        from numpy.array_slicing import arr_1d, arr_2d

        assert np.array_equal(arr_1d[1:4], np.array([2, 3, 4]))
        assert np.array_equal(arr_2d[:2, 1:3], np.array([[2, 3], [5, 6]]))

    def test_copy_vs_view(self):
        """Test copy vs view."""
        from numpy.copy_vs_view import original, view_arr, copy_arr

        # View shares memory
        view_arr[0] = 99
        assert original[0] == 99

        # Copy doesn't share memory
        copy_arr[0] = 100
        assert original[0] == 99  # Still 99 from view change

    def test_array_shape(self):
        """Test array shape operations."""
        from numpy.array_shape import arr, reshaped, resized

        assert arr.shape == (2, 3)
        assert reshaped.shape == (3, 2)
        assert resized.shape == (2, 6)

    def test_array_reshape(self):
        """Test array reshape."""
        from numpy.array_reshape import arr_1d, arr_2d, arr_3d

        assert arr_1d.shape == (6,)
        assert arr_2d.shape == (2, 3)
        assert arr_3d.shape == (2, 3, 1)

    def test_array_iterating(self):
        """Test array iteration."""
        from numpy.array_iterating import arr_2d

        assert arr_2d.ndim == 2

    def test_array_join(self):
        """Test array joining."""
        from numpy.array_join import joined_1d, joined_2d

        assert np.array_equal(joined_1d, np.array([1, 2, 3, 4, 5, 6]))
        assert joined_2d.shape == (2, 6)

    def test_array_split(self):
        """Test array splitting."""
        from numpy.array_split import split_arrays

        assert len(split_arrays) == 3

    def test_array_search(self):
        """Test array search."""
        from numpy.array_search import arr, indices

        assert list(indices) == [2, 5]

    def test_array_sort(self):
        """Test array sorting."""
        from numpy.array_sort import sorted_arr

        assert np.array_equal(sorted_arr, np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))

    def test_array_filter(self):
        """Test array filtering."""
        from numpy.array_filter import arr, filtered

        assert np.array_equal(filtered, np.array([4, 5, 6, 7, 8, 9]))

    def test_random_intro(self):
        """Test random module."""
        from numpy.random_intro import rand_int, rand_float, rand_arr

        assert isinstance(rand_int, np.integer)
        assert isinstance(rand_float, np.floating)
        assert rand_arr.shape == (2, 3)

    def test_data_distribution(self):
        """Test data distribution."""
        from numpy.data_distribution import dist

        assert dist.shape == (1000,)

    def test_random_permutation(self):
        """Test random permutation."""
        from numpy.random_permutation import perm, shuffle_arr

        assert set(perm) == set(range(10))
        assert set(shuffle_arr) == set(range(10))

    def test_ufunc_intro(self):
        """Test ufunc introduction."""
        from numpy.ufunc_intro import arr, sqrt_arr

        assert np.array_equal(sqrt_arr, np.sqrt(arr))

    def test_ufunc_arithmetic(self):
        """Test arithmetic ufuncs."""
        from numpy.ufunc_arithmetic import x, y, add, sub, mul, div, pow_arr, mod

        assert np.array_equal(add, x + y)
        assert np.array_equal(sub, x - y)
        assert np.array_equal(mul, x * y)
        assert np.array_equal(div, x / y)
        assert np.array_equal(pow_arr, x**y)
        assert np.array_equal(mod, x % y)

    def test_ufunc_rounding(self):
        """Test rounding ufuncs."""
        from numpy.ufunc_rounding import arr, trunc, fix, round_arr, floor, ceil

        assert np.array_equal(trunc, np.trunc(arr))
        assert np.array_equal(fix, np.fix(arr))
        assert np.array_equal(round_arr, np.round(arr))
        assert np.array_equal(floor, np.floor(arr))
        assert np.array_equal(ceil, np.ceil(arr))

    def test_ufunc_logs(self):
        """Test log ufuncs."""
        from numpy.ufunc_logs import arr, log, log2, log10

        assert np.allclose(log, np.log(arr))
        assert np.allclose(log2, np.log2(arr))
        assert np.allclose(log10, np.log10(arr))

    def test_ufunc_summations(self):
        """Test summation ufuncs."""
        from numpy.ufunc_summations import arr, cumsum, sum_arr

        assert np.array_equal(cumsum, np.cumsum(arr))
        assert sum_arr == np.sum(arr)

    def test_ufunc_products(self):
        """Test product ufuncs."""
        from numpy.ufunc_products import arr, cumprod, prod

        assert np.array_equal(cumprod, np.cumprod(arr))
        assert prod == np.prod(arr)

    def test_ufunc_differences(self):
        """Test difference ufuncs."""
        from numpy.ufunc_differences import arr, diff, diff2

        assert np.array_equal(diff, np.diff(arr))
        assert np.array_equal(diff2, np.diff(arr, n=2))

    def test_ufunc_trigonometric(self):
        """Test trigonometric ufuncs."""
        from numpy.ufunc_trigonometric import arr, sin_arr, cos_arr, tan_arr

        assert np.allclose(sin_arr, np.sin(arr))
        assert np.allclose(cos_arr, np.cos(arr))
        assert np.allclose(tan_arr, np.tan(arr))

    def test_ufunc_set_operations(self):
        """Test set operations."""
        from numpy.ufunc_set_operations import arr1, arr2, union, intersection, diff, sym_diff

        assert set(union) == set(arr1) | set(arr2)
        assert set(intersection) == set(arr1) & set(arr2)
        assert set(diff) == set(arr1) - set(arr2)
        assert set(sym_diff) == (set(arr1) - set(arr2)) | (set(arr2) - set(arr1))
