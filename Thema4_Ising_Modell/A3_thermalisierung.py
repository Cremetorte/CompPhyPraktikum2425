import numpy as np
import matplotlib.pyplot as plt

# Parameter
betas = [0.1, 0.5, 1]
N_sweeps = 4000
L = 128

# Funktion zur Initialisierung des Spin-Gitters
def initialize_lattice(L):
    return np.random.choice([-1, 1], size=(L, L))

# Berechnung der Energie einer Konfiguration
def compute_energy(spins, J=1, h=0):
    L = spins.shape[0]
    E = 0
    for i in range(L):
        for j in range(L):
            s = spins[i, j]
            E -= J * s * (spins[(i+1) % L, j] + spins[i, (j+1) % L])
            E -= h * s
    return E / (L * L)

# Metropolis-Update für gesamtes Gitter
def metropolis_sweep(spins, beta, J=1, h=0):
    L = spins.shape[0]
    for i in range(L):
        for j in range(L):
            s = spins[i, j]
            neighbor_sum = (
                spins[(i+1) % L, j] + spins[(i-1) % L, j] +
                spins[i, (j+1) % L] + spins[i, (j-1) % L]
            )
            dE = 2 * J * s * neighbor_sum + 2 * h * s
            if dE < 0 or np.random.rand() < np.exp(-beta * dE):
                spins[i, j] *= -1
    return spins

# Thermalisierungsanalyse
def analyze_thermalization(L, betas, N_sweeps_max=N_sweeps):
    sweeps = np.arange(N_sweeps_max)
    energies = {beta: [] for beta in betas}

    for beta in betas:
        spins = initialize_lattice(L)
        energy_vals = []
        
        for n in sweeps:
            spins = metropolis_sweep(spins, beta)
            energy_vals.append(compute_energy(spins))
            
        energies[beta] = energy_vals

    # Plot der Energiedichte als Funktion der Sweeps
    plt.figure(figsize=(8, 5))
    for beta in betas:
        plt.plot(sweeps, energies[beta], label=f"$\\beta$ = {beta}")

    plt.xlabel("Anzahl der Sweeps")
    plt.ylabel("Energiedichte $\\epsilon$")
    plt.title(f"Thermalisierungsanalyse für L = {L}")
    plt.legend()
    plt.grid()
    plt.show()

analyze_thermalization(L, betas)
