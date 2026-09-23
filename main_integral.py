"""
main_integral.py

Produces all results for the electric potential energy integral problem:
    - Approximates W = integral from R to r_max of k*q1*q2/r^2 dr using
      Riemann sum, trapezoidal rule, and Simpson's rule (hand-written)
    - Compares trapezoidal and Simpson's rule against SciPy's versions
    - Compares all results against the analytic solution W = k*q1*q2/R
      (in the limit r_max -> infinity)
    - Prints an error table
    - Saves a convergence plot (error vs. number of points) and a plot
      showing how the truncated integral approaches the analytic value
      as r_max increases

Run with no arguments to reproduce the default results:
    python main_integral.py

Optional arguments let you override the default physical parameters
without editing this file, e.g.:
    python main_integral.py --q1 2e-6 --q2 -1e-6 --R 0.05 --r_max 500
"""

import argparse
import os

import numpy as np
import matplotlib.pyplot as plt

from integral.potential_energy import integrand, analytic_solution, DEFAULT_PARAMS
from integral.integrators import INTEGRATION_METHODS

FIGURE_DIR = "figures"


def parse_args():
    parser = argparse.ArgumentParser(description="Electric potential energy integral demo")
    parser.add_argument("--q1", type=float, default=DEFAULT_PARAMS["q1"])
    parser.add_argument("--q2", type=float, default=DEFAULT_PARAMS["q2"])
    parser.add_argument("--R", type=float, default=DEFAULT_PARAMS["R"])
    parser.add_argument("--r_max", type=float, default=DEFAULT_PARAMS["r_max"])
    parser.add_argument("--n_points", type=int, default=DEFAULT_PARAMS["n_points"])
    return parser.parse_args()


def run_comparison(params):
    """Run all integration methods and return {name: value}."""
    results = {}
    for name, method in INTEGRATION_METHODS.items():
        value = method(
            integrand,
            params["R"],
            params["r_max"],
            params["n_points"],
            params["q1"],
            params["q2"],
        )
        results[name] = value
    return results


def print_error_table(results, params, W_true):
    print("\nMethod comparison (vs. analytic W = k*q1*q2/R)")
    print(f"Analytic value: {W_true:.6e} J")
    print("-" * 60)
    for name, value in results.items():
        rel_err = abs(value - W_true) / abs(W_true)
        print(f"{name:>18s} : W = {value: .6e} J   rel. error = {rel_err:.3e}")


def plot_convergence(params, W_true):
    """Plot relative error vs. number of points for each hand-written method."""
    os.makedirs(FIGURE_DIR, exist_ok=True)

    point_counts = [10, 20, 50, 100, 200, 500, 1000, 2000]
    methods_to_plot = ["riemann", "trapezoid", "simpson"]
    errors = {name: [] for name in methods_to_plot}

    for n_points in point_counts:
        for name in methods_to_plot:
            method = INTEGRATION_METHODS[name]
            value = method(
                integrand, params["R"], params["r_max"], n_points,
                params["q1"], params["q2"],
            )
            errors[name].append(abs(value - W_true) / abs(W_true))

    plt.figure(figsize=(7, 5))
    for name, err in errors.items():
        plt.loglog(point_counts, err, "o-", label=name)
    plt.xlabel("Number of sample points")
    plt.ylabel("Relative error")
    plt.title("Integral Convergence: Error vs. Number of Points")
    plt.legend()
    plt.tight_layout()
    outpath = os.path.join(FIGURE_DIR, "integral_convergence.png")
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Saved convergence plot to {outpath}")


def plot_truncation_behavior(params, W_true):
    """Show the truncated integral approaching the analytic value as r_max grows."""
    os.makedirs(FIGURE_DIR, exist_ok=True)

    r_max_values = np.logspace(1, 5, 20)  # from 10 to 100,000
    trapezoid = INTEGRATION_METHODS["trapezoid"]
    values = [
        trapezoid(integrand, params["R"], r_max, params["n_points"],
                  params["q1"], params["q2"])
        for r_max in r_max_values
    ]

    plt.figure(figsize=(7, 5))
    plt.semilogx(r_max_values, values, "o-", label="Truncated integral")
    plt.axhline(W_true, color="k", linestyle="--", label="Analytic (r_max -> infinity)")
    plt.xlabel("r_max (truncated upper bound)")
    plt.ylabel("W (J)")
    plt.title("Approach to Analytic Value as r_max Increases")
    plt.legend()
    plt.tight_layout()
    outpath = os.path.join(FIGURE_DIR, "integral_truncation.png")
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Saved truncation-behavior plot to {outpath}")


def main():
    args = parse_args()
    params = vars(args)

    W_true = analytic_solution(params["R"], params["q1"], params["q2"])

    results = run_comparison(params)
    print_error_table(results, params, W_true)
    plot_convergence(params, W_true)
    plot_truncation_behavior(params, W_true)


if __name__ == "__main__":
    main()
