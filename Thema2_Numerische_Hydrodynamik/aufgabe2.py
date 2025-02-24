import numpy as np
import matplotlib.pyplot as plt
import functions2

# Parameter
xmin, xmax = 0.0, 1.0
x0 = 0.5
gamma = 1.4
N = 100
T_end = 0.228
dt = 0.001
dx = (xmax - xmin) / N

# staggered grid
x_B = np.linspace(xmin + 0.5*dx, xmax - 0.5*dx, N, endpoint=False) # Zellmitten
x_A = np.linspace(xmin, xmax, N+1) # Zellränder

# Variablen mit Geisterzellen
rho = np.zeros(N+4)
u = np.zeros(N+5)
epsilon = np.zeros(N+4)
p = np.zeros(N+4)

# Anfangsbedingung
rho[:N//2+2] = 1.0  # Links
rho[N//2+2:] = 0.125  # Rechts
p[:N//2+2] = 1.0
p[N//2+2:] = 0.1
epsilon[:N//2+2] = 2.5
epsilon[N//2+2] = 2.0

# Berechnung der Lösung des Stoßrohrs
rho_final, u_final, epsilon_final, p_final = functions2.solve_shock_tube(rho, u, epsilon, p, N, dt, dx, T_end, gamma)
T_final = (gamma - 1) * epsilon_final

# Plot der Ergebnisse
plt.figure(figsize=(12, 10))
plt.plot(x_B, rho_final[2:N+2], label="Dichte", linewidth=2)
plt.plot(x_B, u_final[2:N+2], label="Geschwindigkeit", linewidth=2)
plt.plot(x_B, p_final[2:N+2], label="Druck", linewidth=2)
plt.plot(x_B, T_final[2:N+2], label="Temperatur", linewidth=2)
plt.xlabel("x", fontsize=16)
plt.ylabel("Wert", fontsize=16)
plt.title(f"1D-Stoßrohr-Lösung nach {T_end}s", fontsize=18)
plt.legend(fontsize=14)
plt.grid()
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()