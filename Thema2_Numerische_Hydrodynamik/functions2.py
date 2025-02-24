import numpy as np

# Aufgabe 2

# Berechnung Delta roh, Delta u, Delta epsilon
def compute_delta_variable(variable, N, j):
    delta_variable = np.zeros(N+4)
    num = (variable[j+1] - variable[j]) * (variable[j] - variable[j-1])
    if num > 0:
        delta_variable = 2*num / ((variable[j+1] - variable[j-1]) + 1e-12)
    else:
        delta_variable = 0
    return delta_variable

# erweitertes Upwindverfahren; variable_adv für rho und epsilon
def variable_adv(variable, N, dt, dx, u, j):
    if u[j] > 0:
        delta_variable_j_1 = compute_delta_variable(variable, N, j-1)
        variable_adv = variable[j-1] + 0.5 * (1 - u[j] * dt/dx) * delta_variable_j_1
    else:
        delta_variable_j = compute_delta_variable(variable, N, j)
        variable_adv = variable[j] - 0.5 * (1 + u[j] * dt/dx) * delta_variable_j
    return variable_adv

# erweitertes Upwindverfahren für u_adv
def u_adv(u, N, dt, dx, j):
    u_mean = np.zeros(N+4)
    u_mean[j] = 0.5 * (u[j] + u[j+1])
    if u_mean[j] > 0:
        delta_u_j = compute_delta_variable(u, N, j)
        variable_adv = u[j] + 0.5 * (1 - u_mean[j] * dt/dx) * delta_u_j
    else:
        delta_u_j1 = compute_delta_variable(u, N, j+1)
        variable_adv = u[j+1] - 0.5 * (1 + u_mean[j] * dt/dx) * delta_u_j1
    return variable_adv

# Berechnung der Flüsse
def compute_F(rho, u, epsilon, N, dt, dx):
    F_m = np.zeros(N+5)
    F_i = np.zeros(N+4)
    F_e = np.zeros(N+5)
    for j in range(2, N+2):
        F_m[j] = u[j] * variable_adv(rho, N, dt, dx, u, j)
        F_e[j] = F_m[j] * variable_adv(epsilon, N, dt, dx, u, j)
    for j in range(2, N+3):
        F_i[j] = 0.5 * (F_m[j] + F_m[j+1]) * u_adv(u, N, dt, dx, j)
    return F_m, F_i, F_e

# Lösung des Stoßrohrs
def solve_shock_tube(rho, u, epsilon, p, N, dt, dx, T_end, gamma):
    t = 0
    while t < T_end:
        rho_mean = np.zeros(N+5)
        rho_mean_new = np.zeros(N+5)

        rho_new, u_new, epsilon_new, p_new = np.copy(rho), np.copy(u), np.copy(epsilon), np.copy(p)

        # Reflektierende Randbedingungen
        u_new[2], u_new[1] = 0, -u_new[3]
        u_new[N+2], u_new[N+3] = 0, -u_new[N+1]
        rho_new[1], rho_new[0] = rho_new[2], rho_new[3]
        rho_new[N+2], rho_new[N+3] = rho_new[N+1], rho_new[N]
        epsilon_new[1], epsilon_new[0] = epsilon_new[2], epsilon_new[3]
        epsilon_new[N+2], epsilon_new[N+3] = epsilon_new[N+1], epsilon_new[N]
        p_new[1], p_new[0] = p_new[2], p_new[3]
        p_new[N+2], p_new[N+3] = p_new[N+1], p_new[N]

        # Berechnung der Flüsse
        F_m, F_i, F_e = compute_F(rho, u, epsilon, N, dt, dx)

        # reflektierende Randbedingungen
        F_m[1], F_m[0] = F_m[2], F_m[3]
        F_m[N+2], F_m[N+3] = F_m[N+1], F_m[N]
        #F_i[1], F_i[0] = F_i[2], F_i[3]
        #F_i[N+2], F_i[N+3] = F_i[N+1], F_i[N]
        F_i[2], F_i[1] = 0, -F_i[3]
        F_i[N+2], F_i[N+3] = 0, -F_i[N+1]
        F_e[1], F_e[0] = F_e[2], F_e[3]
        F_e[N+2], F_e[N+3] = F_e[N+1], F_e[N]

        # Advektionsschritt
        for j in range(1, N+3):
            rho_new[j] = rho[j] - (dt/dx) * (F_m[j+1] - F_m[j])
            rho_mean[j] = 0.5 * (rho[j-1] + rho[j]) 
            rho_mean_new[j] = 0.5 * (rho_new[j-1] + rho_new[j])
            u_new[j] = (u[j] * rho_mean[j] - dt/dx * (F_i[j] - F_i[j-1])) / rho_mean_new[j]
            epsilon_new[j] = (epsilon[j] * rho[j] - dt/dx * (F_e[j+1] - F_e[j])) / rho_new[j]

        # Reflektierende Randbedingungen
        u_new[2], u_new[1] = 0, -u_new[3]
        u_new[N+2], u_new[N+3] = 0, -u_new[N+1]
        rho_new[1], rho_new[0] = rho_new[2], rho_new[3]
        rho_new[N+2], rho_new[N+3] = rho_new[N+1], rho_new[N]
        epsilon_new[1], epsilon_new[0] = epsilon_new[2], epsilon_new[3]
        epsilon_new[N+2], epsilon_new[N+3] = epsilon_new[N+1], epsilon_new[N]

        # Kräfte, Druckarbeit
        p_new = (gamma - 1) * rho_new * epsilon_new
        for j in range(2, N+2):
            u_new[j] -= dt/dx * (p_new[j] - p_new[j-1]) / rho_mean_new[j]
        for j in range(2, N+3):    
            epsilon_new[j] -= dt/dx * p_new[j]/rho_new[j] * (u_new[j+1] - u_new[j])


        rho, u, epsilon, p = rho_new, u_new, epsilon_new, p_new
        t += dt

    return rho, u, epsilon, p