# Import the Riemann solver library. Note that this will only work if the file
# 'riemannsolver.py' is in the same directory as this script.
import riemannsolver
# Import the Python numerical libraries, as we need them for arange.
import numpy as np
# Import Matplotlib, which we will use to plot the results.
import matplotlib.pyplot as plt

################################################################################
# some global definitions
################################################################################

# the constant adiabatic index
GAMMA = 5./3.

# the Riemann solver
solver = riemannsolver.RiemannSolver(GAMMA)

# the constant time step
timestep = 0.001

# number of steps
numstep = 200

# number of cells
numcell = 100

################################################################################
# the actual program
################################################################################

# reference solution: as the Sod shock problem is in fact a Riemann problem,
# this is just the actual solution of the Riemann problem, evaluated at the
# final time of the simulation.
xref = np.arange(-0.5, 0.5, 0.001)
# rhoref = [solver.solve(1., 0., 1.0, 0.1, 0., 0.1, (x) / (timestep * numstep))[0]  for x in xref]
rhoref = [solver.solve(1., 0., GAMMA-1, 0.1, 0., 0.1*(GAMMA-1), x / (timestep * numstep))[0] for x in xref]
uref = [solver.solve(1., 0., GAMMA-1, 0.1, 0., 0.1*(GAMMA-1), x / (timestep * numstep))[1] for x in xref]
pref = [solver.solve(1., 0., GAMMA-1, 0.1, 0., 0.1*(GAMMA-1), x / (timestep * numstep))[2] for x in xref]


fig, ax = plt.subplots(3)
# plot the reference solution and the actual solution
ax[0].plot(xref, rhoref, c='b', lw=2, label='$t=0.2$')
ax[1].plot(xref, uref, lw=2, c='r', label='$t=0.2$')
ax[2].plot(xref, pref, lw=2, c='orange', label='$t=0.2$')
#pl.plot([cell._midpoint for cell in cells], [cell._density for cell in cells], "k.")
ax[2].set_xlabel(r'$x$')
ax[0].set_ylim(-0.01,1.1)
ax[2].set_ylim(-0.01,)
ax[1].set_ylim(-0.01,0.8)
ax[0].set_ylabel("density")
ax[1].set_ylabel("velocity")
ax[2].set_ylabel("pressure")
# save the plot as a PNG image
#fig.savefig("sodshock_analytical.pdf")
plt.show()