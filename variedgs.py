import numpy as np

from grayscott import GrayScott
from model import Model

class VariedGS(GrayScott):
	"""
	A version of the GrayScott Model which reads it's parameters in from a grid.
	i.e., each parameter can itself be varied with time. (From another model say)
	"""
	def __init__(self, source="data/gs.dat", **kwargs):
		super().__init__(**kwargs)
		
		# point to interpolate between, given as (kill, feed)
		self.left_point = (0.06229, 0.03657)
		self.right_point = (0.06033, 0.02696)
		# Model both of them based on a clipped function.
		self.feed = np.clip((self.x+5)/10, a_min=0.0, a_max=1.0)
		self.kill = np.clip((self.x+5)/10, a_min=0.0, a_max=1.0)
		
		self.values["Feed"] = (self.feed, self.delta_feed)
		self.values["Kill"] = (self.kill, self.delta_kill)
		
		pass
	
	def evolve_parameter_model(self):
		scale_factor = 5
		pass
	
	def deltaA(self):
		A = self.activator
		H = self.inhibitor
		F = VariedGS.interpolate(self.feed, self.left_point[1], self.right_point[1])
		
		return (F*(np.ones((self.x_count, self.y_count))-A)\
				- A * np.power(H, 2)\
				+ self.Da*self.laplace(A))
	
	def deltaH(self):
		A = self.activator
		H = self.inhibitor
		F = VariedGS.interpolate(self.feed, self.left_point[1], self.right_point[1])
		K = VariedGS.interpolate(self.kill, self.left_point[0], self.right_point[0])
		
		return (A * np.power(H, 2)\
				- (F + K)*H\
				+ self.Dh*self.laplace(H))
	
	def delta_feed(self):
		"""
		Updates the feed and kill themselves by loading the model fresh.
		"""
		# self.new_data = next(self.in_model)
		
		# self.feed = self.new_data['Inhibitor']
		# self.values["Kill"] = (self.kill, self.delta_kill)
		return np.zeros((self.x_count, self.y_count))
		
	def delta_kill(self):
		# self.kill = self.new_data['Inhibitor']
		
		# self.values["Kill"] = (self.kill, self.delta_kill)
		return np.zeros((self.x_count, self.y_count))
	
	def interpolate(array: np.ndarray, left, right):
		"""
		Uses 'array' (ranging from 0 to 1), to interpolate between left and rightmost values.
		Returns a new array, ranging from left to right.
		"""
		
		return left*np.ones(array.shape) + (right-left)*array