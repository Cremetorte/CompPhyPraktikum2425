import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from numba import njit
import aufgabe3_test as A3
from joblib import Parallel, delayed

def aufgabe_b(nr_obs, N_try=5, N_thermalizing=1000, N_a=200000, J=1, h=0):
    beta_critical = 0.4406868
    L_sizes = [4, 8, 32]

    print("\nMetropolis-Simulation bei kritischer Temperatur β = 0.4406868:")

    def process_L(L):
        E, M, m_sq = A3.get_obs_arrays(nr_obs, beta_critical, L, N_try, N_thermalizing, N_a, J, h)
        return f"L = {L} -> ⟨E⟩ = {np.mean(E):.4f}, ⟨|m|⟩ = {np.mean(M):.4f}, ⟨m²⟩ = {np.mean(m_sq):.4f}"

    results = Parallel(n_jobs=-1)(delayed(process_L)(L) for L in L_sizes)
    for result in results:
        print(result)


if __name__ == "__main__":
    aufgabe_b(nr_obs=500, N_try=5, N_thermalizing=1000, N_a=200000, J=1, h=0)

"""
Ergebnisse:
Metropolis-Simulation bei kritischer Temperatur β = 0.4406868:
L = 4 -> ⟨E⟩ = -1.5800, ⟨|m|⟩ = 0.8538, ⟨m²⟩ = 0.7706
L = 8 -> ⟨E⟩ = -1.4854, ⟨|m|⟩ = 0.7768, ⟨m²⟩ = 0.6452
L = 32 -> ⟨E⟩ = -1.4393, ⟨|m|⟩ = 0.6658, ⟨m²⟩ = 0.4713
"""