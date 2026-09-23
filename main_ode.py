"""
main_ode.py

Produces all results for the RC circuit ODE problem:
    - Solves dQ/dt = -Q/(RC) using Euler, RK4, and SciPy's solve_ivp
    - Compares each against the analytic solution Q(t) = Q0 * exp(-t/RC)
    - Prints a table of errors
    - Saves a comparison plot and an error-vs-step-size convergence plot

Run with no arguments to reproduce the default results:
    python main_ode.py

Optional arguments let you override the default physical parameters
without editing this file, e.g.:
    python main_ode.py --Q0 2.0 --R 500 --C 0.002 --t_end 20 --n_steps 400
"""

import argparse
import os

import numpy as np
import matplotlib.pyplot as plt

from ode.rc_circuit import dQdt, analytic_solution, DEFAULT_PARAMS
from ode.solvers import ODE_METHODS

FIGURE_DIR = "figures"


def parse_args():
    parser = argparse.ArgumentParser(description="RC circuit ODE demo")
    parser.add_argument("--R", type=float, default=DEFAULT_PARAMS["R"])
    parser.add_argument("--C", type=float, default=DEFAULT_PARAMS["C"])
    parser.add_argument("--Q0", type=float, default=DEFAULT_PARAMS["Q0"])
    parser.add_argument("--t_start", type=float, default=DEFAULT_PARAMS["t_start"])
    parser.add_argument("--t_end", type=float, default=DEFAULT_PARAMS["t_end"])
    parser.add_argument("--n_steps", type=int, default=DEFAULT_PARAMS["n_steps"])
    return parser.parse_args()


def run_comparison(params):
    """Run all three ODE methods and return their (t, Q) results."""
    results = {}
    for name, solver in ODE_METHODS.items():
        t, Q = solver(
            dQdt,
            params["Q0"],
            params["t_start"],
            params["t_end"],
            params["n_steps"],
            params["R"],
            params["C"],
        )
        results[name] = (t, Q)
    return results


def print_error_table(results, params):
    """Print max absolute error of each method vs. the analytic solution."""
    print("\nMethod comparison (max absolute error vs. analytic solution)")
    print("-" * 55)
    for name, (t, Q) in results.items():
        Q_true = analytic_solution(t, params["Q0"], params["R"], params["C"])
        max_err = np.max(np.abs(Q - Q_true))
        print(f"{name:>15s} : max|error| = {max_err:.6e}")


def plot_solutions(results, params):
    """Plot each numerical solution against the analytic curve."""
    os.makedirs(FIGURE_DIR, exist_ok=True)

    t_fine = np.linspace(params["t_start"], params["t_end"], 1000)
    Q_true = analytic_solution(t_fine, params["Q0"], params["R"], params["C"])

    plt.figure(figsize=(7, 5))
    plt.plot(t_fine, Q_true, "k-", label="Analytic", linewidth=2)
    for name, (t, Q) in results.items():
        plt.plot(t, Q, "--", marker="o", markersize=3, label=name)

    plt.xlabel("Time (s)")
    plt.ylabel("Charge Q(t) (C)")
    plt.title("RC Circuit Discharge: Numerical vs. Analytic")
    plt.legend()
    plt.tight_layout()
    outpath = os.path.join(FIGURE_DIR, "ode_solution_comparison.png")
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Saved solution comparison plot to {outpath}")


def plot_convergence(params):
    """Plot max error vs. number of steps for Euler and RK4."""
    os.makedirs(FIGURE_DIR, exist_ok=True)

    step_counts = [10, 20, 50, 100, 200, 500, 1000]
    errors = {"euler": [], "rk4": []}

    for n_steps in step_counts:
        for name in ("euler", "rk4"):
            solver = ODE_METHODS[name]
            t, Q = solver(
                dQdt, params["Q0"], params["t_start"], params["t_end"],
                n_steps, params["R"], params["C"],
            )
            Q_true = analytic_solution(t, params["Q0"], params["R"], params["C"])
            errors[name].append(np.max(np.abs(Q - Q_true)))

    plt.figure(figsize=(7, 5))
    for name, err in errors.items():
        plt.loglog(step_counts, err, "o-", label=name)
    plt.xlabel("Number of steps")
    plt.ylabel("Max absolute error")
    plt.title("ODE Convergence: Error vs. Number of Steps")
    plt.legend()
    plt.tight_layout()
    outpath = os.path.join(FIGURE_DIR, "ode_convergence.png")
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Saved convergence plot to {outpath}")


def main():
    args = parse_args()
    params = vars(args)

    results = run_comparison(params)
    print_error_table(results, params)
    plot_solutions(results, params)
    plot_convergence(params)


if __name__ == "__main__":
    main()
