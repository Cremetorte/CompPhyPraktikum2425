import matplotlib.pyplot as plt
import numpy as np

a = 1.0
T_end = 3.5
xmin = -1
xmax = 1

x = np.arange(-1, 1, 0.001)
def y(x):
    if abs(x)<= 1./3:
        return 1.0
    if 1./3 < abs(x) <= 1:
        return 0.0
    else:
        print("Error: x out of range")
        return None
    
y = [y(xi) for xi in x]
#plt.plot(x, y)
#plt.show()

def psi_analytisch(x, t, a):
    x_shifted = (x - a * t) % (xmax - xmin) + xmin
    return np.where(np.abs(x_shifted) <= 1./3, 1.0, 0.0)

x_fine = np.arange(xmin, xmax, 0.001)
psi_analytisch_fine = psi_analytisch(x_fine, T_end, a)
plt.plot(x_fine, psi_analytisch_fine)
plt.show()
