import numpy as np
import matplotlib.pyplot as plt
import time
import functions

# Parameter
a = 1.0
xmin, xmax = -1.0, 1.0
N = 40
dx = (xmax - xmin) / N
sigma = 0.8
dt = sigma * dx / a
T_end = 4.0

# staggered grid
x_B = np.linspace(xmin + 0.5*dx, xmax - 0.5*dx, N, endpoint=False) # Zellmitten
x_A = np.linspace(xmin, xmax, N+1) # Zellränder

# Geisterzellen
psi = np.zeros(N+4)
u = np.zeros(N+5)

# Rechteckimpuls
psi[2:N+2] = np.where(np.abs(x_B) <= 1./3, 1.0, 0.0)

# Start der Rechenzeit
start_time = time.time()
    
# Berechnung für t=4
psi_final = functions.solve_advection(psi, N, dt, dx, T_end, a)

# Ende der Rechenzeit
end_time = time.time()
calculation_time = end_time - start_time
print(f"Benötigte Rechenzeit für N={N}: {calculation_time:.6f} Sekunden")

# Berechnung der analytischen Lösung auf feinerem Gitter
def psi_analytisch(x, t, a):
    x_shifted = (x - a * t) % (xmax - xmin) + xmin
    return np.where(np.abs(x_shifted) <= 1./3, 1.0, 0.0)

x_fine = np.arange(xmin, xmax, 0.001)
psi_analytisch_fine = psi_analytisch(x_fine, T_end, a)

# Interpolation der analytischen Lösung auf Gitter der numerischen Lösung
psi_analytisch_interp = np.interp(x_B, x_fine, psi_analytisch_fine)

# Plot der Ergebnisse
plt.figure(figsize=(16, 10))
plt.plot(x_B, psi_final[2:N+2], label="Numerische Lösung", linestyle="--", linewidth=2)
#plt.plot(x_B, psi_analytisch_interp, label="Analytische Lösung", linestyle=":", linewidth=2)
plt.xlabel("x", fontsize=16)
plt.ylabel(f"$\Psi(x, t={T_end})$", fontsize=16)
plt.title(f"Numerische vs. analytische Lösung der Advektionsgleichung mit $N={N}$", fontsize=18)
plt.legend(fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid()
plt.show()