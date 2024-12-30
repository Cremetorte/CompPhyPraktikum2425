import numpy as np
from numba import njit
np.seterr(all='raise')
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import time


# -------------------------------------------------------------------------------- Numba Setup
USE_NUMBA = True
def cond_njit(func):
    if USE_NUMBA:
        return njit(func)
    else:
        return func
    
def precompile() -> None:
    if not USE_NUMBA:
        print("Numba is not used")
    else:
        print("Precompiling functions ...")

        # calls function solve_rho without doing any calculations to precompile it.
        solve_rho(1,1,1, compile=True)
        
        print("Precompiled functions")

# ------------------------------------------------------------------------------ Phi and Phi'

@cond_njit
def phi_prime(n):
    return -1*np.log(1-n)

@cond_njit
def phi(n): 
    return n + (1-n) * np.log(1-n)
    
# --------------------------------------------------------------------------- n^(1) and n^(0)

@cond_njit
def n_1(s: int, l: int, rho: np.ndarray) -> float:
    rho_trunc: np.ndarray = rho[s-l+1: s+1]
    return np.sum(rho_trunc)

@cond_njit
def n_0(s: int, l: int, rho: np.ndarray) -> float:
    rho_trunc: np.ndarray = rho[s-l+1: s]
    return np.sum(rho_trunc)



# ------------------------------------------------------------------------------------ mu_ex

@cond_njit
def mu_ex(rho: np.ndarray, l: int, beta: float = 1) -> np.ndarray:
    res = np.zeros_like(rho)
    for s in range(rho.shape[0]):
        sum1 = 0
        for s_prime in range(s, s+l):
            sum1 += phi_prime(n_1(s_prime, l, rho))
        
        sum2 = 0
        for s_prime in range(s+1, s+l):
            sum2 += phi_prime(n_0(s_prime,l, rho))
        
        res[s] = sum1 - sum2

    return 1/beta * res

def mu_ex_eq(rho_0, l: int, beta: float = 1):
    return 1/beta *(- l*np.log(1 - l*rho_0) 
            + (l - 1)*np.log(1-(l-1)*rho_0)
            )

@cond_njit
def mu_id_ex(rho_0: float, l: int, beta: float = 1) -> np.ndarray:
    
    return 1/beta * (
        np.log(rho_0)
        - l * np.log(1 - l*rho_0)
        + (l - 1) * np.log(1 - (l - 1)*rho_0)
    )

@cond_njit
def mu_homo_ex(rho_0: float, l: int, beta: float = 1) -> float:
    return 1/beta * (-1 * l * np.log(1 - l*rho_0)
                     + (l - 1) * np.log(1- (l-1)*rho_0))
    

@cond_njit
def initial_rho(N: int, l: int, eta: float):
    res = np.zeros(N)
    rho_0 = eta/l
    res[l:N-l] = rho_0
    return res

@cond_njit
def exp_pot(rho: np.ndarray, l: int):
    res = np.zeros_like(rho)
    N = rho.shape[0]
    res[l:N-l] = 1
    return res


@cond_njit
def solve_rho(N: int, l: int, eta: float, beta: float = 1, compile: bool = False):
    epsilon_per_lat_point: float = 1E-12    # mean epsilon/N
    epsilon = epsilon_per_lat_point * N     # epsilon
    if compile:
        return None

    if eta < 0.8:
        alpha = 0.1
        max_steps = 1000
    else: 
        alpha = 0.01
        max_steps = 1000
        if l > 3:
            alpha = 0.001
            max_steps = 10000

    residual: float = 100


    rho_i = initial_rho(N,l,eta)
    pot = exp_pot(rho_i, l)

    mu = mu_homo_ex(eta/l, l, beta)

    if not USE_NUMBA:
        print("Beginning calculation using N = {}, l = {}, eta = {} ...".format(N, l, eta))
    else:
        print(f"Beginning caclulation ... ")

    step = 0
    while True:

        rho_new = eta/l * np.exp(beta * (mu - mu_ex(rho_i, l, beta))) * pot

        residual = np.sum(np.square(rho_new - rho_i))

        if residual < epsilon:
            break

        if not USE_NUMBA:
            print(f"\rCalculating step {step}. Residual = {residual}   ", end = "")

        rho_i = (1-alpha) * rho_i + alpha * rho_new

        step += 1

        if step > max_steps:
            print("\nProcess did not converge after " + str(step) + " steps")
            break

    if not USE_NUMBA:
        print("Finished calculation after " + str(step) + " steps. Residual = " + str(residual) + ".")
    else: 
        print("Finished calculation after " + str(step) + " steps.")
    print("")

    return rho_i

# ---------------------------------------------------------------------------------------- Surface Tension

def free_energy(rho: np.ndarray, l: int, beta: float = 1):
    rho_prime = rho[l:rho.shape[0]-l]
    F_id = np.sum(rho_prime * (np.log(rho_prime) - 1))
    
    F_ex = 0
    for i in range(rho.shape[0]):
        F_ex += phi(n_1(i, l, rho)) - phi(n_0(i, l, rho))
    return 1/beta * (F_id + F_ex)

def grand_pot(rho: np.ndarray, l: int, beta: float = 1):
    f_e = free_energy(rho,l,beta)

    rho_truc = rho[l:rho.shape[0]-l]

    rho_0 = rho[int(rho.shape[0]/2)]

    # mu = mu_id(rho_truc, l, beta) + mu_ex(rho_truc, l, beta)

    mu = mu_id_ex(rho_0, l, beta) 
    
    sum = -mu*np.sum(rho_truc)

    return f_e + sum

def surface_tension(rho: np.ndarray, l: int, eta: float, beta: float = 1) -> float:
    eq_grand_pot = grand_pot(rho, l, beta)
    rho_0 = eta/l

    rho_0_arr = np.zeros_like(rho)
    rho_0_arr[l:rho.shape[0]-l] += rho_0

    homo_grand_pot = grand_pot(rho_0_arr, l, beta)

    return eq_grand_pot - homo_grand_pot

def p(rho_0: float, l: int, beta: float = 1):
    return 1/beta * np.log(1 + rho_0/(1-l*rho_0))

def surf_tension_ana(rho_0: float, l: int, beta: float = 1) -> float:
    part_1 = mu_ex_eq(rho_0, l, beta)
    part_2 = (2*l - 1) * p(rho_0, l, beta)
    return 0.5 * (part_1 - part_2)
     
    


# ----------------------------------------------------------------------------------------- Plotting stuff


def plot_array(x: np.ndarray, filename: str) -> None:
    plt.clf()
    N = x.shape[0]
    idx = np.arange(0,N,1)

    plt.plot(idx, x)
    plt.savefig(filename)

def is_homogeneous(array: np.ndarray, epsilon) -> bool:
    return (np.max(array) - np.min(array))/np.mean(array) < epsilon

def plot_rho(rho: np.ndarray, l: int, filename: str) -> None:
    cutoff = 6*l

    rho_trunc = rho[l:cutoff]
    plot_array(rho_trunc, filename)