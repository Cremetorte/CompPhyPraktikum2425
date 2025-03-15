import numpy as np
import aufgabe3

# Aufgabe a)

# Funktion zur Initialisierung des Spin-Gitters
def initialize_lattice(L):
    return np.random.choice([-1, 1], size=(L, L))

# Wärmebad-Update für das gesamte Gitter (ein Sweep)
def heat_bath_sweep(spins, beta, J=1, h=0):
    L = spins.shape[0]
    for i in range(L):
        for j in range(L):
            # Berechnung der Energieänderung ΔE bei Flip eines Spins
            neighbor_sum = (
                spins[(i+1) % L, j] + spins[(i-1) % L, j] +
                spins[i, (j+1) % L] + spins[i, (j-1) % L]
            )
            k = beta * (J * neighbor_sum + h)
            # Berechnung der Wahrscheinlichkeit, den Spin zu flippen
            q = np.exp(-k) / (2 * np.cosh(k))
            r = np.random.rand()  # Zufallszahl für die Akzeptanz
            if r < q:
                spins[i, j] = 1
            else:
                spins[i, j] = -1
    return spins

# Simulation mit dem Wärmebad-Algorithmus
def ising_heat_bath(L, beta, num_sweeps=200000, therm_steps=5000):
    spins = initialize_lattice(L)  # Zufällige Startkonfiguration
    
    # Thermalisation (System ins Gleichgewicht bringen)
    for _ in range(therm_steps):
        spins = heat_bath_sweep(spins, beta)
    
    # Mittelwerte berechnen
    energy_vals, magnet_vals, abs_magnet_vals, magnet_sq_vals = [], [], [], []
    for _ in range(num_sweeps):
        spins = heat_bath_sweep(spins, beta)
        E, M, abs_M, M_sq = compute_observables(spins)
        energy_vals.append(E)
        magnet_vals.append(M)
        abs_magnet_vals.append(abs_M)
        magnet_sq_vals.append(M_sq)
    
    # Mittelwerte berechnen
    avg_E = np.mean(energy_vals)
    avg_M = np.mean(magnet_vals)
    avg_absM = np.mean(abs_magnet_vals)
    avg_Msq = np.mean(magnet_sq_vals)
    
    # Spezifische Wärme berechnen: c = (⟨E²⟩ - ⟨E⟩²) / T²
    specific_heat = (np.var(energy_vals)) / (beta**2)
    
    return avg_E, avg_M, avg_absM, avg_Msq, specific_heat

# Aufgabe 4 b)

# Funktion zur Berechnung der Magnetisierung als Funktion von h
def hysteresis_curve(L, beta, h_initial, h_final, num_sweeps=200000, therm_steps=5000):
    h_values = np.linspace(h_initial, h_final, 50)  # Magnetfeld von h_initial bis h_final
    magnetizations = []
    
    for h in h_values:
        avg_E, avg_M, avg_absM, avg_Msq, c = ising_heat_bath(L, beta, num_sweeps, therm_steps)
        magnetizations.append(avg_M)  # Magnetisierung für jedes h
    
    return h_values, magnetizations

# Beispiel für eine Hysterese-Kurve
L = 32  # Beispielgröße des Gitters
beta = 0.5  # Beispielwert für β
h_initial = 1.0  # Startwert für das Magnetfeld
h_final = -1.0  # Endwert für das Magnetfeld

h_values, magnetizations = hysteresis_curve(L, beta, h_initial, h_final)
print(f"Hysterese-Kurve für L={L}, β={beta}:")
for h, mag in zip(h_values, magnetizations):
    print(f"h = {h:.2f}, ⟨m⟩ = {mag:.4f}")

# Aufgabe 4 c)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Funktion zur Berechnung der Magnetisierung als Funktion von β und h
def magnetization_vs_beta_h(L, beta_values, h_values, num_sweeps=200000, therm_steps=5000):
    magnetizations = np.zeros((len(beta_values), len(h_values)))  # Matrix für Magnetisierung
    
    for i, beta in enumerate(beta_values):
        for j, h in enumerate(h_values):
            avg_E, avg_M, avg_absM, avg_Msq, c = ising_heat_bath(L, beta, num_sweeps, therm_steps)
            magnetizations[i, j] = avg_M  # Magnetisierung für jedes β und h
    
    return magnetizations

# Beispielwerte für β und h
beta_values = np.linspace(0.1, 1, 20)
h_values = np.linspace(-1.0, 1.0, 20)

# Berechnung der Magnetisierung
magnetizations = magnetization_vs_beta_h(32, beta_values, h_values)

# 3D-Plot der Magnetisierung als Funktion von β und h
X, Y = np.meshgrid(h_values, beta_values)
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, magnetizations, cmap='viridis')

ax.set_xlabel('Magnetfeld h')
ax.set_ylabel('β (1/T)')
ax.set_zlabel('Magnetisierung ⟨m⟩')
ax.set_title('Magnetisierung als Funktion von β und h')

plt.show()
