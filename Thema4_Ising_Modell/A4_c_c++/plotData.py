# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib
# # matplotlib.use('TkAgg')

# beta_values, h_values, mean_energy, mean_magnetization_abs, mean_magnetization, specific_heat = np.loadtxt("results.csv", delimiter=",", skiprows=1, unpack=True)

# print("beta_values: ", beta_values)
# print("h_values: ", h_values)

# # 3D-Plot der Magnetisierung als Funktion von β und h
# X, Y = np.meshgrid(h_values, beta_values)
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_trisurf(h_values, beta_values, Y, mean_magnetization, cmap='viridis')

# # ax.set_xlabel('Magnetfeld $h$')
# # ax.set_ylabel('Inverse Temperatur $\\beta$')
# # ax.set_zlabel('Magnetisierung $\\langle m \\rangle$')
# # ax.set_title('Magnetisierung als Funktion von $\\beta$ und $h$')

# # plt.show()

# # 3D-Plot des Betrags der Magnetisierung als Funktion von β und h
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(h_values,beta_values, mean_magnetization, cmap='viridis')

# ax.set_xlabel('Magnetfeld $h$')
# ax.set_ylabel('Inverse Temperatur $\\beta$')
# ax.set_zlabel('Betrag der Magnetisierung $\\langle |m| \\rangle$')
# ax.set_title('Betrag der Magnetisierung als Funktion von $\\beta$ und $h$')

# # plt.savefig("3d_plot_betrag_m")
# plt.show()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# CSV-Datei einlesen (Pfad anpassen)
df = pd.read_csv("results.csv", delimiter=',')

# Annahme: Spaltennamen in der CSV-Datei sind exakt 'beta', 'h', 'M(beta,h)'
beta = df['beta']
h = df['h']
M_abs = df['mean_magnetization_abs']
M = df['mean_magnetization']

# 3D-Plot erstellen
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Trisurf-Plot
surf = ax.plot_trisurf(h, beta, M, cmap='viridis', edgecolor='none')

# Farblegende hinzufügen
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# Achsentitel setzen
ax.set_xlabel(r'$h$')
ax.set_ylabel(r'$\beta$')
ax.set_zlabel(r'$M(\beta, h)$')
ax.set_title('Betrag der Magnetisierung als Funktion von $\\beta$ und $h$')

plt.savefig("3d_plot_m")

plt.cla()

# 3D-Plot erstellen
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Trisurf-Plot
surf = ax.plot_trisurf(beta, h, M_abs, cmap='viridis', edgecolor='none')

# Farblegende hinzufügen
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# Achsentitel setzen
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$h$')
ax.set_zlabel(r'$|m|(\beta, h)$')
ax.set_title('Magnetisierung als Funktion von $\\beta$ und $h$')

# plt.show()
plt.savefig("3d_plot_abs_m")