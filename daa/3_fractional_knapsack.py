"""
=============================================================================
Assignment: DAA 3 (Group A)
Title: Write a program to solve a fractional Knapsack problem using a 
       greedy method.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""


class Item:
    """Represents an item with an ID, weight, value, and value-to-weight ratio."""
    def __init__(self, item_id, weight, value):
        self.item_id = item_id
        self.weight = weight
        self.value = value
        self.ratio = value / weight


def fractional_knapsack(capacity, items):
    """
    Solves Fractional Knapsack problem using the Greedy approach.
    
    Greedy Strategy:
        1. Compute the value-to-weight ratio for each item.
        2. Sort all items in descending order of their ratios.
        3. Greedily place the item with the highest ratio into the knapsack.
           If the remaining capacity cannot fit the whole item, take the fraction
           needed to fill the knapsack completely.
           
    Time Complexity:
        - Sorting items: O(n log n)
        - Greedy selection loop: O(n)
        - Total Time Complexity: O(n log n)
    Space Complexity:
        - Auxiliary Space: O(1) if sorting in-place, or O(n) for storing fractions.
        
    Returns:
        (total_value, total_weight_used, solution_details)
    """
    # Step 1 & 2: Sort items in descending order of ratio (v_i / w_i)
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)

    remaining_capacity = capacity
    total_value = 0.0
    total_weight_used = 0.0
    solution_details = []

    for item in sorted_items:
        if remaining_capacity <= 0:
            break

        if item.weight <= remaining_capacity:
            # Take entire item (fraction = 1.0)
            fraction = 1.0
            weight_taken = item.weight
            value_taken = item.value
        else:
            # Take fraction of the item to fill the remaining capacity
            fraction = remaining_capacity / item.weight
            weight_taken = remaining_capacity
            value_taken = item.value * fraction

        remaining_capacity -= weight_taken
        total_weight_used += weight_taken
        total_value += value_taken

        solution_details.append({
            "item_id": item.item_id,
            "weight": item.weight,
            "value": item.value,
            "ratio": item.ratio,
            "fraction": fraction,
            "weight_taken": weight_taken,
            "value_taken": value_taken,
            "remaining_cap": remaining_capacity
        })

    return total_value, total_weight_used, solution_details


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


def main():
    print("=" * 75)
    print("      DAA Assignment 3: Fractional Knapsack Problem (Greedy Method)")
    print("=" * 75)

    # Offer user choice: use Lab Manual default dataset or enter custom items
    print("Choose mode:")
    print("  1. Run with Lab Manual Problem (Capacity = 60 kg, n = 5 items) [Default]")
    print("  2. Enter custom knapsack capacity and items")
    choice = safe_input("Enter choice (1/2) [Default: 1]: ", "1")

    if choice == "2":
        try:
            capacity = float(safe_input("\nEnter Knapsack Capacity (W in kg): ", "60"))
            n = int(safe_input("Enter number of items (n): ", "5"))
            items = []
            for i in range(1, n + 1):
                w = float(safe_input(f"  Item {i} - Enter weight: ", "10"))
                v = float(safe_input(f"  Item {i} - Enter value/profit: ", "20"))
                items.append(Item(i, w, v))
        except ValueError:
            print("Invalid input! Falling back to Lab Manual example dataset.")
            capacity = 60
            items = [
                Item(1, 5, 30),
                Item(2, 10, 40),
                Item(3, 15, 45),
                Item(4, 22, 77),
                Item(5, 25, 90),
            ]
    else:
        # Exact problem from Lab Manual Page 31:
        # W = 60 kg, n = 5
        capacity = 60
        items = [
            Item(1, 5, 30),
            Item(2, 10, 40),
            Item(3, 15, 45),
            Item(4, 22, 77),
            Item(5, 25, 90),
        ]

    print("\n" + "-" * 75)
    print("GIVEN DATASET:")
    print("-" * 75)
    print(f"Knapsack Capacity (W): {capacity} kg")
    print(f"{'Item ID':<10} | {'Weight (kg)':<12} | {'Value / Profit':<15} | {'Ratio (Value/Weight)':<20}")
    print("-" * 75)
    for it in items:
        print(f"Item {it.item_id:<5} | {it.weight:<12.2f} | {it.value:<15.2f} | {it.ratio:<20.2f}")
    print("-" * 75)

    # Solve Fractional Knapsack
    max_value, total_weight, details = fractional_knapsack(capacity, items)

    # Display Step-by-Step Selection Table
    print("\n" + "-" * 85)
    print("GREEDY SELECTION & KNAPSACK FILLING TABLE (Sorted by Ratio):")
    print("-" * 85)
    print(f"{'Item ID':<8} | {'Weight':<8} | {'Value':<8} | {'Ratio':<8} | {'Fraction':<12} | {'Weight Taken':<14} | {'Profit Added':<14}")
    print("-" * 85)
    for step in details:
        frac_str = f"{step['fraction'] * 100:.1f}% ({step['fraction']:.2f})"
        print(f"Item {step['item_id']:<3} | {step['weight']:<8.1f} | {step['value']:<8.1f} | {step['ratio']:<8.2f} | {frac_str:<12} | {step['weight_taken']:<14.2f} | {step['value_taken']:<14.2f}")
    print("-" * 85)

    # Display Summary Results
    print("\n" + "=" * 75)
    print("                         OPTIMAL SOLUTION")
    print("=" * 75)
    print(f"Total Weight in Knapsack : {total_weight:.2f} kg / {capacity:.2f} kg")
    print(f"Maximum Value / Profit   : {max_value:.2f} units")
    
    # Format subset matching Lab Manual notation: < I1, I2, I5, (20/22) I4 >
    selected_repr = []
    for s in details:
        if abs(s['fraction'] - 1.0) < 1e-6:
            selected_repr.append(f"I{s['item_id']}")
        else:
            selected_repr.append(f"({s['weight_taken']:.0f}/{s['weight']:.0f}) I{s['item_id']}")
    print(f"Items in Knapsack        : < {', '.join(selected_repr)} >")
    print("Time Complexity          : O(n log n) [Dominated by sorting]")
    print("Space Complexity         : O(1) auxiliary [or O(n) to store items]")
    print("=" * 75)


if __name__ == "__main__":
    main()
