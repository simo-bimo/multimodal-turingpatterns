import numpy as np
from model import Model

class GrayScott(Model):
	def __init__(self, feed=0.055, decay=0.062, **kwargs):
		super().__init__(**kwargs)

		self.feed = feed
		self.decay = decay
		
		# Parameters for inhibitor
		self.Da = 1
		# Parameters for activator
		self.Dh = 0.5
		
		# Initialise to zeros
		self.set_activator(np.zeros((self.x_count, self.y_count)))
		self.set_inhibitor(np.zeros((self.x_count, self.y_count)))
		
		# Initialise all values to random variables to begin.
		# self.activator += np.random.rand(self.x_count, self.y_count) * 0
		# self.inhibitor += np.random.rand(self.x_count, self.y_count) * 0
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
	
	# def take_step(self, num=1):
	# 	for i in range(0, num):
	# 		delA = self.deltaA() * self.dt
	# 		delH = self.deltaH() * self.dt

	# 		self.activator += delA
	# 		self.inhibitor += delH

	# 		np.clip(self.activator, a_min=0.0, a_max=1.0)
	# 		np.clip(self.inhibitor, a_min=0.0, a_max=1.0)

	# 		# clip values near zero to zero.
	# 		self.activator[self.activator < self.zero_tol] = 0.0
	# 		self.inhibitor[self.inhibitor < self.zero_tol] = 0.0

	# 	self.curr_step+=num
	# 	pass

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