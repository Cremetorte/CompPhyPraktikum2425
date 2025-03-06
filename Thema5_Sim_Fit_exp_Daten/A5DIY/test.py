import matplotlib.pyplot as plt
from functions import rand_dist
import numpy as np


values = []

for i in range(1000):
    values.append(rand_dist(np.exp, -10,0,1))

plt.hist(values, bins=50, edgecolor='black')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Randomly Distributed Values')
plt.show()
