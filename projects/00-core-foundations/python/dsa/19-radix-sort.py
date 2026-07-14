"""
DSA Tutorial 19 - Radix Sort
==============================

Radix Sort: Sort by processing individual digits.
Uses counting sort as a subroutine for each digit position.

Time Complexity: O(d * (n + b)) where d = digits, b = base
Space Complexity: O(n + b)
Stable: Yes
When to use: Integers with similar number of digits
"""

# =============================================================================
# 1. RADIX SORT (LSD - LEAST SIGNIFICANT DIGIT)
# =============================================================================

def counting_sort_by_digit(arr, exp):
    """Counting sort used for each digit position"""
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    return output

def radix_sort(arr):
    """Radix sort (LSD). O(d * (n + 10))"""
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr

print("=== LSD Radix Sort ===")
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print(f"Original: {arr}")
print(f"Sorted: {radix_sort(arr.copy())}")


# =============================================================================
# 2. RADIX SORT WITH STEPS
# =============================================================================

def radix_sort_steps(arr):
    """Radix sort showing each digit pass"""
    arr = arr.copy()
    max_val = max(arr)
    exp = 1
    steps = []

    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        steps.append(f"Exp {exp}: {arr.copy()}")
        exp *= 10

    return arr, steps

print("\n=== Radix Sort with Steps ===")
arr = [170, 45, 75, 90, 802, 24, 2, 66]
sorted_arr, steps = radix_sort_steps(arr)
for step in steps:
    print(f"  {step}")
print(f"Final: {sorted_arr}")


# =============================================================================
# 3. MSD RADIX SORT (MOST SIGNIFICANT DIGIT)
# =============================================================================

def radix_sort_msd(arr):
    """MSD Radix Sort - processes from most significant digit"""
    if not arr:
        return arr

    max_val = max(arr)
    max_digits = len(str(max_val))

    def msd_sort(arr, digit_pos):
        if len(arr) <= 1 or digit_pos < 0:
            return arr

        buckets = [[] for _ in range(10)]

        for num in arr:
            digit = (num // (10 ** digit_pos)) % 10
            buckets[digit].append(num)

        result = []
        for bucket in buckets:
            if bucket:
                result.extend(msd_sort(bucket, digit_pos - 1))

        return result

    return msd_sort(arr, max_digits - 1)

print("\n=== MSD Radix Sort ===")
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print(f"Sorted: {radix_sort_msd(arr.copy())}")


# =============================================================================
# 4. RADIX SORT FOR NEGATIVES
# =============================================================================

def radix_sort_with_negatives(arr):
    """Radix sort handling negative numbers"""
    if not arr:
        return arr

    # Separate negatives and positives
    negatives = [-x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]

    # Sort both
    if negatives:
        negatives = radix_sort(negatives)
        negatives = [-x for x in reversed(negatives)]

    if positives:
        positives = radix_sort(positives)

    return negatives + positives

print("\n=== Radix Sort with Negatives ===")
arr = [-170, 45, -75, 90, -802, 24, 2, -66]
print(f"Original: {arr}")
print(f"Sorted: {radix_sort_with_negatives(arr.copy())}")


# =============================================================================
# 5. RADIX SORT FOR STRINGS
# =============================================================================

def radix_sort_strings(strings, max_len=None):
    """Radix sort for strings of equal length"""
    if not strings:
        return strings

    if max_len is None:
        max_len = max(len(s) for s in strings)

    # Pad shorter strings
    strings = [s.ljust(max_len) for s in strings]

    for pos in range(max_len - 1, -1, -1):
        # Counting sort by character at position
        count = [0] * 256  # ASCII
        output = [''] * len(strings)

        for s in strings:
            count[ord(s[pos])] += 1

        for i in range(1, 256):
            count[i] += count[i - 1]

        for s in reversed(strings):
            idx = ord(s[pos])
            output[count[idx] - 1] = s
            count[idx] -= 1

        strings = output

    return [s.strip() for s in strings]

print("\n=== Radix Sort Strings ===")
strings = ["banana", "apple", "cherry", "date", "elderberry"]
# Pad to same length for demo
strings = [s.ljust(10) for s in strings]
sorted_strings = radix_sort_strings(strings)
print(f"Sorted: {sorted_strings}")


# =============================================================================
# 6. RADIX SORT FOR DECIMALS
# =============================================================================

def radix_sort_floats(arr):
    """Radix sort for floating point numbers"""
    if not arr:
        return arr

    # Handle negatives
    negatives = [-x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]

    def sort_positive_floats(floats):
        # Convert to integers by scaling
        max_decimals = 0
        for f in floats:
            s = str(f)
            if '.' in s:
                max_decimals = max(max_decimals, len(s) - s.index('.') - 1)

        scale = 10 ** max_decimals
        int_arr = [int(round(f * scale)) for f in floats]
        int_arr = radix_sort(int_arr)
        return [x / scale for x in int_arr]

    if negatives:
        negatives = sort_positive_floats(negatives)
        negatives = [-x for x in reversed(negatives)]

    if positives:
        positives = sort_positive_floats(positives)

    return negatives + positives

print("\n=== Radix Sort Floats ===")
arr = [3.14, 1.41, 2.72, 0.58, 1.73]
print(f"Original: {arr}")
print(f"Sorted: {radix_sort_floats(arr.copy())}")


# =============================================================================
# 7. RADIX SORT PERFORMANCE
# =============================================================================

def analyze_radix_sort():
    """Analyze radix sort performance"""
    import time
    import random

    print("\n=== Radix Sort Performance ===")

    def counting_sort(arr):
        if not arr:
            return arr
        max_val = max(arr)
        count = [0] * (max_val + 1)
        for num in arr:
            count[num] += 1
        sorted_arr = []
        for i, c in enumerate(count):
            sorted_arr.extend([i] * c)
        return sorted_arr

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    sizes = [1000, 10000, 100000]
    max_vals = [1000, 10000, 100000]

    for size in sizes:
        for max_val in max_vals:
            arr = [random.randint(0, max_val) for _ in range(size)]

            # Radix
            test = arr.copy()
            start = time.time()
            radix_sort(test)
            radix_time = time.time() - start

            # Counting
            test = arr.copy()
            start = time.time()
            counting_sort(test)
            count_time = time.time() - start

            # Merge
            test = arr.copy()
            start = time.time()
            merge_sort(test)
            merge_time = time.time() - start

            print(f"\nn={size}, max={max_val}:")
            print(f"  Radix:    {radix_time*1000:.2f}ms")
            print(f"  Counting: {count_time*1000:.2f}ms")
            print(f"  Merge:    {merge_time*1000:.2f}ms")

analyze_radix_sort()


# =============================================================================
# 8. RADIX SORT COMPARISON
# =============================================================================

def compare_radix_variants():
    """Compare LSD vs MSD radix sort"""
    import time
    import random

    print("\n=== LSD vs MSD Radix Sort ===")

    sizes = [1000, 10000, 100000]

    for size in sizes:
        arr = [random.randint(0, 100000) for _ in range(size)]

        # LSD
        test = arr.copy()
        start = time.time()
        lsd_result = radix_sort(test)
        lsd_time = time.time() - start

        # MSD
        test = arr.copy()
        start = time.time()
        msd_result = radix_sort_msd(test)
        msd_time = time.time() - start

        print(f"\nn={size}:")
        print(f"  LSD: {lsd_time*1000:.2f}ms")
        print(f"  MSD: {msd_time*1000:.2f}ms")

compare_radix_variants()


# =============================================================================
# 9. PRACTICAL APPLICATIONS
# =============================================================================

print("\n=== Practical Applications ===")

# Sort phone numbers
def sort_phone_numbers(phones):
    """Sort phone numbers using radix sort"""
    return radix_sort([int(p.replace('-', '').replace(' ', ''))
                       for p in phones])

phones = ["555-1234", "555-5678", "555-9012", "555-3456"]
print(f"Phones: {phones}")
sorted_phones = sort_phone_numbers(phones)
print(f"Sorted: {sorted_phones}")

# Sort dates (as integers YYYYMMDD)
def sort_dates(dates):
    """Sort dates using radix sort"""
    date_ints = []
    for d in dates:
        year, month, day = d.split('-')
        date_ints.append(int(year + month + day))

    sorted_ints = radix_sort(date_ints)

    result = []
    for d in sorted_ints:
        s = str(d)
        result.append(f"{s[:4]}-{s[4:6]}-{s[6:]}")
    return result

dates = ["2024-01-15", "2023-12-25", "2024-03-01", "2023-06-30"]
print(f"\nDates: {dates}")
print(f"Sorted: {sort_dates(dates)}")


# =============================================================================
# 10. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Radix Sort - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Radix sort processes digits, not comparisons")
    print("2. O(d * n) time - linear for fixed-size integers")
    print("3. LSD processes from right, MSD from left")
    print("4. Stable sort - useful for multi-key sorting")
    print("5. Efficient for integers, strings, and fixed-format data")
