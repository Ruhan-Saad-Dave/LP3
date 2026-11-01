"""
=============================================================================
Assignment: DAA 4 (Group A)
Title: Write a program to solve a 0-1 Knapsack problem using dynamic 
       programming or branch and bound strategy.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""


def solve_01_knapsack_dp(weights, values, capacity):
    """
    Solves the 0-1 Knapsack Problem using Dynamic Programming (Tabulation).
    
    Recurrence Relation (as given in Lab Manual Page 39):
        T(i, j) = max(T(i-1, j), value_i + T(i-1, j - weight_i))  if weight_i <= j
        T(i, j) = T(i-1, j)                                       otherwise
        
        Where:
            T(i, j) = maximum profit possible using a subset of items {1..i}
                      with weight capacity restriction j.
                      
    Time Complexity:
        - Table filling: theta(n * W) where n is number of items, W is capacity.
        - Backtracking solution: theta(n)
        - Overall Time Complexity: theta(n * W)
        
    Space Complexity:
        - Table size: theta((n+1) * (W+1)) = theta(n * W)
        
    Returns:
        (max_profit, dp_table, selected_items)
    """
    n = len(weights)

    # Step 1: Draw table 'T' with (n+1) rows and (capacity+1) columns filled with 0s
    dp_table = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Step 2: Fill the table row-wise top to bottom, left to right
    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]
        for j in range(1, capacity + 1):
            if wt <= j:
                dp_table[i][j] = max(dp_table[i - 1][j], val + dp_table[i - 1][j - wt])
            else:
                dp_table[i][j] = dp_table[i - 1][j]

    # Step 3: Identify items to be put into knapsack (Traceback)
    max_profit = dp_table[n][capacity]
    selected_items = []
    w = capacity

    for i in range(n, 0, -1):
        if dp_table[i][w] != dp_table[i - 1][w]:
            # Item i (1-indexed) was selected
            selected_items.append(i)
            w -= weights[i - 1]  # Deduct weight of chosen item

    selected_items.reverse()  # Order items ascending by index
    return max_profit, dp_table, selected_items


def print_t_table(dp_table, weights, values, capacity):
    """
    Prints the formatted Dynamic Programming Lookup Table (T-Table)
    matching the layout in the Lab Manual Page 42.
    """
    print("\n" + "=" * 65)
    print("       DYNAMIC PROGRAMMING TABLE (T-Table)")
    print("=" * 65)

    header = f"{'Item (wt,val)':<15} | " + " ".join([f"{c:^6}" for c in range(capacity + 1)])
    print(header)
    print("-" * len(header))

    for i, row in enumerate(dp_table):
        if i == 0:
            label = "0 (Base)"
        else:
            label = f"Item {i} ({weights[i-1]},{values[i-1]})"
        row_str = f"{label:<15} | " + " ".join([f"{val:^6}" for val in row])
        print(row_str)
    print("-" * len(header))


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


def main():
    print("=" * 70)
    print("   DAA Assignment 4: 0-1 Knapsack Problem (Dynamic Programming)")
    print("=" * 70)

    print("Choose mode:")
    print("  1. Run with Lab Manual Problem (Capacity = 5 kg, n = 4 items) [Default]")
    print("  2. Enter custom knapsack capacity and items")
    choice = safe_input("Enter choice (1/2) [Default: 1]: ", "1")

    if choice == "2":
        try:
            capacity = int(safe_input("\nEnter Knapsack Capacity (W): ", "5"))
            n = int(safe_input("Enter number of items (n): ", "4"))
            weights = []
            values = []
            for i in range(1, n + 1):
                w = int(safe_input(f"  Item {i} - Enter weight: ", "2"))
                v = int(safe_input(f"  Item {i} - Enter value/profit: ", "3"))
                weights.append(w)
                values.append(v)
        except ValueError:
            print("Invalid input! Falling back to Lab Manual example problem.")
            capacity = 5
            weights = [2, 3, 4, 5]
            values = [3, 4, 5, 6]
    else:
        # Exact problem from Lab Manual Page 39:
        # Knapsack capacity (w) = 5 kg, n = 4 items
        # (w1, w2, w3, w4) = (2, 3, 4, 5)
        # (b1, b2, b3, b4) = (3, 4, 5, 6)
        capacity = 5
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]

    print("\n" + "-" * 60)
    print("GIVEN DATASET:")
    print("-" * 60)
    print(f"Knapsack Capacity (W) : {capacity} kg")
    print(f"Number of Items (n)   : {len(weights)}")
    print(f"{'Item ID':<10} | {'Weight (kg)':<12} | {'Value / Profit':<15}")
    print("-" * 60)
    for i in range(len(weights)):
        print(f"Item {i + 1:<5} | {weights[i]:<12} | {values[i]:<15}")
    print("-" * 60)

    # Solve 0-1 Knapsack
    max_profit, dp_table, selected_items = solve_01_knapsack_dp(weights, values, capacity)

    # Print T-Table
    print_t_table(dp_table, weights, values, capacity)

    # Compute total weight of selected items
    total_selected_weight = sum(weights[idx - 1] for idx in selected_items)
    selected_items_str = ", ".join([f"Item-{idx}" for idx in selected_items])

    print("\n" + "=" * 65)
    print("                     OPTIMAL SOLUTION")
    print("=" * 65)
    print(f"Maximum Profit (Value)   : {max_profit} units")
    print(f"Total Weight Used        : {total_selected_weight} kg / {capacity} kg")
    print(f"Included Items           : {selected_items_str}")
    print(f"Details of Selected Items:")
    for idx in selected_items:
        print(f"  - Item-{idx}: Weight = {weights[idx-1]} kg, Value = {values[idx-1]} units")
    print("-" * 65)
    print("Time Complexity          : theta(n * W)")
    print("Space Complexity         : theta(n * W) for DP lookup table")
    print("=" * 65)


if __name__ == "__main__":
    main()
