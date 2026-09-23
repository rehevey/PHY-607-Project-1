# main_integral.py

# Produces all results for the electric potential energy integral problem:
#    - Approximates W = integral from R to r_max of k*q1*q2/r^2 dr using
#      Riemann sum, trapezoidal rule, and Simpson's rule (hand-written)
#    - Compares trapezoidal and Simpson's rule against SciPy's versions
#    - Compares all results against the analytic solution W = k*q1*q2/R
#      (in the limit r_max -> infinity)
#    - Prints an error table
#    - Saves a convergence plot (error vs. number of points) and a plot
#      showing how the truncated integral approaches the analytic value
#      as r_max increases

# Run with no arguments to reproduce the default results:
#    python main_integral.py

# Optional arguments let you override the default physical parameters
# without editing this file, e.g.:
#    python main_integral.py --q1 2e-6 --q2 -1e-6 --R 0.05 --r_max 500

