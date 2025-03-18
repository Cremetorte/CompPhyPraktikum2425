from hmac import new
import random
import electron
from electron import Electron
import numpy as np
from functions import random_percent
import matplotlib.pyplot as plt


# Constants/Parameters
NUM_ELECTRONS = 5
START_ENERGY = 20 # MeV
START_POSITION = (0, 0, 0)
START_DIRECTION = (0, 0)
T_MIN = 0.1

# probabilities 
p_moeller_mott = 0.1


electrons = [Electron(*START_POSITION, *START_DIRECTION, START_ENERGY) for i in range(NUM_ELECTRONS)]
positions = {e: [e.position()] for e in electrons}

nr_electrons_run = 0
for e in electrons:
    while e.T > T_MIN and e.is_inside():
        # get path length s
        s = -np.log(np.random.rand()) * e.T/10
        e.propagate(s)

        if random_percent(p_moeller_mott):
            # Moeller Scattering
            new_electron = Electron(*e.position(), *e.direction(), 0)
            electrons.append(new_electron)
            changed_angle = e.moeller_scatter(new_electron)
            e.energy_loss(s, not changed_angle)

        else:
            # Mott Scattering
            changed_angle = e.mott_scatter()
            e.energy_loss(s, not changed_angle)

        positions[e].append(e.position())
    print(f"calculated {nr_electrons_run} electrons")
        
        
        
        
# --------------------------------------------------------------------- Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.xlim([-10,10])
plt.ylim([-10,10])


for e in electrons:
    for pos in positions[e]:
        plt.plot(*pos, "b-")

plt.show()