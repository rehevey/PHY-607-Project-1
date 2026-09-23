# Physics Integration Project

Numerical solutions to two physics problems, each compared against an
analytic (closed-form) solution:

1. **ODE problem — RC circuit discharge.**
   `dQ/dt = -Q / (RC)`, solved with a hand-written Euler's method,
   a hand-written 4th-order Runge-Kutta method, and SciPy's `solve_ivp`.

2. **Definite integral problem — electric potential energy.**
   `W = integral from R to r_max of k*q1*q2 / r^2 dr` (a stand-in for
   the improper integral out to infinity), approximated with a
   hand-written Riemann sum, trapezoidal rule, and Simpson's rule, with
   the trapezoidal and Simpson results also checked against SciPy's
   `trapezoid` and `simpson` functions.

## Folder structure

```
physics_integration_project/
├── README.md
├── requirements.txt
├── main_ode.py            # produces all ODE results/figures
├── main_integral.py        # produces all integral results/figures
├── ode/
│   ├── __init__.py
│   ├── rc_circuit.py       # ODE right-hand side + analytic solution
│   └── solvers.py          # Euler, RK4, SciPy wrapper
├── integral/
│   ├── __init__.py
│   ├── potential_energy.py # integrand + analytic solution
│   └── integrators.py      # Riemann, trapezoid, Simpson, SciPy wrappers
└── figures/                # created automatically; holds saved plots
```

## Dependencies

- Python 3.9+
- numpy
- scipy
- matplotlib

Install with:

```bash
pip install -r requirements.txt
```

## How to run

From the `physics_integration_project/` folder:

```bash
python main_ode.py
python main_integral.py
```

Each script runs with no arguments required and will:
- Print a table comparing each numerical method to the analytic solution
- Save all figures into the `figures/` folder

## Changing parameters

Both scripts accept optional command-line arguments so you can explore
different physical scenarios without editing any code. Defaults are
defined in `ode/rc_circuit.py` (`DEFAULT_PARAMS`) and
`integral/potential_energy.py` (`DEFAULT_PARAMS`).

Examples:

```bash
# RC circuit: change resistance, capacitance, initial charge, and step count
python main_ode.py --R 500 --C 0.002 --Q0 2.0 --t_end 20 --n_steps 400

# Potential energy: use opposite-sign charges and a larger truncated bound
python main_integral.py --q1 2e-6 --q2 -1e-6 --R 0.05 --r_max 1000 --n_points 1000
```

## Switching integration methods

Both problems use a "registry" dictionary (`ODE_METHODS` in
`ode/solvers.py`, and `INTEGRATION_METHODS` in `integral/integrators.py`)
mapping method names to functions with an identical interface. To add or
swap a method, add a new function with the same signature and register
it in the corresponding dictionary — no other code needs to change.
