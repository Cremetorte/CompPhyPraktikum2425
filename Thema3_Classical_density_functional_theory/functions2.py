import numpy as np
from numpy import log as ln
from numba import njit
np.seterr(all='raise')
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import time


# -------------------------------------------------------------- Numba Setup
USE_NUMBA = False
def cond_njit(func):
    if USE_NUMBA:
        return njit(func)
    else:
        return func

# --------------------------------------------------------- Helper Functions
def walls(array: np.ndarray, border: int) -> list[int]:
    N = array.shape[0]
    wall1 = border	
    wall2 = N - 2*border 
    return [wall1, wall2]

def initial_rho(lat_N: int, rod_l: int, eta_0: float) -> np.ndarray:
    idx = np.zeros(lat_N)
    wall1, wall2 = walls(idx, rod_l)
    rho_0: float = eta_0/rod_l

    idx[wall1:wall2] = rho_0

    return idx

# ------------------------------------------------- "mathematical" equations

def phi_prime(x):
    return -ln(1-x)

# -------------------------------------------------  Thermodynamic Equations

def n_1(rho: np.ndarray, rod_l: int) -> np.ndarray:
    N = rho.shape[0]

    wall1, wall2 = walls(rho, rod_l)

    res: np.ndarray = np.zeros_like(rho)

    for s in range(wall1-1, N):
        rho_cropped: np.ndarray = rho[s-rod_l+1:s+1]
        res[s] = np.sum(rho_cropped)
    
    # print(f"n_1 = {res}")
    return res

def n_0(rho: np.ndarray, rod_l: int) -> np.ndarray:
    N = rho.shape[0]

    wall1, wall2 = walls(rho, rod_l)

    res: np.ndarray = np.zeros_like(rho)

    for s in range(wall1-1, N):
        rho_cropped:np.ndarray = rho[s-rod_l+1:s]
        res[s] = np.sum(rho_cropped)

    # print(f"n_0 = {res}")
    return res


def mu_ex(rho: np.ndarray, rod_l: int, beta: float = 1):
    N = rho.shape[0]

    res = np.zeros_like(rho)

    phi_n_1: np.ndarray = phi_prime(n_1(rho, rod_l))
    phi_n_0: np.ndarray = phi_prime(n_0(rho, rod_l))

    for s in range(N - rod_l):
        sum1 = np.sum(phi_n_1[s:s+rod_l])
        sum2 = np.sum(phi_n_0[s+1:s+rod_l])
        res[s] = sum1 - sum2

    return 1/beta * res

def mu_homo(eta_0: float, rod_l: int, beta: float = 1):
    rho_0 = eta_0/rod_l
    part1 = ln(rho_0)
    part2 = -rod_l * ln(1 - rod_l*rho_0)
    part3 = (rod_l - 1) * ln(1 - (rod_l-1)*rho_0)
    return 1/beta * (part1 + part2 + part3)

def mu_homo_ex(eta_0: float, rod_l: int, beta: float = 1):
    rho_0 = eta_0/rod_l
    # part1 = ln(rho_0)
    part2 = -rod_l * ln(1 - rod_l*rho_0)
    part3 = (rod_l - 1) * ln(1 - (rod_l-1)*rho_0)
    return 1/beta * ( part2 + part3)

def pot(x: np.ndarray, rod_l) -> np.ndarray:
    res = np.zeros_like(x)
    wall1, wall2 = walls(res, rod_l)
    res[wall1:wall2] = 1
    return res
        


def solve_rho(lat_points: int, rod_length: int, eta_0: float, beta: float = 1, epsilon: float = 10**(-15), alpha: float = 0.01):
    N = lat_points
    L = rod_length
    eta = eta_0
    alpha = 0.01
    

    mu = mu_homo_ex(eta, L, beta)
    rho_0 = eta/L
    rho_i: np.ndarray = initial_rho(N, L, eta)
    mu_ex_i = mu_ex(rho_i, L, beta)

    exp_pot = pot(rho_i, L)

    print(f"Beginning iterative solving of rho using {N = }, {L = }, {eta = }.")
    nr_steps = 1
    while True:
        # print(f"\n{rho_i = }")
        # print(f"mu_ex = {mu_ex(rho_i, L, beta) }")
        # time.sleep(1)

        

        rho_new = rho_0 * np.exp(beta* (mu - mu_ex_i))*exp_pot
        
        while True:
            try:
                rho_i_1 = (1-alpha)*rho_i + alpha*rho_new

                mu_ex_i = mu_ex(rho_i, L, beta)
                break
            except:
                alpha = alpha/2
                print(f"{alpha = }")
                time.sleep(1)
                

        residual = np.sum(np.square(rho_new - rho_i))
        if residual < epsilon:
            break

        rho_i = rho_i_1
        nr_steps += 1
        if nr_steps > 1000:
            print("Iterative process did not converge.")
            break

        if not USE_NUMBA:
            print(f"\rCalculating step {nr_steps}. Residual: {residual:.2f}    ", end="")

        

    print(f"\nFinished Calculation after {nr_steps} steps.")
    return rho_i



