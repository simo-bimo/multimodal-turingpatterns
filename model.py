import numpy as np
from scipy import ndimage
import pickle

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Model:
	def __init__(self, dx=0.04, dy=0.04, dt=0.1, bottom_left=(-5,-5), top_right=(5,5)):
		# General Params
		self.dx=dx
		self.dy=dy
		
		self.bottom_left=bottom_left
		self.top_right=top_right
		
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
		
		self.clip = True
		self.clip_min=0.0
		self.clip_max=1.0
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
				if self.clip:
					if np.iscomplexobj(substance):
						np.clip(substance.real, a_min=self.clip_min, a_max=self.clip_max, out=substance.real)
						np.clip(substance.imag, a_min=self.clip_min, a_max=self.clip_max, out=substance.imag)
					else:
						np.clip(substance, a_min=self.clip_min, a_max=self.clip_max, out=substance)
						
				# Round zeros down.
				if np.iscomplexobj(substance):
					substance[np.abs(substance) < self.zero_tol] = 0.0
				else:
					substance[substance < self.zero_tol] = 0.0
				self.values[k] = (substance,func)
			self.curr_step+=1

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
	
	def to_file(model, filename: str, frames=1, steps_per_frame=1):
		"""
		Saves result of simulation with frames frames into filename.dat.
		"""
		with open(filename+".dat", 'wb') as handle:
			# Write the x and y first so plotting can use them
			pickle.dump(model.x, handle, protocol=pickle.HIGHEST_PROTOCOL)
			pickle.dump(model.y, handle, protocol=pickle.HIGHEST_PROTOCOL)
			
			for curr_frame in range(0, frames):
				vals = {}
				for k in model.values:
					vals[k] = model.values[k][0]
				pickle.dump(vals, handle, protocol=pickle.HIGHEST_PROTOCOL)
				pickle.dump(vals, handle, protocol=pickle.HIGHEST_PROTOCOL)
				model.take_step(steps_per_frame)
			vals = {}
			for k in model.values:
				vals[k] = model.values[k][0]
			pickle.dump(vals, handle, protocol=pickle.HIGHEST_PROTOCOL)
		pass
	
	def from_file(filename):
		"""
		Yields the values function of each frame with each call.
		The first two values are the x, and then y coordinates.
		"""
		handle = open(filename+".dat", "rb")
		value = pickle.load(handle)
		while not value is None:
			yield value
			value = pickle.load(handle)
		handle.close()
		
	def create_animation(name, source, to_plot, frame_count=1000, frame_skip=20, plot_func = lambda x: x):
		"""
		Creates an animation saved in 'name.gif' from the model source 'source.dat',
		plotting the value 'to_plot'. 
		plot_func is a func that is applied to the plotted value to make it palatable.
		i.e. np.real().
		frame_skip is the number of frames to label as skipped in the title. This doesn't
		affect how many frames are actually rendered at all.
		"""
		print(f"Beginning animation '{name}' from '{source}.dat'")
		data = Model.from_file(source)
		x = next(data)
		y = next(data)

		fig, ax = plt.subplots()
		fig.suptitle(f"{to_plot}: 0")


		quad = ax.pcolormesh(x, y, plot_func(next(data)[to_plot]))
		cb = plt.colorbar(quad)

		def animate(i):
			fig.suptitle(f"{to_plot}: {i*frame_skip}")
			quad.set_array(plot_func(next(data)[to_plot]))
			return quad,

		anim = FuncAnimation(fig, animate, frames=frame_count)

		anim.save('animations/'+name+'.gif', writer='pillow', fps=30)
		print("Saved animation: " + name)
		pass