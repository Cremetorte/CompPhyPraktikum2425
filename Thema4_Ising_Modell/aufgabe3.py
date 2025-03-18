import numpy as np
import matplotlib.pyplot as plt

# Funktion zur Initialisierung des Spin-Gitters
def initialize_lattice(L):
    return np.random.choice([-1, 1], size=(L, L))

"""
# Berechnung der Energieänderung ΔE bei Flip eines Spins (Metropolis-Kriterium)
def delta_energy(spins, i, j, J=1, h=0):
    L = spins.shape[0]
    s = spins[i, j]
    # Summe der Nachbarn (oben, unten, links, rechts mit periodischen Randbedingungen)
    neighbor_sum = (
        spins[(i+1) % L, j] + spins[(i-1) % L, j] +
        spins[i, (j+1) % L] + spins[i, (j-1) % L]
    )
    dE = 2 * J * s * neighbor_sum + 2 * h * s  # Energiedifferenz bei Flip
    return dE
"""
    
# Metropolis-Update für das gesamte Gitter (ein Sweep)
def metropolis_sweep(spins, beta, N_try, J=1, h=0):
    L = spins.shape[0]  # Gittergröße
    indices = np.random.permutation(L * L)  # Zufällige Reihenfolge der Spins

    for idx in indices:
        i, j = divmod(idx, L)  # 1D-Index in 2D umwandeln

        s = spins[i, j]
        neighbor_sum = (
            spins[(i+1) % L, j] + spins[(i-1) % L, j] +
            spins[i, (j+1) % L] + spins[i, (j-1) % L]
        )
        dE = 2 * J * s * neighbor_sum + 2 * h * s  # Energieänderung bei Flip

        for _ in range(N_try):
            if dE < 0 or np.random.rand() < np.exp(-beta * dE):  
                spins[i, j] *= -1  # Spin flip

    return spins

# Funktion zur Berechnung von Observablen nach Sweeps
def compute_observables(spins):
    L = spins.shape[0]
    E = 0
    M = np.sum(spins)  # Magnetisierung berechnen
    for i in range(L):
        for j in range(L):
            s = spins[i, j]
            # Energie berechnen (nur rechte und untere Nachbarn zählen, um doppelte Summation zu vermeiden)
            E -= s * (spins[(i+1) % L, j] + spins[i, (j+1) % L])
    return E / (L * L), M / (L * L), abs(M) / (L * L), (M**2) / (L * L)

# Monte-Carlo-Simulation mit Metropolis-Algorithmus
def ising_metropolis(L, beta, N_try, num_sweeps, therm_steps):
    spins = initialize_lattice(L)  # Zufällige Startkonfiguration
    
    # Thermalisation (System ins Gleichgewicht bringen)
    for _ in range(therm_steps):
        spins = metropolis_sweep(spins, beta, N_try)
    
    # Mittelwerte berechnen
    energy_vals, magnet_vals, abs_magnet_vals, magnet_sq_vals = [], [], [], []
    for _ in range(num_sweeps):
        spins = metropolis_sweep(spins, beta, N_try)
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

# Parameter für Aufgabe 3a
L_large = 128  # Großes Gitter
beta_values = np.linspace(0.1, 1, 10)  # Temperaturbereich
N_try = 5  # Anzahl der Versuche pro Spin
N_sweeps = 1000

# Listen zur Speicherung der Ergebnisse
avg_E_values = []
avg_M_values = []
avg_absM_values = []
specific_heat_values = []
for beta in beta_values:
    avg_E, avg_M, avg_absM, avg_Msq, c = ising_metropolis(L_large, beta, N_try, N_sweeps, therm_steps=500)
    avg_E_values.append(avg_E)
    avg_M_values.append(avg_M)
    avg_absM_values.append(avg_absM)
    specific_heat_values.append(c)

print(f"\nMetropolis-Simulation für L = {L_large}:")
for beta in beta_values:
    print(f"β = {beta:.2f} -> ⟨E⟩ = {avg_E:.4f}, ⟨m⟩ = {avg_M:.4f}, ⟨|m|⟩ = {avg_absM:.4f}, c = {c:.4f}")

# Plot der Ergebnisse
plt.figure(figsize=(10, 6))
plt.plot(beta_values, avg_E_values, label="⟨E⟩", color='blue')
plt.plot(beta_values, avg_M_values, label="⟨m⟩", color='red')
plt.plot(beta_values, avg_absM_values, label="⟨|m|⟩", color='green')
plt.plot(beta_values, specific_heat_values, label="c", color='purple')
plt.xlabel("$\\beta$")
plt.ylabel("Observablen")
plt.title(f"Metropolis-Simulation für L = {L_large}")
plt.legend()
plt.grid()
plt.show()
    
# Aufgabe 3b: Simulation für verschiedene Gittergrößen bei β = 0.4406868
beta_critical = 0.4406868
L_sizes = [4, 8, L_large]

"""
print("\nMetropolis-Simulation bei kritischer Temperatur β = 0.4406868:")
for L in L_sizes:
    avg_E, avg_M, avg_absM, avg_Msq, c = ising_metropolis(L, beta_critical, num_sweeps=200000, therm_steps=5000, multihit=5)
    print(f"L = {L} -> ⟨E⟩ = {avg_E:.4f}, ⟨|m|⟩ = {avg_absM:.4f}, ⟨m²⟩ = {avg_Msq:.4f}")"
"""