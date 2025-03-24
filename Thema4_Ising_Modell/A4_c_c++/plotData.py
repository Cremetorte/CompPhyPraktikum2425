import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

beta_values, h_values, mean_energy, mean_magnetization, specific_heat = np.loadtxt("results.csv", delimiter=",", skiprows=1, unpack=True)


# 3D-Plot der Magnetisierung als Funktion von β und h
X, Y = np.meshgrid(h_values, beta_values)
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, mean_magnetization, cmap='viridis')

ax.set_xlabel('Magnetfeld $h$')
ax.set_ylabel('Inverse Temperatur $\\beta$')
ax.set_zlabel('Magnetisierung $\\langle m \\rangle$')
ax.set_title('Magnetisierung als Funktion von $\\beta$ und $h$')

plt.show()

# 3D-Plot des Betrags der Magnetisierung als Funktion von β und h
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, mean_magnetization, cmap='viridis')

ax.set_xlabel('Magnetfeld $h$')
ax.set_ylabel('Inverse Temperatur $\\beta$')
ax.set_zlabel('Betrag der Magnetisierung $\\langle |m| \\rangle$')
ax.set_title('Betrag der Magnetisierung als Funktion von $\\beta$ und $h$')

plt.show()