import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#get console arguments (without sys.argv[0] which is the file name)
cmd_args = sys.argv[1::]

#check for correct nr of arguments
if len(cmd_args) != 3:
    raise ValueError(f"Not the correct number of arguments!\nUsage: {sys.argv[0]} integrator nr_particles delta_t")
else:
    #extract arguments
    integrator, N, delta_t = cmd_args
    N, delta_t = int(N), float(delta_t)
    filename = f"{N}-body/{N}Body_{integrator}.csv"
    print(f"Starting post-processing of file {filename}. Parameters: N = {N}, delta_t = {delta_t}.")



#import data
data = np.loadtxt(filename, delimiter=",")

# Extract particles
particles = []
particle_rs = []
particle_vs = []
for i in range(N):
    particle = data[i::N, :]
    particle_r = particle[:, :3]
    particle_v = particle[:, 3:6]
    particles.append(particle)
    particle_rs.append(particle_r)
    particle_vs.append(particle_v)


# set up time array
nr_steps = int(len(data)/N)
t_list = np.arange(0,nr_steps*delta_t, delta_t)[0:-1:1]

# if len(t_list) !=  nr_steps:
#     print(f"len t_list = {len(t_list)} != {nr_steps}" )
#     print(t_list)




# total angular momentum
ang_mom = np.zeros_like(t_list)
for t in range(nr_steps):
    ang_mom_i = 0
    for i in range(N):
        ang_mom_i += np.linalg.norm(np.cross(particle_rs[i], particle_vs[i]))
    ang_mom[t] = ang_mom_i


# Runge Lenz vec
RLV = []
for i in range(nr_steps):
    RLV.append()

