import numpy as np
import matplotlib.pyplot as plt
import itertools

# Berechnung der Energie einer Konfiguration
def energie(spins, L, J=1, h=0):
    H = 0
    for i in range(L):
        for j in range(L):
            s = spins[i, j]
            H -= J * s * (spins[(i+1) % L, j] + spins[i, (j+1) % L])  # Periodische Randbedingungen
            H -= h * s  # Externes Magnetfeld
    return H

# Zustandssumme und Mittelwerte berechnen
def ising_direct_sum(L, beta):
    states = list(itertools.product([-1, 1], repeat=L*L))  # Alle möglichen Konfigurationen
    Z, avg_E, avg_absM = 0, 0, 0

    for state in states:
        spins = np.array(state).reshape(L, L)
        H = energie(spins, L)
        M = np.sum(spins)

        weight = np.exp(-beta * H)
        Z += weight
        avg_E += H * weight
        avg_absM += abs(M) * weight

    return avg_E / (Z * L * L), avg_absM / (Z * L * L)  # Normierung durch Z

# Analytische Lösung für L → ∞ aus Onsager (nur für h = 0)
def analytical_energy(beta):
    J = 1
    return -J * (1 + (1 / np.sinh(2 * beta * J)) ** 2)  # Exakte Lösung für große L

def analytical_magnetization(beta):
    J = 1
    beta_c = 0.4406868  # Kritische Temperatur β_c = 1/T_c
    if beta < beta_c:
        return 0
    else:
        return (1 - np.sinh(2 * beta * J) ** (-4)) ** (1/8)

# Simulation für verschiedene L
beta_values = np.linspace(0.1, 1, 20)
L_values = [2, 3, 4]

energies = {L: [] for L in L_values}
magnetizations = {L: [] for L in L_values}

# Berechnung der numerischen Werte für L = 2, 3, 4
for beta in beta_values:
    for L in L_values:
        E, absM = ising_direct_sum(L, beta)
        energies[L].append(E)
        magnetizations[L].append(absM)

# Berechnung der analytischen Werte
E_analytic = [analytical_energy(beta) for beta in beta_values]
M_analytic = [analytical_magnetization(beta) for beta in beta_values]

# -----------------------
# 📌 Plot: Energie vs. β
# -----------------------
plt.figure(figsize=(8, 5))
for L in L_values:
    plt.plot(beta_values, energies[L], 'o-', label=f"L = {L}")

plt.plot(beta_values, E_analytic, 'k--', label="Analytische Lösung (L → ∞)")
plt.xlabel("Inverse Temperatur β")
plt.ylabel("⟨E⟩ / L²")
plt.title("Energie vs. Temperatur für verschiedene L")
plt.legend()
plt.grid()
plt.show()

# -----------------------
# 📌 Plot: Magnetisierung vs. β
# -----------------------
plt.figure(figsize=(8, 5))
for L in L_values:
    plt.plot(beta_values, magnetizations[L], 'o-', label=f"L = {L}")

plt.plot(beta_values, M_analytic, 'k--', label="Analytische Lösung (L → ∞)")
plt.xlabel("Inverse Temperatur β")
plt.ylabel("⟨|m|⟩")
plt.title("Magnetisierung vs. Temperatur für verschiedene L")
plt.legend()
plt.grid()
plt.show()
