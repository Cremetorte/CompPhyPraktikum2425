import numpy as np
import itertools
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Berechnung der Energie einer bestimmten Konfiguration
def energie(spins, L, J=1, h=0):
    H = 0
    for i in range(L):
        for j in range(L):
            s = spins[i, j]
            H -= J * s * (spins[(i+1) % L, j] + spins[i, (j+1) % L])
            H -= h * s
    return H

# Berechnung der Zustandssumme und Observablen
def ising_direct_sum(L, beta):
    states = list(itertools.product([-1, 1], repeat=L*L))
    
    Z = 0
    avg_E = 0
    avg_M = 0
    avg_absM = 0
    
    for state in states:
        spins = np.array(state).reshape(L, L)  # Spins in L×L-Form bringen
        H = energie(spins, L)
        M = np.sum(spins)
        
        weight = np.exp(-beta * H)
        Z += weight
        avg_E += H * weight
        avg_M += M * weight
        avg_absM += abs(M) * weight
    
    # Normierung
    avg_E /= Z
    avg_M /= Z
    avg_absM /= Z
    
    return avg_E / (L * L), avg_M / (L * L), avg_absM / (L * L)

# Analytische Lösung
def analytical_energy(beta):
    J = 1
    xi = 2 * np.tanh(2 * beta * J) / np.cosh(2 * beta * J)
    def integrand(theta, xi):
        return 1 / np.sqrt(1 - xi**2 * np.sin(theta)**2)
    K, _ = quad(integrand, 0, np.pi/2, args=(xi))
    coth = np.cosh(2 * beta * J) / np.sinh(2 * beta * J)
    epsilon = - J * coth * (1 + (2 * np.tanh(2*beta*J)**2 -1) * 2/np.pi * K)
    return epsilon

def analytical_magnetization(beta):
    beta_c = 0.440687
    if beta < beta_c:
        return 0
    else:
        return (1 - np.sinh(2 * beta) ** (-4)) ** (1/8)

# Simulation für verschiedene L
beta_values = np.linspace(0.01, 1, 100)
L_values = [2, 3, 4]

energies = {L: [] for L in L_values}
magnetizations = {L: [] for L in L_values}

# Berechnung der numerischen Werte für L = 2, 3, 4
for beta in beta_values:
    for L in L_values:
        E, M, absM = ising_direct_sum(L, beta)
        energies[L].append(E)
        magnetizations[L].append(absM)

# Berechnung der analytischen Werte
E_analytic = [analytical_energy(beta) for beta in beta_values]
M_analytic = [analytical_magnetization(beta) for beta in beta_values]

# Plot für Energiedichte
plt.figure(figsize=(8, 5))
for L in L_values:
    plt.plot(beta_values, energies[L], '-', label=f"L = {L}")

plt.plot(beta_values, E_analytic, 'k--', label="Analytische Lösung")
plt.xlabel("$\\beta$")
plt.ylabel("$\\epsilon$")
plt.title("Energiedichte als Funktion der inversen Temperatur")
plt.legend()
plt.grid()
plt.show()

# Plot für Magnetisierung
plt.figure(figsize=(8, 5))
for L in L_values:
    plt.plot(beta_values, magnetizations[L], '-', label=f"L = {L}")

plt.plot(beta_values, M_analytic, 'k--', label="Analytische Lösung")
plt.xlabel("$\\beta$")
plt.ylabel("$⟨|m|⟩$")
plt.title("Spontane Magnetisierung als Funktion der inversen Temperatur")
plt.legend()
plt.grid()
plt.show()