import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from numba import njit
from joblib import Parallel, delayed
import Thema4_Ising_Modell.AlterCode.Aufgabe4a_copy as A4a

def aufgabe_b(nr_obs, N_try=5, N_thermalizing=1000, N_a=200000, J=1, h=0):
    beta_critical = 0.4406868
    L_sizes = [4, 8, 32]

    print("\nMetropolis-Simulation bei kritischer Temperatur β = 0.4406868:")

    def process_L(L):
        E, M, m_sq = A4a.get_obs_arrays(nr_obs, beta_critical, L, N_try, N_thermalizing, N_a, J, h)
        return f"L = {L} -> ⟨E⟩ = {np.mean(E):.4f}, ⟨|m|⟩ = {np.mean(M):.4f}, ⟨m²⟩ = {np.mean(m_sq):.4f}"

    results = Parallel(n_jobs=-1)(delayed(process_L)(L) for L in L_sizes)
    for result in results:
        print(result)


if __name__ == "__main__":
    aufgabe_b(nr_obs=500, N_try=5, N_thermalizing=1000, N_a=200000, J=1, h=0)

"""
Metropolis-Simulation bei kritischer Temperatur β = 0.4406868:
L = 4 -> ⟨E⟩ = -1.5645, ⟨|m|⟩ = 0.8347, ⟨m²⟩ = 0.7546
L = 8 -> ⟨E⟩ = -1.4904, ⟨|m|⟩ = 0.7812, ⟨m²⟩ = 0.6511
L = 32 -> ⟨E⟩ = -1.4341, ⟨|m|⟩ = 0.6548, ⟨m²⟩ = 0.4604
"""