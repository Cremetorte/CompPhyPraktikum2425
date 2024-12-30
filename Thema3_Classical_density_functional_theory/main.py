import functions2 as funcs
import elementforelement as ee
import numpy as np
import auswertung as a

# -------------------- Variables ------------------
l_list = [3, 10]
N = 1000
eta_list = np.arange(0.1,1,0.1)

surface_tension = {}



def run_all(jit = True):
    for l in l_list:
        for eta in eta_list:
            eta = round(eta, 1)

            solved_rho = ee.solve_rho(N, l, eta)
            # ee.plot_rho(solved_rho, l, f"{l=}_{eta=}.png")
            # ee.plot_rho(solved_rho, l, f"{l=}_{eta=}.png")
            surface_tension[f"{l=}_{eta=}"] = (a.surf_tension_num(solved_rho, l, eta), a.surf_tension_anal(eta,l))

    for i in surface_tension:
        print(f"{i}: {surface_tension[i]}. frac = {surface_tension[i][0]/surface_tension[i][1]}")

def run_problematic():
    eta = 0.9
    l = 10
    solved_rho = ee.solve_rho(N,l,eta)


if __name__ == "__main__":
    ee.precompile()
    run_all()
    # run_problematic()