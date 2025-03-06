# Electron Class

# Warning: Most of the physics and transformation are wrong here,
# replace it with the correct formula 

from math import sin, cos, pi, sqrt, atan, atan2, exp
import numpy as np
import numpy.random as random

def rand_dist(f, a, b, maxf):
    """
    Returns random numbers between a and b distributed with f
    Warning: this method is very ineffective for strongly varying f

    Advice: Generate the distribution function via random.choice (from numpy)
    Example for Gauß function between -5 and 5, sigma = 1:
    1. Generate the y range: 
    y = np.linspace(-5,5,num=1000)
    2. Generate and normalize the distribution
    py = np.exp(-y*y/2)
    ps = py.sum()
    py = py / ps
    3. Generate 1000 random numbers according to this distribution
    x = random.choice(y,p=py,size=1000)
    """
    while True:
        x, y = random.rand(2)
        x = a + (b-a)*x
        y = y*maxf
        if y <= f(x):
            return x



        
class Electron:

    m = 0.511
    r = 0.0005

    def __init__(self, x, y, z, dphi, dtheta, T):
        """
        Takes the initial position and direction (dphi, dtheta)
        and kinetic energy T in MeV
        """
        self.x = x
        self.y = y
        self.z = z
        self.dphi = dphi
        self.dtheta = dtheta
        self.T = T

    def __repr__(self):
        return str(self.x)+' '+str(self.y)+' '+str(self.z)


    def propagate(self, s):
        """
        Propagates the electron by s in the direction specified
        by dphi, dtheta (this is correct!)
        """
        self.x += s*sin(self.dtheta)*cos(self.dphi)
        self.y += s*sin(self.dtheta)*sin(self.dphi)
        self.z += s*cos(self.dtheta)
        self.T -= 0.1*s/self.T


    def change_direction(self, dphi, dtheta):
        """
        Changes the direction of the electron by dphi, dtheta
        using a transformation into the local system of reference
        """

        # Get velocity unit vector
        v_x = np.sin(self.dtheta) * np.cos(self.dphi)
        v_y = np.sin(self.dtheta) * np.sin(self.dphi)
        v_z = np.cos(self.dtheta)

        # change direction a little bit \Delta v
        v_x += np.sin(dtheta) * np.cos(dphi)
        v_y += np.sin(dtheta) * np.sin(dphi)
        v_z += np.cos(dtheta)

        # normalize new velocity vector
        norm = np.sqrt(v_x**2 + v_y**2 + v_z**2)
        v_x /= norm
        v_y /= norm
        v_z /= norm

        # get new angles
        self.dtheta = np.arccos(v_z)
        self.dphi = np.atan2(v_x, v_y)


    def scatter(self, other):
        """
        Elastic scattering of electron with other electron,
        the angle by which the electron gets deflected is
        chosen randomly (this is correct!)
        """
        P = sqrt((self.T + self.m)**2 - self.m**2)
        phi = random.uniform(-pi, pi)

        # Moeller scattering (warning: formulas are not correct)
        moeller = lambda x: self.r**2/4*(self.m/P)**2 * (3 + np.cos(x))**2/np.sin(x)**4
        theta_cms = rand_dist(moeller, 0.2, pi/2, moeller(0.2))
        gamma = (self.T + other.m) / np.sqrt(self.m**2 + other.m**2 + 2*self.T*other.m)

        # get new directions (Warning: partially wrong!)
        theta1 = sin(theta_cms)/gamma/(1 + cos(theta_cms))
        theta2 = sin(theta_cms)/gamma/(1 - cos(theta_cms))

        # set new directions
        self.change_direction(phi, theta1)
        other.change_direction(-phi, theta2) 

        # new momenta and energies (warning: wrong!)
        P1 = 2*self.m*(self.T + self.m)*P*np.cos(theta1)/((self.T + self.m)**2 - P**2*np.cos(theta1)**2)
        P2 = 2*self.m*(self.T + self.m)*P*np.cos(theta2)/((self.T + self.m)**2 - P**2*np.cos(theta2)**2)
        T1 = np.sqrt(P1**2 + self.m**2) - self.m
        T2 = np.sqrt(P2**2 + self.m**2) - self.m

        self.T = T1
        other.T = T2