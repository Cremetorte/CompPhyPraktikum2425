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
if len(cmd_args) != 1:
    raise ValueError(f"Not the correct number of arguments!\nUsage: {sys.argv[0]} delta_t")
else:
    #extract arguments
    delta_t = cmd_args[0]
    delta_t = float(delta_t)
    N = 2
    
    print(f"Starting post-processing of file all files using parameters: N = 2, delta_t = {delta_t}.")


# handle integrator cases
integrators = ["euler", "euler-cromer", "velocity_verlet", "heun", "RK4", "hermite", "hermite_it"]  
symp_int = ["euler-cromer", "velocity_verlet", "hermite"]
non_symp_int = ["euler", "heun", "RK4",  "hermite_it"]


#------------------------ Import & process data ------------------------
def input_filename(integrator, delta_t):
    return f"2Body_{integrator}_{delta_t}.csv"

#import data
def import_data(integrator, delta_t):
    data = np.loadtxt(input_filename(integrator, delta_t), delimiter=",")
    nr_steps = int(len(data)/N)                  
    
    t_list = np.arange(0, nr_steps*delta_t, delta_t)
    if (len(data) != 2*len(t_list)):
    # if t_list[-1] == t_list[-2]:
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

# 1. Energie
def energy(data,t_list):
    # Extract particles at times t
    particle1 = data[0::2, :]
    particle2 = data[1::2, :]

    # Extract r and v vectors
    r_1 = get_r(particle1)
    r_2 = get_r(particle2)
    v_1 = get_v(particle1)
    v_2 = get_v(particle2)

    #set up energies and masses
    energy_1 = np.zeros_like(t_list)
    energy_2 = np.zeros_like(t_list)
    m_1 = data[0][6]
    m_2 = data[1][6]

    for t in range(len(t_list)):
        pot_term = 0
        kin_term_1 = 0
        kin_term_2 = 0

        pot_term -= (m_1 * m_2) / (np.linalg.norm(r_1[t] - r_2[t]))

        kin_term_1 += 0.5 * m_1 * np.linalg.norm(v_1[t])**2
        kin_term_2 += 0.5 * m_2 * np.linalg.norm(v_2[t])**2

        energy_1[t] = pot_term + kin_term_1
        energy_2[t] = pot_term + kin_term_2

    energy_tot = energy_1 + energy_2

    return logarithmizer(energy_tot, t_list)


# 2. Specific angular momentum
def spec_ang_mom(data, t_list):
    # Extract particles at times t
    particle1 = data[0::2, :]
    particle2 = data[1::2, :]

    # Extract r and v vectors
    r = get_r(particle1) - get_r(particle2)
    v = get_v(particle1) - get_v(particle2)

    j = np.zeros_like(t_list)
    for t in range(len(t_list)):
        j[t] = np.linalg.norm(np.cross(r[t], v[t]))
    
    return logarithmizer(j, t_list)
    
    

# 3. Runge Lenz vector/eccentricity
def ecc(data, t_list):
    # Extract particles at times t
    particle1 = data[0::2, :]
    particle2 = data[1::2, :]

    # Extract r and v vectors
    r = get_r(particle1) - get_r(particle2)
    v = get_v(particle1) - get_v(particle2)

    e = np.zeros_like(t_list)
    for t in range(len(t_list)):
        e[t] = np.linalg.norm(np.cross(v, np.cross(r[t], v[t])) - r/(np.linalg.norm(r[t])**2))
    
    return logarithmizer(e, t_list)

def ecc_0(data):
    r_1 = data[0,0:3]
    r_2 = data[1,0:3]
    r = r_1 - r_2

    v_1 = data[0,3:6]
    v_2 = data[1,3:6]
    v = v_1 - v_2



    e = np.linalg.norm(np.cross(v, np.cross(r, v)) - r/(np.linalg.norm(r)**2))

    return e


# 4. Great major axis
def a(data, t_list):
    # Extract particles at times t
    particle1 = data[0::2, :]
    particle2 = data[1::2, :]

    # Extract r and v vectors
    r = get_r(particle1) - get_r(particle2)
    v = get_v(particle1) - get_v(particle2)

    j = np.zeros_like(t_list)
    for t in range(len(t_list)):
        j[t] = np.linalg.norm(np.cross(r[t], v[t]))

    e = np.zeros_like(t_list)
    for t in range(len(t_list)):
        e[t] = np.linalg.norm(np.cross(v, np.cross(r[t], v[t])) - r/(np.linalg.norm(r)**2))
    
    e_squared  = np.square(e)
    j_squared = np.square(j)

    a = j_squared/(1-e_squared)

    return logarithmizer(a, t_list)





# ---------------------------------- Plotting ------------------------------------

def gen_plots(integrator_list, delta_t, suffix = ""):

    linestyle_list = ["-", "--", "-.", ":", "-", "--", "-.", ":"]

    data_dict = {}
    for i in integrator_list:
        data_dict[i] = import_data(i, delta_t)

    cm = 1/2.54  # cm <-> inch

    ecc_0_c = ecc_0(data_dict[integrator_list[0]][0])

    fig, axs = plt.subplots(4)
    fig.suptitle(f"Erhaltungsgrößen der Integratoren bei $\\Delta t = {delta_t}$ und $|\\vec e| = {ecc_0_c:.4E}$")
    fig.tight_layout()
    fig.set_size_inches(25*cm, 40*cm)  # Increase the height to make the plots taller


    #Energie
    axs[0].set_title("Energie")
    axs[0].set_xlabel("Zeit $t$")
    axs[0].set_ylabel(r"$log\left(\frac{|E_{tot}-E_{tot}(0)|}{E_{tot}(0)}\right)$")

    for idx, i in enumerate(integrator_list):
        x,t = energy(data_dict[i][0], data_dict[i][1])
        axs[0].plot(t,x, linestyle_list[idx], label = f"Integrator: {i}")
    
    axs[0].legend()


    # j
    axs[1].set_title("Spezifischer Drehimpuls")
    axs[1].set_xlabel("Zeit $t$")
    axs[1].set_ylabel(r"$log\left(\frac{||j|_{tot}-|j|(0)|}{|j|_{tot}(0)}\right)$")

    for idx, i in enumerate(integrator_list):
        x,t = spec_ang_mom(data_dict[i][0], data_dict[i][1])
        axs[1].plot(t,x, linestyle_list[idx], label = f"Integrator: {i}")

    axs[1].legend()


    # eccentricity
    axs[2].set_title("Runge-Lenz-Vektor")
    axs[2].set_xlabel("Zeit $t$")
    axs[2].set_ylabel(r"$log\left(\frac{||e|_{tot}-|e|_{tot}(0)|}{|e|_{tot}(0)}\right)$")
    
    for idx, i in enumerate(integrator_list):
        x,t = ecc(data_dict[i][0], data_dict[i][1])
        axs[2].plot(t,x, linestyle_list[idx], label = f"Integrator: {i}")
    
    axs[2].legend()

    # Great major axis
    axs[3].set_title("Große Halbachse")
    axs[3].set_xlabel("Zeit $t$")
    axs[3].set_ylabel(r"$log\left(\frac{|a_{tot}-a_{tot}(0)|}{a_{tot}(0)}\right)$")

    for idx, i in enumerate(integrator_list):
        x,t = a(data_dict[i][0], data_dict[i][1])
        axs[3].plot(t,x, linestyle_list[idx], label = f"Integrator: {i}")
    
    axs[3].legend()

    plt.tight_layout()
    plt.savefig(f"plots_{delta_t}{suffix}{ecc_0_c=}.png", dpi = 300)




# -------------------- "Main" ----------------------------
# gen_plots(symp_int, delta_t, "_symplectic")
# gen_plots(non_symp_int, delta_t, "_non_symplectic")
gen_plots(integrators, delta_t, "all_ints")
