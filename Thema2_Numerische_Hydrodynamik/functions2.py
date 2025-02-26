import numpy as np

# Aufgabe 2

# Berechnung Delta roh, Delta u, Delta epsilon
def compute_delta_rho(rho, N):
    delta_rho = np.zeros(N+4)
    for j in range(1, N+3):
        num = (rho[j+1] - rho[j]) * (rho[j] - rho[j-1])
        if num > 0:
            delta_rho[j] = 2*num / ((rho[j+1] - rho[j-1]) + 1e-12)
        else:
            delta_rho[j] = 0
    return delta_rho

def compute_delta_u(u, N):
    delta_u = np.zeros(N+4)
    for j in range(2, N+2):
        num = (u[j+1] - u[j]) * (u[j] - u[j-1])
        if num > 0:
            delta_u[j] = 2*num / ((u[j+1] - u[j-1]) + 1e-12)
        else:
            delta_u[j] = 0
    return delta_u

def compute_delta_epsilon(epsilon, N):
    delta_epsilon = np.zeros(N+4)
    for j in range(1, N+3):
        num = (epsilon[j+1] - epsilon[j]) * (epsilon[j] - epsilon[j-1])
        if num > 0:
            delta_epsilon[j] = 2*num / ((epsilon[j+1] - epsilon[j-1]) + 1e-12)
        else:
            delta_epsilon[j] = 0
    return delta_epsilon

# erweitertes Upwindverfahren; rho_adv, u_adv und epsilon_adv
def compute_rho_adv(rho, N, dt, dx, u):
    delta_rho = compute_delta_rho(rho, N)
    rho_adv = np.zeros(N+4)
    for j in range(2, N+3):
        if u[j] > 0:
            rho_adv[j] = rho[j-1] + 0.5 * (1 - u[j] * dt/dx) * delta_rho[j-1]
        else:
            rho_adv[j] = rho[j] - 0.5 * (1 + u[j] * dt/dx) * delta_rho[j]
    return rho_adv

def compute_u_adv(u, N, dt, dx):
    delta_u = compute_delta_u(u, N)
    u_mean = np.zeros(N+4)
    u_adv = np.zeros(N+4)
    for j in range(2, N+2):
        u_mean[j] = 0.5 * (u[j] + u[j+1])
        if u_mean[j] > 0:
            u_adv[j] = u[j] + 0.5 * (1 - u_mean[j] * dt/dx) * delta_u[j]
        else:
            u_adv[j] = u[j+1] - 0.5 * (1 + u_mean[j] * dt/dx) * delta_u[j+1]
    return u_adv

def compute_epsilon_adv(epsilon, N, dt, dx, u):
    delta_epsilon = compute_delta_epsilon(epsilon, N)
    epsilon_adv = np.zeros(N+4)
    for j in range(2, N+3):
        if u[j] > 0:
            epsilon_adv[j] = epsilon[j-1] + 0.5 * (1 - u[j] * dt/dx) * delta_epsilon[j-1]
        else:
            epsilon_adv[j] = epsilon[j] - 0.5 * (1 + u[j] * dt/dx) * delta_epsilon[j]
    return epsilon_adv

# Berechnung der Flüsse
def compute_F(rho, u, epsilon, N, dt, dx):
    F_m = np.zeros(N+5)
    F_i = np.zeros(N+4)
    F_e = np.zeros(N+5)
    rho_adv = compute_rho_adv(rho, N, dt, dx, u)
    u_adv = compute_u_adv(u, N, dt, dx)
    epsilon_adv = compute_epsilon_adv(epsilon, N, dt, dx, u)
    for j in range(2, N+3):
        F_m[j] = u[j] * rho_adv[j]
        F_e[j] = F_m[j] * epsilon_adv[j]
    for j in range(2, N+2):
        F_i[j] = 0.5 * (F_m[j] + F_m[j+1]) * u_adv[j]
    return F_m, F_i, F_e

# Lösung des Stoßrohrs
def solve_shock_tube(rho, u, epsilon, p, N, dt, dx, T_end, gamma):
    t = 0
    while t < T_end:
        rho_mean = np.zeros(N+5)
        rho_mean_new = np.zeros(N+5)

        rho_new, u_new, epsilon_new, p_new = np.copy(rho), np.copy(u), np.copy(epsilon), np.copy(p)
        
        # Berechnung der Flüsse
        F_m, F_i, F_e = compute_F(rho, u, epsilon, N, dt, dx)

        # Advektionsschritt
        for j in range(2, N+2):
            rho_new[j] = rho[j] - (dt/dx) * (F_m[j+1] - F_m[j])
        for j in range(3, N+2):
            rho_mean[j] = 0.5 * (rho[j-1] + rho[j]) 
            rho_mean_new[j] = 0.5 * (rho_new[j-1] + rho_new[j])
            u_new[j] = (u[j] * rho_mean[j] - dt/dx * (F_i[j] - F_i[j-1])) / rho_mean_new[j]
        for j in range(2, N+2):
            epsilon_new[j] = (epsilon[j] * rho[j] - dt/dx * (F_e[j+1] - F_e[j])) / rho_new[j]

        # Reflektierende Randbedingungen
        u_new[2], u_new[1] = 0, -u_new[3]
        u_new[N+2], u_new[N+3] = 0, -u_new[N+1]
        rho_new[1], rho_new[0] = rho_new[2], rho_new[3]
        rho_new[N+2], rho_new[N+3] = rho_new[N+1], rho_new[N]
        epsilon_new[1], epsilon_new[0] = epsilon_new[2], epsilon_new[3]
        epsilon_new[N+2], epsilon_new[N+3] = epsilon_new[N+1], epsilon_new[N]

        # Kräfte, Druckarbeit
        for j in range(N+4):
            p_new[j] = (gamma - 1) * rho_new[j] * epsilon_new[j]
        utmp = np.copy(u_new)
        for j in range(3, N+2):
            u_new[j] = u_new[j] - dt/dx * (p_new[j] - p_new[j-1]) / rho_mean_new[j]
        for j in range(2, N+2):    
            epsilon_new[j] = epsilon_new[j] - dt/dx * p_new[j]/rho_new[j] * (utmp[j+1] - utmp[j])

        rho, u, epsilon, p = rho_new, u_new, epsilon_new, p_new
        t += dt

    return rho, u, epsilon, p