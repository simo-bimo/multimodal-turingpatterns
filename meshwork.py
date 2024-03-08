import numpy as np
import scipy
from utilities import generate_grid

"""
This code is based on a model proposed in the following paper:
Guo, S., Sun, M. Z., & Zhao, X. (2021). Wavelength of a Turing-type mechanism regulates the morphogenesis of meshwork patterns. Scientific Reports, 11(1), 4813.
"""

class MeshworkSystem:
    def __init__(self):
        # General Params
        self.dx=0.3
        self.dy=0.3

        # Parameters for activator
        self.c = 0.002
        self.mu = 0.16
        self.rho_a = 0.03
        self.Da = 0.02
        # Parameters for inhibitor
        self.v = 0.04
        self.rho_h = 0.00005
        self.Dh = 0.26
        # Parameters for Substrate
        self.c_naught = 0.02
        self.gamma = 0.02
        self.epsilon = 0.475
        self.Ds = 0.06
        # Parameters for Differentiation
        self.d = 0.008
        self.e = 0.1
        self.f = 10.0

        # Parameters for Simulation
        self.dt = self.dx * self.dy * 0.4 * self.Dh
        self.curr_step = 0

        # Two grids, one with a set of x coordinates, 
        # one with a set of y coordinates.
        # The next two values are just the number of points.
        self.x, self.y, self.x_count, self.y_count = generate_grid(dx=self.dx, dy=self.dy,
                                                                   bottom_left = (-15, -15),
                                                                   top_right=(15, 15))

        # Initialise all four values to random variables to begin.
        self.activator = np.random.rand(self.x_count, self.y_count) * 0.1
        self.inhibitor = np.random.rand(self.x_count, self.y_count) * 0.01
        # self.substrate = np.random.rand(self.x_count, self.y_count) 
        self.differentiation = np.random.rand(self.x_count, self.y_count)

        # self.activator = np.ones((self.x_count, self.y_count)) * 0.001
        # self.inhibitor = np.ones((self.x_count, self.y_count)) * 0.01
        self.substrate = np.ones((self.x_count, self.y_count))
        # self.differentiation = np.ones((self.x_count, self.y_count)) * 0.0

        # To choose laplacian
        self.laplace = scipy.ndimage.laplace

        pass

    def add_differentiation(self, p = (0.0, 0.0), r = 1, amount = 1.0):
        """
        Adds a circle of differentiated cells, by default in the middle.
        """

        mask = (self.x - p[0])**2 + (self.y - p[1])**2 <= r**2

        self.differentiation += mask*amount

        self.differentiation += np.random.rand(self.x_count, self.y_count) / 100
        np.clip(self.differentiation, a_min=0.0, a_max=1.0)

        pass

    def deltaA(self):
        A = self.activator
        H = self.inhibitor
        S = self.substrate
        Y = self.differentiation
        
        return ((self.c*np.power(A, 2)*S)/H) \
                - (self.mu*A)\
                + (self.rho_a*Y)\
                + (self.Da*self.laplace(A))
    
    def deltaH(self):
        A = self.activator
        H = self.inhibitor
        S = self.substrate
        Y = self.differentiation
        
        return (self.c*np.power(A, 2)*S) \
                - (self.v*H)\
                + (self.rho_h*Y)\
                + (self.Dh*self.laplace(H))
    
    def deltaS(self):
        A = self.activator
        H = self.inhibitor
        S = self.substrate
        Y = self.differentiation
        
        return (self.c_naught) \
                - (self.gamma*S)\
                + (self.epsilon*S*Y)\
                + (self.Ds*self.laplace(S))

    def deltaY(self):
        A = self.activator
        H = self.inhibitor
        S = self.substrate
        Y = self.differentiation
        
        return (self.d * A) \
                - (self.e*Y)\
                + ( np.power(Y, 2) / (1 + self.f*np.power(Y, 2)) )
    
    def take_step(self, num=1):
        for i in range(0, num):
            delA = self.deltaA() * self.dt
            delH = self.deltaH() * self.dt
            delS = self.deltaS() * self.dt
            delY = self.deltaY() * self.dt

            self.activator += delA
            self.inhibitor += delH
            self.substrate += delS
            self.differentiation += delY

            np.clip(self.differentiation, a_min=0.0, a_max=1.0)

        self.curr_step+=num
        pass

    def take_step_subsystem(self, num=1):
        for i in range(0, num):
            delA = self.deltaA() * self.dt
            delH = self.deltaH() * self.dt

            self.activator += delA
            self.inhibitor += delH

            np.clip(self.differentiation, a_min=0.0, a_max=1.0)

        self.curr_step+=num
        pass

