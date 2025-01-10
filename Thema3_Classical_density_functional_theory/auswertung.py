import numpy as np
from numpy import log as ln
import functions as funcs


# -------------------------------------------------------------------- Formeln aus Vorlesung
def mu_id(rho_0: float, l: int):
    return ln(rho_0)

def mu_ex(rho_0: float, l: int):
    return -1 * l*ln(1 - l*rho_0) + (l-1)*ln(1-(l-1)*rho_0)

def mu(rho_0: float, l: int):
    return mu_id(rho_0, l) + mu_ex(rho_0, l)

def mu_s(rho: np.ndarray, l: int):
    N = rho.shape[0]
    wall1, wall2 = (l, N-l)

    mu_id = 0

    mu_ex = np.zeros_like(rho)
    for s in range(N):
        for s_prime in range(s, s+l):
            mu_ex[s] += funcs.phi_prime(funcs.n_1(s_prime, l, rho))

        for s_prime in range(s+1, s+l):
            mu_ex[s] -= funcs.phi_prime(funcs.n_0(s_prime, l, rho))

    return mu_id + mu_ex


def free_energy(rho: np.ndarray, l: int):
    N = rho.shape[0]
    wall1, wall2 = (l, N-l)

    rho_trunc = rho[wall1:wall2]
    F_id = np.sum(rho_trunc * (ln(rho_trunc) - 1))

    F_ex = 0
    for s in range(rho.shape[0]):
        F_ex += funcs.phi(funcs.n_1(s, l, rho)) - funcs.phi(funcs.n_0(s,l,rho))

    
    return F_id + F_ex

def grand_pot(rho: np.ndarray, l: int):
    N = rho.shape[0]
    wall1, wall2 = (l, N-l)
    rho_0 = rho[int(N/2)]
    # mu_par = mu_s(rho, l)
    mu_par = mu(rho_0, l)

    F = free_energy(rho, l)


    sum_part = np.sum(-mu_par * rho)

    return F + sum_part



def pressure(rho_0: float, l: int): 
    return ln(1 - (l-1)*rho_0) - ln(1 - l*rho_0)

def surf_tension_num(rho: np.ndarray, l: int):
    N = rho.shape[0]
    wall1, wall2 = (l, N-l)
    rho_0 = rho[int(N/2)]

    N_free = wall2 - wall1 
    grand_pot_hom = -pressure(rho_0, l) * N_free

    # rho_homo = np.zeros_like(rho)
    # rho_homo[wall1:wall2] = rho_0

    return 0.5*(grand_pot(rho, l) - grand_pot_hom)


def surf_tension_an(rho: np.ndarray, l: int):
    rho_0 = rho[int(rho.shape[0]/2)]
    return 0.5 * ((l-1)*ln(1-l*rho_0) - l*ln(1-(l-1)*rho_0))
    

def excess_adsorption(rho: np.ndarray, l: int, eta: float):
    N = rho.shape[0]
    wall1, wall2 = (l, N-l)
    rho_0 = rho[int(N/2)]

    rho_trunc = rho[wall1 : wall2]
    return 0.5 * np.sum(rho_trunc - rho_0)