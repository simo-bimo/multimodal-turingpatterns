import numpy as np
from .model import Model

class GrayScott(Model):
	def __init__(self, feed=0.055, decay=0.062, 
			  activator_diffusion=1.0, 
			  inhibitor_diffusion=0.5, 
			  diffusion_extra=1,
			  **kwargs):
		super().__init__(**kwargs)

		self.feed = feed
		self.decay = decay
		
		self.Da = activator_diffusion
		self.Dh = inhibitor_diffusion
		
		# number of diffusion frames to run before also doing the reaction
		self.diffusion_extra = diffusion_extra
		
		# reasonable initial condition
		self.set_activator(np.ones((self.x_count, self.y_count)))
		self.set_inhibitor(np.zeros((self.x_count, self.y_count)))
		self.add_inhibitor(r=0.5)
		pass
	
	def set_activator(self, value):
		self.activator = value
		self.values["Activator"] = (self.activator, self.deltaA)
		pass
	
	def set_inhibitor(self, value):
		self.inhibitor = value
		self.values["Inhibitor"] = (self.inhibitor, self.deltaH)
		pass
	
	def deltaA(self):
		A = self.activator
		H = self.inhibitor
		F = self.feed
		Da = self.Da
		
		# import pdb; pdb.set_trace()
		
		if (self.curr_step % self.diffusion_extra == 0):
			return (F * (np.ones(self.x.shape)-A)\
					- A * np.power(H, 2)\
					+ Da*self.laplace(A))
		return self.Da*self.laplace(A)
	
	def deltaH(self):
		A = self.activator
		H = self.inhibitor
		F = self.feed
		K = self.decay
		Dh = self.Dh
		if (self.curr_step % self.diffusion_extra == 0):
			return (A * np.power(H, 2)\
					- (F + K)*H\
					+ Dh*self.laplace(H))
		return Dh*self.laplace(H)
	
	def add_activator(self, p = (0.0, 0.0), r = 1.0, amount = 1.0):
		"""
		Adds a circle of activation, by default in the middle.
		"""

		mask = (self.x - p[0])**2 + (self.y - p[1])**2 <= r**2

		self.activator += mask*amount

		# self.activator += np.random.rand(self.x_count, self.y_count) / 100
		np.clip(self.activator, a_min=0.0, a_max=1.0)

		pass

	def add_inhibitor(self, p = (0.0, 0.0), r = 1.0, amount = 1.0):
		"""
		Adds a circle of activation, by default in the middle.
		"""

		mask = (self.x - p[0])**2 + (self.y - p[1])**2 <= r**2

		self.inhibitor += mask*amount

		# self.inhibitor += np.random.rand(self.x_count, self.y_count) / 100
		np.clip(self.inhibitor, a_min=0.0, a_max=1.0)

		pass