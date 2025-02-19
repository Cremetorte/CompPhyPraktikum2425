import numpy as np

# Aufgabe 1.2
# Berechnung von Delta rho bzw. Delta psi (Gleichung 2.16)
def compute_delta_psi(psi, N, j):
    delta_psi = np.zeros(N+4)
    num = (psi[j+1] - psi[j]) * (psi[j] - psi[j-1])
    if num > 0:
        delta_psi = 2*num / ((psi[j+1] - psi[j-1]) + 1e-8)
    else:
        delta_psi = 0
    return delta_psi

# Lösung der Advektionsgleichung
def solve_advection(psi, N, dt, dx, T_end, a):
    t = 0
    while t < T_end:
        psi_new = np.copy(psi)
        F_m = np.zeros(N+5)  # Massenfluss
        #delta_psi = compute_delta_psi(psi, N)

        # Erweitertes Upwind-Verfahren (Gleichung 2.15)
        for j in range(2, N+2):
            u_j = a
            if u_j > 0:
                delta_psi_j_1 = compute_delta_psi(psi, N, j-1)
                psi_adv = psi[j-1] + 0.5 * (1 - u_j * dt/dx) * delta_psi_j_1
            else:
                delta_psi_j = compute_delta_psi(psi, N, j)
                psi_adv = psi[j] - 0.5 * (1 + u_j * dt/dx) * delta_psi_j

            F_m[j] = u_j * psi_adv  # Gleichung 2.14

        # Neues Psi (Gleichung 2.13)
        for j in range(2, N+2):
            psi_new[j] = psi[j] - (dt/dx) * (F_m[j+1] - F_m[j])

        # Periodische Randbedingungen
        psi_new[0] = psi_new[N]
        psi_new[1] = psi_new[N+1]
        psi_new[N+2] = psi_new[2]
        psi_new[N+3] = psi_new[3]

        psi = psi_new
        t += dt

    return psi