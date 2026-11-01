"""
=============================================================================
Assignment: DAA (Index Sr 5 / Alternate DAA5)
Title: Write a program to generate binomial coefficients using 
       dynamic programming.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""


def binomial_coefficient_dp(n, k):
    """
    Computes Binomial Coefficient C(n, k) using Dynamic Programming (Pascal's Triangle).
    
    Recurrence Relation:
        C(n, k) = C(n-1, k-1) + C(n-1, k)
        Base Cases: C(n, 0) = C(n, n) = 1
        
    Time Complexity:  O(n * k)
    Space Complexity: O(n * k) for 2D DP Table, or O(k) for space-optimized 1D array.
    """
    if k < 0 or k > n:
        return 0, []

    # Initialize (n+1) x (k+1) table
    C = [[0 for _ in range(k + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            # Base cases: C(i, 0) = 1 and C(i, i) = 1
            if j == 0 or j == i:
                C[i][j] = 1
            else:
                # Value is sum of two values directly above in Pascal's Triangle
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    return C[n][k], C


def binomial_coefficient_space_optimized(n, k):
    """
    Computes C(n, k) using 1D array (Space-Optimized DP).
    Time Complexity:  O(n * k)
    Space Complexity: O(k)
    """
    if k < 0 or k > n:
        return 0

    dp = [0] * (k + 1)
    dp[0] = 1  # C(i, 0) = 1

    for i in range(1, n + 1):
        # Iterate backwards to avoid using updated values from current row
        for j in range(min(i, k), 0, -1):
            dp[j] = dp[j] + dp[j - 1]

    return dp[k]


def print_pascals_triangle(table, n, k):
    """Prints the DP table formatted as Pascal's Triangle."""
    print("\n--- Pascal's Triangle / DP Table up to C(n, k) ---")
    for i in range(n + 1):
        row_vals = [f"{table[i][j]:>5}" for j in range(min(i, k) + 1)]
        print(f"Row n={i:>2}: " + " ".join(row_vals))


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


def main():
    print("=" * 70)
    print(" DAA Assignment: Binomial Coefficients using Dynamic Programming")
    print("=" * 70)

    n_str = safe_input("Enter n (total items) [Default: 5]: ", "5")
    k_str = safe_input("Enter k (items to choose) [Default: 2]: ", "2")
    try:
        n = int(n_str)
        k = int(k_str)
    except ValueError:
        n, k = 5, 2

    print(f"\nComputing C({n}, {k}) [n choose k]...")

    res, table = binomial_coefficient_dp(n, k)
    res_opt = binomial_coefficient_space_optimized(n, k)

    print_pascals_triangle(table, n, k)

    print("\n" + "=" * 60)
    print("                      RESULTS")
    print("=" * 60)
    print(f"Value of C({n}, {k}) (2D DP Table)       : {res}")
    print(f"Value of C({n}, {k}) (Space Optimized DP): {res_opt}")
    print("-" * 60)
    print("Time Complexity           : O(n * k)")
    print("Space Complexity (2D DP)  : O(n * k)")
    print("Space Complexity (1D DP)  : O(k) [Space-Optimized]")
    print("=" * 60)


if __name__ == "__main__":
    main()
