import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import glob
from tabulate import tabulate


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

def error(array):
    nr_measurements = array.shape[0]/10000  
    # sigma = np.sqrt((np.mean(np.square(array)) - np.mean(array)**2)/nr_measurements)
    # return sigma/np.sqrt(nr_measurements)
    return np.std(array)/nr_measurements


# z_list = [0.05, 0.125, 0.25, 0.56, 0.84, 1.1, 1.15, 1.5]
files = glob.glob("Fertig/*.csv")

z_list = []
for i in files:
    z_list.append(float(i[13:18]))


file_dict = dict(zip(z_list, files))
file_dict = dict(sorted(file_dict.items()))
z_list = sorted(z_list)


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
    
    table.append([z, np.mean(n_hor), error(n_hor), np.mean(n_ver), error(n_ver), np.mean(n_tot), error(n_tot), np.mean(eta), error(eta), np.mean(np.abs(S)), error(np.abs(S))])
    
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

print("Results:\n")
print(tabulate(table, 
               headers= ["z", "N_hor", "dN_hor", "N_ver", "dN_ver", "N_tot", "dN_tot", "Eta", "dEta", "|S|", "d|S|"], 
               floatfmt=(".4f",".4f",  ".4f",    ".4f",   ".4f",    ".4f",   ".4f",    ".8f", ".8f",  ".8f", ".8f")))



# -------------------------------------------------------------------------------------------- Plot Ns

fig, axs = plt.subplots(2)

axs[0].set_title("N_tot")
axs[0].set_xlabel("Time")
axs[0].set_ylabel("N_tot")  
for z in z_list:
    axs[0].plot(obs_dict[z][:,2], label=f"{z = }")
axs[0].legend()


axs[1].set_title("N_diff")
axs[1].set_xlabel("Time")
axs[1].set_ylabel("N_hor - N_ver")
for z in z_list:
    axs[1].plot(obs_dict[z][:,0] - obs_dict[z][:,1], label=f"{z = }")
axs[1].legend()

plt.tight_layout()
plt.savefig("N_tot_N_diff.png")


# ------------------------------------------------------------------------------- S(eta)
plt.clf()

table = np.array(table)

eta_mean = table[:,7]
eta_err = table[:,8]

s_mean = table[:,9]
s_err = table[:,10]

plt.errorbar(eta_mean, s_mean, xerr=eta_err, yerr=s_err, linestyle="", color="red", marker="o", ecolor="black", capsize=4)
plt.ylabel(fr"$|S|(\eta)$")
plt.xlabel(fr"$\eta$")
plt.title("Ordnung $|S|$ in Abhängingkeit der Dichte $\eta$")
plt.grid()
plt.savefig("S_eta_plot.png")
