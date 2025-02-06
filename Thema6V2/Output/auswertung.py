import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import glob
from tabulate import tabulate

z_list = [0.05, 0.125, 0.25, 0.56, 0.84, 1.1, 1.15, 1.5]
files = glob.glob("Fertig/*.csv")

file_dict = dict(zip(z_list, files))


def plot_array(x: np.ndarray, filename: str) -> None:
    plt.clf()
    N = x.shape[0]
    idx = np.arange(0,N,1)

    plt.plot(idx, x)
    # plt.savefig(filename)
    plt.show()
    
def split_columns(array):
    # Splits the columns of the array into separate arrays
    if len(array.shape) != 2:
        raise ValueError("Array must be 2D")
    
    
    res = []
    for i in range(array.shape[1]):
        res.append(array[:,i])
    return res


thermalized = slice(150,None,None)


print("Loading Observations")
obs_dict = {}
# obs = np.loadtxt("observations.csv", delimiter=",", skiprows=1)
for z in z_list:
    obs = np.loadtxt(file_dict[z], delimiter=",", skiprows=1)
    obs_dict[z] = obs


print(f"Loaded Observations. Dimension of Array: {obs.shape}")


table = []

# Format: n_hor,n_ver,n_tot,eta,S
for z in z_list:
    obs = obs_dict[z]
    n_hor, n_ver, n_tot, eta, S = split_columns(obs)
    
    table.append([z, np.mean(n_hor), np.mean(n_ver), np.mean(n_tot), np.mean(eta), np.mean(S)])
    
    # print(tabulate([[np.mean(n_hor), np.mean(n_ver), np.mean(n_tot), np.mean(eta), np.mean(S)]], headers=["N_hor", "N_ver", "N_tot", "Eta", "S"], floatfmt=".8f"))
    # print("\n\n")

# n_hor, n_ver, n_tot, eta, S = split_columns(obs)

# fig, axs = plt.subplots(2,3)

# axs[0,0].hist(n_hor, bins=100)
# axs[0,0].set_title("Horizontal")
# axs[0,1].hist(n_ver, bins=100)
# axs[0,1].set_title("Vertical")
# axs[0,2].hist(n_tot, bins=100)
# axs[0,2].set_title("Total")
# axs[1,0].hist(eta, bins=100)
# axs[1,0].set_title("Eta")
# axs[1,1].hist(S, bins=100)
# axs[1,1].set_title("S")


# plt.tight_layout()
# plt.show()

# ----------------------------------------------- Means
# mean_n_hor = float(np.mean(n_hor))
# mean_n_ver = float(np.mean(n_ver))
# mean_n_tot = float(np.mean(n_tot))
# mean_eta = float(np.mean(eta))
# mean_S = float(np.mean(S))

# table = [[mean_n_hor, mean_n_ver, mean_n_tot, mean_eta, mean_S]]
print(tabulate(table, headers= ["z", "N_hor", "N_ver", "N_tot", "Eta", "S"], floatfmt=".8f"))

