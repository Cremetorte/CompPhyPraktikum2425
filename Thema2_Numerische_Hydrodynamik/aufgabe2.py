import numpy as np
import matplotlib.pyplot as plt
import functions2
import riemannsolver

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

################################################################
# Analytische Lösung
################################################################

# the Riemann solver
solver = riemannsolver.RiemannSolver(gamma)
# Anzahl der Schritte
numstep = 228

xref = np.arange(-0.5, 0.5, 0.001)

rhoref = [solver.solve(1., 0., 1., 0.125, 0., 0.1, x / (dt * numstep))[0] for x in xref]
uref = [solver.solve(1., 0., 1., 0.125, 0., 0.1, x / (dt * numstep))[1] for x in xref]
pref = [solver.solve(1., 0., 1., 0.125, 0., 0.1, x / (dt * numstep))[2] for x in xref]

# weil die Referenzlösung um 0.5 verschoben ist
xref_shifted = xref + 0.5

fig, ax = plt.subplots(4, figsize=(12, 10))
# Plot der numerischen und analytischen Lösung
ax[0].plot(xref_shifted, rhoref, c='b', linestyle='--', lw=2, label=f'$t={T_end}$')
ax[0].plot(x_B, rho_final[2:N+2], c='r', linestyle=':', label="Dichte", linewidth=2)
ax[1].plot(xref_shifted, uref, lw=2, c='b', linestyle='--', label=f'$t={T_end}$')
ax[1].plot(x_B, u_final[2:N+2], c='r', linestyle=':', label="Geschwindigkeit", linewidth=2)
ax[2].plot(xref_shifted, pref, lw=2, c='b', linestyle='--', label=f'$t={T_end}$')
ax[2].plot(x_B, p_final[2:N+2], c='r', linestyle=':', label="Druck", linewidth=2)
ax[3].plot(x_B, T_final[2:N+2], c='b', linestyle='--', label="Temperatur", linewidth=2)
#pl.plot([cell._midpoint for cell in cells], [cell._density for cell in cells], "k.")
# größere Achsenbeschriftungen
for a in ax:
    a.tick_params(axis='both', labelsize=12)
# dass alle Plots die gleichen ticks haben
yticks = [0, 0.5, 1.0]
for a in ax:
    a.set_yticks(yticks)
    a.tick_params(axis='both', labelsize=12)
ax[2].set_xlabel(r'$x$', fontsize=16)
ax[0].set_title("Numerische vs. analytische Lösung der Stoßwelle", fontsize=18)
ax[0].set_ylim(-0.01,)
ax[2].set_ylim(-0.01,)
ax[1].set_ylim(-0.01,)
ax[0].set_ylabel("density", fontsize=14)
ax[1].set_ylabel("velocity", fontsize=14)
ax[2].set_ylabel("pressure", fontsize=14)
ax[3].set_ylabel("temperature", fontsize=14)
plt.show()
"""
# Plot der Ergebnisse ohne analytische Lösung aber dafür größer
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
"""