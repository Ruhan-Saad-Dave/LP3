"""
=============================================================================
Assignment: ML 4 (Group B)
Title: Implement Gradient Descent Algorithm to find the local minima of a function.
       For example, find the local minima of the function y = (x+3)^2 starting 
       from the point x = 2.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""

import sys
import matplotlib.pyplot as plt
import numpy as np


def objective_function(x):
    """
    Given Function: y = f(x) = (x + 3)^2
    """
    return (x + 3) ** 2


def derivative_function(x):
    """
    First Derivative: dy/dx = f'(x) = 2 * (x + 3)
    """
    return 2 * (x + 3)


def gradient_descent(start_x, learning_rate, precision, max_iterations):
    """
    Executes Gradient Descent algorithm:
    Update rule: x_next = x_current - (learning_rate * dy/dx)
    
    Parameters:
        start_x (float): Initial starting value (specified as x = 2 in manual)
        learning_rate (float): Step size multiplier (eta)
        precision (float): Stopping criteria threshold for change in x
        max_iterations (int): Maximum allowable iterations
        
    Returns:
        (x_min, history) where history records (iter, x, f(x), grad)
    """
    x_current = start_x
    history = []

    print("\n" + "=" * 80)
    print("                 GRADIENT DESCENT ITERATION PROGRESS")
    print("=" * 80)
    print(f"{'Iter':<6} | {'Current x':<14} | {'f(x)':<14} | {'Gradient dy/dx':<18} | {'Step Size':<14}")
    print("-" * 80)

    for i in range(1, max_iterations + 1):
        grad = derivative_function(x_current)
        step = learning_rate * grad
        fx = objective_function(x_current)

        history.append((i, x_current, fx, grad))

        print(f"{i:<6} | {x_current:<14.6f} | {fx:<14.6f} | {grad:<18.6f} | {abs(step):<14.6f}")

        # Check stopping criteria (convergence threshold)
        if abs(step) < precision:
            print("-" * 80)
            print(f"[*] Convergence achieved at iteration {i} (Step size < {precision})")
            break

        x_current = x_current - step

    return x_current, history


def plot_convergence(history, optimal_x):
    """
    Plots the objective function curve and the optimization trajectory.
    Saves the figure to 'gradient_descent_plot.png'.
    """
    try:
        x_vals = np.linspace(-6, 4, 300)
        y_vals = objective_function(x_vals)

        plt.figure(figsize=(9, 5))
        plt.plot(x_vals, y_vals, 'b-', label=r'$y = (x + 3)^2$')

        # Extract trajectory points
        hist_x = [pt[1] for pt in history]
        hist_y = [pt[2] for pt in history]

        plt.plot(hist_x, hist_y, 'ro-', markersize=5, label='Gradient Descent Steps')
        plt.plot(optimal_x, objective_function(optimal_x), 'g*', markersize=12, label=f'Local Minima ({optimal_x:.3f}, {objective_function(optimal_x):.3f})')

        plt.title('Gradient Descent Optimization for $y = (x + 3)^2$', fontsize=13)
        plt.xlabel('x', fontsize=11)
        plt.ylabel('y', fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig('gradient_descent_plot.png')
        plt.close()
        print("\n[+] Optimization trajectory plot saved to 'gradient_descent_plot.png'")
    except Exception as e:
        print(f"\n[!] Note: Plotting skipped ({e})")


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


def main():
    print("=" * 80)
    print("   ML Assignment 4: Gradient Descent to find Local Minima of y = (x+3)^2")
    print("=" * 80)

    # Problem statement parameters from Lab Manual
    start_x_str = safe_input("Enter starting point x [Manual Example: 2.0]: ", "2.0")
    eta_str = safe_input("Enter learning rate (eta) [Default: 0.1]: ", "0.1")
    max_iter_str = safe_input("Enter max iterations [Default: 50]: ", "50")

    try:
        start_x = float(start_x_str)
        eta = float(eta_str)
        max_iters = int(max_iter_str)
    except ValueError:
        print("Invalid input. Using default parameters.")
        start_x, eta, max_iters = 2.0, 0.1, 50

    precision = 1e-6

    print(f"\nOptimization Setup:")
    print(f"  Function              : y = (x + 3)^2")
    print(f"  Derivative dy/dx      : 2 * (x + 3)")
    print(f"  Initial Point x0      : {start_x}")
    print(f"  Learning Rate (eta)   : {eta}")
    print(f"  Stopping Tolerance    : {precision}")
    print(f"  Max Iterations        : {max_iters}")

    optimal_x, history = gradient_descent(start_x, eta, precision, max_iters)
    optimal_y = objective_function(optimal_x)

    print("\n" + "=" * 80)
    print("                             OPTIMIZATION RESULTS")
    print("=" * 80)
    print(f"  Starting Point x0          : {start_x}")
    print(f"  Final Local Minima (x)     : {optimal_x:.6f}")
    print(f"  Minimum Function Value y   : {optimal_y:.6e}")
    print(f"  Exact Analytical Minimum   : x = -3.000000, y = 0.000000")
    print(f"  Absolute Error |x - (-3)|  : {abs(optimal_x - (-3.0)):.6e}")
    print(f"  Total Iterations Executed  : {len(history)}")
    print("=" * 80)

    plot_convergence(history, optimal_x)


if __name__ == "__main__":
    main()
