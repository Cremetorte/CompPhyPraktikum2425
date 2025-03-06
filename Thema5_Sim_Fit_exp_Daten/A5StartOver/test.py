from functions import rand_dist, rand_dist_alt
import numpy as np
import matplotlib.pyplot as plt



moeller = lambda x: (3 + np.cos(x))**2/np.sin(x)**4

thetas = []

for i in range(100000):
    thetas.append(rand_dist_alt(moeller, 0, np.pi/2, alpha=0.5, M=1))

plt.hist(thetas, bins=100)
plt.show()    