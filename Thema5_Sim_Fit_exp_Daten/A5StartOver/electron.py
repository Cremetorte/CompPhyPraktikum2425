import numpy as np
from functions import rand_dist_alt


class Electron:
    m = 0.511
    r = 0.0005

    def __init__(self, x, y, z, theta, phi, T):
        self.x = x
        self.y = y
        self.z = z
        self.theta = theta
        self.phi = phi
        self.T = T

    def position(self):
        return (self.x, self.y, self.z)
    
    def direction(self):
        return (self.theta, self.phi)
    
    def gamma(self):
        return 1 + self.T/self.m
    
    def beta(self):
        return np.sqrt(1 - 1/self.gamma()**2)
    

    def propagate(self, distance):
        self.x += distance * np.cos(self.theta) * np.cos(self.phi)
        self.y += distance * np.cos(self.theta) * np.sin(self.phi)
        self.z += distance * np.sin(self.theta) 

    def moeller_scatter(self, other):
        P = np.sqrt((self.T + self.m)**2 - self.m**2)
        phi = np.random.rand() * 2 * np.pi

        # Moeller scattering (warning: formulas are not correct)
        moeller = lambda x: self.r**2/4*(self.m/P)**2 * (3 + np.cos(x))**2/np.sin(x)**4
        theta_cms = rand_dist_alt(moeller, 0.0001, np.pi/2)
        
        

        


        if theta_cms >= 0.2:
            gamma = (self.T + other.m) / np.sqrt(self.m**2 + other.m**2 + 2*self.T*other.m)

            # get new directions (Warning: partially wrong!)
            theta1 = np.sin(theta_cms)/gamma/(1 + np.cos(theta_cms))
            theta2 = np.sin(theta_cms)/gamma/(1 - np.cos(theta_cms))
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

            return True
        
        return False


    def mott_scatter(self):
        phi = np.random.rand() * 2 * np.pi
        mott = lambda x: 1/self.T**2/np.sin(x/2)**4 * (1 - self.beta()*np.sin(x/2)**2)
        theta_cms = rand_dist_alt(mott, 0.0001, np.pi/2)

        if theta_cms >= 0.2:
            gamma = 1

            # get new directions (Warning: partially wrong!)
            theta1 = np.sin(theta_cms)/gamma/(1 + np.cos(theta_cms))
            theta2 = np.sin(theta_cms)/gamma/(1 - np.cos(theta_cms))
            # set new directions
            self.change_direction(phi, theta1)
            
            # new momenta and energies (warning: wrong!)
            P1 = 2*self.m*(self.T + self.m)*P*np.cos(theta1)/((self.T + self.m)**2 - P**2*np.cos(theta1)**2)

            T1 = np.sqrt(P1**2 + self.m**2) - self.m

            self.T = T1

            return True
        return False

    def energy_loss(self, path_length, CSDA_approx):
        if CSDA_approx:
            self.T -= 0.1*self.T*path_length
        else:
            pass

    def is_inside(self):
        return self.z >= 0 and self.z < 10 and self.x > -10 and self.x < 10 and self.y > -10  and self.y < 10