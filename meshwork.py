import numpy as np
import scipy
from utilities import generate_grid

class MeshworkSystem:

    def __init__(self):
        # Parameters for activator
        self.c = 1.0
        self.mu = 1.0
        self.rho_a = 1.0
        self.Da = 1.0
        # Parameters for inhibitor
        self.v = 1.0
        self.rho_h = 1.0
        self.Dh = 1.0
        # Parameters for Substrate
        self.c_naught = 1.0
        self.gamma = 1.0
        self.epsilon = 1.0
        self.Ds = 1.0
        # Parameters for Differentiation
        self.d = 1.0
        self.e = 1.0
        self.f = 1.0

        # Parameters for Simulation
        self.dt = 0.1
        self.curr_step = 0

        # Two grids, one with a set of x coordinates, 
        # one with a set of y coordinates.
        # The next two values are just the number of points.
        self.x, self.y, x_count, y_count = generate_grid(dx=0.1, dy=0.1)

        # Initialise all four values to random variables to begin.
        # self.activator = np.random.rand(x_count, y_count)
        # self.inhibitor = np.random.rand(x_count, y_count)
        # self.substrate = np.random.rand(x_count, y_count)
        # self.differentiation = np.random.rand(x_count, y_count)

        self.activator = np.ones((x_count, y_count)) /  1000
        self.inhibitor = np.ones((x_count, y_count)) / 100
        self.substrate = np.ones((x_count, y_count))
        self.differentiation = np.zeros((x_count, y_count))

        self.add_differentiation()

        # To choose laplacian
        self.laplace = scipy.ndimage.laplace

        pass

    def add_differentiation(self, p = (0.0, 0.0), r = 1, amount = 1.0):
        """
        Adds a circle of subtrate in the middle.
        """

        mask = (self.x - p[0])**2 + (self.y - p[1])**2

        self.differentiation += mask*amount

        pass

    def deltaA(self):
        A = self.activator
        H = self.inhibitor
        S = self.substrate
        Y = self.differentiation
        
        return self.c*np.power(A, 2)*S/H \
                - self.mu*A\
                + self.rho_a*Y\
                + self.Da*self.laplace(A)
    
    def deltaH(self):
        A = self.activator
        H = self.inhibitor
        S = self.substrate
        Y = self.differentiation
        
        return self.c*np.power(A, 2)*S \
                - self.v*H\
                + self.rho_h*Y\
                + self.Dh*self.laplace(H)
    
    def deltaS(self):
        A = self.activator
        H = self.inhibitor
        S = self.substrate
        Y = self.differentiation
        
        return self.c_naught \
                - self.gamma*S\
                + self.epsilon*S*Y\
                + self.Ds*self.laplace(S)

    def deltaY(self):
        A = self.activator
        H = self.inhibitor
        S = self.substrate
        Y = self.differentiation
        
        return self.d * A \
                - self.e*Y\
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
