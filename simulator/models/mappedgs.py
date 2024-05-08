from .model import Model
from .grayscott import GrayScott
from .variedgs import VariedGS

import numpy as np

class MappedGS(GrayScott):
	"""
	A GrayScott Model which interprets all parameters through a mapping.
	Parameters are checked from the mapping every frame, and so can be changed adaptively with the model itself.
	@param mapping: a dictionary that maps a parameter name i.e 'feed' to a function to get the next feed.
	@param update_func: an optional function that is called once per step (i.e. to take a step in another model)
	Note if scale is going to be <1, it is recommended to set dt < 1 aswell in proportion, so that we aren't taking
	excessively large steps in reaction processes each frame.
	"""
	def __init__(self, mapping={}, update_func=lambda: None, **kwargs):
		super().__init__(**kwargs)
		self.mapping = mapping
		self.update_func = update_func
		
		# If any values are not mapped, set a sensible default.
		self.set_default('Feed', 			  	0.055*np.ones(self.x.shape))
		self.set_default('Kill', 		 	  	0.062*np.ones(self.x.shape))
		self.set_default('Activator Diffusion',   1.0*np.ones(self.x.shape))
		self.set_default('Inhibitor Diffusion',   0.5*np.ones(self.x.shape))
		self.set_default('Scale', 					  np.ones(self.x.shape))
		
		return
	
	def set_default(self, key: str, default: np.ndarray):
		if key in self.mapping:
			return
		self.mapping[key] = lambda: default
		return
	
	def take_step(self, num=1):
		for i in range(0, num):
			self.update_func()
			super().take_step()
		# append mapped values to values
		for k in self.mapping:
			self.other_store["Mapped_"+k] = self.mapping[k]()
		
		return
	
	def take_step_opt(self, num=1):
		for i in range(0, num):
			self.update_func()
			super().take_step_opt(1)
		return
	
	def deltaA(self):
		A = self.activator
		H = self.inhibitor
		F = self.mapping['Feed']()
		S = self.mapping['Scale']()
		Da = self.mapping['Activator Diffusion']()
		
		# import pdb; pdb.set_trace()
		
		return (F * (np.ones(self.x.shape)-A)\
				- A * np.power(H, 2) ) / S \
				+ Da*self.laplace(A)
	
	def deltaH(self):
		A = self.activator
		H = self.inhibitor
		F = self.mapping['Feed']()
		K = self.mapping['Kill']()
		S = self.mapping['Scale']()
		Dh = self.mapping['Inhibitor Diffusion']()
		
		return (A * np.power(H, 2)\
				- (F + K)*H)/S\
				+ Dh*self.laplace(H)
	
	def interpolate(array: np.ndarray, left, right):
		"""
		Uses 'array' (ranging from 0 to 1), to interpolate between left and rightmost values.
		Returns a new array, ranging from left to right.
		"""
		
		return left*np.ones(array.shape) + (right-left)*array