import numpy as np
from numpy import sin, cos, tan, atan2, arccos, sqrt, pi

from Thema5_Sim_Fit_exp_Daten.A5DIY.functions import fifty_fifty, rand_dist



class Electron:
    m = 0.511
    r = 0.0005


    # Constructor
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
        self.T = T  # Kinetic energy


    # Postion getter
    def position(self):
        return np.array([self.x, self.y, self.z])


    # # get gamma factor
    # def gamma(self):
    #     return 1 + self.T/self.m

    # # Get Beta factor
    # def beta(self):
    #     return sqrt(1 - 1/self.gamma()**2)


    def propagate(self, s):
        """
        Propagates the electron by s in the direction specified
        by dphi, dtheta (this is correct!)
        Energy loss is handled by energy loss method called by scattering method
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
        v_x = sin(self.dtheta) * cos(self.dphi)
        v_y = sin(self.dtheta) * sin(self.dphi)
        v_z = cos(self.dtheta)

        # change direction a little bit \Delta v
        v_x += sin(dtheta) * cos(dphi)
        v_y += sin(dtheta) * sin(dphi)
        v_z += cos(dtheta)

        # normalize new velocity vector
        norm = sqrt(v_x**2 + v_y**2 + v_z**2)
        v_x /= norm
        v_y /= norm
        v_z /= norm

        # get new angles
        self.dtheta = arccos(v_z)
        self.dphi = atan2(v_x, v_y)


def moeller_scatter(self, other):
    """
    Elastic scattering of electron with other electron,
    the angle by which the electron gets deflected is
    chosen randomly (this is correct!)
    """
    P = sqrt((self.T + self.m)**2 - self.m**2)
    phi = np.random.uniform(-pi, pi)

    
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