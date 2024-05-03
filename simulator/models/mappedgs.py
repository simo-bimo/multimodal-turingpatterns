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
	"""
	def __init__(self, mapping: dict, update_func=lambda x: None, **kwargs):
		super().__init__(**kwargs)
		self.mapping = mapping
		self.update_func = update_func
		
		# If any values are not mapped, set a sensible default.
		self.set_default('Feed', 			  	0.055*np.ones(self.x.shape))
		self.set_default('Kill', 		 	  	0.062*np.ones(self.x.shape))
		self.set_default('Activator Diffusion', 1.000*np.ones(self.x.shape))
		self.set_default('Inhibitor Diffusion', 0.500*np.ones(self.x.shape))
		self.set_default('Scale', 				1.000*np.ones(self.x.shape))
		
		return
	
	def set_default(self, key: str, default: np.ndarray):
		if key in self.mapping:
			return
		self.mapping[key] = lambda: default
		return
	
	def take_step(self, num=1):
		for i in range(0, num):
			self.update_func(1)
			super().take_step(1)
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
		
		return (F*(np.ones(self.x.shape)-A)/S\
				- A * np.power(H, 2)/S\
				+ Da*self.laplace(A))
	
	def deltaH(self):
		A = self.activator
		H = self.inhibitor
		F = self.mapping['Feed']()
		K = self.mapping['Kill']()
		S = self.mapping['Scale']()
		Dh = self.mapping['Inhibitor Diffusion']()
		
		return (A * np.power(H, 2)/S\
				- (F + K)*H/S\
				+ Dh*self.laplace(H))