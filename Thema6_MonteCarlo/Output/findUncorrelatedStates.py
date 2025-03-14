from networkx import density
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use("TkAgg")




# sort files
data = {0.56: "Kontrolle/Fertig/obs_z=00.56.csv",
         0.84: "Kontrolle/Fertig/obs_z=00.84.csv",
         1.1: "Kontrolle/Fertig/obs_z=001.1.csv"}


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
    n_hor[z] = data[z][:,0]
    n_ver[z] = data[z][:,1]
    n_tot[z] = data[z][:,2]
    eta[z] = data[z][:,3]
    s[z] = data[z][:,4]
    
for z in data.keys():
    print(n_hor[z].shape)


c_j_hor_array = {}
g_j_hor_array = {}



for z in data.keys():
    print("Starting with z = ", z)
    g_j_hor_array[z] = []
    c_j_hor_array[z] = []
    n_hor_mean = np.mean(n_hor[z])

    for j in range(1, 1000,1):
        n_hor_shifted = n_hor[z][j::]
        n_hor_not_shifted = n_hor[z][0:-j]
        
        c_j_hor_array[z].append(1/len(n_hor_shifted) * np.sum(n_hor_shifted * n_hor_not_shifted))
        

        
        g_j_hor_array[z].append((c_j_hor_array[z][-1] - n_hor_mean ** 2)/n_hor_mean ** 2)


def indices(array):
    return np.arange(0, len(array))
    


for z in data.keys():
    plt.plot(100*indices(g_j_hor_array[z]), g_j_hor_array[z], label = "z = " + str(z))

plt.legend()
plt.xlabel("j")
plt.ylabel(r"$g_j$")
plt.title(r"$g_j$ for different z")
plt.grid()
plt.show()


