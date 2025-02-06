import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation

#Matplotlib stuff
matplotlib.use('Agg')
plt.style.use('seaborn-v0_8-darkgrid')

# ------------------------ Console arguments & Setup ------------------------
#get console arguments (without sys.argv[0] which is the file name)
cmd_args = sys.argv[1::]

#check for correct nr of arguments
if len(cmd_args) != 2:
    raise ValueError(f"Not the correct number of arguments!\nUsage: {sys.argv[0]} N delta_t")
else:
    #extract arguments
    N = int(cmd_args[0])
    delta_t = float(cmd_args[1])
    
    print(f"Starting post-processing of file all files using parameters: N = {N}, delta_t = {delta_t}.")


# handle integrator cases
integrators = ["euler", "euler-cromer", "velocity_verlet", "RK4", "hermite", "hermite_it"]  # <--- not yet implemented
symp_int = ["euler-cromer", "hermite", "velocity_verlet"]
non_symp_int = ["euler", "RK4", "hermite_it"]

#------------------------ Import & process data ------------------------
def input_filename(N, integrator, delta_t):
    return f"{N}-body/{N}Body_{integrator}_{delta_t}.csv"
def output_filename(N, delta_t, suffix = ""):
    return f"{N}-body/plot_energy_{N}_{delta_t}_{suffix}.png"

#import data
def import_data(N, integrator, delta_t):
    data = np.loadtxt(input_filename(N, integrator, delta_t), delimiter=",")
    nr_steps = int(len(data)/N)
    
    t_list = np.arange(0, nr_steps*delta_t, delta_t)

    # fix double entires at end of t_steps
    if (len(data) != N*len(t_list)):
        t_list = t_list[:-1]

    return (data, t_list)


# ----------------------------- Def helping funtions --------------------------------

def get_r(particle):
    return particle[:, 0:3]

def get_v(particle):
    return particle[:, 3:6]

def logarithmizer(quantity, times):
    res = np.abs((quantity - quantity[0]) / quantity[0])[1:-1:]
    res = np.log10(res)
    return (res, times[1:-1:])


# ----------------------------- Def functions for quantities -----------------------------

def energy(data,t_list):
    # Extract particles at times t
    # particle1 = data[0::2, :]
    # particle2 = data[1::2, :]
    zero_like_t = np.zeros_like(t_list)

    particles = []
    r_i = []
    v_i = []
    m_i = []
    energy_i = []
    for i in range(N):
        particles.append(data[i::N, :])
        r_i.append(get_r(particles[i]))
        v_i.append(get_v(particles[i]))
        m_i.append(particles[i][0, 6])
        energy_i.append(zero_like_t)


    # # Extract r and v vectors
    # r_1 = get_r(particle1)
    # r_2 = get_r(particle2)
    # v_1 = get_v(particle1)
    # v_2 = get_v(particle2)

    # #set up energies and masses
    # energy_1 = np.zeros_like(t_list)
    # energy_2 = np.zeros_like(t_list)
    # m_1 = data[0][6]
    # m_2 = data[1][6]

    energy_tot = zero_like_t

    for t in range(len(t_list)):
        pot_term = np.zeros(N)
        kin_term = np.zeros(N)

        for i in range(N):
            for j in range(N):
                if i==j:
                    continue
                pot_term[i] -= m_i[i]*m_i[j] / np.linalg.norm(r_i[i][t] - r_i[j][t])
            
            kin_term[i] += 0.5 * m_i[i] * np.linalg.norm(v_i[i][t])**2
            energy_i[i][t] = pot_term[i] + kin_term[i]

            energy_tot[t] += energy_i[i][t]

        # kin_term_1 += 0.5 * m_1 * np.linalg.norm(v_1[t])**2
        # kin_term_2 += 0.5 * m_2 * np.linalg.norm(v_2[t])**2

        # energy_1[t] = pot_term + kin_term_1
        # energy_2[t] = pot_term + kin_term_2



    return logarithmizer(energy_tot, t_list)




# ---------------------------------- Plotting ------------------------------------

def gen_plots(integrator_list, delta_t, suffix = ""):
    data_dict = {}
    linestyle_list = ["-", "--", "-.", ":", ".", "-", "--", "-.", ":", "."]

    for i in integrator_list:
        data_dict[i] = import_data(N, i, delta_t)
    cm = 1/2.54
    fig, ax = plt.subplots()
    fig.suptitle(f"Energieerhaltung der Integratoren bei N = {N} und $\\Delta t = {delta_t}$")#
    fig.set_size_inches(15*cm, 8*cm)
    
    ax.set_xlabel("Zeit $t$")
    ax.set_ylabel(r"$log\left(\frac{|E_{tot}-E_{tot}(0)|}{E_{tot}(0)}\right)$")

    for idx, i in enumerate(integrator_list):
        E,t = energy(data_dict[i][0], data_dict[i][1])
        ax.plot(t, E, linestyle_list[idx], label = f"Integrator: {i}")
    
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_filename(N, delta_t, suffix), dpi = 300)



# ---------------------------- "Main" -------------------------------
gen_plots(integrators, delta_t, suffix="all_ints")
# gen_plots(non_symp_int, delta_t, suffix="non-symplectic")
