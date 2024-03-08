import numpy as np
import scipy
from utilities import generate_grid

class GrayScott:
    def __init__(self, feed=0.025, decay=0.15):
        # General Params
        self.dx=0.04
        self.dy=0.04

        self.feed = feed
        self.decay = decay
        # Parameters for activator
        self.Da = 0.00001
        # Parameters for inhibitor
        self.Dh = 0.00002

        # Parameters for Simulation
        self.dt = 0.1
        self.curr_step = 0

        # Two grids, one with a set of x coordinates, 
        # one with a set of y coordinates.
        # The next two values are just the number of points.
        self.x, self.y, self.x_count, self.y_count = generate_grid(dx=self.dx, dy=self.dy, bottom_left=(-1,-1), top_right=(1,1))

        # Initialise all four values to random variables to begin.
        self.activator = np.random.rand(self.x_count, self.y_count) * 0
        self.inhibitor = np.random.rand(self.x_count, self.y_count) * 0

        # self.activator = np.ones((self.x_count, self.y_count)) * 0.001
        # self.inhibitor = np.ones((self.x_count, self.y_count)) * 0.01

        # To choose laplacian
        self.laplace = scipy.ndimage.laplace
        pass
    
    def deltaA(self):
        A = self.activator
        H = self.inhibitor
        
        return (self.feed*(1.0-A)\
                - A * np.power(H, 2)\
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

    def add_activator(self, p = (0.0, 0.0), r = 1.0, amount = 1.0):
        """
        Adds a circle of activation, by default in the middle.
        """

        mask = (self.x - p[0])**2 + (self.y - p[1])**2 <= r**2

        self.activator += mask*amount

        self.activator += np.random.rand(self.x_count, self.y_count) / 100
        np.clip(self.activator, a_min=0.0, a_max=1.0)

        pass