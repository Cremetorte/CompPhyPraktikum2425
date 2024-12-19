import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt 
np.seterr(all='raise')
# --------------------------------------------------------------------------------------- ConditionalNjit
USE_NUMBA = False
NOPYTHON = True

if USE_NUMBA:
    from numba import jit
    

# Conditional decorator
def conditional_njit(func):
    if USE_NUMBA:
        return jit(nopython=NOPYTHON)(func)
    else:
        return func

# ------------------------------------------------------------------------------------- Helper functions 
@conditional_njit
def walls(nr_lat_points: int, l: int) -> tuple[int]:
    wall_1: int = l
    wall_2: int = nr_lat_points - 2*l + 1
    return (wall_1, wall_2)

def physical_walls(nr_lat_points: int, l: int) -> tuple[int]:
    wall_1: int = l
    wall_2: int = nr_lat_points - 2*l + 1
    return (wall_1, wall_2)


# -------------------------------------------------------------------------------- Thermodynamic functions
@conditional_njit
def n_1(s: int, l: int, rho: np.ndarray) -> float:

    rho_trunc = rho[s-(l-1):s+1:] # only consider rho_s between s-l+1 and s (included)
    return np.sum(rho_trunc)

@conditional_njit
def n_0(s: int, l: int, rho: np.ndarray) -> float:
    rho_trunc = rho[s-(l-1):s:] # only consider rho_s between s-l+1 and s-1 (included)
    return np.sum(rho_trunc)

@conditional_njit
def n_1_arr(l: int, rho: np.ndarray) -> np.ndarray:
    res = np.zeros_like(rho)
    wall1, wall2 = walls(rho.shape[0],l)
    for i in range(wall1, wall2):
        
        res[i] = n_1(i, l, rho)
    return res

@conditional_njit
def n_0_arr(l: int, rho: np.ndarray) -> np.ndarray:
    res = np.zeros_like(rho)
    wall1, wall2 = walls(rho.shape[0],l)
    for i in range(wall1, wall2):

        res[i] = n_0(i, l, rho)
    return res

@conditional_njit
def phi_0D(x: np.ndarray) -> np.ndarray:
    return x + (1-x)*np.log(1-x)

@conditional_njit
def phi_0D_prime(x: np.ndarray) -> np.ndarray:
    try:
        return -1 * np.log(1-x)
    except:
        print(x)

@conditional_njit
def mu_homogenous(l: int, rho_0: float) -> float:
    part_0 = np.log(rho_0)
    part_1 = -l * np.log(1 - l*rho_0)
    part_2 = (l - 1) * np.log(1 - (l-1)*rho_0)
    return part_0 + part_1 + part_2


@conditional_njit
def mu_homogenous_ex(l: int, rho_0: float) -> float:
    part_1: float = -l * np.log(1 - l*rho_0)
    part_2: float = (l - 1) * np.log(1 - (l-1)*rho_0)
    return part_1 + part_2


@conditional_njit
def exp_pot(N: int, l: int) -> np.ndarray:
    res: np.ndarray = np.zeros((N,))
    wall_1, wall_2 = walls(N, l)
    res[wall_1:wall_2] = 1
    return res


@conditional_njit
def mu_ex(l: int, rho: np.ndarray, beta: float = 1) -> np.ndarray:
    N = rho.shape[0]
    # wall_1, wall_2 = walls(N, l)

    res = np.zeros_like(rho)
    sum_1 = sum_2  = 0
    for s in range(N):
        sum_1: float = np.sum(phi_0D_prime(n_1_arr(l, rho)[s:s+l]))
        sum_2: float = np.sum(phi_0D_prime(n_0_arr(l, rho)[s+1:s+l]))
        res[s] = sum_1 - sum_2
        
        
        # sum_1: float = 0
        # for s_prime in range(s, min(s+l, N)):
        #     sum_1 += phi_0D_prime(n_1(s_prime, l, rho))

        # sum_2: float = 0
        # for s_prime in range(s+1, s+l):
        #     sum_2 += phi_0D_prime(n_0(s_prime, l, rho))

        # res[s] = sum_1 - sum_2

    return 1/beta * res
    



def initial_rho(l: int, eta: float, N: int) -> np.ndarray:
    rho: np.ndarray = np.zeros((N,))
    rho_0: float = eta/l

    wall_1, wall_2 = walls(N, l)
    rho[wall_1:wall_2] = rho_0

    return rho


# -------------------------------------------------------------------------------------------------------- Iterative Solving


# @conditional_njit
# def rho_solver(rho_initial: np.ndarray, eta: float, l: int, beta: float = 1, epsilon: float = 1e-20) -> np.ndarray:
#     N = rho_initial.shape[0]
#     alpha: float = 0.9  # Relaxation parameter
#     rho_0: float = eta / l  # Homogeneous density
#     mu_0: float = mu_homogenous_ex(l, rho_0)  # Homogeneous chemical potential

#     rho_i: np.ndarray = rho_initial.copy()
#     rho_new: np.ndarray = np.zeros_like(rho_i)

#     print("Beginning calculation using l = " + str(l) + ", eta = " + str(eta) +  " and rho_0 = " + str(rho_0) )
#     step = 0

#     while True:
        
#         # Update rule for rho_new
#         mu_excess = mu_ex(l, rho_i)

#         rho_new = rho_0 * np.exp(beta * (mu_0 - mu_excess)) * exp_pot(N, l)

#         # Convergence check
#         diff = np.sum(np.square(rho_new - rho_i))
        
#         # Optional progress report
#         if not USE_NUMBA:
#             print(f"\rStep {step}: Residual = {diff:.3e}", end="")

#         if diff < epsilon:
#             break

#         # Relaxation step
#         rho_i = (1 - alpha) * rho_i + alpha * rho_new

        
#         step += 1
#         if step >= 100000:
#             raise RuntimeError("Convergence not achieved within iteration limit.")

#     print("\nFinished calculation")
#     return rho_i



@conditional_njit
def rho_solver(rho_initial: np.ndarray, eta: float, l: int, beta: float = 1, epsilon: float = 10**-16) -> np.ndarray:
    N = rho_initial.shape[0]
    alpha: float = 0.9
    rho_0: float = eta/l
    mu_0: float = float(mu_homogenous(l, rho_0))
    print(f"{mu_0=}")

    rho_i: np.ndarray = rho_initial
    print(f"{rho_i=}")

    rho_it: np.ndarray = np.zeros_like(rho_i)
    rho_new: np.ndarray = np.zeros_like(rho_i)

    print("Beginning calculation using l =",l," and eta =", eta)
    step = 0

    while True:

        rho_new = np.exp(beta*(mu_0 - mu_ex(l, rho_i)))*exp_pot(N, l)


        res = np.sum(np.square(rho_new - rho_i))
        if res < epsilon:
            break

        rho_it = (1-alpha)*rho_i + alpha*rho_new

        rho_i = rho_it

        if not USE_NUMBA:
            print("\rCalculating step " + str(step) + ". Residual =", res, end="")

        step += 1
        if step >= 100000:
            raise RuntimeError("Computed too long")

    print("Finished calculation\n")
    return rho_it



# ---------------------------------------------------------------------------------------------------------- Plotting


def plot_array(array: np.ndarray, l: int, eta: float, filename: str) -> None:
    sl = slice(l, 5*l)

    x: np.ndarray = np.arange(0, array.shape[0]+1, 1)

    plt.plot(x[sl], array[sl], label = f"Densities for L = {l}, eta_0 = {eta}")
    plt.title(f"Densities for L = {l}, eta_0 = {eta}")
    plt.xlabel("Lattice point s")
    plt.ylabel("Calculated eq. density")

    plt.savefig(filename, dpi = 250)