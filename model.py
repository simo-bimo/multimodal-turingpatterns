import numpy as np
from scipy import ndimage

class Model:
	def __init__(self, dx=0.04, dy=0.04, dt=0.1, bottom_left=(-5,-5), top_right=(5,5)):
		# General Params
		self.dx=dx
		self.dy=dy
		
		# Parameters for Simulation
		self.dt = dt
		self.curr_step = 0
		
		# Two grids, one with a set of x coordinates, 
		# one with a set of y coordinates.
		# The next two values are just the number of points.
		self.x, self.y, self.x_count, self.y_count = Model.generate_grid(dx=self.dx, dy=self.dy,\
															 bottom_left=bottom_left, top_right=top_right)

		# Every model needs a laplacian for diffusion.
		# stencil = np.array([[0, 1, 0],[1, -4, 1], [0, 1, 0]])
		stencil = np.array([[0.05, 0.2, 0.05],[0.2, -1, 0.2], [0.05, 0.2, 0.05]])
		lapl = lambda x: ndimage.convolve(x, stencil, mode='wrap')
		self.laplace = lapl
		
		# The point at which to round a float down to zero.
		self.zero_tol = 1e-6
		
		# A dictionary of the values, and their corresponding step functions.
		# The key is a string, the value is (np.ndarray, function)
		self.values = {}
		pass
	
	def take_step(self, num=1):
		for i in range(0, num):
			deltas = {}
			# Calculate changes to substances
			for k in self.values:
				substance,func = self.values[k]
				deltas[k] = func() * self.dt
			
			# Apply changes to substances
			for k in self.values:
				substance,func = self.values[k]
				substance += deltas[k]
				# Clip to [0,1]
				np.clip(substance, a_min=0.0, a_max=1.0)
				# Round zeros down.
				substance[substance < self.zero_tol] = 0.0
				self.values[k] = (substance,func)

		self.curr_step+=num
		pass
	
	def generate_grid(dx=1, dy=1, bottom_left=(-5,-5), top_right=(5,5), **kwargs):
		'''
		Generates a grid of x values and y values, 
		based on the distance between points (dx, dy),
		and the corners specified.
		Returns a grid of x values, a grid of y values,
		the number of x values, and the number of y values.
		'''

		x_start = bottom_left[0]
		x_stop = top_right[0]
		
		y_start = bottom_left[1]
		y_stop = top_right[1]

		x_num = round((x_stop - x_start) / dx) + 1
		y_num = round((y_stop - y_start) / dy) + 1

		x = np.linspace(x_start, x_stop, x_num)
		y = np.linspace(y_start, y_stop, y_num)

		x_vals, y_vals = np.meshgrid(x,y, **kwargs)

		return x_vals, y_vals, x_num, y_num