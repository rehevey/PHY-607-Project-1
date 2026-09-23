
# main_ode.py

# Produces all results for the RC circuit ODE problem:
#    - Solves dQ/dt = -Q/(RC) using Euler, RK4, and SciPy's solve_ivp
#    - Compares each against the analytic solution Q(t) = Q0 * exp(-t/RC)
#    - Prints a table of errors
#    - Saves a comparison plot and an error-vs-step-size convergence plot

# Run with no arguments to reproduce the default results:
#    python main_ode.py

# Optional arguments let you override the default physical parameters
# without editing this file, e.g.:
#    python main_ode.py --Q0 2.0 --R 500 --C 0.002 --t_end 20 --n_steps 400

