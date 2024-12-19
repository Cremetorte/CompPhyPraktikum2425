import functions as funcs

# -------------------- Variables ------------------
l = 10
N = 500
eta = 0.9


initial_rho = funcs.initial_rho(l, eta, N)
# print(funcs.exp_pot(N,l))

# print(funcs.n_1_arr(l, initial_rho))


final_rho = funcs.rho_solver(initial_rho, eta, l)

funcs.plot_array(final_rho, l, eta, "Plot.png")