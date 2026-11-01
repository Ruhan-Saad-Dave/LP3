"""
=============================================================================
Assignment: DAA 1 (Group A)
Title: Write a program to calculate Fibonacci numbers using non-recursive 
       and recursive methods, find their step count, and analyze their 
       time and space complexity.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""

import sys


# ---------------------------------------------------------------------------
# Method 1: Non-Recursive (Iterative / Space-Optimized Dynamic Programming)
# ---------------------------------------------------------------------------
def fibonacci_non_recursive(n):
    """
    Calculates the n-th Fibonacci number non-recursively (iteratively)
    and prints the sequence up to n terms.
    
    Time Complexity:  O(n) - Linear time (single loop of n iterations)
    Space Complexity: O(1) - Constant auxiliary space (only 2 variables used)
    
    Returns:
        (sequence, nth_term, step_count)
    """
    if n <= 0:
        return [], 0, 1

    sequence = []
    step_count = 0

    n1, n2 = 0, 1
    count = 0

    step_count += 1  # initialization step

    if n == 1:
        sequence.append(n1)
        step_count += 1
        return sequence, n1, step_count

    while count < n:
        sequence.append(n1)
        nth = n1 + n2
        # update values
        n1 = n2
        n2 = nth
        count += 1
        step_count += 1  # loop iteration step

    return sequence, sequence[-1], step_count


# ---------------------------------------------------------------------------
# Method 2: Recursive Method
# ---------------------------------------------------------------------------
recursive_step_count = 0

def fibonacci_recursive(n):
    """
    Calculates the n-th Fibonacci number using pure recursion.
    
    Recurrence Relation: F(n) = F(n-1) + F(n-2) for n > 1
    Base Cases: F(0) = 0, F(1) = 1
    
    Time Complexity:  O(2^n) - Exponential time (binary recursion tree)
    Space Complexity: O(n)   - Auxiliary call stack space
    
    Returns:
        n-th Fibonacci number
    """
    global recursive_step_count
    recursive_step_count += 1

    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def get_recursive_sequence(n):
    """
    Generates Fibonacci sequence up to n terms using the recursive function.
    """
    global recursive_step_count
    recursive_step_count = 0
    sequence = [fibonacci_recursive(i) for i in range(n)]
    return sequence, sequence[-1] if sequence else 0, recursive_step_count


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


# ---------------------------------------------------------------------------
# Main Execution & Complexity Comparison
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("   DAA Assignment 1: Fibonacci Numbers (Non-Recursive vs Recursive)")
    print("=" * 70)

    user_input = safe_input("Enter number of terms (n) [Default: 7]: ", "7")
    try:
        n = int(user_input)
    except ValueError:
        print("Invalid input! Using default n = 7")
        n = 7

    if n <= 0:
        print("Please enter a positive integer greater than 0.")
        return

    print(f"\nEvaluating Fibonacci Series for n = {n} terms...\n")

    # 1. Non-Recursive Execution
    seq_iter, nth_iter, steps_iter = fibonacci_non_recursive(n)
    print("---------------------------------------------------------------------")
    print("1. NON-RECURSIVE (ITERATIVE) METHOD:")
    print("---------------------------------------------------------------------")
    print(f"Fibonacci Sequence ({n} terms): {seq_iter}")
    print(f"Term F({n - 1}) [0-indexed]     : {nth_iter}")
    print(f"Total Step Count (Iterations) : {steps_iter}")
    print("Time Complexity               : O(n)")
    print("Space Complexity              : O(1) [Space-Optimized]")

    # 2. Recursive Execution
    seq_rec, nth_rec, steps_rec = get_recursive_sequence(n)
    print("\n---------------------------------------------------------------------")
    print("2. RECURSIVE METHOD:")
    print("---------------------------------------------------------------------")
    print(f"Fibonacci Sequence ({n} terms): {seq_rec}")
    print(f"Term F({n - 1}) [0-indexed]     : {nth_rec}")
    print(f"Total Step Count (Calls)      : {steps_rec}")
    print("Time Complexity               : O(2^n) [Exponential]")
    print("Space Complexity              : O(n)   [Call Stack Depth]")

    # 3. Summary Comparison Table (as presented in Lab Manual Page 14)
    print("\n" + "=" * 70)
    print("                   COMPLEXITY ANALYSIS TABLE")
    print("=" * 70)
    print(f"{'Method':<30} | {'Time Complexity':<18} | {'Space Complexity':<15}")
    print("-" * 70)
    print(f"{'Using Recursion':<30} | {'T(n)=T(n-1)+T(n-2)':<18} | {'O(n)':<15}")
    print(f"{'Using DP (Space Optimized)':<30} | {'O(n)':<18} | {'O(1)':<15}")
    print(f"{'Using Memoization (DP)':<30} | {'O(n)':<18} | {'O(n)':<15}")
    print(f"{'Using Matrix Exponentiation':<30} | {'O(log n)':<18} | {'O(1)':<15}")
    print("=" * 70)


if __name__ == "__main__":
    main()
