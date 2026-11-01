"""
=============================================================================
Assignment: DAA 5 (Group A)
Title: Design n-Queens matrix having first Queen placed. Use backtracking 
       to place remaining Queens to generate the final n-queen's matrix.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""


def print_board(board, n):
    """
    Prints the NxN chessboard matrix in both visual grid and 0/1 binary matrix
    format as described in the Lab Manual (Page 50).
    """
    print("\nVisual Chessboard (Q = Queen, . = Empty):")
    col_header = "    " + "   ".join([f"C{c}" for c in range(n)])
    print(col_header)
    print("  +" + "---+" * n)
    for r in range(n):
        row_str = f"R{r}| " + " | ".join(['Q' if board[r][c] == 1 else '.' for c in range(n)]) + " |"
        print(row_str)
        print("  +" + "---+" * n)

    print("\nBinary Matrix Representation (1 = Queen, 0 = Empty):")
    for r in range(n):
        print("  " + "  ".join(str(board[r][c]) for c in range(n)))


def is_safe(row, col, board, n):
    """
    Checks if a queen can be safely placed at board[row][col].
    According to Lab Manual (Pages 50-54):
    A cell is under attack if:
      1. Another queen exists in the same column.
      2. Another queen exists on the upper-left diagonal.
      3. Another queen exists on the upper-right diagonal.
      4. Another queen exists on the lower-left diagonal.
      5. Another queen exists on the lower-right diagonal.
      (Since the first queen may be placed on any row, we check all 4 diagonal directions).
    """
    # 1. Check column 'col' across all rows
    for r in range(n):
        if r != row and board[r][col] == 1:
            return False

    # 2. Check row 'row' across all columns
    for c in range(n):
        if c != col and board[row][c] == 1:
            return False

    # 3. Check upper-left diagonal
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            return False
        r -= 1
        c -= 1

    # 4. Check upper-right diagonal
    r, c = row - 1, col + 1
    while r >= 0 and c < n:
        if board[r][c] == 1:
            return False
        r -= 1
        c += 1

    # 5. Check lower-left diagonal
    r, c = row + 1, col - 1
    while r < n and c >= 0:
        if board[r][c] == 1:
            return False
        r += 1
        c -= 1

    # 6. Check lower-right diagonal
    r, c = row + 1, col + 1
    while r < n and c < n:
        if board[r][c] == 1:
            return False
        r += 1
        c += 1

    return True


def solve_nqueens_with_first_placed(board, current_row, fixed_row, n):
    """
    Backtracking solver that places remaining queens row by row.
    Skips fixed_row where the 1st Queen was already placed.
    
    Time Complexity:  O(N!) in worst-case backtracking.
    Space Complexity: O(N^2) for board matrix + O(N) recursion stack.
    """
    # If we have reached beyond the last row, all queens are placed!
    if current_row >= n:
        return True

    # If the current row is the one where 1st Queen is already fixed, move to next row
    if current_row == fixed_row:
        return solve_nqueens_with_first_placed(board, current_row + 1, fixed_row, n)

    # Try placing queen in each column of the current row
    for col in range(n):
        if is_safe(current_row, col, board, n):
            board[current_row][col] = 1  # Place Queen

            # Recursively place queens in subsequent rows
            if solve_nqueens_with_first_placed(board, current_row + 1, fixed_row, n):
                return True

            # Backtrack: undo choice
            board[current_row][col] = 0

    return False


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


def main():
    print("=" * 75)
    print("   DAA Assignment 5: N-Queens Matrix with 1st Queen Already Placed")
    print("=" * 75)

    user_n = safe_input("Enter Chessboard Size N (e.g., 4 or 8) [Default: 8]: ", "8")
    try:
        n = int(user_n)
    except ValueError:
        n = 8

    if n in (2, 3):
        print(f"\n[!] Mathematical property: No valid solution exists for N = {n}.")
        return

    # Initialize empty NxN board with 0
    board = [[0 for _ in range(n)] for _ in range(n)]

    # Default position for first Queen
    # For N=4, (0, 1) has a known solution (Lab Manual Page 47-49)
    # For N=8, (0, 0) has a known solution
    default_r = 0
    default_c = 1 if n == 4 else 0

    print(f"\nPlace the 1st Queen on the board (0-indexed indices from 0 to {n-1}):")
    r_input = safe_input(f"Enter Row index for 1st Queen [Default: {default_r}]: ", str(default_r))
    c_input = safe_input(f"Enter Column index for 1st Queen [Default: {default_c}]: ", str(default_c))
    try:
        first_r = int(r_input)
        first_c = int(c_input)
    except ValueError:
        first_r, first_c = default_r, default_c

    if not (0 <= first_r < n and 0 <= first_c < n):
        print(f"Indices out of range! Using default position ({default_r}, {default_c}).")
        first_r, first_c = default_r, default_c

    # Place First Queen
    board[first_r][first_c] = 1
    print(f"\n[+] 1st Queen placed successfully at Position (Row: {first_r}, Col: {first_c}).")
    print("[+] Using backtracking to place remaining {0} Queens...".format(n - 1))

    # Solve using backtracking starting from row 0
    success = solve_nqueens_with_first_placed(board, 0, first_r, n)

    if success:
        print("\n" + "=" * 75)
        print(f"           SUCCESSFUL {n}-QUEENS CONFIGURATION FOUND!")
        print("=" * 75)
        print_board(board, n)

        # Print position tuple (col numbers for each queen, 1-indexed as in Manual Page 49)
        tuple_1indexed = []
        tuple_0indexed = []
        for r in range(n):
            for c in range(n):
                if board[r][c] == 1:
                    tuple_0indexed.append((r, c))
                    tuple_1indexed.append(c + 1)

        print("\nQueen Positions (Row, Column) [0-indexed]:")
        for idx, (r, c) in enumerate(tuple_0indexed, 1):
            mark = " (First Queen Fixed)" if r == first_r and c == first_c else ""
            print(f"  Queen {idx}: Row {r}, Column {c}{mark}")

        print(f"\nManual Tuple Format (1-indexed columns by row): {tuple(tuple_1indexed)}")
    else:
        print("\n" + "=" * 75)
        print(f" [!] No valid solution exists when 1st Queen is placed at ({first_r}, {first_c}).")
        print("=" * 75)
        print("Note: In N-Queens, not every initial placement admits a solution.")
        print(f"For instance, in 4-Queens, placing 1st Queen at (0, 0) has NO solution,")
        print(f"while placing 1st Queen at (0, 1) yields the valid solution (2, 4, 1, 3).")

    print("\n" + "-" * 75)
    print("ALGORITHM COMPLEXITY ANALYSIS:")
    print("  Time Complexity  : O(N!) - Backtracking explores decision tree with pruning")
    print("  Space Complexity : O(N^2) for NxN matrix + O(N) recursion stack")
    print("-" * 75)


if __name__ == "__main__":
    main()
