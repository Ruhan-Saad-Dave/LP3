"""
=============================================================================
Assignment: DAA 7 (Group A - Optional/Analysis)
Title: Write a program for analysis of quick sort by using deterministic 
       and randomized variant.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""

import random
import time
import sys

# Increase recursion limit to handle worst-case deep recursion on large sorted arrays
sys.setrecursionlimit(25000)


# ---------------------------------------------------------------------------
# Global Counters for Comparative Analysis
# ---------------------------------------------------------------------------
det_comparisons = 0
rand_comparisons = 0


# ---------------------------------------------------------------------------
# Partition Schemes (Lomuto Partition as in Lab Manual Page 59)
# ---------------------------------------------------------------------------
def partition_deterministic(arr, low, high):
    """
    Standard Lomuto partition using the LAST element as the fixed pivot.
    """
    global det_comparisons
    pivot = arr[high]  # Last element as pivot
    i = low - 1

    for j in range(low, high):
        det_comparisons += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def partition_randomized(arr, low, high):
    """
    Randomized partition: selects a random index between low and high,
    swaps it with arr[high], then uses standard Lomuto partition.
    """
    global rand_comparisons
    # Select random pivot and swap with high
    rand_pivot_idx = random.randint(low, high)
    arr[rand_pivot_idx], arr[high] = arr[high], arr[rand_pivot_idx]

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        rand_comparisons += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ---------------------------------------------------------------------------
# QuickSort Functions
# ---------------------------------------------------------------------------
def quicksort_deterministic(arr, low, high):
    """Recursive Deterministic QuickSort function."""
    if low < high:
        pi = partition_deterministic(arr, low, high)
        quicksort_deterministic(arr, low, pi - 1)
        quicksort_deterministic(arr, pi + 1, high)


def quicksort_randomized(arr, low, high):
    """Recursive Randomized QuickSort function."""
    if low < high:
        pi = partition_randomized(arr, low, high)
        quicksort_randomized(arr, low, pi - 1)
        quicksort_randomized(arr, pi + 1, high)


# ---------------------------------------------------------------------------
# Safe Input Helper
# ---------------------------------------------------------------------------
def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


# ---------------------------------------------------------------------------
# Main Execution & Performance Benchmark
# ---------------------------------------------------------------------------
def main():
    global det_comparisons, rand_comparisons

    print("=" * 75)
    print(" DAA Assignment 7: Analysis of Quick Sort (Deterministic vs Randomized)")
    print("=" * 75)

    # -----------------------------------------------------------------------
    # Part 1: Standard Lab Manual Test Example (Page 59)
    # -----------------------------------------------------------------------
    manual_sample = [10, 80, 30, 90, 40, 50, 70]
    print("\n--- PART 1: LAB MANUAL VERIFICATION TEST ---")
    print(f"Given Array: {manual_sample}")

    # Deterministic test
    arr_det = manual_sample.copy()
    det_comparisons = 0
    t0 = time.perf_counter()
    quicksort_deterministic(arr_det, 0, len(arr_det) - 1)
    t1 = time.perf_counter()
    det_time = (t1 - t0) * 1e6  # microseconds

    print(f"\n[1] Deterministic QuickSort (Fixed Last Pivot):")
    print(f"    Sorted Output : {arr_det}")
    print(f"    Comparisons   : {det_comparisons}")
    print(f"    Time Taken    : {det_time:.2f} microseconds")

    # Randomized test
    arr_rand = manual_sample.copy()
    rand_comparisons = 0
    t0 = time.perf_counter()
    quicksort_randomized(arr_rand, 0, len(arr_rand) - 1)
    t1 = time.perf_counter()
    rand_time = (t1 - t0) * 1e6

    print(f"\n[2] Randomized QuickSort (Random Pivot):")
    print(f"    Sorted Output : {arr_rand}")
    print(f"    Comparisons   : {rand_comparisons}")
    print(f"    Time Taken    : {rand_time:.2f} microseconds")

    # -----------------------------------------------------------------------
    # Part 2: Algorithmic Complexity Analysis on Varying Datasets
    # -----------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- PART 2: THEORETICAL & EMPIRICAL COMPARISON BENCHMARK ---")
    print("=" * 75)
    size_str = safe_input("Enter benchmark array size N [Default: 1000]: ", "1000")
    try:
        N = int(size_str)
    except ValueError:
        N = 1000

    test_cases = {
        "Already Sorted (Worst-Case for Det)": list(range(1, N + 1)),
        "Reverse Sorted (Worst-Case for Det)": list(range(N, 0, -1)),
        "Random Unsorted Array (Average-Case)": [random.randint(1, 100000) for _ in range(N)]
    }

    print(f"\nBenchmarking with Array Size N = {N}:")
    print("-" * 80)
    print(f"{'Dataset Condition':<35} | {'Variant':<15} | {'Comparisons':<12} | {'Time (ms)':<10}")
    print("-" * 80)

    for case_name, data in test_cases.items():
        # Deterministic run
        d_copy = data.copy()
        det_comparisons = 0
        t0 = time.perf_counter()
        quicksort_deterministic(d_copy, 0, len(d_copy) - 1)
        t1 = time.perf_counter()
        d_ms = (t1 - t0) * 1000

        # Randomized run
        r_copy = data.copy()
        rand_comparisons = 0
        t0 = time.perf_counter()
        quicksort_randomized(r_copy, 0, len(r_copy) - 1)
        t1 = time.perf_counter()
        r_ms = (t1 - t0) * 1000

        print(f"{case_name:<35} | {'Deterministic':<15} | {det_comparisons:<12} | {d_ms:<10.3f}")
        print(f"{'':<35} | {'Randomized':<15} | {rand_comparisons:<12} | {r_ms:<10.3f}")
        print("-" * 80)

    # -----------------------------------------------------------------------
    # Part 3: Theoretical Summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("                 THEORETICAL COMPLEXITY SUMMARY")
    print("=" * 75)
    print("Metric                 | Deterministic Quick Sort | Randomized Quick Sort")
    print("-" * 75)
    print("Best-Case Time         | O(n log n)               | O(n log n)")
    print("Average-Case Time      | O(n log n)               | O(n log n)")
    print("Worst-Case Time        | O(n^2) [Sorted/Reverse]  | O(n log n) Expected*")
    print("Space Complexity       | O(log n) stack (O(n) w.c)| O(log n) stack")
    print("Worst-case Trigger     | Pre-sorted inputs        | Extremely improbable")
    print("=" * 75)
    print("*Note: Randomized QuickSort reduces the probability of worst-case to almost 0.")


if __name__ == "__main__":
    main()
