from hmac import new
import random
import electron
import numpy as np
from functions import random_percent


# Constants/Parameters
NUM_ELECTRONS = 10
START_ENERGY = 20 # MeV
START_POSITION = (0, 0, 0)
START_DIRECTION = (0, 0)
T_MIN = 0.1

# probabilities 
p_mott_moeller = 0.5


electrons = [electron(*START_POSITION, *START_DIRECTION, START_ENERGY) for i in range(NUM_ELECTRONS)]
positions = {e: [e.position()] for e in electrons}


for e in electrons:
    if e.T > T_MIN and e.is_inside():
        # get path length s
        s = -np.log(np.random.rand()) * e.T/10
        e.propagate(s)

        if random_percent(p_mott_moeller):
            # Moeller Scattering
            new_electron = electron(*e.position(), *e.direction(), 0)
            electrons.append(new_electron)
            changed_angle = e.moeller_scatter(new_electron)
            e.energy_loss(s, not changed_angle)

        else:
            # Mott Scattering
            changed_angle = e.mott_scatter()
            e.energy_loss(s, not changed_angle)

        positions[e].append(e.position())
        