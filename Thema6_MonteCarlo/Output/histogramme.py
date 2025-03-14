from networkx import density
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


STEP = 100

# sort files
data = {0.56: "obs_z=00.56.csv",
         0.84: "obs_z=00.84.csv",
         1.1: "obs_z=01.10.csv"}


# load data
print("Loading data ...")
for z in data.keys():
    data[z] = np.loadtxt(data[z], delimiter=",", skiprows=1)
print("Data loaded")




# extract observables
n_tot = {}
n_hor = {}
n_ver = {}
eta = {}
s = {}

for z in data.keys():
    n_hor[z] = data[z][::STEP,0]
    n_ver[z] = data[z][::STEP,1]
    n_tot[z] = data[z][::STEP,2]
    eta[z] = data[z][::STEP,3]
    s[z] = data[z][::STEP,4]
    
    
# plot histograms

bin = 50



for z in data.keys():
    plt.cla()
    fig, axs = plt.subplots(2,3)
    
    axs[0,0].hist(n_hor[z], bins=bin, density=True)
    axs[0,0].set_title("# Horizontal Rods")
    
    axs[0,1].hist(n_ver[z], bins=bin, density=True)
    axs[0,1].set_title("# Vertical Rods")
    
    axs[0,2].hist(n_tot[z], bins=bin, density=True)
    axs[0,2].set_title("# Total Rods")
    
    axs[1,0].hist(eta[z], bins=bin, density=True)
    axs[1,0].set_title(r"$\eta$")
    
    axs[1,1].hist(s[z], bins=bin, density=True)
    axs[1,1].set_title("S")
    
    axs[1,2].axis("off")

    fig.suptitle(f"z = {z}")
    plt.tight_layout()
    
    plt.savefig(f"histogram_z={z}.png")
    # plt.close()
    