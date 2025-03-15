import numpy as np
import itertools

# Berechnung der Energie einer bestimmten Konfiguration
def energie(spins, L, J=1, h=0):
    H = 0
    for i in range(L):
        for j in range(L):
            s = spins[i, j]
            # Nachbar-Spins mit periodischen Randbedingungen
            H -= J * s * (spins[(i+1) % L, j] + spins[i, (j+1) % L])
            H -= h * s  # Externes Magnetfeld
    return H

# Funktion zur Berechnung der Zustandssumme und Observablen
def ising_direct_sum(L, beta):
    # Alle möglichen Spin-Konfigurationen durchgehen
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
    
    # Normierung durch Zustandssumme Z
    avg_E /= Z
    avg_M /= Z
    avg_absM /= Z
    
    return avg_E / (L * L), avg_M / (L * L), avg_absM / (L * L)

# Temperaturbereich
beta_values = np.linspace(0, 1, 10)

# Gittergrößen L = 2, 3, 4
for L in [2, 3, 4]:
    print(f"\nIsing-Modell für L = {L}:")
    for beta in beta_values:
        energy, magnetization, abs_magnetization = ising_direct_sum(L, beta)
        print(f"β = {beta:.2f} -> ⟨E⟩ = {energy:.4f}, ⟨m⟩ = {magnetization:.4f}, ⟨|m|⟩ = {abs_magnetization:.4f}")