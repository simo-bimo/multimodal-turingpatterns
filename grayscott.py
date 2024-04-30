import numpy as np
from model import Model

class GrayScott(Model):
	def __init__(self, feed=0.055, decay=0.062, 
			  activator_diffusion=1.0, 
			  inhibitor_diffusion=0.5, 
			  **kwargs):
		super().__init__(**kwargs)

		self.feed = feed
		self.decay = decay
		
		self.Da = activator_diffusion
		self.Dh = inhibitor_diffusion
		
		self.set_activator(np.zeros((self.x_count, self.y_count)))
		self.set_inhibitor(np.zeros((self.x_count, self.y_count)))
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
		
		return (self.feed*(np.ones((self.x_count, self.y_count))-A)\
				- A * np.power(H, 2)\
				+ self.Da*self.laplace(A))
	
	def deltaH(self):
		A = self.activator
		H = self.inhibitor
		
		return (A * np.power(H, 2)\
				- (self.feed + self.decay)*H\
				+ self.Dh*self.laplace(H))
	
	def add_activator(self, p = (0.0, 0.0), r = 1.0, amount = 1.0):
		"""
		Adds a circle of activation, by default in the middle.
		"""

		mask = (self.x - p[0])**2 + (self.y - p[1])**2 <= r**2

		self.activator += mask*amount

		self.activator += np.random.rand(self.x_count, self.y_count) / 100
		np.clip(self.activator, a_min=0.0, a_max=1.0)

		pass

	def add_inhibitor(self, p = (0.0, 0.0), r = 1.0, amount = 1.0):
		"""
		Adds a circle of activation, by default in the middle.
		"""

		mask = (self.x - p[0])**2 + (self.y - p[1])**2 <= r**2

		self.inhibitor += mask*amount

		self.inhibitor += np.random.rand(self.x_count, self.y_count) / 100
		np.clip(self.inhibitor, a_min=0.0, a_max=1.0)

		pass