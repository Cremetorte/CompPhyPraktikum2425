import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation

# ------------------------ Console arguments ------------------------
#get console arguments (without sys.argv[0] which is the file name)
cmd_args = sys.argv[1::]

#check for correct nr of arguments
if len(cmd_args) != 2:
    raise ValueError(f"Not the correct number of arguments!\nUsage: {sys.argv[0]} integrator delta_t")
else:
    #extract arguments
    integrator, delta_t = cmd_args
    delta_t = float(delta_t)
    N = 2
    filename = f"2Body_{integrator}_{delta_t}.csv"
    print(f"Starting post-processing of file {filename}. Parameters: N = 2, delta_t = {delta_t}.")


epsilon = 1e-10 # to avoid division by zero and log(0) errors


#------------------------ Import & process data ------------------------
#import data
data = np.loadtxt(filename, delimiter=",")


# set up time array
nr_steps = int(len(data)/N)
t_list = np.arange(0, nr_steps*delta_t, delta_t)
if t_list[-1] == t_list[-2]:
    t_list = t_list[:-1]


# Extract particles at times t
particle1 = data[0::2, :]
particle2 = data[1::2, :]

# Extract r and v vectors
particle1_r = particle1[:, 0:3]
particle2_r = particle2[:, 0:3]
particle1_v = particle1[:, 3:6]
particle2_v = particle2[:, 3:6]


# ------------------------ Calculate quantities ------------------------
# calculate specific angular momentum
ang_mom_1 = np.zeros_like(t_list)
ang_mom_2 = np.zeros_like(t_list)

for t in range(nr_steps):
    ang_mom_1[t] = np.linalg.norm(np.cross(particle1_r[t], particle1_v[t]))
    ang_mom_2[t] = np.linalg.norm(np.cross(particle2_r[t], particle2_v[t]))

ang_mom_tot = ang_mom_1 + ang_mom_2

# Ensure no division by zero and log(0) errors
ang_mom_0 = ang_mom_tot[0]
ang_mom_tot_log = np.abs((ang_mom_tot - ang_mom_0) / (ang_mom_0))[1:-1:]
ang_mom_tot_log = np.where(ang_mom_tot_log == 0, epsilon, ang_mom_tot_log)
ang_mom_tot_log = np.log10(ang_mom_tot_log)


# calculate Runge Lenz vector/eccentricity
rl_1 = np.zeros_like(t_list)
rl_2 = np.zeros_like(t_list)

for t in range(nr_steps):
    rl_1[t] = np.linalg.norm(np.cross(particle1_v[t], np.cross(particle1_r[t], particle1_v[t])) - particle1_r[t] / (np.linalg.norm(particle1_r[t] - particle2_r[t]) + epsilon))
    rl_2[t] = np.linalg.norm(np.cross(particle2_v[t], np.cross(particle2_r[t], particle2_v[t])) - particle2_r[t] / (np.linalg.norm(particle1_r[t] - particle2_r[t]) + epsilon))

rl_tot = rl_1 + rl_2

# Ensure no division by zero and log(0) errors
rl_0 = rl_tot[0]
rl_tot_log = np.abs((rl_tot - rl_0) / (rl_0))[1:-1:]
rl_tot_log = np.log10(rl_tot_log)


# great semiaxis
a_1 = np.square(ang_mom_1) / (1 - np.square(rl_1) + epsilon)
a_2 = np.square(ang_mom_2) / (1 - np.square(rl_2) + epsilon)
a_tot = np.square(ang_mom_tot) / (1 - np.square(rl_tot) + epsilon)

# Ensure no division by zero and log(0) errors
a_tot_0 = a_tot[0]
a_tot_log = np.abs((a_tot - a_tot_0) / (a_tot_0))[1:-1:]
a_tot_log = np.log10(a_tot_log)


# Energy
energy_1 = np.zeros_like(t_list)
energy_2 = np.zeros_like(t_list)
m_1 = data[0][6]
m_2 = data[1][6]

for t in range(nr_steps):
    pot_term = 0
    kin_term_1 = 0
    kin_term_2 = 0

    pot_term -= (m_1 * m_2) / (np.linalg.norm(particle1_r[t] - particle2_r[t]) + epsilon)

    kin_term_1 += 0.5 * m_1 * np.linalg.norm(particle1_v[t])**2
    kin_term_2 += 0.5 * m_2 * np.linalg.norm(particle2_v[t])**2

    energy_1[t] = pot_term + kin_term_1
    energy_2[t] = pot_term + kin_term_2

energy_tot = energy_1 + energy_2

# Ensure no division by zero and log(0) errors
energy_tot_0 = energy_tot[0]
energy_tot_log = np.abs((energy_tot - energy_tot_0) / (energy_tot_0))[1:-1:]
energy_tot_log = np.log10(energy_tot_log)





# ----------------- Plotting stuff ----------------------
matplotlib.use('Agg')

plt.style.use('seaborn-v0_8-darkgrid')

t_list = t_list[1:-1:] # remove first element to avoid log(0) errors

cm = 1/2.54  # cm <-> inch

fig, axs = plt.subplots(4)
fig.suptitle(f"Erhaltungsgrößen des {integrator}-Integrators mit $\\Delta t = {delta_t}$")
fig.tight_layout()
fig.set_size_inches(20*cm, 30*cm)  # Increase the height to make the plots taller


# Energy
axs[0].set_title("Energie")
axs[0].set_xlabel("Zeit $t$")
axs[0].set_ylabel(r"$log\left(\frac{|E_{tot}-E_{tot}(0)|}{E_{tot}(0)}\right)$")
axs[0].plot(t_list, energy_tot_log, label="Energie", color="red")
# axs[0].legend()

# Specific Angular Momentum
axs[1].set_title("Spezifischer Drehimpuls")
axs[1].set_xlabel("Zeit $t$")
axs[1].set_ylabel(r"$log\left(\frac{||j|_{tot}-|j|(0)|}{|j|_{tot}(0)}\right)$")
axs[1].plot(t_list, ang_mom_tot_log, label=r"$log\left(\frac{||j|_{tot}-|j|(0)|}{|j|_{tot}(0)}\right)$", color="red")
# axs[1].legend()

# Runge Lenz Vektor
axs[2].set_title("Runge-Lenz-Vektor")
axs[2].set_xlabel("Zeit $t$")
axs[2].set_ylabel(r"$log\left(\frac{||e|_{tot}-|e|_{tot}(0)|}{|e|_{tot}(0)}\right)$")
axs[2].plot(t_list, rl_tot_log, label=r"$log\left(\frac{||e|_{tot}-|e|_{tot}(0)|}{|e|_{tot}(0)}\right)$", color="red")
# axs[2].legend()

# Great major axis
axs[3].set_title("Große Halbachse")
axs[3].set_xlabel("Zeit $t$")
axs[3].set_ylabel(r"$log\left(\frac{|a_{tot}-a_{tot}(0)|}{a_{tot}(0)}\right)$")
axs[3].plot(t_list, a_tot_log, label=r"$log\left(\frac{|a_{tot}-a_{tot}(0)|}{a_{tot}(0)}\right)$", color="red")
# axs[3].legend()

plt.tight_layout()


plt.savefig(f"plots_{integrator}_{delta_t}.png", dpi=300)