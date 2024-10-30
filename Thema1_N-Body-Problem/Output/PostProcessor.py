import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



#Number of particles
N = 2

data = np.loadtxt("Output/2Body_Velocity_Verlet.csv", delimiter = ",")

particle1 = data[::2,::]
#print(particle1.shape)
particle1_r = particle1[:,:3]

particle2 = data[1::2,::]
#print(particle2.shape)
particle2_r = particle2[:,:3]


eta = 0.001
fps = 60 #gives about 30s with 1 step/frame



fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")
scat1 = ax.scatter([], [], [], color = "blue", label = "Körper 1")
scat2 = ax.scatter([], [], [], color = "red", label = "Körper 2")


x_max = np.max(data[:,0])
y_max = np.max(data[:,1])
z_max = np.max(data[:,2])

max_border = np.max([x_max,y_max,z_max])


ax.set_xlim(-max_border, max_border)
ax.set_ylim(-max_border, max_border)
ax.set_zlim(-max_border, max_border)
ax.legend()


def init():
    scat1._offsets3d = ([], [], [])
    scat2._offsets3d = ([], [], [])
    return scat1, scat2

def update(frame):
    x1, y1, z1 = particle1_r[frame*2]
    x2, y2, z2 = particle2_r[frame*2]
    scat1._offsets3d = ([x1], [y1], [z1])
    scat2._offsets3d = ([x2], [y2], [z2])
    return scat1, scat2

num_frames = min(len(particle1_r), len(particle2_r))
ani = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval = 1000/fps)


print("Starting to write mp4 file. This could take some time.")
ani.save("Output/Zweikoerper_animation.mp4", writer="ffmpeg")
print("\007")