
import functions as funcs
import numpy as np
import auswertung as a
from tabulate import tabulate


# -------------------- Variables ------------------
l_list = [3,10]
N = 1000
eta_list = np.arange(0.1,1,0.1)

table = []



def run_all(jit = True):
    funcs.use_numba = jit
    for l in l_list:
        for eta in eta_list:
            eta = round(eta, 1)

            solved_rho = funcs.solve_rho(N, l, eta)
            # funcs.plot_rho(solved_rho, l, f"Output/{l=}_{eta=}.png")
            # funcs.plot_with_title(solved_rho, l, eta)
            
            # surface_tension[f"{l=}_{eta=}"] = (a.surf_tension_num(solved_rho, l), a.surf_tension_an(solved_rho,l))
            table.append([l, eta, a.surf_tension_num(solved_rho, l), a.surf_tension_an(solved_rho,l), a.excess_adsorption(solved_rho, l, eta)])

    # for i in surface_tension:
    #     print(f"{i}: numerically: {surface_tension[i][0]:.4e}, analytically: {surface_tension[i][1]:.4e}")

    # tabulate
    print(tabulate(table, headers=["L", "eta_0", "surface tension (num.)", "surface tension (ana.)", "Ex. Ads."], floatfmt=(None, ".1f", ".8e", ".8e", ".8e")))


if __name__ == "__main__":
    # funcs.precompile()
    run_all()