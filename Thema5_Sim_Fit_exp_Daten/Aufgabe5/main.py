from Electron_temp import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import exp
import numpy as np

T0 = 20.0
Tmin = 0.5
numElectrons = 1000

def random_percent(p):
    return np.random.rand() < p

def getElectronTrajectory(el, electrons):
    """
    This returns a curve x, y, z of one electron and adds newly created electrons to the list
    """
    x = [el.x]
    y = [el.y]
    z = [el.z]
    while el.T > Tmin and el.z >= 0 and el.z < 10 and el.x > -10 and el.y > -10 and el.x < 10 and el.y < 10:
    # while el.T > Tmin and el.z >= 0 and el.z < 10:
        s = rand_dist(lambda x: exp(-x), 0, 100, 1)
        el.propagate(s*el.T/10)
        
        if random_percent(0.5):
            newElectron = Electron(el.x, el.y, el.z, el.dphi, el.dtheta, 0)
            el.moeller_scatter(newElectron)
            electrons.append(newElectron)
        else:  
            el.mott_scatter()           
        
        
        if (el.z >= 0 and el.z < 10 and el.x > -10 and el.y > -10 and el.x < 10 and el.y < 10):
            x.append(el.x)
            y.append(el.y)
            z.append(el.z)
    return x, y, z

def main():

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    

    electrons = [ Electron(0, 0, 0, 0, 0, T0) for i in range(numElectrons) ]

    for el in electrons:
        if el.T < Tmin or el.z < 0 or el.z > 10:
            continue
        x, y, z = getElectronTrajectory(el, electrons)
        plt.plot(x, y, z, 'b-')

    plt.xlim([-10,10])
    plt.ylim([-10,10])
    ax.set_zlim([0, 10])
    plt.show()


if __name__ == '__main__':
    main()