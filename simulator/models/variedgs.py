import numpy as np

from .grayscott import GrayScott
from .model import Model

class VariedGS(GrayScott):
	"""
	A version of the GrayScott Model which reads it's parameters in from a grid.
	i.e., each parameter can itself be varied with time. (From another model say)
	This takes a source file, and uses it to generate a pattern of phase transitions.
	The source file is read statically from the last computer model - it does not evolve over time.
	"""
	def __init__(self, 
			  source="data/gs", 
			  left=(0.06229, 0.03657), 
			  right=(0.06033, 0.02696), 
			  **kwargs):
		super().__init__(**kwargs)
		
		# point to interpolate between, given as (kill, feed)
		self.left_point = left
		self.right_point = right
		
		# Model both of them based on the final state of a pre-computed model.
		data = Model.get_last(source)
		if (data['Inhibitor'].shape != self.x.shape):
			raise ValueError("Given model is of incorrect shape.")
		self.feed = data['Inhibitor']
		self.kill = data['Inhibitor']
		
		self.values["Feed"] = (self.feed, self.delta_feed)
		self.values["Kill"] = (self.kill, self.delta_kill)
		
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