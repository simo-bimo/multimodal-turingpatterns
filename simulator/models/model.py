import numpy as np
from scipy import ndimage
import pickle

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Model:
	def __init__(self, dx=0.04, dy=0.04, dt=1.0, bottom_left=(-5,-5), top_right=(5,5)):
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
		# other values to store when converting to file.
		self.other_store = {}
		
		self.clip = True
		self.clip_min=0.0
		self.clip_max=1.0
		pass
	
	def take_step_opt(self, num=1):
		"""
		An optimised version of take-step that uses maps instead of for loops on values.
		TESTED - Correct but actually slower. May make a difference depending on numpy
		backend, could also open up to some threading but I doub't it'd be significant.
		"""
		for i in range(0, num):
			def calc_delt(k,v):
				return v[1]() * self.dt
			
			deltas = map(calc_delt, self.values.keys(), self.values.values())
			
			if self.clip:
				def update(k,v,d):
					sub = v[0]
					sub += d
					if np.iscomplexobj(sub):
						np.clip(sub.real, a_min=self.clip_min, a_max=self.clip_max, out=sub.real)
						np.clip(sub.imag, a_min=self.clip_min, a_max=self.clip_max, out=sub.imag)
						# rounds down zeros
						sub[np.abs(sub) < self.zero_tol] = 0.0
					else:
						np.clip(sub, a_min=self.clip_min, a_max=self.clip_max, out=sub)
						sub[sub < self.zero_tol] = 0.0
					return k,(sub, v[1])
			else: 
				def update(k,v,d):
					sub = v[0]
					sub += d
					if np.iscomplexobj(sub):
						sub[np.abs(sub) < self.zero_tol] = 0.0
					else:
						sub[sub < self.zero_tol] = 0.0
					return k,(sub, v[1])
			
			self.values = dict(map(update, self.values.keys(), self.values.values(), deltas))
			
			self.curr_step+=1
	
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
	
	def to_file(model, filename: str, frames=1000, steps_per_frame=20, optimised=False):
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
				for k in model.other_store:
					# Avoid overwrites
					new_key = k
					if k in vals:
						new_key += '_other'
					vals[new_key] = model.other_store[k]
				pickle.dump(vals, handle, protocol=pickle.HIGHEST_PROTOCOL)
				pickle.dump(vals, handle, protocol=pickle.HIGHEST_PROTOCOL)
				if optimised:
					model.take_step_opt(steps_per_frame)
				else:
					model.take_step(steps_per_frame)
			vals = {}
			for k in model.values:
				vals[k] = model.values[k][0]
			for k in model.other_store:
				# Avoid overwrites
				new_key = k
				if k in vals:
					new_key += '_other'
				vals[new_key] = model.other_store[k]
			pickle.dump(vals, handle, protocol=pickle.HIGHEST_PROTOCOL)
		pass
	
	def from_file(filename):
		"""
		Yields the values function of each frame with each call.
		The first two values are the x, and then y coordinates.
		"""
		handle = open(filename+".dat", "rb")
		while True:
			try:
				value = pickle.load(handle)
			except EOFError:
				break
			yield value
		handle.close()
		pass
			
		
	def create_animation(name: str, source: str, to_plot: str, frame_count=1000, frame_skip=20, plot_func = lambda x: x):
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
	
	def get_last(source, do_cache=True):
		"""
		Gets the last frame stored in a serialised model.
		@param do_cache, whether to save the file with _last 
			as an extension for future calls to the function.
		"""
		do_save=False
		if do_cache:
			new_source=source+'_last'
			try:
				generator = Model.from_file(new_source)
				x = next(generator)
				do_save = False
			except FileNotFoundError:
				do_save = True
				generator = Model.from_file(source)		
				x = next(generator)
		
		y = next(generator)
		last = None
		for curr in generator:
			last = curr
			
		if do_cache and do_save:
			with open(new_source+".dat", 'wb') as handle:
				pickle.dump(x, handle, protocol=pickle.HIGHEST_PROTOCOL)
				pickle.dump(y, handle, protocol=pickle.HIGHEST_PROTOCOL)
				pickle.dump(last, handle, protocol=pickle.HIGHEST_PROTOCOL)
		
		return last, x, y
	
	def compare_difference(sources: list[str], tolerance=1e-5, do_print = False):
		models = list(map(Model.from_file, sources))
		
		xs = list(map(next, models))
		ys = list(map(next, models))
		
		# verify identical shapes
		shapes = list(map(lambda x: x.shape, xs))
		# rolling by zero converts it to an ndarray 
  		# so the comparison can take place
		shape_comparisons = (np.roll(shapes,0) - np.roll(shapes, 1))
		if (np.max(shape_comparisons)):
			raise ValueError(f"Some models have a different shape: {shape_comparisons}")
		
		dicts = list(map(next, models))
		count = 0
		while dicts:
			vals = list(map(lambda x: list(x.values()), dicts))
			difference = np.abs(np.roll(vals, 0, 0) - np.roll(vals, 1, 0))
			difference[difference <= tolerance] = 0.0
			if (difference.max() > 0.0):
				if do_print:
					print(f"Difference outside tolerance of: {np.max(difference)}")
				count += 1
			dicts = list(map(next, models))
		
		# Close remaining files.
		for x in models:
			[y for y in x]
		
		return count
			
		
		