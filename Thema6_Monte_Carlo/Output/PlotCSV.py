import numpy as np
import matplotlib.pyplot as plt


def plot_array(x: np.ndarray, filename: str) -> None:
    plt.clf()
    N = x.shape[0]
    idx = np.arange(0,N,1)

    plt.plot(idx, x)
    # plt.savefig(filename)
    plt.show()


N_array = np