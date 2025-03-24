from networkx import draw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from numba import njit
from joblib import Parallel, delayed





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
            neighbors_sum = (spins[(i-1)%L, j] 
                             + spins[(i+1)%L, j]
                             + spins[i, (j-1)%L]
                             + spins[i, (j+1)%L])
            # neighbors_sum = (spins[(i+1)%L, j]
            #                  + spins[i, (j+1)%L])
            H_spin_coupling -= J*neighbors_sum*spins[i,j]/2
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
def heat_bath_sweep(spins, beta, J=1, h=0):
    L = spins.shape[0]
    for i in range(L):
        for j in range(L):
            # Berechnung der Energieänderung ΔE bei Flip eines Spins
            delta = (
                spins[(i+1) % L, j] + spins[(i-1) % L, j] +
                spins[i, (j+1) % L] + spins[i, (j-1) % L]
            )
            k = beta * (J * delta + h)
            # Berechnung der Wahrscheinlichkeit, den Spin zu flippen
            q = np.exp(-k) / (2 * np.cosh(k))
            r = np.random.rand()  # Zufallszahl für die Akzeptanz
            if r < q:
                spins[i, j] = -1
            else:
                spins[i, j] = 1
    return spins


@njit
def compute_observables(spins, J=1, h=0):
    L = spins.shape[0]

    M = np.sum(spins)  # Magnetisierung berechnen
    E = hamiltonian(spins, J, h)
    M_sq = M**2/L**2
    
    return E / (L * L), np.abs(M) / (L * L), M_sq/L**2




@njit
def draw_heat_bath(beta, L, N_try, N_thermalizing=1000, N_a=1000, J=1, h=0):
    spins = initialize_lattice(L)
    
    # Thermalising
    for _ in range(N_thermalizing):
        spins = heat_bath_sweep(spins, beta, J=1, h=0)
        
    while True:
        # destroy auto correlartions
        for _ in range(N_a):
            spins = heat_bath_sweep(spins, beta, J=1, h=0)
            yield spins


@njit
def get_obs_arrays(nr_obs, beta, L, N_try, N_thermalizing=1000, N_a=1000, J=1, h=0):
    energy, magnetization, mag_sq = [], [], []
    for _ in range(nr_obs):
        obs = compute_observables(next(draw_heat_bath(beta, L, N_try, N_thermalizing, N_a, J, h)))
        energy.append(obs[0])
        magnetization.append(obs[1])
        mag_sq.append(obs[2])
    return energy, magnetization, mag_sq

def aufgabe_a(nr_obs, N_try=5, N_thermalizing=1000, N_a=10000, J=1, h=0):
    L = 128
    beta = np.linspace(0.1, 1, 40)
    # beta = [0.4406868]
    
    def compute_for_beta(b):
        print(f"Calculating beta = {b}")
        obs = get_obs_arrays(nr_obs, b, L, N_try, N_thermalizing, N_a, J, h)
        energy = np.mean(obs[0])
        magnetization = np.mean(obs[1])
        specific_heat = np.var(obs[0]) * b**2
        print(f"energy = {energy}, magnetization = {magnetization}")
        return energy, magnetization, specific_heat

    results = Parallel(n_jobs=-1)(delayed(compute_for_beta)(b) for b in beta)

    energies, magnetizations, spec_heat = zip(*results)
        
    
        
    # Plot der Ergebnisse
    # Innere Energiedichte
    plt.figure(figsize=(10, 6))
    plt.plot(beta, energies)
    plt.xlabel("$\\beta$")
    plt.ylabel("$\\epsilon$")
    plt.title("Innere Energiedichte")
    plt.grid()
    plt.savefig("4a_energiedichte.png")

    # Magnetisierung
    plt.figure(figsize=(10, 6))
    plt.plot(beta, magnetizations)
    plt.xlabel("$\\beta$")
    plt.ylabel("$|m|$")
    plt.title("Magnetisierung")
    plt.grid()
    plt.savefig("4a_magnetisierung.png")
    

    # Spezifische Wärme
    plt.figure(figsize=(10, 6))
    plt.plot(beta, spec_heat)
    plt.xlabel("$\\beta$")
    plt.ylabel("$c/k_B$")
    plt.title("Spezifische Wärme")
    plt.grid()
    plt.savefig("4a_spec_heat")

    # plt.tight_layout()
    # plt.savefig('energy_magnetization_vs_beta.png')
    # plt.close()



def aufgabe_4b(beta, L, N_try=5, N_thermalizing=1000, N_a=10000, J=1):
    # hysteresekuve
    h_space = np.linspace(-1, 1, 100)
    np.concatenate([h_space, h_space[::-1]])

    # energy = []
    magnetization = []
    # specific_heat = []
    for h in h_space:
        print(f"Calculating h = {h}")
        obs = get_obs_arrays(N_try, beta, L, N_try, N_thermalizing, N_a, J, h)
        # energy.append(np.mean(obs[0]))
        magnetization.append(np.mean(obs[1]))
        # specific_heat.append(np.var(obs[0]) * beta**2)
        # print(f"energy = {energy}, magnetization = {magnetization}")
    
    
    # Plot der Ergebnisse
    plt.figure(figsize=(8, 5))
    plt.plot(h_space, magnetization, linestyle='-', color='b')
    # plt.plot(h_values, magnetization_2, linestyle='-', color='b')

    plt.xlabel("Externes Magnetfeld $h$")
    plt.ylabel("Magnetisierung $⟨m⟩$")
    plt.title(f"Hysterese-Effekt für $L={L}$, $\\beta={beta}$")
    plt.grid()
    plt.savefig("A4b_hysterese.png")

        
    
if __name__ == "__main__":
    aufgabe_a(nr_obs=100)