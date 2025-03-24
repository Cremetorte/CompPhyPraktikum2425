import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

beta, mean_energy, mean_magnetization, mean_magnetization_sq, specific_heat = np.loadtxt("results.csv", delimiter=",", skiprows=1, unpack=True)

 # Plot der Ergebnisse
# Innere Energiedichte
plt.figure(figsize=(10, 6))
plt.plot(beta, mean_energy)
plt.xlabel("$\\beta$")
plt.ylabel("$\\epsilon$")
plt.title("Innere Energiedichte")
plt.grid()
plt.savefig("3A_energiedichte.png")

# Magnetisierung
plt.figure(figsize=(10, 6))
plt.plot(beta, mean_magnetization)
plt.xlabel("$\\beta$")
plt.ylabel("$|m|$")
plt.title("Magnetisierung")
plt.grid()
plt.savefig("3A_magnetisierung.png")


# Spezifische Wärme
plt.figure(figsize=(10, 6))
plt.plot(beta, specific_heat)
plt.xlabel("$\\beta$")
plt.ylabel("$c/k_B$")
plt.title("Spezifische Wärme")
plt.grid()
plt.savefig("A3_spec_heat")