import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


def index_1d_array(array, step = 1):
    return np.arange(0, len(array), step)


# sort files
data = {0.56: "obs_z=00.56.csv",
         0.84: "obs_z=00.84.csv",
         1.1: "obs_z=01.10.csv"}

# load data
for z in data.keys():
    data[z] = np.loadtxt(data[z], delimiter=",", skiprows=1)


# extract Ns
n_tot = {}
n_hor = {}
n_ver = {}
for z in data.keys():
    n_hor[z] = data[z][:,0]
    n_ver[z] = data[z][:,1]
    n_tot[z] = data[z][:,2]
    
# print(n_tot)
    
fig, axs = plt.subplots(3, figsize=(10, 15))

for i, z in enumerate(data.keys()):
    # print(n_tot[z].shape)
    axs[i].plot(index_1d_array(n_tot[z]), n_tot[z], label=fr"$N_{{tot}}, z={z}$", color="green")
    axs[i].plot(index_1d_array(n_hor[z]), n_hor[z], label=fr"$N_{{hor}}, z={z}$", color="red")
    axs[i].plot(index_1d_array(n_ver[z]), n_ver[z], label=fr"$N_{{ver}}, z={z}$", color="blue")
    axs[i].legend(loc=1)
    axs[i].set_xlabel("TIteration/100")
    axs[i].set_ylabel("N")
    axs[i].set_title(fr"$z={z}$")
    axs[i].grid()



plt.tight_layout()
plt.savefig("Ns.png")

