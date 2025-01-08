import numpy as np
import functions as funcs

# mu

def mu(rho_0: float, l: int, beta: float = 1):
    # rho_0 = eta/l

    return 1/beta * (
        np.log(rho_0)
        - l * np.log(1 - rho_0*l)
        + (l - 1) * np.log(1 - (l-1)*rho_0)
    )

# pressure
def p(eta: float, l: int):
    rho_0 = eta/l

    return np.log(1 - (l-1)*rho_0) - np.log(1 - l*rho_0)


# free energy functional
def free_energy(rho: np.ndarray, l: int, beta: float = 1):
    wall1 = l
    wall2 = rho.shape[0] - l

    f_id = 0
    for s in range(wall1, wall2):
        f_id += rho[s] * (np.log(rho[s]) - 1)

    f_ex = 0
    for s in range(rho.shape[0]):
        f_ex += funcs.phi(funcs.n_1(s, l, rho)) - funcs.phi(funcs.n_0(s, l, rho))
    
    return 1/beta * (f_id + f_ex)


# grand potential functional
def grand_pot_functional(rho: np.ndarray, l: int, eta: float, beta: float = 1):
    F = free_energy(rho, l, beta)

    wall1 = l
    wall2 = rho.shape[0] - l

    mu_p = mu(eta/l, l, beta)
    sum = 0
    for s in range(wall1, wall2+1):
        sum -= mu_p*rho[s]

    return F + sum

# surface tension (numerically)
def surf_tension_num(rho: np.ndarray, l: int, eta: float, beta: float = 1):
    wall1 = l
    wall2 = rho.shape[0] - l
    g_p_eq = grand_pot_functional(rho, l, eta, beta)
    return 0.5 * (g_p_eq + p(eta, l)*(wall2 - wall1 + 1))

# analytical stuff


def mu_ex(eta: float, l: int, beta: float = 1):
    rho_0 = eta/l
    return 1/beta * (np.log(rho_0)
                     - l*np.log(1 - l*rho_0)
                     + (l-1) * np.log(1 - (l-1)*rho_0))

def surf_tension_anal(eta: float, l: int, beta: float = 1):
    return 0.5 * (mu(eta/l, l, beta) - (2*l - 1)*p(eta,l))

def surf_tension_2(eta: float, l: int, beta:float = 1):
    rho_0 = eta/l
    return 0.5/beta * (
        (l-1) * np.log(1-l*rho_0)
        - l * np.log(1-(l-1)*rho_0)
    )