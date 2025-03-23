from networkx import draw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from numba import njit





# Funktion zur Initialisierung des Spin-Gitters
@njit
def initialize_lattice(L):
    return np.random.choice(np.array([-1,1]), size=(L, L))

@njit
def hamiltonian(spins, J=1, h=0):
    L = spins.shape[0]
    
    H_spin_coupling = 0
    H_ext_mag = 0
    for i in range(L):
        for j in range(L):
            # neighbors_sum = (spins[(i-1)%L, j] 
            #                  + spins[(i+1)%L, j]
            #                  + spins[i, (j-1)%L]
            #                  + spins[i, (j+1)%L])
            neighbors_sum = (spins[(i+1)%L, j]
                             + spins[i, (j+1)%L])
            H_spin_coupling -= J*neighbors_sum*spins[i,j]
            H_ext_mag += h*spins[i,j]
            
    return H_spin_coupling + H_ext_mag
     
     
@njit       
def dH(s, s_prime, i, j, spins, J=1, h=0):
    L = spins.shape[0]
    # neighbors
    neighbors_sum = (spins[(i-1)%L, j] 
                    + spins[(i+1)%L, j]
                    + spins[i, (j-1)%L]
                    + spins[i, (j+1)%L])
    
    # Hamiltonians
    H_s = -J*neighbors_sum*s + h*s
    H_s_prime = -J*neighbors_sum*s_prime + h*s_prime
    
    return H_s_prime - H_s


@njit
def multihit(spins, beta, N_try, J=1, h=0):
    L = spins.shape[0]
    
    for i in range(L):
        for j in range(L):
            for t in range(N_try):
                s1 = int(np.random.choice(np.array([-1,1])))
                s = spins[i,j]
                change_H = dH(s, s1, i, j, spins, J, h)
                if change_H < 0:
                    spins[i,j] = s1
                else:
                    r = np.random.rand()
                    if r < np.exp(-beta*change_H):
                        spins[i,j] = s1

    return spins


@njit
def compute_observables(spins, J=1, h=0):
    L = spins.shape[0]

    M = np.sum(spins)  # Magnetisierung berechnen
    E = hamiltonian(spins, J, h)
    
    return E / (L * L), np.abs(M) / (L * L), M**2/L**2




@njit
def draw_multihit(beta, L, N_try, N_thermalizing=1000, N_a=1000, J=1, h=0):
    spins = initialize_lattice(L)
    
    # Thermalising
    for _ in range(N_thermalizing):
        spins = multihit(spins, beta, N_try, J, h)
        
    while True:
        # destroy auto correlartions
        for _ in range(N_a):
            spins = multihit(spins, beta, N_try, J, h)
            yield spins


@njit
def get_obs_arrays(nr_obs, beta, L, N_try, N_thermalizing=1000, N_a=1000, J=1, h=0):
    energy, magnetization, mag_sq = [], [], []
    for _ in range(nr_obs):
        obs = compute_observables(next(draw_multihit(beta, L, N_try, N_thermalizing, N_a, J, h)))
        energy.append(obs[0])
        magnetization.append(obs[1])
        mag_sq.append(obs[2])
    return energy, magnetization

def aufgabe_a(nr_obs, N_try, N_thermalizing=1000, N_a=1000, J=1, h=0):
    L = 16
    beta = np.linspace(0.1, 1, 10)
    # beta = [0.4406868]
    
    energies = []
    magnetizations = []
    spec_heat = []
    
    for b in beta:
        print(f"Calculating beta = {b}")
        
        obs = get_obs_arrays(nr_obs, b, L, N_try, N_thermalizing, N_a, J, h)
        energies.append(np.mean(obs[0]))
        magnetizations.append(np.mean(obs[1]))
        spec_heat.append(np.var(obs[0])*b**2)
        
        print(f"energy = {energies}\n, magentization = {magnetizations}")
        
    
        
    # Plot der Ergebnisse
    # Innere Energiedichte
    plt.figure(figsize=(10, 6))
    plt.plot(beta, energies)
    plt.xlabel("$\\beta$")
    plt.ylabel("$\\epsilon$")
    plt.title("Innere Energiedichte")
    plt.grid()
    plt.savefig("3A_energiedichte.png")

    # Magnetisierung
    plt.figure(figsize=(10, 6))
    plt.plot(beta, magnetizations)
    plt.xlabel("$\\beta$")
    plt.ylabel("$|m|$")
    plt.title("Magnetisierung")
    plt.grid()
    plt.savefig("3A_magnetisierung.png")
    

    # Spezifische Wärme
    plt.figure(figsize=(10, 6))
    plt.plot(beta, spec_heat)
    plt.xlabel("$\\beta$")
    plt.ylabel("$c/k_B$")
    plt.title("Spezifische Wärme")
    plt.grid()
    plt.savefig("A3_spec_heat")

    # plt.tight_layout()
    # plt.savefig('energy_magnetization_vs_beta.png')
    # plt.close()
        
    
if __name__ == "__main__":
    aufgabe_a(100, 5, 1000, 100)