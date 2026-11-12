# XRD Group Messaging Experiments

Research prototypes exploring server-chain assignments for group communication in XRD, a metadata-private messaging system.

Includes greedy assignment strategies, linear-programming heuristics, a mixed-integer formulation, and simulations of group communication success rates.

The experiments live in `xrd_extensions/`, with parameters set near the top of each script. These are standalone research scripts rather than a packaged application: several simulators use Python 2 syntax, the LP heuristics use SciPy, and `mixed_int.py` uses Python-MIP.
