import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#get console arguments (without sys.argv[0] which is the file name)
cmd_args = sys.argv[1::]

#check for correct nr of arguments
if len(cmd_args) != 4:
    raise ValueError(f"Not the correct number of arguments!\nUsage: {sys.argv[0]} input_filename nr_particles delta_t output_filename")
else:
    #extract arguments
    filename, N, eta, output_filename = cmd_args
    N, eta = int(N), float(eta)
    print(f"Starting post-processing of file {filename}. Parameters: N = {N}, delta_t = {eta}.")



#import data
data = np.loadtxt(filename, delimiter=",")

# Extract particles
particles = []
particle_rs = []
for i in range(N):
    particle = data[i::N, :]
    particle_r = particle[:, :3]
    particles.append(particle)
    particle_rs.append(particle_r)

#setup animation
fps = 30
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

scatterers = []
for i in range(N):
    scat = ax.scatter([], [], [], color = np.random.rand(3,), label = f"Körper {i+1}")
    scatterers.append(scat)



x_max = np.max(data[:,0])
y_max = np.max(data[:,1])
z_max = np.max(data[:,2])

max_border = np.max([x_max,y_max,z_max])


ax.set_xlim(-max_border, max_border)
ax.set_ylim(-max_border, max_border)
ax.set_zlim(-max_border, max_border)
if N<5:
    ax.legend()


def init():
    for i in range(N):
        scatterers[i]._offsets3d = ([],[],[])
    return scatterers

def update(frame):
    for i in range(N):
        x, y, z = particle_rs[i][frame*2]
        scatterers[i]._offsets3d = ([x], [y], [z])
    return scatterers

num_frames = int(data.shape[0]/N)
ani = FuncAnimation(fig, update, frames=int(num_frames/2), init_func=init, blit=True, interval = 1000/fps)

print("Starting to write mp4 file. This could take some time.")
ani.save(output_filename, writer="ffmpeg")
print("Finished Saving video.")
print("\007")