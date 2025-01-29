import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("agg")


def plot_array(x: np.ndarray, filename: str) -> None:
    plt.clf()
    N = x.shape[0]
    idx = np.arange(0,N,1)

    plt.plot(idx, x)
    plt.savefig(filename)
    # plt.show()
    
    
thermalized = slice(150,None,None)

print("Loading arrays")
N_array = np.loadtxt("TotalRods.csv", delimiter=',')[thermalized]
S_array = np.loadtxt("diffRods.csv", delimiter=',')[thermalized]
ver_arr = np.loadtxt("verRods.csv", delimiter=",")[thermalized]
hor_arr = np.loadtxt("horRods.csv", delimiter=",")[thermalized]
print("Loaded arrays")

# plot_array(N_array[:20_000:100], "N.png")
# plot_array(S_array[::1000], "S.png")


# ---------------------------------------------------------- histograms

fig, axs = plt.subplots(2,2)

axs[0,0].hist(N_array, bins=200)
axs[0,0].set_title("N")
axs[0,1].hist(S_array, bins=200)
axs[0,1].set_title("S")
axs[1,0].hist(ver_arr, bins=200)
axs[1,0].set_title("Vertical")
axs[1,1].hist(hor_arr, bins=200)
axs[1,1].set_title("Horizontal")

plt.savefig("histograms.png")