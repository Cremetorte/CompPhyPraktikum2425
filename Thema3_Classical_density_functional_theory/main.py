
import functions as funcs
import numpy as np
import auswertung as a
import auswertung2 as a2

# -------------------- Variables ------------------
l_list = [3, 10]
N = 1000
eta_list = np.arange(0.1,1,0.1)

surface_tension = {}



def run_all(jit = True):
    funcs.use_numba = jit
    for l in l_list:
        for eta in eta_list:
            eta = round(eta, 1)

            solved_rho = funcs.solve_rho(N, l, eta)
            # funcs.plot_rho(solved_rho, l, f"Output/{l=}_{eta=}.png")
            
            surface_tension[f"{l=}_{eta=}"] = (a2.surf_tension_num(solved_rho, l), a2.surf_tension_an(solved_rho,l))

    for i in surface_tension:
        print(f"{i}: numerically: {surface_tension[i][0]:.4e}, analytically: {surface_tension[i][1]:.4e}")



if __name__ == "__main__":
    # funcs.precompile()
    run_all()