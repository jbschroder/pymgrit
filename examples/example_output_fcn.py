"""
Access and plot the solution
"""

import pathlib
import numpy as np
import matplotlib.pyplot as plt

from pymgrit.dahlquist.dahlquist import Dahlquist
from pymgrit.core.simple_setup_problem import simple_setup_problem
from pymgrit.core.mgrit import Mgrit


def main():
    # Define output function that writes the solution to a file
    def output_fcn(self):
        # Set path to solution
        path = 'results/' + 'dahlquist'
        # Create path if not existing
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        # Save solution to file; here, we just have a single solution value at each time point
        np.save(path + '/' + str(self.t[0][0]) + ':' + str(self.t[0][-1]),  # Local time interval for distinguishing procs
                [self.u[0][i].get_values() for i in self.index_local[0]])   # Save solution values at local time points

    # Create Dahlquist's test problem with 101 time steps in the interval [0, 5]
    dahlquist = Dahlquist(t_start=0, t_stop=5, nt=101)

    # Construct a two-level multigrid hierarchy for the test problem using a coarsening factor of 2
    dahlquist_multilevel_structure = simple_setup_problem(problem=dahlquist, level=2, coarsening=2)

    # Set up the MGRIT solver for the test problem and set the output function
    mgrit = Mgrit(problem=dahlquist_multilevel_structure, output_fcn=output_fcn)

    # Solve the test problem
    info = mgrit.solve()

    # Plot the solution
    t = np.linspace(dahlquist.t_start, dahlquist.t_end, dahlquist.nt)
    sol = np.load('results/dahlquist/0.0:5.0.npy')
    plt.plot(t, sol)
    plt.xlabel('t')
    plt.ylabel('u(t)')
    plt.show()


if __name__ == '__main__':
    main()
