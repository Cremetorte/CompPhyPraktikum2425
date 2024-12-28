import functions2 as funcs
import elementforelement as ee
import numpy as np

# -------------------- Variables ------------------
l_list = [3, 10]
N = 400
eta_list = np.arange(0.1,1,0.1)

surface_tension = {}


ee.precompile()

for l in l_list:
    for eta in eta_list:
        solved_rho = ee.solve_rho(N, l, eta)
        # ee.plot_rho(solved_rho, l, f"{l=}_{eta=}.png")
        # ee.plot_rho(solved_rho, l, f"{l=}_{eta=}.png")
        surface_tension[f"{l=}_{eta=}"] = (ee.surface_tension(solved_rho, l), ee.surf_tension_homo(eta/l, l))

for i in surface_tension:
    print(f"{i}: {surface_tension[i]}. frac = {surface_tension[i][0]/surface_tension[i][1]}")