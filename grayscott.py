import numpy as np
import scipy
from utilities import generate_grid

class GrayScott:
    def __init__(self):
        # General Params
        self.dx=0.1
        self.dy=0.1

        self.feed = 0.025
        self.decay = 0.15
        # Parameters for activator
        self.Da = 0.00001
        # Parameters for inhibitor
        self.Dh = 0.00002

        # Parameters for Simulation
        self.dt = self.dx * self.dy * self.Dh
        self.curr_step = 0

        # Two grids, one with a set of x coordinates, 
        # one with a set of y coordinates.
        # The next two values are just the number of points.
        self.x, self.y, self.x_count, self.y_count = generate_grid(dx=self.dx, dy=self.dy)

        # Initialise all four values to random variables to begin.
        self.activator = np.random.rand(self.x_count, self.y_count) * 0.1
        self.inhibitor = np.random.rand(self.x_count, self.y_count) * 0.1

        # self.activator = np.ones((self.x_count, self.y_count)) * 0.001
        # self.inhibitor = np.ones((self.x_count, self.y_count)) * 0.01

        # To choose laplacian
        self.laplace = scipy.ndimage.laplace
        pass
    
    def deltaA(self):
        A = self.activator
        H = self.inhibitor
        
        return (-A * np.power(H, 2)\
                + self.feed*(1-A)\
                + self.Da*self.laplace(A))
    
    def deltaH(self):
        A = self.activator
        H = self.inhibitor
        
        return (A * np.power(H, 2)\
                - (self.feed + self.decay)*H\
                + self.Dh*self.laplace(H))
    
    def take_step(self, num=1):
        for i in range(0, num):
            delA = self.deltaA() * self.dt
            delH = self.deltaH() * self.dt

            self.activator += delA
            self.inhibitor += delH

            np.clip(self.activator, a_min=0.0, a_max=1.0)
            np.clip(self.inhibitor, a_min=0.0, a_max=1.0)

        self.curr_step+=num
        pass