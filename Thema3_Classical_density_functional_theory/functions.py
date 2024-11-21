import numpy as np

def n_1(s, l, rho):
    rho_trunc = rho[s-(l-1):s+1:] # only consider rho_s between s-l+1 and s (included)
    return np.sum(rho_trunc)

def n_2(s, l, rho):
    rho_trunc = rho[s-(l-1):s:] # only consider rho_s between s-l+1 and s-1 (included)
    return np.sum(rho_trunc)

def phi_0D(x):
    return x + (1-x)*np.log(1-x)

def phi_0D_prime(x):
    return -1 * np.log(1-x)

def mu_ex_homo(l, rho_0):
    part_1 = l * np.log(1 - l*rho_0)
    part_2 = (l - 1) * np.log(1 - (l-1)*rho_0)
    return part_1 + part_2





def initial_rho(length, lattice_nodes):
    rho = np.zeros(lattice_nodes)
    